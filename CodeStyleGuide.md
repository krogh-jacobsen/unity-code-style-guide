# GitHub Copilot Instructions: Unity C# Style Guide & Naming

The following are instructions for GitHub Copilot to provide suggestions in terms of following a specific code style guide and naming principles for Unity 6 projects. While primarily written for Copilot as instructions, I also added some human-friendly explanations of the "why" for other users. Some of the guidance intentionally has a bit of repetition, saying the same thing in two different ways. The intent here is more context and examples improves Codepilots understanding of the intent.

## Inspiration

- The code style guide is a modified subset of Microsoft's Framework Design Guidelines here: [Microsoft Framework Design Guidelines](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/)
- Microsoft's general industry standard recommendation for C# practices applies when a rule is not specified here.
- A code style standard is a living document. It should be updated as the project evolves and the team grows.

## Key Principles

- The most important thing is to be consistent. Being consistent creates patterns and enables Copilot to make more accurate predictions.
- Simple is better than complicated.
- The code should strive to be clean and DRY.
- Favor readability over brevity.
- The goal is to make the code more readable, maintainable, and consistent.
- Doing things like naming the right way from the beginning will save time and effort later, particularly when debugging and extending functionality.
- As much as possible, stick to industry standards and conventions but be pragmatic.
- As a beginner, it's important to learn the rules before you break them. As you gain experience, you can make informed decisions about when to deviate.
- However, as a beginner, keep your guidelines light. The most important thing is to write code that works before making it "clean."

## Naming

- This one deserves a repeat: Favor readability over brevity.
- Don't use abbreviations. Clarity is more important than any time saved from omitting a few vowels.
- Use meaningful names. Don't abbreviate (unless it's math or commonly accepted). Your variable names should reveal their intent.
- Pick meaningful names from the beginning to minimize refactoring later.
- Variable names should be descriptive, clear, and unambiguous because they represent a thing or state.
- Use a noun when naming them except when the variable is of the type `bool`.
- Prefix Booleans with a verb to make their meaning more apparent. e.g., `isDead`, `isWalking`, `hasDamageMultiplier`.
- Favor what can be pronounced naturally and readability (e.g., `HorizontalAlignment` instead of `AlignmentHorizontal`).
- Make type names unambiguous across namespaces and problem domains by avoiding common terms or adding a prefix or a suffix (e.g., use `PhysicsSolver`, not `Solver`).

```csharp
// Examples of good naming
bool m_isPlayerDead;
bool m_hasWeapon;

// Examples of bad naming
bool m_dead;
bool m_weapon;
```

## Casing and Prefixes

- Specificity reduces guesswork.
- Use prefixes for private member variables (`m_`), constants (`k_`), and static variables (`s_`), so the name reveals more about the variable at a glance.
- Use Pascal case (e.g., `ExamplePlayerController`, `MaxHealth`, etc.) unless noted otherwise.
- Use camel case (e.g., `examplePlayerController`, `maxHealth`, etc.) for local/private variables and parameters.
- Avoid snake case, kebab case, Hungarian notation.

```csharp
// Member variable should have an m_ prefix
int m_playerHealth;

// Static variable should have an s_ prefix
static int s_instanceCount;

// Constant with k_ prefix
const float k_maxSpeed = 10f;
```

## Avoid Redundancy

- Drop redundant initializers (i.e., no `= 0` on the ints, `= null` on ref types, etc.) as they are initialized to 0 or null by default.
- Omit private access level modifiers consistently as these are redundant.
- Avoid redundant names: If your class is called `Player`, you don't need to create member variables called `PlayerScore` or `PlayerTarget`. Trim them down to `Score` or `Target`.

## Formatting

- This guide follows the Allman (opening curly braces on a new line) style braces.
- Readability is key. Try to keep lines short. Consider horizontal whitespace.
- You can also define a standard max line width in your style guide (some prefer less than 120 characters).
- Break a long line into smaller statements rather than letting it overflow.
- Use a single space before flow control conditions, e.g., `while (x == y)`.
- Avoid spaces inside brackets, e.g., `x = dataArray[index]`.

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

// Avoid
public void ProcessItems ( List<Item>items,int startIndex ) { for(int i=startIndex;i<items.Count;i++) { ProcessItem( items [ i ] ); } Debug.Log("Processing complete"); }
```

## Spacing

- Use a single space after a comma between function arguments, e.g., `CollectItem(myObject, 0, 1);`.
- Don't add a space after the parenthesis and function arguments, e.g., `CollectItem(myObject, 0, 1);`.
- Don't use spaces between a function name and parenthesis, e.g., `DropPowerUp(myPrefab, 0, 1);`.
- Use vertical spacing (extra blank line) for visual separation.
- Use one variable declaration per line in most cases. It's less compact but enhances readability.
- Use a single space before and after comparison operators, e.g., `if (x == y)`.

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

// Avoid
public void ProcessItems ( List<Item>items,int startIndex ) { for(int i=startIndex;i<items.Count;i++) { ProcessItem( items [ i ] ); } Debug.Log("Processing complete"); }
```

