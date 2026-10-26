# Unity defect diagnosis

Load when the user reports a symptom: a Unity runtime/Editor discrepancy, a lifecycle failure, or a
build-only defect. This is a diagnosis mode, not an audit lens: it starts from a reported failure
rather than a review scope, and has no `Finding when` checks of its own. It routes the symptom to the
lens that owns the evidence, then closes with a probe and a regression test. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard) to the final report. Use the available
Editor/IDE tools rather than assuming the agent cannot inspect a debugger.

If a bug-diagnosis skill is available, follow its loop. Otherwise use this one: **reproduce** the
failure, **hypothesise** one cause at a time, **probe** to separate the suspected cause from an
alternative, **fix** the cause, then add a **regression test** that failed before the fix.

## Capture the failing context

Record expected versus actual behavior, exact trigger, first relevant error/stack, engine/package
version, platform/backend, scene/prefab, and recent changes. Distinguish saved authoring state from
live runtime state and the component, scene, action, or request identity involved. Confirm logs
belong to this reproduction rather than a previous compilation/Play session. Record Play state,
compilation/reload state, activity (gameplay, recompilation, preview, or test fixture), log cursor or
timestamp range, and source revision plus relevant dirty-file state per collection. Reuse shared
context and record differences per finding. Retain supplied or measured context as known; mark only
unavailable fields Not verified.

Before implementation, state the observed failure, cause assessment (established, suspected, or
unknown), intended outcome, and checkable acceptance condition. Separate containment from recovery:
a guard preventing invalid callbacks does not establish that gameplay recovers after recompilation.
A probe must distinguish the proposed cause from alternatives; observing an exception alone cannot.

## Route the symptom

| Symptom | Evidence that distinguishes causes | Owning guide |
|---|---|---|
| Null/missing Unity reference | SerializedProperty, required/optional contract, prefab overrides, runtime assignments, destroyed-object check | [Scenes](UnityScenesAndLifecycleInstructions.md) (destroyed objects), [Editor tooling](UnityEditorToolingInstructions.md) (saved references) |
| Second Play/re-enable breaks | Reload settings, mutable statics, subscriptions, registries, pending requests | [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Input/UI misfires | Actual action instance/phases, update mode, live tree, focus/picking, propagation, domain entry point | [Input](UnityInputSystemInstructions.md), [UI Toolkit](UnityUIToolkitInstructions.md) |
| Contact/query wrong | Actual collider/body pair, layers, query count/capacity, physics synchronization | [3D Physics](UnityPhysicsInstructions.md) or [Physics2D](UnityPhysics2DInstructions.md) |
| Action/effect late or doubled | Animator state/parameters, interruption, event receiver, gameplay effect owner | [Animation](UnityAnimationInstructions.md) |
| Silent/misrouted audio | Source/listener state, group/parameter identity, playback/voice owner | [Audio](UnityAudioInstructions.md) |
| Missing/wrong rendering effect | Effective renderer, camera/pass order, graph resources, shader output | [Rendering](UnityRenderingInstructions.md) |
| Cost or memory grows | Comparable player captures, allocation stacks, retained references, repeated-cycle baseline | [Performance](UnityPerformanceOptimizationInstructions.md), [Assets](UnityAssetsAndMemoryInstructions.md) |
| Editor works; build fails | Platform defines, stripping/AOT, included content, effective assembly, initialization path | [Assemblies](UnityAssemblyDefinitionsInstructions.md) |
| Save/load diverges | Schema/version, real capture/load path, prior fixtures, reconstructed identity | [Persistence](UnityPersistenceInstructions.md) |
| Route/arrival wrong | Pending/partial/invalid path, loaded data, destination floor, actor movement authority | [Navigation](UnityNavigationInstructions.md) |
| Locale or access barrier | Actual supported language/input, fallback, glyph/layout, essential cue and option behavior | [Localization/accessibility](UnityLocalizationAccessibilityInstructions.md) |
| Remote state diverges | Topology, sender authority, durable state, spawn and delivery order | [Networking](UnityNetworkingInstructions.md) |
| ECS state races or disappears | World/group ordering, job dependency, ECB scope/playback and baked content | [Entities](UnityEntitiesInstructions.md) |
| Terrain seam/contact differs | Tile neighbors, authored edges, collider data and height synchronization | [Terrain](UnityTerrainInstructions.md) |
| Camera/cinematic control sticks | Target clock, selected output, saved bindings and interrupted ownership handoff | [Cameras/cinematics](UnityCamerasCinematicsInstructions.md) |

## Traps to keep in view

- ⚠️ The destroyed-object trap (`UnityEngine.Object` wrapping a destroyed native object, and why `?.`
  and `??` miss it) is owned by [Scenes](UnityScenesAndLifecycleInstructions.md). A caught exception or
  blanket null guard can hide missing required wiring rather than explain it.
- ⚠️ A prefab's source reference can differ from the scene instance. Inspect the instance that fails
  (see [Editor tooling](UnityEditorToolingInstructions.md) for saved-reference checks).
- ⚠️ An Editor-only repair, static cache, or already-loaded asset can hide a build/startup defect.
  Reproduce from a clean entry path (see [Assemblies](UnityAssemblyDefinitionsInstructions.md)).
- ⚠️ Fixing a visible symptom is not proof of cause. Use a probe that distinguishes the suspected
  owner/order/state from an alternative; record what evidence rules the alternative out.

Re-run the original trigger and verify the exact symptom. Remove temporary probes and restore changed
diagnostic settings. Take result freshness and coverage standards from
[Testing](UnityTestingInstructions.md).
