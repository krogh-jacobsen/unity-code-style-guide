# Unity guide-conformance audit

Review a Unity project's owned code, saved wiring, and settings against its documented conventions.
This is the base conformance workflow. An invoked broader audit skill can extend scope, reporting,
test authorization, and plan reconciliation. `unity-project-review` owns generic pitfall review;
[AuditGuides](README.md) supply subsystem evidence checks without repeating its recipes.

## 1. Establish sources and scope

Locate the project's current `AGENTS.md`, style guide, audit index, and setup instructions. This
repository keeps them in `CodeStyleGuide/`, `AuditGuides/`, and `SetupInstructions/`; discover their
actual location in the target project. Missing sources leave the affected conformance checks
Not verified; continue independent review rather than substituting remembered rules.

Use the user's selected project/folder/change scope. If unspecified, state the first-party scope
and exclusions; ask only when an unresolved choice materially changes the review. Record the base
revision for change review, working-tree state, engine/package versions, platform, and selected stack.
Read actual project settings as evidence; a mismatch with a binding project rule is a finding.

Read the [audit index](README.md) and apply its authority/evidence standard. A whole
project audit covers all applicable families below. For narrower work, select the behavior and its
relevant dependencies. Preserve concurrent edits and unsaved scenes throughout inspection.

## 2. Check integrity, then conformance

Check asset identity before conventions. The Editor tooling lens owns GUID, metadata, serialized
rename/enum, and saved-reference checks. Inspect vendor metadata if needed for database-wide
integrity; exclude vendor/generated source from style review unless requested.

| Check family | Source of truth | Evidence to inspect |
|---|---|---|
| Asset integrity and tools | [Editor tooling](UnityEditorToolingInstructions.md) | Metadata, relevant diffs, saved references, migration paths |
| Naming and formatting | [Style guide](../CodeStyleGuide/UnityStyleGuide.md) and project `.editorconfig` | Prefix/casing exceptions, modifiers, fields/properties, braces, actual code |
| Class organization | Project/style guide | Member order, MonoBehaviour/file identity, approved region usage |
| Hot paths and resources | [Performance](UnityPerformanceOptimizationInstructions.md), [Assets](UnityAssetsAndMemoryInstructions.md) | Reached helper calls, acquisition/release, workload/capture |
| Lifetime and async | [Scenes](UnityScenesAndLifecycleInstructions.md) | Subscription identity, cancellation, registries, repeated Play |
| Design and commands | [Design](UnityDesignPatternsInstructions.md) | Current owner, authoritative command, rejection/repetition effects |
| API/stack compatibility | Project tech stack and installed source/official docs | Actual versions, obsolete API availability, selected input/UI/pipeline |
| Input, UI, physics, animation, audio | Relevant [subsystem lens](README.md#select-a-guide) | Source plus saved/live settings required by the check |
| Assemblies and builds | [Assemblies](UnityAssemblyDefinitionsInstructions.md) | Effective platform/reference/define boundaries, representative build |
| Testing | [Testing](UnityTestingInstructions.md) | Behavioral assertions, fixture cleanup, fresh results and exclusions |
| Save/load | [Persistence](UnityPersistenceInstructions.md) | Snapshot/version/identity, write failure, reconstruction |
| Structure and settings | Project rules and [setup index](../SetupInstructions/README.md) | Intended folder/settings policy versus actual state |

Every search pattern is a candidate. Read enclosing code and callers; honor documented project
choices. Avoid automatic findings from all lambdas, all statics, missing asmdefs, any Resources
folder, or a version-independent CSS/API ban list. Confirm the actual failure or binding rule.

## 3. Fill live and test evidence gaps

Use `unity-cli` for Editor inspection and the repository runner for authorized tests; follow any
required test-runner subagent. Read-only queries of the current state do not need repeated permission
when already authorized. Preserve dirty scenes; use saved-asset inspection or isolated scenes for
checks that need different content. Obtain missing authorization only for additional disruptive
live actions outside the current scope.

If the Editor, runner, device, or build is unavailable, record the specific checks Not verified and
continue static work. Do not call an unopened prefab correct from source alone or claim a live
repair is saved. Parse fresh test results/logs; distinguish failures, exclusions, and not-run tests.

## 4. Report and finish

Use the invoked workflow's output format and the user's progress/handoff preferences. Each finding
needs location, trigger/evidence, consequence, governing source, smallest useful change, and
validation. Separate confirmed defects, measured costs, convention drift, and design proposals.
Group one repeated cause with counts and representative locations; list every affected duplicate-GUID
pair. Record conflicts and limits, including inspected samples and whether live/tests/build checks ran.

Review is complete when every applicable family in the selected scope has an evidence outcome and
all surviving findings have been inspected. A clean static review means no confirmed findings in
that scope; it does not imply unperformed runtime checks passed.

Apply fixes only when authorized. Selected fixes preserve serialized identity, follow the matching
implementation skill/project workflow, and run relevant validation before closure. A review report's
unselected proposals remain proposals; mark plans implemented only when their actual work and required
validation are complete.
