> This README is intended for human readers and explains the rationale behind the choices in the style guide.

# The Unity C# Style Guide Rationale

This repo is a practical Unity C# style guide designed to work well with LLM assistants. It combines standard C# and Unity guidance with a few opinionated conventions that are easy to adapt.

## Check out the original guide

This version is inspired by the [Unity C# style guide for Unity 6](https://unity.com/resources/c-sharp-style-guide-unity-6), which I helped create and later update. The companion ebook, [Level up your code with design patterns and SOLID](https://unity.com/resources/design-patterns-solid-ebook), is also relevant for the design patterns material in this repo.

## Why this version differs

The original guide was useful, but many people wanted more concrete examples and clearer explanations. Others wanted to use AI tools to follow the guide consistently, but were unsure how to make that work without extra prompting and setup.

This version is intended to be more LLM-friendly, more approachable, and easier to adapt. The instruction files are written for machines, but they also include short explanations of why each rule exists so you can follow the reasoning as you read.

This is still grounded in standard C# and Unity practice, while also including a few opinionated preferences. Those are clearly marked with `[opinion]` so you can decide what to keep, remove, or change.

## A living document

Any style guide should evolve over time. This one is no exception. Some choices are based on industry conventions, while others reflect readability and teaching-first decisions. That's intentional: a style guide should support the way your team actually works.

## There is no single "correct" way

The goal here is not to claim that one format is universally better than every alternative. Instead, the aim is to reduce ambiguity and make collaboration easier.

A good style guide is one that works for your project. That can mean different things for a solo developer, a beginner learning the craft, or a larger team working on a more complex codebase. This repo is meant to be a strong starting point: adapt it, tweak it, and make it your own.


## What's opinionated here

Most of this guide is standard C# and Unity practice. The points below are the ones I personally prefer and would discuss before adopting them wholesale. Fork them, change them, argue with them:

| Convention | My choice | Common alternative |
|---|---|---|
| Private field prefix | `m_camelCase` | `_camelCase` or bare `camelCase` |
| Constant prefix | `k_camelCase` for private consts | `PascalCase` or `SCREAMING_CASE` |
| Static field prefix | `s_camelCase` | no prefix |
| Brace style | Allman (brace on its own line) | K&R (brace on the same line) |
| Line width | 120–140 characters | 80, 100, or unlimited |
| `private` modifier | Always written | Omitted |
| ScriptableObject naming | `DataSO` suffix | no suffix |
| Method verbs | `Handle` for event callbacks, `Process` for game-flow logic | `On`, or no distinction |

Everything else — PascalCase types and methods, `is`/`has`/`can` booleans, `I`-prefixed interfaces, caching in `Awake`, and unsubscribing in `OnDisable` — is standard practice rather than preference.

---

# Why these rules exist

This section explains the intent behind the conventions. The instruction files stay concise so they are efficient to feed to a model; this section is where the deeper reasoning lives.

## Balancing succinctness vs. verbosity

Code should be readable and explicit over clever or overly compressed. Clear names and deliberate structure usually make code easier to maintain, especially in larger teams or when working with AI tools that need strong context. The tradeoff is that some names are a bit longer, but that extra precision often helps understanding instead of hurting it.

A standard line width also helps with consistency. Many teams use 120–140 characters as a practical middle ground: wide enough for readable code, narrow enough to avoid awkward wrapping.

## General naming

Names should be meaningful, descriptive, and easy to discuss in conversation. Favor clarity over cleverness and avoid ambiguous names when a more specific one would help. Boolean names should read like predicates, such as `isDead`, `hasWeapon`, and `canJump`.

When an identifier could be ambiguous in a larger system, add enough context to clarify its purpose. For example, `PhysicsSolver` is usually clearer than a generic `Solver`.

## Comments and custom attributes for context and intent

Comments should explain intent or context that is not obvious from the code itself. They should not simply restate what the code already does. If a variable or method name can make intent clear, prefer that over adding commentary.

Before adding comments, first consider whether clearer variable or method names would make the intent self-evident. Good naming often removes the need for commentary altogether. But where the reasoning genuinely isn't visible in the code — a workaround for a platform bug, a magic threshold someone tuned by hand — write it down. That context improves maintainability and also enables better automated code generation.

For serialized fields, prefer Inspector-facing attributes where appropriate. A `[Tooltip]` is often more useful than a comment when a field needs explanation in the Inspector, and `[SerializeField]` can expose values that benefit from runtime debugging or tuning. Use attributes such as `[Range]`, `[Header]`, and `[ContextMenu]` to improve clarity and usability for designers and developers interacting with the Inspector. Keep one field per line and include units directly in field names when relevant (for example, `m_speedInMetersPerSecond`) to avoid ambiguity.

Avoid attribution comments like `// Created by…`; version control already provides accurate ownership and history. When a component has hard dependencies, use `[RequireComponent(typeof(OtherComponent))]` to enforce those relationships at edit time, ensuring required components are always present and eliminating the need for defensive null checks later.

## Follow OOP principles

Favor composition over inheritance, leaning toward interfaces and component-based designs rather than deep class hierarchies. As a default, keep fields private to ensure proper encapsulation and adherence to core object-oriented principles. Expose behavior through methods and controlled access points instead of shared state.

To reduce guesswork and make intent obvious at a glance, use consistent naming prefixes: `m_` for private member variables, `k_` for constants, and `s_` for static variables. This added specificity improves readability and helps communicate how a value is meant to be used.

Keep MonoBehaviours focused on a single responsibility. If a class begins to grow too large or complex, consider decomposing it into smaller components or moving data and configuration into ScriptableObjects. Use properties for simple state access or lightweight state changes, and methods for actions or operations such as input handling and event-driven behavior. Method names should describe intent and behavior clearly — for example, prefer `ApplyDamage(int amount)` over `SetHealth(int amount)` to reflect what the operation actually does.

Avoid magic numbers and hardcoded strings. Replace inline values (such as a literal `5f` used for speed) with named constants or serialized fields to improve clarity, flexibility, and ease of tuning.

Finally, while "method" and "function" are often used interchangeably in casual conversation, "method" is the more accurate term in C#, as it refers to functions that belong to a class and operate on its state.

## Avoid redundancy without sacrificing clarity

Avoid redundant initializers for fields and variables. Value types such as `int` and `float` are initialized to `0` by default, and reference types to `null`, so explicitly assigning these values adds noise without providing value. Similarly, although the `private` access modifier is technically redundant, it should still be specified explicitly. Microsoft's guidelines recommend doing so to make intent clear, improve readability, and avoid ambiguity — especially for less experienced readers.

Be mindful of redundant naming. When a class already provides context, repeating that context in member names adds unnecessary verbosity. For example, within a `Player` class, prefer `Score` or `Target` over `PlayerScore` or `PlayerTarget`. The surrounding scope already communicates ownership and intent.

For public APIs, consider using XML documentation comments to improve output documentation and IntelliSense support. These comments provide immediate, structured context to consumers of the code without requiring them to inspect the implementation.

Use `#region` directives sparingly. While they can occasionally help with organization, they often hide complexity and may indicate that a class has grown too large and should be refactored instead. One valid use case is grouping clearly delineated code that is invoked externally, such as Animation Event handlers or Input Event callbacks, so those entry points are visually separated from the rest of the implementation.

## Beginner tips: avoid overusing shorthand syntax

When you're new to programming or Unity, it can be tempting to use shorthand syntax to make code look more concise. However, clarity and readability should take priority over brevity, especially while you're still building familiarity with the language and engine. As your experience grows, you'll naturally become more comfortable recognizing and applying more compact syntax where it genuinely improves readability.

Prefer explicit, easy-to-follow code whenever shorthand would obscure intent. For example, use explicit types instead of `var` when the assigned type is not immediately obvious from the right-hand side, and favor traditional method definitions over lambda expressions for multi-line logic or non-trivial behavior. Similarly, avoid using the ternary operator for complex conditions, as it can quickly reduce readability and make intent harder to understand.

In short, write code that is easy to read first, and concise second. Readable code is easier to debug, easier to maintain, and easier for others — including your future self — to understand.

```csharp
// Calculate the current movement speed based on input

// Less clear version with a ternary operator
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

## Using `.editorconfig` to enforce formatting rules

Use an `.editorconfig` file to define and enforce consistent formatting rules across the project. This helps keep your editor, formatters, and AI tools aligned with the same conventions. 
I've included an example in the [EditorConfig](EditorConfig/) folder.
The important part is making sure the file actually exists in your repo and is picked up by your editor. The README example is useful for reference, but the effective enforcement happens when it is placed at the repository root as a real `.editorconfig` file.


