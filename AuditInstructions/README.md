> How it works: pick the topic you need, copy the URL of its agent document, and tell your LLM
> "implement this in my Unity project". The agent audits the project, reports what it found,
> recommends changes, and applies only the ones you pick and confirm.

# LLM instructions

Each folder covers one topic and holds two kinds of file:

- **Agent documents** are the instructions you hand to your LLM by URL. Each stands alone.
- **`README.md`** explains the concepts and key decisions for a human reader.

Start with the topic's readme to understand the choices, then give the agent document to your LLM.

## How every guide runs

Every agent document follows the same four stages, so you stay in control whichever one you hand over:

1. **Audit.** The agent reads your project and reports what already matches, what differs, and what it could not check. It writes nothing.
2. **Recommend.** Each difference becomes a numbered recommendation with the reason, the risk, and a default. The agent adds its own suggestions too.
3. **Choose.** You pick any subset, "all recommended", or none. You can carry over one element of a guide without the rest.
4. **Confirm.** The agent restates the exact changes for your picks and waits for an explicit yes. Nothing changes before it.

Only then does it apply, verify, and report, including the recommendations you skipped. In a
non-interactive session the agent stops after the recommendations and changes nothing.

## Topics

| I want to… | Hand your agent | Read first |
|---|---|---|
| Set up a project end to end | [SetupInstructions](SetupInstructions/README.md) | same |
| Configure Windows/macOS build settings | [DesktopBuilds.md](BuildSettings/DesktopBuilds.md) | [BuildSettings](BuildSettings/README.md) |
| Configure Android/iOS build settings | [MobileBuilds.md](BuildSettings/MobileBuilds.md) | [BuildSettings](BuildSettings/README.md) |
| Create the folder layout in a new project | [SetupFolders.md](FolderStructure/SetupFolders.md) | [FolderStructure](FolderStructure/README.md) |
| Review (and optionally reorganize) an existing project's folders | [ReviewFolders.md](FolderStructure/ReviewFolders.md) | [FolderStructure](FolderStructure/README.md) |
| Set up Git rules (`.gitignore`, `.gitattributes`, LFS, merging) | [SetupVersionControl.md](VersionControl/SetupVersionControl.md) | [VersionControl](VersionControl/README.md) |
| Install script templates | [SetupScriptTemplates.md](ScriptTemplates/SetupScriptTemplates.md) | [ScriptTemplates](ScriptTemplates/README.md) |
| Install import presets | [SetupPresets.md](Presets/SetupPresets.md) | [Presets](Presets/README.md) |
| Add strategy scene templates | [SetupSceneTemplates.md](SceneTemplates/SetupSceneTemplates.md) | [SceneTemplates](SceneTemplates/README.md) |
| Review or set core project settings | [ProjectSettings.md](ProjectSettings/ProjectSettings.md) | [ProjectSettings](ProjectSettings/README.md) |
| Capture/implement issues, review PRs, or complete merge/cleanup | [GithubInstructions.md](Github/GithubInstructions.md) | [Github](Github/README.md) |
| Set up CI (works without a paid Unity licence) | [SetupCI.md](ContinuousIntegration/SetupCI.md) | [ContinuousIntegration](ContinuousIntegration/README.md) |
| Review my packages and install the missing ones I need | [InstallPackages.md](PackageInstaller/InstallPackages.md) | [PackageInstaller](PackageInstaller/README.md) |
| Set up tests | [TestingInstructions.md](Testing/TestingInstructions.md) | [Testing](Testing/README.md) |
| Review a project, picking the reviews you want (animation, physics, UI, audio and more) | [ProjectReview.md](ProjectAuditGuides/ProjectReview.md) | [ProjectAuditGuides](ProjectAuditGuides/README.md) |
| See a custom CLI command with tests | [CliScriptAndTests](UnityCLI/CliScriptAndTests/README.md) | same |
| Prepare for a CoreCLR migration (experimental) | [CoreCLRUpgrade.md](CoreCLRmigration/CoreCLRUpgrade.md) | [CoreCLRmigration](CoreCLRmigration/README.md) |
| Pick the tech stack | [UnityTechStack.md](../AgentsInstructions/UnityTechStack/UnityTechStack.md) | same |

## Not finished yet

These folders are drafts or empty; do not hand them to an agent yet:

- [TerrainGeneration](TerrainGeneration/) remains unfinished.
- [UnityProjectRules](../AgentsInstructions/UnityProjectRules/UnityRules.md) holds rough notes, not an agent document.

UnityProjectRules remains rough notes outside this audit collection.
