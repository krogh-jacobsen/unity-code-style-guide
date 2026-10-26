# Compatibility and validation

The intended profile is [Unity 6.7](AgentsInstructions/UnityTechStack/UnityTechStack.md). This record distinguishes
that choice from the exact prerelease Editor tested. It is not a guarantee for every 6000.7 patch,
package upgrade, target platform, or copied project. Date: 2026-10-12.

## Project review feedback implementation — 2026-10-26

Implemented all six approved refinements: concrete-scope approval without a mandatory literal
"yes", acceptance conditions and cause assessments, runtime collection context, concurrent-source
freshness and explicit ownership, separate implementation/acceptance reporting, and incidental
observations outside selected-lens coverage. The canonical contract and all 18 published copies
match. Active human summaries and completion criteria use the same approval terminology; historical
validation entries retain their original wording.

| Check | Result | Evidence / limit |
|---|---|---|
| Complete repository validation with required .NET gates | Passed | `python3 -B -u AuditInstructions/Tools/validate_all.py --require-dotnet` with host access: 74 Markdown files, 467 local links/anchors, 75 unique GUIDs, six topic validators, installation staging/four negative probes, 22 CI fixture projects and style gates |
| Contract and replay regressions | Passed | `python3 -B AuditInstructions/Tools/test_audit_contract.py`: 14 tests; exact contract copies, corruption rejection, and scenario-specific authorization prompts checked |
| Replay generation and integrity | Passed | 204 unique fixtures generated outside the repository; five new approval scenario families apply to all 18 entry points, plus four review-specific evidence/acceptance/scope scenarios. Default audit prompts remain read-only; decision prompts retain their scenario authorization and prohibit real workspace mutation from fictional evidence |
| Syntax and whitespace | Passed | AST parsing of the two changed Python modules and `git diff --check` |
| Concurrent-edit preservation | Passed | Saved the starting text snapshot and diff outside the repository; compared pre-existing added lines. All remain except the old hard-coded replay stop instruction, now preserved as the default task so decision scenarios can continue. No resets, stashes, or whole-file restoration |
| Fresh-agent behavioral replay | Not verified | New cases and expected decisions were reviewed and generated, but no fresh-agent session or disposable Unity target was executed. Fixture/contract tests establish structure, not agent compliance |
| Unity gameplay, Editor, and player validation | Not verified | Documentation and maintenance tooling only; no Unity implementation/assets changed and no Editor/test/build run was needed |

The validated source was this dirty working tree, including concurrent workflow changes and the
review refinements, rather than a single commit. The initial sandboxed full validator did not
complete promptly and was stopped with its child processes after the host-access run above completed
successfully, including required .NET gates.

## Fresh-agent workflow replays — 2026-10-26

The original checkpoint and its corrective replays are complete. Each case used a new built-in
leaf agent with `fork_turns=none`, inherited model/reasoning, and no model override. Expected outcomes
were withheld from the leaf; a coordinator graded each response and quoted its evidence. The parent
independently checked source hashes, unique identities, expected arrays, counts, and verbatim quotations.

| Run | Cases | Pass | Fail | Not verified |
|---|---:|---:|---:|---:|
| Original frozen snapshot | 106 | 77 | 3 | 26 |
| Corrected guides and concrete fixture evidence | 55 | 55 | 0 | 0 |
| Nested-project and ArtSource scope checks | 4 | 4 | 0 | 0 |
| Latest observed verdict per original/added case ID | 110 | 110 | 0 | 0 |

This is **165 fresh-agent case executions**, retaining the original failures and incomplete verdicts.
The original three failures were dirty-tree rules pausing independent read-only audit. Eighteen
incomplete cases lacked the identity of the missing prerequisite; seven omitted a fallback decision;
one had ambiguous platform evidence. Corrected replays resolve those cases. Additional agent
compensations exposed unknown-versus-unset status, unconditional platform profiles, ArtSource scope,
standalone budget handoff, older-project reload policy, and missing delegated-guide reporting.

The [replay evidence archive](AuditInstructions/Tools/replay_results_2026-10-26.json) contains frozen
source documents, case inputs, full responses, agent identities, hashes, grades, and exact quotations.
Raw temporary inputs/responses also remain under `/private/tmp/audit-replays-20261026-v1`, `v2`, and
`v4`; `v3` was prepared but never executed. Data in the archive is the portable evidence source.

**Expanded checkpoint: partial evidence captured for publication.** The fixed checkpoint contains
213 generated cases, including 103 new case IDs. The archived capture has 42 graded expanded cases:
38 Pass, two Fail, and two Not verified; 61 selected IDs lack grades in this capture. Later concurrent
work remains unfinished and is not included in these counts. Together with the earlier checkpoint,
the archive contains 207 case executions across 152 observed IDs: latest verdicts are 148 Pass,
two Fail, and two Not verified. These are observed decisions, not physical tool execution.

The two failures concern invented execution scope after duplicate approval in the CI and folder-review
fixtures. The two Not verified cases concern omission of continued independent inspection when concrete
scope was missing. Subsequent wording clarifies both boundaries; no corrective replay pass is inferred.
All grades retain their original source hashes, expected outcomes, response quotations, and limitations.
Source hashes, grade/fixture identity and expected arrays, quotations, and counts were checked during
publication. Pending IDs are retained explicitly in the archive's partial-checkpoint integrity record.

