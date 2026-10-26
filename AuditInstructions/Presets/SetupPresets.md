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

- Do three separate things only when selected, in this order: **install** (copy files),
  **apply** (change existing asset importers), **register** (future-import rules). Install is the
  recommended default.
- Copy shipped bytes and metadata unchanged. Never author, edit, or regenerate a `.preset` or its
  `.meta`, never invent GUIDs, and never delete metadata to force a re-import.
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
explicit yes.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Restate the exact changes for the picked subset (files, settings, values, commands)
   and wait for an explicit yes. Make no change before it, including saving the report. In a
   non-interactive session, or when no answer arrives, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

Here, steps 1 and 2 are the audit and the recommendations; steps 3 to 6 run only for confirmed items.

## 1. Preflight

Read the target's instructions. Identify one Unity project: the user's destination or the current
workspace, containing `Assets` and `ProjectSettings/ProjectVersion.txt`. Record:

- Editor version, whether that Editor is open, and source-control state.
- Target platforms (Build Profiles and the active build target), to apply the desktop rule above.
- Existing contents of `Assets/Settings/Presets/` and any presets already registered under
  Project Settings > Preset Manager.
- Whether the project has a Unity-template `Assets/Settings` folder (reuse it as it stands).
- The source revision you will use. Resolve `main` to a commit when you can and report it.

**Done:** the target, Editor state, existing presets, and source revision are known, and the audit
(stage 1) was reported without writing anything.

## 2. Ask and select

Ask in one batch. Each default is the recommendation for that question; it takes effect only after
stage 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Which operation: install only, apply to existing assets, or register defaults? | Install only |
| Which asset roles do you have: textures (albedo, normal, mask, UI sprite), audio (music, ambience, SFX, UI), static models, animation-only? | Only roles with real content in the project |
| For apply or register: which owned folders? | None; ask for exact folders |
| Which audio policy for each kind of clip? | One policy per clip; ask when unclear |
| Platform texture and audio budgets now? | No; see step 6 |

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

Turn the answers into numbered recommendations (stage 2): one per preset worth installing (only for
roles with real content), one each for applying to existing assets, registering defaults, and platform
budgets (step 6). Give each its finding from the audit, why it matters, risk, and a default. The user
may pick any subset (stage 3), then confirms the exact list (stage 4).

**Done:** the recommendations were shown, the user picked from them, and the selected presets, the
operation, and any exact target folders or assets were confirmed before any file was written.

## 3. Install

Only the presets confirmed in stage 4. Stage first, then check, then copy.

1. **Stage.** Download each selected `.preset` and `.preset.meta` into a temporary folder outside
   the target's `Assets`, plus the license. URL-encode filenames with spaces. Reject HTML or error
   responses, and any pair that is missing a half.
2. **Verify.** Each `.meta` must contain the `guid:` from the table above. Stop on a mismatch.
3. **Preflight destinations.** Each preset installs to `Assets/Settings/Presets/<Role>/<Name>.preset`
   (keep the role subfolder), with its `.meta` beside it. Reject path traversal, symlinked entries,
   and case-only collisions. Check each GUID against existing project assets, including package assets.

   | Destination state | Action |
   |---|---|
   | Absent and the GUID unused | New: install |
   | Same bytes and GUID at the path | Already installed: leave it |
   | Different content or GUID, a half pair, or the GUID elsewhere | Conflict: report both paths and resolve before copying |

4. **Copy.** With the target's Editor closed, create only missing directories and copy the staged
   pairs intact; Unity generates metadata for the new folders. With the Editor open, use an
   approved route that preserves the pairs, or ask the user to close the project's Editor. Install
   no bridge or package, and never overwrite an imported or customized preset.
5. **License.** Place the MIT license in the project's existing third-party notices location outside
   `Assets`, or at `ThirdPartyNotices/UnityCodeStyleGuide-LICENSE.txt`. Reuse an identical notice;
   preserve unrelated ones.
6. **Import and read back.** Import through existing Editor access, or open the project when that is
   safe and in scope. Read each installed asset's bytes and GUID; check the logs for fresh errors.
   A repeat run must plan no copies. With no safe import route, report files copied and import
   **Not verified**, with the next action.

**Done:** every selected pair is installed or already present, the license is placed, a repeat run
does nothing, and import has an observed result or an explicit pending check.

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

Only the rules confirmed in stage 4. Default presets apply when Unity imports an asset or creates a component, and only to new imports;
they do not reconfigure assets that already exist. Configure them in Project Settings >
Preset Manager, or by script with `Preset.GetDefaultListForType` and
`Preset.SetDefaultPresetsForType(PresetType, DefaultPreset[])`.

- Scope every filter to owned folders. A filter matches file names, folders, and extensions, and a
  `glob:` prefix enables case-sensitive glob patterns. Preview what each filter matches first.
- Order matters: entries apply top to bottom and later entries override earlier ones. Read the existing
  list, preserve unrelated rules, reuse a matching registration, and never add duplicates on a rerun.
- **Textures on Unity 6000.7.0b4:** registering texture defaults crashed Unity during first import.
  On that version, import the texture first, then apply the preset explicitly (step 4). Treat any
  other Editor version as unverified until a fresh texture import succeeds there. Audio and model
  defaults passed on that version.
- Verify with a genuinely new asset imported into a filtered folder, then remove the test asset
  through Editor APIs. Install no `AssetPostprocessor` or other enforcer; persistent enforcement is a
  separate project decision.
- If a safe new-import test is unavailable, keep the files and report registration as unvalidated.

**Done:** the selected rules are saved, a new import shows the intended policy, and unrelated rules
are untouched, or the unperformed check is stated.

## 6. Platform budgets (separate selection)

The role presets set data meaning and sampling; they do not choose resolution or compression for a
platform. Platform budgets are texture and audio `Standalone`, `Android`, or `iOS` overrides applied to
owned assets after the presets. The presets preserve those overrides when re-applied. For starting
values, use the budgets in the matching build guide:
[desktop](../BuildSettings/DesktopBuilds.md) or [mobile](../BuildSettings/MobileBuilds.md). Do not
apply budgets from this step unless the user selected and confirmed them.

## 7. Report

| Item | Status | Detail |
|---|---|---|
| Source URL and revision | | |
| Each selected preset | Installed / Already installed / Conflict | Path and GUID |
| License | Placed / Already present | Location |
| Repeat run | Nothing to do / Work found | |
| Unity import | Verified / Not verified | Next action if pending |
| Apply to assets | Applied / Not selected / Not verified | Targets and readback |
| Register defaults | Registered / Not selected / Not verified | Filters, order, new-import result |
| Unpicked recommendations | Proposal | IDs, with the reason each was skipped |

Put conflicts, unanswered choices, unpicked recommendations, and failed checks in a "Needs your
decision" block at the top.

## References

- [Presets](https://docs.unity3d.com/Manual/Presets.html)
- [Preset Manager settings](https://docs.unity3d.com/Manual/class-PresetManager.html)
- [Preset API](https://docs.unity3d.com/ScriptReference/Presets.Preset.html)
- [Texture formats](https://docs.unity3d.com/Manual/texture-formats-reference.html)
- [Audio clip import settings](https://docs.unity3d.com/Manual/class-AudioClip.html)
