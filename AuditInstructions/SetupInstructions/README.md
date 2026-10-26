> How it works: give this URL to your agent, for example "Set up my Unity project from this
> document". The agent audits the project, recommends changes across every topic below, lets you pick
> which to carry over, and changes nothing before you confirm.

# Set up a Unity project

Use this workflow for a new project or an explicitly scoped configuration change. It specifies
outcomes; available `new-unity-project`, `unity-cli`, and `unity-package-management` skills own
execution. This repository ships no automatic installer. Prefer Unity CLI; the Editor UI is the
fallback when CLI execution is unavailable.

For a single resource task, use its URL/local-file entry point and stop within that scope:

| Task | Entry point |
|---|---|
| Folders only | [Folder workflow](../FolderStructure/SetupFolders.md) |
| Git ignore, attributes, LFS, and merge setup | [Version control workflow](../VersionControl/SetupVersionControl.md) |
| CI checks and test gate | [CI workflow](../ContinuousIntegration/SetupCI.md) |
| Selected script templates | [Template workflow](../ScriptTemplates/SetupScriptTemplates.md) |
| Selected presets | [Preset workflow](../Presets/SetupPresets.md) |
| Update an existing kit installation | [Update workflow](../KitMaintenance/UpdateKit.md) |

These workflows use available tools without installing a project package or CLI. Template/preset
installation follows the [shared resource protocol](InstallResources.md); broader configuration below
remains a separate selection.

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit yes.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Restate the exact changes for the picked subset (files, settings, values, commands)
   and wait for an explicit yes. Make no change before it, including saving the report. In a
   non-interactive session, or when no answer arrives, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

**Across topics.** Each workflow this document delegates to (folders, version control, CI, script
templates, presets, and the guides in step 3) has its own review contract. Run their audit and
recommend stages first and aggregate every recommendation into one list, with IDs prefixed by topic,
so the user picks across topics once and confirms once. A delegated workflow must not re-prompt for
an item already confirmed here; it applies only the confirmed items from its own recommendations.

## 1. Establish choices

Confirm the destination, project name/namespace, installed Editor, platform, and selected resources.
Read [UnityTechStack.md](../../AgentsInstructions/UnityTechStack/UnityTechStack.md). Retain the URP/Input System/UI Toolkit/Awaitable/ObjectPool
profile unless the user selects another stack. The intended engine line is recorded there; use an
exact chosen release, not an assumed latest version. For an existing project, inspect its settings,
packages, dirty scenes, and source-control state first.

**Done:** selected choices and existing content are known; unresolved decisions affecting setup are
resolved. Avoid a general architecture interview for a small project.

## 2. Select and copy resources

Use [the installation guidance](../../README.md#how-to-install) and [snapshot manifest](installation.json)
for destinations. Preserve the reference hierarchy at `Documentation/UnityStarterKit/` outside `Assets`;
merge root instruction links with that prefix. Install only selected asset groups inside `Assets`. Preserve existing imported metadata
when copying the shipped resources. Do not overwrite the destination's instructions/configuration
without inspecting and merging them. Include the MIT license with reused resources.

**Done:** the reference snapshot and merged root instructions have resolving file links/anchors; `.editorconfig` is at the target root; only
selected presets/templates/examples are staged for import.

## 3. Configure the selected baseline

| Guide | Outcome | Selection |
|---|---|---|
| [Tech stack](../../AgentsInstructions/UnityTechStack/UnityTechStack.md) | Exact Editor/packages, selected systems, targets | Baseline |
| [Project settings](../ProjectSettings/README.md) | Settings match the agreed project/platform | Baseline plus explicit options |
| [Mac and Windows builds](../BuildSettings/DesktopBuilds.md) | Desktop support contract, budgets, build profiles, and native player acceptance | Only selected desktop targets |
| [Android and iOS builds](../BuildSettings/MobileBuilds.md) | Mobile support contract, store/toolchain checks, budgets, and device acceptance | Only selected mobile targets |
| [Package audit](../PackageInstaller/InstallPackages.md) | Existing dependencies inspected; only confirmed missing packages installed | When package setup or a missing prerequisite is in scope |
| [Folder layout](../FolderStructure/README.md) | Small owned feature layout and correct special folders | Baseline; expand when used |
| [Version control](../VersionControl/README.md) | Unity ignore and attribute rules installed; settings that Git depends on confirmed | Baseline |
| [CI](../ContinuousIntegration/README.md) | Licence-free checks installed; Editor tests run locally or on the user's own runner | When tests/examples selected |
| [Presets](../Presets/README.md) | Scoped import policy registered with tested filters | Optional assets |
| [Script templates](../ScriptTemplates/README.md) | Selected menu templates compile under their prerequisites | Optional assets |
| [Scene templates](../SceneTemplates/README.md) | Strategy sandbox, UI preview, and asset lookdev scenes with explicit dependency cloning | Optional assets |
| [Testing](../Testing/TestingInstructions.md) | Tests discoverable and excluded from normal players | When tests/examples selected |

Use CLI discovery rather than copying remembered commands:

```bash
unity --version
unity editors --installed --format json
unity templates list --help
unity status --format json
unity command --project-path /absolute/target/project --format json
```

Creation, Editor/module installation, package operations, and saved settings changes follow the
matching skills. For packages, invoke `UnityEditor.PackageManager.Client` through a supported CLI
command or batch Editor script; verify completed requests. Merely editing a dependency list is not
proof of resolution. Without CLI access, create the project in Hub, use Package Manager, and apply
settings in the Editor; mark unavailable automation checks explicitly.

**Done:** selected settings are read back, requested packages have resolved, and excluded options
have not been applied. Desktop tiers are selected through the desktop guide; fixed gameplay tags and networking are not assumed.

## 4. Import, save, and verify

Use Unity CLI to import and compile the target, then save selected assets/scenes through Editor APIs.
Inspect logs for compilation and UXML/USS/import warnings. Verify metadata and saved references,
restart/reopen the selected scene, and exercise repeated Play with the chosen reload settings.
Run selected tests through `unity test`; inspect fresh result XML. Build the agreed platform through
`unity build` or a CLI-invoked BuildPipeline script. Preserve unrelated dirty scenes.

**Done:** imported resources work from saved state; selected checks have results. An unavailable
Editor/device/build module leaves that check Not verified rather than silently passing.

## 5. Record the result

Update the target's tech-stack record with exact resolved versions, platform/backend, reload choice,
and deviations. Report changed resources/settings, validation results, and remaining limitations.
Record source revision, destinations, selected groups and local adaptations in
`Documentation/UnityStarterKit-installation.json` when selected, so a future update has a baseline.

**Done:** selected choices, evidence, and deviations are recorded or reported with unavailable checks explicit.

Commit only within the user's source-control scope; inspect generated-folder exclusions first.
[Validation.md](../../Validation.md) records testing of this starter, not every downstream project.

## Optional migration

[CoreCLRUpgrade.md](../CoreCLRmigration/CoreCLRUpgrade.md) is a dated compatibility reference. Load only for an actual
migration; it is not a required step for creating the selected baseline.
