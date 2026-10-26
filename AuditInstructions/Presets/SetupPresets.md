> How it works: give this URL to your agent, for example "Install the import presets I need from
> this document into my Unity project". The agent audits your project first and recommends
> presets, lets you pick which to carry over, and changes nothing before you confirm the exact list.
> It then installs only those presets and, if you choose, applies them to existing assets or
> registers them as defaults. Human overview: [readme](README.md).

# Set up import presets (agent instructions)

Install selected import presets into an existing Unity project and, only when the user asks,
apply them to existing assets or register them as default import rules. This document is
self-contained; it fetches the preset files from the source below. **Last verified: October 2026.**

Source (replace `main` with a commit SHA for a repeatable run):
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/AuditInstructions/Presets/`
Each preset is two files, `<Role>/<Name>.preset` and `<Role>/<Name>.preset.meta`. The license is
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/LICENSE`.

## Operating rules

- Do three separate things only when selected, in this order: **install/update** (manage selected preset assets),
  **apply** (change existing asset importers), **register** (future-import rules). Install is the
  recommended default.
- For first installation, copy shipped bytes and metadata unchanged. Update imported presets only
  through the confirmed Editor workflow in step 3; preserve destination metadata and references.
  Never hand-edit serialized preset YAML, invent GUIDs, or delete metadata to force a re-import.
- The presets are tuned for desktop PC and Mac games (Windows and macOS standalone). When the
  project also targets mobile, Web, console, or VR, tell the user the audio and model policies were
  not reviewed for those targets and ask before applying them; the texture role presets are
  platform-neutral.
- Preserve the target's own instructions, unsaved work, vendor assets, and customized importers.
- Do not apply a preset to vendor or third-party assets, or to anything outside owned folders.
- Report observed results separately from checks you could not run (**Not verified**). Copying a
  preset proves a file arrived, not that any policy took effect.

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit user confirmation.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Present the exact changes for the picked subset (files, settings, values, commands)
   and obtain explicit user authorization before making them, including saving the report.
   Confirmation need not contain the literal word "yes": after the concrete scope is presented,
   "implement R1 and R3" can both select and confirm those items. Selection alone ("R1 and R3")
   chooses scope without authorizing implementation. Honor existing authorization for unchanged
   scope without asking again; clarify a delayed reply only when its scope is materially ambiguous.
   Resolve IDs against the presented change list rather than guide defaults. If evidence establishes
   that exact scope was previously presented and authorized but its record is now unavailable,
   retrieve that record before execution; recovered unchanged scope needs no repeat confirmation.
   If concrete changes were never presented, an instruction to implement an ID leaves scope
   unconfirmed: first present the exact changes and obtain confirmation before execution.
   Changed scope needs confirmation for the changed items. In a non-interactive session, or when
   authorization is absent, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

Here, steps 1 and 2 are the audit and the recommendations; steps 3 to 6 run only for confirmed items.
A correction that fulfills the approved policy, preset identities, owned paths, and preservation
requirements stays within that authorization: for example, fixing filter syntax or using a targeted
save route after a failed readback. Record the correction and rerun affected checks. A changed policy,
additional path or asset, migration, or broader write becomes a new recommendation for confirmation.

## 1. Preflight

Read the target's instructions. Identify one Unity project: the user's destination or the current
workspace, containing `Assets` and `ProjectSettings/ProjectVersion.txt`. Record:

- Editor version, whether that Editor is open, and source-control state.
- Target platforms (Build Profiles and the active build target), to apply the desktop rule above.
- Presets throughout `Assets` and available package assets, including bundled reference copies;
  record path, GUID, content/source revision, and whether each is an active installation or reference.
  Read Preset Manager registrations and relevant scripts/configuration referencing these paths.
- The established active installation path (for example `Assets/Presets`). Reuse it; use
  `Assets/Settings/Presets/<Role>/` only for a new installation without an established path.
  Resolve multiple candidates before recommending a destination; migration is a separate selection.
- Existing helpers' API compatibility and write scope: inspect list replacement, save calls, and
  side effects before proposing execution. Record unrelated dirty assets/scenes to preserve.
