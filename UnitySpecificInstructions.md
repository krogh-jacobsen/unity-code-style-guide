
## Unity version specific instructions for this project
- This project uses Unity 6. Make sure to use the latest sources and documentation that applies to Unity 6
- This project uses the newer Input System and not the older Input Manager
- This project use the newer UI Toolkit and not the older UGUI for anything UI
- This project use Universal Render Pipeline and not the old Bultin Render Pipeline
- When implementing systems like Object Pooling make sure to use Unitys own API

## Unity-Specific Patterns

### MonoBehaviour Usage
- Prefer composition over inheritance with MonoBehaviours
- Keep MonoBehaviours focused on a single responsibility
- Use `[RequireComponent(typeof(OtherComponent))]` when dependencies exist

### Serialization
```csharp
// Serialized fields should have clear tooltips
[Tooltip("Movement speed in units per second")]
[SerializeField] private float m_movementSpeed = 5f;

// Use SerializeReference for polymorphic serialization in Unity 2020.1+
[SerializeReference] private IInteractable m_currentInteractable;
```

## Script Lifecycle
- Organize the scripts in the script execution order meaning Awake() should be in the top before Start()
```csharp
Awake()
{}
Start()
{}
Update()
{}
LateUpdate()
{}
```

## Coroutines and Async
Name coroutines with a Co suffix: 
```csharp
StartCoroutine(LoadAssetsCo())
```
-Always handle coroutine cancellation when objects are destroyed
- Consider using UniTask for async operations

## 2. Project Organization Guidelines

```markdown
## Project Organization

### Folder Structure
- Organize assets by type(Scripts, Prefabs, Scenes, etc.)
- Use assembly definitions to manage dependencies and compilation time
- Follow a consistent naming pattern for scenes: `Scene_Purpose_Variant`

### Prefab Structure
-Prefer nested prefabs over monolithic ones
- Use prefab variants for specialized versions of common elements
- Maintain a clear hierarchy in complex prefabs
```

## Performance Considerations

### Efficient Unity Coding
-Cache component references in `Awake()` rather than `Start()` when possible
  - `Awake()` runs earlier in the lifecycle
  - References will be available to other components' `Start()` methods
  - `Awake()` runs even when GameObjects are disabled
- Use object pooling for frequently instantiated/ destroyed objects
- Avoid using `GetComponent<T>()` in `Update()` methods

```csharp
// Recommended approach
private Rigidbody m_rigidbody;
private Animator m_animator;

private void Awake()
{
    // Cache all component references in Awake
    m_rigidbody = GetComponent<Rigidbody>();
    m_animator = GetComponent<Animator>();

    // Initialize internal state that doesn't depend on other components
    m_initialPosition = transform.position;
}

private void Start()
{
    // Use cached references and perform operations that might 
    // depend on other components being initialized
    m_animator.SetTrigger("Initialize");
}

private void OnEnable()
{

}

private void OnDisable()
{
    
}

private void Update()
{
    // Use cached reference
    m_rigidbody.AddForce(Vector3.up);
}

// Avoid - getting component every frame
private void Update()
{
    // Don't do this
    GetComponent<Rigidbody>().AddForce(Vector3.up);
}

private void FixedUpdate()
{
    
}

private void LateUpdate()
{
    
}

```

## 4. Error Handling and Debugging


## Error Handling

### Debug Practices

- Use Unity's custom debug features instead of standard output
- Format debug messages consistently


```csharp
// Better error logging
Debug.LogError($"[{GetType().Name}] Failed to load data: {exception.Message}");

// Context-aware logging
Debug.LogWarning("Player health critical", gameObject);
```


Error Prevention
Use CompareTag() instead of string comparison with tag property
Validate reference dependencies with [RequireComponent] or null checks
Implement graceful fallbacks for missing references



## 5. Input System Implementation

```markdown
## Input System (New)

### Input Action Assets
- Organize input actions by functionality (Movement, Combat, UI)
- Use consistent naming across action maps
- Prefer callback-based input over polling when possible

```csharp
// Example of Input System usage
public class PlayerController : MonoBehaviour
{
    private PlayerInput m_playerInput;
    private InputAction m_moveAction;

    private void Awake()
    {
        m_playerInput = GetComponent<PlayerInput>();
        m_moveAction = m_playerInput.actions["Move"];
    }

    private void OnEnable()
    {
        m_moveAction.performed += OnMove;
    }

    private void OnDisable()
    {
        m_moveAction.performed -= OnMove;
    }

    private void OnMove(InputAction.CallbackContext context)
    {
        Vector2 moveInput = context.ReadValue<Vector2>();
        // Handle movement
    }
}
```
## Scene Management

### Scene Loading Best Practices
- Use SceneManager.LoadSceneAsync instead of LoadScene for better user experience
- Implement loading screens for scene transitions when appropriate
- Consider using additive scene loading for persistent elements
- Organize scenes into logical "levels" with a consistent structure

```csharp
// Async scene loading example
public class SceneLoader : MonoBehaviour
{
    [SerializeField] private GameObject m_loadingScreen;

