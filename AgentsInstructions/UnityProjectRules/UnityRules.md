# Unity Project Rules

> **Applying this to an existing project:** audit first. Report where the project differs, list each
> proposed change, and let the user pick and confirm the exact list before editing anything, whether
> they handed over the whole kit or only this document. Writing new code under these rules needs no audit.

My coding philosophy is heavily based on the books Clean Code, The Pragmatic Programmer, and A Philosophy of Software Design, but adapted in a pragmatic way for Unity projects. My core principles are to generate code that is extremely readable, testable, decoupled, and optimized for visual debugging in the Unity Editor.

Rules marked `[opinion]` are personal preferences: keep, change or drop them to fit your team. Unmarked rules are standard C# and Unity practice, or they prevent known bugs. ([What's opinionated](../CodeStyleGuide/README.md#whats-opinionated-here))

## 1. Naming & Intent (Self-Documenting Code)

- **Extreme Verbosity:** `[opinion]` Name all variables and methods so they are completely self-explanatory. Never abbreviate the name itself. Use `DistanceToTargetInMeters` rather than `Distance` or `Dist`. The style guide's `m_`, `k_` and `s_` prefixes are always allowed, but spell out the name after them: `m_distanceToTargetInMeters`, not `m_dist`. ([Fields](../CodeStyleGuide/UnityStyleGuide.md#fields))
- **Nouns and Verbs:** Use nouns for classes (`Pathfinder`) and verbs for methods (`CalculateRoute`).
- **Positive Framing:** Frame boolean variables positively to reduce cognitive load (e.g., `IsVisible` instead of `IsNotHidden`).
- **No Magic Values:** Replace hardcoded numbers and strings with named constants or serialized variables.
- **Strict Commenting Rule:** `[opinion]` Remove comments that simply restate the code. Only write comments to explain "Why" (business logic, math formulas, or hacky Unity workarounds). Prioritize using `[Tooltip("...")]` on serialized fields instead of inline comments to reveal intent.

## 2. State & Inspector Debugging

