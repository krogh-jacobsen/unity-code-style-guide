# Audit guides for Unity agents

These are on-demand review lenses: failure risks, evidence to inspect, and validation that closes a
finding. Use them during an audit or to review a change in the relevant subsystem. Implementation
recipes, tool setup, and API catalogs belong in skills or official documentation.

## Loading and authority

- Read the project's `AGENTS.md` first. Its choices and the user's scope govern the review.
- Establish the actual engine version, packages, target platform, and owned code before applying a
  check. Report a mismatch with a binding project choice; do not silently change the stack.
- Select guides by the behavior being reviewed. Trace its dependencies into other guides only when
  needed. A whole-project audit covers all applicable areas; a button edit does not load the folder.
- Treat examples and recommendations as guidance. A documented no-asmdef policy, composition-time
  injection, or supported legacy UI is not a defect just because a generic template prefers another
  approach. Record unresolved conflicts with both sources.
- Skills own execution. Prefer Unity CLI for Editor inspection, tests, and builds; discover commands and target the
  intended project explicitly. Use an available matching skill for implementation or diagnosis. If unavailable, use project tooling and version-matched official docs; these guides
  remain usable without a particular plugin. Skill defaults do not override project decisions.

## Evidence standard

A search hit is a candidate. Read the enclosing code, callers, ownership, and applicable settings
before reporting it. Follow per-frame helper calls; inspect release, cancellation, and failure paths.
Exclude generated and vendor code from style review unless scoped in. Vendor metadata may still
matter to a project-wide GUID integrity check.

For each selected check family, record **Checked**, **Finding**, **Not applicable**, or **Not verified**.
State the inspected scope or sample and any missing evidence. Static inspection does not establish
runtime behavior, target-device performance, or correct saved scene/prefab wiring.

A finding needs: location, trigger, observed evidence, consequence, governing project rule or
technical source, smallest useful fix, and validation. Rank confirmed corruption, data loss, bugs,
and leaks ahead of measured performance problems; label convention drift and design proposals
separately. Combine repeated instances of one cause while preserving affected locations.

Review is complete when every applicable check family in the selected scope has an outcome, each
finding has inspected evidence, and unverified work is explicit. Follow the invoked audit skill for
report layout, test authorization, plan reconciliation, and handoff. A review request alone does not
select its recommendations for implementation.

## Select a guide

| Review scope | Guide | Skills that own related execution, when available |
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
| Compilation, Editor/player/test isolation | [Assemblies](UnityAssemblyDefinitionsInstructions.md) | `unity-project-review`, project build tooling |
| Behavioral coverage, fixtures, test-result evidence | [Testing](UnityTestingInstructions.md) | `tdd`, `unity-cli`, repository test runner |
| Saved asset integrity, Undo, migrations, Editor tools | [Editor tooling](UnityEditorToolingInstructions.md) | `unity-cli`, `ui-uitk` / `ui-imgui` |
| Unity-specific diagnostic evidence | [Debugging](UnityDebuggingInstructions.md) | `diagnosing-bugs`, `physics-3d-collision` |

C# naming and formatting stay in [the style guide](../CodeStyleGuide/UnityStyleGuide.md). One-time
configuration stays in [SetupInstructions](../SetupInstructions/README.md). Full project review uses [the conformance workflow](ProjectReview.md), extended by the target
project's selected audit tooling and plan convention where applicable.

## Maintenance

Keep one owner per check: general frame cost in Performance, resource residency in Assets, async
lifetime in Scenes, command ownership in Design, persisted state in Persistence. Other guides link
there and add only subsystem-specific failure cases. Keep existing filenames stable for consumers.
Add a guide only for a distinct recurring risk with a clear loading condition; update this index
and `AGENTS.md` together. Verify version-sensitive claims against engine/package source or official
Unity docs. Keep tutorial examples, historical project class names, and review logs outside this folder.