    public async void LoadSceneAsync(string sceneName)
    {
        m_loadingScreen.SetActive(true);

        var operation = SceneManager.LoadSceneAsync(sceneName);
        operation.allowSceneActivation = false;

        // Wait until the scene is ready
        while (operation.progress < 0.9f)
        {
            await Task.Delay(100);
        }

        operation.allowSceneActivation = true;
        m_loadingScreen.SetActive(false);
    }
}
```

## Scriptable Objects Usage
- Data Architecture
- Use ScriptableObjects for configuration data, game settings, and level design
- Create custom editors for complex ScriptableObjects to improve designer workflow
- Consider ScriptableObjects for modular event systems
- Keep ScriptableObject assets in a dedicated folder structure

```csharp
[CreateAssetMenu(fileName = "WeaponData", menuName = "Game/Weapons/WeaponData")]
public class WeaponData : ScriptableObject
{
    [Tooltip("The name that will appear in the UI")]
    public string DisplayName;

    [Tooltip("Damage per hit")]
    public float BaseDamage = 10f;

    [Tooltip("Time between attacks in seconds")]
    public float CooldownTime = 1.5f;

    [Tooltip("Visual prefab for the weapon")]
    public GameObject WeaponPrefab;
}
```

## Dependency Management
- System Architecture
- Prefer dependency injection over direct singletons or static references
- If using singletons, follow a consistent pattern for implementation
- Consider using service locator pattern for systems that need frequent global access

```csharp
// Singleton implementation example - if needed
public class GameManager : MonoBehaviour
{
    private static GameManager s_instance;

    public static GameManager Instance
    {
        get
        {
            if (s_instance == null)
            {
                Debug.LogError("GameManager is null! Make sure it exists in the scene.");
            }
            return s_instance;
        }
    }

    private void Awake()
    {
        // Singleton pattern with proper scene handling
        if (s_instance != null && s_instance != this)
        {
            Destroy(gameObject);
            return;
        }

        s_instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```


Physics & Collision Handling
Physics Optimization
Use non-allocating physics queries when possible (Physics.OverlapSphereNonAlloc)
Layer-based collision filtering instead of tag checks for performance
Cache physics results when appropriate
Use fixed timestep calculations in FixedUpdate for consistency

```csharp
// Example of efficient physics checking
private Collider[] m_colliderResults = new Collider[10]; // Pre-allocate array

private void CheckNearbyObjects()
{
    // Use non-allocating physics method to avoid garbage
    int hitCount = Physics.OverlapSphereNonAlloc(
        transform.position,
        m_detectionRadius,
        m_colliderResults,
        m_targetLayer
    );

    for (int i = 0; i < hitCount; i++)
    {
        // Process each detected object
        ProcessDetectedObject(m_colliderResults[i]);
    }
}
```

Editor Extensions & Tools
Editor Workflow
Write custom property drawers for complex data types
Create editor tools for common design tasks
Use custom inspectors to make designers' lives easier
Add gizmos for visual debugging of game elements

```csharp
// Example of custom gizmos for a patrol path
private void OnDrawGizmos()
{
    if (m_patrolPoints == null || m_patrolPoints.Length == 0)
        return;

    Gizmos.color = Color.yellow;

    // Draw patrol path
    for (int i = 0; i < m_patrolPoints.Length; i++)
    {
        Gizmos.DrawSphere(m_patrolPoints[i], 0.5f);

        if (i < m_patrolPoints.Length - 1)
        {
            Gizmos.DrawLine(m_patrolPoints[i], m_patrolPoints[i + 1]);
        }
        else if (m_loopPath)
        {
            Gizmos.DrawLine(m_patrolPoints[i], m_patrolPoints[0]);
        }
    }
}
```

UI Toolkit Best Practices
UI Architecture
Use USS (UI Toolkit StyleSheets) instead of inline styles
Organize UI hierarchies with clear naming conventions
Separate visual elements from controllers with MVVM pattern when appropriate
Use UI Builder for complex layouts

```csharp
// Example of proper UI Toolkit usage
public class InventoryUI : MonoBehaviour
{
    [SerializeField] private VisualTreeAsset m_itemTemplate;
    private ListView m_listView;

    private void InitializeUI()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;

        // Use named queries to find elements
        m_listView = root.Q<ListView>("inventory-list");
        var closeButton = root.Q<Button>("close-button");

        // Setup callbacks
        closeButton.clicked += CloseInventory;

        // Setup list view with data binding
        m_listView.makeItem = () => m_itemTemplate.Instantiate();
        m_listView.bindItem = (element, index) => BindItem(element, m_items[index]);
        m_listView.itemsSource = m_items;
    }
}
```

Memory & Resource Management
Optimization Techniques
Use object pools for frequently instantiated objects
Implement proper resource loading/unloading with Addressables
Be mindful of allocations in performance-critical code
Implement proper cleanup in OnDisable/OnDestroy methods

```csharp
// Example of addressable asset loading
public async Task<GameObject> LoadAssetAsync(string assetAddress)
{
    try
    {
        var loadOperation = Addressables.LoadAssetAsync<GameObject>(assetAddress);
        var prefab = await loadOperation.Task;
        return Instantiate(prefab);
    }
    catch (Exception e)
    {
        Debug.LogError($"Failed to load asset {assetAddress}: {e.Message}");
        return null;
    }
}
```

Animation Best Practices
Animation System Usage
Use Animator Parameters for state transitions rather than direct calls when possible
Keep Animation Controllers organized with logical state machines
Use Animation Events for precise timing of game events
Consider using Animation Rigging for procedural animation needs

```csharp
// Example of proper Animator usage
[RequireComponent(typeof(Animator))]
public class CharacterAnimationController : MonoBehaviour
{
    private static readonly int s_movementSpeed = Animator.StringToHash("MovementSpeed");
    private static readonly int s_isGrounded = Animator.StringToHash("IsGrounded");
    private static readonly int s_attackTrigger = Animator.StringToHash("Attack");

