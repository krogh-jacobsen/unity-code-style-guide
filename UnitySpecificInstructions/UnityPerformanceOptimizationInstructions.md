# Unity Performance Optimization Instructions for LLM Coding Tools

Use this guide when reviewing Unity projects for performance issues. These instructions help identify common bottlenecks and suggest optimizations that Claude can apply when analyzing code structure and project organization.

Table of contents:
- [Unity Version-Specific Notes](#unity-version-specific-notes)
- [Code Review Priority Checklist](#code-review-priority-checklist)
- [Update Loop Optimization](#update-loop-optimization)
    - [Avoiding Per-Frame Allocations](#avoiding-per-frame-allocations)
    - [Caching Expensive Operations](#caching-expensive-operations)
    - [Throttling Update Logic](#throttling-update-logic)
- [Memory Management](#memory-management)
    - [String Operations](#string-operations)
    - [Collections and Allocations](#collections-and-allocations)
    - [Boxing and Unboxing](#boxing-and-unboxing)
- [Object Pooling](#object-pooling)
- [Physics Optimization](#physics-optimization)
- [Rendering Considerations](#rendering-considerations)
- [GetComponent and Find Operations](#getcomponent-and-find-operations)
- [LINQ and Delegates](#linq-and-delegates)
- [Async and Coroutine Patterns](#async-and-coroutine-patterns)
- [Data Structure Selection](#data-structure-selection)
- [Unity API Best Practices](#unity-api-best-practices)
- [Profiling Markers](#profiling-markers)
- [Common Anti-Patterns](#common-anti-patterns)

---

# Unity Version-Specific Notes

- ℹ️ Unity 6 introduces `Awaitable` which is more performant than coroutines for simple delays and sequences.
- ℹ️ Unity 6's `UnityEngine.Pool.ObjectPool<T>` should be preferred over custom pooling implementations.
- ℹ️ The Burst compiler can dramatically improve performance for math-heavy code when used with the Jobs system.
- ℹ️ IL2CPP builds have different performance characteristics than Mono—profile on target platform.

---

# Code Review Priority Checklist

When reviewing Unity code for performance, check these areas in order of impact:

1. **Update loops** — Allocations, expensive operations, unnecessary work
2. **Physics** — OverlapSphere, Raycast frequency, collision matrix
3. **Memory** — String concatenation, LINQ in hot paths, boxing
4. **GetComponent/Find** — Uncached lookups, per-frame calls
5. **Rendering** — Material instances, shader keywords, draw calls

---

# Update Loop Optimization

## Avoiding Per-Frame Allocations

- ❌ **Never allocate in Update(), FixedUpdate(), or LateUpdate()** — This triggers garbage collection spikes.
- ❌ Avoid `new` keyword for reference types in update loops.
- ❌ Avoid string concatenation or interpolation in update loops.
- ❌ Avoid LINQ queries in update loops.
- ✅ Pre-allocate collections and reuse them with `.Clear()`.
- ✅ Use object pooling for frequently instantiated objects.

```csharp
// ❌ Bad - allocates every frame
private void Update()
{
    var enemies = FindObjectsOfType<Enemy>();           // Allocates array
    var nearbyEnemies = new List<Enemy>();              // Allocates list
    string status = $"Enemies: {enemies.Length}";      // Allocates string
    
    foreach (var enemy in enemies.Where(e => e.IsAlive)) // LINQ allocates
    {
        nearbyEnemies.Add(enemy);
    }
}

// ✅ Good - zero allocations in update
private Enemy[] m_enemyCache = new Enemy[100];
private readonly List<Enemy> m_nearbyEnemies = new(50);
private readonly StringBuilder m_statusBuilder = new(64);

private void Update()
{
    int count = FindObjectsOfType(m_enemyCache);       // Reuses array
    
    m_nearbyEnemies.Clear();                            // Reuses list
    for (int i = 0; i < count; i++)
    {
        if (m_enemyCache[i].IsAlive)
        {
            m_nearbyEnemies.Add(m_enemyCache[i]);
        }
    }
    
    m_statusBuilder.Clear();                            // Reuses StringBuilder
    m_statusBuilder.Append("Enemies: ").Append(count);
}
```

## Caching Expensive Operations

- ✅ Cache results of expensive calculations outside Update when possible.
- ✅ Use dirty flags to recalculate only when state changes.
- ✅ Cache Transform, Rigidbody, and other component references in Awake().
- ❌ Avoid accessing `transform`, `gameObject`, or calling GetComponent every frame.

```csharp
// ❌ Bad - repeated property access and calculations
private void Update()
{
    Vector3 pos = transform.position;                   // Property access overhead
    Vector3 targetDir = (m_target.transform.position - pos).normalized;
    float distance = Vector3.Distance(transform.position, m_target.transform.position);
}

// ✅ Good - cached references and calculations
private Transform m_transform;
private Transform m_targetTransform;
private Vector3 m_cachedTargetDirection;
private float m_cachedDistance;
private bool m_isDirty = true;

private void Awake()
{
    m_transform = transform;                            // Cache once
    m_targetTransform = m_target.transform;
}

private void Update()
{
    if (m_isDirty)
    {
        Vector3 offset = m_targetTransform.position - m_transform.position;
        m_cachedDistance = offset.magnitude;
        m_cachedTargetDirection = offset / m_cachedDistance; // Avoid double sqrt
        m_isDirty = false;
    }
}
```

## Throttling Update Logic

- ✅ Spread expensive work across multiple frames.
- ✅ Use time-based throttling for non-critical updates.
- ✅ Consider using coroutines or Awaitable for periodic checks.
- ⚠️ Be mindful of frame-rate dependent behavior when throttling.

```csharp
// ✅ Good - throttled updates
[SerializeField] private float m_updateInterval = 0.1f;
private float m_nextUpdateTime;

private void Update()
{
    if (Time.time < m_nextUpdateTime) return;           // Skip until interval
    
    m_nextUpdateTime = Time.time + m_updateInterval;
    PerformExpensiveOperation();
}

// ✅ Good - staggered processing across frames
private int m_currentIndex;
private const int k_itemsPerFrame = 10;

private void Update()
{
    int endIndex = Mathf.Min(m_currentIndex + k_itemsPerFrame, m_items.Count);
    
    for (int i = m_currentIndex; i < endIndex; i++)
    {
        ProcessItem(m_items[i]);
    }
    
    m_currentIndex = endIndex >= m_items.Count ? 0 : endIndex;
}
```

---

# Memory Management

## String Operations

- ❌ Never use string concatenation (`+`) in loops or frequent code paths.
- ❌ Avoid `string.Format()` in hot paths — it allocates.
- ✅ Use `StringBuilder` for building strings dynamically.
- ✅ Cache formatted strings when values don't change frequently.
- ✅ Use `string.Create()` or `Span<char>` for advanced zero-allocation scenarios.

```csharp
// ❌ Bad - multiple allocations
private void UpdateUI()
{
    m_scoreText.text = "Score: " + m_score;                     // 2 allocations
    m_healthText.text = string.Format("HP: {0}/{1}", m_hp, m_maxHp); // Allocates
}

// ✅ Good - cached and pooled
private readonly StringBuilder m_sb = new(32);
private int m_lastScore = -1;
private string m_cachedScoreText;

private void UpdateUI()
{
    if (m_score != m_lastScore)
    {
        m_sb.Clear();
        m_sb.Append("Score: ").Append(m_score);
        m_cachedScoreText = m_sb.ToString();                    // Only allocate on change
        m_lastScore = m_score;
    }
    m_scoreText.text = m_cachedScoreText;
}
```

## Collections and Allocations

- ✅ Initialize collections with expected capacity to avoid resizing.
- ✅ Prefer `List<T>.Clear()` over creating new lists.
- ✅ Use `CollectionPool<T>` or `ListPool<T>` from Unity's pooling utilities.
- ❌ Avoid `ToArray()`, `ToList()` in performance-critical code.
- ✅ Use `Span<T>` and `stackalloc` for temporary small arrays.

```csharp
// ❌ Bad - resizing allocations
private void ProcessEnemies()
{
    var enemies = new List<Enemy>();                    // No capacity, will resize
    // ... add many items
}

// ✅ Good - pre-sized capacity
private readonly List<Enemy> m_enemies = new(100);     // Expected max capacity

// ✅ Good - using Unity's pooling
using UnityEngine.Pool;

private void ProcessWithPool()
{
    var tempList = ListPool<Enemy>.Get();
    try
    {
        // Use tempList...
    }
    finally
    {
        ListPool<Enemy>.Release(tempList);
    }
}

// ✅ Good - stackalloc for small temporary arrays (C# 7.2+)
private void ProcessSmallBatch()
{
    Span<int> indices = stackalloc int[8];             // No heap allocation
    // Use indices...
}
```

## Boxing and Unboxing

- ❌ Avoid passing value types to methods expecting `object`.
- ❌ Avoid storing value types in non-generic collections.
- ✅ Use generic collections (`List<int>` not `ArrayList`).
- ✅ Use generic methods and interfaces to avoid boxing.
- ⚠️ Watch for hidden boxing in string interpolation with value types.

```csharp
// ❌ Bad - boxing occurs
object boxed = 42;                                      // Boxing
int unboxed = (int)boxed;                              // Unboxing

ArrayList oldList = new ArrayList();
oldList.Add(42);                                        // Boxing

Debug.Log($"Value: {myStruct}");                       // May box if no override

// ✅ Good - no boxing
List<int> genericList = new List<int>();
genericList.Add(42);                                    // No boxing

Debug.Log($"Value: {myInt}");                          // Primitives handled efficiently
```

---

# Object Pooling

- ✅ Use `UnityEngine.Pool.ObjectPool<T>` for frequently spawned objects (bullets, particles, UI elements).
- ✅ Implement `IDisposable` pattern or use `actionOnRelease` to reset object state.
- ✅ Set appropriate `defaultCapacity` and `maxSize` based on expected usage.
- ❌ Don't use `Instantiate`/`Destroy` for objects spawned more than a few times per second.
- ⚠️ Remember to return objects to the pool — leaked pooled objects defeat the purpose.

```csharp
using UnityEngine;
using UnityEngine.Pool;

public class ProjectilePool : MonoBehaviour
{
    [SerializeField] private Projectile m_prefab;
    [SerializeField] private int m_defaultCapacity = 20;
    [SerializeField] private int m_maxSize = 100;
    
    private ObjectPool<Projectile> m_pool;

    private void Awake()
    {
        m_pool = new ObjectPool<Projectile>(
            createFunc: CreateProjectile,
            actionOnGet: OnGetFromPool,
            actionOnRelease: OnReturnToPool,
            actionOnDestroy: OnDestroyPooled,
            collectionCheck: false,                     // Disable in release for perf
            defaultCapacity: m_defaultCapacity,
            maxSize: m_maxSize
        );
    }

    private Projectile CreateProjectile()
    {
        var proj = Instantiate(m_prefab);
        proj.SetPool(m_pool);                           // Give projectile pool reference
        return proj;
    }

    private void OnGetFromPool(Projectile proj)
    {
        proj.gameObject.SetActive(true);
        proj.ResetState();
    }

    private void OnReturnToPool(Projectile proj)
    {
        proj.gameObject.SetActive(false);
    }

    private void OnDestroyPooled(Projectile proj)
    {
        Destroy(proj.gameObject);
    }

    public Projectile Get() => m_pool.Get();
    public void Return(Projectile proj) => m_pool.Release(proj);
}
```

---

# Physics Optimization

- ✅ Use layer masks to limit physics queries to relevant layers.
- ✅ Cache `LayerMask` values — don't call `LayerMask.GetMask()` every frame.
- ✅ Use non-allocating physics methods: `Physics.RaycastNonAlloc`, `Physics.OverlapSphereNonAlloc`.
- ✅ Prefer simple colliders (sphere, capsule, box) over mesh colliders.
- ❌ Avoid physics queries in Update — use FixedUpdate or throttle them.
- ✅ Configure the Physics collision matrix to disable unnecessary layer interactions.

```csharp
// ❌ Bad - allocating physics query every frame
private void Update()
{
    Collider[] hits = Physics.OverlapSphere(transform.position, m_radius);
    foreach (var hit in hits)
    {
        // Process...
    }
}

// ✅ Good - non-allocating with cached arrays and layer mask
private readonly Collider[] m_hitBuffer = new Collider[32];
private LayerMask m_enemyLayer;

private void Awake()
{
    m_enemyLayer = LayerMask.GetMask("Enemy");          // Cache layer mask
}

private void FixedUpdate()
{
    int hitCount = Physics.OverlapSphereNonAlloc(
        transform.position, 
        m_radius, 
        m_hitBuffer,
        m_enemyLayer                                     // Only check enemy layer
    );
    
    for (int i = 0; i < hitCount; i++)
    {
        ProcessHit(m_hitBuffer[i]);
    }
}
```

## Raycast Optimization

- ✅ Use `Physics.Raycast` with `maxDistance` parameter to limit range.
- ✅ Use `QueryTriggerInteraction.Ignore` if you don't need trigger colliders.
- ✅ For multiple raycasts, consider `Physics.RaycastCommand` with Jobs for batching.

```csharp
// ✅ Good - optimized raycast
private RaycastHit m_hitInfo;
private const float k_maxRayDistance = 100f;

private bool CheckLineOfSight(Vector3 origin, Vector3 direction)
{
    return Physics.Raycast(
        origin,
        direction,
        out m_hitInfo,
        k_maxRayDistance,
        m_lineOfSightMask,
        QueryTriggerInteraction.Ignore
    );
}
```

---

# Rendering Considerations

- ⚠️ Accessing `.material` creates a material instance — use `.sharedMaterial` when possible.
- ✅ Batch material property changes using `MaterialPropertyBlock`.
- ✅ Use `Renderer.GetPropertyBlock` / `SetPropertyBlock` for per-instance changes.
- ❌ Avoid changing materials at runtime unless necessary.
- ✅ Use GPU instancing for many similar objects.

```csharp
// ❌ Bad - creates material instance per object
private void Start()
{
    GetComponent<Renderer>().material.color = Color.red; // Creates instance!
}

// ✅ Good - uses MaterialPropertyBlock (no allocation after first call)
private static readonly int k_colorId = Shader.PropertyToID("_Color");
private MaterialPropertyBlock m_propertyBlock;
private Renderer m_renderer;

private void Awake()
{
    m_renderer = GetComponent<Renderer>();
    m_propertyBlock = new MaterialPropertyBlock();
}

private void SetColor(Color color)
{
    m_renderer.GetPropertyBlock(m_propertyBlock);
    m_propertyBlock.SetColor(k_colorId, color);
    m_renderer.SetPropertyBlock(m_propertyBlock);
}
```

## Shader Property IDs

- ✅ Cache shader property IDs with `Shader.PropertyToID()`.
- ❌ Never use string-based property access in update loops.

```csharp
// ❌ Bad - string lookup every call
m_material.SetFloat("_Intensity", value);

// ✅ Good - cached ID
private static readonly int k_intensityId = Shader.PropertyToID("_Intensity");

private void UpdateShader(float value)
{
    m_material.SetFloat(k_intensityId, value);
}
```

---

# GetComponent and Find Operations

- ❌ **Never call GetComponent in Update** — cache in Awake/Start.
- ❌ Avoid `FindObjectOfType`, `FindObjectsOfType` at runtime — they are O(n) scene scans.
- ❌ Avoid `GameObject.Find` — string-based, searches entire hierarchy.
- ✅ Use `[SerializeField]` to assign references in the Inspector.
- ✅ Use `TryGetComponent` for null-safe lookups (slightly faster than GetComponent + null check).
- ✅ Use dependency injection or service locators for cross-system references.

```csharp
// ❌ Bad - expensive lookups every frame
private void Update()
{
    var rb = GetComponent<Rigidbody>();                 // Lookup every frame
    var player = FindObjectOfType<Player>();           // Scene scan every frame
    var enemy = GameObject.Find("Enemy");              // String search every frame
}

// ✅ Good - cached references
[SerializeField] private Rigidbody m_rigidbody;
[SerializeField] private Player m_player;
private Transform m_cachedTransform;

private void Awake()
{
    m_cachedTransform = transform;
    
    // Cache if not assigned in Inspector
    if (m_rigidbody == null)
    {
        TryGetComponent(out m_rigidbody);
    }
}

private void Update()
{
    // Use cached references
    m_rigidbody.AddForce(Vector3.up);
}
```

## RequireComponent Pattern

- ✅ Use `[RequireComponent]` to ensure dependencies exist and enable caching confidence.

```csharp
[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(Collider))]
public class PhysicsController : MonoBehaviour
{
    private Rigidbody m_rigidbody;
    private Collider m_collider;

    private void Awake()
    {
        // Safe to cache — RequireComponent guarantees existence
        m_rigidbody = GetComponent<Rigidbody>();
        m_collider = GetComponent<Collider>();
    }
}
```

---

# LINQ and Delegates

- ❌ **Never use LINQ in Update loops** — most LINQ methods allocate.
- ❌ Avoid lambda expressions in hot paths — they can allocate closures.
- ✅ Use explicit loops instead of LINQ for performance-critical code.
- ✅ Cache delegates when subscribing to events repeatedly.
- ⚠️ LINQ is fine for initialization, editor code, or infrequent operations.

```csharp
// ❌ Bad - LINQ allocations in Update
private void Update()
{
    var activeEnemies = m_enemies.Where(e => e.IsActive).ToList();
    var closestEnemy = m_enemies.OrderBy(e => e.Distance).FirstOrDefault();
}

// ✅ Good - explicit loops, no allocations
private Enemy m_closestEnemy;
private readonly List<Enemy> m_activeEnemies = new(50);

private void Update()
{
    m_activeEnemies.Clear();
    float minDistance = float.MaxValue;
    m_closestEnemy = null;
    
    for (int i = 0; i < m_enemies.Count; i++)
    {
        var enemy = m_enemies[i];
        if (enemy.IsActive)
        {
            m_activeEnemies.Add(enemy);
            
            if (enemy.Distance < minDistance)
            {
                minDistance = enemy.Distance;
                m_closestEnemy = enemy;
            }
        }
    }
}
```

## Delegate Caching

```csharp
// ❌ Bad - creates delegate instance each time
private void OnEnable()
{
    m_button.clicked += () => OnButtonClicked();       // Allocates closure
}

// ✅ Good - cached method reference
private void OnEnable()
{
    m_button.clicked += OnButtonClicked;               // Method group, no allocation
}

private void OnButtonClicked()
{
    // Handle click
}
```

---

# Async and Coroutine Patterns

- ✅ Prefer `Awaitable` (Unity 6+) over coroutines for simple delays.
- ✅ Cache `WaitForSeconds` objects when using coroutines repeatedly.
- ❌ Don't create new `WaitForSeconds` in loops.
- ✅ Use `WaitForSecondsRealtime` when you need unscaled time.
- ✅ Always check for object destruction after await/yield.

```csharp
// ❌ Bad - allocates WaitForSeconds every iteration
private IEnumerator BadCoroutine()
{
    while (true)
    {
        yield return new WaitForSeconds(0.1f);         // Allocates each loop
        DoSomething();
    }
}

// ✅ Good - cached wait object
private readonly WaitForSeconds m_shortWait = new(0.1f);

private IEnumerator GoodCoroutine()
{
    while (true)
    {
        yield return m_shortWait;                       // Reuses cached object
        DoSomething();
    }
}

// ✅ Better - Unity 6 Awaitable (no allocation)
private async Awaitable PeriodicUpdateAsync(CancellationToken token)
{
    while (!token.IsCancellationRequested)
    {
        await Awaitable.WaitForSecondsAsync(0.1f, token);
        
        if (this == null) return;                       // Check for destruction
        
        DoSomething();
    }
}
```

---

# Data Structure Selection

- ✅ Use `Dictionary<K,V>` for O(1) lookups by key.
- ✅ Use `HashSet<T>` for O(1) contains checks.
- ✅ Use `List<T>` when order matters and you iterate frequently.
- ✅ Use arrays for fixed-size, frequently-accessed data.
- ✅ Use `Queue<T>` for FIFO operations.
- ✅ Use `Stack<T>` for LIFO operations (undo systems, state history).
- ⚠️ Consider `NativeArray<T>` for Jobs/Burst compatibility.

```csharp
// Choose the right data structure for the operation

// O(1) lookup by ID
private Dictionary<int, Enemy> m_enemyById = new();

// O(1) membership check
private HashSet<int> m_processedIds = new();

// Ordered iteration, dynamic size
private List<Enemy> m_activeEnemies = new();

// Fixed size, frequent access
private Enemy[] m_enemyPool = new Enemy[100];

// Command queue
private Queue<ICommand> m_commandQueue = new();

// Undo stack
private Stack<ICommand> m_undoStack = new();
```

---

# Unity API Best Practices

## Transform Operations

- ✅ Batch transform changes — multiple SetPosition calls are inefficient.
- ✅ Use `Transform.SetPositionAndRotation()` when setting both.
- ❌ Avoid modifying individual components of position/rotation separately.

```csharp
// ❌ Bad - multiple transform operations
transform.position = newPosition;
transform.rotation = newRotation;

// ✅ Good - single combined operation
transform.SetPositionAndRotation(newPosition, newRotation);

// ❌ Bad - modifying individual components
transform.position = new Vector3(x, transform.position.y, transform.position.z);

// ✅ Good - set complete vector
Vector3 pos = transform.position;
pos.x = x;
transform.position = pos;
```

## CompareTag vs ==

- ✅ Use `CompareTag()` instead of `==` for tag comparison — no allocation.

```csharp
// ❌ Bad - string allocation for comparison
if (other.gameObject.tag == "Player")

// ✅ Good - no allocation
if (other.CompareTag("Player"))
```

## Camera.main

- ❌ Avoid `Camera.main` in Update — it performs a FindGameObjectWithTag internally.
- ✅ Cache the main camera reference.

```csharp
// ❌ Bad - lookup every frame
private void Update()
{
    Vector3 screenPos = Camera.main.WorldToScreenPoint(transform.position);
}

// ✅ Good - cached reference
private Camera m_mainCamera;

private void Awake()
{
    m_mainCamera = Camera.main;
}

private void Update()
{
    Vector3 screenPos = m_mainCamera.WorldToScreenPoint(transform.position);
}
```

---

# Profiling Markers

- ✅ Add profiler markers to identify expensive methods in the Unity Profiler.
- ✅ Use `ProfilerMarker` for lightweight, zero-allocation profiling.
- ✅ Remove or conditionally compile profiling code for release builds.

```csharp
using Unity.Profiling;

public class PerformanceCriticalSystem : MonoBehaviour
{
    private static readonly ProfilerMarker s_updateMarker = 
        new ProfilerMarker("PerformanceCriticalSystem.Update");
    
    private static readonly ProfilerMarker s_processEnemiesMarker = 
        new ProfilerMarker("PerformanceCriticalSystem.ProcessEnemies");

    private void Update()
    {
        using (s_updateMarker.Auto())
        {
            ProcessEnemies();
            UpdateUI();
        }
    }

    private void ProcessEnemies()
    {
        using (s_processEnemiesMarker.Auto())
        {
            // Expensive processing...
        }
    }
}
```

---

# Common Anti-Patterns

## Anti-Pattern Checklist for Code Review

When reviewing Unity code, flag these patterns:

| Anti-Pattern | Impact | Solution |
|--------------|--------|----------|
| `GetComponent` in Update | High | Cache in Awake |
| `FindObjectOfType` at runtime | High | Use references or events |
| `new List<T>()` in Update | High | Pre-allocate and Clear() |
| String concatenation in loops | Medium | Use StringBuilder |
| `Camera.main` in Update | Medium | Cache reference |
| LINQ in Update | Medium | Use explicit loops |
| `Physics.Raycast` every frame | Medium | Throttle or use FixedUpdate |
| `material` instead of `sharedMaterial` | Medium | Use MaterialPropertyBlock |
| Lambda in event subscription | Low | Use method group |
| `new WaitForSeconds` in coroutine loop | Low | Cache wait object |

## Code Smell Detection

Look for these patterns that indicate potential issues:

```csharp
// 🔴 Red flags in Update methods
void Update()
{
    GetComponent<T>()                    // 🔴 Uncached lookup
    FindObjectOfType<T>()                // 🔴 Scene scan
    new List<T>()                        // 🔴 Allocation
    new T[]                              // 🔴 Allocation
    string + string                      // 🔴 String allocation
    $"interpolated {value}"              // 🔴 String allocation
    .Where() .Select() .ToList()         // 🔴 LINQ allocation
    Camera.main                          // 🔴 Uncached lookup
    GameObject.Find()                    // 🔴 String search
    Physics.OverlapSphere()              // ⚠️ Allocating version
}

// 🟢 Preferred patterns
void Update()
{
    m_cachedComponent                    // 🟢 Cached reference
    m_cachedList.Clear()                 // 🟢 Reused collection
    m_stringBuilder.Clear().Append()     // 🟢 Reused builder
    for (int i = 0; i < count; i++)      // 🟢 Explicit loop
    m_cachedCamera                       // 🟢 Cached reference
    Physics.OverlapSphereNonAlloc()      // 🟢 Non-allocating
}
```

---

# Summary: Quick Reference

## Always Do ✅
- Cache component references in Awake()
- Pre-allocate collections with expected capacity
- Use object pooling for frequently spawned objects
- Use non-allocating physics methods
- Cache shader property IDs
- Use ProfilerMarker for performance-critical code
- Use Awaitable over coroutines in Unity 6+

## Never Do ❌
- GetComponent/Find in Update loops
- Allocate (new) in Update loops
- Use LINQ in Update loops
- String concatenation in hot paths
- Access Camera.main every frame
- Create WaitForSeconds in coroutine loops
- Use .material when .sharedMaterial suffices

## Consider ⚠️
- Throttle expensive operations
- Batch physics queries
- Profile on target platform
- Use Jobs/Burst for heavy computation
- Configure physics collision matrix

---

# Version Information

- **Target Unity Version**: Unity 6 (6000.x) and later
- **C# Version**: C# 9.0+ features supported
- **Last Updated**: January 2026
