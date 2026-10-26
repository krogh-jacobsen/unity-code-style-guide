> How it works: give this URL to your agent, for example "Review my current folder structure
> against this guide and recommend what and how to improve", or add "and move things in small,
> verified batches" to reorganize. The agent audits first and recommends, you pick what to carry
> over, and nothing moves before you confirm the exact change list. Human overview: [readme](README.md).

# Review and reorganize an existing project's folders (agent instructions)

Compare a project that already has content and its own folder structure against the layout below,
recommend improvements, and, only when the user opts in, move content in small reversible batches.
This document is self-contained. For a brand-new project, use [SetupFolders.md](SetupFolders.md)
instead. **Last verified: October 2026.**

## Operating rules

- Start in **review** mode: read and report only. Move nothing until the user has picked items and
  confirmed the exact batch list (stages 3 and 4 below).
- Move imported assets only through Editor APIs (`AssetDatabase.ValidateMoveAsset`, then
  `AssetDatabase.MoveAsset`) or the Project window. Unity ties references to the GUID in each
  `.meta` file, and moving files outside the Editor risks disconnecting the GUID from the file.
  Treat a non-empty string returned by `MoveAsset` as a failure and stop.
- Take a checkpoint before every batch (a clean commit, or a stash the user agrees to) so a batch can
  be undone. If the working tree is dirty with the user's own work, ask before continuing.
- Leave `Packages/`, `ProjectSettings/`, and vendor content with a required layout where they are.
- Keep a move log (old path, new path, GUID) in the conversation; it is the rollback record.
- Stop at the first error, compile failure, or unexpected change. Report it; never push through.
- Mark checks you cannot run **Not verified**.

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit user confirmation.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Present the exact changes for the picked subset (files, settings, values, commands)
   and obtain explicit user authorization before making them, including saving the report.
   Confirmation need not contain the literal word "yes": after the concrete scope is presented,
   "implement R1 and R3" can both select and confirm those items. Selection alone ("R1 and R3")
   chooses scope without authorizing implementation. Honor existing authorization for unchanged
   scope without asking again; clarify a delayed reply only when its scope is materially ambiguous.
   Resolve IDs against the presented change list rather than guide defaults. If evidence establishes
   that exact scope was previously presented and authorized but its record is now unavailable,
   retrieve that record before execution; recovered unchanged scope needs no repeat confirmation.
   If concrete changes were never presented, an instruction to implement an ID leaves scope
   unconfirmed: first present the exact changes and obtain confirmation before execution.
   Changed scope needs confirmation for the changed items. In a non-interactive session, or when
   authorization is absent, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

## 1. Preflight

Read the project's own instructions first; they win over this document. Then record:

- Editor version and whether the Editor is open. Moves need the Editor (or an Editor-driven CLI
  command); a review alone can read the files directly.
- Source-control state, and whether the project compiles cleanly now. Do not start moves on a
  project with compile errors.
- Test baseline: the project's tests pass, or the failures that already exist, listed.
- The `Assets` tree to three levels, with file counts and the longest asset path.
- Template leftovers (`Assets/Settings`, sample scene and assets), vendor folders (Asset Store or
  package-style content with its own layout), and any `Resources`, `StreamingAssets`, `Plugins`,
  `Editor`, or `Gizmos` folders and where they sit.
- Assembly definitions and references, and each script's effective assembly.

**Done:** the inventory and baseline exist, you can state which parts you will treat as vendor, and
nothing has been changed.

## 2. Ask

Ask in one batch. The defaults are recommended answers that still need stages 3 and 4, even when the
user says "use defaults".

| Question | Default |
|---|---|
| Review only, or also reorganize? | Review only |
| Whole project or specific folders or features? | Whole `Assets`, owned content only |
| Adopt the whole layout or only parts? | Parts: keep the project's convention where it is consistent, and fix inconsistencies |
| Move scripts and asmdefs? | No: propose them, move only after separate approval |
| Move path-dependent content (`Resources`, Addressables, `StreamingAssets`)? | No |
| Checkpoint method (commit or stash)? | Commit |

**Done:** the mode and scope are agreed and repeated back in one line each.

## 3. Review against the layout

The target layout, as a menu rather than a mandate:

```text
ArtSource/                # Optional, beside Assets: PSD, Blend, other source files
Packages/                 # Reusable code as embedded packages
Assets/
├── ScriptTemplates/  StreamingAssets/  ThirdPartyAssets/   # direct children when used
├── Settings/Presets/     # Import presets (the starter's convention)
└── {ProjectName}/
    ├── Scenes/  Settings/  Shared/  SceneTemplates/
    └── {Feature}/        # Scenes, Scripts, Editor, Tests, Data, Prefabs, Art, UI
```

Check each area, citing a path as evidence for every finding:

| Area | Look for |
|---|---|
| Organization | Type-first folders (`Scripts`, `Prefabs` at the root) instead of feature-first; duplicate or ambiguous roots (`Scripts` and `Code`); loose assets in the `Assets` root |
| Naming | Spaces, mixed casing, case-only duplicates, dot-prefixed names (Unity skips them on import), accidental `~` suffixes |
| Depth and paths | Nesting beyond about four levels below the content root; very long asset paths |
| Ownership | Content under a feature that other features own, and `Shared` content that depends on feature code or assets; dependency cycles between features |
| Special folders | `StreamingAssets` or `ScriptTemplates` not direct children of `Assets`; `Resources` used for convenience instead of a loading need; `Plugins`, `Editor`, or `Gizmos` placed where they change compilation or behavior |
| Assemblies | Scripts outside any intended asmdef; `Editor` folders inside runtime asmdefs without Editor-only assemblies; test asmdefs that cannot reference production assemblies |
| Vendor content | Vendor files mixed with owned content; vendor files modified in place |
| Source art | PSD, Blend, or other source files inside `Assets` |
| Template leftovers | Unused sample scenes and assets |

