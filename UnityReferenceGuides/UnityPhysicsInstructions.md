# Unity Physics

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

3D PhysX: moving bodies, collision callbacks, colliders, and queries.

**Query cost is not covered here.** Non-allocating overloads, cached layer masks and buffer reuse
live in [Performance](UnityPerformanceOptimizationInstructions.md#physics-optimization), because
they're an allocation decision rather than a physics one. This guide covers which API is
*correct*; that one covers making it *cheap*.

Table of contents:
- [Choosing how to move a body](#choosing-how-to-move-a-body)
- [FixedUpdate and the timestep](#fixedupdate-and-the-timestep)
- [Interpolation](#interpolation)
- [Collision detection modes](#collision-detection-modes)
- [What actually fires](#what-actually-fires)
- [Colliders](#colliders)
- [Layer collision matrix](#layer-collision-matrix)
- [Queries](#queries)
- [Simulation control](#simulation-control)
- [Unity 6 API changes](#unity-6-api-changes)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## Choosing how to move a body

Most physics bugs are this decision made wrong. Pick from the table, then never mix approaches on
one object.

| The object | How to move it | Where |
|---|---|---|
| Simulated — falls, gets pushed, bounces | `AddForce` / `AddTorque` | `FixedUpdate` |
| Script-driven but must push and carry things — platforms, elevators, kinematic characters | `MovePosition` / `MoveRotation` on a kinematic body | `FixedUpdate` |
| Needs one instant velocity change — a jump | Assign `linearVelocity` once | `FixedUpdate` |
| Has no Rigidbody at all — scenery, markers | `transform.position` | Anywhere |
| Teleporting a body deliberately, accepting the discontinuity | `transform.position`, then zero `linearVelocity` | `FixedUpdate` |

- ❌ **Never write `transform.position` on an active non-kinematic Rigidbody.** It teleports the
  body inside PhysX: velocity is discarded, continuous collision detection is skipped for that
  step, and the transform has to be re-synced into the physics scene. Objects pass through walls
  and forces behave unpredictably.
- ✅ Always pass an explicit `ForceMode`. `Force` for sustained thrust, `Impulse` for an instant
  kick, `Acceleration` and `VelocityChange` when the body's mass should be ignored.
- ⚠️ `MovePosition` on a **non**-kinematic body still interpolates toward the target rather than
  teleporting, but it fights the simulation. Use it on kinematic bodies.

```csharp
[RequireComponent(typeof(Rigidbody))]
public class Mover : MonoBehaviour
{
    [SerializeField] private float m_thrust = 10f;
    [SerializeField] private float m_jumpImpulse = 5f;

    private Rigidbody m_rigidbody;
    private Vector3 m_moveInput;
    private bool m_jumpQueued;

    private void Awake()
    {
        m_rigidbody = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        // Read input here — Update runs once per frame, FixedUpdate may not run at all.
        m_moveInput = ReadMoveInput();

        if (WasJumpPressed())
        {
            m_jumpQueued = true;
        }
    }

    private void FixedUpdate()
    {
        m_rigidbody.AddForce(m_moveInput * m_thrust, ForceMode.Force);

        if (m_jumpQueued)
        {
            m_rigidbody.AddForce(Vector3.up * m_jumpImpulse, ForceMode.Impulse);
            m_jumpQueued = false;
        }
    }
}
```

- ✅ Latch one-shot input in `Update` and consume it in `FixedUpdate`, as above. Reading a
  "pressed this frame" input directly in `FixedUpdate` drops presses on frames where physics
  doesn't step, and repeats them on frames where it steps twice.

---

## FixedUpdate and the timestep

- ℹ️ `FixedUpdate` runs zero, one, or many times per rendered frame. Never assume it pairs with
  `Update`.
- ✅ Use `Time.fixedDeltaTime` inside `FixedUpdate`, never `Time.deltaTime`.
- ✅ **Fixed Timestep** defaults to `0.02` (50 Hz). Raise it to `0.01666` (60 Hz) or `0.01111`
  (90 Hz) only when the game needs the precision — fast action, VR. Every increase is a
  proportional CPU cost.
- ⚠️ **Maximum Allowed Timestep** (default `0.333`) caps how much simulation one frame may run. It
  exists to stop the death spiral, where a slow frame schedules more physics steps, which makes the
  next frame slower. Don't raise it to "fix" slow-motion under load — profile instead.
- ⚠️ `Time.fixedDeltaTime` scales with `Time.timeScale`. Setting `timeScale = 0` stops
  `FixedUpdate` entirely.

---

## Interpolation

Physics runs at a fixed rate; rendering doesn't. Interpolation smooths the gap.

| Mode | Use it for | Cost |
|---|---|---|
| `None` | Everything by default. Objects the camera doesn't track closely. | Free |
| `Interpolate` | The player, anything the camera follows, anything a player stares at | One physics step of visual latency |
| `Extrapolate` | Fast projectiles where latency reads worse than overshoot | Overshoots on sudden impact or direction change |

- ✅ Turn `Interpolate` on for the player Rigidbody and little else. It is the standard fix for
  "my character stutters at high frame rates".
- ❌ Don't enable it on every Rigidbody in the scene. It costs per-body work and buys nothing for
  objects nobody is watching closely.
- ⚠️ Interpolation moves the *visual* transform between physics states. Reading
  `transform.position` mid-frame on an interpolated body gives you the smoothed value, not the
  simulated one.

---

## Collision detection modes

Fast objects tunnel through thin colliders because discrete detection only tests discrete
positions. The fix is a *pair* of settings, not one.

| Mode | Detects against | Use for |
|---|---|---|
| `Discrete` | Other discrete bodies, at step positions | Default. Everything slow. |
| `Continuous` | Sweeps against **static** geometry | Static walls and floors that fast objects hit |
| `ContinuousDynamic` | Sweeps against static **and** `Continuous`/`ContinuousDynamic` bodies | The fast object itself |
| `ContinuousSpeculative` | Speculative contacts, works on kinematic bodies | Fast kinematic bodies; cheaper than the above |

- ✅ Set the fast object to `ContinuousDynamic` **and** the things it must not pass through to
  `Continuous`. Setting only one side is the usual reason "I turned on continuous and it still
  tunnels".
- ⚠️ Continuous detection is only supported on Rigidbodies with **Sphere, Capsule or Box**
  colliders. A fast body with a MeshCollider will still tunnel.
- ✅ `ContinuousSpeculative` is the only continuous mode that works on kinematic bodies, and it is
  cheaper than the sweep-based modes.
- ❌ Don't set everything to `ContinuousDynamic`. It is the most expensive mode in the engine.

---

## What actually fires

Unity's collision action matrix, condensed. **A collider with no Rigidbody anywhere in the pair
sends nothing.** This one rule explains most "my trigger doesn't work" reports.

| | Static | Dynamic | Kinematic |
|---|---|---|---|
| **Static** | — | `OnCollision*` | — |
| **Dynamic** | `OnCollision*` | `OnCollision*` | `OnCollision*` |
| **Kinematic** | — | `OnCollision*` | — |

With `isTrigger` on either collider, the pair sends `OnTrigger*` instead of `OnCollision*` — and
only when at least one of the two objects has a Rigidbody, kinematic or not.

- ✅ To make a static trigger volume detect a moving object, the **moving object** needs the
  Rigidbody. A trigger box with no Rigidbody and a player with no Rigidbody detect nothing.
- ✅ Give a purely script-moved detector a **kinematic** Rigidbody. That is the standard way to make
  a moving trigger volume work without introducing physics simulation.
- ℹ️ Trigger colliders never send collision messages, and collision messages never fire for two
  static colliders.
- ⚠️ `OnCollisionEnter` receives a `Collision`; `OnTriggerEnter` receives a `Collider`. They are
  not interchangeable, and writing the wrong signature fails silently — Unity simply never calls it.
- ⚠️ Both objects receive the callback. Don't apply an effect on both sides or it happens twice.

```csharp
private void OnTriggerEnter(Collider other)
{
    // CompareTag does not allocate; other.tag == "Player" does.
    if (!other.CompareTag("Player"))
    {
        return;
    }

    // TryGetComponent avoids the null-check-after-GetComponent dance.
    if (other.TryGetComponent(out Health health))
    {
        health.ApplyDamage(m_damage);
    }
}
```

---

## Colliders

- ✅ Prefer primitives — Sphere, Capsule, Box. A compound of three primitives beats one
  MeshCollider almost every time, for both cost and contact quality.
- ⚠️ **Convex** MeshColliders are capped at **255 triangles**. Unity silently simplifies past that,
  so the collision shape stops matching the mesh you can see.
- ❌ A non-convex MeshCollider on a non-kinematic Rigidbody is not supported and logs an error at
  runtime. Non-convex is for static level geometry and kinematic bodies only.
- ❌ A non-convex MeshCollider cannot be a trigger.
- ℹ️ Two non-convex MeshColliders cannot collide with each other. At least one side must be convex
  or a primitive.
- ✅ Author collision geometry separately from render geometry. A 20k-triangle visual mesh reused as
  a collider is a common and expensive mistake.

---

## Layer collision matrix

- ✅ Prune **Project Settings → Physics → Layer Collision Matrix** early. Unchecked pairs are
  skipped in broad phase, before any contact work happens — this is the cheapest physics
  optimisation available.
- ✅ Give queries their own layers. A layer that only raycasts never needs to collide with anything.
- ⚠️ The matrix is project-wide state that no scene records. A pair disabled here is invisible to
  someone reading the code, so document non-obvious entries in
  [`UnityCustomInstructions/`](../UnityCustomInstructions/).

---

## Queries

Allocation rules live in
[Performance](UnityPerformanceOptimizationInstructions.md#physics-optimization). What matters for
correctness:

- ✅ Always pass a **layer mask** and a **max distance**. An unbounded query against every layer is
  both slow and usually wrong — it hits the caster's own collider first.
- ✅ Pass `QueryTriggerInteraction.Ignore` (or `Collide`) explicitly per query rather than relying on
  the project default.
- ℹ️ `Physics.queriesHitTriggers` is a **`bool`** project-wide default, not an enum. The per-query
  `QueryTriggerInteraction` parameter overrides it.
- ✅ Batch many independent raycasts with `RaycastCommand.ScheduleBatch` and the Jobs system. AI
  line-of-sight checks across dozens of agents is the case this exists for.
- ⚠️ Queries read the physics scene's state, not the transform's. After writing a transform, a
  query in the same frame sees the *old* position unless you call `Physics.SyncTransforms()`.

---

## Simulation control

- ℹ️ `Physics.autoSyncTransforms` is `false` by default. Leave it there — `true` re-syncs the
  physics scene after every transform write, which is a significant cost.
- ✅ Call `Physics.SyncTransforms()` explicitly in the rare case where you move a transform and must
  query against its new position before the next physics step.
- ✅ `Physics.simulationMode` defaults to `SimulationMode.FixedUpdate`. Set it to
  `SimulationMode.Script` and drive `Physics.Simulate(dt)` yourself only for deterministic ticks or
  netcode rollback.

---

## Unity 6 API changes

Renamed in Unity 6. The old names are obsolete, and they are what most training data contains.

| Old | Unity 6 |
|---|---|
| `Rigidbody.velocity` | `Rigidbody.linearVelocity` |
| `Rigidbody.drag` | `Rigidbody.linearDamping` |
| `Rigidbody.angularDrag` | `Rigidbody.angularDamping` |
| `Rigidbody2D.velocity` | `Rigidbody2D.linearVelocity` |
| `Rigidbody2D.drag` | `Rigidbody2D.linearDamping` |
| `Rigidbody2D.angularDrag` | `Rigidbody2D.angularDamping` |

- ⚠️ **`AddForceAtPosition` and `AddExplosionForce` changed behaviour.** Angular force is now scaled
  by the body's inertia tensor rather than its mass. Code ported from an earlier version that
  relied on the old scaling needs the force multiplied by `body.mass`, with `ForceMode.Acceleration`
  becoming `ForceMode.Force` and `ForceMode.VelocityChange` becoming `ForceMode.Impulse`.

---

## Troubleshooting

**`OnTriggerEnter` never fires.**
Neither object has a Rigidbody. Add a kinematic one to whichever object moves. Failing that:
`isTrigger` is off, the layer pair is disabled in the collision matrix, or the method signature
takes a `Collision` instead of a `Collider`.

**`OnCollisionEnter` never fires.**
Both objects are static or both are kinematic — see [What actually fires](#what-actually-fires).
Or one collider is a trigger, which suppresses collision messages entirely.

**A fast object passes through walls.**
Discrete collision detection. Set the projectile to `ContinuousDynamic` *and* the wall to
`Continuous`. If the fast body uses a MeshCollider, continuous detection doesn't apply to it at
all — swap to a primitive.

**The character stutters, but only at high frame rates.**
Rigidbody interpolation is `None`. Set it to `Interpolate` on the body the camera follows.

**Movement is frame-rate dependent.**
Forces applied in `Update` instead of `FixedUpdate`, or `Time.deltaTime` used inside
`FixedUpdate`.

**A raycast hits nothing immediately after moving the object.**
The physics scene hasn't been re-synced. Call `Physics.SyncTransforms()`, or restructure so the
query happens after the next physics step.

**A raycast always hits the object casting it.**
No layer mask, so it hits the caster's own collider at distance zero. Mask the caster's layer out.

**Physics goes slow-motion when the frame rate drops.**
Maximum Allowed Timestep is clamping the simulation — working as designed. The real problem is
frame time; profile it.

**Everything jitters when objects rest on each other.**
Contact stiffness against gravity. Raise Default Solver Iterations, or increase the mass ratio
tolerance — a 1000:1 mass ratio between touching bodies is unstable by nature.

**A ragdoll explodes on activation.**
Interpenetrating colliders at the moment of enabling. Ensure limbs don't overlap in the bind pose,
and disable collision between adjacent bones.

---

## Review checklist

| Check | Look for |
|---|---|
| Movement | `transform.position` assigned on a non-kinematic Rigidbody |
| Movement | `AddForce` or velocity writes in `Update` instead of `FixedUpdate` |
| Movement | `ForceMode` omitted from `AddForce` |
| Timing | `Time.deltaTime` used inside `FixedUpdate` |
| Timing | One-shot input read directly in `FixedUpdate` |
| Callbacks | Trigger volume where neither object has a Rigidbody |
| Callbacks | `OnTriggerEnter(Collision)` or `OnCollisionEnter(Collider)` — silently never called |
| Callbacks | Effect applied on both sides of a pair, so it happens twice |
| Callbacks | `other.tag == "X"` instead of `CompareTag` |
| Colliders | MeshCollider where a primitive or compound would do |
| Colliders | Convex MeshCollider over 255 triangles |
| Colliders | Non-convex MeshCollider on a non-kinematic Rigidbody |
| Tunnelling | Fast body left on `Discrete` |
| Tunnelling | Continuous set on only one side of the pair |
| Tunnelling | Continuous detection expected from a MeshCollider |
| Interpolation | `Interpolate` on every Rigidbody rather than the tracked ones |
| Queries | Raycast with no layer mask or no max distance |
| Queries | Query immediately after a transform write, with no `SyncTransforms` |
| Settings | Layer Collision Matrix left fully enabled |
| Unity 6 | `.velocity`, `.drag`, `.angularDrag` |

---

## Learn more

- [Physics, Unity manual](https://docs.unity3d.com/6000.3/Documentation/Manual/PhysicsSection.html)
- [Collider interactions](https://docs.unity3d.com/6000.3/Documentation/Manual/collider-interactions.html)
- [Rigidbody scripting reference](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/Rigidbody.html)
- [Collision detection mode](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/Rigidbody-collisionDetectionMode.html)
- [Mesh Collider component](https://docs.unity3d.com/6000.3/Documentation/Manual/class-MeshCollider.html)
