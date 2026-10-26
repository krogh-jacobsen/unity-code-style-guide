# Unity scenes and lifecycle audit

Load for startup, scene flow, enable/disable behavior, asynchronous work, destroyed-object checks, or
repeated Play sessions. Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Use the
project's lifecycle and composition decisions; inspect live state through `unity:unity-cli` (or project
tooling) when needed. This lens owns pool and async staleness and cancellation checks.
**Last verified: October 2026.**

## Establish lifetime ownership

Map application-, scene-, enable-, and request-lifetime owners. Find who initializes, registers,
cancels, and releases each one. Inspect the supported entry scenes and Enter Play Mode settings.
A bootstrap scene is one valid choice; it is not mandatory for every game.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Readiness | Bootstrap/composition path, required services, inactive and spawned objects | A consumed value depends on initialization that is not guaranteed to precede the read, leaving an inspected failure path or a reproduced wrong value. Serialized/default state independent of the other object’s callbacks need not have explicit execution ordering |
| Enable lifetime | Publisher/delegate identity and cleanup paths | A subscription made in `OnEnable`/`Start` has no matching unsubscribe in `OnDisable`/`OnDestroy`, or a Play-toggle of `enabled` doubles a callback count (live run) |
| Registration ownership | Registry entries on disable, destroy, scene exit, and replacement | A registry still holds an entry after its owner's disable/destroy (count before and after), or a removal keyed by type/name rather than owner identity can delete a newer owner's entry |
| Session reset | Mutable statics, static events, caches, SO channels, reload settings | A static field, static event, cache, or SO channel holds state that survives into the next Play and no documented reset policy covers it (see the policy below); confirm with a second Play where a counter or subscriber from the first run is still present |
| Persistence scope | Persistent roots and scene reload behavior | Reloading a scene creates a second instance of a service marked persistent (`DontDestroyOnLoad` with no duplicate guard), or a persistent object keeps references to objects of an unloaded scene |
| Scene transitions | Load/activation/unload order, failure and overlapping requests | An overlapping request or unload/activation ordering loses required scene state, deadlocks a queued operation, or leaves loading/input-block flags set. Unloading first to fit a memory budget is valid with a defined recovery path |
| Active scene | Instantiation and lighting expectations after additive loads | Actual object scene ownership or effective lighting differs from the intended additive-scene contract. Inspect supported explicit destination-scene instantiation, parent placement, SetActiveScene and MoveGameObjectToScene paths; absence of one API alone is not a finding |
| Async ownership | Every await and operation start, cancellation and error observation | Pending work can outlive its consumer with an unsafe continuation or unreleased result, or an operation error has no observing owner. Bounded or intentionally application-owned work need not accept a cancellation token merely because it awaits |

## Async cases that basic null checks miss

- ⚠️ `destroyCancellationToken` covers destruction. Enable-lifetime work needs cancellation on disable;
  request-lifetime work also needs replacement/cancel handling. Create and dispose token sources
  according to that ownership.
- ⚠️ After an await, verify that the result still belongs to the current request. A live, enabled object
  can have been returned to a pool and reused. A generation/request ID can distinguish the old work.
  A pooled object's reset must happen before consumers observe activation.
- ⚠️ Cancellation of a wait does not necessarily cancel its underlying scene/asset operation. Establish
  what completes, who releases the result, and who restores transition state on every exit path.
  The release path itself is checked in [Assets](UnityAssetsAndMemoryInstructions.md).
- ⚠️ A Unity `Awaitable` instance is pooled and should be awaited only once: the Awaitable
  documentation says awaiting more than once is never safe and can throw or deadlock. Shared
  completion needs a deliberately reusable representation. Return to the main thread before accessing
  Unity objects.
- ⚠️ Observe errors at the operation's owner, including fire-and-forget entry points. Do not assume an
  un-awaited `Awaitable` surfaces its exception: the Awaitable documentation does not say it does, so
  verify exception behavior in the installed version.

The [continuation manual](https://docs.unity3d.com/Manual/async-awaitable-continuations.html)
now describes thread switching as local to the current async method, with caller-thread resumption.
Older Unity manuals describe different Awaitable continuation behavior. Verify the installed engine
and actual continuation path, especially after explicit thread switches or context suppression;
require a main-thread switch where needed rather than after every await. Background work also needs
an application-exit owner when component destruction alone does not end it.

## Destroyed-object checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Destroyed-object null check | Fields typed `UnityEngine.Object` or a subclass (`GameObject`, `Component`, `ScriptableObject`); callbacks after `OnDestroy`; pooled and async results | `?.`, `??`, `??=` or `is null` is applied to such a field and the guarded access can run after the object is destroyed (grep `\?\.`, `\?\?`, `is null`, then read the caller) |

Unity's `Object` reference says `?.` and `??` are not supported with Unity Objects because they cannot
be overridden to treat detached objects as null, and are safe only when the checked object is
guaranteed never to be detached. It also says a detached object compares equal to `null` while
`Object.ReferenceEquals(obj, null)` returns false. C# [constant null patterns](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns)
bypass overloaded equality, so `is null` does not invoke Unity's destroyed-object check.
Use Unity's `== null` or implicit bool check for
objects that can be destroyed. A hit on an object that cannot be destroyed (a plain C# class, an
`Object` held only by its owner for its own lifetime) is not a finding.

Triage by lifetime: a `?.`, `??`, or `is null` site is a candidate only when the referenced object's
lifetime can be shorter than its holder's (a scene object held by a longer-lived owner, a pooled or
spawned object, an object another system destroys). Scene membership alone does not prove equal
lifetime: a component can be destroyed while its holder
survives. For `GetComponent<T>() ?? AddComponent<T>()`, establish the actual returned reference and
failure path; an Editor allocation observation alone does not establish a detached-object bug.

## Interpret with care

Read the real Enter Play Mode setting before judging session reset. Unity's manual states that the
Editor does not perform a domain reload on entering Play mode by default, and the
[project settings guide](../ProjectSettings/ProjectSettings.md#reload-policy) records the new-project
default as Reload Scene only (domain reload off) and owns the policy. With domain reload off, static
state survives between Play sessions, so a mutable static or static event is a finding when its state
can leak into the next Play and no documented reset covers it. Documented resets are
`[AutoStaticsCleanup]`/`[NoAutoStaticsCleanup]` (documented from Unity 6.5) and the
`[OnEnteringPlayMode]`/`[OnExitingPlayMode]` lifecycle attributes that the manual names. A project that
documents `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]` resets is
following a valid policy; do not report it as a conflict. The
[`SubsystemRegistration` reference](https://docs.unity3d.com/ScriptReference/RuntimeInitializeLoadType.SubsystemRegistration.html)
names `OnCodeInitializing` as the option for new code (better resource pre-allocation timing) and does
not say it resets statics, so verify in the installed version before adopting it for resets.
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

Technical reference: [Awaitable introduction](https://docs.unity3d.com/Manual/async-awaitable-introduction.html).
Match the reference to the installed engine version when implementing a fix.

Scene placement reference: [Object.Instantiate overloads](https://docs.unity3d.com/ScriptReference/Object.Instantiate.html).
Match the installed engine before recommending an explicit destination-scene overload.
