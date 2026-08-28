# Unity C# Style Guide & Naming

> **Opinionated.** These are my preferences. Fork them, change them, argue with them — a style guide
> only works if the team using it agrees with it. The general, non-negotiable best practices live in
> [`UnityReferenceGuides/`](UnityReferenceGuides/); project-specific settings live in
> [`UnityCustomInstructions/`](UnityCustomInstructions/).

Follow these guidelines for all Unity C# code. See the [readme](README.md) for the rationale behind
the choices.

## What's opinionated here

Most of this guide is standard C# and Unity practice. These specific calls are mine, and they're the
ones worth discussing before you adopt the guide wholesale:

| Convention | My choice | Common alternative |
|---|---|---|
| Private field prefix | `m_camelCase` | `_camelCase` or bare `camelCase` |
| Constant prefix | `k_camelCase` for private consts | `PascalCase` or `SCREAMING_CASE` |
| Static field prefix | `s_camelCase` | no prefix |
| Brace style | Allman (brace on its own line) | K&R (brace on the same line) |
| Line width | 120–140 characters | 80, 100, or unlimited |
| `private` modifier | Always written, even though it's implicit | Omitted |
| ScriptableObject naming | `DataSO` suffix | no suffix |
| Method verbs | `Handle` for event callbacks, `Process` for game-flow logic | `On`, or no distinction |

Everything else — PascalCase types and methods, `is`/`has`/`can` booleans, `I`-prefixed interfaces,
caching in `Awake`, unsubscribing in `OnDisable` — is standard practice, not preference.

> **Tech stack assumptions** (Unity version, render pipeline, input and UI system) live in
> [`UnityCustomInstructions/UnityTechStack.md`](UnityCustomInstructions/UnityTechStack.md).
> That is the first file to edit when you adopt this guide.

