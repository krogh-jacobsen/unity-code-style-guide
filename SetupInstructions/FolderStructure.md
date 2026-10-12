# Folder layout

**Prerequisite:** project name/namespace and selected resources are known. Start with only the folders
being used. This is an owned-content convention, not a requirement to create empty directories.

```text
ProjectRoot/
├── AGENTS.md
├── CodeStyleGuide/
├── SetupInstructions/
├── AuditGuides/
└── Assets/
    ├── ScriptTemplates/       # Selected .cs.txt files; exact project-level location
    ├── StreamingAssets/      # Optional raw player content; exact Unity special location
    ├── ThirdPartyAssets/     # Asset imports you control; UPM packages remain under Packages
    ├── Settings/Presets/     # Selected reusable preset assets
    └── {ProjectName}/
        ├── Scenes/
        ├── Settings/         # URP, Input Actions, shared UI settings
        ├── Shared/           # Only genuinely shared code/content
        └── Inventory/        # Example feature; create actual features when needed
            ├── Scripts/
            ├── Editor/
            ├── Data/
            ├── Prefabs/
            ├── Art/
            └── UI/
                ├── Sprites/
                ├── UXML/
                └── USS/
```

Keep UI sprites with their UI feature so scoped import filters can distinguish them from world
textures. Keep guides, build outputs, and validation reports outside `Assets`. Resources and Plugins
folders are optional: create them only for an actual runtime-loading/plugin requirement. An Editor
folder beneath an asmdef may need an explicit Editor-only child assembly.

## CLI/manual application

Create/import folders through CLI-driven `AssetDatabase` calls. Move existing imported content with
`AssetDatabase.MoveAsset`; preserve GUIDs, references, prefab overrides, and vendor boundaries. Manual
fallback: Project window folder creation/moves. Copy shipped groups intact before initial import;
Unity generates missing metadata for new assets.

**Done:** owned feature content is discoverable, selected templates are directly under
`Assets/ScriptTemplates`, StreamingAssets content (if used) is directly under `Assets/StreamingAssets`,
and moved content reopens with unchanged references.

Technical reference: [StreamingAssets special folder](https://docs.unity3d.com/6000.0/Documentation/Manual/StreamingAssets.html).
