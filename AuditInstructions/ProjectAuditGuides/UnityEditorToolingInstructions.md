# Unity Editor tooling and asset-integrity audit

Load for custom tools, serialized changes, migrations, or asset-integrity review. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). `unity:unity-cli` owns safe Editor
execution (fallback: the Editor's own menus and batch mode); `unity:ui-uitk` / `unity:ui-imgui` own UI
implementation. Project asset-editing guardrails remain in `AGENTS.md`. **Last verified: October 2026.**

This lens has two parts. Run the [Integrity pass](#integrity-pass) for every whole-project audit and every
metadata-touching change. Load [Tool authoring](#tool-authoring) only when the project owns Editor tooling.

## Integrity pass

Always on for a whole-project audit and for any change that touches `.meta` files, serialized assets, or
renamed fields. Skip it for a change that touches none of those. It is read-only, combining static metadata checks with Editor-assisted reference/type checks.
Read metadata and serialized references as evidence, never hand-edit them. Account for ignored paths, packages,
deliberate optional references, and import state before calling something broken. List every affected
asset pair for a duplicate GUID, including vendor metadata when it participates in the same database.

Move-time GUID checks belong to [ReviewFolders](../FolderStructure/ReviewFolders.md). The settings that keep
`.meta` files visible and tracked belong to [ProjectSettings](../ProjectSettings/ProjectSettings.md) and
[SetupVersionControl](../VersionControl/SetupVersionControl.md); this pass checks metadata content.

| Check | How to inspect | Finding when |
|---|---|---|
| Duplicate GUIDs | `grep -rh "^guid:" --include='*.meta' Assets Packages \| sort \| uniq -d`, then grep each duplicate to list every `.meta` that holds it | Any `guid:` value appears in more than one `.meta` |
| Missing or orphan metadata | For each path under `Assets` and embedded `Packages` (scan only `Assets` and embedded `Packages`; skip folders ending in `~`, hidden folders whose name starts with `.`, and copies such as agent worktrees, `Library`, or build output), check `<path>.meta` exists; for each `.meta`, check its asset exists | An asset has no `.meta` after the Editor has imported the project, or a `.meta` has no asset; files added while the Editor was closed are not findings until it opens |
| Null or unresolved scripts | Grep saved scenes, prefabs, and assets for `m_Script: {fileID: 0}`; read one saved MonoBehaviour for the exact reference form, then resolve each script GUID against the project's `.meta` files | `m_Script` is `fileID: 0`, or a script GUID resolves to no `.meta` and no deliberate optional-package guard. Unity's built-in resource references (all-zero-prefix GUIDs such as `0000000000000000e000000000000000` and `0000000000000000f000000000000000`, used by built-in shaders, fonts, and materials) are expected and not findings; no official list of them was found, so confirm what a reference points to in the installed Editor before excusing it |
| Missing references | A `unity:unity-cli` Editor query for missing scripts and missing object references over scenes and prefabs (discover the installed command first) | A count above zero for any asset; each is a finding unless documented as optional. Needs a live Editor: record Not verified otherwise. Static fallback: every `guid:` referenced by first-party scenes, prefabs, and assets resolves to a `.meta` in scope (built-in references excepted); an unresolved GUID is a candidate missing reference |
| Managed-reference types | Hosts using `[SerializeReference]`; `SerializationUtility.HasManagedReferencesWithMissingTypes` in an Editor query | Required data has an unresolved managed type after namespace/class/assembly changes; preserve recoverable serialized data and diagnose the missing type before proposing a migration |
| Tracked generated content | `git ls-files Library Temp obj Logs UserSettings` | Any generated folder has tracked files |

## Tool authoring

Load only when the project owns Editor tooling: custom EditorWindows, Inspectors, or drawers, menu or batch
migrations, `OnValidate` or `InitializeOnLoad` code, or scripts that use Undo. Otherwise record Not applicable.
With many tools, sample by risk (tools that act on open scenes or prefab instances, or that write many assets) and state the sample instead of inspecting every file.

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Serialized identity | Diff of renamed or moved serialized fields, `FormerlySerializedAs` use, enum member lists, saved assets | A renamed field has no migration attribute or script while saved assets still hold the old name (grep the old name in `.asset`, `.prefab`, `.unity`), or an enum member's number changed and a saved asset reads back as a different member |
| Inspector edits | `SerializedObject` / `SerializedProperty`, `Update`, `ApplyModifiedProperties`, or binding | An Inspector writes `target` fields directly without those calls or without Undo, bypassing multi-object editing, prefab overrides, or Undo |
| Tool edits | `Undo.*` calls before each change, `SetDirty`, prefab-instance modification recording | A tool that acts on open scenes or prefab instances mutates an object with no `Undo.*` call before the change, or an Undo/Redo run leaves the change in place, or a prefab-instance edit is not recorded. A missing `Undo.` call is only a candidate elsewhere: batch tools that load, change, and save assets do not need it |
| Asset operations | `System.IO` and `AssetDatabase` calls on `Assets/` paths | A tool moves, copies, or deletes files under `Assets/` with `System.IO` instead of `AssetDatabase`, or a `.meta` pair is broken after it ran |
| Batch safety | `StartAssetEditing` / `StopAssetEditing` or `AssetDatabase.AssetEditingScope` | A `StartAssetEditing` has no matching `StopAssetEditing` in a guaranteed `finally`, or an `AssetEditingScope` is created outside a `using` statement without a guaranteed `Dispose` |
| Migration scope | Target filter, preview or dry-run mode, a second run on a throwaway copy, result log | The filter reaches unselected package or vendor content, there is no preview, a second run changes assets again (diff it), or completion is reported with no per-asset failure list |
| Editor callbacks | `OnValidate`, `InitializeOnLoad`, `InitializeOnLoadMethod`, reload hooks | `OnValidate` reaches a non-thread-safe operation, or initialization uses imported assets before they are available. File I/O/scans in `InitializeOnLoad` are cost/reload-safety candidates, not automatic defects |
| Serialization callbacks | `ISerializationCallbackReceiver` implementations and their helper calls | A callback reaches main-thread-only Unity APIs or depends on an undocumented ordering between managed-reference siblings; keep conversion local to owned fields |
| Saved result | `SetDirty`, `SaveAssets`, read-back after reload, git diff on a throwaway copy | A tool that must ship its change never calls `SetDirty`/`SaveAssets`, or the git diff is empty after the tool ran, or a reopened scene or prefab lacks the change |

## Cases worth explicit inspection

- ⚠️ `SerializedProperty` editing through ApplyModifiedProperties/binding already manages normal Undo
  and dirtying. Direct non-inspector edits need the appropriate Undo API before mutation, plus
  prefab-instance recording and scene/asset persistence appropriate to the object.
- ⚠️ Creation, component addition, hierarchy changes, and destruction may need specialized Undo APIs;
  `Undo.RecordObject` alone is not a complete transaction for every tool action.
- ⚠️ `FormerlySerializedAs` lets a renamed field keep its saved value
  ([reference](https://docs.unity3d.com/ScriptReference/Serialization.FormerlySerializedAsAttribute.html)).
  Unity's docs reviewed here do not describe enum numbering or when the attribute is safe to remove, so treat
  existing enum numbers as part of the saved format and prove changes with a read-back of saved assets.
  Removing migration support needs evidence that all supported content has migrated, not a time limit.
- ⚠️ `OnValidate` can run when scripts load or values change, including on threads other than the main
  thread. Keep it to validating the data that changed; schedule scene and asset operations through a safe
  Editor path.
- ⚠️ A migration should identify intended targets, record failures, avoid overwriting unsaved work,
  and distinguish already-correct content. Pause imports with `AssetDatabase.AssetEditingScope` in a `using`
  statement, or `StartAssetEditing` / `StopAssetEditing` inside `try`/`finally`; unbalanced calls leave
  imports paused ([reference](https://docs.unity3d.com/ScriptReference/AssetDatabase.AssetEditingScope.html)).
- ⚠️ When a result must be committed, inspect saved asset references and the diff. Reopen representative
  scenes/prefabs, including variants/overrides. A screenshot or runtime hierarchy proves only that state.

## Validation

For tools, exercise Undo/Redo, multi-selection if supported, prefab instances/variants, cancel/failure,
and rerun where applicable. Re-read saved output and verify GUID/reference identity after reload.
Do not save an unrelated dirty scene to make a tool check pass. Keep live-only or unopened assets
Not verified. Editor/player compilation boundaries belong in
[Assemblies](UnityAssemblyDefinitionsInstructions.md).

Technical reference: [OnValidate](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnValidate.html).

Serialization references: [missing managed types](https://docs.unity3d.com/ScriptReference/SerializationUtility.HasManagedReferencesWithMissingTypes.html)
and [callback threading/order](https://docs.unity3d.com/ScriptReference/ISerializationCallbackReceiver.html).

Initialization reference: [InitializeOnLoad asset availability](https://docs.unity3d.com/ScriptReference/InitializeOnLoadAttribute.html).