- For an update, immutable old/new source revisions and actual local content. Match by GUID and
  path; a matching GUID establishes identity, not that content is unmodified. Mark a missing baseline
  unknown and compare manually before recommending replacement.
- The source revision you will use. Resolve `main` to a commit when you can and report it.

**Done:** the target, Editor state, existing presets, and source revision are known, and the audit
(stage 1) was reported without writing anything.

## 2. Ask and select

Ask in one batch. Each default is the recommendation for that question; it takes effect only after
stage 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Which operations: install/update preset assets, apply to existing assets, register defaults? | First installation only; updates individually proposed |
| Which asset roles do you have: textures (albedo, normal, mask, UI sprite), audio (music, ambience, SFX, UI), static models, animation-only? | Only roles with real content in the project |
| For apply or register: which owned folders? | None; ask for exact folders |
| Which audio policy for each kind of clip? | One policy per clip; ask when unclear |
| Separate platform texture/audio budget review? | No; optionally recommend the handoff in step 6 |

Select presets from this inventory. Fetch only the selected pairs; do not copy the whole folder.

| Preset (path under the source) | Use | Policy | GUID |
|---|---|---|---|
| `Textures/AlbedoTextureImporter` | Tiling world color | Default texture, sRGB, mipmaps, repeat, bilinear; CPU read off | `f61eb0483155c4510af0ab38dfedddf2` |
| `Textures/NormalTextureImporter` | Tangent-space normals | Normal map, linear, mipmaps, repeat, bilinear; CPU read off | `e909e14824a2d4c7bbbddfffaad65823` |
| `Textures/MaskTextureImporter` | Packed linear material data | Default texture, linear, mipmaps, repeat, bilinear; CPU read off | `c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4` |
| `Textures/UISpriteTextureImporter` | Screen-space UI sprites | Sprite, sRGB, no mipmaps, clamp, bilinear, alpha transparency; CPU read off | `2e363ae08c3a848c7854d798a8dd05f2` |
| `Audio/MusicAudioImporter` | Long music | Streaming, Vorbis 0.7; background load | `6ad43c7dea473466bb6e33ba84426394` |
| `Audio/AmbienceAudioImporter` | Long ambience loops | Streaming, Vorbis 0.7; background load | `2ab0a5b23622b46e691e0ba9fba25ecf` |
| `Audio/SFXAudioImporter` | Short, frequent effects | Decompress on load, Vorbis 0.7; preload | `b5cd1643fcc1e4237a3652bde885ab25` |
| `Audio/UIAudioImporter` | Short UI feedback | Decompress on load, Vorbis 0.7; preload | `d7473bccbe2ca42bba6967e205d90af3` |
| `Audio/UIShortAudioImporter` | Tiny UI clicks where codec artifacts matter | Decompress on load, PCM; preload, foreground load | `3f34697a999664156938eab0b9439b00` |
| `Audio/SpatialSFXAudioImporter` | Noisy repeated positional effects | Compressed in memory, ADPCM, force mono; preload, foreground load | `22dbbcb91dde34dc39cbf56beb605c18` |
| `Audio/LayeredAmbienceAudioImporter` | Short overlapping ambience loops | Compressed in memory, Vorbis 0.7; preload, background load | `370ad86a5eb1d47e9a43f258a1e6e80e` |
| `Models/FBXModelImporter` | Static meshes with external materials | No animation, no generated colliders, read/write off; material creation off | `5fbe9a9b7b7441dea18aa7fce90c4820` |
| `Animations/FBXAnimationImporter` | Animation-only source with an existing rig | Import animation; preserve rig, clips, avatar, geometry, materials, scale | `a1c8dd08508c4341a75ed3fd45a1bfd5` |

Rules for choosing:

- Choose **one audio policy per clip**; the audio presets are alternatives, not layers. UIShort suits
  tiny clicks when PCM size is acceptable. SpatialSFX suits noisy overlapping positional effects, and
  forces mono (keep stereo for authored stereo beds and music). LayeredAmbience suits short loops that
  would otherwise create many streams; use Ambience for long beds.
