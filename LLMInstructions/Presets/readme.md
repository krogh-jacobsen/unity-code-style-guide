> How it works: give this URL to your agent and it will help configure your Presets


# Scoped import presets

For URL/local-file setup by an agent, start with the [preset workflow](SetupPresets.md). It defaults to
installation only and separates application to existing assets from registration of future-import rules.

Copy selected presets, with their existing `.meta` files, to `Assets/Settings/Presets/`. There is
no bundled installer or import-enforcement script. Presets are optional choices for owned assets.
Do not apply them indiscriminately to vendor assets or already tuned platform variants.

## Inventory

| Asset | Intended use | Included policy |
|---|---|---|
| Textures/AlbedoTextureImporter.preset | Tiling world color | Default texture, sRGB, mipmaps, repeat, bilinear; CPU read disabled |
| Textures/NormalTextureImporter.preset | Tangent-space normal data | Normal map, linear, mipmaps, repeat, bilinear; CPU read disabled |
| Textures/MaskTextureImporter.preset | Packed linear material data | Default texture, linear, mipmaps, repeat, bilinear; CPU read disabled |
| Textures/UISpriteTextureImporter.preset | Screen-space UI sprites | Sprite, sRGB, no mipmaps, clamp, bilinear, alpha transparency; CPU read disabled |
| Audio/MusicAudioImporter.preset | Long music | Streaming, Vorbis, quality 0.7; load in background |
| Audio/AmbienceAudioImporter.preset | Long ambience loops | Streaming, Vorbis, quality 0.7; load in background |
| Audio/SFXAudioImporter.preset | Short frequently played effects | Decompress on load, Vorbis, quality 0.7; preload |
| Audio/UIAudioImporter.preset | Short UI feedback | Decompress on load, Vorbis, quality 0.7; preload |
| Audio/UIShortAudioImporter.preset | Tiny UI clicks where codec artifacts matter | Decompress on load, PCM; preload, foreground load; preserve channel/sample-rate choices |
| Audio/SpatialSFXAudioImporter.preset | Noisy repeated spatial effects: footsteps, impacts, weapons | Compressed in memory, ADPCM, force mono; preload, foreground load |
| Audio/LayeredAmbienceAudioImporter.preset | Short overlapping ambience loops | Compressed in memory, Vorbis, quality 0.7; preload, background load |
| Models/FBXModelImporter.preset | Static meshes with external materials | No animation, no generated colliders, read/write off; material creation disabled |
| Animations/FBXAnimationImporter.preset | Animation-only source with an existing rig | Import animation; preserve rig, clips, avatar, geometry, material and scale choices |

The UI preset preserves configured single/multiple mode, slicing, borders, pivots, outlines, physics shapes,
and sprite identities. Model policies preserve remapped materials, rig/avatar configuration,
clip ranges, and scale. All policies preserve user data, bundle labels, external mappings, and
unrelated platform overrides. The spatial SFX variant deliberately forces mono; the other audio
policies preserve channel choices, and all preserve sample-rate and normalization choices. Texture
resolution/compression budgets are selected separately below. The animation policy is not a character-import preset.

## Mac and Windows texture budgets

Role presets establish data meaning and sampling. Apply a separately selected desktop budget through
TextureImporter platform settings in the target project; the shipped texture presets preserve those
settings on subsequent application. Use a preview of owned asset paths and preserve opt-outs. The
Standalone texture override is shared by desktop targets in this Editor; do not assume independent
Windows/macOS overrides. Split content or select another supported workflow if their budgets diverge.

| Role | Starting budget | Inspect before accepting |
|---|---|---|
| Ordinary world albedo | Maximum 2048; BC7 for quality, BC1 for suitable opaque content | Compare at gameplay distance; reduce small props to 512–1024 |
| Normal maps | Maximum 2048; evaluate BC5 | Check tangent-space shading and the target shader's normal decoding |
| Packed masks | Usually 1024–2048; evaluate BC7 when multiple channels are needed | Preserve required channels; check metallic/smoothness artifacts and shader channel packing |
| Prominent close-up surfaces | Allow 4096 only where a comparison justifies it | Read imported memory size and the representative scene's total residency |
| Screen-space UI | Match maximum displayed size; compare BC7 with RGBA32 | Inspect alpha edges/gradients at high DPI; keep slicing and atlas identities |

These are starting budgets for ordinary desktop hardware, not per-file requirements. Compression
support depends on the minimum GPU/API: BC7 requires the documented desktop support; BC5 stores two
channels and cannot replace an arbitrary multi-channel mask. Keep color textures sRGB and data
textures linear as the role presets specify. A 4096 texture has four times the pixels of a 2048
texture at the same format; inspect total residency rather than choosing resolution by filename.

Keep mipmaps for world surfaces. The supplied UI preset is for screen-space sprites; world-space or
strongly minified UI needs a separate evaluated mipmap policy. Evaluate anisotropic filtering for
oblique surfaces and mip streaming for large worlds only with a measured need and configured budget.
For packed sprites, inspect the SpriteAtlas platform settings and resulting atlas textures as well;
the source importer's budget alone does not establish the packed texture's format or residency.