- **Expose State:** `[opinion]` Serialize all variables (`[SerializeField]`) so they can be viewed and debugged in the Unity Inspector without looking at the code.
- **Protect Internal State:** `[opinion]` For variables that are strictly internal state (not meant to be edited by designers), serialize them but use a `[ReadOnly]` attribute to prevent accidental modification while retaining visual debugging.
- **Data vs. Objects:** Keep data structures (which expose data but have no behavior) distinct from objects (which hide data and expose behavior).
- **Safe Collections:** Always return empty collections (e.g., `Array.Empty<T>()`) rather than `null` to prevent `NullReferenceException`s.
- **Serialize with Intent:** Serialize what you want to debug. Keep purely internal state non-serialized to limit scene and prefab churn and merge noise.
- **Rename-Safe Serialization:** Add `[FormerlySerializedAs]` when renaming serialized fields, and keep serialized enum values stable. ([Asset and serialization safety](../../AGENTS.md#asset-and-serialization-safety))

## 3. Class & Method Design

- **Single Responsibility & Deep Modules:** A `MonoBehaviour` should have only one reason to change. Expose a narrow, simple public interface but encapsulate complex internal behavior.
- **Keep Methods Tiny:** `[opinion]` A function should do exactly one thing. If a method requires vertical scrolling to read, extract its logic into smaller methods.
- **Extract Conditionals:** Move complex boolean logic inside `if` statements into well-named private methods (e.g., `if (IsPlayerEligibleForCombo())`).
- **Command-Query Separation:** `[opinion]` A method must either perform an action (Command) or return data (Query), but never both.
- **Limit Arguments:** `[opinion]` Aim for 0-2 arguments per function. Wrap 3+ arguments in a struct or class.
- **The Newspaper Metaphor:** `[opinion]` Organize classes with public methods at the top, cascading down to the private helper methods that support them.
- **Testable Logic:** Keep logic in plain C# classes and make the `MonoBehaviour` a thin shell, so the logic can be covered by EditMode tests. ([Testing setup](../../AuditInstructions/Testing/TestingInstructions.md))

## 4. Architecture & Decoupling

- **Question New Layers:** Before introducing a new manager, service, wrapper, or decorator, ask whether it hides meaningful complexity, provides a distinct responsibility, or simply moves existing code into another class.
- **Bootstrap Scene:** `[opinion]` Use a bootstrap scene. I prefer that over service locator patterns. It owns startup and global services, loads other scenes additively, and is the one allowed exception to "Prefabs are Truth". Make Play work from any scene in the Editor. ([Scenes and lifecycle lens](../../AuditInstructions/ProjectAuditGuides/UnityScenesAndLifecycleInstructions.md))
- **Composition over Inheritance:** Avoid deep class hierarchies. Build systems using modular `MonoBehaviour` components snapped onto GameObjects.
- **Decouple via Events:** `[opinion]` Components must broadcast state changes (`Action`, `UnityEvent`) rather than directly calling methods on other components.
- **Clean Up Subscriptions:** Subscribe in `OnEnable`, unsubscribe in `OnDisable`, and never leave a static event subscribed after its owner is destroyed. ([Events](../CodeStyleGuide/UnityStyleGuide.md#subscribing-and-unsubscribing-to-events), [static events](../CodeStyleGuide/UnityStyleGuide.md#static-events-and-domain-reload))
- **Law of Demeter:** Talk only to immediate friends. Never chain references (e.g., avoid `GameManager.Instance.Player.Inventory.GetItem()`).
- **Kill Singletons:** `[opinion]` Avoid Singletons for game state. Connect systems with serialized wiring first, constructor injection for plain C# classes, or ScriptableObject-based event channels. Add no DI framework without approval.
- **DRY with ScriptableObjects:** Use ScriptableObjects for shared configuration data rather than duplicating values across prefabs.
- **ScriptableObjects Hold Config, Not Runtime State:** Values written in Play Mode persist in the Editor, so clone or reset any runtime state. ([ScriptableObjects](../CodeStyleGuide/UnityStyleGuide.md#scriptable-objects), [Assets and memory lens](../../AuditInstructions/ProjectAuditGuides/UnityAssetsAndMemoryInstructions.md))
- **Assembly Definitions:** `[opinion]` Use one asmdef per feature with one-way dependencies, so boundaries are enforced at compile time. ([Assembly lens](../../AuditInstructions/ProjectAuditGuides/UnityAssemblyDefinitionsInstructions.md))

## 5. Unity-Specific Pragmatism

- **Initialization Discipline:** Use `Awake()` strictly for caching local references (`GetComponent`). Use `Start()` strictly for logic that relies on those references.
- **Execution Order Independence:** Never rely on Unity's Script Execution Order. Scripts must initialize safely regardless of order.
- **Prefabs are Truth:** `[opinion]` Assume Scene files are empty containers. All meaningful hierarchy and logic must live inside Prefabs to prevent merge conflicts.
- **YAGNI:** Build only what is needed today. Do not over-engineer systems for hypothetical future updates.
- **Async:** Prefer `Awaitable` over coroutines for new async work, cancel with `destroyCancellationToken`, and always observe errors. ([Async & Awaitable usage](../CodeStyleGuide/UnityStyleGuide.md#async--awaitable-usage))
- **Hot Paths:** Do not poll variables in `Update()`. Use events or C# properties with backing fields to trigger logic only when data actually changes. Cache `GetComponent` results, and avoid `Find*`, LINQ and string concatenation in `Update()`. Use `CompareTag` and pool frequently spawned objects. ([String allocations](../CodeStyleGuide/UnityStyleGuide.md#managing-string-allocations), [Performance lens](../../AuditInstructions/ProjectAuditGuides/UnityPerformanceOptimizationInstructions.md))
- **Input and UI:** Use Input System actions, not `Input.GetKey`. UI reads state through events and never owns it. ([Input System lens](../../AuditInstructions/ProjectAuditGuides/UnityInputSystemInstructions.md), [UI Toolkit lens](../../AuditInstructions/ProjectAuditGuides/UnityUIToolkitInstructions.md))
- **Editor-Only Code:** Keep it in an Editor assembly or behind `#if UNITY_EDITOR`, so player builds don't break. ([Editor tooling lens](../../AuditInstructions/ProjectAuditGuides/UnityEditorToolingInstructions.md))
- **Asset Loading Ownership:** Whoever loads an asset or Addressables handle releases it. ([Assets and memory lens](../../AuditInstructions/ProjectAuditGuides/UnityAssetsAndMemoryInstructions.md))
- **Reload-Safe Static State:** Reset every mutable static with `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]`, so code works with domain reload on or off. ([Static events and domain reload](../CodeStyleGuide/UnityStyleGuide.md#static-events-and-domain-reload), [Reload policy](../../AuditInstructions/ProjectSettings/ProjectSettings.md#reload-policy))
- **Vendor and Protected Code:** Wrap third-party code instead of editing it. When an edit is unavoidable, log it in a patch ledger and keep the file's encoding and line endings. List protected folders in the project's `AGENTS.md`. ([Starter AGENTS.md](../AGENTS.md))

## 6. Robustness & Error Handling

- **Fail Fast / Crash Early:** `[opinion]` Do not let invalid states propagate silently. Use `Debug.Assert()` heavily in `Awake()` to halt the editor if required components or references are missing.
- **Validate Early:** Use `OnValidate` and `[RequireComponent]` to catch missing references at edit time, before `Debug.Assert()` fires in `Awake()`. ([General notes](../CodeStyleGuide/UnityStyleGuide.md#general-notes), [Editor tooling lens](../../AuditInstructions/ProjectAuditGuides/UnityEditorToolingInstructions.md))
- **Destroyed-Object Null Checks:** Don't use `?.`, `??` or `is null` on `UnityEngine.Object` fields. They bypass Unity's overloaded null check, so a destroyed object looks alive. ([Destroyed-object checks](../../AuditInstructions/ProjectAuditGuides/UnityScenesAndLifecycleInstructions.md#destroyed-object-checks))
- **Define Errors Out of Existence:** Design APIs so invalid states cannot be represented (e.g., use Enums/structs instead of strings).
- **Never Swallow Exceptions:** If using a `try-catch` block, you must handle the error or explicitly log it. Empty `catch` blocks are forbidden.
- **Zero Warnings:** `[opinion]` Treat all compiler and Unity console warnings as errors. This applies to your own code. Warnings from Unity packages are tracked, not blocking.
- **Strategic over Tactical:** Never hack things together just to make them work. Always write clean, maintainable structures from the start.
- **Fix at the Owning Source:** Reproduce a bug before tuning anything. Fix it in the prefab, tool or data that owns it, not the scene-local symptom, and edit the generator rather than its generated prefab. ([Working rules](../AGENTS.md#working-rules))
- **Definition of Done:** Before finishing, compile, run the EditMode tests, and confirm the console is clean. ([Working rules](../../AGENTS.md#working-rules), [Testing setup](../../AuditInstructions/Testing/TestingInstructions.md))
- **Verification Honesty:** Zero tests run, a cached result or "command accepted" is not a pass. Editor compilation does not prove the player build compiles. Report automated checks and player-visible behavior separately. ([Verification](../AGENTS.md#verification))

## Working with GitHub

- Whenever you are asked to create a PR, make sure to provide test conditions.
- **PR Quality:** Keep PRs small and scoped, link the issue, and include a screenshot or clip for visual changes. ([GitHub workflow](../../AuditInstructions/Github/GithubInstructions.md))
