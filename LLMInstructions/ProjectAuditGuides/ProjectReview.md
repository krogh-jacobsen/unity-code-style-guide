# Unity project review

The entry point for every audit, change review, or subsystem review. This file holds the shared
loading rules, workflow, evidence standard, and lens index. The other files in this folder are
on-demand review lenses: failure risks, evidence to inspect, and validation that closes a finding.
Implementation recipes, tool setup, and API catalogs belong in skills or official documentation.

An invoked broader audit skill can extend scope, reporting, test authorization, and plan
reconciliation. `unity-project-review` owns generic pitfall review; lenses supply focused evidence
checks without repeating the base recipes.

Table of contents:
- [Loading and authority](#loading-and-authority)
- [1. Establish sources and scope](#1-establish-sources-and-scope)
- [2. Check integrity, then conformance](#2-check-integrity-then-conformance)
- [Select a lens](#select-a-lens)
- [3. Fill live and test evidence gaps](#3-fill-live-and-test-evidence-gaps)
- [4. Report and finish](#4-report-and-finish)
- [Evidence standard](#evidence-standard)
- [Maintenance](#maintenance)

## Loading and authority

- ✅ Read the project's `AGENTS.md` first. Its choices and the user's scope govern the review.
- ✅ Establish the actual engine version, packages, target platform, and owned code before applying a
  check. Report a mismatch with a binding project choice; do not silently change the stack.
- ✅ Select lenses by the behavior being reviewed. Trace its dependencies into other lenses only when
  needed. A whole-project audit covers all applicable areas; a button edit does not load the folder.
- ⚠️ Treat examples and recommendations as guidance. A documented no-asmdef policy, composition-time
  injection, or supported legacy UI is not a defect just because a generic template prefers another
  approach. Record unresolved conflicts with both sources.
- ℹ️ Skills own execution. Prefer Unity CLI for Editor inspection, tests, and builds; discover
  commands and target the intended project explicitly. Use an available matching skill for
  implementation or diagnosis. If unavailable, use project tooling and version-matched official docs;
  these guides remain usable without a particular plugin. Skill defaults do not override project
  decisions.

## 1. Establish sources and scope

Locate the project's current `AGENTS.md`, style guide, audit guides, and setup instructions. This
repository keeps them in `CodeStyleGuide/`, `AuditGuides/`, and `SetupInstructions/`; discover their
actual location in the target project. Missing sources leave the affected conformance checks
Not verified; continue independent review rather than substituting remembered rules.

Use the user's selected project/folder/change scope. If unspecified, state the first-party scope
and exclusions; ask only when an unresolved choice materially changes the review. Record the base
revision for change review, working-tree state, engine/package versions, platform, and selected stack.
Read actual project settings as evidence; a mismatch with a binding project rule is a finding.

A whole-project audit covers every family in step 2 and every applicable lens. For narrower work,
select the behavior and its relevant dependencies. Preserve concurrent edits and unsaved scenes
throughout inspection.

## 2. Check integrity, then conformance

Check asset identity before conventions. The [Editor tooling](UnityEditorToolingInstructions.md) lens
owns GUID, metadata, serialized rename/enum, and saved-reference checks. Inspect vendor metadata if
needed for database-wide integrity; exclude vendor/generated source from style review unless requested.

These families have no lens of their own; everything else is covered by [a lens](#select-a-lens).

| Check family | Source of truth | Evidence to inspect |
|---|---|---|
| Naming and formatting | [Style guide](../CodeStyleGuide/UnityStyleGuide.md) and project `.editorconfig` | Prefix/casing exceptions, modifiers, fields/properties, braces, actual code |
| Class organization | Project/style guide | Member order, MonoBehaviour/file identity, approved region usage |
| API/stack compatibility | Project tech stack and installed source/official docs | Actual versions, obsolete API availability, selected input/UI/pipeline |
| Structure and settings | Project rules and [setup index](../SetupInstructions/README.md) | Intended folder/settings policy versus actual state |

⚠️ Every search pattern is a candidate. Read enclosing code and callers; honor documented project
choices. Avoid automatic findings from all lambdas, all statics, missing asmdefs, any Resources
folder, or a version-independent CSS/API ban list. Confirm the actual failure or binding rule.

## Select a lens

| Review scope | Lens | Skills that own related execution, when available |
|---|---|---|
| CPU/GPU cost, allocations, pooling, jobs | [Performance](UnityPerformanceOptimizationInstructions.md) | `unity-project-review`, `optimize-web`, Render Graph validation |
| Asset residency, load/release ownership, import cost | [Assets and memory](UnityAssetsAndMemoryInstructions.md) | `prepare-unity-3d-asset`, `optimize-audio`, sprite atlas skills |
| Responsibilities, command boundaries, dependencies | [Design](UnityDesignPatternsInstructions.md) | `codebase-design`, `unity-project-review` |
| Startup, scene transitions, async lifetime, repeated Play | [Scenes and lifecycle](UnityScenesAndLifecycleInstructions.md) | `unity-cli`, `unity-project-review` |
| Save/load, migrations, player settings | [Persistence](UnityPersistenceInstructions.md) | Project save tooling, `tdd` for test-first implementation |
| Runtime UXML/USS, bindings, recycled rows, UI input | [UI Toolkit](UnityUIToolkitInstructions.md) | `ui` / `ui-uitk` |
| Existing Canvas UI | [uGUI](UnityUGUIInstructions.md) | `ui-ugui`, `optimize-text-mesh-pro` |
| Action ownership, gameplay/UI arbitration, rebinding | [Input](UnityInputSystemInstructions.md) | `unity-cli` for asset inspection |
| 3D body movement, contacts, query completeness | [Physics](UnityPhysicsInstructions.md) | `physics-3d-collision` |
| Animator state, interruption, root motion | [Animation](UnityAnimationInstructions.md) | `unity-cli` for controller/clip inspection |
| Mixer routing, settings, voice lifecycle | [Audio](UnityAudioInstructions.md) | `audio-setup-mixers`, `optimize-audio` |
| Compilation, Editor/player/test isolation, representative build | [Assemblies](UnityAssemblyDefinitionsInstructions.md) | `unity-project-review`, project build tooling |
| Behavioral coverage, fixtures, test-result evidence | [Testing](UnityTestingInstructions.md) | `tdd`, `unity-cli`, repository test runner |
| Saved asset integrity, Undo, migrations, Editor tools | [Editor tooling](UnityEditorToolingInstructions.md) | `unity-cli`, `ui-uitk` / `ui-imgui` |
| Unity-specific diagnostic evidence | [Debugging](UnityDebuggingInstructions.md) | `diagnosing-bugs`, `physics-3d-collision` |

ℹ️ C# naming and formatting stay in [the style guide](../CodeStyleGuide/UnityStyleGuide.md). One-time
configuration stays in [SetupInstructions](../SetupInstructions/README.md).

## 3. Fill live and test evidence gaps

Use `unity-cli` for Editor inspection and the repository runner for authorized tests; follow any
required test-runner subagent. Read-only queries of the current state do not need repeated permission
when already authorized. Preserve dirty scenes; use saved-asset inspection or isolated scenes for
checks that need different content. Obtain missing authorization only for additional disruptive
live actions outside the current scope.

If the Editor, runner, device, or build is unavailable, record the specific checks Not verified and
continue static work. Parse fresh test results/logs; distinguish failures, exclusions, and not-run tests.

- ❌ Do not call an unopened prefab correct from source alone.
- ❌ Do not claim a live repair is saved.

## 4. Report and finish

Use the invoked workflow's output format and the user's progress/handoff preferences. Each finding
meets the [evidence standard](#evidence-standard). Separate confirmed defects, measured costs,
convention drift, and design proposals. Group one repeated cause with counts and representative
locations; list every affected duplicate-GUID pair. Record conflicts and limits, including inspected
samples and whether live/tests/build checks ran.

Apply fixes only when authorized. Selected fixes preserve serialized identity, follow the matching
implementation skill/project workflow, and run relevant validation before closure.

⚠️ A review request alone does not select its recommendations for implementation. Unselected
proposals remain proposals; mark plans implemented only when their actual work and required
validation are complete.

## Evidence standard

A search hit is a candidate. Read the enclosing code, callers, ownership, and applicable settings
before reporting it. Follow per-frame helper calls; inspect release, cancellation, and failure paths.
Exclude generated and vendor code from style review unless scoped in. Vendor metadata may still
matter to a project-wide GUID integrity check.

For each selected check family or lens, record **Checked**, **Finding**, **Not applicable**, or
**Not verified**. State the inspected scope or sample and any missing evidence.

⚠️ Static inspection does not establish runtime behavior, target-device performance, or correct
saved scene/prefab wiring.

A finding needs:
- **Location** and **trigger**
- **Observed evidence** and **consequence**
- **Governing source** — project rule or technical source
- **Smallest useful fix** and **validation**

Rank confirmed corruption, data loss, bugs, and leaks ahead of measured performance problems; label
convention drift and design proposals separately. Combine repeated instances of one cause while
preserving affected locations.

Review is complete when every applicable check family and lens in the selected scope has an outcome,
each finding has inspected evidence, and unverified work is explicit. A clean static review means no
confirmed findings in that scope; it does not imply unperformed runtime checks passed.

## Maintenance

- ✅ Keep one owner per check: general frame cost in Performance, resource residency in Assets, async
  lifetime in Scenes, command ownership in Design, persisted state in Persistence. Other lenses link
  there and add only subsystem-specific failure cases.
- ✅ Keep each lens focused on one recurring risk. Add a lens only for a distinct recurring risk with
  a clear loading condition; update the lens table above and `AGENTS.md` together.
- ✅ Keep existing lens filenames stable for consumers.
- ✅ Verify version-sensitive claims against engine/package source or official Unity docs.
- ❌ Keep tutorial examples, historical project class names, and review logs outside this folder.
