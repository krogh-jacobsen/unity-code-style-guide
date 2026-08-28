---
description: Guidelines for debugging Unity projects via MCP connection
applyTo: "**/*.cs"
---

# Unity Debugging Instructions for LLM Coding Tools

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).


## Overview

This document provides instructions for AI coding assistants connected to Unity projects via MCP (Model Context Protocol).
Use these guidelines when helping developers debug Unity applications.

## Table of Contents

- [Diagnostic Priority Order](#diagnostic-priority-order)
- [Console Output Analysis](#console-output-analysis)
- [SerializeField and Inspector Debugging](#serializefield-and-inspector-debugging)
- [Script Execution Order Issues](#script-execution-order-issues)
- [Null Reference Debugging](#null-reference-debugging)
- [Input System Debugging](#input-system-debugging)
- [Physics Debugging](#physics-debugging)
- [Animation and Animator Debugging](#animation-and-animator-debugging)
- [UI Toolkit Debugging](#ui-toolkit-debugging-unity-6)
- [Audio Debugging](#audio-debugging)
- [Async and Coroutine Debugging](#async-and-coroutine-debugging)
- [Event System Debugging](#event-system-debugging)
- [ScriptableObject Runtime Issues](#scriptableobject-runtime-issues)
- [Transform and Hierarchy Issues](#transform-and-hierarchy-issues)
- [Performance Debugging](#performance-debugging)
- [Scene and Asset Debugging](#scene-and-asset-debugging)
- [Build and Platform-Specific Debugging](#build-and-platform-specific-debugging)
- [Collaborative Debugging with AI Tools](#collaborative-debugging-with-ai-tools)
- [LLM-Focused Triage Prompts](#llm-focused-triage-prompts)

## LLM-Focused Triage Prompts
- Paste the exact **error/warning text + stack trace** (include file path and line number).
- State **Unity version** (e.g., 6.3.x), **platform/build type** (Editor/Dev/Release), and **Enter Play Mode Options** (domain/scene reload on/off).
- Give **repro steps** and name the **scene/prefab** and **scripts** involved.
- For **Input/UI**, list the active **action map/control scheme** and **UXML/USS asset names** you are querying.
- Mention any **recent code or asset changes** just before the bug appeared.
- If possible, share a **minimal log snippet** around the failure (no screenshots).

## Diagnostic Priority Order

When investigating Unity issues, check these areas in order:

1. **Console errors and warnings** - Always start here
2. **Null reference exceptions** - Most common Unity issue
3. **Serialization state** - Inspector values vs runtime values
4. **Lifecycle timing** - Script execution order problems
5. **Scene/Prefab state** - Missing references, disabled objects
6. **Physics/Rendering settings** - Layer masks, culling, collision matrices

---

## Console Output Analysis

### Error Categories

| Prefix | Meaning | Typical Cause |
|--------|---------|---------------|
| `NullReferenceException` | Missing object reference | Unassigned SerializeField, destroyed object, wrong execution order |
| `MissingReferenceException` | Reference to destroyed object | Accessing object after Destroy() |
| `MissingComponentException` | GetComponent returned null | Component not attached, wrong type |
| `IndexOutOfRangeException` | Array/List bounds exceeded | Off-by-one errors, empty collections |
| `InvalidOperationException` | Operation not allowed | Modifying collection while iterating |

### Stack Trace Interpretation

```
NullReferenceException: Object reference not set to an instance of an object
  at PlayerController.Update () [0x00012] in Assets/Scripts/PlayerController.cs:47
  at UnityEngine.Internal.$MethodUtility.InvokeMethod (...)
```

**Key information:**
- Script name: `PlayerController`
- Method: `Update()`
- Line number: `47`
- File path: `Assets/Scripts/PlayerController.cs`

### Common Warning Patterns

```csharp
// Warning: "SendMessage cannot be called during Awake, CheckConsistency, or OnValidate"
// Fix: Defer to Start() or use Invoke/Coroutine

// Warning: "The referenced script on this Behaviour is missing!"
// Fix: Script file deleted or class name doesn't match filename

// Warning: "You are trying to create a MonoBehaviour using the 'new' keyword"
// Fix: Use AddComponent<T>() or Instantiate()
```

---

## SerializeField and Inspector Debugging

### Verify Serialization State

Four ways to declare the same reference, and what each does in the Inspector:

| Declaration | Serialized | In Inspector | Verdict |
|---|---|---|---|
| `[SerializeField] private GameObject m_target;` | ✅ | ✅ visible | ✅ Correct |
| `private GameObject m_target;` | ❌ | ❌ absent | The field is null at runtime and you can't assign it |
| `public GameObject Target;` | ✅ | ✅ visible | Works, but breaks encapsulation — avoid |
| `[HideInInspector] public GameObject Target;` | ✅ | ❌ hidden | Deliberate: persisted but not designer-editable |

```csharp
// ✅ The one you want
[SerializeField] private GameObject m_target;
```

⚠️ A field that "won't show up in the Inspector" is almost always the second row — the
`[SerializeField]` attribute is missing. Unity gives no warning for this.

### Runtime vs Inspector Values

```csharp
// Debug serialized values at runtime
private void OnValidate()
{
    Debug.Log($"[Editor] m_target assigned: {m_target != null}");
}

private void Awake()
{
    Debug.Log($"[Runtime] m_target assigned: {m_target != null}");
}
```

### Check for Prefab Overrides

When a SerializeField appears assigned in the Prefab but null at runtime:
1. Check if the scene instance has an override (bold in Inspector)
2. Check if the value was cleared in a prefab variant
3. Check if OnValidate() or Reset() is clearing the value

---

## Script Execution Order Issues

### Unity Lifecycle Order

```
[Script Execution Order]
    ↓
Awake()           ← Object initialization, references to self
    ↓
OnEnable()        ← Subscribe to events
    ↓
Start()           ← References to other objects, initialization that depends on others
    ↓
FixedUpdate()     ← Physics updates (fixed timestep)
    ↓
Update()          ← Game logic (every frame)
    ↓
LateUpdate()      ← Camera follow, post-processing
    ↓
OnDisable()       ← Unsubscribe from events
    ↓
OnDestroy()       ← Cleanup
```

### Diagnosing Order Problems

```csharp
// Add execution order logging
private void Awake()
{
    Debug.Log($"{GetType().Name}.Awake() on {gameObject.name}", this);
}

private void Start()
{
    Debug.Log($"{GetType().Name}.Start() on {gameObject.name}", this);
}
```

### Setting Script Execution Order

```csharp
// Force early execution
[DefaultExecutionOrder(-100)]
public class GameManager : MonoBehaviour { }

// Force late execution
[DefaultExecutionOrder(100)]
public class UIManager : MonoBehaviour { }
```

### Common Timing Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Reference null in `Awake()` | Other object not yet initialized | Move to `Start()` |
| Reference null in `Start()` | Object created later in scene | Use `FindFirstObjectByType` with null check or events |
| Camera jitter | Camera in `Update()`, target in `Update()` | Move camera to `LateUpdate()` |
| Physics inconsistency | Physics logic in `Update()` | Move to `FixedUpdate()` |

- If state resets or Awake/OnEnable timing looks odd, verify **Enter Play Mode Options** (Project Settings → Editor). Domain reload off keeps static state; scene reload off keeps scene state.

---

## Null Reference Debugging

### Systematic Null Checking

```csharp
// Pattern: Validate all SerializeFields in Awake/Start
private void Awake()
{
    Debug.Assert(m_playerTransform != null, "PlayerTransform not assigned!", this);
    Debug.Assert(m_healthBar != null, "HealthBar not assigned!", this);
    Debug.Assert(m_audioSource != null, "AudioSource not assigned!", this);
}

// Pattern: Null-conditional for optional references
m_optionalComponent?.DoSomething();

// Pattern: Explicit null check with error
if (m_requiredComponent == null)
{
    Debug.LogError($"Required component missing on {gameObject.name}", this);
    enabled = false;
    return;
}
```

### GetComponent Failure Patterns

```csharp
// Issue: Component on different GameObject
Rigidbody rb = GetComponent<Rigidbody>();  // Only checks THIS object

// Fix: Specify where to look
Rigidbody rb = GetComponentInChildren<Rigidbody>();
Rigidbody rb = GetComponentInParent<Rigidbody>();
Rigidbody rb = someOtherObject.GetComponent<Rigidbody>();

// Issue: Component added at runtime not yet available
// Fix: Use RequireComponent or check timing
[RequireComponent(typeof(Rigidbody))]
public class PhysicsController : MonoBehaviour { }
```

### Destroyed Object Access

```csharp
// Issue: Accessing destroyed object
private GameObject m_enemy;

private void Update()
{
    // This throws MissingReferenceException after enemy is destroyed
    float dist = Vector3.Distance(transform.position, m_enemy.transform.position);
}

// Fix: Unity's fake null check
if (m_enemy != null)  // Works for destroyed objects
{
    float dist = Vector3.Distance(transform.position, m_enemy.transform.position);
}

// Note: C# null check doesn't catch destroyed objects
if (m_enemy is not null)  // WRONG - doesn't detect destroyed Unity objects
```

---

## Input System Debugging

### Device Connection Issues

```csharp
// Debug: Monitor device changes
private void OnEnable()
{
    InputSystem.onDeviceChange += OnDeviceChange;
}

private void OnDisable()
{
    InputSystem.onDeviceChange -= OnDeviceChange;
}

private void OnDeviceChange(InputDevice device, InputDeviceChange change)
{
    Debug.Log($"Device '{device.displayName}' {change}");
}

// Debug: List all connected devices
private void LogConnectedDevices()
{
    foreach (var device in InputSystem.devices)
    {
        Debug.Log($"Device: {device.displayName} ({device.GetType().Name})");
    }
}
```

### PlayerInput Component Issues

```csharp
// Issue: Actions not firing
// Check 1: Is PlayerInput component enabled?
// Check 2: Is the correct Action Map active?

// Debug: Log all action triggers
private void OnEnable()
{
    var playerInput = GetComponent<PlayerInput>();
    playerInput.onActionTriggered += OnActionTriggered;
}

private void OnActionTriggered(InputAction.CallbackContext context)
{
    Debug.Log($"Action: {context.action.name}, Phase: {context.phase}");
}

// Issue: Wrong action map active
var playerInput = GetComponent<PlayerInput>();
Debug.Log($"Current Action Map: {playerInput.currentActionMap?.name ?? "None"}");

// Fix: Switch action map
playerInput.SwitchCurrentActionMap("Gameplay");
```

### Input Action Debugging

```csharp
// Debug: Check if action is bound
private void DebugAction(InputAction action)
{
    Debug.Log($"Action: {action.name}");
    Debug.Log($"  Enabled: {action.enabled}");
    Debug.Log($"  Bindings: {action.bindings.Count}");

    foreach (var binding in action.bindings)
    {
        Debug.Log($"    Path: {binding.effectivePath}");
    }
}

// Issue: Action enabled but not responding
// Check: Is the binding path correct for the current device?
// Check: Is another action consuming the input?

// Debug: Read action value directly
private void Update()
{
    var moveAction = m_inputActions.Player.Move;
    Vector2 value = moveAction.ReadValue<Vector2>();
    Debug.Log($"Move: {value}, Phase: {moveAction.phase}");
}
```

### Common Input System Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| No input response | Is InputActionAsset assigned? | Assign in Inspector or via code |
| Actions not firing | Is action map enabled? | Call `actionMap.Enable()` |
| Wrong device input | Check control scheme | Verify bindings for target device |
| Input works in Editor only | Is Input System package in build? | Check Player Settings → Active Input Handling |
| Duplicate input events | Multiple PlayerInput components? | Use single PlayerInput or manual action management |

- Use **Input Debugger** (Window → Analysis → Input Debugger) to inspect devices, events, and action states live. Verify the active control scheme matches the connected device.

---

## Physics Debugging

For the rules themselves — which callbacks fire for which Rigidbody combination, collider
limits, and tunnelling — see [Physics](UnityPhysicsInstructions.md).

### Layer and Collision Issues

```csharp
// Debug: Check layer configuration
Debug.Log($"Object layer: {gameObject.layer} ({LayerMask.LayerToName(gameObject.layer)})");

// Debug: Visualize raycast
Debug.DrawRay(origin, direction * maxDistance, Color.red, 2f);

// Debug: Check what layers a LayerMask includes
private void LogLayerMask(LayerMask mask)
{
    for (int i = 0; i < 32; i++)
    {
        if ((mask.value & (1 << i)) != 0)
        {
            Debug.Log($"Layer {i}: {LayerMask.LayerToName(i)}");
        }
    }
}
```

### Collision Matrix Verification

Check Edit → Project Settings → Physics (or Physics 2D):
- Verify layer collision matrix has expected checkboxes enabled
- Both objects must be on layers that collide with each other

### Rigidbody Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| No collision detected | Is Rigidbody present? | Add Rigidbody to at least one object |
| Collision but no callback | Is trigger enabled incorrectly? | Match OnCollision vs OnTrigger methods |
| Objects pass through | Is one kinematic with no continuous detection? | Enable Continuous collision detection |
| Jittery movement | Moving in Update() | Move physics objects in FixedUpdate() |

### Trigger vs Collision Methods

```csharp
// Colliders (IsTrigger = false)
private void OnCollisionEnter(Collision collision) { }
private void OnCollisionStay(Collision collision) { }
private void OnCollisionExit(Collision collision) { }

// Triggers (IsTrigger = true)
private void OnTriggerEnter(Collider other) { }
private void OnTriggerStay(Collider other) { }
private void OnTriggerExit(Collider other) { }

// 2D variants
private void OnCollisionEnter2D(Collision2D collision) { }
private void OnTriggerEnter2D(Collider2D other) { }
```

---

## Animation and Animator Debugging

### Animator State Issues

```csharp
// Debug: Log current animator state
private void Update()
{
    var stateInfo = m_animator.GetCurrentAnimatorStateInfo(0);
    Debug.Log($"State: {stateInfo.shortNameHash}, NormalizedTime: {stateInfo.normalizedTime}");
}

// Debug: Check if specific state is playing
private bool IsPlaying(string stateName)
{
    var stateInfo = m_animator.GetCurrentAnimatorStateInfo(0);
    return stateInfo.IsName(stateName);
}

// Issue: State not transitioning
// Check: Are transition conditions met?
private void DebugTransitionConditions()
{
    Debug.Log($"IsGrounded: {m_animator.GetBool("IsGrounded")}");
    Debug.Log($"Speed: {m_animator.GetFloat("Speed")}");
    Debug.Log($"IsInTransition: {m_animator.IsInTransition(0)}");
}
```

### Animator Parameter Issues

```csharp
// Issue: Parameter not updating
// Check 1: Is parameter name spelled correctly? (case-sensitive)
// Check 2: Is parameter type correct?

// Debug: List all parameters
private void LogAnimatorParameters()
{
    foreach (var param in m_animator.parameters)
    {
        string value = param.type switch
        {
            AnimatorControllerParameterType.Bool => m_animator.GetBool(param.name).ToString(),
            AnimatorControllerParameterType.Float => m_animator.GetFloat(param.name).ToString(),
            AnimatorControllerParameterType.Int => m_animator.GetInteger(param.name).ToString(),
            AnimatorControllerParameterType.Trigger => "(trigger)",
            _ => "unknown"
        };
        Debug.Log($"Param: {param.name} ({param.type}) = {value}");
    }
}

// Best practice: Cache parameter hashes
private static readonly int s_speedHash = Animator.StringToHash("Speed");
private static readonly int s_jumpHash = Animator.StringToHash("Jump");

private void SetSpeed(float speed)
{
    m_animator.SetFloat(s_speedHash, speed);
}
```

### Animation Event Issues

```csharp
// Issue: Animation event not firing
// Check 1: Is the method public?
// Check 2: Does the method signature match?

// Valid animation event methods:
public void OnFootstep() { }                    // No parameters
public void OnFootstep(string sound) { }        // String parameter
public void OnFootstep(float volume) { }        // Float parameter
public void OnFootstep(int index) { }           // Int parameter
public void OnFootstep(AnimationEvent evt) { }  // Full event data

// Debug: Add logging to event method
public void OnFootstep(AnimationEvent evt)
{
    Debug.Log($"Footstep event at time {evt.time}, clip: {evt.animatorClipInfo.clip.name}");
}
```

### Root Motion Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| Character not moving | Apply Root Motion enabled? | Enable on Animator component |
| Movement jittery | Mixing root motion with script movement | Use one or the other, not both |
| Wrong movement direction | Animation import settings | Check Bake Into Pose options |
| Sliding feet | Animation doesn't match speed | Adjust animation or movement speed |

```csharp
// Override root motion in script
private void OnAnimatorMove()
{
    // Custom root motion handling
    Vector3 position = m_animator.rootPosition;
    Quaternion rotation = m_animator.rootRotation;

    // Apply with modifications
    transform.position = position;
    transform.rotation = rotation;
}
```

---

## UI Toolkit Debugging (Unity 6+)

### Common UI Toolkit Issues

```csharp
// Issue: Element not found
var button = root.Q<Button>("myButton");  // Returns null if not found

// Debug: List all elements
root.Query().ForEach(e => Debug.Log($"{e.GetType().Name}: {e.name}"));

// Issue: Styles not applying
// Check: Is the USS file assigned to the UXML?
// Check: Is the selector correct? (use UI Toolkit Debugger)

// Issue: Events not firing
// Check: Is picking mode set correctly?
button.pickingMode = PickingMode.Position;  // Required for interaction
```

### UI Toolkit Debugger

Access via Window → UI Toolkit → Debugger:
- Inspect live element hierarchy
- View computed styles
- Check class lists and inline styles
- Verify picking mode

### Data Binding Issues (Unity 6)

```csharp
// Verify binding path
[CreateAssetMenu]
public class PlayerData : ScriptableObject
{
    public int health;  // Binding path: "health"
}

// In UXML: data-source-path="health"
// Common issue: Path is case-sensitive

// Debug: Verify data source is set
var element = root.Q("health-bar");
Debug.Log($"Data source: {element.dataSource}");
Debug.Log($"Data source type: {element.dataSource?.GetType().Name}");
```

### Runtime Data Source Swapping

```csharp
// Pattern: Design-time mock, runtime real data
private void OnEnable()
{
    var root = GetComponent<UIDocument>().rootVisualElement;
    var pane = root.Q("stats-pane");

    // Swap from mock asset to runtime data
    pane.dataSource = m_playerStats.runtimeData;
}
```

For comprehensive UI Toolkit patterns, see `UIToolkitBestPractices.md` in the project root.

---

## Audio Debugging

### AudioSource Issues

```csharp
// Issue: Sound not playing
// Debug: Check AudioSource state
private void DebugAudioSource(AudioSource source)
{
    Debug.Log($"AudioSource on {source.gameObject.name}:");
    Debug.Log($"  Clip: {source.clip?.name ?? "None"}");
    Debug.Log($"  Volume: {source.volume}");
    Debug.Log($"  Mute: {source.mute}");
    Debug.Log($"  IsPlaying: {source.isPlaying}");
    Debug.Log($"  Enabled: {source.enabled}");
    Debug.Log($"  GameObject Active: {source.gameObject.activeInHierarchy}");
}

// Common issues checklist:
// 1. Is AudioClip assigned?
// 2. Is volume > 0?
// 3. Is AudioListener in scene?
// 4. Is AudioSource not muted?
// 5. Is GameObject active?
```

### Spatial Audio Issues

```csharp
// Issue: 3D sound not working
// Check: Spatial Blend setting (0 = 2D, 1 = 3D)
m_audioSource.spatialBlend = 1f;  // Fully 3D

// Check: Distance settings
Debug.Log($"Min Distance: {m_audioSource.minDistance}");
Debug.Log($"Max Distance: {m_audioSource.maxDistance}");

// Debug: Distance to listener
var listener = FindFirstObjectByType<AudioListener>();
if (listener != null)
{
    float distance = Vector3.Distance(transform.position, listener.transform.position);
    Debug.Log($"Distance to listener: {distance}");
}
```

### AudioMixer Issues

```csharp
// Issue: Mixer parameter not changing
// Check: Is parameter exposed? (right-click in Mixer → Expose)

// Debug: Get current mixer values
float value;
if (m_mixer.GetFloat("MasterVolume", out value))
{
    Debug.Log($"MasterVolume: {value} dB");
}
else
{
    Debug.LogError("Parameter 'MasterVolume' not found or not exposed");
}

// Note: Mixer uses decibels (-80 to 0), not linear (0 to 1)
// Convert linear to dB:
float LinearToDecibel(float linear)
{
    return linear > 0 ? 20f * Mathf.Log10(linear) : -80f;
}
```

### Common Audio Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| No sound at all | Is AudioListener in scene? | Add AudioListener to camera |
| Sound plays once only | Is Play() called multiple times? | Check loop setting or call Play() again |
| 3D sound always same volume | Is Spatial Blend set to 3D? | Set Spatial Blend to 1 |
| Sound cuts off | Max Distance too small? | Increase Max Distance |
| Mixer not affecting sound | Is AudioSource output set to mixer? | Assign Output in AudioSource |

---

## Async and Coroutine Debugging

### Coroutine Issues

```csharp
// Issue: Coroutine stops unexpectedly
// Cause: GameObject disabled or destroyed

// Debug: Track coroutine lifecycle
private IEnumerator MyCoroutine()
{
    Debug.Log("Coroutine started");
    try
    {
        while (true)
        {
            yield return new WaitForSeconds(1f);
            Debug.Log("Coroutine tick");
        }
    }
    finally
    {
        Debug.Log("Coroutine ended");  // Called even when stopped
    }
}

// Issue: Multiple coroutines running
// Fix: Store and stop reference
private Coroutine m_currentCoroutine;

public void StartMyCoroutine()
{
    if (m_currentCoroutine != null)
        StopCoroutine(m_currentCoroutine);
    m_currentCoroutine = StartCoroutine(MyCoroutine());
}
```

### Async/Await Issues (Legacy Pattern)

```csharp
// Issue: Async method continues after object destroyed
private async void Start()
{
    await SomeAsyncOperation();
    // This line may execute after Destroy()!
    transform.position = Vector3.zero;  // Potential error
}

// Fix: Check for destruction
private async void Start()
{
    await SomeAsyncOperation();

    if (this == null) return;  // Unity's destroyed check

    transform.position = Vector3.zero;
}
```

### Awaitable API (Unity 6)

```csharp
// Unity 6 preferred pattern: Use Awaitable with destroyCancellationToken
private async Awaitable DoSomethingAsync()
{
    // Automatically cancelled when MonoBehaviour is destroyed
    await Awaitable.WaitForSecondsAsync(1f, destroyCancellationToken);

    // Safe to access - this line won't run if destroyed
    transform.position = Vector3.zero;
}

// Wait for next frame
private async Awaitable WaitOneFrame()
{
    await Awaitable.NextFrameAsync(destroyCancellationToken);
}

// Wait for end of frame
private async Awaitable WaitEndOfFrame()
{
    await Awaitable.EndOfFrameAsync(destroyCancellationToken);
}

// Wait for fixed update
private async Awaitable WaitForPhysics()
{
    await Awaitable.FixedUpdateAsync(destroyCancellationToken);
}

// Custom cancellation
private CancellationTokenSource m_cts;

private async Awaitable DoWithCustomCancellation()
{
    m_cts = new CancellationTokenSource();

    try
    {
        await Awaitable.WaitForSecondsAsync(5f, m_cts.Token);
        Debug.Log("Completed");
    }
    catch (OperationCanceledException)
    {
        Debug.Log("Cancelled");
    }
}

public void Cancel() => m_cts?.Cancel();
```

### Awaitable vs Coroutine Comparison

| Feature | Coroutine | Awaitable (Unity 6) |
|---------|-----------|---------------------|
| Cancellation | Manual StopCoroutine | Built-in token support |
| Return values | Not supported | Supported via `Awaitable<T>` |
| Exception handling | Limited | Full try/catch support |
| Destruction safety | Must check manually | `destroyCancellationToken` |
| Syntax | `yield return` | `async/await` |

---

## Event System Debugging

### UnityEvent Issues

```csharp
// Issue: UnityEvent not firing
// Debug: Check listener count
Debug.Log($"Listener count: {m_onPlayerDeath.GetPersistentEventCount()}");

// Check: Are listeners assigned in Inspector?
// Check: Is the target object not destroyed?
// Check: Is the method signature correct?

// Debug: Log when event fires
[SerializeField] private UnityEvent m_onPlayerDeath;

public void Die()
{
    Debug.Log($"Invoking OnPlayerDeath with {m_onPlayerDeath.GetPersistentEventCount()} listeners");
    m_onPlayerDeath?.Invoke();
}
```

### C# Event Subscription Leaks

```csharp
// Issue: Event keeps firing after object should be done
// Cause: Forgot to unsubscribe

// BAD: Memory leak and potential errors
private void Start()
{
    GameManager.OnGameOver += HandleGameOver;  // Subscribes
    // Never unsubscribes!
}

// GOOD: Always unsubscribe
private void OnEnable()
{
    GameManager.OnGameOver += HandleGameOver;
}

private void OnDisable()
{
    GameManager.OnGameOver -= HandleGameOver;
}

// Debug: Track subscriptions
public static class GameManager
{
    private static event Action m_onGameOver;

    public static event Action OnGameOver
    {
        add
        {
            Debug.Log($"Subscriber added: {value.Target?.GetType().Name}.{value.Method.Name}");
            m_onGameOver += value;
        }
        remove
        {
            Debug.Log($"Subscriber removed: {value.Target?.GetType().Name}.{value.Method.Name}");
            m_onGameOver -= value;
        }
    }
}
```

### Event Invocation Order

```csharp
// Issue: Events firing in wrong order
// Debug: Log invocation order

public event Action<int> OnScoreChanged;

private void AddScore(int points)
{
    m_score += points;

    // Log each subscriber as it's called
    if (OnScoreChanged != null)
    {
        int index = 0;
        foreach (var handler in OnScoreChanged.GetInvocationList())
        {
            Debug.Log($"Calling handler {index++}: {handler.Target?.GetType().Name}.{handler.Method.Name}");
            ((Action<int>)handler).Invoke(m_score);
        }
    }
}
```

### Common Event Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| Event never fires | Is Invoke() called? | Add null check and Invoke |
| Event fires multiple times | Subscribed multiple times? | Unsubscribe in OnDisable |
| NullReference on Invoke | No subscribers? | Use `?.Invoke()` pattern |
| Wrong object receives event | Static event with instance handler? | Unsubscribe on disable/destroy |

---

## ScriptableObject Runtime Issues

### Instance vs Asset Confusion

```csharp
// Issue: Runtime changes persist in Editor
[SerializeField] private PlayerDataSO m_playerData;

private void TakeDamage(int damage)
{
    m_playerData.health -= damage;  // Modifies the ASSET in Editor!
}

// Fix: Create runtime instance
private PlayerDataSO m_runtimeData;

private void Awake()
{
    // Create a copy for runtime modifications
    m_runtimeData = Instantiate(m_playerData);
}

private void TakeDamage(int damage)
{
    m_runtimeData.health -= damage;  // Safe - modifies instance only
}

private void OnDestroy()
{
    // Clean up runtime instance
    if (m_runtimeData != null)
        Destroy(m_runtimeData);
}
```

### ScriptableObject as Runtime Data Container

```csharp
// Pattern: Create SO at runtime for data binding
public class RuntimeDataProvider : MonoBehaviour
{
    [SerializeField] private PlayerDataSO m_template;

    private PlayerDataSO m_runtimeData;

    public PlayerDataSO RuntimeData
    {
        get
        {
            if (m_runtimeData == null)
            {
                m_runtimeData = ScriptableObject.CreateInstance<PlayerDataSO>();
                m_runtimeData.hideFlags = HideFlags.HideAndDontSave;

                // Copy initial values from template
                m_runtimeData.health = m_template.health;
                m_runtimeData.maxHealth = m_template.maxHealth;
            }
            return m_runtimeData;
        }
    }
}
```

### Shared Reference Issues

```csharp
// Issue: Multiple objects sharing same SO modify each other's data
// This is INTENTIONAL for shared state, but a bug if unexpected

// Debug: Log which object is modifying
public void ModifyHealth(int delta, string source)
{
    Debug.Log($"Health modified by {delta} from {source}. New value: {health + delta}");
    health += delta;
}

// Fix if unintentional: Each object needs its own instance
private void Awake()
{
    m_playerData = Instantiate(m_playerData);
}
```

### Common ScriptableObject Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| Changes persist after play mode | Modifying asset directly? | Use Instantiate() for runtime copy |
| Multiple objects share state | Same SO assigned to all? | Intentional: shared state. Unintentional: instantiate |
| SO reference null at runtime | Asset not in build? | Check Resources folder or Addressables |
| OnEnable called in Editor | Normal behavior | Use `Application.isPlaying` check |

---

## Transform and Hierarchy Issues

### Local vs World Space

```csharp
// Issue: Position not where expected
// Debug: Log both spaces
Debug.Log($"Local Position: {transform.localPosition}");
Debug.Log($"World Position: {transform.position}");
Debug.Log($"Parent: {transform.parent?.name ?? "None"}");

// Common confusion:
transform.position = new Vector3(0, 0, 0);      // World space
transform.localPosition = new Vector3(0, 0, 0); // Relative to parent

// Issue: Rotation behaving unexpectedly
Debug.Log($"Local Rotation: {transform.localEulerAngles}");
Debug.Log($"World Rotation: {transform.eulerAngles}");
```

### Parent-Child Relationship Bugs

```csharp
// Issue: Child transform not updating
// Check: Is parent transform being modified?

// Debug: Log hierarchy
private void LogHierarchy(Transform t, int depth = 0)
{
    string indent = new string(' ', depth * 2);
    Debug.Log($"{indent}{t.name} (pos: {t.localPosition}, scale: {t.localScale})");

    foreach (Transform child in t)
    {
        LogHierarchy(child, depth + 1);
    }
}

// Issue: SetParent not working as expected
transform.SetParent(newParent);              // Maintains world position
transform.SetParent(newParent, false);       // Maintains local position
transform.SetParent(newParent, true);        // Maintains world position (explicit)
```

### Scale Inheritance Issues

```csharp
// Issue: Child scaled unexpectedly
// Debug: Check lossy scale (world scale)
Debug.Log($"Local Scale: {transform.localScale}");
Debug.Log($"Lossy Scale: {transform.lossyScale}");  // Accumulated scale

// Issue: Non-uniform parent scale causes skewing
// Fix: Avoid non-uniform scale on parents, or unparent before scaling

// Get world scale without parent influence
Vector3 GetWorldScaleIndependent()
{
    Vector3 scale = transform.localScale;
    Transform parent = transform.parent;

    while (parent != null)
    {
        scale = Vector3.Scale(scale, parent.localScale);
        parent = parent.parent;
    }

    return scale;
}
```

### Common Transform Issues

| Symptom | Check | Solution |
|---------|-------|----------|
| Object in wrong position | Local vs world space? | Use correct position property |
| Object doesn't move with parent | Is it actually a child? | Verify hierarchy in Inspector |
| Scale looks wrong | Parent has non-uniform scale? | Avoid or compensate for parent scale |
| Rotation gimbal lock | Using Euler angles? | Use Quaternion for complex rotations |

---

## Performance Debugging

### Profiler Markers

```csharp
using Unity.Profiling;

private static readonly ProfilerMarker s_updateMarker = new ProfilerMarker("MyScript.Update");

private void Update()
{
    using (s_updateMarker.Auto())
    {
        // Code to profile
    }
}
```

### Common Performance Issues

| Symptom | Diagnostic | Solution |
|---------|------------|----------|
| Frame rate drops | Profiler → CPU | Identify expensive methods |
| Memory grows | Profiler → Memory | Check for leaks, pooling |
| GC spikes | Profiler → GC Alloc | Reduce allocations in Update |
| GPU bound | Frame Debugger | Reduce draw calls, overdraw |

### Allocation-Free Patterns

```csharp
// BAD: Allocates every frame and scans the whole scene
private void Update()
{
    var enemies = FindObjectsByType<Enemy>(FindObjectsSortMode.None); // Scan + array alloc
    string log = $"Count: {enemies.Length}";                          // Allocates string
}

// GOOD: Keep a registry, reuse the builder
private readonly List<Enemy> m_activeEnemies = new(100);  // Enemies add/remove themselves
private readonly StringBuilder m_statusBuilder = new(64);

private void Update()
{
    m_statusBuilder.Clear();
    m_statusBuilder.Append("Count: ").Append(m_activeEnemies.Count);  // No allocation
}
```

---

## Scene and Asset Debugging

### Missing Reference Detection

```csharp
#if UNITY_EDITOR
[ContextMenu("Find Missing References")]
private void FindMissingReferences()
{
    var fields = GetType().GetFields(
        System.Reflection.BindingFlags.Public |
        System.Reflection.BindingFlags.NonPublic |
        System.Reflection.BindingFlags.Instance);

    foreach (var field in fields)
    {
        if (typeof(UnityEngine.Object).IsAssignableFrom(field.FieldType))
        {
            var value = field.GetValue(this) as UnityEngine.Object;
            if (value == null)
            {
                Debug.LogWarning($"Missing reference: {field.Name}", this);
            }
        }
    }
}
#endif
```

### Prefab Issues

- **Prefab Mode**: Changes in Prefab Mode don't affect scene instances with overrides
- **Nested Prefabs**: Inner prefab changes may not propagate if outer prefab has overrides
- **Prefab Variants**: Check the base prefab for missing references

---

## Build and Platform-Specific Debugging

### Conditional Compilation

```csharp
#if UNITY_EDITOR
    Debug.Log("Editor only");
#endif

#if DEVELOPMENT_BUILD
    Debug.Log("Development build");
#endif

#if UNITY_STANDALONE_WIN
    // Windows-specific code
#elif UNITY_STANDALONE_OSX
    // macOS-specific code
#elif UNITY_IOS
    // iOS-specific code
#elif UNITY_ANDROID
    // Android-specific code
#endif
```

### Build-Only Issues

Common causes for "works in Editor, fails in build":
1. **Script stripping**: Add `[Preserve]` attribute or link.xml
2. **Assembly definitions**: Missing references in .asmdef
3. **Resources path**: Case sensitivity on some platforms
4. **Editor-only code**: Wrapped in `#if UNITY_EDITOR`

---

## Collaborative Debugging with AI Tools

AI coding assistants (like Claude Code) cannot directly control IDE debuggers but can effectively assist with debugging through a collaborative workflow.

### What AI Tools Can Do

| Capability | Method |
|------------|--------|
| Read IDE diagnostics | Access compiler errors and warnings via MCP |
| Analyze code flow | Trace logic paths, identify potential issues |
| Add diagnostic code | Insert targeted logging, assertions |
| Interpret errors | Explain stack traces, suggest causes |
| Suggest fixes | Propose code changes based on analysis |

### What Requires Human Interaction

| Capability | Reason |
|------------|--------|
| Set breakpoints | Requires IDE UI interaction |
| Step through code | Real-time interactive process |
| Inspect runtime variables | Requires active debug session |
| Evaluate watch expressions | Requires debugger context |
| View call stack at breakpoint | Requires paused execution |

### Effective Collaboration Workflow

**Step 1: Describe the Issue**
```
Error: NullReferenceException in PlayerController.Update() line 47
Repro: Start game, press jump button
Expected: Player jumps
Actual: Exception thrown, player frozen
```

**Step 2: AI Analyzes Code**
The AI reads relevant files, traces execution flow, and identifies suspects.

**Step 3: AI Adds Diagnostic Code**
```csharp
private void Update()
{
    // Diagnostic logging added by AI
    Debug.Log($"[DEBUG] m_inputHandler: {m_inputHandler != null}", this);
    Debug.Log($"[DEBUG] m_characterController: {m_characterController != null}", this);
    Debug.Log($"[DEBUG] m_isGrounded: {m_isGrounded}", this);

    HandleMovement();
    HandleJump();  // Line 47 - exception occurs here
}
```

**Step 4: Human Runs and Reports**
Share the console output with the AI.

**Step 5: AI Interprets and Fixes**
Based on logs, the AI identifies the null reference and proposes a fix.

### Programmatic Breakpoints

When you need the debugger to pause at a specific condition:

```csharp
private void Update()
{
    // Pause debugger when unexpected state occurs
    if (m_health < 0)
    {
        Debug.LogError("Health went negative - breaking to debugger");
        System.Diagnostics.Debugger.Break();  // Rider/VS will pause here
    }

    // Conditional break with context logging
    if (m_player == null && m_wasPlayerValid)
    {
        Debug.LogError($"Player reference lost! Last valid frame: {m_lastValidFrame}");
        System.Diagnostics.Debugger.Break();
    }
}
```

### Diagnostic Code Patterns

**Trace Method Entry/Exit**
```csharp
private void ProcessInput()
{
    Debug.Log($"→ {nameof(ProcessInput)} entered", this);

    // ... method logic ...

    Debug.Log($"← {nameof(ProcessInput)} exiting", this);
}
```

**State Snapshot**
```csharp
[ContextMenu("Log State Snapshot")]
private void LogStateSnapshot()
{
    Debug.Log("=== STATE SNAPSHOT ===");
    Debug.Log($"Position: {transform.position}");
    Debug.Log($"Velocity: {m_rigidbody?.linearVelocity}");
    Debug.Log($"IsGrounded: {m_isGrounded}");
    Debug.Log($"CurrentState: {m_currentState}");
    Debug.Log($"InputVector: {m_inputVector}");
    Debug.Log("======================");
}
```

**Conditional Logging (Editor Only)**
```csharp
[System.Diagnostics.Conditional("UNITY_EDITOR")]
private void DebugLog(string message)
{
    Debug.Log($"[{GetType().Name}] {message}", this);
}

// Usage - automatically stripped from builds
DebugLog($"Processing {m_items.Count} items");
```

### Tips for Effective AI-Assisted Debugging

1. **Provide context**: Include error messages, stack traces, and repro steps
2. **Share console output**: Copy/paste the actual log output after running
3. **Describe expected vs actual**: What should happen vs what does happen
4. **Mention recent changes**: What was modified before the bug appeared
5. **Include relevant settings**: Unity version, platform, Enter Play Mode Options

---

## Learn more

- [Debugging C# code in Unity](https://docs.unity3d.com/6000.3/Documentation/Manual/managed-code-debugging.html)
- [Console window](https://docs.unity3d.com/6000.3/Documentation/Manual/Console.html)
- [Frame Debugger](https://docs.unity3d.com/6000.3/Documentation/Manual/FrameDebugger.html)
