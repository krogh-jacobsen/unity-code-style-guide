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
| State ownership | Writers per parameter and layer (search the `Set*` calls); reads of Animator state in gameplay rules | Conflicting writers produce wrong state/effects, or Animator-driven gameplay violates a binding domain rule. State queries and intentionally ordered writers alone are valid; architectural separation is otherwise a proposal |
| Transition semantics | Controller dump: Has Exit Time, duration, interruption source for each input-driven transition | The configured exit/interruption/duration behavior breaks an intended action/cancel response. Interpret Fixed Duration in seconds and other durations relative to source-state length/speed; confirm player-visible delay live |
| Pending triggers | Every `SetTrigger` writer against the transitions that consume it, plus cancel/interrupt/disable paths | A trigger has writers but no transition in any layer consumes it, or a canceled/disabled action fires later after re-enable (live run) |
| Event safety | Clip events: function names, receiving components, clip reuse across states | An event names a function absent from every component on the same object, or required cleanup runs only from an event on a clip that can be interrupted or looped |
| Root-motion writer | `applyRootMotion`, any `OnAnimatorMove`, and the physics/controller writers on the same object | Root motion and another writer conflict on the same pose, or a runtime `applyRootMotion` toggle re-initializes the Animator and causes an unintended state change (confirm live). `OnAnimatorMove` takes control of root motion; an ignored `applyRootMotion` flag alone is no finding |
| Controller/override lifetime | Search `runtimeAnimatorController` assignments and `new AnimatorOverrideController` | A shared mutable override leaks actor-specific mappings, or a controller swap loses required state; shared mappings and a swap alone are valid |
| Culling correctness | `cullingMode` per Animator against gameplay that reads its events, root motion, or bone transforms | The configured culling mode suppresses a required event, root-motion result, or bone update and changes gameplay offscreen (confirm the specific behavior live); mode plus dependency alone is a candidate |
| Clock alignment | `updateMode`, scaled/unscaled time, pause policy, physics and root-motion timing | The selected clock freezes required animation or disagrees with intended collider/movement timing (confirm live); choose mode per actor/use case |

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

Additional references: [transition duration/interruption](https://docs.unity3d.com/Manual/class-Transition.html),
[update clocks](https://docs.unity3d.com/ScriptReference/AnimatorUpdateMode.html). Skinned deformation
and visibility bounds are checked in [Rendering](UnityRenderingInstructions.md).
