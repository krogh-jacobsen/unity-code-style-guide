> How it works: give this URL to your agent, for example "Set up folders only in my Unity project
> from this document". The agent inspects the project, asks which features you need, creates only
> those folders, and reports what it verified. Human overview: [readme](readme.md).

# Set up project folders (agent instructions)

Scaffold the owned-content folders of a newly created Unity project. This document is
self-contained and creates directories only: presets, script templates, scenes, asmdefs, packages,
project settings, and copied guides are separate tasks. Use the tools you already have; install
no package, CLI, or setup script.

## Operating rules

- Create the selected missing directories and nothing else. Never generate `.meta` files, move,
  rename, or delete existing content, or create suffixed duplicates to dodge a conflict.
- The target project's own instructions take precedence over this document.
- Leave existing assets, instructions, and unsaved work untouched.
- When required instructions cannot be read, stop before creating anything rather than working
  from memory. Report the source URL or path you followed.
- Report folder creation and Unity import verification as two separate results.

## 1. Preflight

Identify the target: the user's destination, or the current workspace when it is exactly one Unity
project (it contains `Assets` and `ProjectSettings/ProjectVersion.txt`). Resolve an ambiguous
destination before writing. This starter repository is not a Unity project.

Inspect the existing folders under `Assets`, any established owned-content root, source-control
changes when available, and whether the project's Editor is open.

**Done:** the target project, local rules, existing folders, and Editor state are known.

## 2. Ask

Ask only what changes the result, in one short round. Apply the default when the user says
"use defaults".

| Question | Default |
|---|---|
| Owned-content root name? | An existing root if one is established; otherwise `Assets/{ProjectName}`, using the project directory's name |
| Which real features exist now, and what does each need next? | None: create the root alone |
| Project-wide `Scenes`, `Settings`, or `Shared`? | Only for a responsibility the user selects |
| `Tests/EditMode` and `Tests/PlayMode` folders? | No |
| `Resources`, `Plugins`, or `StreamingAssets`? | No: create only for an actual loading, plugin, or raw-content requirement |

**Done:** every selected directory has a stated purpose and a concrete path under the target `Assets`.

## 3. Choose the layout

Use this tree as a menu. Create only the selected branches; `Inventory` and its UI files are an
example feature, not scaffolding to copy.

```text
Assets/
├── ScriptTemplates/      # Selected .cs.txt files (separate task); must be a direct child of Assets
├── StreamingAssets/      # Optional raw player content; must be a direct child of Assets
├── ThirdPartyAssets/     # Vendor imports whose layout permits relocation
├── Settings/Presets/     # Selected import presets (separate task); a starter convention, not a Unity special folder
└── {ProjectName}/
    ├── SceneTemplates/   # Optional source scenes/templates and shared resources
    ├── Scenes/           # Bootstrap, composition, and other project-wide scenes
    ├── Settings/         # Project-wide URP, Input Actions, shared UI settings
    ├── Shared/           # Independent shared code and content
    └── Inventory/        # Example feature; create the real ones
        ├── Scenes/       # Optional feature-owned, test, or demo scenes
        ├── Scripts/
        ├── Editor/
        ├── Tests/        # Optional; EditMode/ and PlayMode/ subfolders
        ├── Data/         # Authored configuration assets
        ├── Prefabs/
        ├── Art/
        └── UI/           # UXML, USS, and C# for a screen together; Sprites/ for UI sprites
```

Apply these ownership rules when placing a folder:

- Put code, configuration, and content with the feature that owns its meaning, even when another
  feature consumes it. Multiple consumers alone do not make something shared.
- Use `Shared` only for content with an independent responsibility that depends on no feature
  implementation, through code or asset references.
- Use project-level `Scenes` and `Settings` for composition and configuration that spans features.
- Keep guides, build outputs, and validation reports outside `Assets`.
- Create `Resources` or `Plugins` only for an actual loading or plugin requirement, and honor
  platform-specific plugin paths.
- Defer `Assets/Settings/Presets` and `Assets/ScriptTemplates` to their own workflows.
- Folder creation does not configure test assemblies or asmdefs, and it does not create placeholder
  files or a permanent setup report to keep empty folders alive.

**Done:** the selected project-relative paths are listed and shown to the user. Continue within the
authorized scope; stop to ask only about unresolved choices or conflicts.

## 4. Check, then create

Check the complete path list before changing anything:

- Each name is a valid single directory segment on the target platform. Reject absolute names,
  separators, `.` and `..`, and case-only collisions with selected or existing paths.
- Every destination resolves inside the intended project's `Assets`. Do not create through a
  symlinked entry inside `Assets`.
- Reuse an existing directory with matching name and casing. A file at a requested directory path,
  or metadata for a missing directory, is a conflict to resolve before creating anything.

Choose the route by Editor state:

- **Editor closed:** create only the selected missing directories with ordinary filesystem
  operations. Unity generates their metadata on import.
- **Editor open:** use Editor access you already have (for example an `AssetDatabase` folder API),
  checking for each folder before creating it, and target the project explicitly. When no such
  access exists, ask the user to close that project's Editor. Never install a bridge or close an
  Editor with unsaved work.
- **Established project being reorganized:** stop. This document does not move existing content;
  see "Moving existing content" below.

If a failure interrupts creation, report the paths already created. A rerun must reuse them and
create only the remaining selected directories.

**Done:** each selected path is Created or Already present, with existing content and metadata unchanged.

## 5. Verify

- Read back every selected path and confirm it is a directory with the intended casing.
- Repeat the missing-folder check; it must find nothing to create.
- Compare before and after. Only the selected directories and Unity-generated folder metadata belong
  to this run. Preserve unrelated concurrent edits.
- After an observed Unity import, confirm that the new folders have generated metadata, GUIDs are
  unique, pre-existing metadata is unchanged, and the import log has no fresh errors. Open the project
  for import only when a safe route exists and doing so is within scope; otherwise mark the import
  checks **Not verified** and tell the user to open the project in Unity.
- Run no gameplay tests or player build for empty-folder scaffolding.

Empty directories may not survive source control. Commit Unity-generated metadata together with the
folders once it exists.

**Done:** directory verification passes, a repeat run has nothing to add, and the import result is
Verified or Not verified.

## 6. Report

| Item | Status | Detail |
|---|---|---|
| Target project, content root, source URL | | |
| Each selected path | Created / Already present / Conflict | Path |
| Missing-folder recheck | Passed / Failed | |
| Unity import and metadata | Verified / Not verified | Next action if pending |

Put unresolved conflicts and choices in a "Needs your decision" block at the top.

## Moving existing content

Reorganizing an established project is a separate task: use `AssetDatabase.MoveAsset` through the
Editor or CLI, or the Project window, and preserve GUIDs, references, prefab overrides, and vendor
layouts. Afterwards, check string-based loads such as `Resources.Load`, scoped import filters, and
each script's assembly membership; compile the Editor and a representative player; reopen affected
saved scenes and prefabs to confirm their references.

## References

- [Special folder names](https://docs.unity3d.com/Manual/SpecialFolders.html)
- [Assembly definitions](https://docs.unity3d.com/Manual/assembly-definitions-intro.html)
- [StreamingAssets](https://docs.unity3d.com/Manual/StreamingAssets.html)