- Classify audio by actual playback use, duration, expected concurrent voices, and spatial/stereo
  requirements; folder names are evidence, not policy. A mixed Ambience folder may contain both long
  beds and tiny animal calls. Recommend narrower existing subfolders or explicit asset mappings;
  folder restructuring needs its own confirmation. Ambiguous future imports remain unregistered.
- Keep the animation-only preset distinct from a character or rig import policy.
- **Models:** the FBX Model preset turns Read/Write off. Unity requires Read/Write on for meshes used
  by a Mesh Collider, a Particle System shape, or a Terrain detail mesh, or the Player build can
  fail. Before applying, ask which meshes need those uses and exclude them (or re-enable Read/Write).
- **Audio length:** SFX and UI decompress on load (Vorbis then takes about ten times its compressed
  memory), so use them only for short clips. For longer or numerous effects choose Spatial SFX or
  Layered Ambience.
- **Textures:** alpha-cutout textures (foliage) also need mip preserve-coverage, which the Albedo
  preset does not set; pixel-art sprites need point filtering and are outside these presets.
- Each preset is partial: it includes only its listed policy and preserves everything else, including
  user data, bundle labels, external mappings, and platform overrides.

Turn the answers into numbered recommendations (stage 2): one per preset worth installing or updating (only for
roles with real content), one each for applying to existing assets, registering defaults, and a separate platform-budget
review handoff (step 6). Give each its finding from the audit, why it matters, risk, and a default. The user
may pick any subset (stage 3), then confirms the exact list (stage 4).

**Done:** the recommendations were shown, the user picked from them, and the selected presets, the
operation, and any exact target folders or assets were confirmed before any file was written.

## 3. Install or update

Only the preset installations or updates confirmed in stage 4. Stage first, then check every destination.

1. **Stage.** Download each selected `.preset` and `.preset.meta` into a temporary folder outside
   the target's `Assets`, plus the license. URL-encode filenames with spaces. Reject HTML or error
   responses, and any pair that is missing a half.
2. **Verify.** Each `.meta` must contain the `guid:` from the table above. Stop on a mismatch.
3. **Preflight destinations.** Use the established active path from preflight; a new installation
   defaults to `Assets/Settings/Presets/<Role>/<Name>.preset`, with its `.meta` beside it. Reject
   path traversal, symlinked entries, and case-only collisions. Check each GUID against existing project assets, including package assets.

   | Destination state | Action |
   |---|---|
   | Absent and the GUID unused | New: install |
   | Same bytes and GUID at the path | Already installed: leave it |
   | Same identity and verified intended effective properties/exclusions after an Editor resave | Already current: retain local serialization and metadata |
   | Same GUID elsewhere at the established active path | Reuse that path; classify its content before planning work |
   | Different content with the destination GUID intact | Update candidate: compare baseline → local and baseline → upstream |
   | Different-GUID reference copy | Separate asset: preserve it and its references; identify the selected active copy |
   | A half pair, duplicate GUIDs, unresolved destination, or identity mismatch | Conflict: report paths and resolve before writes |

4. **Execute the selected branch.**
   - **First installation:** with the target's Editor closed, create only missing directories and
     copy staged pairs intact; Unity generates folder metadata. With the Editor open, use an
     approved import route preserving the pairs, or ask the user to close that Editor.
   - **Update:** classify upstream-only, local-only, overlapping, and unknown-baseline differences.
     Present effective included-property and exclusion-policy changes, source/destination identities,
     affected default rules, exact Editor commands, and recovery/validation steps before confirmation.
     Preserve local-only changes; resolve overlaps/unknown baselines explicitly. Keep recovery bytes
     outside `Assets`. Load the pinned source preset through an available, project-approved Editor
     route and update the existing asset through version-checked Editor APIs; preserve its GUID,
     metadata, references, and unrelated importer settings. Test that route on a disposable copy
     before changing the destination. Keep source inspection in a separate disposable project when
     needed to avoid importing a duplicate source GUID into the target. If no safe route exists,
     leave the destination untouched and
     report Update Not verified. An Editor-resaved preset may differ in bytes: compare effective
     properties and exclusions, rather than promising byte-identical upstream serialization.
   Install no bridge/package or permanent updater. Closing the Editor does not authorize filesystem
   replacement of an imported preset. Application to existing asset importers remains step 4 only.
