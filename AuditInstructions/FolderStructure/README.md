> How it works: give the URL of [SetupFolders.md](SetupFolders.md) to your agent and it will audit
> your project, recommend the folders it needs, and create only the ones you pick and confirm,
> leaving existing content untouched.

# Folder structure

A small, feature-first layout for the content you own in a Unity project. The agent document
creates folders only; this page explains the thinking behind them. Unity's own guidance is that
[no single structure is right](https://unity.com/how-to/organizing-your-project): document your
conventions and apply them consistently. This layout is one such convention.

| I want to… | Give your agent |
|---|---|
| Scaffold folders in a new project | [SetupFolders.md](SetupFolders.md) |
| Review or reorganize a project that already has content | [ReviewFolders.md](ReviewFolders.md) |

Example prompt: *"Set up folders only in my Unity project from this document. Use the existing
project name and ask only for missing feature choices."* Close the project's Unity Editor first;
the agent creates plain directories and Unity adds their metadata the next time you open it.

## What happens when you hand it over

1. **Audit.** The agent reads your project: existing folders, template leftovers, path length.
2. **Recommendations.** Each folder that fits becomes a numbered recommendation with its purpose.
3. **You pick.** Take any subset, "all recommended", or none; a single folder is fine.
4. **You confirm.** The agent restates the exact paths and waits for a yes. Nothing is created before it.
5. **Apply and verify.** It creates the confirmed folders, repeats the check, and reports what you
   skipped as proposals.

[ReviewFolders.md](ReviewFolders.md) runs the same way, and each batch of moves also gets its own checkpoint.

## The layout

```text
ArtSource/                # Optional: PSD, Blend, and other source files Unity should not import
Packages/                 # Embedded local packages for reusable code
Assets/
├── ScriptTemplates/      # Selected script templates
├── StreamingAssets/      # Optional raw player content
├── ThirdPartyAssets/     # Vendor imports
├── Settings/Presets/     # Selected import presets
└── {ProjectName}/
    ├── Scenes/           # Bootstrap and project-wide scenes
    ├── Settings/         # Project-wide URP, Input Actions, shared UI settings
    ├── Shared/           # Independent shared code and content
    └── Inventory/        # An example feature
        ├── Scripts/  Editor/  Tests/  Data/  Prefabs/  Art/
        └── UI/           # UXML, USS, C# and Sprites/ for each screen
```

The tree is a menu, not a template. A project starts with its owned-content root and gains folders
the first time a feature needs them.

## Key ideas

**Feature first.** Group by what something is for (`Inventory`), not by file type (`Scripts`,
`Prefabs`). A feature's code, data, art, and UI then travel together, and deleting a feature is one
folder.

**Ownership decides placement.** Content lives with the feature that gives it meaning, even when
other features use it. Several consumers alone do not make something shared. Put content in `Shared`
only when it has its own responsibility and depends on no feature, through either code or asset
references. Keep cross-feature dependencies explicit and free of cycles.

**Project-wide versus feature-local.** Scenes and settings that compose several features sit at
the project level. A feature's own scenes and configuration stay inside it. Authored configuration
assets go in the feature's `Data`.

**Start with only what you use.** Empty folders add navigation cost and imply structure that doesn't
exist yet. The agent asks which real features you have and creates only their folders.

**UI Toolkit screens stay together.** Keep a screen's UXML, USS, and C# in one folder while the
feature is small. Keep UI sprites in `UI/Sprites` so import presets can tell them from world textures.

## Unity's special folders

- `StreamingAssets` and the starter's `ScriptTemplates` must be direct children of `Assets`.
- Create `Resources` or `Plugins` only for a real loading or plugin need, and follow platform-specific
  plugin paths.
- `Assets/Settings/Presets` is this starter's convention, not a Unity special folder. It is separate
  from the project's rendering, input, and UI settings under `{ProjectName}/Settings`.
- Keep guides, build outputs, and validation reports outside `Assets`.

See Unity's [reserved folder names](https://docs.unity3d.com/Manual/SpecialFolders.html).

## Folders are not assemblies

Creating `Tests/EditMode` does not create a test suite, and an `Editor` folder is not isolated by its
name once an assembly definition (asmdef) covers it.

- Start with the default assemblies. Add asmdefs for concrete needs: testing, platform isolation,
  reuse, or faster iteration.
- An asmdef includes only its own folder tree. One in `Scripts` does not cover a sibling `UI` folder.
- An `Editor` folder under a runtime asmdef needs its own Editor-only asmdef or an asmref.
- Test asmdefs reference production assemblies; they cannot reference the predefined
  `Assembly-CSharp`. Keep production code out of test assemblies.

See [assembly definitions](https://docs.unity3d.com/Manual/assembly-definitions-intro.html).

## Vendor content

Use `ThirdPartyAssets` only when the vendor supports relocating its files. Keep vendor-required
paths and internal layout, and manage UPM dependencies through Package Manager. Put your own adapters
beside the feature they serve rather than editing vendor source, and record any unavoidable patch.

## Starting from a Unity template

A project created from a Unity template already has an `Assets/Settings` folder; what it holds
depends on the template (for example render-pipeline and volume settings). It usually also has a
sample scene and sample assets. The agent reuses `Assets/Settings`, so the starter's
`Settings/Presets` sits inside the folder Unity already made. It leaves the samples in place and
tells you they exist; deleting them is your call. See Unity's
[default project directories](https://docs.unity.com/en-us/engine/6000.6/manual/get-started/project-configuration/default-directories).

## Names and paths

- Name folders in PascalCase with no spaces, and keep casing consistent. Case-only differences
  collide on Windows and macOS and diverge on Linux build machines.
- Never start a folder name with a dot: the Editor converts a leading dot to an underscore, and
  Unity skips dot-prefixed folders on import.
- Keep nesting shallow, about four levels below your content root.
- Keep the project's own path short and free of spaces. Windows path-length failures in IL2CPP
  and Android builds are reported often; Unity publishes no safe limit, and enabling Windows long
  paths [did not fully fix the Editor](https://discussions.unity.com/t/unity-editor-still-hits-windows-max-path-260-char-limit-even-with-longpathsenabled-any-real-fix/1732098)
  for at least one user.

Unity does not require the spaces, nesting, or PascalCase rules; they are this guide's
recommendations for fewer surprises with tools and CI.

## Source art and hidden folders

Unity imports everything under `Assets`, so large source files (PSD, Blend, and similar) slow the
project and bloat it. Keep them in an `ArtSource` folder beside `Assets` and export the game-ready
files into the feature's `Art`. Unity also skips folders ending in `~`, folders named `cvs`, and
dot-prefixed folders (except under `StreamingAssets`), and does not create `.meta` files for them. The
`~` suffix is how packages hide `Documentation~` and `Samples~`. See the
[special folders](https://docs.unity3d.com/Manual/SpecialFolders.html) page.

## Reusable code: local packages

Code that several projects share belongs in a package, not in `Shared`. An embedded package is a
folder under `Packages/` with a lowercase `package.json` and Unity's recommended layout: `Runtime`
and `Editor` (each with its asmdef), `Tests`, and optional `Documentation` and `Samples`. Unity
requires `.meta` files for `Runtime`, `Editor`, and `Tests`. Unity's Create Package tool scaffolds
`Documentation` and `Samples` without the `~`, and the `~` is added to `Samples` when you export. See
the [custom package layout](https://docs.unity3d.com/Manual/cus-layout.html). The folder-setup agent
leaves package creation to a separate task.

## Platform plugin folders

Custom Android build files go in `Assets/Plugins/Android/`: Gradle templates and a custom main
manifest. Unity generates them when you enable the matching option in Player Settings, so don't create
them by hand. The Android manifest page is older than the Unity 6 docs, so confirm the option name
in your Editor. See the [mobile build guide](../BuildSettings/README.md).

## Namespaces and folders

Unity does not derive namespaces from folders. An asmdef's Root Namespace is only the default that
Rider and Visual Studio add to new scripts created inside it, and existing scripts keep what they
declare. Pick a convention (namespace mirrors the feature folder) and enforce it through the style
guide and `.editorconfig`.

## Related topics

- **Source control.** `.gitignore`, Git LFS for large binaries, Force Text serialization, and Visible
  Meta Files are not folder rules. They will live with the Github guide, which is not written yet.
- **Addressables.** If you adopt them, group assets by how they load, not by folder. Add this when
  Addressables is a selected system.

## Already have a project? Review it first

[ReviewFolders.md](ReviewFolders.md) is for a project that already has content and its own folders.
Start with a review: it only reads, and it gives you findings with evidence. Reorganizing is a
separate, optional step.

Example prompts:

- *"Review my current folder structure against this guide and recommend what and how to improve."*
- *"Review only `Assets/Gameplay` against this guide and tell me which moves are safe."*
- *"Move the low-risk findings in small batches, and check each batch before the next."*

What makes it safe:

- **Review before moving.** Nothing moves until you approve a specific batch.
- **Risk-rated moves.** Assets that only GUIDs refer to are low risk. Scripts and assembly
  definitions are medium, because a folder decides which assembly a script compiles into. Anything
  that depends on path text is high risk: `Resources.Load` names, hard-coded `Assets/` strings,
  Addressables addresses, and path-scoped import presets.
- **Unity does the moving.** Moves go through the Editor so each `.meta` file and GUID travels
  with its asset. Moving files in Explorer, Finder, or by hand risks breaking references.
- **Small, checkpointed batches.** Each batch starts from a commit and is verified (GUIDs, compile,
  scenes and prefabs, tests) before the next. A failed batch is undone.
- **Partial adoption is fine.** Keep your own consistent convention and adopt only the parts that help.
- **Some things stay put.** `Packages/`, `ProjectSettings/`, vendor content with a required layout,
  and Unity template folders are left alone.

## What the agent reports

It lists each path as Created or Already present, repeats the check to prove a second run adds
nothing, and marks Unity's metadata generation as *Not verified* until the project has been opened
in the Editor. Commit the metadata files along with the folders.
