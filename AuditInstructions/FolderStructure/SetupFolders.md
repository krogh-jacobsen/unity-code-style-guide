> How it works: give this URL to your agent, for example "Set up folders only in my Unity project
> from this document". The agent audits the project, recommends the folders that fit, lets you pick
> which to carry over, and creates nothing until you confirm the exact list. Then it reports what it
> verified. Human overview: [readme](README.md).

# Set up project folders (agent instructions)

Scaffold the owned-content folders of a newly created Unity project. This document is
self-contained and creates directories only (plus `.gitkeep` markers in scaffold mode): presets,
script templates, scenes, asmdefs, packages, project settings, and copied guides are separate tasks.
Use the tools you already have; install no package, CLI, or setup script.
**Last verified: November 2026.**

Run it as the first step of project setup, before `.gitignore`, version control, and package work.
With vendor and sample content already inside `Assets/ThirdPartyAssets/`, the starter's
`Unity.gitignore` ThirdPartyAssets section excludes all of it with one rule, no per-vendor ignore
lines are needed, and the first commit holds only owned content. In one real setup the first
`git add` shrank from a 12 GB `Library` plus about 7 GB of vendor imports to 55 files (about
400 KB). That section is optional; where it is removed, the relocation still groups vendor content
but no longer keeps it out of the repository.

## Operating rules

- Create the selected missing directories, plus a `.gitkeep` file in each empty leaf folder in
  scaffold mode, and nothing else. Never generate `.meta` files, move, rename, or delete existing
  content, or create suffixed duplicates to dodge a conflict.
- Relocating existing content (vendor folders at the `Assets` root, for example) belongs to
  [ReviewFolders.md](ReviewFolders.md). Propose it as a ReviewFolders move batch in the same first
  step, rather than moving anything here.
- The target project's own instructions take precedence over this document.
- Leave existing assets, instructions, and unsaved work untouched.
- When required instructions cannot be read, stop before creating anything rather than working
  from memory. Report the source URL or path you followed.
- Report folder creation and Unity import verification as two separate results.

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

Identify the target: the user's destination, or the current workspace when it is exactly one Unity
project (it contains `Assets` and `ProjectSettings/ProjectVersion.txt`). Resolve an ambiguous
destination before writing. This starter repository is not a Unity project.

Inspect the existing folders under `Assets`, any established owned-content root, source-control
changes when available, and whether the project's Editor is open.

Look for what the Unity template left behind. Template-created projects arrive with a
`Assets/Settings` folder (its contents depend on the template, for example render pipeline and volume
settings) and often a sample scene and sample assets. List what exists by inspection, and do not
assume names. Reuse `Assets/Settings` as it stands; leave sample content in place and report it.

List vendor and sample folders that sit directly under `Assets` (Asset Store packs, demo scenes,
imported samples). Each one whose layout permits relocation becomes a proposed ThirdPartyAssets move
batch for [ReviewFolders.md](ReviewFolders.md), including its pre-move checks (a render pipeline
asset or other `ProjectSettings` dependency inside the vendor folder, hard-coded `Assets/` paths,
`Resources` folders). Record whether the target's `.gitignore` already has the ThirdPartyAssets
section.

