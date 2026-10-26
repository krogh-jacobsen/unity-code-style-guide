# Unity animation audit

Load for Animator parameters, transitions/interruption, animation events, root motion, or culling.
Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Use `unity:unity-cli` (or the
Editor) to inspect saved controllers/clips and runtime state; this guide adds ownership and
gameplay-correctness checks. Animation cost is owned by
[Performance](UnityPerformanceOptimizationInstructions.md); this lens covers correctness only.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Parameter contract | Controller parameter names/types from a controller dump or its saved asset; every `Set*`/`Get*` call and cached hash in code | A code-set parameter name or type does not exist in the controller, or code assumes an override controller adds parameters |
| State ownership | Writers per parameter and layer (search the `Set*` calls); reads of Animator state in gameplay rules | Two or more code paths write one parameter in the same update, or a gameplay outcome (damage, reward, win) is decided by reading Animator state |
| Transition semantics | Controller dump: Has Exit Time, duration, interruption source for each input-driven transition | An input-driven transition has Has Exit Time enabled with no documented reason, or its duration exceeds the project's stated response budget (confirm the player-visible delay with a live run) |
| Pending triggers | Every `SetTrigger` writer against the transitions that consume it, plus cancel/interrupt/disable paths | A trigger has writers but no transition in any layer consumes it, or a canceled/disabled action fires later after re-enable (live run) |
| Event safety | Clip events: function names, receiving components, clip reuse across states | An event names a function absent from every component on the same object, or required cleanup runs only from an event on a clip that can be interrupted or looped |
| Root-motion writer | `applyRootMotion`, any `OnAnimatorMove`, and the physics/controller writers on the same object | Root motion and another writer conflict on the same pose, or a runtime `applyRootMotion` toggle re-initializes the Animator and causes an unintended state change (confirm live). `OnAnimatorMove` takes control of root motion; an ignored `applyRootMotion` flag alone is no finding |
| Controller/override lifetime | Search `runtimeAnimatorController` assignments and `new AnimatorOverrideController` | One override instance is mutated while assigned to several Animators, or a runtime swap has no check of the resulting state |
| Culling correctness | `cullingMode` per Animator against gameplay that reads its events, root motion, or bone transforms | The configured culling mode suppresses a required event, root-motion result, or bone update and changes gameplay offscreen (confirm the specific behavior live); mode plus dependency alone is a candidate |

## Interpret with care

- ℹ️ Cache frequently used hashes according to project conventions, then verify their controller
  contract. A cached hash does not prevent typos and should not serve as a stable save identifier.
- ℹ️ Exit time and deliberate transition duration can be correct. The `SetTrigger` reference says a
  trigger returns to false automatically, but does not say when or what consumes it, and its example
  calls `ResetTrigger` on the other trigger first. Reset a trigger when the ownership contract requires
  canceling pending work; `ResetTrigger` before every `SetTrigger` is not a universal fix.
- ℹ️ Animation events can time presentation/hit windows, but interruption still needs reliable state
  cleanup. Inspect invulnerability, hitboxes, reservations, and audio/VFX on every exit path.
- ℹ️ Shared override controllers are useful only when their mappings should be shared. An actor-specific
  mutable mapping may require its own instance. The reference documents that swapping an
  `AnimatorOverrideController` based on the same controller does not reset the current state; it does
  not state parameter behavior, so verify that on the installed engine.
- ℹ️ `AnimatorCullingMode` documents `AlwaysAnimate` (animated even offscreen), `CullCompletely`
  (animation disabled when renderers are not visible), and `CullUpdateTransforms` (retarget, IK, and
  transform writes disabled). The page states no default and does not mention root motion, so treat
  culling first as a behavior decision and verify root-motion and event needs live. Measure any cost
  change with [Performance](UnityPerformanceOptimizationInstructions.md) before editing culling.

## Validation

Play the real action, cancel/interrupt it at relevant points, disable/re-enable, switch clip sets,
and move offscreen. Verify exactly-once effects and reliable cleanup. Use the actual collider/mover
for root-motion checks.

Persisted controller/clip edits must use Unity's Editor APIs; see
[Editor tooling](UnityEditorToolingInstructions.md).

Technical references: [Animator.applyRootMotion](https://docs.unity3d.com/ScriptReference/Animator-applyRootMotion.html),
[AnimatorCullingMode](https://docs.unity3d.com/ScriptReference/AnimatorCullingMode.html), and
[Animator.runtimeAnimatorController](https://docs.unity3d.com/ScriptReference/Animator-runtimeAnimatorController.html).