Table of contents:
- [General Guidelines](#general-guidelines)
  - [Formatting](#formatting)
    - [Spacing](#spacing)
    - [Use of regions](#use-of-regions)
  - [Comments](#comments)
- [Organize classes by the Unity Script Execution Order](#organize-classes-by-the-unity-script-execution-order)
  - [Using statements](#using-statements)
    - [Namespaces](#namespaces)
  - [Fields](#fields)
  - [Properties](#properties)
  - [Events](#events)
    - [Subscribing and unsubscribing to events](#subscribing-and-unsubscribing-to-events)
  - [MonoBehaviour methods](#monobehaviour-methods)
    - [Awake()](#awake)
    - [OnEnable()](#onenable)
    - [Start()](#start)
    - [OnDisable()](#ondisable)
    - [OnDestroy()](#ondestroy)
    - [FixedUpdate()](#fixedupdate)
    - [Update()](#update)
    - [LateUpdate()](#lateupdate)
    - [General notes](#general-notes)
  - [Public methods](#public-methods)
  - [Private methods](#private-methods)
  - [Other classes](#other-classes)
- [Methods](#methods)
- [General tips to cleaner Unity code](#general-tips-to-cleaner-unity-code)
  - [Interfaces](#interfaces)
  - [Naming files and folders](#naming-files-and-folders)
  - [Use enums for managing states](#use-enums-for-managing-states)
  - [Avoid nesting if statements](#avoid-nesting-if-statements)
  - [Managing string allocations](#managing-string-allocations)
  - [Collection type selection](#collection-type-selection)
  - [Async & Awaitable usage](#async--awaitable-usage)
  - [Scriptable Objects](#scriptable-objects)
  - [Animation parameters, layers, tags, sorting layers, and input action names](#animation-parameters-layers-tags-sorting-layers-and-input-action-names)
  - [Debugging](#debugging)
  - [Using try-catch & debugger breaks](#using-try-catch--debugger-breaks)
- [Where to go deeper](#where-to-go-deeper)

# General Guidelines

## Formatting

- ⚠️ Readability is key. Try to keep lines short. Consider horizontal whitespace.
- ✅ Use the Allman style (opening curly braces on a new line).
- ✅ Line width should be less than 120–140 characters.
- ✅ Break a long line into smaller statements rather than letting it overflow.
- ✅ Use a single space before flow control conditions, e.g., `while (x == y)`.
- ❌ Avoid spaces inside brackets, e.g., `x = dataArray[index]`.

### Spacing

- ✅ Use a single space after a comma between function arguments, e.g., `CollectItem(myObject, 0, 1);`.
- ❌ Don't add spaces just inside the parentheses before the first or after the last argument, e.g., `CollectItem( myObject, 0, 1 );`.
- ❌ Don't use spaces between a function name and parenthesis, e.g., `DropPowerUp(myPrefab, 0, 1);`.
- ✅ Use vertical spacing (extra blank line) for visual separation.
- ✅ Use one variable declaration per line in most cases. It's less compact but enhances readability.
- ✅ Use a single space before and after comparison operators, e.g., `if (x == y)`.

```csharp
// Good spacing example using Allman style braces
public void ProcessItems(List<Item> items, int startIndex)
{
    for (int i = startIndex; i < items.Count; i++)
    {
        ProcessItem(items[i]);
    }

    // Note vertical spacing here for visual separation
    Debug.Log("Processing complete");
}

// Avoid
public void ProcessItems ( List<Item>items,int startIndex ) { for(int i=startIndex;i<items.Count;i++) { ProcessItem( items [ i ] ); } Debug.Log("Processing complete"); }
```

### Use of regions
- ℹ️ Use `#region` sparingly as it can hide code and reduce readability. A class that needs regions to
  stay navigable is usually a class that should be split.
- ✅ Use `#region` to group Animation Event Handlers or Input Event Handlers, called from the animation
  system etc. so they are separated from the rest of the code.

```csharp
#region Animation Event Methods
// This method is called from animation events to signal landing
public void OnLand()
{
    Debug.Log("OnLand called from animation event");
}

// This method is called from animation events
public void OnFootstep()
{
    // This method can be used to play footstep sounds
    Debug.Log("Footstep event triggered");
}
#endregion
```

## Comments
- ✅ Comment intent ("why") rather than restating code ("what").
- ✅ Before writing a comment, check whether a clearer name would make it unnecessary. Good naming
  removes the need for most commentary.
- ✅ When the reasoning behind a decision isn't obvious from the code, write it down. Non-obvious
  context is exactly what a comment is for.
- ✅ Use `[Tooltip]`, `[Header]`, `[Space]`, etc. for serialized fields that need Inspector context.
  A `[Tooltip]` is more useful than a comment for anything a designer will touch.
- ✅ Use XML documentation comments (`///`) on public APIs so consumers get IntelliSense without
  reading the implementation.
- ❌ Avoid attribution comments like `// Created by…`. Version control is the authoritative source
  for authorship and history.

```csharp
// Good - explains why, not just what
// Skip processing if below threshold to avoid performance issues with small batches
if (itemCount < processingThreshold)
{
    return;
}

[Tooltip("Maximum distance the player can travel in one frame")]
[SerializeField] private float m_maxDeltaMovement = 10f;

/// <summary>
/// Applies damage and raises <see cref="HealthChanged"/> if the value actually changed.
/// </summary>
public void ApplyDamage(int amount) { }
```

# Organize classes by the Unity Script Execution Order
- ✅ Organize your class in the Unity script execution order:
  - [Using statements](#using-statements)
    - [Namespace](#namespaces)
  - [Fields](#fields)
  - [Properties](#properties)
  - [Events](#events)
  - [MonoBehaviour methods](#monobehaviour-methods)
    - [Awake()](#awake)
    - [OnEnable()](#onenable)
    - [Start()](#start)
    - [OnDisable()](#ondisable)
    - [OnDestroy()](#ondestroy)
    - [FixedUpdate()](#fixedupdate)
    - [Update()](#update)
    - [LateUpdate()](#lateupdate)
  - [Public methods](#public-methods)
  - [Private methods](#private-methods)
  - [Other classes](#other-classes)

## Using statements

- ✅ Keep using statements at the top of your file.
- ✅ Ordering `using` statements improves readability and ensures consistency across files. It also helps avoid conflicts when namespaces have overlapping class names.
- ✅ Start with system namespaces (e.g., `System`, `System.Collections`) at the top.
- ✅ Follow with Unity namespaces (e.g., `UnityEngine`).
- ✅ Add project-specific namespaces (e.g., `MyGameProject.Utilities`) last.
- ✅ Remove unused `using` statements to keep the file clean and avoid unnecessary dependencies.

```csharp
// System namespaces
using System;
using System.Collections;
using System.Collections.Generic;

// Unity namespaces
using UnityEngine;

// Project-specific namespaces
using MyGameProject.Utilities;
```

### Namespaces

- ✅ Use namespaces to ensure that your classes, interfaces, enums, etc., won't conflict with existing ones from other namespaces or the global namespace.
- ✅ Use PascalCase, without special symbols or underscores.
- ✅ Create sub-namespaces with the dot (`.`) operator, e.g., `MyApplication.GameFlow`, `MyApplication.AI`, etc.

```csharp
namespace MyGame.Characters
{
    public class Player : MonoBehaviour
    {
        // Class implementation
    }
}
```

## Fields
- ✅ Don't omit the `private` accessor even though it's technically implicit. It provides context about the intent.
- ✅ Use `m_` for private fields, `k_` for private constants, and `s_` for static fields. All three use
  **camelCase after the prefix** (`m_health`, `k_maxCount`, `s_sharedCount`).
- ⚠️ **Exception:** `public const` members of a static lookup class are API surface, so they use
  PascalCase without a prefix (see [Animation parameters](#animation-parameters-layers-tags-sorting-layers-and-input-action-names)).
  The `k_` prefix is for private constants.
- ✅ Use descriptive names that clearly indicate the field's purpose.
- ❌ Avoid abbreviations unless they are widely understood (e.g., `UI`, `ID`).
- ✅ Include units in the name if applicable (e.g., `m_speedInMetersPerSecond`).
- ✅ Prefix Boolean fields with verbs like `is`, `has`, or `can` for clarity (e.g., `m_isActive`, `m_hasPermission`).
- ❌ Avoid redundancy by not repeating the class name in field names (e.g., use `m_health` instead of `m_playerHealth` in a `Player` class).
- ✅ Expose fields in the Inspector with `[SerializeField]`, keeping the field itself private.
- ✅ Use properties when you need to access them from other classes.
- ❌ Avoid redundant initializers. Value types default to `0` and reference types to `null`; writing
  that out adds noise.

```csharp
// Use `m_` prefix for private fields
private int m_health;

// Static field with s_ prefix
private static int s_sharedCount;

// Private constant with k_ prefix
private const int k_maxCount = 100;

// Use [SerializeField] rather than exposing your field publicly; keep it private or make it a property
[SerializeField] private int m_startingHealth;

// Specify the unit used to eliminate guessing. Favor readability over brevity
private int m_elapsedTimeInHours;
private int m_elapsedTimeInDays;
private int m_elapsedTimeInSeconds;

// Prefix Booleans with a verb like "is" to make their meaning apparent
[SerializeField] private bool m_isPlayerDead;
```

### Properties
- ✅ Place properties after fields and before MonoBehaviour methods as per your class organization.
- ✅ Use PascalCase for properties and avoid prefixes/suffixes.
- ✅ Prefer predicate names for boolean properties (Is/Has/Can), e.g., `IsGrounded`, `HasHealthPack`, `CanJump`.
- ❌ Don't try to serialize a property directly. Use `[SerializeField] private T m_field` plus a public
  property that returns or validates it.
- ✅ Use `[field: SerializeField]` on an auto-property when you want the Inspector field without writing
  a backing field by hand. It's the concise option — note the Inspector label will show the compiler-
  generated backing field name.
- ✅ Use properties for accessing or modifying the state of an object. Properties are ideal for
  lightweight operations with no or minimal side effects. Example: `Health`, `Speed`, `IsGrounded`.
- ℹ️ Use methods for actions or operations, such as input handling and event-driven behavior. Name them
  appropriately: `ApplyDamage(int amount)` instead of `SetHealth(int amount)`.
- ❌ Avoid using properties for actions. Properties should not perform significant computations, trigger
  events, or have side effects.

```csharp
// Private backing field
private int m_maxHealth;

// Read-only property
public int MaxHealthReadOnly => m_maxHealth;

// Property with full implementation
public int MaxHealth
{
    get => m_maxHealth;
    set => m_maxHealth = value;
}

// Auto-implemented property
public string DescriptionName { get; set; } = "Fireball";

// Serialized auto-property - Inspector-editable without a hand-written backing field
[field: SerializeField] public float MoveSpeed { get; private set; } = 5f;

// Avoid: Using a property for an action like SetMovementInput to handle input events.
public Vector2 MovementInput
{
    set
    {
        m_forwardMovementInput = value;
        Debug.Log("Movement input set.");
    }
}
```

### Events
- ✅ Use `event Action` or `event Action<T>` for declaring events for the majority of cases.
- ✅ Use `UnityEvent` only when you need to expose callbacks to the Inspector. I generally avoid
  `UnityEvent` for code-only events as `Action` is more lightweight and flexible.
- ✅ Follow the C# event naming convention: use past tense verbs (e.g., `DoorOpened`, not `OnDoorOpen`).
- ✅ Use the `On` prefix for methods that raise events (e.g., `OnDoorOpened`), and use past-tense verbs
  for the event name itself (e.g., `DoorOpened`).
- ✅ Make the raiser `protected virtual` when the class may be subclassed, so derived types can extend
  rather than replace the behaviour. Use `private` when it won't be.
- ✅ Use the observer pattern to decouple systems and reduce dependencies (e.g., firing events for UI to update instead of direct references to UI components).
- ✅ Use the null-conditional operator (`?.`) when raising events to avoid null reference exceptions.
- ✅ Use a custom event-argument type for events that carry multiple values. A readonly `struct` avoids
  the allocation that a class-based `EventArgs` would incur — worth it for anything raised frequently.
- ⚠️ Avoid overusing events for tightly coupled systems where direct method calls would be simpler.
    - ✅ *Use Events*: When you need to decouple systems that don't need to know about each other directly (e.g., broadcasting game state changes to multiple systems). For example, when a GameManager needs to notify multiple unrelated systems (e.g., UI, Audio, Analytics) about a game state change.
    - ❌ *Avoid Events*: When the systems are tightly coupled, and a direct method call or dependency injection is simpler and more efficient. For example, when a PlayerController directly controls a Weapon.

```csharp
// Event declarations
public event Action DoorOpened;         // Use past tense verbs for event names
public event Action<int> PointsScored;
public event Action<DamageInfo> DamageTaken;

// Event raising methods
protected virtual void OnDoorOpened()
{
    // Use the null-conditional operator to avoid null reference exceptions
    DoorOpened?.Invoke();
}

// When passing data with events
protected virtual void OnPointsScored(int points)
{
    PointsScored?.Invoke(points);
}

// Readonly struct for complex event data - no allocation per raise
public readonly struct DamageInfo
{
    public int SourceId { get; }
    public float Amount { get; }

    public DamageInfo(int sourceId, float amount)
    {
        SourceId = sourceId;
        Amount = amount;
    }
}
```

#### Subscribing and unsubscribing to events
- ✅ Subscribe in `OnEnable` and always unsubscribe in `OnDisable` to prevent memory leaks.
- ✅ Avoid using lambda expressions when subscribing to events as it makes unsubscribing impossible unless you store the lambda in a variable first.
- ⚠️ Be cautious when subscribing long-lived objects (e.g., singletons) to events from short-lived objects to avoid memory leaks.

```csharp
private void OnEnable()
{
    m_gameManager.DoorOpened += HandleDoorOpened;
}

private void OnDisable()
{
    m_gameManager.DoorOpened -= HandleDoorOpened;
}
```

## MonoBehaviour methods

### Awake()
- ✅ Use Awake for initializing references between components and from different GameObjects.
- ✅ Cache component references (`GetComponent`, pool creation).
- ✅ Initialize internal state that does not depend on other GameObjects.
- ✅ Avoid heavy work, scene-dependent calls or subscribing to external events here.

```csharp
private void Awake()
{
    // Cache component references here
    m_rigidbody = GetComponent<Rigidbody>();
}
```

### OnEnable()
- ✅ Subscribe to events, register input callbacks, reset per-enable state.
- ✅ Keep work small and reversible. Unsubscribe in `OnDisable()`.

```csharp
private void OnEnable()
{
    // Subscribe here; the matching -= belongs in OnDisable()
    m_inputActions.Player.Jump.performed += HandleJumpPerformed;
    m_health.Died += HandleDied;
}
```

### Start()
- ✅ Use Start to call initialization methods that require other components to exist and be ready.
- ✅ Perform initialization that requires other components or scene objects to exist.
- ✅ Use for one-time setup (animations, UI wiring) that must run after all `Awake()`/`OnEnable()`.

```csharp
private void Start()
{
    // Use cached references and perform operations that might depend on other components being initialized
    m_animator.SetTrigger(k_initializeTrigger);
}
```

### OnDisable()
- ✅ Use OnDisable for unsubscribing from events and cleaning up state when the object is disabled.
- ✅ Mirror `OnEnable()` exactly. Every `+=` there needs its `-=` here.

```csharp
private void OnDisable()
{
    // Unsubscribe from events here to prevent memory leaks or unexpected behavior
    m_inputActions.Player.Jump.performed -= HandleJumpPerformed;
    m_health.Died -= HandleDied;
}
```

### OnDestroy()
- ✅ Use OnDestroy for teardown that must happen once, permanently — releasing native resources,
  disposing handles, unregistering from a service locator.
- ⚠️ `OnDestroy` runs after `OnDisable`, so event unsubscription belongs in `OnDisable`, not here.
  Anything you do in both will run twice.
- ⚠️ `OnDestroy` is not called if the GameObject was never enabled, and ordering between objects during
  scene teardown is not guaranteed. Don't rely on another object still being alive.
- ✅ Release anything that isn't garbage-collected: `NativeArray`, `RenderTexture`, `Addressables`
  handles, `IDisposable` fields.

```csharp
private void OnDestroy()
{
    // Release resources the GC won't clean up for you
    m_inputActions?.Dispose();

    if (m_renderTexture != null)
    {
        m_renderTexture.Release();
    }

    ServiceLocator.Unregister(this);
}
```

### FixedUpdate()
- ⚠️ FixedUpdate runs on the fixed physics timestep and may run zero, one, or many times between Update calls depending on frame time.
- ✅ Use FixedUpdate for physics-related updates (e.g., applying forces, physics calculations).
- ✅ Put deterministic physics work here: `AddForce`, rigidbody velocity, simulation steps.
- ✅ Do not read input here; read input in `Update()` and apply it in `FixedUpdate()` if needed.
- ✅ Keep it allocation-free and lightweight.

```csharp
// Use FixedUpdate for physics
private void FixedUpdate()
{
    HandlePhysicsMovement();
}
```

### Update()
- ✅ Use Update for regular frame updates (e.g., input handling, non-physics calculations).
- ✅ Read input, update timers, run non-physics per-frame logic and state machines.
- ✅ Avoid allocations, use early returns and delegate to well-named helper methods.
- ❌ Never create new collections in `Update()`. Reuse existing ones and call `.Clear()`.
- ❌ Never call `GetComponent`, `Find*`, or `Camera.main` here. Cache them in `Awake()`.
- ✅ Instead of having logic directly in the Update loop, move it to methods with descriptive names to improve cleanliness and self-documentation.

```csharp
private void Update()
{
    // Put all your regular frame logic update code in Update()

    if (!m_isActive) return; // Early return pattern

    // Move logic to well-named methods
    HandleMovement();
    UpdateAnimations();
    CheckPlayerInput();
}
```

### LateUpdate()
- ✅ Finalize transforms, camera follow, animation-driven adjustments and cleanup after `Update()`.
- ✅ Use for logic that must run after all `Update()` work — anything that reads a value another script
  writes during `Update()`.

```csharp
// Use LateUpdate for camera follow so it reads the player's final position for this frame
private void LateUpdate()
{
    Vector3 targetPosition = m_target.position + m_followOffset;
    transform.position = Vector3.SmoothDamp(transform.position, targetPosition, ref m_followVelocity, m_smoothTime);
    transform.LookAt(m_target);
}
```

### General notes
- ✅ Keep related methods together for better readability.
- ✅ Keep MonoBehaviours focused on a single responsibility.
- ✅ Use `[RequireComponent(typeof(OtherComponent))]` when dependencies exist. It ensures the required component is always present so we don't need to check for null references later.
- ✅ Cache expensive operations outside of Update loops to prevent repeated allocations.
- ❌ Avoid magic numbers and strings. Replace hardcoded values (e.g., `5f` for speed) with constants or serialized fields for better flexibility and readability.

```csharp
// Avoid - expensive operations in Update
private void Update()
{
    // Bad - expensive operation every frame
    var nearbyEnemies = Physics.OverlapSphere(transform.position, m_detectionRadius);

    // Better - cache and update less frequently
    if (Time.time > m_nextUpdateTime)
    {
        UpdateNearbyEnemies();
        m_nextUpdateTime = Time.time + m_updateInterval;
    }
}
```

## Public methods
- ✅ Place public methods after the MonoBehaviour lifecycle methods. They are the class's API, so they
  come before the private helpers that support them.
- ✅ Order them by relatedness, not alphabetically. A reader should be able to follow one feature down
  the file rather than jumping around.
- ✅ Document non-obvious behaviour with XML comments (`///`) — this is the surface other scripts see.
- ✅ Validate arguments at the boundary. A public method is where bad input arrives.

```csharp
/// <summary>Applies damage and raises DamageTaken. Ignores non-positive amounts.</summary>
public void ApplyDamage(int amount)
{
    if (amount <= 0) return;

    m_health = Mathf.Max(0, m_health - amount);
    OnDamageTaken(amount);

    if (m_health == 0)
    {
        HandleDeath();
    }
}

public bool CanAfford(int cost) => m_currency >= cost;
```

## Private methods
- ✅ Place private methods after public methods, at the bottom of the behaviour.
- ✅ Keep the `Handle*` event callbacks grouped together so the reactive surface of the class is easy
  to find.
- ✅ Private helpers exist to make the public methods readable. If a private method is long enough to
  need its own helpers, that's a sign the class is doing too much.
- ❌ Don't leave `throw new NotImplementedException()` in generated stubs. Leave the body empty or add
  a comment noting the work is pending.

```csharp
// Event callbacks grouped together
private void HandleDied()
{
    m_animator.SetTrigger(k_deathTrigger);
}

private void HandleJumpPerformed(InputAction.CallbackContext context)
{
    Jump();
}

// Supporting helpers
private void HandleDeath()
{
    enabled = false;
    m_collider.enabled = false;
}
```

## Other classes
- ✅ Small helper types used only by this file — a state class, a config struct, a private enum — can
  live at the bottom of the same file. Keeping them nearby beats scattering one-line files.
- ✅ Anything used by more than one file gets its own file, named after the type.
- ✅ Nested types are fine when the type is meaningless outside its parent, e.g., `Inventory.Slot`.
- ⚠️ Unity only auto-creates a component from a file whose name matches the MonoBehaviour inside it.
  A second MonoBehaviour in the same file will compile, but you can't add it via `Add Component`.
  Keep one MonoBehaviour per file.

```csharp
public class Inventory : MonoBehaviour
{
    [SerializeField] private List<Slot> m_slots = new();

    // Nested - meaningless outside Inventory
    [Serializable]
    public struct Slot
    {
        public ItemDataSO Item;
        public int Count;
    }
}

// Small helper enum used only by this file
internal enum SortOrder
{
    Newest,
    Rarity,
    Name
}
```

# Methods
- ✅ Use methods for behavior and event callbacks (actions, side effects, or inputs). Examples: `Jump()`, `TakeDamage(int amount)`, `SetMovementInput(Vector2 input)`. Unity's PlayerInput and Inspector events call methods, not properties, so prefer methods for input handlers.
- ✅ Name methods with descriptive verbs to state the action clearly (e.g., `ApplyDamage`, `PlaySound`, `RotateTurret`, `SetPosition`, `CalculateDamage`).
- ✅ Use clear prefixes: `SetX` for assigning/updating a value (e.g., `SetMovementInput(Vector2 input)`), `ChangeX` for modifying or transforming state (e.g., `ChangeHealth(int amount)`).
- ✅ **Use "Handle" for event-driven callbacks** — responding to external input or events. Examples:
  `HandleTargetSelected()`, `HandleTurnEnded()`, `HandleJumpPerformed()`. These are invoked by the
  event system in response to external triggers.
- ✅ **Use "Process" for game logic operations** — turn-based, scheduled, or system-driven work that is
  part of game flow. Examples: `ProcessTurnIncome()`, `ProcessModifierDecay()`. These are distinct
  from event handlers: you call them, the event system doesn't.
- ✅ Boolean methods should pose a question and return bool, using Is, Has, or Can (e.g., `IsPlayerAlive()`).
- ❌ Avoid noun-style method names except for factory methods or event handlers; avoid gerund/continuous names like `Walking()` or `Rotating()` (those indicate state — use `isWalking` / `isRotating` as variables or properties instead).
- ⚠️ Terminology: prefer the term "method" in C# (a function that is part of a class).

```csharp
// Action: performs behavior / side effects
public void Jump()
{
    m_rigidbody.AddForce(Vector3.up * m_jumpForce, ForceMode.Impulse);
}

// Setter: clearly assigns or updates a value (suitable for input callbacks)
public void SetMovementInput(Vector2 input)
{
    m_forwardMovementInput = input;
}

// Modifier: transforms or changes state
public void ChangeHealth(int amount)
{
    m_health += amount;
}

// "Handle" for event-driven callbacks (responding to external events/input)
private void HandleTargetSelected(Targetable target)
{
    ChangeState(CombatState.Aiming);
}

// "Process" for game logic operations (part of game flow, usually turn-based or system-driven)
private void ProcessTurnIncome()
{
    foreach (Settlement settlement in m_settlements)
    {
        m_resources.AddGold(settlement.GoldPerTurn);
    }
}

// Boolean methods asking questions
public bool IsNewPosition(Vector3 newPosition)
{
    return transform.position == newPosition;
}

// Good examples - each indicates an action being performed
// SetInitialPosition(float x, float y, float z)
// SaveGame()
// IsPlayerAlive()
// CreatePlayer()
// Walk()

// Avoid 'ing as that implies a continuous state or property rather than an action
// Walking()   ❌
```

# General tips to cleaner Unity code

## Interfaces
- ✅ Use interfaces to define clear "contracts" and decouple systems.
- ✅ Use the single responsibility rule per interface (Interface Segregation). Small, focused interfaces are better than large monoliths.
- ✅ Use the `I` prefix and PascalCase (e.g., `IDamageable`, `IAudioService`).
- ✅ Name methods with verbs and boolean members with Is/Has/Can.
- ✅ Use an interface for a pure contract with no shared implementation, and an abstract base class when multiple implementations share behaviour or state.

```csharp
public interface IDamageable
{
    float CurrentHealth { get; }
    bool IsAlive { get; }

    void ApplyDamage(int amount);
}

public interface IDamageable<T>
{
    void Damage(T damageTaken);
}
```

## Naming files and folders
- ✅ Use PascalCase for all file and folder names to maintain consistency with class and script naming conventions (e.g., `CharacterController.cs`, `AnimationController.cs`, `CoreSystems/`, `UI/`).
- ✅ Organize scripts into folders based on functionality or feature areas (e.g., `CoreSystems/`, `UI/`).
- ✅ Don't worry about long folder paths if they improve organization and clarity. That only helps future maintainers and your coding assistant.
- ❌ Avoid spaces and special characters in file and folder names to prevent issues with version control systems and cross-platform compatibility.
- ℹ️ If you have a very long folder name with variations you can consider using `_` to separate words. Example: `InputSystemActions_PlayerInputComponent_UnityEvents`, `InputSystemActions_PlayerInputComponent_CSharpEvents`, etc.
- ❌ Don't use `NotImplementedException` when stubbing out new methods or event handlers. It adds unnecessary noise and makes it harder to read the code. Instead, leave the method body empty or add a comment indicating that the implementation is pending.

```csharp
private void LookInputReceived(InputAction.CallbackContext context)
{
    // Don't: when your assistant helps create new methods, leave out the NotImplementedException
    throw new NotImplementedException();
}
```

## Use enums for managing states
- ✅ Use enums for mutually exclusive states (e.g., animation, movement, UI, or game phases).
- ✅ Use enums in switch statements for clear, maintainable logic.
- ❌ Avoid using strings or integers directly for state tracking.
- ✅ Use enums when an object or action can only have one value at a time.
- ✅ Use PascalCase for enum names and values.
- ✅ Use a singular noun for the enum name as it represents a single value from a set of possible values.
- ❌ Avoid prefixes or suffixes (e.g., don't add `Enum`, `Type`, or `E_`).
- ✅ Public enums can be declared outside of a class if they need to be accessed globally.

```csharp
// Simple enum
public enum Direction
{
    North,
    South,
    East,
    West
}

private Direction m_currentDirection;

private void Update()
{
    switch (m_currentDirection)
    {
        case Direction.North:
            // Move north
            break;
        case Direction.South:
            // Move south
            break;
        case Direction.East:
            // Move east
            break;
        case Direction.West:
            // Move west
            break;
    }
}

// Flag enum
[Flags]
public enum AttackModes
{
    // Decimal                         // Binary
    None = 0,                          // 000000
    Melee = 1,                         // 000001
    Ranged = 2,                        // 000010
    Special = 4,                       // 000100

    MeleeAndSpecial = Melee | Special  // 000101
}
```

## Avoid nesting if statements
- ✅ Simplify the structure of your if statements by avoiding nesting. Use early returns — often called
  a guard clause — so the happy path stays at the left margin.

```csharp
// Avoid nesting
if (conditionA)
{
    if (conditionB)
    {
        ExecuteAction();
    }
}

// Better - guard clauses, same behaviour
if (!conditionA) return;
if (!conditionB) return;

ExecuteAction();
```

## Managing string allocations
- ✅ Use string interpolation (`$""`) instead of concatenation (`+`) for **readability**. Both allocate,
  so this is a clarity choice, not a performance one.
- ⚠️ In hot paths — `Update`, `FixedUpdate`, tight loops — every string you build is garbage. Cache the
  result and only rebuild when the underlying value actually changes.
- ✅ Use `StringBuilder` when assembling a string from many parts.
- ℹ️ See [Performance: String Operations](UnityReferenceGuides/UnityPerformanceOptimizationInstructions.md#string-operations)
  for the zero-allocation techniques.

```csharp
public class ScoreDisplay : MonoBehaviour
{
    [SerializeField] private TMP_Text m_scoreText;
    private int m_lastScore = -1;

    // Bad - readable, but allocates a new string every single frame
    private void Update()
    {
        m_scoreText.text = $"Score: {m_score}";
    }

    // Good - only allocates when the score actually changes
    private void Update()
    {
        if (m_score == m_lastScore) return;

        m_lastScore = m_score;
        m_scoreText.text = $"Score: {m_score}";
    }
}
```

## Collection type selection
- ✅ Use `List<T>` when the collection size changes dynamically or frequent additions/removals are needed.
- ✅ Use arrays when the size is fixed and performance matters (e.g., tight update loops).
- ✅ Use `Stack<T>` for Last-In-First-Out (LIFO) logic such as undo systems, state history, or command buffers.
- ✅ Use `Dictionary<TKey, TValue>` when you need fast lookups by key.
- ❌ Avoid allocations inside loops — reuse existing collections and call `.Clear()` instead of creating new instances.
- ✅ Initialize collections with a reasonable capacity when possible (e.g., `new List<T>(capacity)`) to reduce resizing overhead.
- ✅ Favor `foreach` loops when iterating read-only collections, as they improve readability and reduce indexing errors.

```csharp
// List<T>: dynamic size, frequent add/remove
public class EnemyRegistry : MonoBehaviour
{
    // Target-typed new expression (C# 9.0+)
    [SerializeField] private List<GameObject> m_enemies = new();

    public void Register(GameObject enemy)
    {
        if (!m_enemies.Contains(enemy))
        {
            m_enemies.Add(enemy);
        }
    }

    public void Unregister(GameObject enemy)
    {
        m_enemies.Remove(enemy);
    }
}
```

## Async & Awaitable usage
- ✅ Use the `Awaitable` API (Unity 6 and later) with async/await for timed delays, sequencing, or
  asynchronous workflows that don't require per-frame iteration. This is cleaner and more readable
  than coroutines.
- ✅ Name async methods with the `Async` suffix (e.g., `OpenDoorAsync`) and coroutines with the `Co`
  suffix (e.g., `LoadAssetsCo`) to clearly distinguish them.
- ✅ Use PascalCase and verb-based names for both async and coroutine methods.
- ❌ Do not mix `Awaitable` and coroutines within the same operation — choose one approach per workflow.
- ✅ Take a `CancellationToken` and guard continuations. After an `await`, the object may have been
  destroyed: `if (this == null || !isActiveAndEnabled) return;`
- ⚠️ Avoid `async void`. It can't be awaited and swallows exceptions. `async Awaitable` is awaitable and
  is valid as a Unity message signature, so use it even for `Start`.
- ⚠️ Cache `WaitForSeconds` in coroutines — allocating one per loop iteration is a classic leak.

```csharp
public async Awaitable OpenDoorAsync(CancellationToken token)
{
    Debug.Log("Door opening...");

    await Awaitable.WaitForSecondsAsync(2f, token);

    // The object may have been destroyed while we were waiting
    if (this == null || !isActiveAndEnabled) return;

    Debug.Log("Door opened!");
}

private IEnumerator LoadAssetsCo()
{
    // Cache the wait - don't allocate one per iteration
    var wait = new WaitForSeconds(0.5f);

    for (int i = 0; i < 5; i++)
    {
        Debug.Log($"Loading asset {i + 1}/5...");
        yield return wait;
    }

    Debug.Log("All assets loaded!");
}

// async Awaitable, not async void - exceptions surface and it can be awaited
private async Awaitable Start()
{
    await OpenDoorAsync(destroyCancellationToken);
}
```

## Scriptable Objects
- ✅ Favor ScriptableObjects for static configuration data and reusable content that stays the same while the game runs (e.g., weapons, enemy stats, skill effects).
- ❌ Don't use ScriptableObjects to store data that changes during gameplay (like player health, score, or runtime state). Edits made in the Editor persist between play sessions and will surprise you.
- ✅ Use ScriptableObjects to reduce coupling between systems — feed configuration into MonoBehaviours instead of having them fetch data manually.
- ✅ Always mark ScriptableObjects with `[CreateAssetMenu]` for easy asset creation via the Project window.
- ✅ Append a `DataSO` suffix (e.g., `WeaponDataSO`) to make ScriptableObjects easily identifiable. *(Opinionated — plenty of teams use no suffix at all.)*
- ✅ Store ScriptableObject assets in a dedicated folder structure (e.g., `Assets/Data/Weapons/`).
- ✅ Keep ScriptableObjects focused on a single responsibility to enhance reusability and maintainability.
- ✅ Keep data and logic separate: ScriptableObjects should primarily hold data. Only add logic that directly relates to the data.
- ✅ Use properties to expose data from ScriptableObjects instead of public fields for better encapsulation.

```csharp
// WeaponDataSO stores weapon configuration
[CreateAssetMenu(fileName = "WeaponData", menuName = "Game Data/Weapon", order = 0)]
public class WeaponDataSO : ScriptableObject
{
    [SerializeField] private string m_weaponName;
    [SerializeField] private int m_damage;
    [SerializeField] private float m_range;
    [SerializeField] private GameObject m_projectilePrefab;

    public string WeaponName => m_weaponName;
    public int Damage => m_damage;
    public float Range => m_range;
    public GameObject ProjectilePrefab => m_projectilePrefab;
}
```

## Animation parameters, layers, tags, sorting layers, and input action names
- ✅ **PascalCase** is recommended for all text-based references such as animation parameters, layers, tags, sorting layers, and input action names. This aligns with Unity conventions and this guide's property naming.
- ✅ Prefix boolean animation parameters and similar flags with **Is**, **Has**, or **Can** (e.g., `IsRunning` rather than `Running`).
- ✅ Use descriptive names that clearly indicate the purpose or state.
- ✅ Always define these names as constants in code to prevent runtime errors, enable refactoring, and avoid typos.
- ✅ Centralize these constants in a dedicated static class for maintainability and discoverability.
- ℹ️ **Naming note:** `public const` members of a static lookup class are API surface, so they use
  PascalCase with no prefix. The `k_` prefix is for private constants inside a behaviour.
- ✅ **For animators, go one step further and hash the parameter names.** `Animator.StringToHash` converts
  the string once at startup; every `SetBool`/`SetFloat`/`SetTrigger` after that skips the string lookup
  entirely. Store the hashes in `static readonly int` fields.
- ⚠️ Layers are integers, not strings. Use `LayerMask.NameToLayer` / `LayerMask.GetMask` once and cache
  the result rather than passing layer names around as strings.

```csharp
// Centralized constants - public const on a static class, so PascalCase
public static class Tags
{
    public const string Collectible = "Collectible";
    public const string Hazard = "Hazard";
}

public static class InputActions
{
    public const string Jump = "Jump";
    public const string Fire = "Fire";
}

// Layers resolve to ints - cache the mask, don't pass strings around
public static class Layers
{
    public static readonly int Player = LayerMask.NameToLayer("Player");
    public static readonly int EnemyMask = LayerMask.GetMask("Enemy");
}

// Animator parameters - hash once, use the int forever after
public class PlayerAnimator : MonoBehaviour
{
    private static readonly int s_isRunningHash = Animator.StringToHash("IsRunning");
    private static readonly int s_speedHash = Animator.StringToHash("Speed");
    private static readonly int s_jumpTriggerHash = Animator.StringToHash("JumpTrigger");

    private Animator m_animator;

    private void Awake()
    {
        m_animator = GetComponent<Animator>();
    }

    private void UpdateMovement(bool isMoving, float currentSpeed)
    {
        // Safe and fast - no string comparison at runtime
        m_animator.SetBool(s_isRunningHash, isMoving);
        m_animator.SetFloat(s_speedHash, currentSpeed);
    }
}

// Bad - magic strings scattered throughout code (runtime errors possible)
private void UpdateMovementBadly(bool isMoving, float currentSpeed)
{
    m_animator.SetBool("IsWalking", isMoving);        // Typo risk
    m_animator.SetFloat("Spead", currentSpeed);       // Typo - fails silently!

    if (m_animator.GetBool("IsWalknig"))              // Another typo
    {
        // This condition will never be true due to the typo
    }
}
```

## Debugging
- ✅ Log strategically. Avoid excessive logging, especially in production builds.
- ✅ Use conditional compilation (`#if UNITY_EDITOR`) or a custom logging wrapper to strip logs in release builds.
- ✅ Always include context in log messages and pass the object as the second parameter so clicking the
  log selects it in the Hierarchy.
- ✅ Use `Debug.DrawLine`, `Debug.DrawRay`, and `Gizmos` for visual debugging in the Editor.
- ⚠️ Avoid logging inside tight loops or performance-critical sections.
- ℹ️ Prefer `[RequireComponent]` over defensive null checks — it makes the dependency an edit-time
  guarantee instead of a runtime question.
- ℹ️ For the full diagnostic workflow — triage order, stack trace interpretation, Input System and
  physics debugging — see [UnityDebuggingInstructions.md](UnityReferenceGuides/UnityDebuggingInstructions.md).

```csharp
// Include context so clicking the log selects the object
Debug.Log("Player has entered the trigger zone.", gameObject);

// Consistent, searchable error format
Debug.LogError($"[{GetType().Name}] Failed to load data: {exception.Message}", this);

// Gizmos for editor visualization
private void OnDrawGizmosSelected()
{
    Gizmos.color = Color.green;
    Gizmos.DrawWireSphere(transform.position, m_detectionRadius);
}

// Use [RequireComponent] instead of null-checking a hard dependency
[RequireComponent(typeof(AudioSource))]
public class AudioPlayer : MonoBehaviour
{
    private AudioSource m_audioSource;

    private void Awake()
    {
        m_audioSource = GetComponent<AudioSource>();
    }
}
```

## Using try-catch & debugger breaks
- ✅ Use try-catch for external dependencies — file I/O, network requests, platform services — where failures are outside your control. These are genuinely exceptional cases.
- ❌ Avoid try-catch for internal logic or expected conditions (e.g., null checks, invalid input). Validate inputs and use control flow instead.
- ✅ Always log the exception details to help with debugging.
- ✅ For critical external failures, consider rethrowing or escalating to a higher-level handler if the system cannot recover gracefully.

```csharp
public void SaveGame(GameData data)
{
    try
    {
        string json = JsonUtility.ToJson(data);
        File.WriteAllText(k_saveFilePath, json);
    }
    catch (IOException ioEx)
    {
        Debug.LogError($"[{GetType().Name}] IO error saving game: {ioEx}", this);
        ShowSaveErrorToPlayer();
    }
    catch (UnauthorizedAccessException uaEx)
    {
        Debug.LogError($"[{GetType().Name}] Access denied saving game: {uaEx}", this);
        ShowSaveErrorToPlayer();
    }
    catch (Exception ex)
    {
        Debug.LogError($"[{GetType().Name}] Unexpected error: {ex}", this);

#if UNITY_EDITOR
        Debug.Break();
#endif

        ShowSaveErrorToPlayer();
    }
}
```

# Where to go deeper

This guide covers style and naming. The general best-practice guides go into depth on everything else:

| Topic | Guide |
|---|---|
| SOLID, patterns, object pooling, state machines | [UnityDesignPatternsInstructions.md](UnityReferenceGuides/UnityDesignPatternsInstructions.md) |
| Hot paths, allocations, profiling, rendering cost | [UnityPerformanceOptimizationInstructions.md](UnityReferenceGuides/UnityPerformanceOptimizationInstructions.md) |
| UXML, USS, BEM, flexbox, runtime binding | [UnityUIToolkitInstructions.md](UnityReferenceGuides/UnityUIToolkitInstructions.md) |
| Canvas structure, layout rebuilds, uGUI pitfalls | [UnityUGUIInstructions.md](UnityReferenceGuides/UnityUGUIInstructions.md) |
| Addressables, import settings, memory budgets | [UnityAssetsAndMemoryInstructions.md](UnityReferenceGuides/UnityAssetsAndMemoryInstructions.md) |
| Bootstrapping, additive scenes, domain reload | [UnityScenesAndLifecycleInstructions.md](UnityReferenceGuides/UnityScenesAndLifecycleInstructions.md) |
| Edit Mode vs Play Mode tests, test assemblies | [UnityTestingInstructions.md](UnityReferenceGuides/UnityTestingInstructions.md) |
| Custom inspectors, property drawers, Gizmos | [UnityEditorToolingInstructions.md](UnityReferenceGuides/UnityEditorToolingInstructions.md) |
| Input System actions, phases, rebinding | [UnityInputSystemInstructions.md](UnityReferenceGuides/UnityInputSystemInstructions.md) |
| Animator parameters, blend trees, events | [UnityAnimationInstructions.md](UnityReferenceGuides/UnityAnimationInstructions.md) |
| Mixers, AudioSource pooling, spatial audio | [UnityAudioInstructions.md](UnityReferenceGuides/UnityAudioInstructions.md) |
| Assembly definitions and dependency boundaries | [UnityAssemblyDefinitionsInstructions.md](UnityReferenceGuides/UnityAssemblyDefinitionsInstructions.md) |
| Triage, stack traces, Input System & physics debugging | [UnityDebuggingInstructions.md](UnityReferenceGuides/UnityDebuggingInstructions.md) |
