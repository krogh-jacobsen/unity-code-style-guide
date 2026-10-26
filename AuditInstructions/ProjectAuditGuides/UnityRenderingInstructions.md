# Unity rendering-correctness audit

Load for owned rendered content: features/passes, shaders, cameras, lighting, LOD/occlusion,
skinned meshes, particles, or VFX Graph. Apply only rows relevant to the selected scene/pipeline. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Establish the installed pipeline and
version first; the Render Graph rows apply only to the active Render Graph path. Compatibility-mode,
Built-in, and HDRP code need their own installed documentation rather than a forced URP migration.
**Last verified: October 2026.**

This lens owns rendering correctness. [Performance](UnityPerformanceOptimizationInstructions.md)
owns measured frame cost; [Assets](UnityAssetsAndMemoryInstructions.md) owns general residency and
shipping content. Use available pipeline-specific review tooling, or inspect installed source and
Unity's Frame Debugger/Render Graph Viewer. Tool availability alone does not prove rendered output.

## Establish the rendered path

Record Graphics and quality-level pipeline assignments, renderer data and camera renderer overrides,
active features, Render Graph versus compatibility mode, target APIs, and relevant shader/material
assets. Trace an affected camera from pass injection through resource production and consumption to
its final output. Inspect saved settings separately from transient runtime state.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Pipeline and feature wiring | Effective pipeline/renderer per quality level and camera; saved feature/material references | A required feature is missing, disabled, or assigned to an unused renderer and the supported scene loses the intended effect; confirm the active path |
| Pass timing and camera scope | Injection event, camera filters, prerequisites, base/overlay/preview cameras | A pass executes before its required input exists, runs on an unintended camera, or applies an effect twice and changes the intended output (capture/live run) |
| Graph resource declarations | Actual texture/buffer reads and writes versus builder declarations, attachments, and access modes | Execution uses a resource absent from the recorded dependency contract or uses an incompatible access mode; confirm against the installed API and graph validation |
| Graph lifetime | Internal handles, imported external resources, frame/camera transitions, owner cleanup | An internal resource handle is reused across graph instances/frames/cameras, or an external resource is released while a pass still uses it; identify the owner and exact lifetime |
| Recording and execution | Pass data, render function, mutable feature/camera state | Deferred execution observes another camera's or a later pass's mutable data instead of the data recorded for this pass, producing wrong output; inspect captured state and test multiple cameras |
| Output dependency | Consumers of each result, graph culling, global-resource declaration | A required result has no declared consumption/side-effect path and its pass is removed, or a consumer reads a resource before its producer (graph inspection plus output check). An intentionally unused pass being culled is correct |
| Target compatibility | Texture descriptors, dimensions, MSAA/depth/format, shader pass and API requirements | The configured target or shader is unsupported by the selected pipeline/API, or resizing/quality switching produces invalid attachments or wrong pixels; use installed support rules and device/build evidence |
| Camera stacking | Saved base/overlay stack, renderer support, ordering, clear/output policy | The intended overlay is absent, clears required content, or composites in the wrong order; confirm supported stacking in this pipeline/version and the resulting image |
| Shader/material compatibility | Actual material/shader assignment, compile log, required variants in a release player | A supported scene renders an error/missing effect due to a pipeline mismatch, compile failure, or missing required variant. Variant/shipping ownership: [Assets](UnityAssetsAndMemoryInstructions.md) |
| Lighting data/probes | Intended realtime/mixed/baked setup, saved lighting data, loaded scene combinations, supported probe system | Missing/stale data or missing intended probe coverage causes wrong supported output on scene/player load; realtime-only lighting and pipeline-specific probe choices are valid |
| LOD/occlusion | Renderer membership, bounds, thresholds, visibility data, actual quality/camera path | Camera movement hides required visible content or selects incorrect/missing geometry; missing LOD or occlusion alone is a measured-cost proposal |
| Deformation bounds | Skinned/procedural poses, runtime clips, actual culling bounds | Valid deformation leaves bounds and disappears; larger bounds/offscreen updates trade visibility correctness against work |
| Effect simulation | Particle/VFX space, clock, bounds/culling, stop/clear, pause/offscreen and pool cycles | Required effects disappear, move in the wrong coordinate frame, retain old particles on reuse, or never complete their owning checkout; inspect VFX dynamic-bounds recomputation in the installed package |
| Effect capacity/completion | Particle limits, bursts, child/sub-emitter completion and stop/reuse paths | Supported required feedback is dropped at capacity, or checkout completion omits live child effects. Decorative saturation and explicit cancellation can be intentional; judge actual outcome |

## Interpret with care

- Internal Render Graph resources are managed by the graph and cannot be carried between frames or
  cameras. Imported resources remain owned externally; their underlying allocation can persist, but
  import it into the graph that uses it. Retention alone is not a leak.
- Record dependencies and pass data during recording; issue rendering commands in the pass's
  execution function. Inspect the installed APIs for global resources and intentional side effects.
- Graph culling, camera filtering, shader keywords, and compatibility mode are legitimate choices.
  Report a broken contract or binding project-rule violation rather than banning a setting.

## Validation

Use the real scene with the feature enabled and disabled, then test applicable resize, quality/API
switching, multiple cameras, and scene reload paths. Inspect the graph/Frame Debugger and output;
compile and run an agreed release player for shader/API claims. Reopen saved renderer and camera
assets to verify configuration survives. Record absent Editor/device/build checks Not verified.

Technical references: [Render Graph resources and lifetime](https://docs.unity3d.com/Manual/urp/render-graph-introduction.html),
[recording dependencies and executing a pass](https://docs.unity3d.com/Manual/urp/render-graph-write-render-pass.html),
[imported textures](https://docs.unity3d.com/Manual/urp/render-graph-import-a-texture.html), and
[camera stacking](https://docs.unity3d.com/Manual/urp/camera-stacking.html).

Additional references: [lighting data](https://docs.unity3d.com/Manual/LightmapSnapshot.html),
[light probes](https://docs.unity3d.com/Manual/LightProbes.html),
[LOD bounds](https://docs.unity3d.com/Manual/class-LODGroup.html),
[occlusion tradeoffs](https://docs.unity3d.com/Manual/OcclusionCulling.html),
[skinned bounds](https://docs.unity3d.com/Manual/class-SkinnedMeshRenderer.html),
[particle space/time](https://docs.unity3d.com/Manual/PartSysMainModule.html), and
[VFX bounds/culling](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest/index.html?subfolder=/manual/VisualEffectGraphAsset.html).
For URP native-pass/XR paths, inspect legacy blit wrappers against
[URP blit compatibility](https://docs.unity3d.com/Manual/urp/customize/blit-overview.html);
use supported installed APIs rather than applying a Built-in API ban across pipelines.

Include applicable clean-player lighting loads, probe transitions, LOD camera distances,
deformation, and offscreen/pause/pool effect cycles in validation. Record missing device/build checks
Not verified; pipeline package presence alone is not evidence those content paths are used.

Effect references: [VFX capacity](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest/index.html?subfolder=/manual/Context-Initialize.html)
and [particle child completion](https://docs.unity3d.com/ScriptReference/ParticleSystem.IsAlive.html).
