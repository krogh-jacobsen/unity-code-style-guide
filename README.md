# Implementing a Unity C# Style Guide as GitHub Copilot Instructions

Earlier in 2025 I helped update the [Unity C# Code Style guide for Unity 6](https://unity.com/resources/c-sharp-style-guide-unity-6). While there’s no single “correct” way to format Unity C# code, agreeing on a consistent style makes it much easier to build a clean, readable, and scalable codebase as a team. 
That said, a style guide is only valuable if it’s actually put into practice.

## Implementing the style guide into your workflows
Since then, I’ve been experimenting with adapting the original style guide into my own and how to apply it in my own setup (using Mac with VS Code or Rider combined with GitHub Copilot testing out different models). 
Copilot is incredibly helpful, but if you don’t give it clear instructions about your preferences, it will often default to generic suggestions. Fortunately, there are several ways to provide custom instructions so Copilot follows your style. 
One of the most effective is creating a .md instructions file.

## Why this version is different from the original guide
The original guide received positive feedback, but it also became clear that many users wanted more concrete examples and explanations for certain topics. Others, like myself, wanted to use AI tools like GitHub Copilot to help follow the guide but weren’t sure how to get the desired results most effectively without extensive prompting. 
Luckily, most modern IDEs offer ways to configure Copilot so it adheres to a specific style guide.

While this updated guide is still based on the original C# style guide and draws heavily from the
[Microsoft Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/), this version is intended to be more LLM‑friendly, pragmatic, and beginner‑friendly. It also includes some of my opinionated preferences which you can of course disregard or adapt to yours.

While the copilot-instructions.md is created for Copilot, this document also includes short explanations about why certain choices are made. 
Intent being that perhaps this resource can also serve as an educational resource that can inspire. 
Some points are repeated or phrased in different ways to give Copilot more examples and context. 
It might feel a bit verbose, but that helps reinforce the intent behind each rule so Copilot can make more informed decisions and you can follow along in the reasoning.

## How do I create my own instructions in Visual Code?
There are plenty of great articles on this and it has changed quite a few times, so I’ll just give you a quick summary. The short answer: create a copilot-instructions.md file in the root of your repository for GitHub Copilot to reference. Then simply add the instructions in .md (Markdown Documentation) formatting. 
Feel free to copy and paste whatever parts you find useful and tweak the rest from my example.

Previously, you had to go through a few extra configuration steps to get this working, but as of my latest version (November 2025), Copilot detects it automatically. The process is very similar for most LLMs and IDEs you might be using.

## A living document
Any code style guide should evolve over time and I’ll try not to make this one an exception :-)  I’m sure there are things I’ve missed, and I’m sure you’ll have suggestions that can make it even better. So let me know what works for you and what could be improved.

The goal here isn’t to claim there’s only one “correct” way to write code or to push too many personal preferences. I’m a fan of following industry standards, but I also work in education and ultimately, a good style guide is one that works for your needs. Those needs can vary a lot depending on whether you’re a solo developer or part of a larger team, whether you’re a beginner looking to learn, who values simplicity and readability, or senior engineer contributing to a large scale project codebase.

Use this guide as inspiration: adapt it, tweak it, or adopt it for your Unity projects however you like.

Happy coding!

---
# Unity C# Style Guide rationale explained
<instructions>

This document explains the *why* behind the rules in `.github/copilot-instructions.md`. Intent is to keep Copilot instructions more clear and then
use this guide as the in-depth and educational reference for the rationale behind the choices.

### Balancing Succinctness vs. Verbosity
Prioritize readability and clarity over cleverness. 
Code should favor explicitness and intent-revealing names, even if that means being slightly more verbose. 
Additional context is generally better than less, but anything that does not add meaningful value should be trimmed. 
Avoid abbreviations unless they are well-established, industry-standard math terms, and ensure that names remain clear and self-describing. 
While succinctness is desirable, it should never come at the cost of removing essential context needed to understand intent. 
To support consistent readability, define a standard maximum line width in the style guide—many teams prefer limits in the 120–140 character range. 

### General Naming
Use meaningful, descriptive names that clearly convey purpose. 
Names should be easy to read, pronounce, and discuss in conversation, favoring natural language constructs such as HorizontalAlignment rather than awkward or inverted phrasing. 
Boolean names should read as predicates by using verb prefixes like is, has, or can (for example, isDead, hasWeapon, or canJump).
When a type name could be ambiguous across different namespaces or domains, add sufficient context to make its responsibility immediately clear, such as PhysicsSolver instead of a generic Solver.

