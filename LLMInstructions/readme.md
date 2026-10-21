> How it works: pick the topic you need, copy the URL of its agent document, and tell your LLM
> "implement this in my Unity project". The agent inspects the project, asks what it cannot infer,
> applies the recommended settings, and reports what it verified.

# LLM instructions

Each folder covers one topic and holds two kinds of file:

- **Agent documents** are the instructions you hand to your LLM by URL. Each stands alone.
- **`readme.md`** explains the concepts and key decisions for a human reader.

Start with the topic's readme to understand the choices, then give the agent document to your LLM.

## Topics

| I want to… | Hand your agent | Read first |
|---|---|---|
| Set up a project end to end | [SetupInstructions](SetupInstructions/README.md) | same |
| Configure Windows/macOS build settings | [DesktopBuilds.md](BuildSettings/DesktopBuilds.md) | [BuildSettings](BuildSettings/readme.md) |
| Configure Android/iOS build settings | [MobileBuilds.md](BuildSettings/MobileBuilds.md) | [BuildSettings](BuildSettings/readme.md) |
| Create the folder layout | [SetupFolders.md](FolderStructure/SetupFolders.md) | [FolderStructure](FolderStructure/readme.md) |
| Install script templates | [SetupScriptTemplates.md](ScriptTemplates/SetupScriptTemplates.md) | [ScriptTemplates.md](ScriptTemplates/ScriptTemplates.md) |
| Install import presets | [SetupPresets.md](Presets/SetupPresets.md) | [Presets](Presets/readme.md) |
| Add strategy scene templates | [SceneTemplates.md](SceneTemplates/SceneTemplates.md) | same |
| Set project settings | [ProjectSettings.md](ProjectSettings/ProjectSettings.md) | same |
| Set up tests | [Testing.md](Testing/Testing.md) | same |
| Review or audit a project | [ProjectReview.md](ProjectAuditGuides/ProjectReview.md) | same |
| See a custom CLI command with tests | [CliScriptAndTests](CliScriptAndTests/readme.md) | same |
| Plan a CoreCLR migration | [CoreCLRUpgrade.md](CoreCLRmigration/CoreCLRUpgrade.md) | same |
| Pick the tech stack | [UnityTechStack.md](UnityTechStack/UnityTechStack.md) | same |

## Not finished yet

These folders are drafts or empty; do not hand them to an agent yet:

- [Agents](Agents/), [Github](Github/), and [TerrainGeneration](TerrainGeneration/) are empty.
- [UnityProjectRules](UnityProjectRules/UnityRules.md) holds rough notes, not an agent document.

Folders without their own `readme.md` yet: Testing, UnityProjectRules, ProjectSettings, Github,
CoreCLRmigration, and ProjectAuditGuides.
