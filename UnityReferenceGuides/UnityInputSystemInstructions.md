# Unity Input System

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

The Input System package, not the legacy Input Manager. If your project still uses
`Input.GetKey`/`Input.GetAxis`, this guide doesn't apply — check
[`UnityTechStack.md`](../UnityCustomInstructions/UnityTechStack.md) first.

Two things cause most Input System bugs: **actions that were never enabled**, and **callbacks that
were never unsubscribed**. Nearly everything below is about getting those two right.

Table of contents:
- [Core concepts](#core-concepts)
- [Choosing an integration style](#choosing-an-integration-style)
- [Action assets and references](#action-assets-and-references)
- [Callback phases](#callback-phases)
- [Subscribing and unsubscribing](#subscribing-and-unsubscribing)
- [Enabling and disabling action maps](#enabling-and-disabling-action-maps)
- [Reading values vs. events](#reading-values-vs-events)
- [Composite bindings](#composite-bindings)
- [Runtime rebinding](#runtime-rebinding)
- [Local multiplayer](#local-multiplayer)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## Core concepts

| Concept | Is | Think of it as |
|---|---|---|
| `InputActionAsset` | The whole `.inputactions` file | Your input vocabulary |
| Action Map | A named group of actions (`Player`, `UI`, `Vehicle`) | One input *mode* |
| `InputAction` | A single verb (`Jump`, `Move`, `Fire`) | What the player wants to do |
| Binding | A control that triggers the action | How they ask for it |
| `InputActionReference` | A serializable pointer to one action | Inspector-assignable action |
| Control Scheme | A device grouping (Keyboard&Mouse, Gamepad) | Which hardware is in play |

- ✅ Name actions after **intent**, not hardware. `Jump`, not `SpaceBar`. `Interact`, not `EButton`.
- ✅ Name action maps after **modes**, and treat them as mutually exclusive states — see
  [Enabling and disabling action maps](#enabling-and-disabling-action-maps).
- ✅ PascalCase for action and map names, matching the
  [style guide](../UnityStyleGuide.md#animation-parameters-layers-tags-sorting-layers-and-input-action-names).

---

## Choosing an integration style

There are three ways to consume input, and mixing them in one project is a reliable source of
confusion. Pick one per project and note it in your tech stack file.

| Style | How | Good for | Cost |
|---|---|---|---|
| **Generated C# class** | Tick *Generate C# Class* on the asset | Most projects. Compile-time safe, no Inspector wiring | You own enable/disable |
| `PlayerInput` component | Add the component, pick a behaviour | Local multiplayer, quick prototypes | Magic-string or Inspector-wired callbacks |
| Raw `InputAction` fields | `[SerializeField] private InputActionReference` | One-off actions on a single component | Easy to forget `Enable()` |

- ✅ **Default to the generated C# class.** It gives you `m_input.Player.Jump` with IntelliSense, so
  a renamed action becomes a compile error rather than silent dead input.
- ⚠️ `PlayerInput`'s *Send Messages* and *Broadcast Messages* behaviours use reflection on method
  names (`OnJump`). They're fast to set up and impossible to refactor safely. Prefer *Invoke Unity
  Events* or *Invoke C# Events* if you use the component at all.
- ⚠️ Don't put a `PlayerInput` component in a scene *and* enable the same map from code. Both hold
  references and you get doubled callbacks.

```csharp
// Generated C# class - the default recommendation
public class PlayerController : MonoBehaviour
{
    private GameInput m_input;          // Generated from GameInput.inputactions

    private void Awake()
    {
        m_input = new GameInput();
    }

    private void OnEnable()
    {
        m_input.Player.Enable();
        m_input.Player.Jump.performed += HandleJumpPerformed;
    }

    private void OnDisable()
    {
        m_input.Player.Jump.performed -= HandleJumpPerformed;
        m_input.Player.Disable();
    }

    private void OnDestroy()
    {
        // The generated class is IDisposable - it holds native memory
        m_input?.Dispose();
    }

    private void HandleJumpPerformed(InputAction.CallbackContext context)
    {
        Jump();
    }
}
```

- ⚠️ The generated class implements `IDisposable`. Dispose it in `OnDestroy` — see
  [OnDestroy()](../UnityStyleGuide.md#ondestroy).

---

## Action assets and references

- ✅ One `.inputactions` asset for the game. Multiple assets means multiple enable states to track.
- ✅ Use `InputActionReference` when a component needs one specific action assigned in the Inspector.
- ⚠️ An `InputActionReference` points at the action **inside the asset**. Enabling it enables it
  everywhere, and another script disabling the map turns it off under you.
- ✅ Store the asset outside `Resources/` and reference it directly, per
  [Assets & Memory](UnityAssetsAndMemoryInstructions.md#choosing-a-loading-strategy).

---

## Callback phases

Every action raises up to three events. Choosing the wrong one is the most common source of
"my input fires twice" and "my input never fires".

| Phase | Fires when | Use for |
|---|---|---|
| `started` | The control first moves past the press point | Charge-up, "button went down" |
| `performed` | The action's interaction is satisfied | **Most things.** The actual "do it" |
| `canceled` | The control returns to default | Release, stop moving, cancel a charge |

- ✅ For a plain Button action, `performed` fires on press. That's what you want.
- ✅ For a Value action like `Move`, `performed` fires **every time the value changes** — including
  every frame a stick is held at a changing angle. Use `canceled` to zero it out.
- ⚠️ With a Hold or Tap interaction, `performed` fires only once the interaction completes. If your
  input feels laggy, check whether an interaction is attached to the binding.
- ⚠️ `started` and `performed` both fire for a simple press. Subscribing to both double-triggers.

```csharp
private void OnEnable()
{
    // Value action: track changes AND the return to neutral
    m_input.Player.Move.performed += HandleMovePerformed;
    m_input.Player.Move.canceled  += HandleMoveCanceled;

    // Button action: performed only
    m_input.Player.Jump.performed += HandleJumpPerformed;
}

private void HandleMovePerformed(InputAction.CallbackContext context)
{
    m_moveInput = context.ReadValue<Vector2>();
}

private void HandleMoveCanceled(InputAction.CallbackContext context)
{
    // Without this the character keeps walking after the stick is released
    m_moveInput = Vector2.zero;
}
```

---

## Subscribing and unsubscribing

This is the [style guide's `OnEnable`/`OnDisable` rule](../UnityStyleGuide.md#subscribing-and-unsubscribing-to-events)
applied to input, and it bites harder here because the action asset outlives the component.

- ✅ Subscribe in `OnEnable`, unsubscribe in `OnDisable`. Mirror them exactly.
- ❌ Never subscribe with a lambda — you can't unsubscribe it, and the action asset will hold a
  reference to your destroyed component.
- ⚠️ An `InputAction` from a shared asset is **not** destroyed with your GameObject. A missed
  unsubscribe means the callback fires on a dead object and throws
  `MissingReferenceException` — often several scenes later.
- ✅ Callback methods take `InputAction.CallbackContext` and follow the `Handle*` naming convention.

```csharp
// ❌ Cannot be unsubscribed - the action asset now holds this component forever
m_input.Player.Jump.performed += ctx => Jump();

// ✅ Method group - removable
m_input.Player.Jump.performed += HandleJumpPerformed;
```

---

## Enabling and disabling action maps

Action maps are the cleanest state boundary the Input System gives you. Use them.

- ✅ Exactly one gameplay map enabled at a time. Opening a menu disables `Player` and enables `UI`.
- ✅ Disabling a map cancels its in-flight actions, so held buttons don't stick across a mode change.
- ⚠️ An action that was never enabled silently does nothing. No warning, no error. If input "doesn't
  work", check this first.
- ⚠️ `InputActionAsset.Enable()` enables *every* map at once, including `UI`. Rarely what you want.

```csharp
public class InputModeService : MonoBehaviour
{
    private GameInput m_input;

    public void SetMode(InputMode mode)
    {
        // Disable everything first so no map is left half-enabled
        m_input.Player.Disable();
        m_input.UI.Disable();

        switch (mode)
        {
            case InputMode.Gameplay:
                m_input.Player.Enable();
                break;
            case InputMode.Menu:
                m_input.UI.Enable();
                break;
        }
    }
}
```

---

## Reading values vs. events

- ✅ **Events** for discrete actions: jump, fire, interact, pause.
- ✅ **Polling** for continuous values read once per frame: movement, look, throttle.
- ⚠️ Don't do both for the same action. Pick one.
- ✅ Polling with `ReadValue<T>()` in `Update` is cheap and avoids caching a value in a field.
- ⚠️ Read input in `Update`, apply it in `FixedUpdate` — see
  [FixedUpdate()](../UnityStyleGuide.md#fixedupdate). Reading input in `FixedUpdate` drops presses,
  because `FixedUpdate` may not run on a given frame.

```csharp
private Vector2 m_moveInput;

private void Update()
{
    // Poll continuous values - no event, no cached-value bugs
    m_moveInput = m_input.Player.Move.ReadValue<Vector2>();
}

private void FixedUpdate()
{
    // Apply in the physics step
    m_rigidbody.AddForce(new Vector3(m_moveInput.x, 0f, m_moveInput.y) * m_moveSpeed);
}
```

- ⚠️ `ReadValue<T>()` must match the action's Control Type exactly. A `Vector2` action read as
  `float` throws `InvalidOperationException` at runtime, not compile time.

---

## Composite bindings

- ✅ Use a **2D Vector** composite for WASD rather than four separate actions.
- ✅ Use **One Modifier** / **Two Modifiers** for chorded input (Ctrl+S) instead of checking modifier
  state manually.
- ⚠️ Composite part names matter (`up`, `down`, `left`, `right`). Renaming them in the asset breaks
  the composite silently.
- ✅ Set the composite's Control Type to match what you'll `ReadValue<T>()`.

---

## Runtime rebinding

- ✅ `PerformInteractiveRebinding` handles listening, matching and applying. Don't hand-roll it.
- ✅ Always `.Dispose()` the rebinding operation — it's unmanaged and leaks otherwise.
- ✅ Disable the action while rebinding, or the rebind press also triggers the action.
- ✅ Exclude the pointer and the cancel key, or the first mouse move completes the rebind.
- ✅ Persist with `SaveBindingOverridesAsJson` / `LoadBindingOverridesFromJson`.

```csharp
private InputActionRebindingExtensions.RebindingOperation m_rebindOperation;

public void StartRebind(InputAction action, int bindingIndex, Action onComplete)
{
    action.Disable();   // Otherwise the rebind keypress also fires the action

    m_rebindOperation = action.PerformInteractiveRebinding(bindingIndex)
        .WithControlsExcluding("<Mouse>/position")
        .WithControlsExcluding("<Mouse>/delta")
        .WithCancelingThrough("<Keyboard>/escape")
        .OnComplete(operation =>
        {
            operation.Dispose();          // Unmanaged - always dispose
            m_rebindOperation = null;
            action.Enable();
            onComplete?.Invoke();
        })
        .OnCancel(operation =>
        {
            operation.Dispose();
            m_rebindOperation = null;
            action.Enable();
        })
        .Start();
}

private void OnDestroy()
{
    m_rebindOperation?.Dispose();
}
```

---

## Local multiplayer

- ✅ Use `PlayerInputManager` for join/leave handling — it pairs devices to players for you.
- ✅ Each player gets a `PlayerInput` with its own action instance, so enabling one player's map
  doesn't affect another's.
- ⚠️ In local multiplayer, `InputUser` pairing matters. Don't read from the global
  `Keyboard.current` — that's every player at once.
- ✅ Subscribe to `PlayerInputManager.onPlayerJoined` / `onPlayerLeft` in `OnEnable`/`OnDisable` like
  any other event.

---

## Troubleshooting

**Input does nothing at all.**
The action or its map was never enabled. This is by far the most common cause and it produces no
error. Check `action.enabled` before anything else.

```csharp
// Diagnostic: dump the state of an action
private void LogActionState(InputAction action)
{
    Debug.Log($"{action.name}: enabled={action.enabled}, phase={action.phase}, " +
              $"bindings={action.bindings.Count}, controls={action.controls.Count}");

    // controls == 0 means nothing on the current device matches the binding
    foreach (InputControl control in action.controls)
    {
        Debug.Log($"  bound to {control.path}");
    }
}
```

**Callback fires twice per press.**
Either subscribed to both `started` and `performed`, or the component subscribes in `Awake` *and*
`OnEnable` (so re-enabling adds a second handler), or a `PlayerInput` component is wired to the same
action in the Inspector as well as in code.

**`MissingReferenceException` from an input callback, often after a scene change.**
A missed unsubscribe. The action asset outlives the component and is still holding the delegate.
Check that every `+=` in `OnEnable` has its `-=` in `OnDisable`.

**Character keeps moving after the stick is released.**
No `canceled` handler on a Value action. `performed` doesn't fire when the value returns to zero.

**`InvalidOperationException: Cannot read value ... as 'Single'`.**
`ReadValue<T>()` doesn't match the action's Control Type. A 2D Vector action must be read as
`Vector2`.

**Input works in the Editor, not in a build.**
Usually a missing device layout for the platform, or *Active Input Handling* in Player Settings still
set to the old system. It must be *Input System Package* or *Both*.

**UI clicks do nothing after the Input System was added.**
The scene still has a legacy `StandaloneInputModule`. It needs `InputSystemUIInputModule` on the
EventSystem.

**Rebinding completes instantly.**
Mouse movement matched first. Add `.WithControlsExcluding("<Mouse>/position")` and `/delta`.

---

## Review checklist

| Check | Look for |
|---|---|
| Enable | An action or map subscribed to but never `Enable()`d |
| Unsubscribe | `performed +=` in `OnEnable` with no `-=` in `OnDisable` |
| Lambdas | `performed += ctx => …` — impossible to unsubscribe |
| Dispose | Generated input class not disposed in `OnDestroy` |
| Phases | `started` and `performed` both subscribed for one button |
| Value actions | `performed` handled but no `canceled` |
| Timing | `ReadValue` called in `FixedUpdate` instead of `Update` |
| Legacy | `Input.GetKey` / `Input.GetAxis` still present |
| Modes | Multiple gameplay maps enabled simultaneously |
| Rebinding | `RebindingOperation` not disposed |
| Naming | Actions named after hardware rather than intent |

---

## Learn more

- [Input System manual](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/index.html)
- [Actions](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/Actions.html)
- [Interactive rebinding](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/ActionBindings.html#interactive-rebinding)