### Use Comments & Custom Attributes For Documenting Context & Intent
Comments should add value by explaining intent or context that is not immediately obvious from the code itself, rather than restating what the code already does. 
When in doubt, err on the side of providing more context rather than less—clear context improves maintainability and also enables better automated code generation. 

Keep comments simple and succinct, focusing on the why behind a decision rather than the what. 
Before adding comments, first consider whether clearer variable or method names would make the intent self-evident. 
Good naming often removes the need for commentary altogether.

For serialized fields, prefer using Inspector-facing attributes where appropriate. 
A [Tooltip] is often more useful than a comment when a field needs explanation in the Inspector, and [SerializeField] can be used to expose values that benefit from runtime debugging or tuning. 

Use attributes such as [Range], [Header], and [ContextMenu] to improve clarity and usability for designers and developers interacting with the Inspector. 
Keep one field per line and include units directly in field names when relevant (for example, m_speedInMetersPerSecond) to avoid ambiguity.

Avoid attribution comments like // Created by…; version control already provides accurate ownership and history. 
When a component has hard dependencies, use [RequireComponent(typeof(OtherComponent))] to enforce those relationships at edit time, ensuring required components are always present and eliminating the need for defensive null checks later.

### Follow OOP Principles
Favor composition over inheritance, leaning toward interfaces and component-based designs rather than deep class hierarchies. 
As a default, keep fields private to ensure proper encapsulation and adherence to core object-oriented principles. 
Expose behavior through methods and controlled access points instead of shared state. T
o reduce guesswork and make intent obvious at a glance, use consistent naming prefixes: m_ for private member variables, k_ for constants, and s_ for static variables. 
This added specificity improves readability and helps communicate how a value is meant to be used.

Keep MonoBehaviours focused on a single responsibility. 
If a class begins to grow too large or complex, consider decomposing it into smaller components or moving data and configuration into ScriptableObjects. 
Use properties for simple state access or lightweight state changes, and methods for actions or operations such as input handling and event-driven behavior. 
Method names should describe intent and behavior clearly—for example, prefer ApplyDamage(int amount) over SetHealth(int amount) to reflect what the operation actually does.

Avoid magic numbers and hardcoded strings. 
Replace inline values (such as a literal 5f used for speed) with named constants or serialized fields to improve clarity, flexibility, and ease of tuning. 

Finally, while “method” and “function” are often used interchangeably in casual conversation, “method” is the more accurate term in C#, as it refers to functions that belong to a class and operate on its state.

### Avoid redundancy without sacrificing clarity

Avoid redundant initializers for fields and variables. 
Value types such as int and float are initialized to 0 by default, and reference types to null, so explicitly assigning these values adds noise without providing value. 
Similarly, although the private access modifier is technically redundant, it should still be specified explicitly. 
Microsoft’s guidelines recommend doing so to make intent clear, improve readability, and avoid ambiguity—especially for less experienced readers.

Be mindful of redundant naming. When a class already provides context, repeating that context in member names adds unnecessary verbosity. 
For example, within a Player class, prefer Score or Target over PlayerScore or PlayerTarget. 
The surrounding scope already communicates ownership and intent.

For public APIs, consider using XML documentation comments to improve output documentation and IntelliSense support. 
These comments provide immediate, structured context to consumers of the code without requiring them to inspect the implementation. 
Attribution comments such as // Created by or // Modified by should be avoided entirely; version control systems are the authoritative source for authorship and change history.

Use #region directives sparingly. 
While they can occasionally help with organization, they often hide complexity and may indicate that a class has grown too large and should be refactored instead. 
One valid use case is grouping clearly delineated code that is invoked externally, such as Animation Event handlers or Input Event callbacks, so those entry points are visually separated from the rest of the implementation.

## Beginner Tips: Avoid Overusing Shorthand Syntax
When you’re new to programming or Unity, it can be tempting to use shorthand syntax to make code look more concise. 
However, clarity and readability should take priority over brevity, especially while you’re still building familiarity with the language and engine. 
As your experience grows, you’ll naturally become more comfortable recognizing and applying more compact syntax where it genuinely improves readability.

