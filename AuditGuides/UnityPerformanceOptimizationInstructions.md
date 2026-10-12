# Unity performance audit

Load for frame cost, allocations, pooling, rendering, or jobs. Apply the
[shared evidence standard](README.md#evidence-standard). Use `unity-project-review` for general
pitfall scanning and the relevant optimization skill for implementation/tool workflows.

## Establish the workload

Identify the target platform, representative scene/action, scale, frame/memory budget, and available
captures. Trace hot paths transitively: frame/physics/render callbacks, per-frame async/coroutine
loops, UI refreshes, and their helpers. A method name or API occurrence alone does not establish cost.
Separate a project rule violation from a measured bottleneck and from an unmeasured risk.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Avoidable hot work | Call frequency, object count, searches, queries, repeated calculations | Work runs more often or over more objects than behavior requires |
| Managed allocation | GC.Alloc stacks, strings, boxing, closures, LINQ, collection growth | A reached frequent path allocates contrary to the budget or project rule |
| Cache validity | Invalidation and replacement paths | A dirty flag, cached camera/component, or derived value becomes stale after state changes |
| Query cost | Query volume, masks, ranges, hit needs | A query searches irrelevant space/layers or collects all hits when one is sufficient |
| Collection use | Capacity, clearing, iteration, ordering assumptions | Resize/copy churn or repeated linear lookup dominates the workload |
| Pool cost | Creation bursts, retained objects, reset and active counts | Reuse fails, retained memory grows, or the required concurrency exceeds an explicit cap |
| Rendering | Captures, material ownership, batching/instancing, overdraw, camera/pass count | A measured draw/submission/fill cost has a verified cause |
| Jobs/native containers | Dependencies, completion, allocator lifetime, disposal | Main-thread stalls erase the gain, or memory is disposed before outstanding work completes |
| Frame pacing | Platform's vSync/frame-cap behavior and frame-time distribution | The configured cap fails the intended pacing or sustained device budget |

## High-value interpretation checks

- `new` on a value type is not automatically a managed allocation. Stored delegates and reused
  collections differ from fresh closures and expanding buffers. Confirm type and call context.
- A reused `StringBuilder` can grow; `ToString()` still allocates. Changing displayed values only
  when needed can be sufficient without complicated zero-allocation formatting.
- `Physics.Raycast(..., out hit, ...)` is already a non-allocating single-hit query. Use collection
  overloads only when the result contract needs them; check completeness in
  [Physics](UnityPhysicsInstructions.md). Moving a query to `FixedUpdate` does not automatically make it cheaper.
- `ObjectPool<T>.defaultCapacity` reserves storage; it does not prewarm instances. `maxSize` limits
  retained inactive objects, not concurrent borrowers. Prewarming needs multiple simultaneous
  checkouts; a repeated Get/Release loop may keep returning the same object.
- Pools need owned cleanup for both retained and checked-out instances. A reset must happen before
  consumers observe activation; async work from an old checkout must not affect a new one. See
  [Scenes](UnityScenesAndLifecycleInstructions.md) for cancellation and generation checks.
- Reading `.material` can create an owned instance; changing `.sharedMaterial` changes shared state.
  `MaterialPropertyBlock` has batching tradeoffs. Recommend from the actual pipeline and capture,
  not a blanket replacement. Audit native ownership with [Assets](UnityAssetsAndMemoryInstructions.md).
- Immutable cached shader/Animator hashes do not need session resets. Check API availability against
  the installed version rather than copying a Unity 6 rename table.
- Jobs/Burst, GPU Resident Drawer, GC suspension, batching changes, and extra caches are proposals
  only when the workload supports them. Their overhead or correctness costs can outweigh savings.

## Validation

Measure representative development-player captures on the target device where available. Record
warmup, scene/action, scale, build/backend, capture settings, and comparable before/after conditions.
Report frame-time distribution and spikes, allocation rate, and retained memory as relevant. Editor
captures can locate candidates; keep target-device claims Not verified without device evidence.

Use focused markers to confirm a hypothesis. Deep Profile is diagnostic instrumentation, not a
neutral before/after baseline. Re-measure a selected change and verify its behavior; a lower draw
count or zero GC column alone does not establish an overall improvement.

Subsystem details belong in [UI Toolkit](UnityUIToolkitInstructions.md), [uGUI](UnityUGUIInstructions.md),
[Animation](UnityAnimationInstructions.md), and [Audio](UnityAudioInstructions.md).

Technical reference: [ObjectPool constructor semantics](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Pool.ObjectPool_1-ctor.html).
