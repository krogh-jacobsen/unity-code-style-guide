> How it works: give this URL to your agent, for example "Set up folders only in my Unity project
> from this document". The agent audits the project, recommends the folders that fit, lets you pick
> which to carry over, and creates nothing until you confirm the exact list. Then it reports what it
> verified. Human overview: [readme](README.md).

# Set up project folders (agent instructions)

Scaffold the owned-content folders of a newly created Unity project. This document is
self-contained and creates directories only (plus `.gitkeep` markers in scaffold mode): presets,
script templates, scenes, asmdefs, packages, project settings, and copied guides are separate tasks.
Use the tools you already have; install no package, CLI, or setup script.
**Last verified: 17 November 2026.**

Run it as the first step of project setup, before `.gitignore`, version control, and package work.
With vendor content already inside `Assets/ThirdPartyAssets/`, the starter's optional
`Unity.gitignore` ThirdPartyAssets section excludes all of it with one rule, and the first commit
holds only owned content.

## Operating rules

- Create the selected missing directories, plus a `.gitkeep` file in each empty leaf folder in
  scaffold mode, and nothing else. Never generate `.meta` files, move, rename, or delete existing
  content, or create suffixed duplicates to dodge a conflict.
- Relocating existing content (vendor folders at the `Assets` root, for example) belongs to
  [ReviewFolders.md](ReviewFolders.md). Propose it as a ReviewFolders move batch in the same first
  step, rather than moving anything here.
- The target project's own instructions take precedence over this document. A recorded project
  choice (for example "no asmdefs") is respected: report what it implies, and recommend no reversal.
- For a brand-new project with no owned content, the audit, recommendations, and exact change list
  may go in one message; stage 4 confirmation still comes before any write.
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
   and obtain explicit user authorization before making them, including saving the report. Give
   each change its undo: a commit checkpoint, a backup copy of a settings file, a log of moves, or
   the trash instead of a permanent delete.
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

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. Any
change outside the confirmed list, however small or obviously helpful (an extra `.gitkeep`, a
related setting), is a new recommendation: it returns to stage 3 before it is made. Noting it in a
report is not confirmation.

## 1. Preflight

Identify the target: the user's destination, or the current workspace when it is exactly one Unity
project (it contains `Assets` and `ProjectSettings/ProjectVersion.txt`). Resolve an ambiguous
destination before writing. This starter repository is not a Unity project.

Inspect the existing folders under `Assets`, any established owned-content root, source-control
changes when available, and whether the project's Editor is open.

List what the Unity template left behind, by inspection: an `Assets/Settings` folder (contents vary
by template), often a sample scene and assets, and sometimes assets loose at the `Assets` root (a
volume profile, pipeline global settings). Reuse `Assets/Settings` as it stands and leave the rest in
place, reported; moving loose root assets into `Assets/Settings` is a low-risk ReviewFolders.md
recommendation.

Vendor folders directly under `Assets` (Asset Store packs, demo scenes) whose layout permits
relocation become proposed ThirdPartyAssets move batches for [ReviewFolders.md](ReviewFolders.md),
with its pre-move checks. Record whether the target's `.gitignore` has the ThirdPartyAssets
section. Tool-owned roots that a tool or package placed at the `Assets` root (`TextMesh Pro`, package
`Samples`, and similar) stay where the tool expects them: report them and propose no move. Report
generated folders such as `_Recovery` (scenes the Editor recovers after a crash) and tool `Temp`
folders, and point to the [version control workflow](../VersionControl/SetupVersionControl.md) for
their ignore rules; create nothing for them.

