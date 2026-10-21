> How it works: give the URL of [SetupFolders.md](SetupFolders.md) to your agent and it will create
> the folders your project needs, with nothing extra, leaving existing content untouched.

# Folder structure

A small, feature-first layout for the content you own in a Unity project. The agent document
creates folders only; this page explains the thinking behind them.

| I want to… | Give your agent |
|---|---|
| Scaffold folders in a new project | [SetupFolders.md](SetupFolders.md) |
| Reorganize an established project | Not covered; see [moving content](#moving-content-safely) |

Example prompt: *"Set up folders only in my Unity project from this document. Use the existing
project name and ask only for missing feature choices."* Close the project's Unity Editor first;
the agent creates plain directories and Unity adds their metadata the next time you open it.

## The layout

```text
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

## Moving content safely

The agent document does not reorganize a project that already has content. Move existing assets
inside the Editor (or with `AssetDatabase.MoveAsset`) so GUIDs and references survive. Afterwards,
check string-based loads like `Resources.Load`, import presets scoped by path, and which assembly
each script ended up in, then reopen affected scenes and prefabs.

## What the agent reports

It lists each path as Created or Already present, repeats the check to prove a second run adds
nothing, and marks Unity's metadata generation as *Not verified* until the project has been opened
in the Editor. Commit the metadata files along with the folders.
