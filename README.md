# A Unity C# Style Guide for LLMs

While there's no single "correct" way to format Unity C# code, agreeing on a consistent style makes it much easier to build a clean, readable, and scalable codebase as a team. It also makes a real
difference to the AI coding assistants most of us now have open all day: given clear conventions, they produce code that looks like the rest of your project instead of a generic approximation of it.

That said, a style guide is only valuable if it's actually put into practice. This repo is my attempt at making that easy. It's a set of instruction files you can drop into a new Unity project so your assistant follows your conventions from the first script.

## Check out the original ebook

This code style part of this repo is inspired by the [Unity C# style guide for Unity 6](https://unity.com/resources/c-sharp-style-guide-unity-6), which I
helped update earlier in 2025. If you want the polished, illustrated version of the reasoning behind a lot of these conventions, start there. The design patterns material here draws on the free companion ebook,
[Level up your code with design patterns and SOLID](https://unity.com/resources/design-patterns-solid-ebook).

## How this repo is organised

Three tiers, in decreasing order of what is opinionated and you can tailor to your preferences to general industry best practice guidelines:

| Tier | What it is | Should you change it? |
|---|---|---|
| [`AGENTS.md`](AGENTS.md) | Compact digest of every rule. One file, ~260 lines. | Copy it, then edit the setup block |
| [`UnityStyleGuide.md`](UnityStyleGuide.md) | **My opinionated preferences** — naming, prefixes, formatting | Freely. It's taste, and it says which bits are |
| [`UnityReferenceGuides/`](UnityReferenceGuides/) | **General best practice** — performance, patterns, UI, memory, testing | Only if you know why (or if I missed something) |
| [`UnityCustomInstructions/`](UnityCustomInstructions/) | **Your project's specifics** — Unity version, pipeline, presets | Always. That's the point |

Rules that are genuinely my preference rather than industry consensus are marked `[opinion]` in
`AGENTS.md` and listed in a table at the top of `UnityStyleGuide.md`, so you know exactly what you're
signing up for.

```
├── AGENTS.md                     ← paste this into your assistant
├── UnityStyleGuide.md            ← subjective: my preferences
├── UnityReferenceGuides/         ← general best practice
│   ├── UnityPerformanceOptimizationInstructions.md
│   ├── UnityAssetsAndMemoryInstructions.md
│   ├── UnityDesignPatternsInstructions.md
│   ├── UnityScenesAndLifecycleInstructions.md
│   ├── UnityUIToolkitInstructions.md
│   ├── UnityUGUIInstructions.md
│   ├── UnityInputSystemInstructions.md
│   ├── UnityPhysicsInstructions.md
│   ├── UnityAnimationInstructions.md
│   ├── UnityAudioInstructions.md
│   ├── UnityAssemblyDefinitionsInstructions.md
│   ├── UnityTestingInstructions.md
│   ├── UnityEditorToolingInstructions.md
│   └── UnityDebuggingInstructions.md
├── UnityCustomInstructions/      ← edit these for your project
│   ├── UnityTechStack.md
│   └── UnityProjectConfiguration.md
└── Skills/
    └── unity-guide-audit/        ← checks a project against the guides
```

## Using it with your assistant

The short version: put `AGENTS.md` where your tool looks for instructions.

| Tool | Where it goes |
|---|---|
| **Claude Code** | `CLAUDE.md` in the repo root, or reference it with `@AGENTS.md` |
| **OpenAI Codex** | `AGENTS.md` in the repo root — it's already the right filename |
| **GitHub Copilot** | `.github/copilot-instructions.md` |
| **Cursor** | `.cursorrules`, or a file under `.cursor/rules/` |
| **JetBrains AI / Junie** | `.junie/guidelines.md` |

Copy the whole repo in if you want the deep references too — the guides cross-link each other, and
`AGENTS.md` points at them for detail it deliberately leaves out.

Then **edit [`UnityCustomInstructions/UnityTechStack.md`](UnityCustomInstructions/UnityTechStack.md)
first**. It declares your Unity version, render pipeline, input system and UI system. Get that wrong
and your assistant will confidently write uGUI code for a UI Toolkit project.

There's also a `Skills/unity-guide-audit/` skill that audits an existing project against these
guides — naming, hot-path violations, event leaks, project settings — and reports what drifted.

## Why this version is different from the original guide

The original guide received positive feedback, but it also became clear that many users wanted more concrete examples and explanations for certain topics. Others, like myself, wanted to use AI tools to help follow the guide but weren't sure how to get the desired results most effectively without
extensive prompting. Luckily, most modern IDEs offer ways to configure assistants so they adhere to a specific style guide.

Previously you had to go through a few extra configuration steps to get this working in your own workflows. Now most tools detect the file automatically. The process is very similar across LLMs and IDEs.

While this updated guide is still based on the original C# style guide and draws heavily from the
[Microsoft Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/),
this version is intended to be more LLM-friendly, pragmatic, and beginner-friendly. It also includes
some of my opinionated preferences which you can of course disregard or adapt to yours.

The instruction files are written for machines, but they also include short explanations of why certain choices are made. The intent is that this can serve as an educational resource too. Some points are repeated or phrased in different ways to give the model more examples and context. It
might feel a bit verbose, but that helps reinforce the intent behind each rule so it can make more informed decisions and so you can follow along in the reasoning.

## A living document

Any code style guide should evolve over time and I'll try not to make this one an exception :-) I'm sure there are things I've missed, and I'm sure you'll have suggestions that can make it even better. So let me know what works for you and what could be improved.

## There is "no right way"
The goal here isn't to claim there's only one "correct" way to write code or to push too many personal preferences. I'm a fan of following industry standards, but I also work in education and so the making things approachable and understandable is more important than say performance, if I had two prioritize one of the two 

Ultimately, a good style guide is one that works for your needs. Those needs can vary a lot depending on whether you're a solo developer or part of a larger team, whether you're a beginner looking to learn, who values simplicity and readability, or a senior engineer contributing to a large scale project codebase.

Use this guide as inspiration: adapt it, tweak it, or adopt it for your Unity projects however you like.

Happy coding!

---

# The rationale behind the rules

This section explains the *why* behind the conventions. The instruction files stay terse so they're efficient to feed to a model. So this is where the reasoning lives if you want to better understand the "why". 

## Balancing succinctness vs. verbosity

Prioritize readability and clarity over cleverness. Code should favor explicitness and intent-revealing names, even if that means being slightly more verbose. Additional context is
generally better than less, but anything that does not add meaningful value should be trimmed. Avoid
abbreviations unless they are well-established, industry-standard math terms, and ensure that names
remain clear and self-describing. While succinctness is desirable, it should never come at the cost
of removing essential context needed to understand intent. To support consistent readability, define
a standard maximum line width — many teams prefer limits in the 120–140 character range.

## General naming

Use meaningful, descriptive names that clearly convey purpose. Names should be easy to read,
pronounce, and discuss in conversation, favoring natural language constructs such as
`HorizontalAlignment` rather than awkward or inverted phrasing. Boolean names should read as
predicates by using verb prefixes like is, has, or can (for example, `isDead`, `hasWeapon`, or
`canJump`). When a type name could be ambiguous across different namespaces or domains, add
sufficient context to make its responsibility immediately clear, such as `PhysicsSolver` instead of a
generic `Solver`.

## Use comments & custom attributes for documenting context & intent

Comments should add value by explaining intent or context that is not immediately obvious from the
code itself, rather than restating what the code already does. Keep them simple and succinct,
focusing on the why behind a decision rather than the what.

Before adding comments, first consider whether clearer variable or method names would make the
intent self-evident. Good naming often removes the need for commentary altogether. But where the
reasoning genuinely isn't visible in the code — a workaround for a platform bug, a magic threshold
someone tuned by hand — write it down. That context improves maintainability and also enables better
automated code generation.

For serialized fields, prefer Inspector-facing attributes where appropriate. A `[Tooltip]` is often
more useful than a comment when a field needs explanation in the Inspector, and `[SerializeField]`
can expose values that benefit from runtime debugging or tuning. Use attributes such as `[Range]`,
`[Header]`, and `[ContextMenu]` to improve clarity and usability for designers and developers
interacting with the Inspector. Keep one field per line and include units directly in field names
when relevant (for example, `m_speedInMetersPerSecond`) to avoid ambiguity.

Avoid attribution comments like `// Created by…`; version control already provides accurate ownership
and history. When a component has hard dependencies, use `[RequireComponent(typeof(OtherComponent))]`
to enforce those relationships at edit time, ensuring required components are always present and
eliminating the need for defensive null checks later.

## Follow OOP principles

Favor composition over inheritance, leaning toward interfaces and component-based designs rather
than deep class hierarchies. As a default, keep fields private to ensure proper encapsulation and
adherence to core object-oriented principles. Expose behavior through methods and controlled access
points instead of shared state.

To reduce guesswork and make intent obvious at a glance, use consistent naming prefixes: `m_` for
private member variables, `k_` for constants, and `s_` for static variables. This added specificity
improves readability and helps communicate how a value is meant to be used.

Keep MonoBehaviours focused on a single responsibility. If a class begins to grow too large or
complex, consider decomposing it into smaller components or moving data and configuration into
ScriptableObjects. Use properties for simple state access or lightweight state changes, and methods
for actions or operations such as input handling and event-driven behavior. Method names should
describe intent and behavior clearly — for example, prefer `ApplyDamage(int amount)` over
`SetHealth(int amount)` to reflect what the operation actually does.

Avoid magic numbers and hardcoded strings. Replace inline values (such as a literal `5f` used for
speed) with named constants or serialized fields to improve clarity, flexibility, and ease of tuning.

Finally, while "method" and "function" are often used interchangeably in casual conversation,
"method" is the more accurate term in C#, as it refers to functions that belong to a class and
operate on its state.

## Avoid redundancy without sacrificing clarity

Avoid redundant initializers for fields and variables. Value types such as `int` and `float` are
initialized to `0` by default, and reference types to `null`, so explicitly assigning these values
adds noise without providing value. Similarly, although the `private` access modifier is technically
redundant, it should still be specified explicitly. Microsoft's guidelines recommend doing so to make
intent clear, improve readability, and avoid ambiguity — especially for less experienced readers.

Be mindful of redundant naming. When a class already provides context, repeating that context in
member names adds unnecessary verbosity. For example, within a `Player` class, prefer `Score` or
`Target` over `PlayerScore` or `PlayerTarget`. The surrounding scope already communicates ownership
and intent.

For public APIs, consider using XML documentation comments to improve output documentation and
IntelliSense support. These comments provide immediate, structured context to consumers of the code
without requiring them to inspect the implementation.

Use `#region` directives sparingly. While they can occasionally help with organization, they often
hide complexity and may indicate that a class has grown too large and should be refactored instead.
One valid use case is grouping clearly delineated code that is invoked externally, such as Animation
Event handlers or Input Event callbacks, so those entry points are visually separated from the rest
of the implementation.

## Beginner tips: avoid overusing shorthand syntax

When you're new to programming or Unity, it can be tempting to use shorthand syntax to make code look
more concise. However, clarity and readability should take priority over brevity, especially while
you're still building familiarity with the language and engine. As your experience grows, you'll
naturally become more comfortable recognizing and applying more compact syntax where it genuinely
improves readability.

Prefer explicit, easy-to-follow code whenever shorthand would obscure intent. For example, use
explicit types instead of `var` when the assigned type is not immediately obvious from the
right-hand side, and favor traditional method definitions over lambda expressions for multi-line
logic or non-trivial behavior. Similarly, avoid using the ternary operator for complex conditions, as
it can quickly reduce readability and make intent harder to understand.

In short, write code that is easy to read first, and concise second. Readable code is easier to
debug, easier to maintain, and easier for others — including your future self — to understand.

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

## Using .editorconfig to enforce formatting rules

Use an `.editorconfig` file to define and enforce consistent formatting rules across the entire
project. This includes conventions for indentation, spacing, line endings, brace style (for example,
Allman braces), and maximum line length. Where applicable, include Unity-specific settings such as
UTF-8 encoding and LF line endings to ensure reliable cross-platform behavior.

Most modern IDEs — including Visual Studio, Visual Studio Code, and JetBrains Rider — automatically
detect and apply `.editorconfig` settings, making it an effective way to keep formatting consistent
without relying on individual editor preferences. Formatting rules can also be applied automatically
using tools like `dotnet format` or IDE-integrated formatters, ensuring compliance with minimal
manual effort.

When necessary, override or specialize rules for specific file types or folders to accommodate
Unity-specific assets. Place the `.editorconfig` file at the root of the repository so it applies
uniformly to the entire project.

```ini
# .editorconfig
# Enforce Unity C# style (Rider / Roslyn / dotnet-format compatible)
root = true

# Global defaults
[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 140

# Binary and generated assets - don't rewrite these
[*.{png,jpg,jpeg,gif,ico,exe,dll,so,zip}]
trim_trailing_whitespace = false
insert_final_newline = false

# Unity YAML assets - preserve exactly as Unity writes them
[*.{unity,asset,prefab,mat,anim,controller,meta}]
trim_trailing_whitespace = false
insert_final_newline = false

# C# files
[*.cs]
indent_style = space
indent_size = 4

# Allman brace style
csharp_new_line_before_open_brace = all
csharp_new_line_before_else = true
csharp_new_line_before_catch = true
csharp_new_line_before_finally = true

# Spacing rules
csharp_space_after_keywords_in_control_flow_statements = true
csharp_space_between_method_call_name_and_open_parenthesis = false
csharp_space_between_method_declaration_name_and_open_parenthesis = false
csharp_space_after_comma = true
csharp_space_around_binary_operators = before_and_after
csharp_space_within_square_brackets = false

# var preferences - explicit types unless the type is already obvious
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = false:suggestion

# Prefer expression-bodied members where concise (optional)
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_properties = when_on_single_line:suggestion

# Naming conventions
# Symbol groups - order matters; the first matching rule wins
dotnet_naming_symbols.const_fields.applicable_kinds = field
dotnet_naming_symbols.const_fields.applicable_accessibilities = private, protected, private_protected
dotnet_naming_symbols.const_fields.required_modifiers = const

dotnet_naming_symbols.static_fields.applicable_kinds = field
dotnet_naming_symbols.static_fields.applicable_accessibilities = private, protected, private_protected
dotnet_naming_symbols.static_fields.required_modifiers = static

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private, protected, private_protected

dotnet_naming_symbols.public_const_fields.applicable_kinds = field
dotnet_naming_symbols.public_const_fields.applicable_accessibilities = public, internal
dotnet_naming_symbols.public_const_fields.required_modifiers = const

dotnet_naming_symbols.properties.applicable_kinds = property
dotnet_naming_symbols.properties.applicable_accessibilities = *

dotnet_naming_symbols.interfaces.applicable_kinds = interface

# Styles - note all three prefixes use camelCase after the prefix
dotnet_naming_style.m_prefix_style.required_prefix = m_
dotnet_naming_style.m_prefix_style.capitalization = camel_case

dotnet_naming_style.k_prefix_style.required_prefix = k_
dotnet_naming_style.k_prefix_style.capitalization = camel_case

dotnet_naming_style.s_prefix_style.required_prefix = s_
dotnet_naming_style.s_prefix_style.capitalization = camel_case

dotnet_naming_style.pascal_case_style.capitalization = pascal_case

dotnet_naming_style.i_prefix_style.required_prefix = I
dotnet_naming_style.i_prefix_style.capitalization = pascal_case

# Rules - const before static before plain private, so the right prefix wins
dotnet_naming_rule.const_fields_should_have_k_prefix.symbols = const_fields
dotnet_naming_rule.const_fields_should_have_k_prefix.style = k_prefix_style
dotnet_naming_rule.const_fields_should_have_k_prefix.severity = suggestion

dotnet_naming_rule.static_fields_should_have_s_prefix.symbols = static_fields
dotnet_naming_rule.static_fields_should_have_s_prefix.style = s_prefix_style
dotnet_naming_rule.static_fields_should_have_s_prefix.severity = suggestion

dotnet_naming_rule.private_fields_should_have_m_prefix.symbols = private_fields
dotnet_naming_rule.private_fields_should_have_m_prefix.style = m_prefix_style
dotnet_naming_rule.private_fields_should_have_m_prefix.severity = suggestion

dotnet_naming_rule.public_consts_should_be_pascal_case.symbols = public_const_fields
dotnet_naming_rule.public_consts_should_be_pascal_case.style = pascal_case_style
dotnet_naming_rule.public_consts_should_be_pascal_case.severity = suggestion

dotnet_naming_rule.properties_should_be_pascal_case.symbols = properties
dotnet_naming_rule.properties_should_be_pascal_case.style = pascal_case_style
dotnet_naming_rule.properties_should_be_pascal_case.severity = suggestion

dotnet_naming_rule.interfaces_should_have_i_prefix.symbols = interfaces
dotnet_naming_rule.interfaces_should_have_i_prefix.style = i_prefix_style
dotnet_naming_rule.interfaces_should_have_i_prefix.severity = suggestion

# Analyzer severities (tunable)
dotnet_analyzer_diagnostic.category-Style.severity = suggestion

# File headers (optional template, uncomment and edit if desired)
# file_header_template = Copyright (c) %year% YourCompany. All rights reserved.

# UXML / XML files (UI Toolkit)
[*.uxml]
indent_style = space
indent_size = 2
max_line_length = 120

[*.xml]
indent_style = space
indent_size = 2

# USS / CSS-like files
[*.uss]
indent_style = space
indent_size = 2
max_line_length = 120
```

A quick explanation of the key settings:

**General**

- 📝 `charset = utf-8` — ensures all files use UTF-8 encoding.
- 📝 `end_of_line = lf` — enforces LF line endings for cross-platform compatibility.
- 📝 `insert_final_newline = true` — adds a newline at the end of files for consistency.
- 📝 `trim_trailing_whitespace = true` — removes unnecessary trailing whitespace.
- 📝 The `[*.{unity,asset,prefab,…}]` block leaves Unity's YAML files alone. Reformatting them
  creates enormous, meaningless diffs and can confuse the asset pipeline.

**C#**

- 📝 `indent_style = space`, `indent_size = 4` — four-space indentation.
- 📝 `csharp_new_line_before_open_brace = all` — this is the key that produces Allman braces.
- 📝 `csharp_style_var_*` — `var` for built-in types and where the type is already apparent on the
  right-hand side, explicit types everywhere else.
- 📝 The `dotnet_naming_*` rules enforce `m_`/`k_`/`s_` with camelCase after the prefix, PascalCase
  properties, and the `I` prefix on interfaces. **Rule order matters** — const and static are
  declared before plain private fields so a `private static` field gets `s_`, not `m_`.
- 📝 `public const` on a static lookup class is treated as API surface and stays PascalCase, which is
  why `Tags.Player` doesn't need a prefix.
- 📝 `file_header_template` — a placeholder for file headers, commented out by default.

**UXML / USS**

- 📝 `indent_size = 2` and `max_line_length = 120` for both, matching typical markup conventions.

> ⚠️ `max_line_length` is honoured by Rider and most editors, but `dotnet format` does not enforce it.
> Treat it as guidance rather than something CI can check.