**Limits:** these are decision replays against fictional project evidence, not observed Unity, asset,
build, GitHub, or publication operations. Fresh conversations share ambient repository instructions
and filesystem access. The canonical confirmation policy changed concurrently; frozen payloads and
that mismatch are preserved. All original/corrective cases withhold implementation authorization,
so both contract wordings require the same no-write decision. Positive authorization has only partial observed coverage
in the expanded checkpoint; its failing and unverified cases remain unresolved. Earlier passing cases were retained while affected branches
were rerun; no statistical reliability or fully hermetic environment claim is made.

The current static validator (including required .NET gates) and naming check passed after the guide
fixes: 74 Markdown files, 467 local links/anchors, 75 unique GUIDs, six topic validators, 14 workflow
regression tests, 22 CI fixtures, and expected naming diagnostics. Final record links will be rechecked.

## Audit pressure-test implementation — 2026-10-26

Implemented the selected review recommendations R1–R10 and R12. R11 was not selected. Changes are
documentation and static maintenance tooling; existing imported resources and metadata were preserved.
Concurrent repository reorganization, installation/maintenance/release guidance, and CI work remain intact.

| Check | Result | Evidence / limit |
|---|---|---|
| Complete repository validation | Passed | `python3 -u AuditInstructions/Tools/validate_all.py --require-dotnet` with authorized host access: 74 Markdown files, 466 local links/anchors, 75 unique GUIDs, six topic validators, installation staging/four negative probes, workflow regressions, and required .NET gates. The earlier static-only invocation also passed |
| Workflow contract/routing regressions | Passed | `python3 -B AuditInstructions/Tools/test_audit_contract.py`: 10 tests, including a published guide missing its preamble, altered/truncated/duplicated/misplaced contracts, setup routes, and rendering/coverage routing |
| CI project fixtures and YAML/workflow checks | Passed | 22 disposable projects: metadata failures, named/GUID asmrefs, embedded packages, predefined/explicit Editor isolation, runtime boundaries, constraint-only/NUnit-only negatives, framework GUID availability, and a nested project path containing spaces |
| .NET whitespace/naming gates | Passed | `python3 -u AuditInstructions/ContinuousIntegration/Tools~/validate_ci.py` outside the sandbox with SDK 10.0.302: clean fixtures pass, bad whitespace/naming fixtures fail, vendor code remains excluded |
| Roslyn naming intersections | Passed | `python3 -u AgentsInstructions/CodeStyleGuide/Tools~/check_naming.py` with SDK 10.0.302: good fixture 0 IDE1006 diagnostics; bad fixture 6 expected diagnostics |
| Python syntax and whitespace | Passed | AST parsing of six changed/new modules; `git diff --check` |
| Workflow replay generation | Passed | 106 unique prompts for 18 discovered entry points across eight scenario families, generated outside the repository with result `Not verified` |
| Fresh-agent workflow replay | Completed subsequently | See the fresh-agent replay section above; this original implementation pass supplied the catalog before behavioral replay |
| Unity runtime, rendering, discovery, and normal-player isolation | Not verified | No Unity project or imported asset implementation changed; no Editor/device run or player build performed |
| Hosted/self-hosted GitHub execution | Not verified | Workflow syntax, targeting, and safety invariants checked locally; no push or runner dispatch |

Technical claims were checked against official Unity documentation for static cleanup (including the
6000.5 API and 6000.7 manual), Android/iOS frame-rate control, root-motion ownership, uGUI layout,
and URP Render Graph recording/resources and camera stacking. Source links live with the affected
guides. The 6.5 API check is documentation evidence, not a new compile/runtime compatibility claim.
Other historical store deadlines and roadmap claims were not comprehensively revalidated in this pass.

The initial sandboxed `--require-dotnet` run failed because Roslyn could not bind its build-host
named pipe (`SocketException (13): Permission denied`). Re-running the CI validator with authorized
host access passed, followed by the complete `--require-dotnet` validator and naming regression
check; that environment failure is separate from fixture or repository failures.

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
Run `python3 AuditInstructions/Tools/validate_all.py` and `python3 CodeStyleGuide/Tools~/check_naming.py` from the kit checkout.

For presets, create representative source PNG, WAV, and animated FBX fixtures through source tools.
Configure sprite slices/borders, user metadata, bundle labels, platform overrides, and an external
FBX material remap before applying. On the tested beta, import first and apply textures explicitly;
select Single/Multiple for a new unconfigured UI sprite. Use Preset.ApplyTo + SaveAndReimport through CLI-driven Editor
APIs, then read back intended and preserved values. Compare GUIDs with `LLMInstructions/Presets/Tools~/inventory.json`.

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

The [example index](AuditInstructions/UnityCLI/CliScriptAndTests/README.md) now includes screen cancellation, pooled notification
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


## Mac and Windows starter improvements — 2026-10-17

Assets were authored through Unity APIs in a new disposable Universal 3D project: Unity
6000.7.0b4 on macOS Apple Silicon, URP 17.7.0, Unity CLI 1.0.0-beta.13. Test Framework 1.9.0 was
installed through PackageManager.Client for the focused EditMode suite. Existing game Editors and
projects were not changed. All 83 previous resource GUIDs remain; six new Unity-generated identities
cover the three audio presets and three UI Toolkit templates.

