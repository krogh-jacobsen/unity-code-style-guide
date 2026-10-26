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
| Readiness | Bootstrap/composition path, required services, inactive and spawned objects | A component reads another object's or service's state in `Awake`/`OnEnable` where that object is on another GameObject, spawned, inactive, or in another scene, and no bootstrap order, Script Execution Order entry, or explicit initialization call precedes the read (grep field/service reads in those callbacks, then read the setup path) |
| Enable lifetime | Publisher/delegate identity and cleanup paths | A subscription made in `OnEnable`/`Start` has no matching unsubscribe in `OnDisable`/`OnDestroy`, or a Play-toggle of `enabled` doubles a callback count (live run) |
| Registration ownership | Registry entries on disable, destroy, scene exit, and replacement | A registry still holds an entry after its owner's disable/destroy (count before and after), or a removal keyed by type/name rather than owner identity can delete a newer owner's entry |
| Session reset | Mutable statics, static events, caches, SO channels, reload settings | A static field, static event, cache, or SO channel holds state that survives into the next Play and no documented reset policy covers it (see the policy below); confirm with a second Play where a counter or subscriber from the first run is still present |
| Persistence scope | Persistent roots and scene reload behavior | Reloading a scene creates a second instance of a service marked persistent (`DontDestroyOnLoad` with no duplicate guard), or a persistent object keeps references to objects of an unloaded scene |
| Scene transitions | Load/activation/unload order, failure and overlapping requests | A second load starts while one is pending with no guard, an old scene unloads before the new scene's activation completes (read the `AsyncOperation` ordering), or an exit path leaves a loading/input-blocked flag set (trace every exit) |
| Active scene | Instantiation and lighting expectations after additive loads | `Instantiate`/`new GameObject` runs after an additive load without `SceneManager.SetActiveScene` or `MoveGameObjectToScene` while the intended scene is not active, or the active scene's lighting settings differ from the expected scene's (live read) |
| Async ownership | Every await and operation start, cancellation and error observation | An `await`/operation start has no cancellation or owner check for its lifetime, an exception from a fire-and-forget entry point has no handler, or canceled work leaves a resource unreleased |

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

## Destroyed-object checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Destroyed-object null check | Fields typed `UnityEngine.Object` or a subclass (`GameObject`, `Component`, `ScriptableObject`); callbacks after `OnDestroy`; pooled and async results | `?.`, `??`, `??=` or `is null` is applied to such a field and the guarded access can run after the object is destroyed (grep `\?\.`, `\?\?`, `is null`, then read the caller) |

Unity's `Object` reference says `?.` and `??` are not supported with Unity Objects because they cannot
be overridden to treat detached objects as null, and are safe only when the checked object is
guaranteed never to be detached. It also says a detached object compares equal to `null` while
`Object.ReferenceEquals(obj, null)` returns false. The `is null` pattern is not mentioned there; treat
it the same way and verify in the installed version. Use Unity's `== null` or implicit bool check for
objects that can be destroyed. A hit on an object that cannot be destroyed (a plain C# class, an
`Object` held only by its owner for its own lifetime) is not a finding.

Triage by lifetime: a `?.`, `??`, or `is null` site is a candidate only when the referenced object's
lifetime can be shorter than its holder's (a scene object held by a longer-lived owner, a pooled or
spawned object, an object another system destroys). An owner that lives as long as the scene is not a
candidate. Treat `GetComponent<T>() ?? AddComponent<T>()` as a candidate to confirm in a live Editor
run: `??` bypasses Unity's null check, the `GetComponent` reference does not say whether a missing
component yields a placeholder object, and the `TryGetComponent` reference notes it does not allocate in
the Editor when the component is missing, which suggests `GetComponent` can. `TryGetComponent` avoids the
question; verify the Editor behavior in the installed version.

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
