> How it works: give the URL of [ProjectReview.md](ProjectReview.md) to your agent. It audits your
> Unity project, shows which reviews apply (animation, physics, UI, audio and more), lets you pick the
> ones you want, reports findings with recommendations, and changes nothing until you choose and confirm.

# Project review

A review is a long checklist, so this folder lets you run the part you care about. One entry document
runs the workflow. The checklists themselves are **lenses**: small files, one per recurring risk. The
agent loads only the lenses you pick, so a quick check stays quick.

Example prompt: *"Review my Unity project with this document. I mostly care about performance and
scene lifecycle."*

## What happens when you hand it over

1. **Audit.** The agent reads your project, records what it contains, and writes nothing.
2. **Choose.** It shows every lens as **Recommended** (with the evidence it found) or **Not detected**.
   You pick a shortcut or any subset.
3. **Review.** It runs the lenses you picked and reports confirmed defects, measured costs, convention
   drift, and design proposals separately, each with evidence.
4. **Recommend and confirm.** Findings become numbered recommended fixes. You pick any subset, and the
   agent presents the exact changes, intended outcome, and acceptance check. Explicit implementation
   instructions can select and authorize already-presented changes; choosing IDs alone selects scope.

## Pick your review

| I want… | Choose |
|---|---|
| A fast health check | **Quick health check**: integrity pass, naming and organization, performance, scenes and lifecycle, assets and memory |
| Everything that applies to my project | **Full review**: the integrity pass, base checks, and every lens marked Recommended |
| Only certain areas | **Custom**: name the lenses |
| To fix one specific bug | **Diagnose a defect**: hand over the symptom instead of a scope |

## The lenses

| Lens | Reviews | Runs when the project has |
|---|---|---|
| Integrity pass | Duplicate or missing GUIDs, orphaned `.meta` files, unresolved script references | Always, for a whole-project review |
| [Performance](UnityPerformanceOptimizationInstructions.md) | Allocations, hot-path cost, pooling, jobs | Runtime C# code |
| [Rendering correctness](UnityRenderingInstructions.md) | Renderer features/passes, Render Graph resources, camera stacks, shader compatibility | Owned custom rendering or a configured camera stack |
| [Assets and memory](UnityAssetsAndMemoryInstructions.md) | Load and release ownership, import cost, Addressables | Imported assets |
| [Scenes and lifecycle](UnityScenesAndLifecycleInstructions.md) | Startup, scene flow, async lifetime, repeated Play, destroyed objects | Scenes or MonoBehaviours |
| [Design](UnityDesignPatternsInstructions.md) | Command ownership, dependencies, state transitions (proposals unless state is corrupted) | Owned C# with shared state |
| [Persistence](UnityPersistenceInstructions.md) | Save and load, migrations, settings | Save or load code |
| [UI Toolkit](UnityUIToolkitInstructions.md) | UXML and USS, bindings, recycled rows | UI Toolkit assets |
| [uGUI](UnityUGUIInstructions.md) | Canvas layout, listeners, input module | A Canvas or EventSystem |
| [Input](UnityInputSystemInstructions.md) | Actions, UI and gameplay arbitration, rebinding | The Input System |
| [Physics](UnityPhysicsInstructions.md) | Contacts, movement, query completeness (3D) | Rigidbodies or colliders |
| [Animation](UnityAnimationInstructions.md) | Animator state, interruption, root motion | Animator controllers |
| [Audio](UnityAudioInstructions.md) | Mixer routing, volume units, voice lifecycle | Mixers or AudioSources |
| [Assemblies](UnityAssemblyDefinitionsInstructions.md) | Compile boundaries, test isolation, build content | Asmdefs or tests |
| [Testing](UnityTestingInstructions.md) | Whether tests would catch a regression, fixtures, result evidence | Tests, or none |
| [Editor tooling](UnityEditorToolingInstructions.md) | Integrity pass, plus Undo and saved results for Editor tools | Owned `Editor/` code |

## Good to know

- **Detection decides the menu, not the verdict.** A lens that finds nothing to review is recorded as
  Not applicable. You can still run one the agent did not recommend.
- **A finding is evidence, not a search hit.** The agent must read the enclosing code, follow callers,
  and honor your project's documented choices before it reports anything.
- **Static review has limits.** Without the Editor, a device, or a build, runtime and saved-scene
  checks are reported **Not verified**; a clean static result never claims they passed.
- **Reviews are read-only.** Fixes happen only for recommendations you pick and confirm.
- **Coverage is explicit.** Navigation, networking, Physics2D, DOTS, and other detected systems without
  a lens are listed as **Outside coverage**, with evidence and the specialist checks not performed.
  Full review covers selected lenses; it does not certify every subsystem. A separate scoped review
  can use version-matched official documentation. One-time setup belongs to
  [SetupInstructions](../SetupInstructions/README.md). C# naming and formatting live in the
  [style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md); the base checks apply it.

## Diagnosing a bug instead

[UnityDebuggingInstructions.md](UnityDebuggingInstructions.md) is not a review. Hand it a symptom, and
the agent captures the failing context, routes the symptom to the owning lens, and works through
reproduce, hypothesize, probe, fix, and regression test.