Check the project's location. The full path and project name should contain no spaces, and the
project should sit close to the drive root on Windows: [reported path-length failures](https://discussions.unity.com/t/unity-editor-still-hits-windows-max-path-260-char-limit-even-with-longpathsenabled-any-real-fix/1732098)
hit IL2CPP and Android builds, and Unity publishes no safe limit. Warn the user when the path is long
instead of moving the project.

**Done:** the target project, local rules, existing folders, template leftovers, vendor, tool-owned,
and generated folders at the `Assets` root, path length, and Editor state are known, and nothing has
been created.

## 2. Ask

Ask only what changes the result, in one short round. The defaults are recommended answers: they
become recommendations that still go through stages 3 and 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Owned-content root name? | An existing root if one is established; otherwise `Assets/{ProjectName}`, using the project directory's name |
| Is there a reusable framework layer in addition to the game? | No: one root. Yes: a core root beside the game root (see [Layered roots](#layered-roots)) |
| Mode: minimal or scaffold? | Minimal. Scaffold creates the full boilerplate tree in step 3, with `.gitkeep` markers, for a team that wants the convention visible from day one |
| Which real features exist now, and what does each need next? | Minimal: none, create the root alone. Scaffold: `FeatureExample` only, to copy and rename |
| Project-wide `Scenes`, `Settings`, `Shared`, or `SceneTemplates`? | Minimal: only for a responsibility the user selects. Scaffold: all four |
| Where do tests live? | Nowhere yet: create no `Tests` folders. (a) Per feature `Tests/EditMode` and `Tests/PlayMode`, which need test asmdefs (a separate task). (b) One central `Assets/Editor/Tests/<Area>` for EditMode tests without asmdefs |
| Vendor folders at the `Assets` root? | Move each relocatable one into `Assets/ThirdPartyAssets/` through ReviewFolders.md, in this step |
| `Resources`, `Plugins`, or `StreamingAssets`? | No: create only for an actual loading, plugin, or raw-content requirement |
| Extra feature subfolders (`Audio`, `Animations`, `VFX`, `Materials`)? | None: add per feature when content of that kind exists |
| Keep source art files (PSD, Blend, and similar) in the project? | No. When yes, use a project-root `ArtSource` folder beside `Assets`, outside the import pipeline |
| Reusable code to share across projects? | No. A local package is a separate task |

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
├── Editor/Tests/         # Tests option (b): central EditMode tests, one subfolder per area
├── {CoreName}/           # Optional core root: the reusable framework layer, laid out like the game root
└── {ProjectName}/
    ├── SceneTemplates/   # Optional source scenes/templates and shared resources
    ├── Scenes/           # Bootstrap, composition, and other project-wide scenes
    ├── Settings/         # Game configuration: Input Actions, shared UI, owned pipeline assets
    ├── Shared/           # Independent shared code and content
    └── FeatureExample/   # Example feature; copy and rename it for each real one
        ├── Scenes/       # Optional feature-owned, test, or demo scenes
        ├── Scripts/
        ├── Editor/
        ├── Tests/        # Tests option (a) only; EditMode/ and PlayMode/ subfolders
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
```

`Art/Audio`, `Art/Animations`, `Art/VFX`, and `UI/Sprites` stay out: add them when content of that
kind exists. Add `Assets/ThirdPartyAssets/` when vendor content is being relocated. Add
`FeatureExample/Tests/EditMode` and `Tests/PlayMode` only for tests option (a), and `Editor/Tests`
only for option (b); every test folder created has a way to run.

Put an empty `.gitkeep` file in every leaf folder that has no other content. Git tracks the folder's
`.meta` but not an empty folder, and on a clean clone Unity deletes `Foo.meta` when `Foo/` is
missing, so an unmarked scaffold silently disappears. Unity ignores dot-prefixed files, so
`.gitkeep` gets no `.meta` and stays out of the Project window. Delete it once the folder has content.

### Layered roots

A reusable framework layer gets its own owned root beside the game root (in one mature project,
`_StrategyCore` and `_RailroadTycoon`), laid out like `{ProjectName}`.

- Dependencies run one way: the game root may reference the core root; the core root references
  no game-root code, asset, or feature.
- Generic, reusable behaviour goes in core; game-specific content and tuning go in the game root.
- A feature name exists in one root only, unless the report states the reason (for example a core
  `Audio` system and the game's `Audio` content).
- Without asmdefs the direction is a convention, enforced by the core-reference check in
  [ReviewFolders.md](ReviewFolders.md); asmdefs would enforce it at compile time (a separate task).
- The core root inside `Assets` is the accepted interim; move it to a package (a separate task) once
  a second project needs it.

### Naming and ownership

Name every folder you create in PascalCase, with no spaces and consistent casing. An owned root may
start with one underscore (`_Core`, `_Game`) so it sorts above vendor and tool folders in the Project
window; that is a choice, not a requirement. Start no name with a digit: keep `ThirdPartyAssets`
rather than `3rdPartyAssets`, which the starter's ignore rule would also miss. Report an existing
differing name as a recommendation; renaming belongs to ReviewFolders.md. Do not start a
name with a dot: the Editor's create menu turns a leading dot into an underscore, and Unity ignores
dot-prefixed folders when importing. Unity also ignores folders ending in `~` and folders named
`cvs`; use the suffix only for contents meant to stay out of the project (`Documentation~`). Keep nesting shallow: aim for at most four levels below the owned-content root.
Those naming and nesting limits are this guide's recommendations, not Unity requirements.

Apply these ownership rules when placing a folder:

- Put code, configuration, and content with the feature that owns its meaning, even when another
  feature consumes it. Multiple consumers alone do not make something shared.
- Use `Shared` only for content with an independent responsibility that depends on no feature
  implementation, through code or asset references.
- Put game-wide content that no single feature owns (environment art, terrain and world data,
  animation sets, editor tools) in plainly named folders under the owning root (`Environment`,
  `Terrains`, `Tools`). It references no feature code. `Shared` holds independent code and content
  with its own responsibility; these folders are the game's content library, grouped by kind.
- Use project-level `Scenes` for composition that spans features. `Settings` has three levels:
  `Assets/Settings` holds what the template created (pipeline and volume assets), reused in place;
  `{CoreName}/Settings` holds framework defaults; `{ProjectName}/Settings` holds game configuration
  (Input Actions, shared UI settings, pipeline assets the project owns beyond the template's).
- Keep guides, plans, build outputs, and validation reports outside `Assets`, in a project-root
  `Docs/` folder (or a folder ending in `~`). Text files inside `Assets` import as TextAssets. One
  short `README.md` per root or feature, stating its purpose and dependency direction, is the
  exception; writing them is a separate task.
- Create `Resources` or `Plugins` only for an actual loading or plugin requirement, and honor
  platform-specific plugin paths (Android build files: see the
  [mobile build setup](../BuildSettings/MobileBuilds.md)). Everything in a `Resources` folder ships in
  the player build, so list each one in the report.
- Keep reusable cross-project code out of `Shared`: its supported home is a custom package in
  `Packages/` (a separate task; create no `package.json` here).
- Keep source art in `ArtSource`, beside `Assets`, instead of importing it.
- Defer presets and `Assets/ScriptTemplates` to their own workflows. `Settings/Presets` is this
  starter's convention; an established `Assets/Presets` is equally fine.
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
- **Editor open:** use existing Editor access (for example `AssetDatabase.CreateFolder`), checking
  each path first and targeting the project explicitly. One route that worked: a Unity CLI
  `command eval` call against the open Editor ran that C# and returned the results; discover the
  installed CLI's commands rather than copying this one. With no route, defer creation or ask for a
  safe closed-Editor route. Never install a bridge or close an Editor with unsaved work.
- **`.gitkeep` markers (scaffold mode):** write them with ordinary filesystem operations after the
  folders exist, whatever the Editor state; Unity does not import them.
- **Established project Assets changes:** continue read-only inventory, then route imported-folder
  additions or reorganization to [ReviewFolders.md](ReviewFolders.md). An existing owned root alone
  does not imply reorganization, nor block a selected project-root ArtSource. Vendor relocation runs
  there as a batch in the same first step, after `Assets/ThirdPartyAssets/` exists.

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
- After an observed Unity import, confirm the new folders under `Assets` have generated metadata
  (`~` folders and `ArtSource` get none), GUIDs are unique, pre-existing metadata is unchanged, and
  the import log has no fresh errors. Open the project only when a safe route exists within scope;
  otherwise mark the import checks **Not verified** and tell the user to open it in Unity.
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
| Template leftovers (`Assets/Settings`, sample content, loose root assets) | Reused / Left in place | What exists |
| Layered roots | One root / Core and game | Root names; core-reference check deferred to ReviewFolders.md |
| Tests placement | None / Per feature (asmdefs) / Central `Editor/Tests` | Recorded project choice, if any |
| Tool-owned and generated folders | Reported | Paths; ignore rules pointed to |
| Docs inside `Assets` | None / Reported | Paths and proposed home |
| `Resources` folders | None / Listed | Paths |
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
