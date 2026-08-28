# Unity Assets & Memory

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Where your memory actually goes, and how assets get into and out of it.

Most teams optimize scripting hot paths first because that's what the Profiler shows by default. But
in a shipped game, **assets are usually 80–95% of memory**, and import settings — not code — decide
how big they are. A single texture with the wrong flag can cost more than every allocation your
gameplay code makes in an hour.

Table of contents:
- [How to think about Unity memory](#how-to-think-about-unity-memory)
- [Choosing a loading strategy](#choosing-a-loading-strategy)
- [Addressables](#addressables)
- [Texture import settings](#texture-import-settings)
- [Mesh & model import settings](#mesh--model-import-settings)
- [Audio import settings](#audio-import-settings)
- [Presets: enforce settings automatically](#presets-enforce-settings-automatically)
- [Managed memory & the garbage collector](#managed-memory--the-garbage-collector)
- [Build size](#build-size)
- [Measuring](#measuring)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## How to think about Unity memory

Unity has two separate heaps, and conflating them wastes a lot of debugging time:

| Heap | Holds | Freed by | Profiled with |
|---|---|---|---|
| **Managed** | C# objects, closures, boxed values, `string` | Garbage collector | Profiler → Memory, GC Alloc column |
| **Native** | Textures, meshes, audio, animation, shaders, scene data | Explicit unload, or reference-counted release | Memory Profiler package |

- ℹ️ A `Texture2D` costs a few dozen bytes on the managed heap and potentially **hundreds of megabytes**
  on the native heap. Chasing GC allocations while ignoring texture import settings is optimizing the
  wrong heap.
- ⚠️ Native memory is not garbage collected. If nothing releases it, it stays until the app quits.

---

## Choosing a loading strategy

| Strategy | Loads when | Unloads when | Use for |
|---|---|---|---|
| Direct `[SerializeField]` reference | The referencing scene/prefab loads | That scene unloads | Anything a scene always needs |
| `Addressables` | You explicitly load it | You explicitly release it | Optional, large, or swappable content |
| `Resources/` folder | **App start**, all of it | Effectively never | ❌ Nothing, in new projects |

### Why `Resources/` should be treated as deprecated

- ❌ **Everything in any `Resources/` folder ships in the build**, whether or not it's referenced.
- ❌ A serialized index of the entire folder is built and loaded **at startup**, adding directly to
  launch time. This scales badly and is a common cause of slow cold starts on mobile.
- ❌ There is no unload granularity — `Resources.UnloadUnusedAssets()` is a full sweep, not a targeted
  release.
- ✅ Use direct references for what's always needed and Addressables for everything else.
- ℹ️ `Resources/` is fine for a jam game or a throwaway prototype. It is not fine for anything you
  intend to ship.

### Direct references are not free

- ⚠️ Every direct reference in a prefab or scene is loaded **when that prefab or scene loads**,
  transitively. A prefab referencing a `WeaponDataSO` that references a 4K icon loads that icon,
  even if the weapon is never equipped.
- ✅ Break the chain with an `AssetReference` (Addressables) when the tail of the graph is large or
  rarely needed.

---

## Addressables

- ✅ Every `LoadAssetAsync` needs exactly one matching `Release`. Loads are reference-counted — two
  loads need two releases.
- ✅ Store the `AsyncOperationHandle`, not just the result. You need the handle to release.
- ✅ Release in `OnDestroy` for object-lifetime assets, or when leaving a scene for scene-lifetime ones.
- ⚠️ `Addressables.InstantiateAsync` must be released with `Addressables.ReleaseInstance`, not
  `Destroy`. Using `Destroy` leaks the reference count and the asset never unloads.
- ⚠️ **The duplicate-asset trap:** if two Addressable groups each reference the same texture and it
  isn't itself marked Addressable, it is duplicated into both bundles — two copies on disk *and* two
  copies in memory. Run the **Analyze → Check Duplicate Bundle Dependencies** rule before shipping.
- ✅ Group by *when things are needed together*, not by asset type. A "Level 3" group beats a
  "Textures" group.
- ✅ Prefer `LoadAssetsAsync` for a batch over many individual awaits — fewer handles to track.

```csharp
public class WeaponLoader : MonoBehaviour
{
    [SerializeField] private AssetReferenceGameObject m_weaponReference;

    private AsyncOperationHandle<GameObject> m_handle;

    private async Awaitable LoadAsync()
    {
        m_handle = m_weaponReference.LoadAssetAsync<GameObject>();
        await m_handle.Task;

        if (this == null) return;   // Destroyed while loading

        if (m_handle.Status != AsyncOperationStatus.Succeeded)
        {
            Debug.LogError($"[{GetType().Name}] Failed to load weapon asset.", this);
            return;
        }

        Instantiate(m_handle.Result, transform);
    }

    private void OnDestroy()
    {
        // Every load needs its release, or the bundle never unloads
        if (m_handle.IsValid())
        {
            Addressables.Release(m_handle);
        }
    }
}
```

---

## Texture import settings

Textures are almost always the largest single category. These four settings do most of the work:

| Setting | Default | Recommended | Why |
|---|---|---|---|
| **Max Size** | 2048 | The smallest that looks right | Memory scales with the *square* of dimension |
| **Compression** | Normal | Platform-specific (ASTC mobile, BC7/DXT desktop) | Uncompressed is 4–8× larger |
| **Generate Mip Maps** | On | **Off for UI and 2D sprites** | Mips add 33% memory; unused for screen-space UI |
| **Read/Write Enabled** | Off | **Keep off** | ⚠️ On = **2× memory**, a full CPU-side copy |

- ⚠️ **Read/Write Enabled is the most common silent 2× in a Unity project.** It keeps a second copy of
  the texture in CPU memory forever. You only need it if you call `GetPixels`, `SetPixels`, or read
  the texture from a script at runtime. Audit every texture that has it on.
- ✅ Halving Max Size quarters the memory. 2048→1024 is a 75% saving, and on most assets nobody notices.
- ✅ Set **sRGB (Color Texture)** on for albedo/UI, **off** for masks, roughness, and data maps.
- ✅ Use **Override for Platform** — mobile wants ASTC and smaller max sizes than desktop.
- ✅ Crunch compression shrinks the *download*, not runtime memory. Use it for build size, and expect
  slower import and load times.
- ✅ Pack UI sprites into a **Sprite Atlas** to cut draw calls. Watch that you don't pull a whole 4K
  atlas into memory to show one icon — group atlases by screen.
- ℹ️ The same rules apply to `RenderTexture`: they are native memory, they are not garbage collected,
  and you must call `Release()`.

---

## Mesh & model import settings

| Setting | Recommended | Why |
|---|---|---|
| **Read/Write Enabled** | Off | Same 2× penalty as textures |
| **Mesh Compression** | Low/Medium for background geometry | Lossy but usually invisible |
| **Optimize Mesh** | On | Reorders vertices for GPU cache coherence |
| **Normals / Tangents** | Calculate only if the shader needs them | Skipping tangents saves per-vertex memory |
| **Import BlendShapes** | Off unless used | Large per-vertex cost |
| **Import Animation** | Off on static props | Animation clips are surprisingly large |
| **Rig → Animation Type** | None on non-animated models | Avoids an unnecessary Animator |

- ⚠️ Read/Write is required for runtime mesh modification, `MeshCollider` baking at runtime, and some
  procedural workflows. It is not required for normal rendering.
- ✅ Static geometry should be marked **Static** so it can be batched and light-mapped.

---

## Audio import settings

Audio is the category most often left entirely on defaults, and the defaults are wrong for music.

| Role | Load Type | Compression | Notes |
|---|---|---|---|
| Short SFX (< 1s) | Decompress On Load | ADPCM or PCM | Instant playback, small enough to afford |
| Medium (1–10s) | Compressed In Memory | Vorbis | Decoded on the fly, modest CPU |
| Music / ambience (> 10s) | **Streaming** | Vorbis | ⚠️ Never load a 3-minute track into memory |
| UI feedback | Decompress On Load | ADPCM | Latency matters more than size |

- ⚠️ A single uncompressed 3-minute stereo track at 44.1 kHz is roughly **30 MB** in memory. On
  Streaming it's a small buffer.
- ✅ **Force To Mono** for anything played as a 3D positional source. Stereo data is wasted — spatial
  panning is computed from the listener anyway — and it halves the size.
- ✅ Override the **sample rate**. Most SFX are indistinguishable at 22 kHz.
- ✅ Limit concurrent voices in the Audio settings; each active voice costs CPU.
- ℹ️ For mixer and DSP configuration, see the `optimize-audio` skill.

---

## Presets: enforce settings automatically

Import settings only help if they're actually applied. Relying on people to remember is how a 4K
Read/Write-enabled texture ends up in the build.

- ✅ Configure one asset correctly, then **Preset icon → Save Current To…** into `Assets/Settings/Presets/`.
- ✅ Wire it up in **Project Settings → Preset Manager** with a filter, so every new import in a folder
  gets the right settings automatically.
- ✅ Have a preset per role, not per type: `UISprite`, `AlbedoTexture`, `NormalMap`, `SFXAudio`,
  `MusicAudio`.
- ✅ Commit presets to version control. They are project configuration, not personal preference.
- ℹ️ See [UnityProjectConfiguration.md](../UnityCustomInstructions/UnityProjectConfiguration.md) for a
  worked preset layout.

---

## Managed memory & the garbage collector

- ℹ️ Unity uses the Boehm GC with **incremental mode** on by default in Unity 6. Incremental spreads
  collection across frames, turning one long spike into several short ones. It does not reduce total
  work.
- ✅ The goal is not "fewer GCs" but **fewer allocations**, so collection has less to do. See
  [UnityPerformanceOptimizationInstructions.md](UnityPerformanceOptimizationInstructions.md#memory-management).
- ⚠️ The managed heap **never shrinks**. Once it grows to accommodate a spike, that address space is
  reserved for the process lifetime. One bad loading screen sets your memory floor permanently.
- ✅ For a hard no-hitch section — a cutscene, a competitive round — you can disable GC entirely and
  re-enable after, provided you know allocations are bounded:

```csharp
using UnityEngine.Scripting;

private void BeginCriticalSection()
{
    // Only safe if you know allocation during this window is bounded.
    // The heap will grow instead of collecting.
    GarbageCollector.GCMode = GarbageCollector.Mode.Disabled;
}

private void EndCriticalSection()
{
    GarbageCollector.GCMode = GarbageCollector.Mode.Enabled;
    GC.Collect();   // Pay the cost now, at a moment you control
}
```

- ✅ Call `Resources.UnloadUnusedAssets()` during a loading screen, after unloading a scene. It only
  frees native assets with **zero remaining references**, so it does nothing if something still holds
  them — which is usually a static field or an un-released Addressables handle.

---

## Build size

- ✅ Set **Managed Stripping Level** to `Medium` or `High` in Player Settings. It removes unused IL.
- ⚠️ Stripping breaks reflection. If you deserialize types by name or use `Activator.CreateInstance`,
  preserve them explicitly:

```xml
<!-- Assets/link.xml -->
<linker>
  <assembly fullname="MyGame.Runtime">
    <type fullname="MyGame.Saves.SaveDataV2" preserve="all" />
  </assembly>
</linker>
```

- ✅ Use **IL2CPP** for release builds — faster and smaller than Mono, and required on most platforms.
- ✅ After a build, read the **Build Report** (or the `Editor.log` size breakdown) to see what actually
  shipped. It's frequently a folder nobody remembered was there.
- ✅ Strip unused shader variants — variant explosion is a top-three build size cause. Check
  **Project Settings → Graphics → Shader Stripping**.
- ✅ Remove unused platform modules from the Editor install; they don't affect build size but they
  slow the Editor down.

---

## Measuring

| Tool | Answers |
|---|---|
| **Memory Profiler** package | What is in native memory *right now*, and what references it |
| Profiler → Memory module | Managed heap size, GC allocation rate per frame |
| Build Report | What shipped, by category and by asset |
| Frame Debugger | Draw calls, batches, and what broke batching |
| Profiler → Highlights (6.3) | Where the frame went, CPU vs GPU, at a glance |

- ✅ **Take two Memory Profiler snapshots and diff them.** A snapshot alone tells you what's resident;
  the diff tells you what leaked. Snapshot after loading a level, play, return to menu, snapshot
  again — anything still there is a leak.
- ✅ Profile a **development build on the target device**, not the Editor. The Editor holds extra
  copies of nearly everything and its numbers are not representative.
- ⚠️ Unity 6.3's Profiler Captures List lets you store and re-open sessions from the project without
  re-importing each time — useful for before/after comparisons.

---

## Troubleshooting

**Memory climbs every time the player returns to the main menu.**
Something still references the old level's assets. Take a Memory Profiler snapshot before and after,
diff them, and look at what holds a reference to a surviving texture. In order of likelihood: an
un-released Addressables handle, a static collection never cleared, or an event subscription keeping
a whole object graph alive.

**`Resources.UnloadUnusedAssets()` frees nothing.**
It only releases assets with **zero** remaining references. If anything still points at them —
including a static field or a live handle — it is a no-op. Find the reference; don't call it twice.

**An Addressable asset never unloads.**
Either `Release` was never called, or `Destroy` was used on something created with
`InstantiateAsync` (which needs `ReleaseInstance`), or the load happened more times than the
release. Loads are reference-counted.

**The same texture appears twice in a memory snapshot.**
Bundle duplication: two Addressable groups each reference it and it isn't marked Addressable itself.
Run **Analyze → Check Duplicate Bundle Dependencies**.

**Build is far larger than the sum of the assets.**
Usually a `Resources/` folder (everything in it ships whether referenced or not), or shader variant
explosion. Read the Build Report to see which.

**Texture memory is exactly double what you calculated.**
`Read/Write Enabled` is on, so there's a full CPU-side copy.

**Stripping broke the build at runtime with a missing type.**
Managed stripping removed a type only reached by reflection. Add it to `link.xml`.
---

## Review checklist

| Check | Look for |
|---|---|
| Read/Write Enabled | Any texture or mesh with it on that isn't read from script |
| Texture Max Size | 2048+ on assets that render small |
| Mip maps | Enabled on UI sprites |
| Audio load type | Music not set to Streaming; 3D sources not Forced To Mono |
| Addressables | `LoadAssetAsync` with no matching `Release`; `Destroy` on an instantiated addressable |
| Duplicate bundles | Analyze rule not run |
| `Resources/` | Any use at all in a shipping project |
| Stripping | Managed Stripping Level at `Disabled` |
| Presets | New assets importing on defaults because no Preset Manager filter exists |
| Leaks | Static collections that grow and are never cleared |

---

## Learn more

- [Memory in Unity](https://docs.unity3d.com/6000.3/Documentation/Manual/performance-memory-overview.html)
- [Addressables documentation](https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/index.html)
- [Memory Profiler package](https://docs.unity3d.com/Packages/com.unity.memoryprofiler@1.1/manual/index.html)
