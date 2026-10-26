# Unity performance audit

Load for frame cost, allocations, pooling, rendering, or jobs. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Use `unity-project-review` for general
pitfall scanning and, when available, an optimization skill such as `unity:optimize-web` for
implementation/tool workflows; without one, use project tooling and official docs.
This lens owns frame cost, including rendering, animation, UI, and audio cost; resource residency
belongs to Assets. [Rendering](UnityRenderingInstructions.md) owns rendering correctness.
**Last verified: October 2026.**

## Establish the workload

Identify the target platform, representative scene/action, scale, frame/memory budget, and available
captures. Trace hot paths transitively: frame/physics/render callbacks, per-frame async/coroutine
loops, UI refreshes, and their helpers. A method name or API occurrence alone does not establish cost.
Separate a project rule violation from a measured bottleneck and from an unmeasured risk.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Avoidable hot work | Call frequency, object count, searches, queries, repeated calculations | A capture shows a per-frame callback or helper recomputing a value whose inputs did not change, or a `Find*`/`GetComponent*`/scene search sits inside a per-frame path (grep, then read the caller) |
| Managed allocation | GC.Alloc stacks, strings, boxing, closures, LINQ, collection growth | A profiler GC.Alloc sample, or a reached `new` of a reference type/closure/LINQ call, sits on a frequent path and breaks the stated budget or project rule |
| Cache validity | Invalidation and replacement paths | A dirty flag, cached camera/component, or derived value is read after the state it derives from changed without the cache being invalidated (trace each write to the cached source) |
| Query cost | Query volume, masks, ranges, hit needs | A query uses a default/all-layers mask where the target layer is known, or collects all hits (`RaycastAll`, `OverlapSphere`) when the caller uses one |
| Collection use | Capacity, clearing, iteration, ordering assumptions | A capture or grep shows linear lookups (`Contains`, `IndexOf`, `Remove`, `Insert(0, ...)`) inside a per-frame loop over the project's stated scale, or a collection recreated or regrown every frame instead of cleared |
| Pool cost | Creation bursts, retained objects, reset and active counts | Reuse fails (a new instance per `Get`), retained inactive count grows past `maxSize` expectations, or required concurrency exceeds an explicit cap |
| Rendering | Captures, batching/instancing, overdraw, camera/pass count | A Profiler or Frame Debugger capture (live run required) shows a draw/submission/fill cost with a verified cause |
| Jobs/native containers | Dependencies, completion, allocator lifetime, disposal | A `Complete()` call stalls the main thread longer than the work it offloads (capture), or a container is disposed while a scheduled job still uses it |
| Frame pacing | Platform's vSync/frame-cap behavior and frame-time distribution | A device capture shows frame time above the target (1000 / target fps ms) in the representative scene, or `Application.targetFrameRate` and `QualitySettings.vSyncCount` are set so the cap cannot reach the target |

## High-value interpretation checks

- ⚠️ `new` on a value type is not automatically a managed allocation. Stored delegates and reused
  collections differ from fresh closures and expanding buffers. Confirm type and call context.
- ⚠️ A reused `StringBuilder` can grow; `ToString()` still allocates. Changing displayed values only
  when needed can be sufficient without complicated zero-allocation formatting.
- ⚠️ Prefer a single-hit query when the caller needs one hit, and use collection overloads only when the
  result contract needs them; check completeness in [Physics](UnityPhysicsInstructions.md). Confirm
  allocation behavior with a capture rather than the overload name, and note that moving a query to
  `FixedUpdate` does not automatically make it cheaper.
- ⚠️ `ObjectPool<T>.defaultCapacity` sets the pool's initial capacity and `maxSize` its retained
  limit; neither is a concurrent-borrower cap. Verify whether instances are prewarmed in the installed
  version: prewarming needs multiple simultaneous checkouts, and a repeated Get/Release loop can keep
  returning the same object. Pool reset and stale async results are checked in
  [Scenes](UnityScenesAndLifecycleInstructions.md).
- ⚠️ `MaterialPropertyBlock` and per-renderer material changes have batching tradeoffs. Recommend from
  the actual pipeline and capture, not a blanket replacement. Material instance ownership is checked
  in [Assets](UnityAssetsAndMemoryInstructions.md).
- ⚠️ Immutable cached shader/Animator hashes do not need session resets. Check API availability against
  the installed version rather than copying a Unity 6 rename table.
- ⚠️ Jobs/Burst, GPU Resident Drawer (verify support in the installed pipeline and graphics API), GC
  suspension, batching changes, and extra caches are proposals only when the workload supports them.
  Their overhead or correctness costs can outweigh savings.

## Validation

Measure representative development-player captures on the target device where available. Record
warmup, scene/action, scale, build/backend, capture settings, and comparable before/after conditions.
Report frame-time distribution and spikes, allocation rate, and retained memory as relevant. Editor
captures can locate candidates; keep target-device claims Not verified without device evidence.

Use focused markers to confirm a hypothesis. Deep Profile is diagnostic instrumentation, not a
neutral before/after baseline. Re-measure a selected change and verify its behavior; a lower draw
count or zero GC column alone does not establish an overall improvement.

Measure subsystem cost here, then read the subsystem lens for its correctness checks:
[UI Toolkit](UnityUIToolkitInstructions.md), [uGUI](UnityUGUIInstructions.md),
[Animation](UnityAnimationInstructions.md), and [Audio](UnityAudioInstructions.md).

Technical reference: [ObjectPool constructor semantics](https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1-ctor.html).
