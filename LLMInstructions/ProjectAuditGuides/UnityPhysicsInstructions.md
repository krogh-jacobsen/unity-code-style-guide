# Unity 3D physics audit

Load for Rigidbody motion, collider contacts/triggers, tunnelling, or physics-query results. This
is a 3D PhysX lens; use the project's 2D guidance for Physics2D. Apply
[the shared evidence standard](ProjectReview.md#evidence-standard). `physics-3d-collision` owns detailed
collision diagnosis and parameter recipes.

## Establish the simulation

Inspect the saved and live body/collider pair, layer matrix/overrides, trigger flags, movement owner,
physics scene, simulation mode, and timestep. Confirm callback signatures and target versions.
A script alone does not prove what colliders and bodies exist on its runtime object.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Movement ownership | Forces, velocity, root motion, transforms, network/teleport paths | Multiple writers fight the simulation or continuous movement bypasses required collision behavior |
| Input/tick semantics | Latching, simulation update mode, force mode/units | One-shot input is lost/repeated or force is integrated twice/wrongly scaled |
| Contact eligibility | Actual collider/body types, callbacks, layers, trigger policy | The intended pair cannot produce the required contact/callback |
| Effect identity | Both callback recipients, compound colliders, duplicate hits | One gameplay interaction applies damage/reward multiple times unintentionally |
| Query contract | Mask, range/radius, trigger policy, result ordering | The query considers wrong objects or assumes a hit order Unity does not promise |
| Query completeness | Buffer capacity, hit count, overflow policy | A full non-alloc buffer silently drops required results or code reads entries beyond the returned count |
| State synchronization | Transform writes and queries before simulation sync | A query sees an unintended older physics state |
| Fast motion | Speeds, collider thickness/shapes, CCD pair, timestep | A reproduced or clearly bounded collision risk is left unhandled |
| Collider validity | Imported/cooked shape, convexity, body type, scale | Unsupported geometry/body setup or an unintended collision shape reaches gameplay |

## Interpret with care

- ℹ️ Use forces/velocity for simulated motion and the supported kinematic movement path for driven
  bodies. Deliberate teleports need an explicit pose/velocity/interpolation contract. A transform
  write does not by itself prove velocity was discarded; inspect the actual movement behavior.
- ℹ️ In `FixedUpdate`, `Time.deltaTime` returns the fixed-step interval. `Time.fixedDeltaTime` can
  express intent more clearly; the former alone is not a timing bug. `AddForce` already applies
  timestep scaling for continuous force modes; inspect units before multiplying by time again.
- ℹ️ Static geometry has no Rigidbody CCD setting. Select moving-body modes based on the actual pair
  and supported shape; do not add a Rigidbody to every wall to satisfy a two-sided CCD slogan.
- ℹ️ Non-allocating queries trade allocation for finite result capacity. "count == capacity" needs
  an explicit completeness policy when omitted hits affect correctness. A single-hit raycast
  already avoids a result array; see [Performance](UnityPerformanceOptimizationInstructions.md).
- ℹ️ A radius-based overlap has no max-distance argument. Require a meaningful spatial bound, not
  parameters the API cannot accept. Choose Update/fixed/manual timing from the query's purpose.
- ℹ️ `Physics.SyncTransforms` is justified when a query must observe a pending transform write; avoid
  using it indiscriminately. Manual physics stepping is not proof of cross-platform determinism.

## Validation

Reproduce the actual pair and effect. Test representative speed/timestep extremes, compound-collider
hits, full query buffers, layer/trigger exclusions, and teleports where applicable. Verify saved
settings survive reopening. Mark unresolved live geometry/contact checks as Not verified.

Technical references: [CCD](https://docs.unity3d.com/6000.0/Documentation/Manual/ContinuousCollisionDetection.html)
and [Time.deltaTime](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Time-deltaTime.html).