Check the project's location. The full path and project name should contain no spaces, and the
project should sit close to the drive root on Windows: [reported path-length failures](https://discussions.unity.com/t/unity-editor-still-hits-windows-max-path-260-char-limit-even-with-longpathsenabled-any-real-fix/1732098)
hit IL2CPP and Android builds, and Unity publishes no safe limit. Warn the user when the path is long
instead of moving the project.

**Done:** the target project, local rules, existing folders, template leftovers, vendor folders at
the `Assets` root, path length, and Editor state are known, and nothing has been created.

## 2. Ask

Ask only what changes the result, in one short round. The defaults are recommended answers: they
become recommendations that still go through stages 3 and 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Owned-content root name? | An existing root if one is established; otherwise `Assets/{ProjectName}`, using the project directory's name |
| Mode: minimal or scaffold? | Minimal. Scaffold creates the full boilerplate tree in step 3, with `.gitkeep` markers, for a team that wants the convention visible from day one |
| Which real features exist now, and what does each need next? | Minimal: none, create the root alone. Scaffold: `FeatureExample` only, to copy and rename |
| Project-wide `Scenes`, `Settings`, `Shared`, or `SceneTemplates`? | Minimal: only for a responsibility the user selects. Scaffold: all four |
| `Tests/EditMode` and `Tests/PlayMode` folders? | Minimal: no. Scaffold: inside `FeatureExample` |
| Vendor or sample folders at the `Assets` root? | Propose moving each into `Assets/ThirdPartyAssets/` through ReviewFolders.md in this same step, when its layout permits relocation |
| `Resources`, `Plugins`, or `StreamingAssets`? | No: create only for an actual loading, plugin, or raw-content requirement |
| Extra feature subfolders (`Audio`, `Animations`, `VFX`, `Materials`)? | None: add per feature when content of that kind exists |
| Keep source art files (PSD, Blend, and similar) in the project? | No. When yes, use a project-root `ArtSource` folder beside `Assets`, outside the import pipeline |
| Reusable code to share across projects? | No. A local package is a separate task, not part of folder scaffolding |
| Sample content from the template? | Leave it in place and report it |

**Done:** every proposed directory has a stated purpose and a concrete path under the target `Assets`,
or is the explicitly selected project-root `ArtSource` beside `Assets`.

## 3. Choose the layout

In minimal mode, use this tree as a menu: each branch that fits the project becomes a numbered
recommendation, with its purpose and risk, and `FeatureExample` stands for the real features. In
scaffold mode, the boilerplate set below is one recommendation.

```text
ArtSource/                # Optional, beside Assets: PSD, Blend, and other source files Unity should not import
Packages/                 # Unity-managed; embedded packages live here (separate task)
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
    └── FeatureExample/   # Example feature; copy and rename it for each real one
        ├── Scenes/       # Optional feature-owned, test, or demo scenes
        ├── Scripts/
        ├── Editor/
        ├── Tests/        # Optional; EditMode/ and PlayMode/ subfolders
        ├── Data/         # Authored configuration assets
        ├── Prefabs/
        ├── Art/          # Models, textures, materials; add Audio/, Animations/, VFX/ when used
        └── UI/           # UXML, USS, and C# for a screen together; Sprites/ for UI sprites
```

### Scaffold mode

Scaffold mode creates exactly this set under the owned-content root, and nothing from the optional
branches above (`ArtSource`, `StreamingAssets`, `ScriptTemplates`, `Settings/Presets`):

```text
{ProjectName}/SceneTemplates/  Scenes/  Settings/  Shared/
{ProjectName}/FeatureExample/Scenes/  Scripts/  Editor/  Data/  Prefabs/  Art/  UI/
{ProjectName}/FeatureExample/Tests/EditMode/  Tests/PlayMode/
```

`Art/Audio`, `Art/Animations`, `Art/VFX`, and `UI/Sprites` stay out: add them when content of that
kind exists. Add `Assets/ThirdPartyAssets/` when vendor content is being relocated.

Put an empty `.gitkeep` file in every leaf folder that has no other content. Git tracks the folder's
`.meta` file but not an empty folder, and on a clean clone Unity treats `Foo.meta` with no `Foo/` as
orphaned and deletes it, so an unmarked scaffold silently disappears. Unity ignores dot-prefixed
files, so `.gitkeep` gets no `.meta` and does not show in the Project window. A `.gitkeep` can be
deleted once the folder holds real content.

### Naming and ownership

Name every folder you create in PascalCase, with no spaces and consistent casing. Do not start a
name with a dot: the Editor's create menu turns a leading dot into an underscore, and Unity ignores
dot-prefixed folders when importing. Unity also ignores folders ending in `~` and folders named
`cvs`, so use that suffix only when you intend the contents to stay out of the project (for example
`Documentation~`). Keep nesting shallow: aim for at most four levels below the owned-content root.
Those naming and nesting limits are this guide's recommendations, not Unity requirements.

Apply these ownership rules when placing a folder:

- Put code, configuration, and content with the feature that owns its meaning, even when another
  feature consumes it. Multiple consumers alone do not make something shared.
- Use `Shared` only for content with an independent responsibility that depends on no feature
  implementation, through code or asset references.
- Use project-level `Scenes` and `Settings` for composition and configuration that spans features.
- Keep guides, build outputs, and validation reports outside `Assets`.
- Create `Resources` or `Plugins` only for an actual loading or plugin requirement, and honor
  platform-specific plugin paths. Custom Android Gradle templates and a custom main manifest
  belong in `Assets/Plugins/Android/`; Unity generates them when the matching Publishing Settings
  option is enabled, so enable the option instead of creating the files by hand. See the
  [mobile build setup](../BuildSettings/MobileBuilds.md).
- Keep reusable cross-project code out of `Shared`. Unity's custom-package layout (a folder with a
  `package.json`, plus `Runtime`, `Editor`, and `Tests`) in `Packages/` is the supported home for it;
  do not create `package.json` files in this workflow.
- Keep source art in `ArtSource`, beside `Assets`, instead of importing it.
- Defer `Assets/Settings/Presets` and `Assets/ScriptTemplates` to their own workflows.
- Folder creation does not configure test assemblies or asmdefs, and it does not create a permanent
  setup report. In minimal mode it creates no placeholder files, because every folder is about to
  receive content; scaffold mode's `.gitkeep` markers are the only exception.

**Done:** the recommended project-relative paths are listed and shown to the user, who has picked a
subset and confirmed it in stage 4. Stop to ask about unresolved choices or conflicts.

