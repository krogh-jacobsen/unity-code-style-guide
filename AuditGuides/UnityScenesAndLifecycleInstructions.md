# Unity scenes and lifecycle audit

Load for startup, scene flow, enable/disable behavior, asynchronous work, or repeated Play sessions.
Apply the [shared evidence standard](README.md#evidence-standard). Use the project's lifecycle and
composition decisions; inspect live state through `unity-cli` when needed.

## Establish lifetime ownership

Map application-, scene-, enable-, and request-lifetime owners. Find who initializes, registers,
cancels, and releases each one. Inspect the supported entry scenes and Enter Play Mode settings.
A bootstrap scene is one valid choice; it is not mandatory for every game.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Readiness | Bootstrap/composition path, required services, inactive and spawned objects | A consumer relies on another object's `Awake`/`OnEnable` ordering without an explicit contract |
| Enable lifetime | Publisher/delegate identity and cleanup paths | Re-enable adds duplicate subscriptions or disabled consumers still receive unintended work |
| Registration ownership | Registry entries on disable, destroy, scene exit, and replacement | Dead entries survive, or old-owner cleanup removes a newer owner's registration |
| Session reset | Mutable statics, static events, caches, SO channels, reload settings | A later Play inherits state or subscribers that should belong to the previous session |
| Persistence scope | Persistent roots and scene reload behavior | Reload duplicates services or persistent owners retain unloaded scene objects |
| Scene transitions | Load/activation/unload order, failure and overlapping requests | Old content unloads too soon, a stale transition wins, or failure leaves input/loading state stuck |
| Active scene | Instantiation and lighting expectations after additive loads | Objects or scene settings use an unintended active scene |
| Async ownership | Every await and operation start, cancellation and error observation | Work outlives its owner, faults go unobserved, or canceled work leaks resources |

## Async cases that basic null checks miss

- `destroyCancellationToken` covers destruction. Enable-lifetime work needs cancellation on disable;
  request-lifetime work also needs replacement/cancel handling. Create and dispose token sources
  according to that ownership.
- After an await, verify that the result still belongs to the current request. A live, enabled object
  can have been returned to a pool and reused. A generation/request ID can distinguish the old work.
- Cancellation of a wait does not necessarily cancel its underlying scene/asset operation. Establish
  what completes, who releases the result, and who restores transition state on every exit path.
- A Unity `Awaitable` instance is pooled and should be awaited only once. Shared completion needs a
  deliberately reusable representation. Return to the main thread before accessing Unity objects.
- Observe errors at the operation's owner, including fire-and-forget entry points. Returning
  `Awaitable` alone does not prove that a caller observes its stored exception.

## Interpret with care

Reset mutable session state, including mutable contents of `static readonly` collections. Immutable
constants, cached hashes, and stateless markers do not need artificial reset methods. A stored lambda
can be unsubscribed using the same delegate instance; an anonymous re-created lambda cannot.

`Start` is not a universal readiness barrier for inactive, spawned, or additively loaded objects.
Match cleanup to ownership rather than assuming `OnDestroy` runs for every allocation path. Preserve
unsaved scenes during inspection; validate saved wiring separately from transient runtime fixes.

## Validation

Exercise disable/re-enable, supported scene entry, unload/reload, a failed/overlapping transition,
and a second Play with the project's reload settings. Include destruction/cancellation while work
is pending and pool reuse when applicable. Verify registry/subscriber counts return to the intended
baseline; inspect asset ownership with [Assets](UnityAssetsAndMemoryInstructions.md).

Technical reference: [Awaitable introduction](https://docs.unity3d.com/6000.0/Documentation/Manual/async-awaitable-introduction.html).
Match the reference to the installed engine version when implementing a fix.
