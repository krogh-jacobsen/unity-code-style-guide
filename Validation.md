# Compatibility and validation

The intended profile is [Unity 6.7](SetupInstructions/UnityTechStack.md). This record distinguishes
that choice from the exact prerelease Editor tested. It is not a guarantee for every 6000.7 patch,
package upgrade, target platform, or copied project. Date: 2026-10-12.

## Tested environment

| Component | Exact version |
|---|---|
| Editor | 6000.7.0b4, macOS Apple Silicon |
| Unity CLI | 1.0.0-beta.13 |
| Universal RP | 17.7.0 |
| Input System | 6.7.0 |
| Test Framework | 1.8.0 |
| Netcode for GameObjects (optional template only) | 3.1.0 |
| Pipeline | 0.7.0-exp.1 |
| .NET SDK for naming fixture | 10.0.302 |

Pipeline 0.8.0-exp.1 with the Editor's Universal 3D template failed compilation in Render Graph
CLI attribute references before importing kit assets. The isolated validation project used
0.7.0-exp.1 successfully. Recheck compatibility rather than copying a universal Pipeline pin.
Package changes went through CLI-supported Pipeline installation and the Editor PackageManager
Client API. No running user project was changed.

## Acceptance results

| Check | Result | Scope/limits |
|---|---|---|
| Local references, anchors, inventory, GUIDs | Passed | 40 Markdown files, 155 links/anchors, 41 unique GUIDs; all 24 existing resource GUIDs retained |
| Naming analyzer intersections | Passed | .NET SDK 10.0.302: valid fixture clean; six invalid declarations receive the intended IDE1006 rules |
| Unity template expansion and compilation | Passed | 14 sources × empty/populated namespace = 28 generated scripts; Editor/test/Netcode prerequisites installed |
| Presenter EditMode behavior | Passed | 3 passed, 0 failed; 2 generated placeholders ignored |
| UI lifecycle PlayMode behavior | Passed | 1 passed, 0 failed; 2 generated placeholders ignored |
| Saved scene and repeated Play | Passed | Initial count 0; one activation increments once; fresh host resets between Plays; scene reload enabled |
| Runtime UI layout/style/rendering | Passed | PanelSettings/UXML/USS references valid; graphical Editor composited capture shows count and button |
| New-import explicit preset policy | Passed | Ten initial imports then explicit application/readback; UI mode selected Single when unconfigured |
| Existing-asset preservation | Passed | All ten presets preserve seeded slices/borders/pivots, metadata, overrides, material remap, scale and rig under revised parent exclusions |
| Preset Manager first-import defaults | Partial | Audio/model defaults passed; texture registration crashed inside native preset application on 6000.7.0b4 |
| Normal macOS player build | Passed | Unity CLI StandaloneOSX build succeeded; normal player excludes isolated test assemblies |
| Native mouse/key device interaction | Not verified | Mac locked; synthetic NavigationSubmit activation and rendered UI verified through CLI |
| Other players/devices, experimental reload modes | Not verified | No claim for mobile/Web/AOT, scene-reload-disabled, or future CoreCLR builds |

The main validation used Universal 3D/URP 17.7.0. A second disposable project used URP 17.6.0
(with resolved Core 17.7.0) for preset regeneration/fresh explicit imports; the preset APIs were
from the same 6000.7.0b4 Editor. Scene reload was enabled; Enter Play Mode options were disabled
(flags None). Faster reload choices remain optional and need their own acceptance checks.

**Texture default-import limitation:** first-import PresetManager application crashed in Unity's
native property-modification/type-tree path on this beta, with both leaf and parent exclusions.
The shipped presets now exclude entire unrelated data containers, and the supported tested texture
route is initial import → explicit preset application → SaveAndReimport → readback. Do not register
texture defaults on the tested beta. Revalidate them on another Editor before enabling that optional
route. A fresh UI texture additionally needs an explicit Single/Multiple sprite-mode selection;
the partial preset preserves configured modes and geometry.

Headless camera screenshots omit overlay UI, and headless screen captures were blank. Rendering
was confirmed using `capture_game_view` with `source=screen` in the graphical scratch Editor.
This is a rendering check, not proof of native device/input coverage.

## Reproduction contract

