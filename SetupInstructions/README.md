# Set up a Unity project

Use this workflow for a new project or an explicitly scoped configuration change. It specifies
outcomes; available `new-unity-project`, `unity-cli`, and `unity-package-management` skills own
execution. This repository ships no automatic installer. Prefer Unity CLI; the Editor UI is the
fallback when CLI execution is unavailable.

## 1. Establish choices

Confirm the destination, project name/namespace, installed Editor, platform, and selected resources.
Read [UnityTechStack.md](UnityTechStack.md). Retain the URP/Input System/UI Toolkit/Awaitable/ObjectPool
profile unless the user selects another stack. The intended engine line is recorded there; use an
exact chosen release, not an assumed latest version. For an existing project, inspect its settings,
packages, dirty scenes, and source-control state first.

**Done:** selected choices and existing content are known; unresolved decisions affecting setup are
resolved. Avoid a general architecture interview for a small project.

## 2. Select and copy resources

Use [the installation guidance](../README.md#how-to-install) for destinations. Copy documentation outside
`Assets`; install only selected asset groups inside `Assets`. Preserve existing imported metadata
when copying the shipped resources. Do not overwrite the destination's instructions/configuration
without inspecting and merging them. Include the MIT license with reused resources.

**Done:** required relative document links resolve; `.editorconfig` is at the target root; only
selected presets/templates/examples are staged for import.

## 3. Configure the selected baseline

| Guide | Outcome | Selection |
|---|---|---|
| [Tech stack](UnityTechStack.md) | Exact Editor/packages, selected systems, targets | Baseline |
| [Project settings](ProjectSettings.md) | Settings match the agreed project/platform | Baseline plus explicit options |
| [Folder layout](FolderStructure.md) | Small owned feature layout and correct special folders | Baseline; expand when used |
| [Presets](Presets/readme.md) | Scoped import policy registered with tested filters | Optional assets |
| [Script templates](ScriptTemplates.md) | Selected menu templates compile under their prerequisites | Optional assets |
| [Testing](Testing.md) | Tests discoverable and excluded from normal players | When tests/examples selected |

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
have not been applied. No fixed gameplay tags, quality tiers, or networking are assumed.

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
Commit only within the user's source-control scope; inspect generated-folder exclusions first.
[Validation.md](../Validation.md) records testing of this starter, not every downstream project.

## Optional migration

[CoreCLRUpgrade.md](CoreCLRUpgrade.md) is a dated compatibility reference. Load only for an actual
migration; it is not a required step for creating the selected baseline.
