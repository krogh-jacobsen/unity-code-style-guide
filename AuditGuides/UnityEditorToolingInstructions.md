# Unity Editor tooling and asset-integrity audit

Load for custom tools, serialized changes, migrations, or asset-integrity review. Apply the
[shared evidence standard](README.md#evidence-standard). `unity-cli` owns safe Editor execution;
`ui-uitk` / `ui-imgui` own UI implementation. Project asset-editing guardrails remain in `AGENTS.md`.

## Integrity before style

Read metadata and serialized references for evidence without hand-editing them. Inspect duplicate
or malformed GUIDs, missing/orphaned metadata, missing scripts/references, and tracked generated
content. Account for ignored paths, packages, deliberate optional references, and import state before
calling something broken. List every affected asset pair for duplicate GUIDs, including vendor
metadata when it participates in the same database.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Serialized identity | Relevant diffs, GUIDs, field/type/enum migrations | Existing content loses identity or silently maps to different values |
| Inspector edits | SerializedObject/Property, Update/Apply or binding | Direct target edits bypass multi-object editing, prefab overrides, or Undo |
| Tool edits | Undo-before-change, dirty state, prefab modifications | Changes cannot be undone or do not persist on the correct scene/asset |
| Asset operations | Move/delete/create/load paths and metadata | A tool bypasses AssetDatabase or leaves references/metadata inconsistent |
| Batch safety | Start/StopAssetEditing and failure paths | Exceptions leave editing/import state locked or a partial migration unreported |
| Migration scope | Search boundaries, preview, idempotence, result validation | A tool edits vendor/unrelated assets, cannot be rerun safely, or reports completion from counts alone |
| Editor callbacks | OnValidate, InitializeOnLoad, reload hooks | Heavy, destructive, or thread-unsafe work runs during import/validation/reload |
| Saved result | Read-back, reopen/reload, scene/prefab variants, source control diff | A successful live change never reaches the asset that must ship |

## Cases worth explicit inspection

- `SerializedProperty` editing through ApplyModifiedProperties/binding already manages normal Undo
  and dirtying. Direct non-inspector edits need the appropriate Undo API before mutation, plus
  prefab-instance recording and scene/asset persistence appropriate to the object.
- Creation, component addition, hierarchy changes, and destruction may need specialized Undo APIs;
  `Undo.RecordObject` alone is not a complete transaction for every tool action.
- Preserve serialized field names with migration attributes where required. Enum compatibility
  depends on stable numeric values; retain existing assignments when adding/restructuring values.
  Removing migration support needs evidence all supported content has migrated, not a time limit.
- `OnValidate` may run during loading and off the main thread. Keep it to local data validation;
  schedule scene/asset operations through a safe Editor path.
- A migration should identify intended targets, record failures, avoid overwriting unsaved work,
  and distinguish already-correct content. Pair batch API cleanup in `finally` where used.
- When a result must be committed, inspect saved asset references and the diff. Reopen representative
  scenes/prefabs, including variants/overrides. A screenshot or runtime hierarchy proves only that state.

## Validation

For tools, exercise Undo/Redo, multi-selection if supported, prefab instances/variants, cancel/failure,
and rerun where applicable. Re-read saved output and verify GUID/reference identity after reload.
Do not save an unrelated dirty scene to make a tool check pass. Keep live-only or unopened assets
Not verified. Editor/player compilation boundaries belong in
[Assemblies](UnityAssemblyDefinitionsInstructions.md).

Technical reference: [OnValidate restrictions](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.OnValidate.html).
