> How it works: give the URL of [SetupPresets.md](SetupPresets.md) to your agent and it will audit
> your project, recommend presets, and install only the ones you pick and confirm. It applies or
> registers them only if you ask.

# Import presets

Unity [Presets](https://docs.unity.com/en-us/engine/6000.7/manual/assets-and-media/presets/default)
store importer settings so every texture, sound, or model of a given kind imports the same way.
This folder ships 13 small, partial presets and an agent guide that installs them safely.

> **Intended target: desktop PC and Mac games.** These presets assume Windows and macOS standalone
> players on mid-range hardware, where memory and decoding cost are modest. They have not been
> reviewed for mobile, Web, console, or VR. Texture role presets (color space, sampling) are
> platform-neutral, but the audio load types and the model read/write setting assume desktop
> budgets. For a mobile project, review those before applying.

| I want to… | Give your agent |
|---|---|
| Install presets, optionally apply or register them | [SetupPresets.md](SetupPresets.md) |

Example prompts:

- *"Install the import presets I need from this document into my Unity project."* The agent asks which
  asset roles you have and installs only those.
- *"Install the texture presets and apply them to `Assets/MyGame/Art`."*
- *"Install the audio presets and register them as defaults for my owned audio folders."*

## What happens when you hand it over

1. **Audit.** The agent reads your project: Editor, platforms, existing presets, Preset Manager rules.
2. **Recommendations.** You get a numbered list: which presets fit the asset roles you have, and
   whether to apply or register them, each with the reason, the risk, and a default.
3. **You pick.** Any subset, "all recommended", or none. Take one preset and leave the rest.
4. **You confirm.** The agent restates the exact files and targets and waits for an explicit yes.
5. **It applies and verifies.** Only the confirmed items run, and the report lists what you skipped.

## Three separate steps

Presets involve three different actions, and the agent does only the ones you choose:

| Step | What happens | Risk |
|---|---|---|
| **Install** (default) | Copies the preset files into `Assets/Settings/Presets/`. No existing asset changes. | Lowest |
| **Apply** | Applies a preset to assets you name. Their importer settings change. | Changes real assets |
| **Register** | Adds a Preset Manager rule so future imports in chosen folders use a preset. | Affects every new import |

Installing is not applying: a preset file sitting in your project changes nothing until you apply
or register it.

## What is included

| Role | Presets | Policy in one line |
|---|---|---|
| Textures | Albedo, Normal, Mask, UI Sprite | Correct color space and sampling per role; CPU read off |
| Audio | Music, Ambience, SFX, UI, UI Short, Spatial SFX, Layered Ambience | Streaming for long clips; decompress or compress in memory for short ones |
| Models | FBX Model | Static meshes: no generated colliders, read/write off |
| Animations | FBX Animation | Animation-only sources that keep an existing rig |

Each preset is **partial**. It sets only the properties it names and leaves everything else alone:
slices, borders, pivots, material mappings, rigs, clips, bundle labels, and platform overrides all
survive. That is what makes applying them to a project with existing content safe.

## Key decisions

**Pick one audio policy per clip.** The audio presets are alternatives, not layers.

- UI Short for tiny clicks where compression artifacts matter and PCM size is acceptable.
- Spatial SFX for noisy, frequently overlapping positional effects. It forces mono, so keep stereo
  for authored beds and music.
- Layered Ambience for short loops that would otherwise open many streams. Use Ambience for long beds.
- Streaming has overhead per clip (roughly 200 KB), so compare Audio Profiler memory and CPU under
  realistic concurrency before streaming many short clips.

**A UI sprite still needs a mode.** The UI preset keeps whatever sprite mode you configured. A fresh
texture needs an explicit choice between Single (one icon) and Multiple (a sheet you slice).

**Presets set meaning, not budgets.** They choose color space and sampling per role. Resolution and
compression per platform are separate settings, and the build guides carry the starting values:
[desktop](../BuildSettings/DesktopBuilds.md) or [mobile](../BuildSettings/MobileBuilds.md). Presets
preserve those platform overrides when applied.

**Defaults only affect new imports.** Registering a preset in Preset Manager never reconfigures an
asset that already exists. Apply it to existing assets as a separate step.

**Keep it to your own assets.** Presets are for content you own. Don't apply them to vendor assets
or to textures you have already tuned for a platform.

## Where the defaults need your judgment

The values were checked against Unity's documentation in October 2026. They suit an average
desktop game, with these limits:

- **Meshes used by a Mesh Collider.** The FBX Model preset turns Read/Write off to save memory.
  Unity's docs say a mesh used by a Mesh Collider, a Particle System shape, or a Terrain detail
  mesh must have Read/Write enabled, or the Player build can fail. Skip the preset for those
  meshes, or turn Read/Write back on after applying.
- **Short sounds only for Decompress On Load.** Unity warns that decompressing Vorbis takes about
  ten times the memory of keeping it compressed (about 3.5 times for ADPCM). SFX and UI are for
  clips of a second or two. For longer or numerous effects, use Spatial SFX (ADPCM) or Layered
  Ambience (compressed in memory).
- **Streaming is not free.** Each streamed clip carries roughly 200 KB of overhead. Use it for long
  music and beds, not dozens of short loops.
- **Compressed in memory costs CPU.** Layered Ambience trades memory for decode work on every
  playing voice. Check Audio Profiler CPU with your real layer count.
- **Vorbis quality 0.7 is a starting point.** Listen to your own clips. Sample rate is left as you
  authored it.
- **Textures use bilinear filtering and leave anisotropic filtering alone.** For oblique ground and
  walls, enable Anisotropic Filtering in Quality Settings and raise the level on those textures.
  Alpha-cutout textures such as foliage also need mip preserve-coverage turned on, which the Albedo
  preset leaves untouched.
- **Not for pixel art.** The sprite preset uses bilinear filtering; pixel art needs point filtering.
- **No sizes or compression.** Resolution and compression per platform are separate; see the build guides.

## Things to know

- **Texture defaults on Unity 6000.7.0b4.** Registering texture presets as defaults crashed that
  beta during first import. The guide installs and applies explicitly instead. Audio and model
  defaults worked. Re-test on your own Editor version before relying on texture defaults.
- **Where files go.** `Assets/Settings/Presets/<Role>/`. `Assets/Settings` is often already there
  from your Unity template; the agent reuses it.
- **No enforcement.** Nothing here re-applies a preset when someone changes an importer. Persistent
  enforcement (an `AssetPostprocessor`) is a project decision, not part of the starter.
- **Never delete `.meta` files to reapply defaults.** That changes an asset's GUID and breaks
  references. The agent applies presets through Unity's API instead.
- **License.** The presets are MIT licensed. The agent places a copy of the license in your
  third-party notices.

## What the agent reports

Each preset is Installed, Already installed, or in Conflict, with its GUID. Unity import, applying to
assets, and registering defaults are reported separately, and any check it couldn't run is marked
*Not verified*.
