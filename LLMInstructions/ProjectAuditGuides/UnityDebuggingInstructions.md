# Unity diagnostic evidence

Load for Unity-specific runtime/Editor discrepancies, lifecycle failures, or build-only defects.
`diagnosing-bugs` owns reproduction, hypotheses, probes, and regression workflow; this guide supplies
Unity evidence to that loop. Apply the [shared evidence standard](ProjectReview.md#evidence-standard).
Use the available Editor/IDE tools rather than assuming the agent cannot inspect a debugger.

## Capture the failing context

Record expected versus actual behavior, exact trigger, first relevant error/stack, engine/package
version, platform/backend, scene/prefab, and recent changes. Distinguish saved authoring state from
live runtime state and the component, scene, action, or request identity involved. Confirm logs
belong to this reproduction rather than a previous compilation/Play session.

## Audit checks by symptom

| Symptom | Evidence that distinguishes causes | Owning guide |
|---|---|---|
| Null/missing Unity reference | SerializedProperty, required/optional contract, prefab overrides, runtime assignments, destroyed-object check | [Editor tooling](UnityEditorToolingInstructions.md) |
| Second Play/re-enable breaks | Reload settings, mutable statics, subscriptions, registries, pending requests | [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Input/UI misfires | Actual action instance/phases, update mode, live tree, focus/picking, propagation, domain entry point | [Input](UnityInputSystemInstructions.md), [UI Toolkit](UnityUIToolkitInstructions.md) |
| Contact/query wrong | Actual collider/body pair, layers, query count/capacity, physics synchronization | [Physics](UnityPhysicsInstructions.md) |
| Action/effect late or doubled | Animator state/parameters, interruption, event receiver, gameplay effect owner | [Animation](UnityAnimationInstructions.md) |
| Silent/misrouted audio | Source/listener state, group/parameter identity, playback/voice owner | [Audio](UnityAudioInstructions.md) |
| Cost or memory grows | Comparable player captures, allocation stacks, retained references, repeated-cycle baseline | [Performance](UnityPerformanceOptimizationInstructions.md), [Assets](UnityAssetsAndMemoryInstructions.md) |
| Editor works; build fails | Platform defines, stripping/AOT, included content, effective assembly, initialization path | [Assemblies](UnityAssemblyDefinitionsInstructions.md) |
| Save/load diverges | Schema/version, real capture/load path, prior fixtures, reconstructed identity | [Persistence](UnityPersistenceInstructions.md) |

## Unity traps to keep in view

- ⚠️ `UnityEngine.Object` can wrap a destroyed native object. Use Unity's `== null`/truth check when
  testing that lifetime; `is null`, `?.`, and `??` only inspect the managed reference. A caught
  exception or blanket null guard can hide missing required wiring rather than explain it.
- ⚠️ A prefab's source reference can differ from the scene instance or a variant override. Inspect the
  instance that fails, including inactive children and references replaced by runtime code.
- ⚠️ An Editor-only repair, static cache, or already-loaded asset can hide a build/startup defect.
  Validate from the supported clean entry path and saved content.
- ⚠️ Fixing a visible symptom is not proof of cause. Use a probe that distinguishes the suspected
  owner/order/state from an alternative; record what evidence rules the alternative out.

## Validation

Re-run the original trigger in the relevant scene/platform and verify the exact symptom. Confirm
regression-test sensitivity where a meaningful seam exists, remove temporary probes, and restore
changed diagnostic settings. Log absence alone does not prove the intended command occurred.
Use [Testing](UnityTestingInstructions.md) for result freshness and remaining coverage limits.