| Check | Result | Scope/limits |
|---|---|---|
| Template expansion/compilation | Passed | Five changed/new templates × empty/populated namespaces = ten scripts, expanded through the installed ProjectWindowUtil.CreateScriptAssetFromTemplate implementation |
| Template Create menus | Passed | All five changed/new entries discovered after Editor restart |
| Focused EditMode suite | Passed | 23 passed, 0 failed, 0 skipped; fresh XML and logs inspected |
| UI Toolkit scaffolds | Passed | Multi-object serialized fields and edits, window tree recreation, unregistered nonrecursive drawer; IMGUI multi-object attribute/override checked |
| Audio variants | Passed | PCM UI, mono ADPCM spatial effects, Vorbis layered ambience apply intended settings after save/reimport; preserve sample rate, normalization, Standalone override, user data, bundle metadata, and labels |
| Static-model collider policy | Passed | Initially enabled collider generation becomes disabled; imported colliders absent; scale/material remap/metadata/labels preserved on a minimal OBJ using ModelImporter |
| Resource static checks | Passed | 89 unique GUIDs, 13 partial presets, 17 template sources; metadata and identity inventory checked |
| Changed setup references | Passed | 31 local links/anchors across six changed setup documents |
| Whole-checkout documentation links | Not passed | Missing references remain in the concurrent directory restructuring; resource-only checks do not waive the full link check |
| Native desktop acceptance | Not verified | No Windows/Mac player builds, Intel Mac checks, graphics/audio listening, native UI input, hardware profiling, or new pool runtime lifecycle checks |

The three audio variants are alternatives to the original policies. They preserve existing platform
overrides, so intended default settings and actual Standalone overrides must be reviewed separately.
The model preset's only serialized policy change is inclusion of m_AddColliders = false; its GUID
is unchanged. Texture role presets remain unchanged and preserve independently chosen desktop budgets.
The proposed budgets and desktop profiles are guidance, not configurations applied to a game project.

UI tests inspect generated trees and SerializedObject edits in EditMode; they do not establish
mouse-driven Inspector behavior, visual layout, Undo/Redo, or downstream prefab overrides. Importer
persistence was tested through save/reimport, not a separate post-restart acceptance pass. The model
fixture uses OBJ; the prior FBX rig-preservation results above were not rerun for this change.
The pool's changes are tooltips/braces only; its original behavior token stream is preserved.
Nonblocking logs include missing normals in the minimal OBJ fixture, retained disposable test assets,
and a licensing handshake fallback that completed successfully.

Reproduce resource validation with `python3 AuditInstructions/Tools/validate_all.py --resources-only`; run without
that flag for the full documentation scan. For Unity validation, import the selected resources into
a disposable project, expand each changed/new template under both namespace configurations, isolate
Editor/tests, and exercise the preservation cases above through Unity CLI. The UI templates remain
unregistered until a real target type is selected; their drawer layouts are intentionally unfinished.

Fresh evidence is under `/tmp/unity-desktop-starter-20261017/`: `authoring.log`,
`template-generation.log`, `template-menu-discovery.txt`, `editmode-results.xml`,
`editmode-editor.log`, and `resource-validation.txt`. The disposable project contains the focused
fixture source at `DesktopStarterValidation/Assets/ValidationTests/Editor/DesktopStarterTests.cs`.
These temporary files are local evidence and are not shipped starter resources.

## Strategy scene templates — 2026-10-17

Added the optional [scene-template group](AuditInstructions/SceneTemplates/README.md):
Strategy Sandbox, UI Preview, and Asset LookDev. Map Authoring remains deferred. Railroad Tycoon's
camera reuse contract and asset-lookdev scenes informed the design; its project was read only.
The delivered camera is a compact independent implementation, and no railroad scripts, vendor art,
game managers, or original game asset GUIDs were copied.

Authoring and validation used separate disposable Universal 3D projects: **Unity 6000.7.0b4**,
**URP/Core 17.7.0**, **Input System 6.7.0**, **Test Framework 1.9.0**, and **Unity CLI
1.0.0-beta.13**, on macOS Apple Silicon. The source asset root was `Assets/StarterSceneTemplates`;
the clean consumer imported at `Assets/StrategyStarter/SceneTemplates` to check relocation. Unity
authored the scenes, prefab, materials, input asset, profiles, templates, thumbnails' import settings,
and metadata. The resource group is approximately 916 KiB and adds 30 identities, retaining all
89 earlier inventory entries: **119 unique GUIDs** in total.

| Check | Result | Scope/limits |
|---|---|---|
| Clean import and compilation | Passed | Three templates plus runtime assembly import without C#, UXML, or USS errors in the separate consumer |
| Template validity and saved scenes | Passed | Three valid default-listed SceneTemplateAssets; two generated scenes each, saved and reopened through SceneTemplateService; no missing scripts, one camera/listener per standalone scene |
| Dependency ownership | Passed | Volume Profiles and UI PanelSettings/UXML/theme/USS clone; camera prefab, source input, scripts, and materials remain shared; no dependencies on other project content |
| Focused EditMode suite | Passed | 6 passed, 0 failed/skipped/inconclusive; independent editable assets, relocated shared references, owned cloned USS dependency, materials, and profile components |
| Focused PlayMode suite | Passed | 2 passed, 0 failed/skipped/inconclusive; actual synthetic keyboard pan after disabling a second rig, blocked movement, projection, camera re-enable; UI selection, host disable/re-enable, modal/Close/Escape focus restoration |
| Normal macOS player | Passed | Non-development arm64 Mach-O player built and ran; generated three-scene list; template test assemblies and NUnit absent from Managed output |
| Graphical acceptance | Passed | Inspected actual player captures of all three scenes at 1280x720, open modal, and resized 800x600 UI; final key/fill lighting, label contrast, and control layout reviewed |
| Thumbnail delivery | Passed | Three player captures imported by Unity, assigned as previews, then reimported from the exact repository delivery before recreating/reopening all six scenes |
| Resource/static checks | Passed | 119 unique identities, complete metadata/inventory, three source scenes/templates/previews; 13 presets and 17 script-template sources retained |
| Focused setup links | Passed | Six setup/maintenance/validation documents, 37 local links/anchors |
| Whole-checkout documentation scan | Not passed | 25 existing missing links in the concurrent documentation restructuring, principally the moved style guide and its audit links; the selected new setup documents pass |
| Native input feel and other platforms | Not verified | Physical mouse/keyboard/controller feel, Windows/Intel Mac, other Editor/package releases, HDR displays, and hardware performance budgets were not tested |

