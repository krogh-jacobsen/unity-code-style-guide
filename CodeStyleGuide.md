# GitHub Copilot Instructions: Unity C# Style Guide & Naming

This document serves two purposes:
1. To provide human-readable explanations of the coding conventions.
2. To guide GitHub Copilot in generating code that aligns with these conventions.

## About this Style Guide (for the human reader)
The instructions are designed to help GitHub Copilot better match my approach and style. The code style standards are a variation of the [Unity C# style guide ebook we released for Unity 6](https://github.com/thomasjacobsen-unity/Unity-Code-Style-Guide), which I co-authored and is intended to be more LLM-friendly, pragmatic, and beginner-friendly. That guide stands on the shoulders of the [Microsoft Framework Design Guidelines](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/) and common industry best practices.

While this guide is aimed at Copilot, it also includes short explanations about why certain choices are made, useful for anyone reading it. Some points are repeated or phrased in a few different ways to give Copilot more examples and context. It might feel a bit verbose, but it helps reinforce the intent behind each rule to help Copilot make more informed decisions.

Any code style guide should evolve over time. That has also been the case for this doc, and the intent is to update it as needed. Note that these instructions are specific to Unity and include some opinionated, Unity-specific conventions based on personal experience.

Feel free to use it for inspiration, tweak it to your own preferences, or use it for your own Unity projects. Happy coding!
## Instructions for GitHub Copilot
The following sections provide specific coding conventions and examples for GitHub Copilot to follow.

- ℹ️ To provide GitHub Copilot with clear instructions on how to generate code that aligns with my coding style and conventions for Unity C# projects.
- ℹ️ To ensure consistency, readability, and maintainability across the codebase by adhering to established coding standards.
- ℹ️ To help Copilot understand the specific Unity version and features being used in this project.
- ℹ️ To improve the quality of code suggestions and completions provided by Copilot, making them more relevant and useful for this particular project.

## Key Principles for this Style Guide

- ℹ️ The standards specified here stand on the shoulders of the [Microsoft Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/) and common industry best practices.
- ℹ️ The variations are generally intended to be more LLM-friendly, pragmatic, and beginner-friendly as well as Unity-specific.
- ℹ️ When something isn’t explicitly covered here, default to Microsoft’s general recommendations for C#.
- ℹ️ The goal is to make the code more readable, maintainable, and consistent. Being consistent creates patterns and enables Copilot to make more accurate predictions.
- ℹ️ Simple is better than complicated.
- ℹ️ The code should strive to comply with the SOLID principles, be clean, and DRY.
- ℹ️ Doing things like naming the right way from the beginning will save time and effort later, particularly when debugging and extending functionality.
- ℹ️ As much as possible, stick to industry standards and conventions but be pragmatic. Not all rules will apply in every situation, so use judgment and adapt as needed.

## Unity Version-Specific Instructions

- ℹ️ This project uses Unity 6. Make sure to use the latest sources and documentation that apply to Unity 6 or later versions.
- ℹ️ This project uses the newer Input System and not the older Input Manager.
- ℹ️ This project uses the newer UI Toolkit and not the older UGUI for UI.
- ℹ️ This project uses the Universal Render Pipeline and not the old Built‑in Render Pipeline.
- ℹ️ When implementing systems like object pooling, make sure to use Unity's own API.
- ℹ️ When implementing async operations, consider using Unity's built-in Awaitable API.


## The Unity C# fundamentals

### Balancing being too succinct vs. too verbose

- ⚠️ Succinctness is often good, but not at the cost of clarity. A code style guide should provide enough context for Copilot to understand the intent behind naming and formatting choices beyond the patience of the reader.
- ✅ Prioritize readability and clarity over cleverness or brevity. More context is better than less. Don't sacrifice context by making things too short, as the LLMs might miss the intent.
- ❌ Don't use abbreviations. Use meaningful names and spell out words completely. Clarity and readability are more important than any time saved from omitting a few vowels.
- ⚠️ Yet don't make it too long by adding unnecessary information. Ensure each point adds value and context.

### General naming
- ✅ Use meaningful, descriptive names that clearly convey the purpose and intent of the variable, method, class, etc. Names should be descriptive, clear, and unambiguous because they represent an action, thing or state.
- ✅ Favor names that can be pronounced naturally and are readable (e.g., `HorizontalAlignment` instead of `AlignmentHorizontal`).
- ❌ Don't use abbreviations unless it's math or commonly accepted. Your variable names should reveal their intent.
- ✅ Pick meaningful names from the beginning to minimize refactoring later.
- ✅ Use a noun when naming them except when the variable is of the type `bool`.
- ✅ Prefix Booleans with a verb to make their meaning more apparent. e.g., `isDead`, `isWalking`, `hasDamageMultiplier`.
- ✅ Make type names unambiguous across namespaces and problem domains by avoiding common terms or adding a prefix or a suffix (e.g., use `PhysicsSolver`, not `Solver`).

```csharp
// Examples of good naming
bool m_isPlayerDead;
bool m_hasWeapon;

// Examples of bad naming
bool m_dead;
bool m_weapon;
```

### Formatting

- ⚠️ Readability is key. Try to keep lines short. Consider horizontal whitespace.
- ✅ Use the Allman style (opening curly braces on a new line).
- ✅ Define a standard max line width in your style guide (some prefer less than 120–140 characters).
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

#### Spacing

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

## Comments
- ✅ Add clarifying comments to most lines. However, they should provide valuable context or clarify intent that isn’t obvious from good naming.
- ⚠️ If a comment is needed to explain complex logic, consider refactoring the code to improve clarity first.
- ✅ Favor simple, succinct comments that explain “why” rather than “what” the code does.
- ✅ Prefer renaming variables or methods to make intent clear before relying on comments.
- ⚠️ When in doubt, err on the side of providing more context, but avoid commenting code that is already self-explanatory.
- ✅ Use the comment to keep the explanation next to the logic.
- ✅ Use a Tooltip instead of a comment for serialized fields if your fields in the Inspector need explanation. If you want to debug or tweak input actions during runtime, consider exposing them in the Inspector using [SerializeField].

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

## Fields
- ⚠️ As a default always make your fields private so they are not exposed to other scripts and properly encapsulated adhering to basic OOP principles.
- ✅ Instead leverage Unity's inspector window by making use of [SerializeField] when you need to expose a field in the Inspector.
- ✅ Use properties when you need to access them from other classes.

```csharp
// Use [SerializeField] rather than exposing your field publicly; keep it private or make it a property
[SerializeField] private int m_playerHealth;
```

### Custom attributes
- ✅ Use Unity attributes to improve the Inspector experience.
- ✅ Use `[Tooltip]`, `[Range]` for exposed fields where relevant.
- ✅ Use `[Header]` and `[Space]` for grouping fields.
- ✅ Consider `[ContextMenu]` or `[Button]` (with Odin or NaughtyAttributes) to create dev tools.

```csharp
[Header("Movement Settings")]
[SerializeField, Range(0f, 20f)] private float m_moveSpeed = 5f;

[ContextMenu("Reset Position")]
private void ResetPosition()
{
    transform.position = Vector3.zero;
}
```

### Casing and Prefixes

- ⚠️ Specificity reduces guesswork and prefixes help reveal intent.
- ✅ Use prefixes for private member variables (`m_`), constants (`k_`), and static variables (`s_`), so the name reveals more about the variable at a glance.
- ✅ Use PascalCase (e.g., `ExamplePlayerController`, `MaxHealth`, etc.) unless noted otherwise.
- ✅ Use camelCase (e.g., `examplePlayerController`, `maxHealth`, etc.) for local/private variables and parameters.
- ✅ Avoid snake_case, kebab-case, Hungarian notation in your C# code (you can consider kebab-case for UXML and USS when using UI Toolkit).

```csharp
// Member variable should have an m_ prefix
[SerializeField] private int m_playerHealth;

// Static variable should have an s_ prefix
private static int s_instanceCount;

// Constant with k_ prefix
private const float k_maxSpeed = 10f;
```

### Avoid redundancy but don't leave out context

- ⚠️ Drop redundant initializers (i.e., no `= 0` on ints, `= null` on ref types, etc.) as they are initialized to 0 or null by default.
- ⚠️ Don't omit private access level modifiers consistently even though they are redundant. Microsoft guidelines recommend explicitly specifying private to make the access level clear and to avoid any ambiguity.
- ⚠️ Avoid redundant names: If your class is called `Player`, you don't need to create member variables called `PlayerScore` or `PlayerTarget`. Trim them down to `Score` or `Target`.
- ⚠️ Consider using XML tags in front of public methods or functions for output documentation/IntelliSense.
- ⚠️ Avoid attributions, e.g., `// Created by`, `// Modified by`, etc. Use version control to track changes.

## Organize your class by the Unity Script Execution Order

- ✅ Organize your class in the Unity script execution order: Fields, Properties, Events, MonoBehaviour methods (`Awake`, `OnEnable`, `Start`, `OnDisable`, `OnDestroy`, etc.), public methods, private methods, other classes.
- ✅ Keep related methods together for better readability.
- ✅ Keep MonoBehaviours focused on a single responsibility. If a class is getting too large or complex, consider breaking it into smaller components or using ScriptableObjects for data/configuration.
- ✅ Use `[RequireComponent(typeof(OtherComponent))]` when dependencies exist. It ensures the required component is always present so we don't need to check for null references later.
- ✅ Cache expensive operations outside of Update loops to prevent repeated allocations.
- ❌ Avoid magic numbers and strings. Replace hardcoded values (e.g., `5f` in Speed) with constants or serialized fields for better flexibility and readability.

```csharp
using UnityEngine;

// Require necessary components
[RequireComponent(typeof(Rigidbody))]

namespace MyGame.Examples
{
    public class ExampleMonoBehaviour : MonoBehaviour
    {
        // Fields before properties
        [SerializeField] private float m_speed = 5f;
        private Rigidbody m_rigidbody;

        // Properties
        public float Speed
        {
            get => m_speed;
            set => m_speed = value;
        }

        // Events
        public event Action OnSpeedChanged;

        // Cache expensive operations in Awake
        private void Awake()
        {
            // Cache component references here
            m_rigidbody = GetComponent<Rigidbody>();
        }

        private void OnEnable()
        {
            // Subscribe to events here. Avoid using lambda
        }

        private void Start()
        {
            // Use cached references and perform operations that might depend on other components being initialized
            m_animator.SetTrigger("Initialize");
        }

        private void OnDisable()
        {
            // Unsubscribe from events here to prevent memory leaks or unexpected behavior
        }

        // Good - descriptive method names and cached values
        private void Update()
        {
            // Put all your regular frame logic update code in Update()

            if (!m_isActive) return; // Early return pattern

            // Move logic to well-named methods
            HandleMovement();
            UpdateAnimations();
            CheckPlayerInput();
        }

        // Use FixedUpdate for physics
        private void FixedUpdate()
        {
            HandlePhysicsMovement();
        }

        // Use LateUpdate for camera or post-processing updates
        private void LateUpdate()
        {

        }

        // MonoBehaviour methods follow after the lifecycle methods

        // Public methods

        // Private methods
    }
}
```

### Use of regions
- ℹ️ Use `#region` sparingly. It's sometimes helpful but generally discouraged because it can hide complexity and often signals a class is too large and should be refactored instead.
- ✅ A good use case for `#region` however is to group Animation Event Handlers or Input Event Handlers, called from the animation system etc. so they are clearly separated from the rest of the code.

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


### Using statements

- ✅ Keep using statements at the top of your file.
- ✅ Start with the generic ones at the top. Add the specific ones, such as your own last.
- ✅ Regularly remove unused `using` statements to keep the file clean and avoid unnecessary dependencies.
- ✅ Start with system namespaces (e.g., `System`, `System.Collections`) at the top.
- ✅ Follow with Unity namespaces (e.g., `UnityEngine`).
- ✅ Add project-specific namespaces (e.g., `MyGameProject.Utilities`) last.
- ✅ Ordering `using` statements improves readability and ensures consistency across files. It also helps avoid conflicts when namespaces have overlapping class names.
- ✅ Use IDE tools like "Organize Imports" in Visual Studio Code to automatically sort and remove unused `using` statements.

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
- ℹ️ Some recommend namespaces that reflect the folder structure of the project so it's logically grouped, but it's not a hard requirement.

```csharp
namespace MyGame.Characters
{
    public class Player : MonoBehaviour
    {
        // Class implementation
    }
}
```


### Fields
- ✅ Don't omit the private accessor field though technically its implicit. It provides context about the intent.
- ✅ Use `m_` prefix for private variables, `k_` for constants
- ✅ Prefix Booleans with a verb like "is" to make their meaning apparent
- ✅ Use `m_` prefix for private fields to distinguish them from local variables.
- ✅ Use `k_` prefix for constants to indicate immutability.
- ✅ Use descriptive names that clearly indicate the field's purpose.
- ❌ Avoid abbreviations unless they are widely understood (e.g., `UI`, `ID`).
- ✅ Include units in the name if applicable (e.g., `m_speedInMetersPerSecond`).
- ✅ Prefix Boolean fields with verbs like `is`, `has`, or `can` for clarity (e.g., `m_isActive`, `m_hasPermission`).
- ❌ Avoid redundancy by not repeating the class name in field names (e.g., use `m_health` instead of `m_playerHealth` in a `Player` class).

```csharp
// Examples
[SerializeField] private int m_health;  // Good: Descriptive and uses prefix
private const float k_gravity = 9.8f;   // Good: Constant with prefix
private bool m_isVisible;               // Good: Boolean with verb prefix
private int m_elapsedTimeInHours;       // Specify the unit used to eliminate guessing
private int m_elapsedTimeInDays;        // Don't omit the private accessor
private int m_elapsedTimeInSeconds;     // Don't abbreviate. Favor readability.
[SerializeField] private bool m_isPlayerDead;   // Prefix Booleans with a verb like "is" to make their meaning apparent
private static int s_sharedCount;          // Static variable with s_ prefix
private const int k_maxCount = 100;      // Constant with k_ prefix

```

### Properties
- ✅ Use PascalCase for properties and avoid prefixes/suffixes.
- ✅ Prefer verb-like names for boolean properties (Is/Has/Can).
- ✅ Use m_ prefix for backing fields and keep one field per line.
- ❌ Do not serialize properties. Instead use [SerializeField] private T m_field when you need to expose it in the inspector plus a public property that returns or validates it.
- ✅ Place properties after fields and before MonoBehaviour methods as per your class organization.
- ✅ Place properties after fields and before MonoBehaviour methods as per your class organization.
- ✅ Use properties for simple state access or modification.
- ℹ️ Use methods for actions or operations. Such as input handling and event-driven behavior. Name appropiate `ApplyDamage(int amount)` instead of `SetHealth(int amount)`.

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
```

### Start vs. Awake
- ✅ Use Awake for initializing references between components and from different GameObjects.
- ✅ Use Start for call initialization methods that require other components to exist and be ready.


```csharp
    public class Player : MonoBehaviour
    {
        private Animator m_animator;
        [SerializeField] private AudioManagerOnOtherGameObject m_audioManager;

        private void Awake()
        {
            // Cache component references here
            m_animator = GetComponent<Animator>();
            m_audioManager = FindObjectOfType<AudioManagerOnOtherGameObject>();
        }

        private void Start()
        {
            // Use cached references and perform operations that might depend on other components being initialized
            m_animator.SetTrigger("Initialize");
            m_audioManager.PlaySound("PlayerSpawn");
        }
    }

```

### Properties vs. Methods: When to Use Each
- ✅  Use Properties for accessing or modifying the state of an object. Properties are ideal for lightweight operations with no or minimal side effects.
Example: Health, Speed, IsGrounded.
- ❌ Avoid Using Properties for Actions: Properties should not perform significant computations, trigger events, or have side effects.

```csharp
// Properties for simple state access
public float Speed { get; private set; }
public bool IsGrounded => m_isGrounded;

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
- ✅ Use Methods for performing actions or operations that involve behavior, side effects, or require input parameters. Example: `Jump()`, `TakeDamage(int amount)`, `SetMovementInput(Vector2 input)`.
- ✅ Use methods for event callbacks, as Unity allows methods (but not properties) to be assigned to events in the Inspector. Example: The PlayerInput component can call a method like `SetMovementInput(Vector2 input)` in response to input events.
- ✅ Use descriptive verb-based names for methods to clearly indicate the action being performed.
- ✅ Use `SetX` as prefix when naming a method which is primarily assigning or updating a value (e.g., SetMovementInput(Vector2 input)).
- ✅ Use `ChangeX` when naming a method that implies a transformation or modification of the current state (e.g., ChangeHealth(int amount)).


```csharp
// Good: Use a method for actions or operations
public void Jump()
{
    m_rigidbody.AddForce(Vector3.up * m_jumpForce, ForceMode.Impulse);
}

// Good: Clear intent for setting a value
public void SetMovementInput(Vector2 input)
{
    m_forwardMovementInput = input;
}

// Good: Clear intent for modifying a value
public void ChangeHealth(int amount)
{
    m_health += amount;
}

// Avoid: Ambiguous name that could be confused with a property
public void MovementInput(Vector2 input)
{
    m_forwardMovementInput = input;
}

```

- ✅ General Rule of Thumb:
Use properties for state (e.g., IsGrounded, Health).
Use methods for behavior (e.g., Jump(), TakeDamage()).
- ℹ️ Unity-Specific Considerations: Unity's PlayerInput component often calls methods for input handling. For example, use a method like SetMovementInput(Vector2 input) instead of a property to align with Unity's event-driven design.


### Update vs. FixedUpdate
- ✅ Use Update for regular frame updates (e.g., input handling, non-physics calculations).
- ✅ Use FixedUpdate for physics-related updates (e.g., applying forces, physics calculations).
- ✅ Never create new collections in Update() but reuse existing ones.
- ✅ Cache string operations and use StringBuilder for complex concatenation.
- ✅ Use early returns to avoid unnecessary processing.
- ✅ Instead of having logic directly in the Update loop, move it to methods with descriptive names to improve cleanliness and self-documentation


```csharp
// Enhanced collection management with modern C# and performance best practices
public class EnemyManager : MonoBehaviour
{
   // Modern initialization syntax (C# 9.0+)
   [SerializeField] private List<GameObject> m_activeEnemies = new();
   [SerializeField] private Dictionary<string, List<GameObject>> m_enemyScores = new();
   [SerializeField] private HashSet<string> m_uniqueIds = new();

   // Reusable collection to avoid allocations in Update
   private List<Enemy> m_tempNearbyEnemies = new();
   private Vector3 m_cachedPosition;

   public void RegisterEnemy(GameObject enemy)
   {
       if (!m_activeEnemies.Contains(enemy))
       {
           m_activeEnemies.Add(enemy);
       }
   }

   public void ClearAllEnemies()
   {
       // Reuse the list to avoid GC pressure
       m_activeEnemies.Clear();
   }

   // Good - avoid allocations in Update
   private void Update()
   {
       if (!m_isActive) return; // Early return pattern

       // Reuse collection instead of creating new one
       GetNearbyEnemies(m_tempNearbyEnemies);
       ProcessEnemies(m_tempNearbyEnemies);
       m_tempNearbyEnemies.Clear(); // Clear for next frame

       // Reuse Vector3 instead of creating new ones
       m_cachedPosition.Set(newX, newY, newZ);
   }

   // Bad example - creates garbage every frame
   private void Update()
   {
       var nearbyEnemies = GetEnemiesInRange(); // Returns new List<>
       var position = new Vector3(x, y, z);     // Creates new Vector3
   }
}

```

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

- ✅ Use verb-based method names so the code clearly states the action being performed (e.g., ApplyDamage, PlaySound, RotateTurret).
- ✅ Prefer names that describe what the method does (for example, SetPosition or CalculateDamage).
- ❌ Avoid noun-style method names except for factory methods or event handlers.
- Boolean methods should ask a question, starting with verbs like `Is`, `Has`, or `Can`.
- ❌ Avoid confusion: Names like `Walking()` or `Rotating()` imply a continuous state or property rather than an action.
- ✅ These are better suited for variables or properties (e.g., `isWalking`, `isRotating`).
- ⚠️ Though people sometimes use method and function interchangeably in casual conversation, the term "method" is more accurate in C# as it refers to functions that are part of a class.

```csharp
// Good examples
public void SetInitialPosition(float x, float y, float z);
public void SaveGame();
public bool IsPlayerAlive();
public Player CreatePlayer();
Walk(); // Indicates an action being performed

// Avoid 'ing as that implies a continuous state or property rather than an action.
Walking();

// Use verb names that describe what the method does
public void SetInitialPosition(float x, float y, float z)
{
    transform.position = new Vector3(x, y, z);
}

// Boolean methods asking questions
public bool IsNewPosition(Vector3 newPosition)
{
    return (transform.position == newPosition);
}

// Using var keyword
void ExampleMethod()
{
    var powerUps = new List<PlayerStats>();
    var dict = new Dictionary<string, List<GameObject>>();

    // Proper loop formatting
    for (int i = 0; i < 100; i++)
    {
        DoSomething(i);
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

### Interfaces
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

## General tips to cleaner Unity code

### Enums

- ✅ Use enums when an object or action can only have one value at a time.
- ✅Use Pascal case for enum names and values.
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
✅ Favor ScriptableObjects for static configuration data and reusable content that stays the same while the game runs (e.g., weapons, enemy stats, skill effects).
✅ You should not use ScriptableObjects to store data that changes during gameplay (like player health, score, or runtime state).
✅ Use ScriptableObjects to reduce coupling between systems—feed configuration into MonoBehaviours instead of having them fetch data manually.
✅ Always mark ScriptableObjects with [CreateAssetMenu] for easy asset creation via the Project window.
✅ Append a `DataSO` suffix (e.g., `WeaponDataSO`) to make ScriptableObjects easily identifiable.
✅ Store ScriptableObject assets in a dedicated folder structure (e.g., Assets/Data/Weapons/).
✅ Keep ScriptableObjects focused on a single responsibility to enhance reusability and maintainability.
✅ Keep data and logic separate: ScriptableObjects should primarily hold data. Only add logic that directly relates to the data.
✅ Use properties to expose data from ScriptableObjects instead of public fields for better encapsulation.

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

### Use Enums for managing states
- ✅ Use enums for mutually exclusive states (e.g., animation, movement, UI, or game phases).
- ✅ Use enums in switch statements for clear, maintainable logic.
- ❌ Avoid using strings or integers directly for state tracking.

```csharp
// Enum for animation states
public enum MovementState
{
    Idle,
    Walking,
    Running,
    Jumping
}

private MovementState m_currentState;

private void Update()
{
    switch (m_currentState)
    {
        case MovementState.Idle:
            // Handle idle logic
            break;
        case MovementState.Walking:
            // Handle walking logic
            break;
        case MovementState.Running:
            // Handle running logic
            break;
        case MovementState.Jumping:
            // Handle jumping logic
            break;
    }
}
```

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


## UXML & USS files
- ✅ Use PascalCase for USS and UXML filenames as well as custom UXML elements (custom controls) to align with Unity conventions and maintain consistency with class and script naming (e.g., MainMenu.uxml, InventoryPanel.uxml, SettingsPanel.uxml, PlayerHUD.uxml)


## Visual Elements in UXML
- ✅ Use kebab-case for UXML elements names (e.g., navbar-menu, shop-button).
- ✅ Keep name unique within its block to improve query performance when using .Q() or .Query() from C#.
- ✅ Element name should stay short, semantic, and unique.


**Example (UXML)**
```xml
<ui:UXML xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ui="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements" noNamespaceSchemaLocation="../../../UIElementsSchema/UIElements.xsd" editor-extension-mode="False">
    <Style src="project://database/Assets/UI/Runtime/B03_MainMenu/MainMenuStyles.uss?fileID=7433441132597879392&amp;guid=a182ccb84c0dd044a8df49d76f575b05&amp;type=3#MainMenuStyles"/>
    <Bagel.MainMenuPaneManager name="main-menu-pane-manager">
        <ui:Label text="Bagel Game" name="title" class="b-title"/>
        <ui:Button text="Play" name="play-button" class="b-primary"/>
        <ui:Button text="Settings" name="settings-button"/>
        <ui:Button text="Leaderboard" name="leaderboard-button"/>
        <ui:Button text="Exit" name="exit-button"/>
    </Bagel.MainMenuPaneManager>
</ui:UXML>
```

**Querying from C#***
```csharp
// Centralize selectors as constants to avoid typos
public static class UiSelectors
{
   public const string NavbarMenu = "navbar-menu"; // block
   public const string ShopButton = "shop-button"; // element
modifier
}


// Usage in a MonoBehaviour or UI controller
var root = GetComponent<UIDocument>().rootVisualElement;
var navbar = root.Q<VisualElement>(UiSelectors.NavbarMenu);
var shopButton = root.Q<Button>(UiSelectors.ShopButton);
shopButton.clicked += OnShopClicked;
```


## USS
**Guidelines**
- ✅ Use BEM (Block-Element-Modifier) for styling and thus for naming USS classes to improve maintainability,
readability, and consistency between code and style and why it's widely considered a best practice standard
- ✅ Use **kebab-case** for class names. prefer **BEM** to encode structure and variants.
- ✅ Keep selectors **flat and specific**: prefer `.block__element` over deep descendant chains.
- ✅ Use **modifiers** as additive classes (e.g., `.button--small`) instead of redefining the base element.
- ✅ Keep **state** styles separate via state classes (e.g., `.is-selected`, `.is-disabled`) or use built-in pseudo-classes when available.
- ✅ Define **design tokens** (colors, spacing, sizes) as USS variables at the root when possible.
- ✅ Do keep class names short, descriptive, and BEM-aligned.
- ✅ Do centralize string constants used in code to avoid typos.
- ❌ Don’t rely on deep descendant selectors (e.g., `.a .b .c`) — they become brittle.
- ❌ Don’t mix unrelated concerns in one class; compose via multiple small classes instead.
- ✅ For nested blocks, use the parent block name as a prefix for child blocks (e.g., navbar-menu__dropdown).

**BEM refresher:**
- ℹ️ Pattern: `block-name__element-name--modifier-name`
   - ℹ️ Block: standalone component that is meaningful on its own (e.g., `navbar-menu`, `sidebar`, `login-form`)
   - ℹ️ Element: part of a block that has no standalone meaning and is semantically tied to its block (e.g., `__item`, `__button`, `__input-field`)
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
   - ❌ `navbar-menu__item-active` (missing -- for the modifier, should be `navbar-menu__item--active`)
   - ❌ `sidebar__toggleButton--collapsed` (camelCase instead of kebab-case)
   - ❌ `login-form__input-field_error` (uses underscores instead of -- for the modifier)

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
## Using .editorconfig to Enforce Formatting Rules ##

- ✅ Use an .editorconfig file to define and enforce consistent formatting rules across your project. This ensures all contributors follow the same coding style, improving readability and maintainability.
- ✅ Place the .editorconfig file in the root of your repository so it applies to the entire project.
- ✅ Define rules for indentation, spacing, line endings, and other formatting preferences (e.g., Allman braces, max line length).
- ✅ Use Unity-specific settings where applicable, such as ensuring utf-8 encoding and LF line endings for cross-platform compatibility.
- ✅ Most modern IDEs, including Visual Studio, Visual Studio Code, and JetBrains Rider, automatically detect and apply .editorconfig settings.
- ✅ Use tools like dotnet-format or IDE-integrated formatters to apply .editorconfig rules automatically.
- ✅ Override rules for specific file types or folders as needed to handle Unity-specific files (e.g., .shader, .meta, .asmdef).

```csharp
# Root .editorconfig file
root = true

# General settings
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

# C# files
[*.cs]
indent_style = space
indent_size = 4
dotnet_style_braces_on_new_line_for_methods = true
dotnet_style_braces_on_new_line_for_types = true
dotnet_style_braces_on_new_line_for_control_blocks = true
dotnet_style_qualification_for_field = false
dotnet_style_qualification_for_property = false
dotnet_style_qualification_for_method = false
dotnet_style_qualification_for_event = false
csharp_new_line_before_open_brace = all
csharp_indent_case_contents = true
csharp_indent_switch_labels = true
csharp_prefer_braces = true
csharp_style_var_for_built_in_types = true
csharp_style_var_when_type_is_apparent = true
csharp_style_var_elsewhere = false
file_header_template = "File generated based on the Unity C# Style Guide."

# XML files (UXML)
[*.uxml]
indent_style = space
indent_size = 2
max_line_length = 120

# CSS files (USS)
[*.css]
indent_style = space
indent_size = 2
max_line_length = 120

# Unity meta files
[*.meta]
end_of_line = lf
insert_final_newline = true
```
Here is a quick explanation of some of the key settings:

***General Settings:***
- 📝 `charset = utf-8`: Ensures all files use UTF-8 encoding.
- 📝 `end_of_line = lf`: Enforces LF line endings for cross-platform compatibility.
- 📝 `insert_final_newline = true`: Adds a newline at the end of files for consistency.
- 📝 `trim_trailing_whitespace = true`: Removes unnecessary trailing whitespace.
***C# Settings:***

- 📝 `indent_style` = space and `indent_size` = 4: Enforces 4-space indentation for C# files.
- 📝 `dotnet_style_braces_on_new_line_*`: Configures Allman-style braces (opening braces on a new line).
- 📝 `csharp_style_var_*`: Configures var usage based on your style guide (e.g., use var for built-in types but not elsewhere).
- 📝 `file_header_template`: Adds a placeholder for file headers if needed.
***UXML Settings:***

- 📝 `indent_size` = 2: Enforces 2-space indentation for XML files.
- 📝 `max_line_length` = 120: Limits line length for better readability.

***USS Settings:***
- 📝 `indent_size` = 2: Enforces 2-space indentation for CSS/USS files.
- 📝 `max_line_length` = 120: Limits line length for better readability.


# Script examples (putting it all together)
This example focuses on a CharacterController and a AnimationController, demonstrating some of the concepts and conventions discussed in this style guide.

```csharp
// This script ties everything together, managing movement, health, and audio.
using UnityEngine;

namespace CoreSystems
{
    [RequireComponent(typeof(Rigidbody))]
    public class CharacterController : MonoBehaviour
    {
        [Header("Movement Settings")]
        [SerializeField, Tooltip("Movement speed of the character.")]
        private float m_moveSpeed = 5f;

        [Header("Jump Settings")]
        [SerializeField, Tooltip("Force applied when the character jumps.")]
        private float m_jumpForce = 7f;

        [Header("Ground Detection")]
        [SerializeField, Tooltip("Layer mask used to determine which surfaces count as ground.")]
        private LayerMask m_groundLayer;

        private Rigidbody m_rigidbody;

        // Event to notify animation changes
        public event System.Action<Vector3> MovementInputReceived;

        private void Awake()
        {
            // Cache the Rigidbody component
            m_rigidbody = GetComponent<Rigidbody>();
        }

        private void Update()
        {
            // Calculating movement input should go in Update
            HandleMovement();
        }

        private void FixedUpdate()
        {
            // Physics-related updates like jumping should go in FixedUpdate
            HandleJump();
        }

        private void HandleMovement()
        {
            float horizontal = Input.GetAxis("Horizontal");
            float vertical = Input.GetAxis("Vertical");

            Vector3 movement = new Vector3(horizontal, 0, vertical).normalized;

            // We use an early return to simplify the logic and reduce nesting.
            if (movement == Vector3.zero) return;

            // Move the character
            transform.Translate(movement * m_moveSpeed * Time.deltaTime, Space.World);

            // Notify listeners about movement input
            OnMovementInputReceived(movement);
        }

        private void OnMovementInputReceived(Vector3 movement)
        {
            MovementInputReceived?.Invoke(movement);
        }

        private void HandleJump()
        {
            if (Input.GetButtonDown("Jump") && IsGrounded())
            {
                m_rigidbody.AddForce(Vector3.up * m_jumpForce, ForceMode.Impulse);
            }
        }

        private bool IsGrounded()
        {
            // Make use of the visual tools in the Debug class for better debugging
            Debug.DrawRay(transform.position, Vector3.down * 1.1f, Color.red);

            // Simple ground check
            return Physics.Raycast(transform.position, Vector3.down, 1.1f, m_groundLayer);
        }
    }
}

// This script listens to the CharacterController's movement events and updates the animator accordingly.
using UnityEngine;

namespace CoreSystems
{
    // RequireComponent ensures necessary components are present so we don't need to check for null references later.
    [RequireComponent(typeof(Animator))]
    [RequireComponent(typeof(CharacterController))]
    public class AnimationController : MonoBehaviour
    {
        [Header("Animation Parameters")]
        [SerializeField, Tooltip("Animator parameter for movement speed.")]
        private string m_speedParam = "Speed";  // Use constant from centralized class

        [SerializeField, Tooltip("Layer mask for ground detection.")]
        private LayerMask m_groundLayer;

        private CharacterController m_characterController;

        private Animator m_animator;

        private void Awake()
        {
            // Cache the Animator component
            m_animator = GetComponent<Animator>();
            m_characterController = GetComponentInParent<CharacterController>();
        }

        private void OnEnable()
        {
            m_characterController.MovementInputReceived += HandleMovementInput;
        }

        private void OnDisable()
        {
            m_characterController.MovementInputReceived -= HandleMovementInput;
        }

        private void HandleMovementInput(Vector3 movement)
        {
            // Update the animator's speed parameter based on movement magnitude
            float speed = movement.magnitude;
            m_animator.SetFloat(m_speedParam, speed);
        }
    }
}

```
# Bonus tips

## Beginner tips: Avoid (too much) shorthand code
- ✅ It can be tempting to use shorthand syntax to make code more concise, but if you're new to programming or Unity, prioritizing clarity and readability is more important. As you gain experience, you can gradually use more advanced syntax.
- ✅ Prioritize code clarity and readability over brevity. If a shorthand syntax makes the code harder to understand, prefer the more explicit form.
- ✅ Use explicit types instead of var when the type is not immediately clear from the right-hand side of the assignment.
- ✅ Prefer traditional method syntax over lambda expressions for multi-line methods or when the logic is not immediately clear.
- ❌ Avoid using the ternary operator for complex conditions that reduce readability.

```csharp

    // Calculate the current movement speed based on input

    // Less clear version ternary operator
    m_currentMovementSpeed = m_forwardMovementInput.y * (m_isRunning ? m_runningSpeed : m_walkSpeed);

    // Clearer version with if-else
    if (m_isRunning)
    {
        m_currentMovementSpeed = m_forwardMovementInput.y * m_runningSpeed;
    }
    else
    {
        m_currentMovementSpeed = m_forwardMovementInput.y * m_walkSpeed;
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