Prefer explicit, easy-to-follow code whenever shorthand would obscure intent. 
For example, use explicit types instead of var when the assigned type is not immediately obvious from the right-hand side, and favor traditional method definitions over lambda expressions for multi-line logic or non-trivial behavior. 
Similarly, avoid using the ternary operator for complex conditions, as it can quickly reduce readability and make intent harder to understand.

In short, write code that is easy to read first, and concise second. Readable code is easier to debug, easier to maintain, and easier for others—including your future self—to understand.

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

## Using .editorconfig to Enforce Formatting Rules
Use an .editorconfig file to define and enforce consistent formatting rules across the entire project. 
This includes conventions for indentation, spacing, line endings, brace style (for example, Allman braces), and maximum line length. 
Where applicable, include Unity-specific settings such as UTF-8 encoding and LF line endings to ensure reliable cross-platform behavior.

Most modern IDEs—including Visual Studio, Visual Studio Code, and JetBrains Rider—automatically detect and apply .editorconfig settings, making it an effective way to keep formatting consistent without relying on individual editor preferences. 
Formatting rules can also be applied automatically using tools like dotnet-format or IDE-integrated formatters, ensuring compliance with minimal manual effort.

When necessary, override or specialize rules for specific file types or folders to accommodate Unity-specific assets such as .shader, .meta, or .asmdef files. 
Place the .editorconfig file at the root of the repository so it applies uniformly to the entire project. 
This approach ensures that all contributors follow the same coding style, improving overall readability, consistency, and long-term maintainability.

```csharp
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

# Ignore binary and asset files (optional)
[*.{png,jpg,jpeg,gif,ico,exe,dll,so,zip,unity,meta}]
trim_trailing_whitespace = false
insert_final_newline = false

# C# files
[*.cs]
indent_style = space
indent_size = 4

# Use Allman brace style where supported
csharp_new_line_before_open_brace = all

# Spacing rules
csharp_space_after_keywords_in_control_flow_statements = true
csharp_space_between_method_call_name_and_open_parenthesis = false
csharp_space_between_method_declaration_name_and_open_parenthesis = false
csharp_space_after_comma = true
csharp_space_around_binary_operators = before_and_after
csharp_space_within_square_brackets = false

# var preferences (idiomatic use)
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_var_elsewhere = true:suggestion

# Prefer expression-bodied members where concise (optional)
csharp_style_expression_bodied_methods = when_on_single_line:suggestion
csharp_style_expression_bodied_properties = when_on_single_line:suggestion

# Naming conventions
# Symbol groups
dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private
dotnet_naming_symbols.private_fields.required_modifiers = 

dotnet_naming_symbols.const_fields.applicable_kinds = field
dotnet_naming_symbols.const_fields.applicable_accessibilities = *
dotnet_naming_symbols.const_fields.required_modifiers = const

dotnet_naming_symbols.properties.applicable_kinds = property
dotnet_naming_symbols.properties.applicable_accessibilities = *

# Styles
dotnet_naming_style.m_prefix_style.required_prefix = m_
dotnet_naming_style.m_prefix_style.capitalization = camel_case

dotnet_naming_style.k_prefix_style.required_prefix = k_
dotnet_naming_style.k_prefix_style.capitalization = pascal_case

dotnet_naming_style.pascal_case_style.capitalization = pascal_case

# Rules
dotnet_naming_rule.private_fields_should_have_m_prefix.symbols = private_fields
dotnet_naming_rule.private_fields_should_have_m_prefix.style = m_prefix_style
dotnet_naming_rule.private_fields_should_have_m_prefix.severity = suggestion

dotnet_naming_rule.const_fields_should_have_k_prefix.symbols = const_fields
dotnet_naming_rule.const_fields_should_have_k_prefix.style = k_prefix_style
dotnet_naming_rule.const_fields_should_have_k_prefix.severity = suggestion

dotnet_naming_rule.properties_should_be_pascal_case.symbols = properties
dotnet_naming_rule.properties_should_be_pascal_case.style = pascal_case_style
dotnet_naming_rule.properties_should_be_pascal_case.severity = suggestion

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

# Rider specific: encourage Rider to use .editorconfig settings
# (JetBrains Rider respects standard .editorconfig; no extra keys required)


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



</instructions>
