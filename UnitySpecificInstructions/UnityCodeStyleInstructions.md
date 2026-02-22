
# GitHub Copilot Instructions: Unity C# Style Guide & Naming

Use this cheat sheet for LLM completions. See the readme.md for the general rationale behind these guidelines.

Table of contents:
- [Unity Version-Specific Instructions](#unity-version-specific-instructions)
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
    - [Awake\(\)](#awake)
    - [OnEnable\(\)](#onenable)
    - [Start\(\)](#start)
    - [OnDisable\(\)](#ondisable)
    - [OnDestroy](#ondestroy)
    - [FixedUpdate\(\)](#fixedupdate)
    - [Update\(\)](#update)
    - [LateUpdate\(\)](#lateupdate)
    - [General notes](#general-notes)
  - [Public methods](#public-methods)
  - [Private methods](#private-methods)
  - [Other classes](#other-classes)
- [Methods](#methods)
- [General tips to cleaner Unity code](#general-tips-to-cleaner-unity-code)
  - [Interfaces](#interfaces)
  - [Naming files and folders](#naming-files-and-folders)
  - [Enums](#use-enums-for-managing-states)
  - [Avoid nesting if statements](#avoid-nesting-if-statements)
  - [Managing String Allocations](#managing-string-allocations)
  - [Collection Type Selection](#collection-type-selection)
  - [Async \& Awaitable Usage](#async--awaitable-usage)
  - [Scriptable Objects](#scriptable-objects)
  - [Animation Parameters, Layers, Tags, Sorting Layers, and Input Action Names](#animation-parameters-layers-tags-sorting-layers-and-input-action-names)
  - [Debugging](#debugging)
  - [Using Try-Catch \& Debugger Breaks](#using-try-catch--debugger-breaks)
  - [Design Patterns for Unity](#design-patterns-for-unity)
    - [Implementing the State Pattern](#implementing-the-state-pattern)
    - [Object Pooling](#object-pooling)
- [UI Toolkit](#ui-toolkit)
  - [UI Toolkit File Naming \& Organization](#ui-toolkit-file-naming--organization)
  - [UXML](#uxml)
    - [BEM refresher](#bem-refresher)
    - [Examples](#examples)
    - [Querying from C\#](#querying-from-c)
  - [USS](#uss)
    - [Guidelines](#guidelines)
    - [Toggling classes from C\#](#toggling-classes-from-c)
  - [UI Toolkit Event Handling](#ui-toolkit-event-handling)

# Unity Version-Specific Instructions

- ℹ️ This project uses Unity 6.3. Make sure to use the latest sources and documentation that apply to Unity 6 or later versions.
- ℹ️ This project uses the newer "Input System" and not the older "Input Manager".
- ℹ️ This project uses the newer UI Toolkit and not the older UGUI for UI.
- ℹ️ This project uses the Universal Render Pipeline and not the old Built‑in Render Pipeline.
- ℹ️ Prefer Unity 6 Awaitables over coroutines for sequencing: `await Awaitable.WaitForSecondsAsync(delay, token);` Guard continuations with `if (this == null || !isActiveAndEnabled) return;`.
- ℹ️ When instantiating frequently, favor `UnityEngine.Pool.ObjectPool<T>` with `actionOnGet`/`actionOnRelease` to toggle active state.

# General Guidelines

## Formatting

- ⚠️ Readability is key. Try to keep lines short. Consider horizontal whitespace.
- ✅ Use the Allman style (opening curly braces on a new line).
- ✅ Define a standard max line width of less than 120–140 characters.
- ✅ Break a long line into smaller statements rather than letting it overflow.
- ✅ Use a single space before flow control conditions, e.g., `while (x == y)`.
- ❌ Avoid spaces inside brackets, e.g., `x = dataArray[index]`.

```csharp
// Good spacing example using Allman style braces and spacing
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

### Spacing

- ✅ Use a single space after a comma between function arguments, e.g., `CollectItem(myObject, 0, 1);`.
- ❌ Don't add spaces just inside the parentheses before the first or after the last argument, e.g., `CollectItem( myObject, 0, 1 );`.
- ❌ Don't use spaces between a function name and parenthesis, e.g., `DropPowerUp(myPrefab, 0, 1);`.
- ✅ Use vertical spacing (extra blank line) for visual separation.
- ✅ Use one variable declaration per line in most cases. It's less compact but enhances readability.
- ✅ Use a single space before and after comparison operators, e.g., `if (x == y)`.

```csharp
// Good spacing example
public void ProcessItems(List<Item> items, int startIndex)
{
    for (int i = startIndex; i < items.Count; i++)
    {
        ProcessItem(items[i]);
    }

    // Note vertical spacing here for visual separation
    Debug.Log("Processing complete");
}

// Bad spacing example
public void ProcessItems ( List<Item>items,int startIndex ) { for(int i=startIndex;i<items.Count;i++) { ProcessItem( items [ i ] ); } Debug.Log("Processing complete"); }
```
### Use of regions
- ℹ️ Use `#region` sparingly as it can hide code and reduce readability.
- ✅ Use `#region` to group Animation Event Handlers or Input Event Handlers, called from the animation system etc. so they are separated from the rest of the code.

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
- ✅ Add clarifying comments to most lines for documentation.
- ✅ Comment intent (“why”) rather than restating code (“what”).
- ✅ Use `[Tooltip]`, `[Header]`, `[Space]`, etc. for serialized fields that need Inspector context.

```csharp
// Good - explains why, not just what
// Skip processing if below threshold to avoid performance issues with small batches
if (itemCount < processingThreshold)
{
    return;
}

[Tooltip("Maximum distance the player can travel in one frame")]
[SerializeField] private float m_maxDeltaMovement = 10f;
```

# Organize classes by the Unity Script Execution Order
- ✅ Organize your class in the Unity script execution order:
  - [Using statements](#using-statements)
    - [Namespace](#namespaces)
  - [Fields](#fields)
  - [Properties](#properties)
  - [Events](#events)
  - [MonoBehaviour methods](#monobehaviour-methods)
    - [Awake\(\)](#awake)
    - [OnEnable\(\)](#onenable)
    - [Start\(\)](#start)
    - [OnDisable\(\)](#ondisable)
    - [OnDestroy](#ondestroy)
    - [FixedUpdate\(\)](#fixedupdate)
    - [Update\(\)](#update)
    - [LateUpdate\(\)](#lateupdate)
  - Public methods
  - Private methods
  - Other classes

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
- ✅ Don't omit the private accessor field though technically its implicit. It provides context about the intent.
- ✅ Use `m_` prefix for private variables, `k_` for constants
- ✅ Use `m_` prefix for private fields to distinguish them from local variables.
- ✅ Use `k_` prefix for constants to indicate immutability.
- ✅ Use descriptive names that clearly indicate the field's purpose.
- ❌ Avoid abbreviations unless they are widely understood (e.g., `UI`, `ID`).
- ✅ Include units in the name if applicable (e.g., `m_speedInMetersPerSecond`).
- ✅ Prefix Boolean fields with verbs like `is`, `has`, or `can` for clarity (e.g., `m_isActive`, `m_hasPermission`).
- ❌ Avoid redundancy by not repeating the class name in field names (e.g., use `m_health` instead of `m_playerHealth` in a `Player` class).
- ✅ Expose fields in the Inspector with `[SerializeField]`.
- ✅ Use properties when you need to access them from other classes.

```csharp
// Use `m_` prefix for private variables
private int m_health;

// Static variable with s_ prefix
private static int s_sharedCount;

// Constant with k_ prefix
private const int k_maxCount = 100;

// Use [SerializeField] rather than exposing your field publicly; keep it private or make it a property
[SerializeField] private int m_health;

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
- ✅ Prefer verb-like names for boolean properties (Is/Has/Can) (e.g., IsGrounded, HasHealtPack, CanJump).
- ❌ Do not serialize properties. Instead use [SerializeField] private T m_field when you need to expose it in the inspector plus a public property that returns or validates it.
- ✅ Use Properties for accessing or modifying the state of an object. Properties are ideal for lightweight operations with no or minimal side effects.
  Example: Health, Speed, IsGrounded.
- ℹ️ Use methods for actions or operations. Such as input handling and event-driven behavior. Name appropiate `ApplyDamage(int amount)` instead of `SetHealth(int amount)`.
  ❌ Avoid Using Properties for Actions: Properties should not perform significant computations, trigger events, or have side effects.
-
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
- ✅ Use event Action or event Action<T> for declaring events for the majority of cases.
- ✅ Use UnityEvent only when you need to expose callbacks to the Inspector. I generally avoid UnityEvent for code-only events as Action is more lightweight and flexible.
- ✅ Follow the C# event naming convention: use past tense verbs (e.g., `DoorOpened`, not `OnDoorOpen`).
- ✅ Use the On prefix for methods that raise events (e.g., OnDoorOpened), and use past-tense verbs for the event name itself (e.g., DoorOpened).
- ✅ Use the observer pattern to decouple systems and reduce dependencies (e.g., firing events for UI to update instead of direct references to UI components).
- ✅ Use the null-conditional operator (`?.`) when raising events to avoid null reference exceptions.
- ✅ Use EventArgs or custom event argument classes for events that require multiple parameters or complex data. This improves readability and maintainability compared to using multiple parameters.
- ⚠️ Avoid overusing events for tightly coupled systems where direct method calls would be simpler.
    - ✅ *Use Events*: When you need to decouple systems that don’t need to know about each other directly (e.g., broadcasting game state changes to multiple systems). For example, when a GameManager needs to notify multiple unrelated systems (e.g., UI, Audio, Analytics) about a game state change.
    - ❌ *Avoid Events*: When the systems are tightly coupled, and a direct method call or dependency injection is simpler and more efficient. For example, when a PlayerController directly controls a Weapon.

```csharp
// Event declarations
public event Action DoorOpened;         // Use past tense verbs for event names
public event Action<int> PointsScored;
public event Action<CustomEventArgs> ThingHappened;

// Event raising methods
public void OnDoorOpened()
{
    // Use the null-conditional operator to avoid null reference exceptions
    DoorOpened?.Invoke();
}

// When passing data with events
public void OnPointsScored(int points)
{
    PointsScored?.Invoke(points);
}

// Custom EventArgs class for complex data
public struct CustomEventArgs
{
    public int ObjectID { get; }
    public Color Color { get; }

    public CustomEventArgs(int objectId, Color color)
    {
        this.ObjectID = objectId;
        this.Color = color;
    }
}
```

#### Subscribing and unsubscribing to events
- ✅ Subscribe in the `OnEnable` and always unsubscribe in `OnDisable` to prevent memory leaks.
- ✅ Avoid using lambda expressions when subscribing to events as it makes unsubscribing impossible unless you store the lambda in a variable first.
- ⚠️ Be cautious when subscribing long-lived objects (e.g., singletons) to events from short-lived objects to avoid memory leaks.

```csharp
// Subscribing to events
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
- ✅ Cache component references (GetComponent, Find, pool creation).
- ✅ Initialize internal state that does not depend on other GameObjects
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
- ✅ Keep work small and reversible. Unsubscribe in OnDisable().

```csharp
private void Awake()
{
    // Cache component references here
    m_rigidbody = GetComponent<Rigidbody>();
}
```

### Start()
- ✅ Use Start for call initialization methods that require other components to exist and be ready.
- ✅ Perform initialization that requires other components or scene objects to exist.
- ✅ Use for one‑time setup (animations, UI wiring) that must run after all Awake()/OnEnable().

```csharp
private void Start()
{
    // Use cached references and perform operations that might depend on other components being initialized
    m_animator.SetTrigger("Initialize");
}
```

### OnDisable()
- ✅ Use OnDisable for unsubscribing from events and cleaning up state when the object is disabled.

```csharp
private void OnDisable()
{
    // Unsubscribe from events here to prevent memory leaks or unexpected behavior
}
```

### FixedUpdate()
- ⚠️ FixedUpdate runs on the fixed physics timestep and may run zero, one, or many times between Update calls depending on frame time.
- ✅ Use FixedUpdate for physics-related updates (e.g., applying forces, physics calculations).
- ✅ Put deterministic physics work here: AddForce, rigidbody velocity, simulation steps.
- ✅ Do not read input here; read input in Update() and apply it in FixedUpdate() if needed.
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
- ✅ Avoid allocations, use early returns (e.g., if (!m_isActive) return;) and delegate to well-named helper methods.
- ❌ Never create new collections in Update() but reuse existing ones.
- ✅ Use early returns to avoid unnecessary processing.
- ✅ Instead of having logic directly in the Update loop, move it to methods with descriptive names to improve cleanliness and self-documentation
-
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
- ✅ Finalize transforms, camera follow, animation-driven adjustments and cleanup after Update().
- ✅ Use for logic that must run after all Update() work.

```csharp
// Use LateUpdate for camera or post-processing updates
private void LateUpdate()
{

}
```

### General notes
- ✅ Keep related methods together for better readability.
- ✅ Keep MonoBehaviours focused on a single responsibility.
- ✅ Use `[RequireComponent(typeof(OtherComponent))]` when dependencies exist. It ensures the required component is always present so we don't need to check for null references later.
- ✅ Cache expensive operations outside of Update loops to prevent repeated allocations.
- ❌ Avoid magic numbers and strings. Replace hardcoded values (e.g., `5f` in Speed) with constants or serialized fields for better flexibility and readability.



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

### Methods
- ✅ Use methods for behavior and event callbacks (actions, side effects, or inputs). Examples: Jump(), TakeDamage(int amount), SetMovementInput(Vector2 input). Unity's PlayerInput and Inspector events call methods, not properties, so prefer methods for input handlers.
- ✅ Name methods with descriptive verbs to state the action clearly (e.g., ApplyDamage, PlaySound, RotateTurret, SetPosition, CalculateDamage).
- ✅ Use clear prefixes: SetX for assigning/updating a value (e.g., SetMovementInput(Vector2 input)), ChangeX for modifying or transforming state (e.g., ChangeHealth(int amount)).
- ✅ **Use "Process" for game logic operations** (turn-based, scheduled, or system-driven operations that are part of game flow). Examples: ProcessTradeIncome(), ProcessModifierDecay(), ProcessAgreementBonuses(). These are distinct from event handlers.
- ✅ **Use "Handle" for event-driven callbacks** (responding to external input or events). Examples: HandleTileSelected(), HandleTurnEnded(), OnDiplomacyButtonClicked(). These are invoked by the event system in response to external triggers.
- ✅ Boolean methods should pose a question and return bool, using Is, Has, or Can (e.g., IsPlayerAlive()).
- ❌Avoid noun-style method names except for factory methods or event handlers; avoid gerund/continuous names like Walking() or Rotating() (those indicate state—use isWalking / isRotating as variables or properties instead).
- ⚠️Terminology: prefer the term "method" in C# (a function that is part of a class).

```csharp
// Good: Use a method for actions or operations

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

// Use verb names that describe what the method does
public void SetInitialPosition(float x, float y, float z)
{
    transform.position = new Vector3(x, y, z);
}

public void SaveGame()
{
    // Implementation omitted: use try/catch for I/O and log errors as needed
}

// ✅ "Handle" for event-driven callbacks (responding to external events/input)
private void HandleTileSelected(MapTile tile)
{
    ChangeState(UIGameState.TownView);
}

// ✅ "Process" for game logic operations (part of game flow, usually turn-based or system-driven)
private void ProcessTradeIncome()
{
    foreach (var relationship in m_relationships)
    {
        if (relationship.InvolvesFaction(m_playerFactionData))
        {
            m_gameResources.ModifyCurrentGold(m_tradeAgreementGold);
        }
    }
}

// Good examples indicate an action being performed
public void SetInitialPosition(float x, float y, float z);
public void SaveGame();
public bool IsPlayerAlive();
public Player CreatePlayer();

// Avoid 'ing as that implies a continuous state or property rather than an action.
Walking(); // ❌ Avoid

// Boolean methods asking questions
public bool IsNewPosition(Vector3 newPosition)
{
    return (transform.position == newPosition);
}

```

# General tips to cleaner Unity code

## Interfaces
- ✅ Use interfaces to define clear "contracts" and decouple systems
- ✅ Use the one responsibility rule per interface (Interface Segregation). Small, focused interfaces are better than large monoliths.
- ✅ Use the I prefix and PascalCase (e.g., `IDamageable`, `IAudioService`).
- ✅ Name methods with verbs and boolean members with Is/Has/Can.
- ✅ Use an interface for a pure contract with no shared implementation and use an abstract base class when multiple implementations share behaviour or state.

```csharp
public interface IDamageable
{
    string DamageTypeName { get; }
    float DamageValue { get; }

    bool ApplyDamage(string description, float damage, int numberOfHits);
}

public interface IDamageable<T>
{
    void Damage(T damageTaken);
}
```
## Naming files and folders
- ✅ Use PascalCase for all file and folder names to maintain consistency with class and script naming conventions (e.g., `CharacterController.cs`, `AnimationController.cs`, `CoreSystems/`, `UI/`).
- ✅ Organize scripts into folders based on functionality or feature areas (e.g., `CoreSystems/`, `UI/`).
- ✅ Don't worry about long folder paths if they improve organization and clarity. That only helps future maintainers and copilot.
- ❌ Avoid spaces and special characters in file and folder names to prevent issues with version control systems and cross-platform compatibility.
- ℹ️ If you have a very long folder name with variations you can consider using _ instead of spaces to seperate words. Example: InputSystemActions_PlayerInputComponent_UnityEvents, InputSystemActions_PlayerInputComponent_CSharpEvents, etc.
- ❌ Don't use the ´NotImplementedException´ when stubbing out new methods or event handlers. It adds unnecessary noise and makes it harder to read the code. Instead, leave the method body empty or add a comment indicating that the implementation is pending.

```csharp

    private void LookInputReceived(InputAction.CallbackContext context)
    {
        // Don't: when Copilot helps create new methods, leave out the the NotImplementedException
        throw new NotImplementedException();
    }

```

### Use Enums for managing states
- ✅ Use enums for mutually exclusive states (e.g., animation, movement, UI, or game phases).
- ✅ Use enums in switch statements for clear, maintainable logic.
- ❌ Avoid using strings or integers directly for state tracking.
- ✅ Use enums when an object or action can only have one value at a time.
- ✅ Use Pascal case for enum names and values.
- ✅ Use a singular noun for the enum name as it represents a single value from a set of possible values.
- ❌ Avoid prefixes or suffixes (e.g., don’t add Enum, Type, or E_).
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

### Avoid nesting if statements
- ✅ Simplify the structure of your if statements by avoiding nesting. Use return instead
```csharp
// Avoid nesting
if (conditionA)
{
    if (conditionB)
    {
        ExecuteAction();
    }
}
// Better - avoid nesting
if (!conditionA) return;

```

### Managing String Allocations
- ✅ Use string interpolation ($"") for building strings instead of concatenation (+) to reduce garbage generation and improve readability.

```csharp
// Efficient string operations
public class ScoreManager : MonoBehaviour
{
   // Bad - creates garbage with string concatenation
   private string BuildLabelWithConcatenation(int score, float time)
   {
       return "Score: " + score + " Time: " + time;
   }

   // Good - use string interpolation
   private void UpdateScoreDisplay(int score, float time)
   {
       string result = $"Score: {score} Time: {time:F1}";
       // Display result...
   }
}
```

### Collection Type Selection
- ✅ Use List<T> when the collection size changes dynamically or frequent additions/removals are needed.
- ✅ Use arrays when the size is fixed and performance matters (e.g., tight update loops).
- ✅ Use Stack<T> for Last-In-First-Out (LIFO) logic such as undo systems, state history, or command buffers.
- ❌ Avoid allocations inside loops — reuse existing collections and call .Clear() instead of creating new instances.
- ✅ Initialize collections with a reasonable capacity when possible (e.g., new List<T>(capacity)) to reduce resizing overhead.
- ✅ Favor foreach loops when iterating read-only collections, as they improve readability and reduce indexing errors.
- ✅ Use Dictionary<TKey, TValue> when you need fast lookups by key.

```csharp
// List<T>: dynamic size, frequent add/remove
public class EnemyRegistry : MonoBehaviour
{
    // Initialize with modern syntax using New() (C# 9.0+)
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
### Async & Awaitable Usage
- ✅ Use the Awaitable API (available in Unity 6 and later) with async/await for timed delays, sequencing, or asynchronous workflows that don’t require per-frame iteration. This results in cleaner and more readable code compared to coroutines.
- ✅ Name async methods with the Async suffix (e.g., OpenDoorAsync) and coroutines with the Co suffix (e.g., LoadAssetsCo) to clearly distinguish them.
- ✅ Use PascalCase and verb-based names for both async and coroutine methods.
- ✅ Prefer Awaitable and async/await over StartCoroutine for simple delays or sequential logic.
- ❌ Do not mix Awaitable and coroutines within the same operation—choose one approach per workflow for clarity and maintainability.
- ✅ Use CancellationToken (for Awaitable) or check this == null to safely handle cancellation and prevent callbacks after an object is destroyed.

```csharp
public async Awaitable OpenDoorAsync()
{
    // Trigger animation or sound
    Debug.Log("Door opening...");

    // Wait 2 seconds before completing
    await Awaitable.WaitForSecondsAsync(2f);

    Debug.Log("Door opened!");
}

private IEnumerator LoadAssetsCo()
{
    // Simulate loading assets over multiple frames
    for (int i = 0; i < 5; i++)
    {
        Debug.Log($"Loading asset {i + 1}/5...");
        yield return new WaitForSeconds(0.5f); // Simulate delay
    }
    Debug.Log("All assets loaded!");
}

private async void Start()
{
    // Demonstrate timed async call
    await OpenDoorAsync();
}
```

### Scriptable Objects
- ✅ Favor ScriptableObjects for static configuration data and reusable content that stays the same while the game runs (e.g., weapons, enemy stats, skill effects).
- ❌ Don't use ScriptableObjects to store data that changes during gameplay (like player health, score, or runtime state).
- ✅ Use ScriptableObjects to reduce coupling between systems—feed configuration into MonoBehaviours instead of having them fetch data manually.
- ✅ Always mark ScriptableObjects with [CreateAssetMenu] for easy asset creation via the Project window.
- ✅ Append a `DataSO` suffix (e.g., `WeaponDataSO`) to make ScriptableObjects easily identifiable.
- ✅ Store ScriptableObject assets in a dedicated folder structure (e.g., Assets/Data/Weapons/).
- ✅ Keep ScriptableObjects focused on a single responsibility to enhance reusability and maintainability.
- ✅ Keep data and logic separate: ScriptableObjects should primarily hold data. Only add logic that directly relates to the data.
- ✅ Use properties to expose data from ScriptableObjects instead of public fields for better encapsulation.

```csharp
// WeaponData is a ScriptableObject that stores weapon configuration
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
### Animation Parameters, Layers, Tags, Sorting Layers, and Input Action Names
- ✅ **PascalCase**  is recommended for all text-based references such as animation parameters, layers, tags, sorting layers, and input action names. This aligns with Unity conventions and this guide's property naming.
- ✅ Prefix boolean animation parameters and similar flags with **Is**, **Has**, or **Can** (e.g., `IsRunning` rather than `Running`)
- ✅ Use descriptive names that clearly indicate the purpose or state, whether for animation, layers, tags, or input actions.
- ✅ Always define these names as constants in code to prevent runtime errors, enable refactoring, and avoid typos.
- ✅ Centralize these constants in a dedicated static class or script for maintainability and discoverability (even with modern IDEs like Visual Studio Code that support refactoring and renaming)

```csharp

// Centralized constants for animation parameters, layers, tags, and input actions

// You can use static classes to group related constants
public static class Layers
{
    public const string Player = "Player";
    public const string Enemy = "Enemy";
}

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

// Good - constants prevent typos and enable refactoring
private const string k_isRunningParam = "IsRunning";
private const string k_speedParam = "Speed";
private const string k_jumpTriggerParam = "JumpTrigger";
private const string k_isGroundedParam = "IsGrounded";
private const string k_attackIndexParam = "AttackIndex";
private const string k_isDeadParam = "IsDead";

// Usage - safe and maintainable
m_animator.SetBool(k_isRunningParam, isMoving);
m_animator.SetFloat(k_speedParam, currentSpeed);
m_animator.SetTrigger(k_jumpTriggerParam);

// Bad - magic strings scattered throughout code (runtime errors possible)
void UpdateMovement()
{
   m_animator.SetBool("IsWalking", isMoving);        // Typo risk
   m_animator.SetFloat("Spead", currentSpeed);       // Typo - fails silently!

   if (m_animator.GetBool("IsWalknig"))              // Another typo
   {
       // This condition will never be true due to typo
   }
}

// Good - centralized, safe, maintainable
private const string k_isWalkingParam = "IsWalking";
private const string k_speedParam = "Speed";


void UpdateMovement()
{
   m_animator.SetBool(k_isWalkingParam, isMoving);
   m_animator.SetFloat(k_speedParam, currentSpeed);

   if (m_animator.GetBool(k_isWalkingParam))
   {
       // Safe - IDE will catch typos at compile time
   }
}
```

## Debugging
- ✅ Log strategically: use Unity's `Debug.Log`, `Debug.LogWarning`, and `Debug.LogError` selectively. Avoid excessive logging, especially in production builds, to prevent performance issues.
- ✅ Use conditional compilation (e.g., `#if UNITY_EDITOR`) or a custom logging wrapper to strip or disable logs in release builds.
- ✅ Always include context in log messages (such as object name, method, or relevant state) to make debugging easier.
- ✅ Validate assumptions and invariants at runtime with `Debug.Assert` where appropriate.
- ✅ When using `Debug.Log`, pass a GameObject or component as the second parameter to link the log message to that object in the Console.
- ✅ Use `Debug.DrawLine`, `Debug.DrawRay`, and `Gizmos` for visual debugging in the Editor.
- ✅ Format debug messages consistently for easier searching and filtering.
- ✅ Validate reference dependencies with [RequireComponent] or explicit null checks.
- ✅ Use the Console window’s filters and stack traces to quickly locate issues.
- ✅ For larger projects, consider a logging abstraction with log levels (Info, Warning, Error) for more control.
- ⚠️ Avoid logging inside tight loops or performance-critical sections unless necessary for debugging specific issues.
- ℹ️ While checking for null references before logging can be useful, excessive null checks can clutter the code and you can use the [RequireComponent] attribute to ensure dependencies are met.

```csharp
// Include context in log messages
Debug.Log("Player has entered the trigger zone.", this.gameObject);

// Better error logging
Debug.LogError($"[{GetType().Name}] Failed to load data: {exception.Message}", this);

// Context-aware logging
Debug.LogWarning("Player health critical", gameObject);

// Using Debug.DrawLine for visual debugging
Debug.DrawLine(startPosition, endPosition, Color.red, 2f);

// Using Gizmos for editor visualization
private void OnDrawGizmos()
{
   Gizmos.color = Color.green;
   Gizmos.DrawWireSphere(transform.position, detectionRadius);
}

// Conditional logging example
#if UNITY_EDITOR
Debug.Log("This log only appears in the Editor.");
#endif

// Null checks can be useful but avoid excessive checks. It can clutter the code.
if (m_audioSource != null)
{
   Debug.Log("Audio source is available.", this);
}

// Instead you can use [RequireComponent] to ensure dependencies are met
[RequireComponent(typeof(AudioSource))]
public class AudioPlayer : MonoBehaviour
{
    private AudioSource m_audioSource;
}

```
## Using Try-Catch & Debugger Breaks

- ✅ Use try-catch blocks for handling external dependencies such as file I/O, network requests, or database operations, where failures are often outside your control (e.g., missing files, network timeouts, or permission issues). These are exceptional cases that justify the use of try-catch.
- ❌ Avoid using try-catch for internal logic or expected conditions (e.g., null checks, invalid input). Instead, validate inputs and use proper control flow to handle predictable scenarios.
- ✅ Always log the exception details (e.g., ex.ToString()) to help with debugging and troubleshooting.
- ✅ For critical external failures, consider rethrowing the exception or escalating it to a higher-level handler if the system cannot recover gracefully (e.g., to an analytics or error reporting service).

```csharp
// Example: Using try-catch sparingly for file I/O, with graceful fallback and Editor break

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
        // Optionally: rethrow or escalate if unrecoverable
    }
}
```

## Design Patterns for Unity
- ✅ Choose patterns pragmatically. Apply them when they solve a real problem or improve maintainability, not just for the sake of using a pattern.
- ⚠️ **Command pattern**: Consider for input handling, undo/redo, and action history systems.
- ⚠️ **Observer pattern** (or C# events): Consider for decoupling systems, such as UI updates or reacting to game events.
- ⚠️ **State pattern**: Consider for complex character controllers, AI, or UI flows where objects change behavior based on state.
- ⚠️ **Factory pattern**: Consider for flexible and centralized object creation (e.g., spawning enemies, projectiles).
- ⚠️ **Singleton pattern**: Consider sparingly for global managers (e.g., AudioManager), but avoid overuse as it can lead to tight coupling. Some prefer Dependency Injection for better testability.
- ✅ Use **Object Pooling** pattern for frequently spawned/despawned objects to improve performance and reduce garbage collection.
- ⚠️ **Strategy pattern**: Consider for interchangeable behaviors (e.g., different movement or attack types).
- ⚠️ **Service Locator / Dependency Injection**: Consider for managing cross-cutting services and improving testability.
- ✅ Use enums for mutually exclusive states (e.g., animation, movement, UI, or game phases).


### Implementing the State Pattern
- ✅ Use the State pattern for complex state-dependent behavior, such as character controllers or AI.

```csharp
// Example of State Pattern for a character controller
public class PlayerController : MonoBehaviour
{
    private PlayerState m_currentState;

    // State references
    private IdleState m_idleState;
    private RunningState m_runningState;
    private JumpingState m_jumpingState;

    private void Awake()
    {
        // Initialize states
        m_idleState = new IdleState(this);
        m_runningState = new RunningState(this);
        m_jumpingState = new JumpingState(this);

        // Set default state
        m_currentState = m_idleState;
    }

    private void Update()
    {
        // Let the current state handle the update
        m_currentState.Update();
    }

    public void ChangeState(PlayerState newState)
    {
        m_currentState.Exit();
        m_currentState = newState;
        m_currentState.Enter();
    }
}

// Base state class
public abstract class PlayerState
{
    protected PlayerController m_controller;

    public PlayerState(PlayerController controller)
    {
        m_controller = controller;
    }

    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}
```

### Object Pooling
- ✅ Use object pooling for frequently spawned and destroyed objects (e.g., bullets, enemies, particle effects) to reduce runtime allocations and improve performance.
- ✅ Prefer Unity’s built-in pooling APIs (e.g., UnityEngine.Pool.ObjectPool<T>) in Unity 6 and later, rather than implementing custom pooling logic.
- ✅ Initialize pools at scene load or on demand, and pre-warm with a reasonable number of objects to avoid spikes during gameplay.
- ✅ Always reset pooled objects’ state (position, rotation, active state, etc.) before reusing them.
- ✅ Return objects to the pool instead of destroying them; never use Destroy() on pooled objects except during cleanup.
- ✅ Use clear, descriptive method names like GetFromPool() and ReturnToPool() for pool operations.
- ✅ Keep pool management logic encapsulated—don’t expose pool internals to consumers.
- ✅ Use [DisallowMultipleComponent] and [RequireComponent] as needed to enforce correct usage on pooled objects.
- ❌ Avoid pooling objects with complex or persistent state that is hard to reset.

```csharp
// Example: Using Unity's built-in ObjectPool<T>
using UnityEngine.Pool;

public class BulletPool : MonoBehaviour
{
    [SerializeField] private Bullet m_bulletPrefab;
    private ObjectPool<Bullet> m_pool;

    private void Awake()
    {
        m_pool = new ObjectPool<Bullet>(
            createFunc: () => Instantiate(m_bulletPrefab),
            actionOnGet: bullet => bullet.gameObject.SetActive(true),
            actionOnRelease: bullet => bullet.gameObject.SetActive(false),
            actionOnDestroy: bullet => Destroy(bullet.gameObject),
            collectionCheck: false,
            defaultCapacity: 20,
            maxSize: 100
        );
    }

    public Bullet GetFromPool()
    {
        return m_pool.Get();
    }

    public void ReturnToPool(Bullet bullet)
    {
        m_pool.Release(bullet);
    }
}
```


# UI Toolkit

## UI Toolkit File Naming & Organization
- ✅ Use PascalCase for UXML filenames to align with Unity conventions and maintain consistency with class and script naming (e.g., `MainMenu.uxml`, `InventoryPanel.uxml`, `SettingsPanel.uxml`, `PlayerHUD.uxml`).
- ✅ Organize UXML and USS files in a consistent folder structure (e.g., Assets/UI/UXML/ and Assets/UI/USS/).
- ✅ Name USS files to match their corresponding UXML files for easy association (e.g., `MainMenu.uss` for `MainMenu.uxml`).

## UXML
- ✅ Use BEM (Block-Element-Modifier) for name and class values to improve maintainability, readability, and consistency between code and style and why it's widely considered a best practice standard
- ✅ Prefer kebab-case for UXML name and class strings (e.g., navbar-menu, shop-button).
- ✅ Use name for unique identifiers (e.g., elements you query in C#) and class for reusable styles or shared behavior.
- ✅ Keep name unique within it's block to improve query performance when using .Q() or .Query() from C#.
- ✅ Avoid overloading a single element with many unrelated classes; keep classes purposeful and focused.
- ✅ Group related elements inside a top-level block container to make queries and styling predictable.
- ✅ For nested blocks, use the parent block name as a prefix for child blocks (e.g., navbar-menu__dropdown).
- ✅ Add accessibility attributes (e.g., aria-label) to UXML elements where applicable.

**BEM refresher:**
- ℹ️ Pattern: `block-name__element-name--modifier-name`
    - ℹ️ Block: standalone component that is meaningful on it's own (e.g., `navbar-menu`, `sidebar`, `login-form`)
    - ℹ️ Element: part of a block that has no standalone meaning and is semantically tied to it's block (e.g., `__item`, `__button`, `__input-field`)
    - ℹ️ Modifier: a flag on a block or element used to change appearance or behavior (e.g., `--active`, `--collapsed`, `--error`)
- ℹ️ Parts joined by `__` (element) and `--` (modifier)
- ℹ️ Examples: `menu__home-button`, `menu__shop-button`, `navbar-menu__shop-button--small`, `button--primary`

**Examples**
- These follow the BEM (Block-Element-Modifier) standard, ensuring clarity, structure, and maintainability.

  ***Block Names***: should clearly describe the purpose or role of the block within the UI and be suitable for grouping related elements
    - ✅ `navbar-menu`(easy to identify navigation menu block)
    - ✅ `sidebar`
    - ✅ `login-form`
    - ❌ `menu` (too generic, lacks context)
    - ❌ `navBarMenu` (camelCase instead of kebab-case)
    - ❌ `navbar_menu` (uses underscores instead of dashes)

  ***Element Names***: should describe the specific part of the block they belong to, maintaining a clear relationship to the block
    - ✅ `navbar-menu__item`
    - ✅ `sidebar__toggle-button`
    - ✅ `login-form__input-field`
    - ❌ `navbar-item` (missing the block reference, should be `navbar-menu__item`)
    - ❌ `sidebar-button` (missing the block reference, should be `sidebar__button`)
    - ❌ `login-form-input` (missing the __ for the element, should be `login-form__input`)

  ***Modifier Names***: should indicate variations or states of blocks or elements
    - ✅ `navbar-menu__item--active`
    - ✅ `sidebar__toggle-button--collapsed`
    - ✅ `login-form__input-field--error`
    - ❌ `navbar-menu__item-active` (missing `--` for the modifier, should be `navbar-menu__item--active`)
    - ❌ `sidebar__toggleButton--collapsed` (camelCase instead of kebab-case)
    - ❌ `login-form__input-field_error` (uses underscores instead of -- for the modifier)

**Example (UXML)**
```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
  <!-- Block container -->
  <ui:VisualElement name="navbar-menu" class="navbar-menu">
    <!-- Element: a specific button inside the block -->
    <ui:Button name="navbar-menu__shop-button" class="navbar-menu__shop-button button button--primary" aria-label="Shop">
      <ui:Button.text>Shop</ui:Button.text>
    </ui:Button>
    <!-- Variant via modifier -->
    <ui:Button name="navbar-menu__shop-button--small" class="navbar-menu__shop-button navbar-menu__shop-button--small button button--small" aria-label="Shop (Small)">
      <ui:Button.text>Shop</ui:Button.text>
    </ui:Button>
  </ui:VisualElement>
</ui:UXML>
```

**Querying from C#***
```csharp
// Centralize selectors as constants to avoid typos
public static class UiSelectors
{
    public const string NavbarMenu = "navbar-menu"; // block
    public const string ShopButton = "navbar-menu__shop-button"; // element
    public const string ShopButtonSmall = "navbar-menu__shop-button--small"; // modifier
}

// Usage in a MonoBehaviour or UI controller
var root = GetComponent<UIDocument>().rootVisualElement;
var navbar = root.Q<VisualElement>(UiSelectors.NavbarMenu);
var shopButton = root.Q<Button>(UiSelectors.ShopButton);
shopButton.clicked += OnShopClicked;
```

## USS
**Guidelines**
- ✅ Make sure not confuse CSS with USS. USS is a subset of CSS with Unity-specific properties and limitations. Refer to the [Unity USS documentation](https://docs.unity3d.com/Manual/UIE-USS.html) for supported features.
- ✅ Use **kebab-case** for class names. prefer **BEM** to encode structure and variants.
- ✅ Keep selectors **flat and specific**: prefer `.block__element` over deep descendant chains.
- ✅ Use **modifiers** as additive classes (e.g., `.button--small`) instead of redefining the base element.
- ✅ Keep **state** styles separate via state classes (e.g., `.is-selected`, `.is-disabled`) or use built-in pseudo-classes when available.
- ✅ Define **design tokens** (colors, spacing, sizes) as USS variables at the root when possible.
- ✅ Do keep class names short, descriptive, and BEM-aligned.
- ✅ Do centralize string constants used in code to avoid typos.
- ❌ Don’t rely on deep descendant selectors (e.g., `.a .b .c`) — they become brittle.
- ❌ Don’t mix unrelated concerns in one class; compose via multiple small classes instead.

**Example (USS)**
```css
/* Block base */
.navbar-menu { padding: 8px; gap: 8px; }

/* Element base */
.navbar-menu__shop-button { min-width: 120px; }

/* Modifier */
.navbar-menu__shop-button--small { min-width: 80px; }

/* Generic button system using BEM-like modifiers */
.button { height: 32px; padding-left: 12px; padding-right: 12px; }
.button--primary { background-color: rgb(40, 120, 240); color: white; }
.button--small { height: 24px; font-size: 11px; }

/* State classes (add/remove from C#) */
.is-selected { outline-color: rgb(255, 200, 0); outline-width: 2px; outline-style: solid; }
.is-disabled { opacity: 0.5; }
```

**Toggling classes from C#**
```csharp
// Toggle modifiers and state via classList
var btn = root.Q<Button>(UiSelectors.ShopButton);
btn.classList.Add("button--primary");

// Set a state
btn.classList.Toggle("is-selected", true);

// Switch to a different size variant
btn.classList.Remove("navbar-menu__shop-button--small");
btn.classList.Add("button--small");
```

### UI Toolkit Event Handling
```csharp
// Proper UI Toolkit event registration
private void OnEnable()
{
   m_button.clicked += OnButtonClicked;
   m_dropdown.RegisterValueChangedCallback(OnDropdownChanged);
}


private void OnDisable()
{
   m_button.clicked -= OnButtonClicked;
   m_dropdown.UnregisterValueChangedCallback(OnDropdownChanged);
}
```
