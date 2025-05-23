# GitHub Copilot instructoons: Unity C# Style Guide & naming

# Software Design Principles
## General principes
- Keep the code DRY (Don't Repeat Yourself)
- Try to adhere to SOLID principles

Use Meaningful and Consistent Naming Conventions
Ensure variable, method, and class names clearly describe their purpose. Follow a consistent naming convention across the project.

Avoid Magic Numbers and Strings
Use constants, enums, or configuration files instead of hardcoding values. This improves code readability and maintainability. For example:
float JumpHeight = 1.2f;

Replace hardcoded values (e.g., 5f in Jump) with constants or serialized fields for better flexibility and readability.

Segregate Responsibilities (Single Responsibility Principle)
Avoid mixing unrelated functionalities in one class or method:

Separate concerns into different layers (e.g., UI logic, gameplay logic, and data management).
Comment Intelligently
Avoid over-commenting your code, but ensure complex logic is accompanied by useful comments. Favor explaining "why" rather than "what," as the code usually explains "what" already.

Centralize Configuration
Define your game configuration (e.g., player settings, game difficulty, or constants) in one central place, such as a ScriptableObject with shared settings.

Refactor Regularly
Dedicate time to refactor old code as projects evolve. This ensures the codebase remains manageable and avoids "code rot."

Use Dependency Injection Where Appropriate
Build better modularity by passing dependencies directly into classes or functions, rather than tightly coupling them within the class.

Performance Optimization
Object Pooling
For objects that are repeatedly created and destroyed (e.g., bullets, enemies, particles), use object pooling to reduce garbage collection overhead and improve performance.

Optimize Update Loops
Minimize or eliminate per-frame updates whenever possible:

Use InvokeRepeating, coroutines, or events where feasible to reduce reliance on the Update method.
Combine multiple Update methods into a single manager class to reduce overhead.
Avoid Overuse of LINQ in Performance-Critical Code
While LINQ can be clean and expressive, it can also introduce performance overhead, especially in hot paths. Use more explicit loops for performance-critical operations.

Reduce Garbage Collection (GC) Pressure

Avoid frequent allocations (e.g., new keyword in loops).
Use List<T>.Clear() instead of creating a new list when reusing collections.
Favor structs over classes for small, simple objects.
Profile and Benchmark Regularly
Frequently use Unity’s Profiler to track bottlenecks and optimize accordingly. Build profiling into your development cycle.

Use Burst Compiler and Jobs System
Leverage Unity's Burst Compiler and Jobs System for multithreading and SIMD performance optimizations.

Minimize Raycast Usage
Reduce the number of ray casts by combining certain checks, caching results, or batching logic when possible.

Optimize Rendering

Reduce the number of draw calls by batching objects with the same materials.
Use LOD (Level of Detail) to scale down object complexity at a distance.
Disable unnecessary components, rendering, or GameObjects outside the player's viewport.
Efficient Physics Handling

Use layers to limit which objects interact in collision/trigger checks.
Minimize the use of rigidbody physics for objects that don’t require it.
Use Rigidbody.Interpolate only when necessary for smoother movement.

Utilize Assembly Definitions
Break your project into assemblies to reduce build times and improve organization.

Keep Assets and Scenes Organized
Create a folder structure for prefabs, materials, scripts, and other assets. Avoid dumping everything into one folder.

Advanced Systems Design
Event-Driven Architecture
Use the observer pattern or scriptable event systems to decouple systems and reduce dependencies (e.g., firing events for UI to update instead of direct references to UI components).

Use ScriptableObjects for Data-Driven Design
ScriptableObjects can hold data shared across objects and provide a cleaner way to work with configurations or settings.

Avoid Overengineering Prematurely
Strike a balance between building scalable systems and keeping things simple. Avoid creating overly abstract systems until the need arises.

Encapsulate Third-Party Code
Wrap third-party libraries or SDKs in your own APIs to ensure future flexibility if you need to swap implementations.

Understand Cache Misses and Memory Layout
For performance-critical code, consider Unity’s Data-Oriented Technology Stack (DOTS) to optimize memory layout and processing with entities.

Debugging and Maintenance
Log Strategically
Use Unity's Debug.Log, Debug.LogWarning, and Debug.LogError selectively, and disable logs for production builds to avoid performance hits.

Graceful Error Handling
Use try-catch blocks sparingly and only where they make sense. Design your systems to fail gracefully or recover when possible.

Use Debug.DrawLine and Gizmos
Visual aids in the Editor can be invaluable for debugging physics and other spatial issues.

Feature Toggles and Debug Flags
Use configurable flags to enable or disable features at runtime without redeploying the application.

Automate Repetitive Processes
Use Unity Editor scripting to automate tasks like generating configuration files, setting up prefabs, or applying repetitive changes to assets.