The PlayMode fixture temporarily changes Input System background/editor focus behavior for synthetic
devices, then restores both values; a batch Editor otherwise disables its virtual keyboard without
a focused Game view. Runtime camera code still respects focus loss. Final visual-only light/color
values and thumbnails were verified by
player rendering and a final six-scene re-instantiation; the runtime behavior sources were unchanged.

The player log reports stripped/unsupported unused Gaussian/Bokeh Depth of Field and Panini shaders
on this beta. Those effects are not enabled in these scenes; the supplied Volume leaves tonemapping
off. There were no missing materials/scripts or runtime exceptions in acceptance. Editor runs also
reported a licensing protocol fallback that recovered, and debugger-listen messages. These are
recorded limitations rather than a claim of warning-free logs or compatibility with every Unity 6
release. New Scene discovery was checked through the asset validity/default-listing contract and
actual template instantiation, not a native mouse walkthrough of the dialog.

Reproduction sources are in [SceneTemplates/Tools~](AuditInstructions/SceneTemplates/Tools~/README.md), outside the
installable asset group. Evidence is local under `/private/tmp/unity-scene-templates-20261017/`:
`authoring.log`, `refine-source.log`, `preview-authoring.log`, `editmode-results.xml`/`editmode.log`,
`playmode-results.xml`/`playmode.log`, `final-player-build.log`, `final-player-acceptance.log`,
`final-delivery-import.log`, and `FinalCaptures/`. The final consumer dependency/readback report
and build summary are in `Consumer/ValidationResults/`. Temporary capture probes and disposable
projects are not included in normal installation. Run the resource check with
`python3 AuditInstructions/Tools/validate_all.py --resources-only`; repeat `--markdown-path` for selected
repository-relative documentation files, or omit it for the whole-checkout scan.

## Script template pressure test — 2026-10-21

Re-expanded the selectable script templates through Unity's own engine
(`ProjectWindowUtil.CreateScriptAssetFromTemplate`, via reflection) in a disposable project on
**Unity 6000.7.0b4**, with Enter Play Mode set to skip domain reload. Harness and steps:
[ScriptTemplates/Tools~](AuditInstructions/ScriptTemplates/Tools~/README.md).