## Comments

- Always add comments when they can have a documenting value and give any extra additional context.
- That is when the code isn't self-explanatory and needs clarification beyond good naming revealing the intent.
- While we want to keep it simple and succinct, comments provide context, and it's better to give too much context than too little.
- However, if you need to add a comment to explain a convoluted tangle of logic, consider restructuring your code to be more obvious.
- Good naming can take out the guesswork. Consider renaming before commenting.
- Rather than simply answering "what" or "how," comments can fill in the gaps and tell us "why."
- Use the comment to keep the explanation next to the logic.
- Use a Tooltip instead of a comment for serialized fields if your fields in the Inspector need explanation.

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

- Rather than using Regions, think of them as a code smell indicating your class is too large and needs refactoring.
- Use XML tags in front of public methods or functions for output documentation/Intellisense.
- Avoid attributions, e.g., `// Created by`, `// Modified by`, etc. Use version control to track changes.
- Documenting the 'why' is far more important than the 'what' or 'how'.

## Class Organization

- Organize your class in the following order: Fields, Properties, Events, MonoBehaviour methods (Awake, Start, OnEnable, OnDisable, OnDestroy, etc.), public methods, private methods, other Classes.
- Use of #region is generally discouraged as it can hide complexity and make it harder to read the code.

## Using Lines

- Keep using lines at the top of your file.
- Remove unused lines.

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
```

## Namespaces

- Use namespaces to ensure that your classes, interfaces, enums, etc., won't conflict with existing ones from other namespaces or the global namespace.
- Use Pascal case, without special symbols or underscores.
- Create sub-namespaces with the dot (`.`) operator, e.g., `MyApplication.GameFlow`, `MyApplication.AI`, etc.
- Some recommend namespaces that reflect the folder structure of the project so it's logically grouped.

```csharp
namespace MyGame.Characters
{
    public class Player : MonoBehaviour
    {
        // Class implementation
    }
}
```

## Complete Code Examples

### Using Lines

- Keep using lines at the top of your file.
- Remove unused lines.

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
```

### Fields and Properties

- Use `m_` prefix.

```csharp
// Fields
int m_elapsedTimeInHours;       // Specify the unit used, prefix with m_ as private variable
int m_elapsedTimeInDays;        // Omit the private accessor as it's redundant
int m_elapsedTimeInSeconds;     // Don't abbreviate. Favor readability. 
[SerializeField] bool m_isPlayerDead;       // Prefix Booleans with a verb like "is" to make their meaning apparent
static int s_sharedCount;
const int k_maxCount = 100;
```

### Properties

```csharp
// Properties
int m_maxHealth;

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

### Methods

- Use verb names for method naming.
- Action-Oriented: Methods represent actions or behaviors, so using verbs makes their purpose clear.
- Verb-based names make code more readable and self-explanatory.
- Use **verb-based names** for methods to clearly indicate the action being performed.
- Avoid noun-based names for methods unless they are factory methods or event handlers.
- Boolean methods should ask a question, starting with verbs like `Is`, `Has`, or `Can`.
- Avoid confusion: Names like `Walking()` or `Rotating()` imply a continuous state or property rather than an action.
- These are better suited for variables or properties (e.g., `isWalking`, `isRotating`).

```csharp
// Good examples
public void SetInitialPosition(float x, float y, float z);
public void SaveGame();
public bool IsPlayerAlive();
public Player CreatePlayer();
Walk(); // Indicates an action being performed

// Avoid
Walking(); // Avoid 'ing as that implies a continuous state or property rather than an action. 

// Methods with verb names
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

```csharp
// Event declarations
public event Action OpeningDoor;
public event Action DoorOpened;
public event Action<int> PointsScored;
public event Action<CustomEventArgs> ThingHappened;

// Event raising methods
public void OnDoorOpened()
{
    DoorOpened?.Invoke();
}

public void OnPointsScored(int points)
{
    PointsScored?.Invoke(points);
}

// Custom EventArgs
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

### Enums

- Use enums when an object or action can only have one value at a time.
- Use Pascal case for enum names and values.
- Use a singular noun for the enum name as it represents a single value from a set of possible values.
- They should have no prefix or suffix.
- You can place public enums outside of a class to make them global.

```csharp
// Simple enum
public enum Direction
{
    North,
    South,
    East,
    West
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

### Interfaces

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