    private Animator m_animator;

    private void Awake()
    {
        m_animator = GetComponent<Animator>();
    }

    public void UpdateMovementAnimation(float speed)
    {
        m_animator.SetFloat(s_movementSpeed, speed);
    }

    public void SetGroundedState(bool isGrounded)
    {
        m_animator.SetBool(s_isGrounded, isGrounded);
    }

    public void TriggerAttackAnimation()
    {
        m_animator.SetTrigger(s_attackTrigger);
    }
}
```

Multithreading & Async Patterns
Threading Guidelines
Use Unity's Job System for CPU-intensive work that can be parallelized
Avoid accessing Unity APIs from background threads
Leverage async/await with proper SynchronizationContext handling
Consider using thread-safe data structures for shared state

```csharp
// Example of Job System usage
public class ParticleProcessor : MonoBehaviour
{
    // Native array to hold particle positions
    private NativeArray<Vector3> m_particlePositions;

    // Job to update particle positions
    private struct ParticleUpdateJob : IJobParallelFor
    {
        public NativeArray<Vector3> positions;
        public float deltaTime;
        public Vector3 force;

        public void Execute(int index)
        {
            // Simple physics update
            Vector3 position = positions[index];
            position += force * deltaTime;
            positions[index] = position;
        }
    }

    private void Update()
    {
        // Create and schedule the job
        ParticleUpdateJob job = new ParticleUpdateJob
        {
            positions = m_particlePositions,
            deltaTime = Time.deltaTime,
            force = Physics.gravity
        };

        JobHandle handle = job.Schedule(m_particlePositions.Length, 64);
        handle.Complete(); // Wait for job to complete
    }
}
```

Design Patterns for Unity
Common Patterns
Use Command pattern for input handling and action history
Consider Observer pattern (or C# events) for loose coupling between systems
Implement State pattern for complex character controllers
Use Factory pattern for complex object creation

Version Control Integration
Git Workflow
Use .gitignore properly for Unity projects
Consider using Git LFS for binary assets
Commit frequently with meaningful commit messages
Maintain a clean main branch with feature branches for development
Unity Collaboration
Configure Unity meta files appropriately for team projects
Set Project Settings → Editor → Version Control Mode to "Visible Meta Files"
Set Project Settings → Editor → Asset Serialization Mode to "Force Text"
Use Unity's Smart Merge tool for scene and prefab merging

```csharp
// Example of State Pattern for a character controller
public class PlayerController : MonoBehaviour
{
    private PlayerState m_currentState;

    // State references
    private IdleState m_idleState;
    private RunningState m_runningState;
    private JumpingState m_jumpingState;

    private void Awake()
    {
        // Initialize states
        m_idleState = new IdleState(this);
        m_runningState = new RunningState(this);
        m_jumpingState = new JumpingState(this);

        // Set default state
        m_currentState = m_idleState;
    }

    private void Update()
    {
        // Let the current state handle the update
        m_currentState.Update();
    }

    public void ChangeState(PlayerState newState)
    {
        m_currentState.Exit();
        m_currentState = newState;
        m_currentState.Enter();
    }
}

// Base state class
public abstract class PlayerState
{
    protected PlayerController m_controller;

    public PlayerState(PlayerController controller)
    {
        m_controller = controller;
    }

    public abstract void Enter();
    public abstract void Update();
    public abstract void Exit();
}
```