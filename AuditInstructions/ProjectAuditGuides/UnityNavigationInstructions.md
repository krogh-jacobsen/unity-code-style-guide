# Unity navigation audit

Load for owned NavMesh agents, surfaces, obstacles, links, or path requests. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Establish engine/navigation package,
agent types, area filters, loaded data, and movement authority. Custom pathfinders need their own
source-matched contracts; package presence alone does not establish NavMesh usage.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Surface/data contract | Saved bake inputs, geometry/layer filters, agent type, loaded surface data | An intended route is absent or unsuitable for the actor in the shipped scene; no universal bake preset is required |
| Request/result contract | `SetDestination`, pending/complete/partial/invalid states, arrival and replacement logic | A submitted request or partial/invalid path is treated as successful arrival; pending or infinite distance is consumed as a completed result |
| Reachability | `SamplePosition` callers, destination constraints and actual path | A nearby point on another floor/disconnected island is accepted where a reachable target is required; sampling proximity alone does not prove reachability |
| Movement authority | Agent pose updates, physics, root motion, `nextPosition` and update flags | Active writers fight, or agent and actor diverge; deliberate one-direction animation/physics integration is valid |
| Obstacle handoff | Agent/Obstacle activation, carving, death/immobilization and pooling | Simultaneously active behavior causes self avoidance/carving or breaks the intended route |
| Route lifetime | Link endpoints, direction, agent type/area, custom traversal, surface unload/rebuild | A supported traversal cannot complete or cancel, or required navigation data disappears while users still depend on it |

## Interpret with care

NavMesh arrival is a gameplay contract, not a universal `remainingDistance` comparison. Check failed,
pending, partial, replaced, and zero-length paths separately. Avoidance does not establish route
reachability. Runtime rebuild and carving frequency are cost proposals under
[Performance](UnityPerformanceOptimizationInstructions.md). A component combination alone is a candidate.

## Validation

Traverse intended narrow passages, slopes, multilevel/disconnected destinations, both supported link
directions, stop/resume and teleports. Interrupt a request/traversal, unload/reload surfaces, and
reuse pooled actors. Reopen saved bake/link configuration. Missing live route checks are Not verified.
General cancellation/resource ownership remains in [Scenes](UnityScenesAndLifecycleInstructions.md)
and [Assets](UnityAssetsAndMemoryInstructions.md).

Technical references: [surface contracts](https://docs.unity3d.com/Packages/com.unity.ai.navigation@latest/index.html?subfolder=/manual/NavMeshSurface.html),
[mixing movement components](https://docs.unity3d.com/Packages/com.unity.ai.navigation@latest/index.html?subfolder=/manual/MixingComponents.html),
[path state](https://docs.unity3d.com/ScriptReference/AI.NavMeshAgent.html), and
[sampling limits](https://docs.unity3d.com/ScriptReference/AI.NavMesh.SamplePosition.html).
Match the installed navigation package; research inspected AI Navigation 2.0.16.