## 4. Check, then create

Only the items confirmed in stage 4 are created. Check the complete confirmed path list before
changing anything:

- Each name is a valid single directory segment on the target platform. Reject absolute names,
  separators, `.` and `..`, and case-only collisions with selected or existing paths.
- Every destination resolves inside the intended project's `Assets`, or is the selected project-root
  `ArtSource`. Do not create through a symlinked entry inside `Assets`.
- Reuse an existing directory with matching name and casing. A file at a requested directory path,
  or metadata for a missing directory, is a conflict to resolve before creating anything.

Choose the route by destination, scope, and Editor state:

- **Project-root ArtSource only:** after exact confirmation, create the selected missing directory
  with ordinary filesystem operations. It stays outside Unity import regardless of Editor state.
- **New-project Assets scaffolding, Editor closed:** create only the selected missing directories
  with ordinary filesystem operations. Unity generates their metadata on import.
- **Editor open:** use existing Editor access (for example `AssetDatabase.CreateFolder`) for selected
  imported folders, checking each path first and targeting the project explicitly. One route that
  worked: with the Unity CLI connected to the open Editor, a `command eval` call ran C# that created
  the folders and returned the results. Discover the installed CLI's commands rather than copying
  this one. If no route is available, defer creation or ask for a safe closed-Editor route for
  new-project scaffolding. Never install a bridge or close an Editor with unsaved work.
- **`.gitkeep` markers (scaffold mode):** write them with ordinary filesystem operations after the
  folders exist, whatever the Editor state. Unity does not import dot-prefixed files, so no metadata
  is involved.
- **Established project Assets changes:** continue read-only inventory, then route imported-folder
  additions or reorganization to [ReviewFolders.md](ReviewFolders.md) for an Editor-owned plan.
  An existing owned root alone does not imply reorganization, and does not block a specifically
  selected project-root ArtSource proposal. This workflow never moves existing content; vendor
  relocation into `Assets/ThirdPartyAssets/` runs as a ReviewFolders.md batch in the same first step,
  after the target folder exists.

If a failure interrupts creation, report the paths already created. A rerun must reuse them and
create only the remaining selected directories.

**Done:** the audit and recommendation list were shown and confirmed before any change, and each
confirmed path is Created or Already present, with existing content and metadata unchanged.

## 5. Verify

- Read back every selected path and confirm it is a directory with the intended casing.
- In scaffold mode, every leaf folder without other content holds a `.gitkeep`, and no `.gitkeep`
  has a `.meta`.
- Repeat the missing-folder check; it must find nothing to create.
- Compare before and after. Only the selected directories and Unity-generated folder metadata belong
  to this run. Preserve unrelated concurrent edits.
- After an observed Unity import, confirm that the new folders under `Assets` have generated
  metadata (folders ending in `~` and `ArtSource` get none, by design), GUIDs are unique, pre-existing metadata is unchanged, and the import log has no fresh errors. Open the project
  for import only when a safe route exists and doing so is within scope; otherwise mark the import
  checks **Not verified** and tell the user to open the project in Unity.
- Run no gameplay tests or player build for empty-folder scaffolding.

Empty directories do not survive source control. Commit Unity-generated metadata together with the
folders once it exists; in minimal mode, commit each folder once it holds content.

**Done:** directory verification passes, a repeat run has nothing to add, and the import result is
Verified or Not verified.

## 6. Report

| Item | Status | Detail |
|---|---|---|
| Target project, content root, source URL | | |
| Audit and recommendations shown, confirmation received | Yes / Stopped before confirming | Items picked |
| Unpicked recommendations | Proposal | Path and reason |
| Template leftovers (`Assets/Settings`, sample content) | Reused / Left in place | What exists |
| Project path | OK / Warned | Length and spaces |
| Mode | Minimal / Scaffold | `.gitkeep` count in scaffold mode |
| Each selected path | Created / Already present / Conflict | Path |
| Vendor relocation | Proposed for ReviewFolders.md / None needed | Folders at the `Assets` root |
| Missing-folder recheck | Passed / Failed | |
| Unity import and metadata | Verified / Not verified | Next action if pending |

Put unresolved conflicts, unpicked recommendations that need a ruling, and open choices in a
"Needs your decision" block at the top.

## References

- [Special folder names](https://docs.unity3d.com/Manual/SpecialFolders.html)
- [Default project directories](https://docs.unity.com/en-us/engine/6000.6/manual/get-started/project-configuration/default-directories)
- [Custom package layout](https://docs.unity3d.com/Manual/cus-layout.html)
- [Organizing your Unity project](https://unity.com/how-to/organizing-your-project)
- [Assembly definitions](https://docs.unity3d.com/Manual/assembly-definitions-intro.html)
- [StreamingAssets](https://docs.unity3d.com/Manual/StreamingAssets.html)
