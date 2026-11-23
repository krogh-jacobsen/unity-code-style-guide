# Unity Project Rules

> **Applying this to an existing project:** audit first. Report where the project differs, list each
> proposed change, and let the user pick and confirm the exact list before editing anything, whether
> they handed over the whole kit or only this document. Writing new code under these rules needs no audit.

These rules draw on Clean Code, The Pragmatic Programmer and A Philosophy of Software Design, adapted pragmatically for Unity. The aim is code that is readable, testable, decoupled and easy to debug in the Unity Editor.

Rules marked `[opinion]` are personal preferences: keep, change or drop them to fit your team. Unmarked rules are standard C# and Unity practice, or they prevent known bugs. ([What's opinionated](../CodeStyleGuide/README.md#whats-opinionated-here))

## Always-on rules live in AGENTS.md

The rules that prevent silent Unity bugs, and the verification rules, are in the [starter AGENTS.md](../AGENTS.md) and in the full-kit version. Either one, at a project's root, loads in every session, so they are not repeated here. Detail for each:

- **Asset and serialization safety:** [Unity safety](../AGENTS.md#unity-safety)
- **Destroyed-object null checks:** [Destroyed-object checks](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityScenesAndLifecycleInstructions.md#destroyed-object-checks), [enforce with analyzers](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/CodeEnforcement/SetupEnforcement.md#6-optional-roslyn-analyzers)
- **Event subscriptions:** [Subscribing and unsubscribing](../CodeStyleGuide/UnityStyleGuide.md#subscribing-and-unsubscribing-to-events), [static events](../CodeStyleGuide/UnityStyleGuide.md#static-events-and-domain-reload)
- **Reload-safe static state:** [Static events and domain reload](../CodeStyleGuide/UnityStyleGuide.md#static-events-and-domain-reload), [Reload policy](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectSettings/ProjectSettings.md#reload-policy)
- **ScriptableObject runtime state:** [ScriptableObjects](../CodeStyleGuide/UnityStyleGuide.md#scriptable-objects), [Assets and memory lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityAssetsAndMemoryInstructions.md)
- **Editor-only code:** [Editor tooling lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityEditorToolingInstructions.md), [player compile check](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/CodeEnforcement/SetupEnforcement.md#5-add-the-player-compile-check)
- **Development code out of players:** [Layering and boundary tests](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/CodeEnforcement/SetupEnforcement.md#2-declare-the-layering)
- **Async lifetime:** [Async & Awaitable usage](../CodeStyleGuide/UnityStyleGuide.md#async--awaitable-usage)
- **Asset loading ownership:** [Assets and memory lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityAssetsAndMemoryInstructions.md)
- **Vendor and protected code, fixing at the owning source, definition of done, verification honesty:** [Unity safety](../AGENTS.md#unity-safety), [Verification](../AGENTS.md#verification), [Working rules](../AGENTS.md#working-rules)

## 1. Naming & Intent (Self-Documenting Code)

- **Extreme Verbosity:** `[opinion]` Name all variables and methods so they are completely self-explanatory. Never abbreviate the name itself. Use `DistanceToTargetInMeters` rather than `Distance` or `Dist`. The style guide's `m_`, `k_` and `s_` prefixes are always allowed, but spell out the name after them: `m_distanceToTargetInMeters`, not `m_dist`. ([Fields](../CodeStyleGuide/UnityStyleGuide.md#fields))
- **Strict Commenting Rule:** `[opinion]` Remove comments that simply restate the code. Only write comments to explain "Why" (business logic, math formulas, or hacky Unity workarounds). Prioritize using `[Tooltip("...")]` on serialized fields instead of inline comments to reveal intent.

## 2. State & Inspector Debugging

- **Expose State:** `[opinion]` Serialize all variables (`[SerializeField]`) so they can be viewed and debugged in the Unity Inspector without looking at the code.
- **Protect Internal State:** `[opinion]` For variables that are strictly internal state (not meant to be edited by designers), serialize them but use a `[ReadOnly]` attribute to prevent accidental modification while retaining visual debugging.
- **Safe Collections:** Always return empty collections (e.g., `Array.Empty<T>()`) rather than `null` to prevent `NullReferenceException`s.
- **Serialize with Intent:** Serialize what you want to debug. Keep purely internal state non-serialized to limit scene and prefab churn and merge noise.

## 3. Class & Method Design

- **Single Responsibility & Deep Modules:** A `MonoBehaviour` should have only one reason to change. Expose a narrow, simple public interface but encapsulate complex internal behavior.
- **Keep Methods Tiny:** `[opinion]` A function should do exactly one thing. If a method requires vertical scrolling to read, extract its logic into smaller methods.
- **Command-Query Separation:** `[opinion]` A method must either perform an action (Command) or return data (Query), but never both.
- **Limit Arguments:** `[opinion]` Aim for 0-2 arguments per function. Wrap 3+ arguments in a struct or class.
- **The Newspaper Metaphor:** `[opinion]` Organize classes with public methods at the top, cascading down to the private helper methods that support them.
- **Testable Logic:** Keep logic in plain C# classes and make the `MonoBehaviour` a thin shell, so the logic can be covered by EditMode tests. ([Testing setup](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/Testing/TestingInstructions.md))

## 4. Architecture & Decoupling

- **Question New Layers:** Before introducing a new manager, service, wrapper, or decorator, ask whether it hides meaningful complexity, provides a distinct responsibility, or simply moves existing code into another class.
- **Bootstrap Scene:** `[opinion]` Use a bootstrap scene as the composition root. It owns startup and global services, loads other scenes (additively, by preference), and is the one allowed exception to "Prefabs are Truth". Make Play work from any scene in the Editor. A service locator inside it is acceptable when registrations are scoped to their owning scene and reset; resolve dependencies there, not deep in gameplay code. ([Scenes and lifecycle lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityScenesAndLifecycleInstructions.md))
- **Composition over Inheritance:** Avoid deep class hierarchies. Build systems using modular `MonoBehaviour` components snapped onto GameObjects.
- **Decouple via Events:** `[opinion]` Components must broadcast state changes (`Action`, `UnityEvent`) rather than directly calling methods on other components.
- **Kill Singletons:** `[opinion]` Avoid Singletons for game state. Connect systems with serialized wiring first, constructor injection for plain C# classes, or ScriptableObject-based event channels. A static event bus is fine when its statics reset on load. Add no DI framework without approval.
- **DRY with ScriptableObjects:** Use ScriptableObjects for shared configuration data rather than duplicating values across prefabs.
- **Assembly Definitions:** `[opinion]` Use one asmdef per feature with one-way dependencies, so boundaries are enforced at compile time. Keep core rules engine-free (`noEngineReferences`), and let only an adapter assembly reference vendor code. ([Assembly lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityAssemblyDefinitionsInstructions.md), [Layering and boundary tests](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/CodeEnforcement/SetupEnforcement.md#2-declare-the-layering))

## 5. Unity-Specific Pragmatism

- **Initialization Discipline:** Use `Awake()` strictly for caching local references (`GetComponent`). Use `Start()` strictly for logic that relies on those references.
- **Execution Order Independence:** Never rely on Unity's Script Execution Order. Scripts must initialize safely regardless of order.
- **Prefabs are Truth:** `[opinion]` Assume Scene files are empty containers. All meaningful hierarchy and logic must live inside Prefabs to prevent merge conflicts.
- **Async:** Prefer `Awaitable` over coroutines for new async work, unless the project's `AGENTS.md` decides otherwise. ([Async & Awaitable usage](../CodeStyleGuide/UnityStyleGuide.md#async--awaitable-usage))
- **Hot Paths:** Do not poll variables in `Update()`. Use events or C# properties with backing fields to trigger logic only when data actually changes. Cache `GetComponent` results, and avoid `Find*`, LINQ and string concatenation in `Update()`. Use `CompareTag` and pool frequently spawned objects. ([String allocations](../CodeStyleGuide/UnityStyleGuide.md#managing-string-allocations), [Performance lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityPerformanceOptimizationInstructions.md))
- **Input and UI:** Use Input System actions, not `Input.GetKey`. UI reads state through events and never owns it. ([Input System lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityInputSystemInstructions.md), [UI Toolkit lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityUIToolkitInstructions.md))

## 6. Robustness & Error Handling

- **Fail Fast / Crash Early:** `[opinion]` Do not let invalid states propagate silently. Use `Debug.Assert()` heavily in `Awake()` to halt the editor if required components or references are missing.
- **Validate Early:** Use `OnValidate` and `[RequireComponent]` to catch missing references at edit time, before `Debug.Assert()` fires in `Awake()`. ([General notes](../CodeStyleGuide/UnityStyleGuide.md#general-notes), [Editor tooling lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityEditorToolingInstructions.md))
- **Zero Warnings:** `[opinion]` Treat all compiler and Unity console warnings as errors. This applies to your own code. Warnings from Unity packages are tracked, not blocking. ([Analyzers and severity](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/CodeEnforcement/SetupEnforcement.md#6-optional-roslyn-analyzers))
- **Logging:** Log through one wrapper. Verbose calls carry `[Conditional("UNITY_EDITOR")]` and `[Conditional("DEVELOPMENT_BUILD")]` so release builds strip them; errors always stay. ([Performance lens](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/ProjectAuditGuides/UnityPerformanceOptimizationInstructions.md))

## Working with GitHub

- Whenever you are asked to create a PR, make sure to provide test conditions.
- **PR Quality:** Keep PRs small and scoped, link the issue, and include a screenshot or clip for visual changes. ([GitHub workflow](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/Github/GithubInstructions.md))

## If your model needs it

General clean-code practice that current models usually follow without being told. They stay here as a reference for people learning the craft, and for a model that drifts from them. Leave them out of an agent's context unless you see the model get them wrong.

- **Nouns and Verbs:** Use nouns for classes (`Pathfinder`) and verbs for methods (`CalculateRoute`).
- **Positive Framing:** Frame boolean variables positively to reduce cognitive load (e.g., `IsVisible` instead of `IsNotHidden`).
- **No Magic Values:** Replace hardcoded numbers and strings with named constants or serialized variables.
- **Data vs. Objects:** Keep data structures (which expose data but have no behavior) distinct from objects (which hide data and expose behavior).
- **Extract Conditionals:** Move complex boolean logic inside `if` statements into well-named private methods (e.g., `if (IsPlayerEligibleForCombo())`).
- **Law of Demeter:** Talk only to immediate friends. Never chain references (e.g., avoid `GameManager.Instance.Player.Inventory.GetItem()`).
- **YAGNI:** Build only what is needed today. Do not over-engineer systems for hypothetical future updates.
- **Define Errors Out of Existence:** Design APIs so invalid states cannot be represented (e.g., use Enums/structs instead of strings).
- **Never Swallow Exceptions:** If using a `try-catch` block, you must handle the error or explicitly log it. Empty `catch` blocks are forbidden.
- **Strategic over Tactical:** Never hack things together just to make them work. Always write clean, maintainable structures from the start.
