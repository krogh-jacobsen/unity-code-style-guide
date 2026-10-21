# Unity animation audit

Load for Animator parameters, transitions/interruption, animation events, root motion, or culling.
Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Use `unity-cli` to inspect saved
controllers/clips and runtime state; this guide adds ownership and gameplay-correctness checks.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Parameter contract | Controller parameter names/types, code IDs, override controller | Code writes a missing/wrong-type parameter or relies on an unverified controller layout |
| State ownership | Writers per parameter/layer and domain decisions | Multiple writers conflict or animation state accidentally becomes authoritative game state |
| Transition semantics | Conditions, exit time, duration units, interruption policy | Input/action timing differs from the game's intended behavior |
| Pending triggers | Unconsumed triggers and cancel/interruption/re-enable paths | A canceled action fires later from a stale trigger |
| Event safety | Clip reuse, receiver/signature, interruption and loop behavior | Events apply an effect twice or required cleanup depends on an event that may be skipped |
| Movement ownership | Root-motion handler, physics/controller/network movement | Animation and gameplay movement fight each other on the same pose/axis |
| Controller/override lifetime | Shared versus per-instance mappings, assignment and cleanup | One actor changes another's clips or controller replacement loses required state |
| Culling correctness | Offscreen state, root motion/events, gameplay dependencies | Culling stops required behavior or unrestricted evaluation causes verified excess cost |

## Interpret with care

- ℹ️ Cache frequently used hashes according to project conventions, then verify their controller
  contract. A cached hash does not prevent typos and should not serve as a stable save identifier.
- ℹ️ Exit time and deliberate transition duration can be correct. Reset a trigger when the ownership
  contract requires canceling pending work; ResetTrigger before every SetTrigger is not a universal fix.
- ℹ️ Animation events can time presentation/hit windows, but interruption still needs reliable state
  cleanup. Inspect invulnerability, hitboxes, reservations, and audio/VFX on every exit path.
- ℹ️ Shared override controllers are useful only when their mappings should be shared. An actor-specific
  mutable mapping may require its own instance. Verify replacement behavior for the installed engine
  rather than assuming every assignment resets every parameter.
- ℹ️ Treat offscreen animation/culling as a behavior decision before a performance change. Root motion
  or authoritative animation events may require evaluation even when the renderer is invisible.

## Validation

Play the real action, cancel/interrupt it at relevant points, disable/re-enable, switch clip sets,
and move offscreen. Verify exactly-once effects and reliable cleanup. Use the actual collider/mover
for root-motion checks. Measure crowd/animation cost with
[Performance](UnityPerformanceOptimizationInstructions.md) before changing culling or controller structure.

Persisted controller/clip edits must use Unity's Editor APIs; see
[Editor tooling](UnityEditorToolingInstructions.md).