Rate each finding **Risk** (likely to cause bugs or build failures), **Improve** (clear benefit), or
**Optional** (taste), and give its **move risk** from the next table.

### Move risk

Moves are safe when only GUIDs refer to the asset, and dangerous where a path, folder name, or
folder position carries meaning.

| Move risk | Content | Why |
|---|---|---|
| Low | Prefabs, materials, textures, models, audio, ScriptableObject assets, UI files, and scenes, moved between ordinary folders | Unity references them by GUID, and the Editor moves the `.meta` file with the asset |
| Medium | Scripts, asmdefs, asmrefs, and anything moved into or out of an `Editor`, `Plugins`, or `Standard Assets` folder | Folder position selects the compile phase and assembly, and an asmdef covers the whole folder tree beneath it, so a move can change which assembly a script belongs to |
| High | `Resources` contents, Addressables, `StreamingAssets` contents, hard-coded `"Assets/..."` strings, import presets and postprocessors scoped by path, CI and `.gitignore` or LFS patterns | Their meaning depends on the path text. Unity's Addressables default address is the asset path, so a moved asset's address can change |
| Leave | `Packages/`, `ProjectSettings/`, vendor content with a required layout, template-created `Assets/Settings`, `Editor Default Resources`, and the special folders themselves | Unity or the vendor expects them where they are |

Before rating anything Medium or High, search the project for `Resources.Load`, hard-coded `Assets/`
paths, Addressables addresses, and path-scoped presets, and record what you find.

**Done:** every finding has evidence, a severity, and a move risk, and every High item has the
code or configuration that depends on it listed. The findings are the audit stage's output.

## 4. Recommend and plan

Present the review: a short summary, the findings table, and what to leave alone, with each finding
as a numbered recommendation (ID, evidence, proposed change, risk, default). Then offer a plan
only if the user asked to reorganize, as ordered batches:

1. Create missing target folders (follow the naming rules: PascalCase, no spaces, no leading dot).
2. Rename and case fixes. On a case-insensitive file system, move a case-only rename through a
   temporary name, and check the result in the Editor.
3. Low-risk content, one feature at a time.
4. Scripts and asmdefs, one assembly at a time (only if approved).
5. High-risk items, only on explicit request and with a stated verification for each.

Each batch lists its moves (old path → new path), the expected effect, the risk, the checks that
prove it, and how to undo it. Keep batches small enough to review: one feature or one assembly.

**Done:** the user has picked specific recommendations and confirmed the exact batches in stage 4,
or chosen review only. The per-batch checkpoints in step 5 stay as extra safety on top of that gate.

## 5. Apply one batch at a time

Only the items confirmed in stage 4 are moved. For each confirmed batch:

1. Checkpoint, then run `ValidateMoveAsset` for every move; resolve any non-empty result first.
2. Move through `MoveAsset`, requiring an empty return each time. Run `AssetDatabase.SaveAssets` and
   `Refresh`, and wait for compilation to finish.
3. Verify (step 6). On success, commit the batch with the move log in the message.
4. On any failure, undo the batch by moving the assets back through `MoveAsset` using the move log.
   If the Editor state is unreliable, close it and restore the checkpoint with source control.

**Done:** the audit and recommendation list were shown and confirmed before batch 1, and the batch is
committed with verification passed, or fully undone with the cause reported.

## 6. Verify each batch

- Every moved asset keeps its GUID (`AssetDatabase.AssetPathToGUID` before and after).
- The project compiles with no new errors, and each moved script's effective assembly is unchanged
  (compare before and after, for example with `CompilationPipeline.GetAssemblyNameFromScriptPath`).
- Open the scenes and prefabs of the affected features: no missing references or scripts.
- The build scene list still points at existing scenes. Check it; do not assume it updated.
- The project's tests pass, matching the baseline, and Play Mode starts the affected scenes.
- Path-dependent items found in step 3 still resolve: `Resources.Load` names, string paths,
  Addressables addresses, preset and postprocessor filters, CI and ignore patterns.
- After script or assembly batches, a build for a representative player target compiles.

**Done:** each check is Passed, Failed, or Not verified, and any failure has been undone or fixed.

## 7. Report

| Item | Status | Detail |
|---|---|---|
| Each finding | Risk / Improve / Optional | Path, evidence, recommendation, move risk |
| Unpicked recommendations | Proposal | ID and reason left open |
| Each batch | Applied / Undone / Not started | Moves, commit, checks |
| Each check | Passed / Failed / Not verified | Evidence |
| Left alone | Vendor / Leave | Path and reason |

Put open questions, unpicked recommendations that need a ruling, and failed checks in a
"Needs your decision" block at the top.

## References

- [Special folders and script compilation order](https://docs.unity3d.com/Manual/SpecialFolders.html)
- [AssetDatabase.MoveAsset](https://docs.unity3d.com/ScriptReference/AssetDatabase.MoveAsset.html)
- [Assembly definition references](https://docs.unity3d.com/Manual/assembly-definitions-referencing.html)
- [Custom package layout](https://docs.unity3d.com/Manual/cus-layout.html)
- [Organizing your Unity project](https://unity.com/how-to/organizing-your-project)
