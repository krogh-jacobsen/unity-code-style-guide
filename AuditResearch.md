# Audit guides: best-practice research and pressure test

Research date: **26 October 2026**. Scope: all existing documents in
[ProjectAuditGuides](AuditInstructions/ProjectAuditGuides/README.md), with primary-source research
across their disciplines and missing neighboring systems. This is a bounded documentation review,
not proof that every Unity practice is covered or every source claim holds on every Editor version.

## Conclusion

Keep the evidence-first, ownership/lifetime and target-measurement foundation. The main weakness was
some rows promoting a suspicious code shape directly into a defect. A valid implementation can have
multiple ordered writers, small linear scans, shared mutable mappings, polling or one implementation
of an interface. The revised guides require a broken contract, measured budget failure or binding
project rule; architectural improvements remain proposals with explicit tradeoffs.

Official manuals establish supported API behavior and describe tradeoffs. They do not establish one
universally optimal architecture. The audit criteria below are engineering inferences from those
contracts unless explicitly described as API facts. Repository naming/stack decisions remain local
conventions. The user authorized this research and guide maintenance; the target-project review
workflow still requires selection and confirmation before changing a game.

## Pressure test of every existing discipline

| Existing discipline | Verdict | Result and primary evidence |
|---|---|---|
| Review router | Keep; clarify | Retain scope, sampling, source context and honest Not verified results. Added an explicit distinction between documented behavior, project rules and proposals; expanded conditional detection and specialist limits |
| Animation | Keep; revise; add | State reads and multiple writers are not automatic defects. Transition duration depends on Fixed Duration; add clock alignment and link deformation bounds to Rendering. [Transitions](https://docs.unity3d.com/Manual/class-Transition.html), [update modes](https://docs.unity3d.com/ScriptReference/AnimatorUpdateMode.html), [root-motion ownership](https://docs.unity3d.com/ScriptReference/Animator-applyRootMotion.html) |
| Physics (3D) | Keep; revise; add | Speed × step is a tunnelling screen rather than proof; assess actual transform/query/simulation order. Add ray-origin-inside and interpolation contracts. [Raycast](https://docs.unity3d.com/ScriptReference/Physics.Raycast.html), [synchronization](https://docs.unity3d.com/ScriptReference/Physics.SyncTransforms.html), [interpolation](https://docs.unity3d.com/Manual/rigidbody-interpolation.html) |
| Audio | Keep; revise; add | Keep routing, units and mixer timing. Validate mutable pool state rather than rewriting invariant fields. Add paused-source completion, voice priority and music-clock checks. [isPlaying](https://docs.unity3d.com/ScriptReference/AudioSource-isPlaying.html), [priority](https://docs.unity3d.com/ScriptReference/AudioSource-priority.html), [scheduling](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html), [SetFloat](https://docs.unity3d.com/ScriptReference/Audio.AudioMixer.SetFloat.html) |
| Rendering | Keep; expand | Custom-pass checks missed ordinary scene content. Add lighting/probes, LOD/occlusion, skinned bounds and particle/VFX simulation; retain pipeline-specific Render Graph contracts. [Lighting data](https://docs.unity3d.com/Manual/LightmapSnapshot.html), [LOD](https://docs.unity3d.com/Manual/class-LODGroup.html), [skinned bounds](https://docs.unity3d.com/Manual/class-SkinnedMeshRenderer.html), [particles](https://docs.unity3d.com/Manual/PartSysMainModule.html) |
| Assets and memory | Keep; revise; add | Reconcile contradictory audio ownership. Imports/residency/readiness belong here; playback belongs in Audio. Duplication/grouping can be intentional. Add audio load-readiness evidence. [Audio import](https://docs.unity3d.com/Manual/class-AudioClip.html), [duplication](https://docs.unity3d.com/Manual/assets-avoid-duplication.html), [asset-management choices](https://docs.unity3d.com/Manual/assets-managing-introduction.html) |
| Performance | Keep; revise; add | Retain representative target captures and comparable conditions. Qualify linear collections/lookups/query masks as candidates until cost/rule evidence exists. Distinguish active CPU/GPU work from waiting. [Highlights Profiler](https://docs.unity3d.com/Manual/ProfilerHighlights.html), [pool constructor](https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1-ctor.html) |
| Scenes and lifecycle | Keep; revise | Async work needs a safe owner, not a mandatory token at every await. Unload-first transitions can be intentional. Correct equal-lifetime assumptions; null patterns bypass overloaded equality. Record Awaitable version differences. [Continuations](https://docs.unity3d.com/Manual/async-awaitable-continuations.html), [C# null patterns](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns) |
| Design | Keep as proposals; revise | Remove automatic findings based solely on discovery/static access, public mutability or one interface implementation. Judge invariant bypass, caller/setup cost and actual dependency policy. This is a project-dependent engineering assessment, not an API prohibition |
| Persistence | Keep; revise | Reconstructible derived UI values need not be saved. Small non-sensitive progress in PlayerPrefs is not automatically wrong; integrity/recovery determines suitability. Sensitive data remains inappropriate, and the Web limit remains relevant. [PlayerPrefs](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html) |
| UI Toolkit | Keep; revise | Binding polling is supported; repeated queries, inline geometry and unmatched selectors need demonstrated impact or a binding rule. Preserve tree/recycled-item identity checks. [Runtime binding sources](https://docs.unity3d.com/Manual/UIE-runtime-binding-define-data-source.html) |
| uGUI | Keep | Existing caveats correctly treat layout, hidden input and Canvas splitting as behavior/cost decisions. Keep live layout/input evidence and measurement before splitting. [Auto layout](https://docs.unity3d.com/Packages/com.unity.ugui@latest/index.html?subfolder=/manual/UIAutoLayout.html), [Unity UI optimization](https://learn.unity.com/topics/best-practices/guide-optimizing-unity-ui) |
| Input | Keep; qualify | Keep action ownership, UI/gameplay arbitration and input latching. Global device reads can be intentional shortcuts; report a pairing failure rather than API occurrence alone. [UI support](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/index.html?subfolder=/manual/UISupport.html), [interaction phases](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/index.html?subfolder=/manual/Interactions.html) |
| Assemblies | Keep | Preserve effective assembly mapping, optional-package constraints and normal-player evidence. GUID/name consistency is documented; absence of asmdefs is a choice. [File format](https://docs.unity3d.com/Manual/assembly-definition-file-format.html), [assembly creation](https://docs.unity3d.com/Manual/assembly-definitions-creating.html) |
| Testing | Keep; correct | EditMode UnityTest can yield null, not only Editor instructions. Require failure-sensitive high-value scenarios rather than an automatic three-tests-per-command rule. [UnityTest API](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityTestAttribute.html) |
| Editor tooling / integrity | Keep; add; revise | Add missing SerializeReference types and callback thread/order safety. Require guaranteed import-resume cleanup. Initialization file I/O alone is not a defect; asset import availability matters. [Missing managed types](https://docs.unity3d.com/ScriptReference/SerializationUtility.HasManagedReferencesWithMissingTypes.html), [callbacks](https://docs.unity3d.com/ScriptReference/ISerializationCallbackReceiver.html), [initialization](https://docs.unity3d.com/ScriptReference/InitializeOnLoadAttribute.html) |
| Diagnosis mode | Keep; extend routing | Retain reproduce/hypothesis/probe/cause/acceptance distinctions. Route new subsystem symptoms to their owning lenses; a symptom disappearing alone still does not establish cause |

## Missing disciplines added

Each new lens has detection, evidence/finding criteria, caveats, validation and primary references.
They remain read-only references loaded through the review router; they do not run every time.

| New lens | Important gap addressed | Primary evidence |
|---|---|---|
| [Navigation](AuditInstructions/ProjectAuditGuides/UnityNavigationInstructions.md) | Request success differs from completed/reachable arrival; multilevel samples and movement handoffs need inspection | [SamplePosition ignores obstructions](https://docs.unity3d.com/ScriptReference/AI.NavMesh.SamplePosition.html), [component integration](https://docs.unity3d.com/Packages/com.unity.ai.navigation@latest/index.html?subfolder=/manual/MixingComponents.html) |
| [Physics2D](AuditInstructions/ProjectAuditGuides/UnityPhysics2DInstructions.md) | Separate body/contact matrix, ray-origin behavior and simulation timing from 3D | [Kinematic contact rules](https://docs.unity3d.com/Manual/2d-physics/rigidbody/body-types/kinematic/kinematic-body-type-reference.html), [ray origins](https://docs.unity3d.com/ScriptReference/Physics2D.Raycast.html), [manual stepping](https://docs.unity3d.com/ScriptReference/Physics2D.Simulate.html) |
| [Localization/accessibility](AuditInstructions/ProjectAuditGuides/UnityLocalizationAccessibilityInstructions.md) | Supported content/fallback/formatting, locale lifecycle, real script layout and player barriers | [Pseudo-localization](https://docs.unity3d.com/Packages/com.unity.localization@latest/index.html?subfolder=/manual/Pseudo-Localization.html), [initialization](https://docs.unity3d.com/Packages/com.unity.localization@latest/index.html?subfolder=/api/UnityEngine.Localization.Settings.LocalizationSettings.html), [Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/) |
| [Networking](AuditInstructions/ProjectAuditGuides/UnityNetworkingInstructions.md) | Authority, durable late-join state, local/remote timing, connection trust and recovery | [Replicated state](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest/index.html?subfolder=/manual/basics/networkvariable.html), [RPCs](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest/index.html?subfolder=/manual/advanced-topics/message-system/rpc.html), [approval](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest/index.html?subfolder=/manual/basics/connection-approval.html) |
| [Entities](AuditInstructions/ProjectAuditGuides/UnityEntitiesInstructions.md) | Worlds/groups, job dependencies, ECB scope/playback and shipped baked content | [Update order](https://docs.unity3d.com/Packages/com.unity.entities@latest/index.html?subfolder=/manual/systems-update-order.html), [ECB safety](https://docs.unity3d.com/Packages/com.unity.entities@latest/index.html?subfolder=/manual/systems-entity-command-buffers.html) |
| [Terrain](AuditInstructions/ProjectAuditGuides/UnityTerrainInstructions.md) | Tile edges, height synchronization, collision agreement and streamed/shipped content | [Neighbors](https://docs.unity3d.com/ScriptReference/Terrain.SetNeighbors.html), [height synchronization](https://docs.unity3d.com/ScriptReference/TerrainData.SyncHeightmap.html) |
| [Cameras/cinematics](AuditInstructions/ProjectAuditGuides/UnityCamerasCinematicsInstructions.md) | Target clock, output/channel selection, bindings and interrupted authority handoff | [Cinemachine Brain](https://docs.unity3d.com/Packages/com.unity.cinemachine@latest/index.html?subfolder=/manual/CinemachineBrain.html) |

Effects use the expanded Rendering lens rather than another overlapping checklist. Particle/VFX
bounds, simulation clock/space, stop/reuse and completion need behavior evidence; effects capacity
must distinguish intentional decorative saturation from lost required feedback. See
[VFX initialization](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest/index.html?subfolder=/manual/Context-Initialize.html)
and [particle child completion](https://docs.unity3d.com/ScriptReference/ParticleSystem.IsAlive.html).

## Concrete counterexamples used to challenge the rules

- An Animator read can intentionally govern a hit window; ask whether interruption produces wrong
  effects before recommending another state owner.
- A paused AudioSource reports false from isPlaying; returning every such source to a pool loses its
  resume even if a fixed clip timer was removed.
- A radius sample near a destination can land on another floor; successful sampling is insufficient
  for a “walk there” command.
- A small shared bundle dependency can be cheaper than cross-bundle coupling; duplication count alone
  is not a measured problem.
- An EditMode UnityTest yielding null is legitimate; a full runtime coroutine environment is a
  different capability.
- A server-only write rule copied from older multiplayer advice can reject an intentional distributed
  authority topology. Match the actual topology and package permissions.

## Verification and remaining boundaries

Research inspected substantive official pages, using versioned package pages when latest wrappers
were unavailable to the browser. Published guide links remain unversioned per repository policy;
consumers must resolve the installed version. Inspected versions include engine 6000.6, AI Navigation
2.0.16, Localization 1.5.13, NGO 3.1.0, Entities 1.3.15, Cinemachine 3.1.7, VFX Graph 17.0.4/17.7.0 and
Input System 1.14.2. These are evidence identities, not recommended upgrade targets. Source URLs can
redirect to newer editions; the researched facts are not a compatibility claim for all versions.

No fixed particle counts, terrain density, clip-length thresholds, contrast ratios or universal
architecture/pipeline migrations were introduced. Accessibility guidance informs barriers/options;
it does not confer certification. Exact Timeline binding API verification was unavailable, so its
lens uses observable binding and handoff contracts. Older terrain manual pages supplied orientation
only; current API references support the added neighbor/synchronization checks.

DOTS Physics contacts/solver behavior, Netcode for Entities ghost prediction/rollback, XR platform
integration, backend/economy/IAP security, custom AI and third-party authoring systems remain specialist
coverage beyond stated rows. Full review means selected applicable lenses, not exhaustive certification
of a game. No target Unity project, live scene, player, network simulation or device was exercised.
[Validation.md](Validation.md) records the actual repository checks separately.

## Fresh-agent follow-up — 26 October 2026

Five fresh sessions tested 38 initial and 16 corrective fictional cases without expected outcomes.
All 54 decisions matched the parent-reviewed expectations. Separately, the readers identified eight
instruction defects; fixes qualify audio slider units/range, finite query completeness, unverified
collider shapes, additive scene placement, initialization readiness, measured uGUI rebuild cost and
static versus Editor-assisted integrity checks. Six detached checklist sections were also rejoined,
and a local parser now catches that Markdown failure with five regression fixtures.

The [evidence archive](AuditInstructions/Tools/discipline_review_replay_results_2026-10-26.json)
retains fixture inputs, expected outcomes, full response JSON, grading notes and frozen source text/hashes.
Each fresh session handled several cases; this is not 54 isolated fresh sessions, actual Unity tests,
or proof of universal agent compliance. See Validation.md for full repository gates.
