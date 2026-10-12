# Unity asset and memory audit

Load for asset loading/release, retained memory, import cost, or build content. Apply the
[shared evidence standard](README.md#evidence-standard). Import recipes belong to skills such as
`prepare-unity-3d-asset`, `optimize-audio`, and sprite atlas management, or
[project presets](../SetupInstructions/Presets.md).

## Establish ownership

Map asset acquisition, consumers, retention, and release for each relevant lifetime. Distinguish
managed wrappers from native asset memory, source assets from runtime instances, and intended caches
from leaks. Follow serialized references transitively; a small configuration asset can retain large content.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Load ownership | Handles, multiple loads/acquires, sharing, replacement | A consumer uses an asset after release or an owner loses the handle needed for release |
| Failure/cancellation | Completion and cleanup after disable/destroy/request replacement | A late result leaks, failed load leaves a handle, or stale data replaces current content |
| Instantiation | Addressables creation path, clones, instance release | Cleanup does not match acquisition or a dependency is released while an instance still uses it |
| Runtime resources | Materials, textures, render targets, meshes, SO clones | Created native objects have no disposal/destroy owner or retained users outlive them |
| Shared configuration | Runtime writes and nested referenced assets | Per-session changes mutate source content or unintentionally affect another consumer |
| Import residency | Actual platform format, size, Read/Write need, mips, audio role | Measured or estimated cost exceeds the budget without a justified runtime need |
| Bundle/atlas dependencies | Build layout, duplicate dependencies, content grouping | Unrelated content is retained together or duplicated at material cost |
| Shipping content | Build report, Resources, stripping/preservation, platform overrides | Unneeded content ships or required dynamic content is stripped/missing |

## Ownership cases to verify

- Match each acquired Addressables reference to the owning release path, including failed operations.
  Match instantiation to the installed package's instance-release contract and handle tracking mode.
  Ordinary `Object.Instantiate` clones do not automatically acquire their source handle; retain
  dependencies until their users are finished.
- A canceled caller may still have an in-flight load. Trace who consumes or releases its eventual
  result. Inspect [Scenes](UnityScenesAndLifecycleInstructions.md) for request/enable lifetimes.
- Releasing a handle does not guarantee immediate physical unloading of a bundle. Inspect remaining
  owners and bundle grouping before labeling resident content a leak.
- A ScriptableObject created/cloned for runtime use can legitimately hold runtime state with an
  explicit reset/disposal contract. Cloning it does not deep-clone every referenced asset; verify
  that nested content is still safe to share.
- `Resources` content is included in builds; it is not all loaded into runtime memory at startup.
  Judge its actual size/use and the project's policy. A small deliberate use does not by itself
  justify an Addressables migration.
- CPU-readable copies, mipmaps, audio streaming, compression, and stripping are workload/platform
  choices. Avoid universal percentages, fixed clip-length rules, or blanket UI mipmap bans.

## Validation

Compare memory snapshots across repeated load/use/unload cycles after comparable warmup. Inspect
surviving reference chains and expected cache lifetime; higher residency alone is not proof of a leak.
Read import values back after reimport and verify appearance/playback on the target platform. Read
the build report for shipping-content claims. Mark measurements not performed as Not verified.

General allocation/frame cost belongs in [Performance](UnityPerformanceOptimizationInstructions.md);
GUID/serialized migrations in [Editor tooling](UnityEditorToolingInstructions.md).

Technical reference: [Addressables handle ownership](https://docs.unity3d.com/Packages/com.unity.addressables@2.3/manual/AddressableAssetsAsyncOperationHandle.html).
Use the project's installed package for exact release and platform behavior.
