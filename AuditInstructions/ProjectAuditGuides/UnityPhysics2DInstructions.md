# Unity 2D physics audit

Load for owned Rigidbody2D/Collider2D, joints/effectors, Physics2D queries, or 2D callbacks. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Establish body types, simulated state,
layers/overrides, trigger settings, physics scene, simulation mode, timestep, and actual saved pair.
The [3D Physics lens](UnityPhysicsInstructions.md) has a different contact/query contract; DOTS
Physics is also separate. **Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Contact eligibility | Dynamic/kinematic/static pair, Full Kinematic Contacts, trigger/layers, callback signature | The configured pair cannot produce the required solid contact/callback under the installed 2D matrix; account for trigger exceptions |
| Movement ownership | Transform/velocity/force/MovePosition writers and automatic/manual stepping | Writers overwrite intended motion, or repeated pre-step MovePosition calls lose intended movement. Ordered contributions and teleports can be valid |
| Step ownership | `simulationMode`, Simulate callers, FixedUpdate and time units | Integration steps twice, is skipped, or consumes input on the wrong cadence. Manual Simulate does not invoke FixedUpdate |
| Query contract | Actual overload, ContactFilter2D, layers/depth/triggers, initial overlaps and returned count | Wrong/self/initial-overlap results are consumed, or required hits are omitted without a capacity policy; inspect the actual overload's ordering contract |
| Callback lifetime | Disabled scripts/objects, pooling and interaction identity | A disabled MonoBehaviour still applies forbidden effects through a 2D trigger callback, or compound hits duplicate one intended effect |
| Fast motion | Required speed/geometry/timestep and collision mode | A supported interaction tunnels or a required contact is missed (live); continuous mode has cost and is not a universal setting |
| Authored geometry | Composite/Tilemap generation, joints and effector configuration where used | Saved geometry/constraints or one-way behavior differs from the required interaction after reopening or runtime changes |

## Interpret with care

Full Kinematic Contacts changes solid-contact eligibility; triggers have different rules. A 2D ray
can report a containing collider at fraction zero with an inverse-ray normal; copying the 3D
ray-origin rule would be wrong. MovePosition is consumed on the next simulation update and has motion
limits; choose cadence from the actual simulation owner. Fixed steps improve repeatability without
proving cross-platform determinism. Input capture belongs in [Input](UnityInputSystemInstructions.md).

## Validation

Test intended body pairs, excluded layers, triggers, start-inside/self queries, saturated buffers,
compound interactions, pause, pooling, and zero/multiple steps per rendered frame. Traverse composite
borders and one-way platforms where used; reopen saved assets. Report unperformed live checks Not verified.
Joint tuning beyond these contracts needs installed documentation and representative solver evidence.

Technical references: [kinematic contacts](https://docs.unity3d.com/Manual/2d-physics/rigidbody/body-types/kinematic/kinematic-body-type-reference.html),
[MovePosition](https://docs.unity3d.com/ScriptReference/Rigidbody2D.MovePosition.html),
[manual simulation](https://docs.unity3d.com/ScriptReference/Physics2D.Simulate.html),
[ray origins](https://docs.unity3d.com/ScriptReference/Physics2D.Raycast.html), and
[disabled-script trigger delivery](https://docs.unity3d.com/ScriptReference/Collider2D.OnTriggerEnter2D.html).
