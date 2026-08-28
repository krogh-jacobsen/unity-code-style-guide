# Project Tech Stack

> **Project-specific. You are expected to edit this file.**
> This is the first file to change when you adopt this guide. Everything here tells your coding
> assistant which Unity APIs are valid for *your* project — get it wrong and it will confidently
> generate code for the wrong render pipeline or input system.

## Versions

- ℹ️ This project uses **Unity 6.3 (6000.3.x)**. Use sources and documentation that apply to Unity 6
  or later. Do not generate code for Unity 2022 or earlier.
- ℹ️ C# language version: **C# 9.0**. Target-typed `new()`, records, and pattern matching enhancements
  are available; newer language features are not.

## Systems in use

| Area | This project uses | Not used — do not generate |
|---|---|---|
| Input | Input System package | Legacy Input Manager (`Input.GetAxis`, `Input.GetKey`) |
| UI | UI Toolkit (UXML/USS) | uGUI / Canvas, IMGUI for runtime UI |
| Rendering | Universal Render Pipeline (URP 17.3) | Built-in Render Pipeline, HDRP |
| Async | `Awaitable` + async/await | Coroutines, except where per-frame iteration is genuinely needed |
| Pooling | `UnityEngine.Pool.ObjectPool<T>` | Hand-rolled pool implementations |

## Conventions that follow from the stack

- ℹ️ Prefer `Awaitable` over coroutines for sequencing:
  `await Awaitable.WaitForSecondsAsync(delay, destroyCancellationToken);`
  Guard continuations with `if (this == null || !isActiveAndEnabled) return;`.
- ℹ️ When instantiating frequently, favour `UnityEngine.Pool.ObjectPool<T>` with
  `actionOnGet`/`actionOnRelease` to toggle active state.
- ℹ️ UI work goes through UI Toolkit. See
  [UnityUIToolkitInstructions.md](../UnityReferenceGuides/UnityUIToolkitInstructions.md).
  If you switch to uGUI, read
  [UnityUGUIInstructions.md](../UnityReferenceGuides/UnityUGUIInstructions.md) instead and update
  the table above.

## Packages

List the packages your project depends on so your assistant doesn't suggest APIs you haven't
installed, or reinvent something a package already provides.

| Package | Version | Used for |
|---|---|---|
| `com.unity.inputsystem` | 1.x | All player input |
| `com.unity.render-pipelines.universal` | 17.3 | Rendering |
| `com.unity.addressables` | — | *(fill in or remove)* |
| `com.unity.test-framework` | — | *(fill in or remove)* |

## Platform targets

- **Primary:** *(e.g. Windows/macOS standalone)*
- **Secondary:** *(e.g. Android)*
- ℹ️ Performance budgets and platform quirks differ a lot between these. Note anything
  non-obvious here — for example a 60 fps cap on mobile, or a memory ceiling.
