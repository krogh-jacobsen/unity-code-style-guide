# Unity Scenes, Bootstrapping & Application Lifecycle

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

How the game starts, how scenes come and go, and what survives in between.

Two problems dominate this area. The first is **initialization order** — something needs a service
that doesn't exist yet. The second is **state that outlives what created it** — a static field, an
event subscription, or a `DontDestroyOnLoad` object that's still there on the second playthrough.

Table of contents:
- [The bootstrap scene pattern](#the-bootstrap-scene-pattern)
- [Additive scene loading](#additive-scene-loading)
- [Initialization order](#initialization-order)
- [Domain reload and static state](#domain-reload-and-static-state)
- [DontDestroyOnLoad discipline](#dontdestroyonload-discipline)
- [Cross-scene references](#cross-scene-references)
- [Teardown](#teardown)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## The bootstrap scene pattern

- ✅ Have one small scene that is always loaded first and never unloaded. It owns the services that
  must exist for the whole session: audio, save system, input, scene loading, analytics.
- ✅ Everything else loads **additively** on top of it.
- ✅ Put it at index 0 in Build Settings so a build always starts there.
- ⚠️ In the Editor you usually start from whatever scene is open, which skips the bootstrap. Handle
  this explicitly rather than letting designers hit a null service:

```csharp
public class Bootstrapper : MonoBehaviour
{
    private const string k_bootstrapSceneName = "Bootstrap";

    // Runs before the first scene's Awake, in builds and in the Editor
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    private static void EnsureBootstrapLoaded()
    {
        if (SceneManager.GetSceneByName(k_bootstrapSceneName).isLoaded) return;

        // Entered play mode on a gameplay scene - pull the bootstrap in behind it
        SceneManager.LoadScene(k_bootstrapSceneName, LoadSceneMode.Additive);
    }
}
```

- ✅ This means a designer can press Play on any scene and it just works. That single convenience
  saves more time than most optimizations.

---

## Additive scene loading

- ✅ Use `LoadSceneAsync(..., LoadSceneMode.Additive)` and `UnloadSceneAsync` for level flow.
- ✅ Split large levels into additive chunks — geometry, lighting, gameplay, UI — so they can load and
  unload independently.
- ⚠️ `LoadSceneMode.Single` destroys everything not marked `DontDestroyOnLoad`. That includes your
  services if the bootstrap isn't protected.
- ✅ Use `allowSceneActivation = false` to load in the background and activate at a moment you choose —
  this is how you avoid a hitch mid-gameplay.
- ⚠️ Progress stalls at `0.9` while `allowSceneActivation` is false. That is expected, not a bug.
  Treat `>= 0.9` as "ready".
- ✅ Call `Resources.UnloadUnusedAssets()` after unloading, while the loading screen is still up.

```csharp
public async Awaitable LoadLevelAsync(string sceneName, CancellationToken token)
{
    AsyncOperation load = SceneManager.LoadSceneAsync(sceneName, LoadSceneMode.Additive);
    load.allowSceneActivation = false;

    // 0.9 is "loaded but not activated" - it will not reach 1.0 until we allow activation
    while (load.progress < 0.9f)
    {
        m_progressBar.value = load.progress / 0.9f;
        await Awaitable.NextFrameAsync(token);

        if (this == null) return;
    }

    await FadeOutAsync(token);

    load.allowSceneActivation = true;
    await load;

    if (this == null) return;

    // Now that the old scene is gone, reclaim its assets
    await Resources.UnloadUnusedAssets();

    SceneManager.SetActiveScene(SceneManager.GetSceneByName(sceneName));
    await FadeInAsync(token);
}
```

- ℹ️ `SetActiveScene` matters: newly instantiated objects and lightmap/skybox settings come from the
  active scene. Forgetting it is why a level sometimes loads with the previous scene's lighting.

---

## Initialization order

Unity's guarantees, in order, for a single scene load:

1. All `Awake()` on all objects
2. All `OnEnable()` on all objects
3. All `Start()` before the first frame

- ✅ **`Awake` for self, `Start` for others.** Cache your own components in `Awake`; touch other
  objects in `Start`. That ordering is guaranteed; anything finer is not.
- ⚠️ Order *within* a phase is undefined. Two `Awake` methods have no guaranteed relative order.
- ⚠️ Script Execution Order (Project Settings → Script Execution Order) works, but it's a global,
  invisible dependency. Use it sparingly and comment why.
- ✅ Prefer explicit initialization for anything order-sensitive: have the bootstrap call
  `Initialize()` on services in the order it wants, rather than relying on lifecycle timing.
- ⚠️ **Objects loaded additively run their `Awake` when that scene finishes loading**, not when the
  first scene did. A service registered in an additive scene isn't available to the base scene's
  `Start`.

| Attribute | Runs |
|---|---|
| `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]` | Earliest — before subsystems register |
| `[RuntimeInitializeOnLoadMethod(BeforeSceneLoad)]` | Before the first scene's `Awake` |
| `[RuntimeInitializeOnLoadMethod(AfterSceneLoad)]` | After the first scene loads, before `Start` |
| `[InitializeOnLoad]` | Editor only, on domain reload |

---

## Domain reload and static state

Disabling Domain Reload (Project Settings → Editor → Enter Play Mode Options) saves 2–5 seconds on
every Play. The cost is that **static state no longer resets**.

- ⚠️ Static fields keep their values from the previous play session.
- ⚠️ Static events keep their subscribers, so handlers accumulate and fire multiple times.
- ⚠️ Singleton instances point at destroyed objects — the classic
  `MissingReferenceException` on second play.
- ✅ Reset every static explicitly. Make it a rule, not a case-by-case fix:

```csharp
public class GameSession
{
    private static int s_score;
    private static readonly List<Player> s_players = new();

    public static event Action<int> ScoreChanged;

    // Runs on every play, whether or not domain reload is enabled
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    private static void ResetStatics()
    {
        s_score = 0;
        s_players.Clear();
        ScoreChanged = null;   // Critical - otherwise last session's handlers survive
    }
}
```

- ✅ Keep the reset method physically next to the statics it resets. A reset method in a different
  file goes stale the moment someone adds a field.
- ✅ If a class has statics and no `ResetStatics`, treat that as a bug when domain reload is disabled.
- ℹ️ See [UnityProjectConfiguration.md](../UnityCustomInstructions/UnityProjectConfiguration.md#caveats-when-domain-reload-is-disabled)
  for the settings themselves.

---

## DontDestroyOnLoad discipline

- ⚠️ `DontDestroyOnLoad` on many objects is usually a sign of a missing bootstrap scene. A bootstrap
  scene that is never unloaded achieves the same thing, visibly, in one place.
- ⚠️ Objects moved to the `DontDestroyOnLoad` scene are easy to lose track of — they don't appear in
  any scene file, so nothing in version control records that they exist.
- ✅ If you do use it, apply it to a single root object and parent everything persistent under it.
- ⚠️ **Reloading the scene that created a `DontDestroyOnLoad` object creates a second one.** Guard it:

```csharp
public class AudioService : MonoBehaviour
{
    private static AudioService s_instance;

    private void Awake()
    {
        // A reload of this scene would otherwise create a duplicate
        if (s_instance != null && s_instance != this)
        {
            Destroy(gameObject);
            return;
        }

        s_instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

---

## Cross-scene references

- ❌ You cannot serialize a reference from an object in one scene to an object in another. Unity will
  either refuse the assignment or silently null it at runtime.
- ✅ Wire scenes together at runtime instead. Three options, in rough order of preference:

| Approach | Good for | Trade-off |
|---|---|---|
| ScriptableObject as a shared channel | Event and data passing between scenes | Needs discipline about runtime state on SOs |
| Service locator / DI registered in bootstrap | Long-lived services | Indirection; harder to trace |
| Objects register themselves on `OnEnable` | Loose collections (enemies, spawn points) | Order-dependent if you read too early |

- ✅ A ScriptableObject "event channel" is the most Unity-native answer: both scenes reference the
  asset, neither references the other.
- ⚠️ Remember that a ScriptableObject holding runtime state persists in the Editor between plays.
  Reset it in `OnEnable` — see
  [ScriptableObjects](../UnityStyleGuide.md#scriptable-objects).

---

## Teardown

- ✅ Unsubscribe in `OnDisable`, release resources in `OnDestroy`. See
  [OnDestroy()](../UnityStyleGuide.md#ondestroy).
- ⚠️ Destruction order between objects is **not** guaranteed. Never assume another object is still
  alive in your `OnDestroy`.
- ⚠️ `OnDestroy` is not called if the object was never enabled.
- ⚠️ `OnApplicationQuit` does not run on mobile when the OS kills a backgrounded app. Save on
  `OnApplicationPause(true)` instead — that's the last callback you're reliably given.
- ✅ Use `Application.quitting` for static cleanup that has no MonoBehaviour to hang off.

```csharp
private void OnApplicationPause(bool isPaused)
{
    // On mobile this is the last reliable chance to persist state
    if (isPaused)
    {
        m_saveService.SaveNow();
    }
}

private void OnApplicationQuit()
{
    // Desktop, and graceful mobile exits only
    m_saveService.SaveNow();
}
```

---

## Troubleshooting

**Pressing Play on a gameplay scene throws null reference errors on services.**
The bootstrap scene wasn't loaded. Add the `[RuntimeInitializeOnLoadMethod]` guard from
[the bootstrap scene pattern](#the-bootstrap-scene-pattern) so any scene works as an entry point.

**Works the first time you press Play, breaks the second time.**
Classic disabled-Domain-Reload symptom. A static field or static event kept its value from the
previous session. Add a `ResetStatics` method — see
[Domain reload and static state](#domain-reload-and-static-state).

**An event handler fires two or three times, increasing each play session.**
Static event subscribers accumulated. Setting the event to `null` in `ResetStatics` is the fix; the
subscription itself is probably fine.

**Loading bar reaches 90% and stops.**
Expected. With `allowSceneActivation = false`, progress caps at `0.9`. Treat `>= 0.9` as ready and
divide by `0.9` for the display value.

**Objects instantiate into the wrong scene, or lighting is wrong after an additive load.**
`SetActiveScene` wasn't called. New objects and lighting settings come from the active scene.

**Two copies of a manager exist after reloading a scene.**
A `DontDestroyOnLoad` object created by a scene that got reloaded. Add the duplicate guard in
`Awake`.

**`MissingReferenceException` during scene teardown.**
`OnDestroy` touched another object that was already destroyed. Destruction order is not guaranteed —
don't reach across objects in `OnDestroy`.

**Save works on desktop, loses data on mobile.**
Saving only in `OnApplicationQuit`, which the OS doesn't call when it kills a backgrounded app. Save
in `OnApplicationPause(true)`.
---

## Review checklist

| Check | Look for |
|---|---|
| Bootstrap | No entry scene; services created ad hoc in gameplay scenes |
| Editor entry | Pressing Play on a gameplay scene throws null service errors |
| Statics | Static fields or events with no `ResetStatics` while domain reload is off |
| Static events | `ScoreChanged = null` missing from the reset |
| DontDestroyOnLoad | Used on many objects; no duplicate guard |
| Scene loading | `LoadSceneMode.Single` used where additive was meant |
| Progress | Loading bar that never passes 90% (`allowSceneActivation` misunderstanding) |
| Active scene | `SetActiveScene` not called after an additive load |
| Mobile save | Saving only in `OnApplicationQuit` |

---

## Learn more

- [Scene management](https://docs.unity3d.com/6000.3/Documentation/Manual/scenes-working-with.html)
- [Domain reloading](https://docs.unity3d.com/6000.3/Documentation/Manual/domain-reloading.html)
- [Order of execution for event functions](https://docs.unity3d.com/6000.3/Documentation/Manual/execution-order.html)
