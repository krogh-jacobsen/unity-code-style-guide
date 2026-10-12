# Scoped import presets

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
| Models/FBXModelImporter.preset | Static meshes with external materials | No animation, no generated colliders, read/write off; material creation disabled |
| Animations/FBXAnimationImporter.preset | Animation-only source with an existing rig | Import animation; preserve rig, clips, avatar, geometry, material and scale choices |

The UI preset preserves configured single/multiple mode, slicing, borders, pivots, outlines, physics shapes,
and sprite identities. Model policies preserve remapped materials, rig/avatar configuration,
clip ranges, and scale. All policies preserve user data, bundle labels, external mappings, and
unrelated platform overrides. Texture resolution/compression budgets and audio channel/sample-rate
choices are project decisions. The animation policy is not a character-import preset.

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
[validation record](../../Validation.md) for the tested Editor, fixtures, and limitations.
For platform tuning, use matching asset/audio skills and official target-version documentation.