Use a disposable project, not a working game with dirty scenes. Establish exact versions with Unity
CLI, create the selected URP template, install compatible Pipeline, and resolve optional Test Framework
and Netcode through the Client API. Import selected kit resources with metadata. Refresh/import and
require no compiler/import errors. Preserve user settings when adapting an existing project.

Generate all default/selected optional templates using the Editor's actual namespace substitutions
under empty and populated namespaces. Isolate test and Editor scripts in their correct assemblies.
Run `python3 Tools/validate_starter.py` and `python3 Tools/check_naming.py` from the kit checkout.

For presets, create representative source PNG, WAV, and animated FBX fixtures through source tools.
Configure sprite slices/borders, user metadata, bundle labels, platform overrides, and an external
FBX material remap before applying. On the tested beta, import first and apply textures explicitly;
select Single/Multiple for a new unconfigured UI sprite. Use Preset.ApplyTo + SaveAndReimport through CLI-driven Editor
APIs, then read back intended and preserved values. Compare GUIDs with resource-inventory.json.

Run `unity test /absolute/project --mode EditMode --output /absolute/fresh-editmode.xml` and a
separate PlayMode run. Parse counts, ignored placeholders, failures, and logs. Test re-enable and
repeated Play with the selected reload options. Open the sample scene, verify PanelSettings/UXML/USS
and input, then build one agreed player target with Unity CLI. Record any checks not executed.

## Implementation status

The nine selected improvements are implemented. Remaining observations are compatibility/coverage
limits above, not pending starter edits. The optional cancellation, pooling, and custom CLI examples
were subsequently added and verified below. No general installer or save/load example is supplied.
Assets were authored/regenerated/moved
through Unity APIs; source resource GUIDs were retained. Existing repository restructuring was preserved.

## Optional example expansion — 2026-10-12

The [example index](ExampleCode/README.md) now includes screen cancellation, pooled notification
leases, and a custom CLI script-generation/test workflow. Validation reused the disposable
6000.7.0b4 project and CLI/Pipeline/Test Framework versions above; no working game was changed.

| Check | Result | Scope/limits |
|---|---|---|
| Screen cancellation EditMode | Passed | 3 tests: out-of-order results, close/reopen with late completion, observable provider failure |
| Pool ownership EditMode | Passed | 2 tests: stale timer and duplicate return, reset/subscription count, borrowed/retained teardown |
| Custom CLI command and generated behavior | Passed | Command discovery, WouldCreate preview, Created import, cold rerun Unchanged; 7 tests verify generation safety and score behavior |
| Scoped EditMode suite | Passed | 15 passed, 0 failed/skipped: 12 new tests plus 3 existing UI presenter tests |
| Scoped PlayMode suite | Passed | 4 passed, 0 failed/skipped: 3 new lifecycle/timed-return tests plus existing UI lifecycle test |
| Normal macOS player build | Passed | New runtime assemblies present; sample Editor/test assemblies and NUnit absent; no claim for other targets |
| Static integration | Passed | Local links/anchors and resource inventory valid; 42 new identities generated by Unity, 83 total unique GUIDs |

On the tested CLI beta, `unity test` rejects an already-open target project. The disposable Editor
was closed through a targeted CLI-driven Editor API before batch tests; the unrelated working
Editor remained open. The READMEs document this prerequisite and fresh result files outside Assets.
Runtime `async void` demonstration boundaries await their operations and observe errors; tests
await each Awaitable once. Controlled providers deliberately ignore cancellation to verify the
identity guards, while PlayMode tests exercise actual timed/cancellable operations.

A repeat PlayMode run exposed a blanket log assertion reacting to an unrelated Netcode tick warning.
The new tests assert their behavioral outcomes and use the runner's normal unhandled error/exception
checks; they no longer assert the absence of every warning from unrelated installed packages. The
final suite passed. The player build succeeded despite a nonblocking licensing access-token warning.
These examples have no native-input or visual-rendering acceptance claim; the adapters demonstrate
ownership without supplying another UI asset set. Versioned persistence remains a later proposal.

Evidence was written outside the repository under `/tmp/unity-starter-validation-20261012/`:
`expanded-editmode.xml`/`.log`, `expanded-playmode-verified.xml`/`.log`, `expanded-cli-rerun.json`,
and `expanded-player-build-cli.json`/`expanded-player-build.log`. The generated score script is an
exercise output in the disposable project, not a pre-generated source shipped in the kit.