5. **License.** Place the MIT license in the project's existing third-party notices location outside
   `Assets`, or at `ThirdPartyNotices/UnityCodeStyleGuide-LICENSE.txt`. Reuse an identical notice;
   preserve unrelated ones.
6. **Import and read back.** Import through existing Editor access, or open the project when that is
   safe and in scope. Read each installed asset's bytes and GUID; check the logs for fresh errors.
   For updates, also read back effective properties/exclusions and existing references after a
   targeted save and reload; metadata must remain unchanged. Record actual per-preset source revisions
   for partial outcomes. A repeat run must plan no copies or updates. With no safe import route,
   report files copied (first installations only) and import **Not verified**, with the next action.

**Done:** every selected preset is installed, updated, already present, or explicitly unresolved;
the license is placed for completed work, completed items need no further writes, and import/update
policy, identity, reference, and saved-state checks have observed results or explicit pending checks.

## 4. Apply to existing assets (only when selected and confirmed)

Only the targets confirmed in stage 4. Preview the exact owned asset paths and each preset's role before changing anything; resolve
overlapping or incompatible mappings first. Run the procedure through an Editor method driven by
Unity CLI or an available C# execution command (discover the installed commands; the CLI has no
universal preset subcommand):

1. Load the preset with `AssetDatabase.LoadAssetAtPath<Preset>()` and get the target's
   `AssetImporter`. Require `preset.CanBeAppliedTo(importer)`.
2. Record each target's GUID, platform overrides, metadata, and designer-authored values (slices,
   borders, pivots, material mappings, rigs, clips, scale).
3. Call `preset.ApplyTo(importer)` and require success, then `importer.SaveAndReimport()`. For an
   unconfigured UI sprite choose Single (one icon) or Multiple (a sheet, with slicing) explicitly,
   and preserve an existing mode and geometry.
4. Read the importer back after the reimport: intended values present, preserved values unchanged,
   GUIDs unchanged. Check a representative scene or prefab that references the asset.

Never delete metadata or use the Inspector's Reset to apply a policy. On a rerun, skip targets that
already match. With no available Editor route, leave importers untouched and report Not verified.

**Done:** each target matches its policy after reimport, preserved values are intact, and any
unperformed application is stated.

## 5. Register as defaults (only when selected and confirmed)

Only the rules confirmed in stage 4. Defaults configure new imports; they do not reconfigure existing
asset importers. Use Project Settings > Preset Manager or version-checked Editor APIs. The documented
getter is `Preset.GetDefaultPresetsForType(PresetType)`; use it with
`Preset.SetDefaultPresetsForType(PresetType, DefaultPreset[])`. Confirm signatures, DefaultPreset
members, and a targeted persistence route against the installed Editor before executing helpers.

1. **Preview matching and order.** Scope filters to confirmed owned paths. Glob matching is
   case-sensitive. Use `glob:"Assets/Game/Audio/SFX/**"` for one pattern; alternatives use
   `glob:("Assets/Game/Audio/SFX/**"|"Assets/Game/Audio/UI/**")`. Parentheses go outside the quoted
   alternatives; `glob:"(Assets/Game/Audio/SFX/**)"` is not that alternatives syntax.
   Check matching through Unity's target-version matcher, not a shell or Python glob approximation.
   Preview direct/nested positive paths, case differences, sibling and vendor negatives, and assets
   matching overlapping roles. Include the planned result of the entire ordered list: later entries
   override earlier included properties. Preserve unrelated entries, order, and enabled states.
2. **Register only differences.** Read the existing list, reuse matching entries, and require setter
   success when a change is needed. Inspect helpers before calling them; supplying the entire list
   requires retaining unrelated entries. Add no duplicate registrations. Save only Preset Manager
   configuration through the verified Editor route; a global asset/scene save is outside this task.