**Done:** representative Mac and Windows players show acceptable appearance at each quality tier;
readback confirms desktop format/size, preserved authoring values, and memory within the target budget.
See [desktop setup](../BuildSettings/DesktopBuilds.md) for platform acceptance and the
[Unity GPU texture-format reference](https://docs.unity3d.com/6000.7/Documentation/Manual/texture-formats-reference.html)
for support and format costs.

## Choose audio by playback role

Keep the original music, ambience, SFX, and UI policies as general choices. Select one policy per
clip; these variants are alternatives rather than layers to apply in sequence.

- Choose UIShort for tiny clicks when PCM quality is useful and the aggregate build size is acceptable.
- Choose SpatialSFX for noisy, frequently overlapping positional effects. ADPCM kept compressed saves
  residency relative to decoded PCM and trades some quality for inexpensive playback decoding. Preserve
  stereo for authored stereo beds/music; listen to mono downmixes and the preserved normalization setting.
- Choose LayeredAmbience for short loops that would otherwise create many concurrent streams. Use the
  streaming ambience policy for long beds. Streaming has roughly 200 KB overhead per clip; compare
  Audio Profiler memory, DSP CPU, Streaming CPU, and voice counts under representative concurrency.

Decompress On Load expands Vorbis into decoded audio in memory; codec quality mainly changes the
stored size and audible result. Background loading can defer playback until data is ready. Preload or
explicitly load upcoming music/ambience and observe AudioClip.loadState when start timing matters.
Keep sample rate content-driven; do not force all audio to one rate. Existing platform overrides take
precedence over default audio settings and need their own audit on both desktop targets.

**Done:** inspect settings after reimport and listen to initial playback, rapid repeats, overlapping
voices, loop seams, and scene transitions in both players. Record CPU/memory and any overrides. See
[Unity audio import settings](https://docs.unity3d.com/6000.0/Documentation/Manual/class-AudioClip.html).

## Apply through Unity CLI

Prerequisites: Unity CLI, a connected target Editor with Pipeline, and selected assets already
imported. Run `unity status --format json`, then discover commands with
`unity command --project-path /absolute/project --format json`. Use the available C# execution
command to run an Editor method implementing this procedure:

1. Load the preset with `AssetDatabase.LoadAssetAtPath<Preset>()` and get the selected target's
   `AssetImporter`. Check `preset.CanBeAppliedTo(importer)` before changing it.
2. Record GUID, platform overrides, metadata, and relevant designer-authored values. Preview the
   preset's included properties and the selected paths. Do not reset the importer.
3. Call `preset.ApplyTo(importer)`; require success. For a selected UI sprite with no configured
   sprite mode, choose Single (individual icon) or Multiple (sheet, with slicing) explicitly. Preserve
   an existing mode and geometry. Then call `importer.SaveAndReimport()`.
4. Read the importer back after import and compare intended settings and preserved values. Check
   serialized references in a representative scene/prefab and record the saved result.

Use version-matched Editor APIs via a CLI-driven Editor script when no live execution command is
available. The CLI does not have a universal preset subcommand; discover the installed command
catalog instead of inventing one. Manual fallback: select the asset, use the Inspector's preset
selector, apply the chosen partial preset, and reimport/read back.

**Never delete metadata to apply defaults.** GUIDs identify existing assets. Ordinary reimport
does not necessarily reapply default presets; apply an existing asset's selected preset explicitly.
Inspector Reset can reset unrelated values and is not the recommended retrofit procedure.

## Default imports and optional enforcement

**Tested-beta constraint:** Unity 6000.7.0b4 crashed inside PresetManager texture application on
first import. Use explicit application after initial import for textures on that version. The UI
preset deliberately preserves sprite mode; a fresh unconfigured texture also needs a Single/Multiple
selection. Audio/model default imports passed. Revalidate texture defaults on another Editor before
enabling them; copying these presets does not register anything automatically.

On a verified Editor, register selected defaults using Preset Manager or its Editor API through CLI. Scope filters to
owned folders and preview the paths they match. Verify a genuinely new import; defaults do not
retroactively configure existing importers. Record filter/order choices in the target setup result.

Persistent enforcement is a separate project decision. If added, restrict an AssetPostprocessor
to owned paths, define per-asset opt-outs and platform precedence, and avoid recursive reimport.
Test moves, overrides, and reimports before enabling it in CI. No enforcer is shipped here.

## Verification

Apply all selected policies to representative new/existing assets. A sliced sprite must keep its
slices and borders; an FBX with remapped materials must keep its mapping; platform overrides must
survive. Preserve preset GUIDs when updating the kit through Unity. See
[validation record](../../../Validation.md) for the tested Editor, fixtures, and limitations.
For platform tuning, use matching asset/audio skills and official target-version documentation.
