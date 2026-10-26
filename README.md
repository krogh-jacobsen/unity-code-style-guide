# Unity starter conventions and audits

A selectable kit of Unity C# conventions, project setup and review instructions, script templates,
import presets, and strategy scene templates. This repository contains documentation and resources;
it is not a Unity project. Adapt stylistic preferences to your team and keep the policy,
EditorConfig, templates, and examples consistent.

## Start here

| Situation | Entry point |
|---|---|
| Understand the conventions | [Agent instructions](AGENTS.md) and [style guide](AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md) |
| Set up a project | [Setup workflow](AuditInstructions/SetupInstructions/README.md) |
| Audit an existing project | [Review router](AuditInstructions/ProjectAuditGuides/ProjectReview.md); select applicable lenses |
| Find one setup or audit topic | [Topic index](AuditInstructions/README.md) |
| Update an installed copy | [Kit maintenance](AuditInstructions/KitMaintenance/README.md) |
| Prepare a release | [Release readiness](AuditInstructions/ReleaseReadiness/README.md) |
| Understand audit best-practice coverage and tradeoffs | [Research and pressure test](AuditResearch.md) |
| Check tested compatibility | [Validation record](Validation.md) and [stack profile](AgentsInstructions/UnityTechStack/UnityTechStack.md) |

Skills supply execution mechanics; project choices and resolved package versions govern APIs.
Examples illustrate specific behavior and do not prescribe an architecture.

## How to install

First audit the destination and confirm the selected changes through the
[setup workflow](AuditInstructions/SetupInstructions/README.md). Use one source commit for the whole
selection. There is no automatic installer.

Keep a **reference snapshot** at `Documentation/UnityStarterKit/` outside `Assets`, preserving the
source hierarchy. Include the files and directories listed in
[installation.json](AuditInstructions/SetupInstructions/installation.json). This snapshot contains
resource sources and maintenance tools as reference material; Unity resources are installed only
when selected and copied separately into `Assets`. Exclude checkout internals, caches, and generated
outputs. The manifest is the authoritative snapshot list; this table explains its destinations.

| Source here | Destination relative to the Unity project root | Action |
|---|---|---|
| Manifest `snapshot_sources`, with their existing paths | `Documentation/UnityStarterKit/` | Retain complete reference hierarchy; merge or choose another location if occupied |
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

The root README belongs to the game; keep this kit's README in the snapshot. Adapt the snapshot's
stack profile to the target and record that adaptation for future merges. Existing project choices
win over starter defaults. Other instruction-entry tools can point to the target's root AGENTS.md.

Inspect all conflicts before copying. Preserve existing metadata; use Editor APIs for existing
imported assets. First installation of selected intact asset/metadata pairs with the Editor closed
uses the [resource protocol](AuditInstructions/SetupInstructions/InstallResources.md). Keep `Tools~/`
and documentation out of the imported selection.

The repository's installation check stages this layout in a temporary fake destination and checks
local links, anchors, case, root instruction rebasing, and the active EditorConfig copy:

```sh
python3 AuditInstructions/Tools/check_installation.py
```

It does not install into your game. If you choose another layout or merge existing instructions,
check the resulting target's links separately. Record source revision, selected groups, destination
paths, and local adaptations in `Documentation/UnityStarterKit-installation.json` after confirmation;
the [update workflow](AuditInstructions/KitMaintenance/UpdateKit.md) defines that record.

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