3. **Read back memory and disk separately.** Compare the live list and independently read saved
   Preset Manager settings for preset GUIDs, filters, enabled states, and order. Read disk without
   editing serialized YAML. A successful API return or fresh import alone does not prove persistence.
   If either view differs, registration is incomplete; correct within approved scope and repeat.
4. **Exercise genuine new imports.** With no existing metadata, import a representative fixture for
   each distinct rule/policy and relevant overlap into confirmed test paths. Check intended values,
   preserved overrides, and negative paths; create vendor-negative fixtures only in a disposable
   project. Existing-asset Reimport is not this test. Include fixture creation/cleanup in the approved
   validation scope and remove only those test assets through Editor APIs. Install no enforcer.
5. **Verify a no-op rerun.** After fixture cleanup and pending Editor saves settle, rerun configuration.
   Matching rules must cause no setter/save calls, duplicates, or configuration-byte changes. Record
   modification time as supporting evidence in a controlled run, not a universal pass/fail condition.
   Check unrelated dirty assets/scenes and rules remain untouched. A safe reopen/reload is additional
   persistence evidence when in scope; do not close an Editor containing unsaved work to obtain it.

**Compatibility evidence (October 2026):** a disposable 6000.7.0b4 run observed audio/model default
imports passing and texture first-import crashes. A later project session reported a model first-import
crash on the same version; it was not reproduced in this guide revision. These are fixture-specific
observations, not an Editor-wide pass. On that beta use initial import → explicit application (step 4)
for textures; keep model defaults unvalidated pending isolated investigation of the reported crash.
Treat every other version/importer/operation combination as unverified until exercised. Keep prior
and conflicting evidence with Editor, preset revision, importer, operation, fixture, result, and limits;
unknown fields stay unknown. Optional repository history: [validation record](../../Validation.md).

**Done:** every selected rule has separate live, saved-file, match, genuine-import, and no-op results;
unrelated rules/dirty work are preserved. Missing safe routes or fixtures are Not verified, and failed
checks remain failed/incomplete rather than a completed registration.

## 6. Platform budgets (separate selection)

The role presets set data meaning and sampling; they preserve existing resolution, compression, and
platform overrides. Audit those overrides without choosing new budgets in this standalone workflow.
When the user wants budget tuning, recommend a separate build-guide handoff:
[desktop](../BuildSettings/DesktopBuilds.md) or [mobile](../BuildSettings/MobileBuilds.md). That workflow
owns device requirements, measurements, exact values, and confirmation. Missing sibling guidance
never blocks preset installation, application, or registration; no budget change is implied here.

**Done:** existing overrides remain preserved and any requested budget tuning is identified as a
separate recommendation/handoff, rather than an incomplete preset operation.

## 7. Report

| Item | Status | Detail |
|---|---|---|
| Source URL and revision | | |
| Each selected preset | Installed / Updated / Already installed / Conflict | Path, GUID, actual source revision, local adaptations |
| License | Placed / Already present | Location |
| Repeat run | Nothing to do / Work found / Not verified | Copies/updates and registration setter/save calls; configuration-byte comparison |
| Unity import | Verified / Not verified | Next action if pending |
| Apply to assets | Applied / Not selected / Not verified | Targets and readback |
| Register defaults | Registered / Incomplete / Not selected / Not verified | Preset identities, filters, enabled states, order; separate live/disk, match, genuine-import, and no-op results |
| Unpicked recommendations | Proposal | IDs, with the reason each was skipped |

Put conflicts, unanswered choices, unpicked recommendations, and failed checks in a "Needs your
decision" block at the top.

**Done:** every selected operation and unpicked proposal has an outcome, with failures and missing
evidence separated from verified results.

## References

- [Presets](https://docs.unity3d.com/Manual/Presets.html)
- [Preset Manager settings](https://docs.unity3d.com/Manual/class-PresetManager.html)
- [Preset API](https://docs.unity3d.com/ScriptReference/Presets.Preset.html)
- [Texture formats](https://docs.unity3d.com/Manual/texture-formats-reference.html)
- [Audio clip import settings](https://docs.unity3d.com/Manual/class-AudioClip.html)