| Check | Result | Scope/limits |
|---|---|---|
| Expansion and compile | Passed | 14 templates × empty and `Sample.Game` namespaces = 28 scripts, zero errors and zero warnings (after the Awaitable template's `CS4014` was fixed with a discard) |
| Awaitable Operation behavior | Passed (partial) | PlayMode test: restart, disable, re-enable, double cancel, destroy mid-run logged no errors. The fault-logging path was not asserted |
| Statics analyzer | Finding, fixed | The old Static Event template produced `UAL0010` and `UAL0013` in both namespace configurations. The `[AutoStaticsCleanup]` version compiled with no diagnostics on 6000.7.0b4 and 6000.6.2f1 |
| Static Event reset across Plays | Not verified | Compile only; two consecutive Plays were not run |
| Test and NetworkBehaviour templates | Not re-run | They need Test Framework and Netcode; last validated earlier (Netcode 3.1.0) |
| Editors before 6.6 | Not verified | The attribute does not exist there; the guide supplies the manual-reset fallback |

## Scene templates re-verification — 2026-10-21

Re-ran the delivery harness from [Tools~](AuditInstructions/SceneTemplates/Tools~/README.md) against the
current shipped files, in fresh `com.unity.template.urp-blank` projects, importing at
`Assets/StrategyStarter/SceneTemplates` (not the authoring path):

| Editor | URP | Input System | Test Framework | Scenes generated and reopened | EditMode | PlayMode |
|---|---|---|---|---|---|---|
| 6000.7.0b4 | 17.7.0 | 6.7.0 | 1.9.0 | 6 of 6 | 6 of 6 | 2 of 2 |
| 6000.6.2f1 | 17.6.0 | 1.20.0 | 1.8.0 | 6 of 6 | 6 of 6 | 2 of 2 |

No compiler, import, or missing-reference diagnostics were logged in either project (the only
errors were local Unity licensing handshake messages). The runtime scripts hold no static state, so
Enter Play Mode without domain reload needs no handling.

Not verified: the New Scene dialog itself (batch runs use `SceneTemplateService.Instantiate`), the
player build and graphical capture steps, other GPUs and Windows, device feel, Editors before 6.6, and a
Built-in or HDRP project (documented as unsupported, not tested).

## Version control rules — 2026-10-21

The starter [ignore and attribute files](AuditInstructions/VersionControl/README.md) were checked in
throwaway Git repositories (Git 2.54, Git LFS 3.8.0) and in a Unity 6000.7.0b4 URP project with Unity CLI
1.0.0-beta.13:

- `Tools/validate_all.py` builds a repository, installs both files, and asserts with `git check-ignore`
  and `git check-attr`: 38 generated or excluded paths ignored, 17 required paths tracked (all `.meta`
  files, `ProjectSettings`, `Packages/manifest.json`, `packages-lock.json`, and folders that merely
  resemble excluded ones), 7 paths routed to LFS, and `eol=lf` for text types. Removing the optional
  ThirdPartyAssets or LFS section leaves a working file.
- `unity vcs doctor` (19 checks, 18 after excluding `META_FILES_IGNORED`) found nothing on the installed
  files with LFS hooks present. The excluded check is the deliberate ThirdPartyAssets exclusion: doctor
  flags any ignored `.meta`. The previous root `.gitignore` produced `GITIGNORE_STALE` (16 missing rules).
- `unity vcs merge-setup` wrote its managed attributes block and driver beside these files, and its
  test merge passed.

Not verified: an existing large repository, LFS against a real remote, Windows line endings, merge setup
without the CLI, and a clean-clone import of a project with ThirdPartyAssets excluded.

## Continuous integration without a licence — 2026-10-21

The [CI starter files](AuditInstructions/ContinuousIntegration/README.md) were exercised locally, in an empty
home directory with no Unity sign-in or licence, against a fresh clone of a Unity 6000.7.0b4 URP project
(Unity CLI 1.0.0-beta.13, .NET SDK 10.0.302, Git 2.54):

- `check_unity_project.py` passed the project (87 assets paired with `.meta` files, 8 tests in 2 files) and,
  in `Tools/validate_all.py`, passes one clean and fails seven broken fixture projects.
- `unity vcs doctor` ran licence-free and exited 4 on a genuine finding, 0 when clean.
- `dotnet format whitespace` and `dotnet format style --diagnostics IDE1006` passed on the shipped sample
  scripts and failed on injected violations, using only the shipped `.editorconfig`.

Not verified: any run on a GitHub-hosted or self-hosted runner, `unity ci init` end to end, Windows and
macOS runners, and `git lfs install --local` behavior on a hosted checkout.

## CoreCLR migration guide — 2026-10-26

[CoreCLRUpgrade.md](AuditInstructions/CoreCLRmigration/CoreCLRUpgrade.md) was restructured and checked statically only:
relative links and the "Last verified" date through `Tools/validate_all.py`. No Unity Editor, CoreCLR build, or
project was used, and the API names, forum claims, and workflow were not re-checked against current sources
(see [recheck.md](AuditInstructions/CoreCLRmigration/Tools~/recheck.md)).

Not verified: the workflow end to end, attribute availability on a Unity 7.0 Alpha Editor, and any 6.7 experimental player.

## Review contract rollout — 2026-10-26

Checked statically only. A script confirmed the `AGENTS.md` block appears byte-for-byte in 12 covered agent
documents, `Tools/validate_all.py` enforces the heading, the phrase "explicit yes" and the placement before step 1,
and every folder validator (CI, presets, scene templates, script templates, version control, CLI example) passes.

Not verified: that an LLM given one of these URLs actually stops at the confirmation gate, picks a subset correctly, or
behaves in a non-interactive session. Run each document once against a disposable project and record the transcript.
The overall validator still prints 16 missing-link errors for `Testing/IntroductionToTesting.md`, which pre-date this
work and are the only remaining errors.

## GitHub collaboration workflow — 2026-10-26

Expanded [GithubInstructions.md](AuditInstructions/Github/GithubInstructions.md) and added its
[human overview](AuditInstructions/Github/README.md), with AGENTS/topic-index routing. Sources reviewed:
UnityTycoonManager's GitHubIssues, PRCompletion and WorktreeRecovery guides, relevant project rules,
ticket-capture and scoped-commit skills, and the "Review and complete open PRs" session's branch/art
preservation outcomes. Reusable guidance keeps target-specific permissions, IDs and recovery internals
out of the starter. Included the current repository's verbatim review/selection/confirmation contract.

- Confirmed rendered REST bodies, closing-keyword timing, and merge-method behavior against linked
  official GitHub documentation. No GitHub issues, PRs, boards or branches were changed.
- Passed scoped `Tools/validate_all.py` checks for AGENTS.md, the topic index, both GitHub documents,
  CHANGELOG.md and this record: 6 Markdown files, 77 local links/anchors, 75 unique GUIDs, 6 folder
  validators. Ran with PATH restricted to system tools to exclude .NET restore/style checks; the
  initial unrestricted validator did not return promptly. CI reported its style gates Not verified.
- Passed focused review of six numbered steps/completion criteria, absence of copied project paths/IDs,
  and whitespace checks for edited documentation.
- Full Markdown scanning reported 16 unresolved links in the existing
  `LLMInstructions/Testing/IntroductionToTesting.md`, outside this change. The first scan also caught
  the newly introduced review-contract requirement; corrected the GitHub guide and verified it in the
  passing scoped run. The full repository is not claimed clean.

Not verified: end-to-end capture/implementation/PR/merge/cleanup against a live GitHub repository,
private-attachment retrieval in this session, .NET style gates, or any Unity Editor/test/build run.
This change is documentation only.

## Review contract gate test — 2026-10-26

Two fresh general-purpose agents, each given only the document path and a one-line request (as a user would hand over
a URL), ran against disposable fake projects with a git baseline (no Editor attached):

| Check | Result | Scope/limits |
|---|---|---|
| MobileBuilds.md stops after audit and recommendations | Passed | 26 numbered recommendations plus 10 questions; `git status` clean afterwards |
| SetupFolders.md stops after audit and recommendations | Passed | 8 recommendations (R1 the only default "do"); no folder created |
| Partial pick (R1 only, no yes) | Passed | Agent restated the single `mkdir`, left `Assets/Scenes` and R2 to R8 alone, wrote nothing |
| Relayed "yes" from the coordinating agent | Refused | Agent required the user's own confirmation; folder still absent. Stricter than needed, and the intended behavior |
| Apply after the user's own yes | Not verified | A subagent harness cannot supply a genuine user yes; needs a manual run |

The relayed "yes" was refused a second time even when it passed on the user's authorization for the sandbox, so apply-after-confirm
needs a manual run where the user types the yes to the agent directly.

Observations: the Mobile agent flagged `AndroidTargetArchitectures: 1` as probably ARMv7 but was unsure of the enum value.
Not confirmed: neither installed Editor (6000.7.0b4, 6000.7.0b6) has the Android module, and Unity's published
`AndroidArchitecture` reference lists the members (None, ARMv7, ARM64, All) without numeric values. MobileBuilds.md names the
enum members rather than numbers, so it is unaffected; install the Android module and read the enum before quoting a value. It also reached the ProjectSettings.asset YAML-edit rule and planned an
`-executeMethod` route instead of hand edits, as the document intends.

## Project review rollout — 2026-10-26

Fifteen lenses and the router were pressure-tested by five independent reviewers (fact-check, audit-worthiness, overlap, hygiene), then edited per an
approved keep/merge/cut table. A fresh agent, given only `ProjectReview.md`, then ran the review read-only (static inspection only, no Editor, Unity CLI,
tests, or builds) against a real 3D tycoon project on Unity 6000.7.0b4 (642 owned C# files, 10 scenes).

| Check | Result | Scope/limits |
|---|---|---|
| Project left untouched | Passed | `git status` plus HEAD hash identical before and after (`e485ef7f4b98`), twice; 5 pre-existing modified doc files unchanged |
| Detection and menu | Passed after two rounds | Round 1 found 11 document defects (uGUI signal matched UI Toolkit, vendor counts, paths with spaces, stage and step numbering, scope and fallback gaps); round 2 found 12 more (lens precedence over project-local copies, first-party definition, Recommended/Optional thresholds, weak-signal rules for physics, animation, audio, persistence, assemblies, testing); all fixed in the hub |
| Full review of 11 detected lenses | Completed | No confirmed corruption, data loss or leaks; 13 numbered recommendations, mostly drift (setting mismatch, unused defines, tags, temp folders); false-positive sources recorded per lens and fixed in 7 lenses |
| Integrity pass | Completed statically | 14,765 `.meta` files, 0 duplicate GUIDs, 0 orphans, 0 unresolved first-party script GUIDs |
| Apply-after-confirm | Not verified | The review never reached confirm; a subagent cannot supply a genuine user yes |
| Live checks | Not verified | Missing references, import warnings, Play-session behaviour, tests, frame time, memory, builds |

Not verified: the round-2 hub fixes were not re-run through a third dry-run, the lens text was fact-checked mostly against 6000.0 and 6000.6 pages (6000.7 pages
where the URLs say so), and Input System claims were checked against package 1.14. The `[AutoStaticsCleanup]` attribute is documented from Unity 6.5; the
`OnCodeInitializing` option for new code is cited from the `SubsystemRegistration` reference and not tested.

## Package installer rewrite — 2026-10-26

| Check | Result | Scope/limits |
|---|---|---|
| Project left untouched | Passed | `git status` hash `97bbb1bf4278` identical before and after both dry-runs; HEAD `ce080424a629` |
| Real project (Unity 6.7.0b4) | Completed | 0 installs recommended: Test Framework, Cinemachine, Input System already direct core packages; Addressables not detected. 103 NUnit files exist in `Assets/Editor/Tests` with no asmdef |
| Synthetic project (Unity 6000.0, missing packages) | Completed | Found: Input System and Cinemachine 2 code with the packages missing, Test Framework transitive-only, vendor Addressables correctly excluded |
| Document defects | Fixed | 13 from the synthetic run and 12 from the real run, including the Cinemachine 2 rule, owned-scope definition, Already direct label, stale-lockfile handling |
| Contract block | Passed | Identical to the AGENTS.md canonical block; heading before step 1 |
| Repository validator | Passed after the folder split | `Tools/validate_all.py` was repointed to `AuditInstructions/` and `AgentsInstructions/`; 430 links, 6 folder validators |
| Install, verify, Editor routes | Not verified | No package was installed and no Editor was run; the `Client.Add` behaviour for an already-core package is expected, not tested |

Not verified: the post-fix document was not re-run through a third dry-run. Core package facts come from the 6000.7 core packages page, the 6.6 upgrade guide and the
`Client.Add` and `VersionsInfo` references; the 6000.0 core list was read by the synthetic run only.

## Repository split — 2026-10-26

| Check | Result | Scope/limits |
|---|---|---|
| Broken links | Fixed | 89 found; 88 rewritten by a layout mapping (old file location to new), 1 prose list edited by hand |
| Repository validator | Passed | 67 Markdown files, 430 local links/anchors, 75 unique GUIDs, 6 folder validators |
| Naming checker | Passed | `AgentsInstructions/CodeStyleGuide/Tools~/check_naming.py`: 0 diagnostics on Good, 6 on Bad (expected) |
| Project untouched | Passed | Railroad Tycoon status hash `97bbb1bf4278` unchanged |

Not verified: raw GitHub URLs in five install guides (they resolve after the push). Pre-existing stale text outside the split: the README copy table still lists `SetupInstructions/`,
`AuditGuides/` and `ExampleCode/`, and `AuditInstructions/SceneTemplates/Tools~/readme.md` refers to deleted `Tools/validate_starter.py` and `Tools/resource-inventory.json`.

## README.md standardisation — 2026-10-26

| Check | Result | Scope/limits |
|---|---|---|
| Rename | Done | 18 files renamed through a temporary name, 0 `readme.md` remain; the new folders are untracked, so git records the new names when they are added |
| Repository validator | Passed | 67 Markdown files, 430 local links/anchors, 6 folder validators |
| Case-exact link check | Passed, and the negative test failed as intended | A temporary `InstallPackages.MD` link was reported and then removed |

## Installation and delivery workflows — 2026-10-26

| Check | Result | Scope/limits |
|---|---|---|
| Integrated repository validator | Passed | 74 Markdown files, 466 local links/anchors, 75 unique GUIDs, six folder validators, and 10 audit regression tests; --require-dotnet enabled |
| Reference installation | Passed | Temporary project snapshot, rebased root AGENTS/CLAUDE links, local anchors/exact case, and root EditorConfig; all four intentionally broken-link probes rejected |
| New agent-document contracts | Passed | KitMaintenance, Testing, and ReleaseReadiness contain the canonical contract verbatim before step 1; each of five steps has a Done criterion |
| Required SDK failure | Passed | CI topic validator with dotnet absent and STARTER_REQUIRE_DOTNET=1 returns failure rather than reporting skipped style gates as success |
| Repository workflow syntax | Passed | Parsed with Ruby YAML; action versions and selected inputs checked against upstream action.yml files |
| Naming intersections | Passed | .NET SDK 10.0.302: Good fixture 0 diagnostics, Bad fixture 6 intended IDE1006 diagnostics |
| Topic validation | Passed | .NET clean/bad style gates, 19 CI fixture projects, preset/template/scene inventories, version-control fixtures, and CLI example identities |
| Audit regression path portability | Passed | Resolved temporary fixture root so macOS /var and /private/var aliases compare consistently; all 10 tests pass |

The initial sandboxed .NET runs could not create Roslyn's local build-host pipe (SocketException:
Permission denied). The successful naming and style checks ran with the required local pipe access.
No Unity import, gameplay tests, player build, device acceptance, installation into an actual game,
three-way update against a customized game, release rehearsal, or hosted GitHub Actions run was
performed. These are static/workflow changes; no shipped Unity assets or metadata were edited.

Sources checked in October 2026: [Unity test assemblies](https://docs.unity3d.com/Packages/com.unity.test-framework@latest),
[assembly references](https://docs.unity3d.com/Manual/assembly-definitions-referencing.html),
[Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[checkout inputs](https://raw.githubusercontent.com/actions/checkout/v7/action.yml),
[setup-python inputs](https://raw.githubusercontent.com/actions/setup-python/v7/action.yml), and
[setup-dotnet inputs](https://raw.githubusercontent.com/actions/setup-dotnet/v6/action.yml).
The test-assembly page was inspected at package 1.4.6; actual target execution must confirm its
installed Test Framework and Editor options. Release guidance intentionally specifies evidence and
ownership rather than embedding volatile store requirements.


## Preset compatibility evidence

This table qualifies the earlier preset results; it does not replace their historical observations.
The later model failure is supplied session feedback, not a reproduced failure in this repository.
Missing original revisions/fixture identifiers are explicitly unknown rather than inferred from the
current preset assets. The same Editor version alone does not make two test contexts equivalent.

| Evidence | Editor / host | Preset revision | Importer | Operation | Fixture | Result | Limitations |
|---|---|---|---|---|---|---|---|
| Earlier recorded disposable run (October 2026) | 6000.7.0b4 / macOS Apple Silicon | Exact source commit not recorded in original result | AudioImporter | Preset Manager first import | Disposable-project audio; exact fixture IDs not recorded | Passed in that run | No universal project/version compatibility claim |
| Earlier recorded disposable run (October 2026) | 6000.7.0b4 / macOS Apple Silicon | Exact source commit not recorded in original result | ModelImporter | Preset Manager first import | Disposable-project model; exact fixture IDs not recorded | Passed in that run | Does not establish every FBX/rig/model configuration |
| Earlier recorded disposable run (October 2026) | 6000.7.0b4 / macOS Apple Silicon | Exact source commit not recorded in original result | TextureImporter | Preset Manager first import | Disposable-project textures; exact fixture IDs not recorded | Native application crash observed | Initial import then explicit ApplyTo/SaveAndReimport was the tested alternative |
| User-supplied pressure-test feedback (reviewed 2026-10-26) | 6000.7.0b4 / host not supplied | Unknown | ModelImporter | First import with defaults | Project fixture/log not supplied | Model crash reported in that project history | Not reproduced here; cause and relationship to earlier pass unresolved |

## Preset workflow refinements — 2026-10-26

Implemented the approved R1–R9 documentation and validation-coverage changes while preserving
pre-existing working-tree edits. No preset asset bytes or metadata were changed. The standalone
workflow now distinguishes first installation from tested Editor updates, preset identity from
customization, matching from import behavior, and live configuration from disk persistence.

| Check | Result | Scope/limits |
|---|---|---|
| Preset resource and scenario validation | Passed | 13 partial presets; GUID table/inventory match; nine structurally valid decision scenarios |
| Preset replay regressions | Passed | Three tests: decision/audit prompt boundaries and withheld grading; existing output preservation; repository output rejection |
| Isolated publication snapshot | Passed | Integrated validator with --require-dotnet: 75 Markdown files, 472 links/anchors, 75 GUIDs, six folder validators, 10 shared audit tests, 22 CI fixtures and .NET style gates |
| Roslyn naming intersections | Passed | .NET SDK 10.0.302; Good fixture zero IDE1006 diagnostics, Bad fixture six expected diagnostics |
| Concurrent checkout preservation | Verified for publication | Commit prepared from HEAD plus preset-only changes; pre-existing and concurrent workflow edits excluded from publication and retained locally |

The isolated snapshot excludes unrelated working-tree work, so its shared regression count differs
from the current checkout. Preset checks do not imply that the nine agent decisions or Unity operations
were exercised. The initial sandboxed integrated-check attempt required a rerun with local .NET
access; the isolated publication run above completed successfully.

Not verified in this change: fresh-agent grading of the nine new decision scenarios, a Unity
update/save helper, actual first-import filters/persistence/no-op behavior, model crash reproduction,
player builds, or profiling. The disposable-project procedure defines those checks without claiming
they ran. No Unity project is part of this documentation repository.

Sources checked for the review in October 2026: Unity's
[Preset Manager filter documentation](https://docs.unity3d.com/cn/current/Manual/class-PresetManager.html),
[GetDefaultPresetsForType signature](https://docs.unity3d.com/ScriptReference/Presets.Preset.GetDefaultPresetsForType.html),
and [SetDefaultPresetsForType signature and example](https://docs.unity3d.com/ScriptReference/Presets.Preset.SetDefaultPresetsForType.html).
The setter page still mentions the older getter in prose; use installed signatures rather than that
stale name. No universal targeted-save API or tested identity-preserving update implementation is
asserted by these documentation changes; the guide requires target-version discovery and validation.


## Independent publication: authorization contract — 2026-10-26

Group 1 is validated as its own cumulative publication snapshot, excluding changes assigned to
later groups and edits arriving after capture. The staged content is checked against this snapshot
before committing. Validation results follow.

| Check | Result | Scope/limits |
|---|---|---|
| Full repository validator with required .NET gates | Passed | Group 1: 75 Markdown files, 472 local links/anchors, 75 unique GUIDs, 6 folder validators; 12 shared regression tests; 22 CI fixtures and required style gates |
| Roslyn naming intersections | Passed | Group 1: .NET SDK 10.0.302; Good fixture zero IDE1006 diagnostics, Bad fixture six expected diagnostics |
| Replay execution | Not performed | Static fixtures are not observed agent or Unity behavior |

No Unity assets or metadata changed. No Editor imports, gameplay tests, or player builds were run.


## Independent publication: review evidence and acceptance — 2026-10-26

Group 2 is validated as its own cumulative publication snapshot, excluding changes assigned to
later groups and edits arriving after capture. The staged content is checked against this snapshot
before committing. Validation results are recorded below after execution.

| Check | Result | Scope/limits |
|---|---|---|
| Full repository validator with required .NET gates | Passed | Group 2: 75 Markdown files, 472 local links/anchors, 75 unique GUIDs, 6 folder validators; 12 shared regression tests; 22 CI fixtures and required style gates |
| Roslyn naming intersections | Passed | Group 2: .NET SDK 10.0.302; Good fixture zero IDE1006 diagnostics, Bad fixture six expected diagnostics |
| Replay execution | Not performed | Static fixtures are not observed agent or Unity behavior |

No Unity assets or metadata changed. No Editor imports, gameplay tests, or player builds were run.


## Independent publication: workflow corrections and replay evidence — 2026-10-26

Group 3 is validated as its own cumulative publication snapshot, excluding changes assigned to
later groups and edits arriving after capture. The staged content is checked against this snapshot
before committing. Validation results are recorded below after execution.

| Check | Result | Scope/limits |
|---|---|---|
| Full repository validator with required .NET gates | Passed | Group 3: 75 Markdown files, 475 local links/anchors, 75 unique GUIDs, 6 folder validators; 14 shared regression tests; 22 CI fixtures and required style gates |
| Roslyn naming intersections | Passed | Group 3: .NET SDK 10.0.302; Good fixture zero IDE1006 diagnostics, Bad fixture six expected diagnostics |
| Replay execution | Not performed | Static fixtures are not observed agent or Unity behavior |

No Unity assets or metadata changed. No Editor imports, gameplay tests, or player builds were run.

Replay-archive integrity validation passed for all four retained phases: 207 unique fresh-agent
executions, 152 observed case IDs, verified source hashes/quotations and consistent aggregate verdicts.
The expanded phase remains partial (42/103 graded); its two failures and two unverified outcomes are
retained. The local live replay directories are not modified or retired by publication.

The publication catalog generates 204 current prompts. The expanded historical checkpoint generated
213 from its frozen catalog; its observed results are attributed to those original inputs, not to
the current catalog or current guide revisions.
