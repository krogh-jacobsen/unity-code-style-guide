# Project configuration

This is the single configuration record to adapt in the target project. Actual project files are
evidence; this document records the intended choices and reasons, not a second package lockfile.

## Versions

- Intended starter line: **Unity 6.7 (6000.7.x)**. An intended line is not a tested release claim.
- Exact target Editor: **fill in from `ProjectSettings/ProjectVersion.txt`**.
- Language/API baseline: **C# 9 / .NET Standard 2.1**, verified against the selected release.
- Starter validation results and prerelease limits: [Validation.md](../../Validation.md).

## Selected systems

| Area | Baseline | Change only when selected |
|---|---|---|
| Rendering | URP matched to the chosen Editor/template | Built-in or HDRP |
| Input | Input System | Legacy Input Manager or deliberate combined handling |
| Runtime UI | UI Toolkit, UXML/USS | uGUI or another runtime UI system |
| Async | Awaitable; coroutines for useful frame iteration | Package-specific Task/coroutine integration |
| Pooling | UnityEngine.Pool.ObjectPool<T> | Specialized pool with a demonstrated requirement |

Editor IMGUI remains an available Editor-tooling option; runtime UI selection does not ban it.
Awaitable operations require owned cancellation/error observation; a destruction token does not
cover disable or request replacement. Pool capacity reserves storage rather than prewarming objects.
Use matching skills for implementations instead of loading audit references during setup.

## Resolved packages

Read `Packages/manifest.json`, `Packages/packages-lock.json`, and Package Manager's completed resolved
list through Unity CLI. Record versions here when needed for compatibility decisions; retain the
lockfile as the authoritative dependency graph. Install only selected packages.

| Capability | Package | Exact resolved version in target |
|---|---|---|
| Rendering | `com.unity.render-pipelines.universal` | Fill in; do not assume a URP/Editor pairing |
| Input | `com.unity.inputsystem` | Fill in |
| Tests, when selected | `com.unity.test-framework` | Fill in or remove |
| Addressables, when selected | `com.unity.addressables` | Fill in or remove |
| Networking, when selected | `com.unity.netcode.gameobjects` | Fill in or remove |

## Target decisions

| Decision | Target value |
|---|---|
| Project namespace | Fill in |
| Desktop platforms / backends | Windows x64 and macOS Apple Silicon; record primary platform and backend per target |
| Additional architectures/platforms | Intel macOS only when selected; others outside the desktop baseline |
| Desktop support and profiles | Fill in minimum OS/GPU/hardware and selected API order; follow [desktop setup](../BuildSettings/DesktopBuilds.md) or [mobile setup](../BuildSettings/MobileBuilds.md) |
| Frame/memory budget | Record when established for a representative workload |
| Enter Play Mode reload | Scene reload enabled; use selected Editor's domain/code reload default |
| Assembly policy | Default assemblies; add boundaries for concrete needs; isolate tests/Editor code |
| Optional presets/templates/examples | List selected groups |
| Optional scene templates | Strategy Sandbox, UI Preview, Asset LookDev; select installed groups and record target validation |

## Deprecated in Unity 6

Use version-matched source/API docs and compiler diagnostics. The following are common traps, not
permission for a search-and-replace migration:

| Older API/pattern | Replacement decision |
|---|---|
| `FindObjectOfType` / `FindObjectsOfType` | Prefer explicit references/registries; select supported FindAny/FindObjects overloads for inspection |
| Rigidbody `velocity`, `drag`, `angularDrag` | Verify `linearVelocity`, `linearDamping`, `angularDamping` in the target's 3D/2D APIs |
| Graphics DrawMesh family | RenderMesh family has different RenderParams, bounds, and argument contracts |
| UxmlFactory/UxmlTraits | Supported UxmlElement/UxmlAttribute generation requires actual attribute/constructor migration |
| UI event default actions / PreventDefault | Propagation and default-action semantics differ; migrate the intended behavior, not the method name |
| URP Execute / camera targets | Render Graph resource/pass lifetime requires a real migration; use the matching skill |

From 6000.6, verify the parameterless FindObjectsByType API and obsolete sorted overloads; older
6000.0–6000.5 projects require their supported signatures. ParticleSystem module writes use a local
module variable (`var emission = particles.emission; emission.enabled = true;`). Do not introduce
future CoreCLR/.NET APIs into this baseline; see the optional [migration reference](CoreCLRUpgrade.md).

## CLI/manual completion

**Prerequisite:** exact Editor, project, and selected platform are known. Use `unity-cli` to inspect
versions/settings, and `unity-package-management` for supported Client API execution. Manual fallback:
Hub + Package Manager + Project Settings. **Done:** exact versions resolve, the selected pipeline/input
actually run, configuration agrees with saved files, and any mismatch is resolved or reported.
