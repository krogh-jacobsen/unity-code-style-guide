# Unity Animation

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Animator controllers, parameters, events, and what they cost.

The Animator is a state machine you configure in a window rather than in code, which makes it easy to
build and hard to debug. Most animation bugs are one of three things: **a parameter name typo**, **a
transition condition that never becomes true**, or **a trigger that was consumed by the wrong
state**.

For the *naming* rules on parameters, layers and tags, see the
[style guide](../UnityStyleGuide.md#animation-parameters-layers-tags-sorting-layers-and-input-action-names).
This guide covers the animation system itself.

Table of contents:
- [Parameter hashes](#parameter-hashes)
- [Setting parameters correctly](#setting-parameters-correctly)
- [Triggers vs. bools](#triggers-vs-bools)
- [Transitions and CrossFade](#transitions-and-crossfade)
- [Blend trees](#blend-trees)
- [Layers and avatar masks](#layers-and-avatar-masks)
- [Animation events](#animation-events)
- [AnimatorOverrideController](#animatoroverridecontroller)
- [Root motion](#root-motion)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## Parameter hashes

- ✅ **Always hash parameter names with `Animator.StringToHash`.** Every string overload of
  `SetBool`/`SetFloat`/`SetTrigger` does the hash lookup internally, every call.
- ✅ Store hashes in `static readonly int` fields so they're computed once per type, not per instance.
- ✅ Keep them in one class per controller so the set of parameters is discoverable.
- ⚠️ A misspelled parameter name **fails silently**. No exception, no warning — the animation simply
  doesn't play. This is the single biggest time sink in Unity animation work.

```csharp
public static class PlayerAnimatorParams
{
    public static readonly int IsRunning   = Animator.StringToHash("IsRunning");
    public static readonly int IsGrounded  = Animator.StringToHash("IsGrounded");
    public static readonly int Speed       = Animator.StringToHash("Speed");
    public static readonly int JumpTrigger = Animator.StringToHash("JumpTrigger");
    public static readonly int AttackIndex = Animator.StringToHash("AttackIndex");
}

[RequireComponent(typeof(Animator))]
public class PlayerAnimatorDriver : MonoBehaviour
{
    private Animator m_animator;

    private void Awake()
    {
        m_animator = GetComponent<Animator>();
    }

    public void SetMovement(float speed, bool isGrounded)
    {
        m_animator.SetFloat(PlayerAnimatorParams.Speed, speed);
        m_animator.SetBool(PlayerAnimatorParams.IsGrounded, isGrounded);
    }
}
```

- ℹ️ Hashes are only valid within a single run. Never serialize one or write it to a save file.

---

## Setting parameters correctly

- ✅ Drive the Animator from **one** component. Several scripts setting the same parameters is how
  you get flicker that's impossible to trace.
- ✅ Treat the Animator as a *view*: it renders state the gameplay code already decided. Don't read
  game logic out of animator state.
- ⚠️ `SetFloat` with a damping parameter (`SetFloat(hash, value, dampTime, deltaTime)`) smooths for
  you — cleaner than lerping into the parameter yourself.
- ⚠️ Setting a parameter on a disabled Animator does nothing and the value is not queued.

```csharp
// ❌ Two scripts writing the same parameter - last writer per frame wins, unpredictably
// PlayerMovement.cs:  m_animator.SetFloat(Speed, m_velocity.magnitude);
// PlayerCombat.cs:    m_animator.SetFloat(Speed, 0f);

// ✅ One driver, fed by both systems
public void SetMovement(float speed) => m_animator.SetFloat(PlayerAnimatorParams.Speed, speed, 0.1f, Time.deltaTime);
```

---

## Triggers vs. bools

| Use | When | Risk |
|---|---|---|
| `bool` | A state that persists (`IsGrounded`, `IsRunning`) | None — it's just a value |
| `trigger` | A one-shot event (`Jump`, `Hit`) | Queues until consumed; can fire late |
| `float` | A blend input (`Speed`, `Direction`) | None |
| `int` | Selecting a variant (`AttackIndex`) | Silent no-match if no transition covers the value |

- ⚠️ **A trigger stays set until a transition consumes it.** Set a trigger while no transition can
  fire, and it will fire later, at an unexpected moment.
- ✅ Call `ResetTrigger` when you set a trigger that may not be consumed — for example, on state exit
  or when interrupting an action.
- ✅ Prefer a `bool` when the condition is really a state. Triggers are for genuine one-shot events.

```csharp
public void Jump()
{
    // Clear any stale queued jump before setting a fresh one
    m_animator.ResetTrigger(PlayerAnimatorParams.JumpTrigger);
    m_animator.SetTrigger(PlayerAnimatorParams.JumpTrigger);
}
```

---

## Transitions and CrossFade

- ✅ Turn **Has Exit Time** off for anything responsive. Left on, the transition waits for the current
  clip to reach its exit point — which is why input feels laggy.
- ✅ Keep Transition Duration short (0.05–0.15s) for gameplay actions; longer only for deliberate
  blends.
- ✅ Use `CrossFade` / `CrossFadeInFixedTime` when you want to jump to a state from code without
  authoring a transition for every source state.
- ⚠️ `Play()` snaps with no blend. Fine for resets, jarring for gameplay.
- ⚠️ `CrossFade` takes normalized time by default; `CrossFadeInFixedTime` takes seconds. Mixing them
  up gives blends that are wildly too long or short.

```csharp
// Blend to a state over 0.1 real seconds, regardless of clip length
m_animator.CrossFadeInFixedTime(PlayerAnimatorStates.Attack, 0.1f);
```

- ✅ **Interruption Source** on a transition controls whether it can be cut short. Default is `None`,
  which means a queued transition must finish — another cause of unresponsive feel.

---

## Blend trees

- ✅ Use a 1D blend tree for speed-driven locomotion (idle → walk → run) rather than three states and
  six transitions.
- ✅ Use 2D Freeform Directional for strafing locomotion.
- ✅ Feed blend trees with damped `SetFloat` so the blend itself is smooth and you don't need
  transitions between the poses.
- ⚠️ Every clip in a blend tree is sampled and blended each frame, even at weight 0 in some modes.
  Keep trees small; a 12-clip tree is a real cost on a crowd.
- ✅ Set thresholds to match actual movement speeds, then tick *Automate Thresholds* off so tuning
  the speeds doesn't silently rescale them.

---

## Layers and avatar masks

- ✅ Use a second layer with an **avatar mask** for upper-body actions (aim, carry, wave) over a
  full-body locomotion base layer.
- ✅ Set the layer's Blending to **Override** for a full replacement, **Additive** for a modifier on
  top of the base pose.
- ⚠️ A layer with weight 0 still evaluates its state machine. Set weight to 0 *and* leave the layer
  in an empty state if it's genuinely unused.
- ✅ Drive layer weight with `SetLayerWeight` to fade an upper-body action in and out.
- ⚠️ Masks are per-layer, not per-state. A mask that's right for aiming will be wrong for a full-body
  reload — that needs a different layer or a base-layer state.

---

## Animation events

- ✅ Use animation events for things that must land on a specific frame: footstep audio, hitbox
  enable, VFX spawn.
- ⚠️ The receiving method must be on a component on the **same GameObject as the Animator**, and it
  must be public. Otherwise Unity logs a warning at runtime and nothing happens.
- ⚠️ Signatures are restricted: no parameters, or exactly one `int`, `float`, `string`,
  `AnimationEvent`, or `Object` reference. You cannot pass two values.
- ✅ Group event handlers in a `#region` so it's obvious they're called from outside the code — this
  is the sanctioned use of regions in the
  [style guide](../UnityStyleGuide.md#use-of-regions).
- ⚠️ Events on the last frame of a clip may not fire if the clip is interrupted or loops. Don't put
  cleanup there.
- ⚠️ Events are stored on the **clip**, so they fire from every state and every controller using it.

```csharp
[RequireComponent(typeof(Animator))]
public class PlayerAnimationEvents : MonoBehaviour
{
    [SerializeField] private WeaponHitbox m_hitbox;
    [SerializeField] private FootstepPlayer m_footsteps;

    #region Animation Event Methods
    // Called from the attack clip on the contact frame
    public void OnAttackContact()
    {
        m_hitbox.EnableForWindow();
    }

    // Called from locomotion clips; int selects the foot
    public void OnFootstep(int footIndex)
    {
        m_footsteps.Play(footIndex);
    }
    #endregion
}
```

---

## AnimatorOverrideController

- ✅ Use it to reuse one controller's structure with different clips — weapon variants, character
  skins, enemy tiers. One state machine, many clip sets.
- ✅ Build the override once and cache it. Creating one per instance duplicates the mapping table.
- ⚠️ Assigning `.runtimeAnimatorController` **resets the state machine** to its default state and
  clears parameter values. Do it during setup, not mid-action.
- ✅ Apply overrides in bulk with the `List<KeyValuePair<AnimationClip, AnimationClip>>` overload;
  the indexer overload rebuilds the table on every assignment.

```csharp
private void ApplyWeaponAnimations(WeaponDataSO weapon)
{
    var overrideController = new AnimatorOverrideController(m_baseController);

    var overrides = new List<KeyValuePair<AnimationClip, AnimationClip>>(overrideController.overridesCount);
    overrideController.GetOverrides(overrides);

    for (int i = 0; i < overrides.Count; i++)
    {
        AnimationClip replacement = weapon.GetClipFor(overrides[i].Key.name);
        if (replacement != null)
        {
            overrides[i] = new KeyValuePair<AnimationClip, AnimationClip>(overrides[i].Key, replacement);
        }
    }

    overrideController.ApplyOverrides(overrides);   // One rebuild, not one per clip
    m_animator.runtimeAnimatorController = overrideController;
}
```

---

## Root motion

- ✅ Use root motion when the animation defines the movement — melee lunges, climbs, precise turns.
- ✅ Use scripted movement when gameplay defines it. Mixing both on one axis fights itself.
- ⚠️ Root motion and a `CharacterController`/`Rigidbody` both writing position is the classic
  "character slides" or "character won't move" bug. Pick one owner per axis.
- ✅ `OnAnimatorMove` lets you intercept root motion and apply it through your own mover, which is
  usually the right answer when you need both.
- ⚠️ `Apply Root Motion` off on the Animator means `deltaPosition` is still computed but not applied
  — you can read it in `OnAnimatorMove` and use it yourself.

```csharp
private void OnAnimatorMove()
{
    // Take the animation's intended motion, apply it through the CharacterController
    // so collision is still respected.
    Vector3 delta = m_animator.deltaPosition;
    delta.y = m_verticalVelocity * Time.deltaTime;   // Gravity stays ours

    m_characterController.Move(delta);
    transform.rotation *= m_animator.deltaRotation;
}
```

---

## Performance

- ⚠️ Every `Animator` has a fixed per-frame cost even when idle in a single state. A crowd of a
  hundred is measurable before any clip plays.
- ✅ Set **Culling Mode** to `Cull Update Transforms` (stops writing transforms offscreen) or
  `Cull Completely` (stops evaluating entirely). The default, `Always Animate`, evaluates offscreen
  characters forever.
- ✅ Disable the Animator component outright for characters that are idle and far away.
- ✅ Tick **Optimize Game Objects** on the model importer to collapse the bone hierarchy into an
  internal representation. Expose only the bones you actually need to attach things to.
- ⚠️ Never put an `Animator` on uGUI elements — it dirties the canvas every frame. See
  [uGUI](UnityUGUIInstructions.md#never-animate-ui-with-an-animator).
- ✅ For simple, non-blended motion (a rotating pickup, a bobbing platform), plain code in `Update`
  is far cheaper than an Animator.
- ℹ️ Profiler markers to watch: `Animators.Update`, `MeshSkinning.Update`, `Animation.Rebind`.
  `Animation.Rebind` appearing every frame means something is reassigning the controller.

---

## Troubleshooting

**Nothing plays and there's no error.**
Almost always a parameter name mismatch — the string in code doesn't match the parameter in the
controller. Unity does not warn about this.

```csharp
// Diagnostic: dump the Animator's actual state
private void LogAnimatorState()
{
    Debug.Log($"Controller: {m_animator.runtimeAnimatorController?.name ?? "NONE"}", this);
    Debug.Log($"Enabled: {m_animator.enabled}, Speed: {m_animator.speed}, " +
              $"Culling: {m_animator.cullingMode}");

    foreach (AnimatorControllerParameter p in m_animator.parameters)
    {
        Debug.Log($"  param '{p.name}' ({p.type})");   // Compare against your constants
    }

    AnimatorStateInfo state = m_animator.GetCurrentAnimatorStateInfo(0);
    Debug.Log($"  layer 0 state hash {state.shortNameHash}, normalized time {state.normalizedTime:F2}");
}
```

**Transition never fires.**
Check the condition against the parameter's live value in the Animator window during play. Common
causes: a float condition using `Greater` when the value never quite reaches the threshold, or
`Has Exit Time` on with a clip that loops so exit time never arrives.

**Animation fires one action too late.**
A trigger was set while no transition could consume it, so it stayed queued. Add `ResetTrigger`
before setting, or use a bool.

**Input feels laggy.**
`Has Exit Time` is on, the transition duration is long, or Interruption Source is `None` so a
queued transition must finish first.

**Animation event does nothing.**
The handler isn't public, isn't on the same GameObject as the Animator, or has an unsupported
signature. Unity logs *"has no receiver"* — check the Console with warnings enabled.

**Character slides, or won't move at all.**
Root motion and scripted movement are both writing position. Decide which owns each axis.

**Character animates but doesn't move after switching controllers.**
Assigning `runtimeAnimatorController` reset the state machine and cleared parameters. Re-apply state
after the assignment.

**Animation plays in the Editor preview but not at runtime.**
The state isn't reachable — no transition path from the default state, or the layer weight is 0.

---

## Review checklist

| Check | Look for |
|---|---|
| Hashes | String literals in `SetBool`/`SetFloat`/`SetTrigger` |
| Hash storage | `StringToHash` called per instance instead of `static readonly` |
| Ownership | More than one component writing the same parameter |
| Triggers | `SetTrigger` with no `ResetTrigger` on interruption paths |
| Triggers | A trigger used where a bool would model the state better |
| Transitions | `Has Exit Time` on for responsive gameplay actions |
| Events | Handler not public, or not on the Animator's GameObject |
| Override controllers | Created per instance instead of cached |
| Root motion | Root motion and scripted movement on the same axis |
| Culling | Culling Mode left at `Always Animate` |
| UI | An `Animator` on a GameObject with a `Graphic` |
| Cost | An Animator used for simple constant motion |

---

## Learn more

- [Animation section, Unity manual](https://docs.unity3d.com/6000.3/Documentation/Manual/AnimationSection.html)
- [Animator Controller](https://docs.unity3d.com/6000.3/Documentation/Manual/class-AnimatorController.html)
- [Animation events](https://docs.unity3d.com/6000.3/Documentation/Manual/script-AnimationWindowEvent.html)
