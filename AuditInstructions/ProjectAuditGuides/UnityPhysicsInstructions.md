# Unity 3D physics audit

Load for Rigidbody motion, collider contacts/triggers, tunnelling, or physics-query results. This
is a 3D PhysX lens: use [Physics2D](UnityPhysics2DInstructions.md) for classic 2D; DOTS Physics
needs its installed package documentation and specialist review. Apply [the shared evidence standard](ProjectReview.md#evidence-standard).
`unity:physics-3d-collision` (when available) owns detailed collision diagnosis and parameter recipes;
without it, use the checks below and the official docs.
**Last verified: October 2026.** Re-read the linked pages against the installed Editor before quoting
a default.

## Establish the simulation

Inspect the saved and live body/collider pair, layer matrix/overrides, trigger flags, movement owner,
physics scene, simulation mode, and timestep. Confirm callback signatures and target versions.
A script alone does not prove what colliders and bodies exist on its runtime object. A saved
scene/prefab dump or `unity:unity-cli` component listing gives the pair; a live run gives the contact.
A project that uses only kinematic bodies and queries (no dynamic Rigidbody contacts) records the
contact- and force-based rows it cannot trigger (Force units, Effect identity, Fast motion, and
Contact eligibility where no callbacks fire) Not applicable per row instead of failing them; a kinematic
body that raises trigger callbacks still needs Contact eligibility.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Movement ownership | Search for writes to `Rigidbody.position`, `linearVelocity`, `AddForce`, `MovePosition`, and `transform.position`/`Translate` on bodies; add network/teleport paths. List every writer per body. Root motion is owned by [Animation](UnityAnimationInstructions.md) | Active writers overwrite or fight the intended pose/velocity, or a transform write bypasses a simulated body’s movement contract; ordered contributions and deliberate teleports can be valid |
| Force units | `AddForce` mode, and any multiplication by `Time.deltaTime`/`Time.fixedDeltaTime`. One-shot input latching is owned by [Input](UnityInputSystemInstructions.md) | A continuous force mode (`Force`, `Acceleration`) is multiplied by a time step again, or `Impulse`/`VelocityChange` is applied every step where the result should scale with time |
| Contact eligibility | Saved or live collider/body types, trigger flags, layer matrix, callback signatures; compare the pair with the collision-action matrix in the installed version's manual | The layer matrix excludes the pair, a callback kind does not match the collider's trigger flag, or a callback signature takes the wrong parameter type |
| Effect identity | Colliders under each body root and the handlers on each | One interaction can reach a handler through more than one collider and no dedupe key exists; confirm by counting invocations for one interaction in a Play run (needs a live run) |
| Query contract | Mask, radius, `queryTriggerInteraction`, result use | Trigger interaction or mask is left at a default the use case contradicts, or code indexes `RaycastAll`/overlap results as if sorted (Unity documents the order as undefined) |
| Query completeness | Buffer length, returned count, overflow handling in every `*NonAlloc` call | Required all-hit, nearest-hit or post-filter semantics can lose relevant results when a finite buffer saturates without a completeness policy, or code consumes stale slots beyond the returned count. An any-hit boolean or explicit acceptable truncation may already satisfy its contract |
| State synchronization | Transform writes in `Update`/`LateUpdate` followed by a query in the same frame; `Physics.SyncTransforms` calls | A required query observes stale geometry after a pose change, or measured redundant synchronization violates a budget. Inspect actual write/query/simulation order and auto-sync mode; callback name alone is insufficient |
| Fast motion | Max speed, `Time.fixedDeltaTime`, thinnest collider extent on each side, `collisionDetectionMode` per body | Supported speed/timestep/geometry produces a missed required collision (confirm live). Speed × step versus thickness screens tunnelling risk; that estimate or discrete mode alone does not prove failure |
| Collider validity | Collider type, convexity, body type, `lossyScale` chain; Editor console or import output | An unsupported shape/body combination is established, or inspected geometry/contact differs from the intended shape. Non-uniform scale alone is a candidate; unavailable shape inspection is Not verified |
| Query origin | Ray origin versus containing colliders and intended initial-overlap behavior | A ray is expected to detect the collider containing its origin, leaving an inspected interaction/obstruction case wrong; 3D raycasts exclude that collider |
| Visual interpolation | Interpolation/extrapolation, camera follow, physics versus rendered pose, teleports | Observed jitter, overshoot, or latency breaks the required visual/aim contract; interpolation adds a physics-step delay and extrapolation can overshoot |

## Interpret with care

- ℹ️ Use forces/velocity for simulated motion and the supported kinematic movement path for driven
  bodies. Deliberate teleports need an explicit pose/velocity/interpolation contract. A transform
  write does not by itself prove velocity was discarded; inspect the actual movement behavior.
- ℹ️ In `FixedUpdate`, `Time.deltaTime` returns the fixed-step interval, so `Time.fixedDeltaTime`
  expresses intent more clearly; the former alone is not a timing bug. `AddForce` applies timestep
  scaling for continuous force modes, but `Impulse` and `VelocityChange` do not depend on step length.
- ℹ️ Continuous collision detection (CCD) is set on the moving body. The `Continuous` mode detects
  static mesh geometry without a Rigidbody, so do not add a Rigidbody to every wall. The reference
  lists support for sphere, capsule, and box colliders on the body, and recommends `ContinuousDynamic`
  for fast bodies and `Continuous` for the bodies they hit. Verify this against the installed version.
- ℹ️ Non-allocating queries trade allocation for finite result capacity. The reference notes that a
  full buffer is not guaranteed to hold the closest hits, so "count == capacity" needs an explicit
  completeness policy when omitted hits affect correctness. A single-hit `Raycast` overload returns one
  `RaycastHit` through `out`, not an array.
- ℹ️ A radius-based overlap has no max-distance argument. Require a meaningful spatial bound, not
  parameters the API cannot accept. Choose Update/fixed/manual timing from the query's purpose.
- ℹ️ The `Physics.SyncTransforms` reference advises against calling it in `FixedUpdate` (transforms
  sync before each step), for synchronizing changed transforms when an immediate query needs them, and against overuse because it is expensive. Manual physics stepping alone does
  not establish cross-platform determinism; verify on the target platforms.
- ℹ️ Rigidbody API renames (`velocity` to `linearVelocity`, `drag` to `linearDamping`) are tracked in
  [UnityTechStack](../../AgentsInstructions/UnityTechStack/UnityTechStack.md); verify them in the target's 3D and 2D APIs.

## Validation

Reproduce the actual pair and effect. Test representative speed/timestep extremes, compound-collider
hits, full query buffers, layer/trigger exclusions, and teleports where applicable. Verify saved
settings survive reopening. Mark unresolved live geometry/contact checks as Not verified.

Technical references: [CCD and collisionDetectionMode](https://docs.unity3d.com/ScriptReference/Rigidbody-collisionDetectionMode.html),
[Time.deltaTime](https://docs.unity3d.com/ScriptReference/Time-deltaTime.html), and
[Physics.SyncTransforms](https://docs.unity3d.com/ScriptReference/Physics.SyncTransforms.html).

Additional references: [ray origin behavior](https://docs.unity3d.com/ScriptReference/Physics.Raycast.html)
and [interpolation tradeoffs](https://docs.unity3d.com/Manual/rigidbody-interpolation.html).

Finite-buffer reference: [RaycastNonAlloc results and saturation](https://docs.unity3d.com/ScriptReference/Physics.RaycastNonAlloc.html).
