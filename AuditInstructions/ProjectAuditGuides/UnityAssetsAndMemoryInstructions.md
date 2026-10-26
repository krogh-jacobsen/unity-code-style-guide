# Unity asset and memory audit

Load for asset loading/release, retained memory, import cost, or build content. Addressables rows
apply only when `com.unity.addressables` is installed; bundle and atlas rows apply only when the
project uses Addressables, AssetBundles, or SpriteAtlas. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Import recipes belong to skills such as
`unity:optimize-audio` and `unity:manage-sprite-atlas` when available, or to
[project presets](../Presets/README.md). This lens owns audio import/residency and streaming-readiness findings; `unity:optimize-audio`
owns implementation recipes, [Audio](UnityAudioInstructions.md) owns playback correctness, and
[Performance](UnityPerformanceOptimizationInstructions.md) owns measured CPU/DSP cost.
**Last verified: October 2026.**

## Establish ownership

Map asset acquisition, consumers, retention, and release for each relevant lifetime. Distinguish
managed wrappers from native asset memory, source assets from runtime instances, and intended caches
from leaks. Follow serialized references transitively; a small configuration asset can retain large content.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Load ownership | Handles, multiple loads/acquires, sharing, replacement | A consumer uses an asset after its release call, or the code that must release a handle no longer holds it |
| Failure/cancellation | Completion and cleanup after disable/destroy/request replacement | A failed load leaves its handle unreleased, or a late result is consumed with no owner to release it (async lifetime is checked in [Scenes](UnityScenesAndLifecycleInstructions.md)) |
| Instantiation (Addressables only) | Addressables creation path, clones, instance release | An instance is released through a different path than the installed package requires, or a dependency is released while an instance still uses it |
| Runtime resources | Materials, textures, render targets, meshes, SO clones | `Renderer.material`/`MeshRenderer.material`, `new Material`, `new Texture2D`, `new Mesh`, or a `RenderTexture` is created in code with no `Destroy`/`Release` on a matching teardown path (grep, then trace) |
| Shared configuration | Runtime writes and nested referenced assets | Runtime writes leak consumer-specific/session state into shared configuration or saved authoring data; intentionally shared mutable state with an explicit lifetime/reset contract is valid |
| Import residency | Actual platform format, size, Read/Write need, mips, audio role | An importer's platform size, Read/Write, or mip setting exceeds the project's stated budget or its [presets](../Presets/README.md) with no runtime need; with no stated budget, report sizes and record "no budget" |
| Bundle/atlas dependencies | Build layout, duplicate dependencies, content grouping | Build layout and representative load/release cycles show avoidable duplication or churn that violates a budget/content lifetime. Intentional small duplication or independently used bundle members can be a valid coupling tradeoff |
| Shipping content | Build report, Resources, stripping/preservation, platform overrides | The build report lists content with no reference path, or a type used by reflection or serialization is missing from a stripped build (needs a build to confirm) |
| Audio readiness | Load type, preload/background loading, clip load state, target memory/CPU/I/O and first-use latency | Required playback is delayed by unloaded data, or the import strategy breaks a measured target budget; evaluate streaming/decompression by role and platform, with no universal clip-duration cutoff |

## Ownership cases to verify

- ⚠️ Match each acquired Addressables reference to its owning release path, including failed
  operations: Unity's handle documentation says to release the handle even when the operation failed.
  Check instantiation against the installed package's documented instance-release API, and verify in
  that package whether an `Object.Instantiate` clone of a loaded asset affects the source handle.
  Retain dependencies until their users are finished.
- ⚠️ For any load whose caller can be canceled, name who consumes or releases the eventual result.
  Cancellation and request lifetimes belong to [Scenes](UnityScenesAndLifecycleInstructions.md).
- ⚠️ Releasing a handle does not guarantee immediate physical unloading: Unity's Addressables memory
  documentation says released assets are not unloaded at once, and a bundle unloads when its
  reference count reaches zero. Inspect remaining owners and bundle grouping before labeling resident
  content a leak.
- ⚠️ A ScriptableObject created/cloned for runtime use can legitimately hold runtime state with an
  explicit reset/disposal contract. Verify that nested referenced assets of a clone are still shared
  rather than copied, and are safe to share.
- ⚠️ `Resources` content ships in builds. Judge its actual size/use and the project's policy. A small
  deliberate use does not by itself justify an Addressables migration.
- ⚠️ CPU-readable copies, mipmaps, audio streaming, compression, and stripping are workload/platform
  choices. Avoid universal percentages, fixed clip-length rules, or blanket UI mipmap bans.

## Validation

Compare memory snapshots across repeated load/use/unload cycles after comparable warmup. Inspect
surviving reference chains and expected cache lifetime; higher residency alone is not proof of a leak.
Read import values back after reimport and verify appearance/playback on the target platform. Read
the build report for shipping-content claims. Mark measurements not performed as Not verified.

General allocation/frame cost belongs in [Performance](UnityPerformanceOptimizationInstructions.md);
GUID/serialized migrations in [Editor tooling](UnityEditorToolingInstructions.md).

Technical reference: [Addressables package documentation](https://docs.unity3d.com/Packages/com.unity.addressables@latest),
and its asynchronous operation handles page. Use the project's installed package for exact release
and platform behavior.

Additional references: [audio import tradeoffs](https://docs.unity3d.com/Manual/class-AudioClip.html),
[duplication tradeoffs](https://docs.unity3d.com/Manual/assets-avoid-duplication.html), and
[runtime asset management choices](https://docs.unity3d.com/Manual/assets-managing-introduction.html).
