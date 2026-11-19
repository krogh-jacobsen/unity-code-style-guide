# Unity C# Code Style & LLM Audit Instructions
  
There may be no single right way to write C#, but agreeing on one removes the guesswork. You focus on the solution, and your team and your LLM follow the same consistent rules which ultimately leads to a higher code base quality.

This [Unity C# style guide](AgentsInstructions/CodeStyleGuide/README.md) is built to work well with LLM assistants and focus on Unity 6.7 and newer projects. It combines industry standard C# and general Unity best practices with a few opinionated conventions that are easy to adapt to your own.

Originally an appendix to the popular ebook *Unity C# style guide for Unity 6*, which I co-authored, the repo now also includes LLM agent instructions and audit files.

Use, copy and cherry-pick whatever is helpful for your own Unity project. More info below.

# Unity Audit & Project Start files

Besides the code style instructions, this repo also includes a selection of tools, instructions and audit files that I find helpful and use in my Unity projects. You can use them to set up new projects, or to audit or optimize an existing one. Pick what is helpful and leave the rest.

## Overview

### What's in the repo

| Area | What you'll find | Start here |
|---|---|---|
| **Code style guide** | Naming, formatting and class-layout rules for Unity 6.7+, a ready-made `.editorconfig`, a naming checker script with good/bad fixtures | [Style guide](AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md) · [README](AgentsInstructions/CodeStyleGuide/README.md) |
| **Agent instructions** | An example `AGENTS.md` to copy and adapt, plus the Unity 6.7 tech stack profile your LLM should assume | [AgentsInstructions](AgentsInstructions/README.md) · [Tech stack](AgentsInstructions/UnityTechStack/UnityTechStack.md) |
| **Project setup** | End-to-end setup workflow, folder structure, version control (`.gitignore`, `.gitattributes`, LFS), package installer, project and build settings (desktop and mobile) | [Setup workflow](AuditInstructions/SetupInstructions/README.md) |
| **Reusable Unity resources** | Script templates (core and optional), 13 texture/audio/model/animation import presets, 3 scene templates (asset look-dev, strategy sandbox, UI preview) | [Script templates](AuditInstructions/ScriptTemplates/README.md) · [Presets](AuditInstructions/Presets/README.md) · [Scene templates](AuditInstructions/SceneTemplates/README.md) |
| **Project audits** | A review router plus 20+ discipline lenses: performance, physics, rendering, UI Toolkit/uGUI, networking, audio, persistence, testing and more | [Review router](AuditInstructions/ProjectAuditGuides/ProjectReview.md) |
| **Automation and CI** | GitHub Actions workflows (cloud and self-hosted), PR template, GitHub issue/PR instructions, Unity CLI cheatsheet with a worked example, testing setup | [CI](AuditInstructions/ContinuousIntegration/README.md) · [GitHub](AuditInstructions/Github/README.md) · [Unity CLI](AuditInstructions/UnityCLI/UnityCLI.md) · [Testing](AuditInstructions/Testing/README.md) |
| **Release and migration** | Release-readiness checklist, experimental CoreCLR migration prep | [Release readiness](AuditInstructions/ReleaseReadiness/README.md) · [CoreCLR](AuditInstructions/CoreCLRmigration/README.md) |
| **Maintenance and evidence** | Kit update workflow, validation scripts, replay tests, audit research and the compatibility record | [Kit maintenance](AuditInstructions/KitMaintenance/README.md) · [Research](AuditResearch.md) · [Validation](Validation.md) |

Every audit and setup guide follows the same four stages: **audit → recommend → choose → confirm**. Nothing changes until you confirm. Full topic list: [AuditInstructions](AuditInstructions/README.md).

### Where to start

| I want to… | Go to |
|---|---|
| Understand the conventions | [Agent instructions](AGENTS.md) and [style guide](AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md) |
| Set up a new project | [Setup workflow](AuditInstructions/SetupInstructions/README.md) |
| Audit an existing project | [Review router](AuditInstructions/ProjectAuditGuides/ProjectReview.md) |
| Find one specific topic | [Topic index](AuditInstructions/README.md) |
| Update an installed copy | [Kit maintenance](AuditInstructions/KitMaintenance/README.md) |


## How to install

There is no automatic installer. Your LLM does the work, and you decide what it changes. Pick the
size of adoption that fits:

| I want to… | Do this |
|---|---|
| **Try one thing** (a style guide, a preset, one audit) | Copy the URL of that topic's agent document from the [topic index](AuditInstructions/README.md) and tell your LLM "implement this in my Unity project". |
| **Adopt the whole kit** | Hand the [setup workflow](AuditInstructions/SetupInstructions/README.md) to your LLM. It audits your project, recommends changes, and applies only the ones you pick and confirm. Use one source commit for the whole selection. |
| **Keep the kit for reference and updates** | Keep a **reference snapshot** at `Documentation/UnityStarterKit/`, outside `Assets`, with the source hierarchy intact. See [Where files end up](#where-files-end-up). |

### Where files end up

The reference snapshot holds the kit's documents, resource sources and maintenance tools.
[installation.json](AuditInstructions/SetupInstructions/installation.json) is the authoritative list
of what goes into it. Exclude checkout internals, caches and generated outputs. Unity resources are
copied into `Assets` separately, and only when selected. The table below shows where each piece lands.

| Source here | Destination relative to the Unity project root | Action |
|---|---|---|
| Manifest `snapshot_sources`, with their existing paths, minus `snapshot_exclude` | `Documentation/UnityStarterKit/` | Retain complete reference hierarchy; merge or choose another location if occupied. Excluded replay archives (about 5 MB) stay upstream; snapshot links to them resolve only there |
| AGENTS.md | AGENTS.md | Merge conventions and routing; prefix file links with `Documentation/UnityStarterKit/`; retain local anchors; remove the repository-maintenance section |
| CLAUDE.md | CLAUDE.md | Optional pointer to the target's root AGENTS.md; preserve existing instructions |
| AgentsInstructions/CodeStyleGuide/EditorConfig/.editorconfig | .editorconfig | Merge selected rules; the reference copy is not the active configuration |
| AuditInstructions/VersionControl/Unity.gitignore | .gitignore | Install the selected managed block |
| AuditInstructions/VersionControl/Unity.gitattributes | Repository root .gitattributes | Install selected attributes and optional LFS rules |
| AuditInstructions/ScriptTemplates/ selected template and .meta pairs | Assets/ScriptTemplates/ | Follow the template guide, including optional prerequisites |
| AuditInstructions/Presets/ selected category contents | Assets/Settings/Presets/ matching categories | Follow the preset guide; preserve identities |
| AuditInstructions/SceneTemplates/ selected groups and shared dependencies | Assets/{ProjectName}/SceneTemplates/ or established content root | Follow the scene-template guide's selection and clone/reference rules |
| AuditInstructions/UnityCLI/CliScriptAndTests/ selected example assets | Assets/Examples/CliScriptAndTests/ | Optional example; follow its README and isolate tests |
| LICENSE | ThirdPartyNotices/UnityCodeStyleGuide-LICENSE.txt | Retain attribution for reused resources; preserve unrelated notices |

### Rules when installing

- **Your project wins.** Existing project choices take priority over starter defaults.
- **Your README stays yours.** The root README belongs to the game; this kit's README lives in the snapshot.
- **Adapt the stack profile** to your target and record that adaptation for future merges.
- **Rebase links carefully.** When merging AGENTS.md, prefix only links that point into the snapshot.
  Leave links to files the installation places at the project root (`AGENTS.md`, `CLAUDE.md`,
  `.editorconfig`, `.gitignore`, `Documentation/UnityStarterKit-installation.json`) and same-file
  `#anchor` links as they are. Fill in its "This project" section.
- **Other instruction-entry tools** can point to your root AGENTS.md.
- **Inspect conflicts before copying.** Preserve existing metadata, and use Editor APIs for assets that are already imported.
- **First install of asset and metadata pairs** happens with the Editor closed, or with auto-refresh suspended, following the [resource protocol](AuditInstructions/SetupInstructions/InstallResources.md).
- **Keep `Tools~/` and documentation** out of the imported selection.

### Check and record

The repository's installation check stages this layout in a temporary fake destination and verifies
local links, anchors, case, root instruction rebasing, and the active EditorConfig copy. It does not
install into your game.

```sh
python3 AuditInstructions/Tools/check_installation.py
```

To check a real installation read-only (root AGENTS.md and CLAUDE.md links and anchors, root
`.editorconfig`, snapshot presence), pass its project root:

```sh
python3 AuditInstructions/Tools/check_installation.py --target /absolute/path/to/UnityProject
```
After confirmation, record the source revision, selected groups, destination paths and local
adaptations in `Documentation/UnityStarterKit-installation.json`. The
[update workflow](AuditInstructions/KitMaintenance/UpdateKit.md) defines that record.

## Loading model

| Material | Load when |
|---|---|
| Root AGENTS.md | Every coding session: essential rules and routing |
| Style guide | First owned C# authoring or style-review task |
| Setup instructions | Selected setup/configuration task |
| Audit lenses | Selected project/change/subsystem review |
| Examples and Unity skills | Relevant implementation or execution task |

## Maintenance

```sh
python3 AuditInstructions/Tools/validate_all.py
python3 AgentsInstructions/CodeStyleGuide/Tools~/check_naming.py
```

The first command checks repository links, anchors, GUIDs, instruction contracts, installation staging,
and each topic validator. The second proves naming-rule intersections with actual Roslyn diagnostics.
Use `--require-dotnet` on the first command to fail when its .NET style checks cannot run.
[Repository CI](.github/workflows/repository-checks.yml) runs both commands on pull requests, pushes
to main, and manual dispatch. It validates this kit; it does not run Unity tests or build a game.
Target-project CI templates remain a separate optional installation.

Follow [AGENTS.md](AGENTS.md) when maintaining the kit. Record changes in
[CHANGELOG.md](CHANGELOG.md) and actual evidence and limits in [Validation.md](Validation.md).

License: [MIT](LICENSE).
