# Unity asset and memory audit

Load for asset loading/release, retained memory, import cost, or build content. Addressables rows
apply only when `com.unity.addressables` is installed; bundle and atlas rows apply only when the
project uses Addressables, AssetBundles, or SpriteAtlas. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Import recipes belong to skills such as
`unity:optimize-audio` and `unity:manage-sprite-atlas` when available, or to
[project presets](../Presets/README.md). Audio import and memory choices go to `unity:optimize-audio`
or [Audio](UnityAudioInstructions.md), not here.
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
| Shared configuration | Runtime writes and nested referenced assets | Code assigns a field of a ScriptableObject or prefab asset referenced by more than one consumer, or `git diff` shows the asset changed after exiting Play |
| Import residency | Actual platform format, size, Read/Write need, mips, audio role | An importer's platform size, Read/Write, or mip setting exceeds the project's stated budget or its [presets](../Presets/README.md) with no runtime need; with no stated budget, report sizes and record "no budget" |
| Bundle/atlas dependencies | Build layout, duplicate dependencies, content grouping | The build layout or build report shows one asset in more than one group/bundle, or a group whose members are never used together |
| Shipping content | Build report, Resources, stripping/preservation, platform overrides | The build report lists content with no reference path, or a type used by reflection or serialization is missing from a stripped build (needs a build to confirm) |

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
