# Pooled notification lease ownership

Use this example when a pooled object subscribes to signals or schedules delayed behavior. The
notification is a minimal state marker, with no rendering dependency; connect it to your selected
visual system only when adopting the pattern. It is not a general pooling framework.

## Contract

`NotificationPool` privately owns Unity's ObjectPool and all borrowed items. `Acquire` returns a
unique `NotificationLease`, initializes message/state, subscribes once, and activates the item.
Returning disposes that lease, cancels its delayed work, unsubscribes, resets state, and deactivates
the item. Dispose is repeatable. An old lease cannot return a new checkout of the same component,
even if the old delay provider completes after ignoring cancellation.

The owner disposes both borrowed and retained items on teardown and rejects later acquisition.
`retainedCapacity` limits retained items, not concurrent leases; the example does not prewarm.
All calls/completions run on Unity's main thread. Factories must produce live inactive components.
Clients return leases rather than independently destroying, disabling, or reparenting their items.
The exposed Item is for configuring/reading the current lease, not ownership transfer.

Each checkout allocates a small lease object, and a timed return allocates a cancellation source.
This sample demonstrates correct ownership rather than a zero-allocation pool; profile those costs
before adapting it to a high-frequency spawn path.

`NotificationPoolHost` is the object-lifetime adapter. Disabling its component does not end the
pool's lifetime; destruction does. Its demo creates inactive child markers through GameObject APIs,
so no prefab asset is required. A production prefab must likewise start inactive. The host observes
timed-return errors and returns the lease in a finally block. A visual-lifetime pool could instead
choose disable as its disposal boundary; make that choice explicitly.

## Install and exercise through Unity CLI

Requires Unity 6 Awaitable and UnityEngine.Pool; optional tests require Test Framework. Copy code,
asmdefs, and metadata to `Assets/Examples/PooledNotifications/`, keeping this README outside Assets.
Inspect path/GUID conflicts first. See [tested compatibility](../../Validation.md).

Discover CLI/Editor commands, import, and require no compiler errors. In an isolated Play scene,
attach `NotificationPoolHost` through CLI-driven Editor APIs. Invoke ShowNotification and inspect
its children and BorrowedCount. A marker activates, then returns inactive. PulseNotifications
updates leased markers only. Destroying the host ends work and removes all its children. Manual
fallback: attach in the Editor and use the context menus during Play.

On the tested CLI beta, save and close the disposable project's Editor before `unity test`; it
starts its own batch Editor. Use fresh result paths outside Assets in an existing output folder.

```bash
unity test /absolute/project --mode EditMode \
  --filter UnityBestPractices.Samples.Pooling.Tests --output /absolute/results/pool-edit.xml
unity test /absolute/project --mode PlayMode \
  --filter UnityBestPractices.Samples.Pooling.Tests --output /absolute/results/pool-play.xml
```

EditMode deliberately completes an old timer after return/reuse, checks duplicate-return safety,
state reset and subscription counts, then verifies owner disposal removes borrowed/retained items.
PlayMode verifies actual timed return and host destruction. Read fresh XML and logs; test discovery,
failures and exclusions are part of the result. Manual fallback: Test Runner.

Unity's [pooling guidance](https://docs.unity.com/en-us/engine/6000.6/manual/scripting/optimization/performance-optimizing-code-managed-memory/reusable-code)
provides the general API mechanics; this example adds checkout identity and ownership checks.
