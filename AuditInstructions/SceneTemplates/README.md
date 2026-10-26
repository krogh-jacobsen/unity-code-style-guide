> How it works: give the URL of [SetupSceneTemplates.md](SetupSceneTemplates.md) to your agent and it
> will audit your project, recommend scenes, and, once you confirm your picks, copy them into your
> project, check Unity can create scenes from them, and report what it verified.

# Scene templates

Scene templates are starting scenes in **File > New Scene**. These three are for a strategy or
top-down game and are meant to be used as configured sandboxes, not as a gameplay framework: each one
opens with a working camera, neutral lighting, and sensible scale, so you start building instead of
setting up.

| I want to… | Give your agent |
|---|---|
| Install the strategy scene templates | [SetupSceneTemplates.md](SetupSceneTemplates.md) |

Example prompts:

- *"Install the strategy scene templates in my Unity project from this document."* All three.
- *"Install only the UI Preview scene template."* Needs the Input System package, nothing else.
- *"Install the Sandbox and Asset LookDev templates and check they generate cleanly."*

## What happens when you hand it over

1. **Audit.** The agent reads your project: Editor, render pipeline, Input System setup, and any
   scene template assets already present.
2. **Recommendations.** You get a numbered list: each scene, the destination folder, the
   verification level, and any missing prerequisite, with a reason, risk, and default.
3. **You pick.** Any subset, "all recommended", or none. One scene is a valid choice.
4. **You confirm.** The agent restates the exact files and destination and waits for an explicit yes.
5. **It applies and verifies.** Only the confirmed scenes are installed, and the report lists what
   you skipped.

## What is included

| Template | You start with | Use it to |
|---|---|---|
| **Strategy / Sandbox** | Strategy camera, sun and fill lights, a neutral Volume, a 160 m ground plane with collider, a 2 m person-scale capsule, building and tower primitives | Prototype camera, scale, and placement without a game session |
| **Strategy / UI Preview** | A screen-space UI Toolkit screen with a resource bar, sidebar controls, a scrollable catalogue, a status line, a tooltip sample, and a working modal | Design strategy UI and keyboard focus without an economy or game managers |
| **Strategy / Asset LookDev** | The same camera and lighting, labelled slots for buildings, props and vegetation, plinths, material samples, and a 2 m scale reference | Drop in imported art and compare scale, silhouette, shadows, and materials |

The placeholders are metre-scale primitives, and the labels use Unity's built-in text, so there is no
TextMesh Pro dependency and no third-party art.

## Requirements

- **URP**, installed and assigned as the project's render pipeline. The materials, Volume, and cameras
  are URP assets. Built-in and HDRP are not supported.
- **Input System package**, with *Active Input Handling* set to *Input System Package (New)* or
  *Both*. The runtime assembly references it, so the UI Preview needs it too.
- Unity 6.6 or later. The assets were authored on 6000.7.0b4 (URP 17.7.0, Input System 6.7.0) and
  also pass on 6000.6.2f1 (URP 17.6.0, Input System 1.20.0). Earlier Editors were not tested.

Installing changes no project setting, build scene list, or layer. Rendering quality, HDR output,
and shadow budgets stay your choices.

## The camera

| Input | Behavior |
|---|---|
| WASD / arrow keys | Pan relative to camera yaw |
| Q / E | Rotate around the ground focus |
| Mouse wheel | Zoom, with pan speed scaling at overview distances |
| Shift | Faster movement and zoom |
| Middle-mouse drag | Change yaw; the new yaw stays after release |
| Tab | Switch perspective / fixed-tilt orthographic projection |

The rig is `StrategyCameraRig/PitchPivot/Main Camera`. Key points when you build on it:

- **Each rig owns a private copy of the input actions.** Two rigs never share enabled state, and the
  copy is destroyed with the rig.
- **Hosts own input arbitration.** Call `SetInputBlocked(true)` when a modal or tool owns input, and
  read `IsDragging` to avoid conflicting world gestures. `SetOrthographic(bool)` keeps the ground focus.
- **One active camera and audio listener** per normal scene. With additive loading, your host chooses.
- **Deliberately small.** Free XZ movement, with no terrain bounds, clearance, or minimap navigation.

The UI Preview has no camera controller. Tab moves focus; opening the modal disables the workspace and
focuses **Close**, and Escape or Close returns focus to the button that opened it. The tooltip, slider,
toggle, and text field are appearance samples with local state only.

## What gets copied when you create a scene

This is the main idea to understand. When you create a scene from a template, Unity either **clones**
an asset (your scene gets its own copy) or **references** it (it shares the original):

| Asset | Mode | Why |
|---|---|---|
| Scene-specific Volume Profile | Clone | Tune lighting and post-processing per scene |
| UI PanelSettings, UXML, theme, USS | Clone | Editing one preview must not change another |
| Camera prefab, input actions, scripts | Reference | One maintained implementation per project |
| Shared ground, stone, accent materials | Reference | A common baseline for comparing scenes |
| Preview thumbnails | Template metadata | They describe the shipped starting scene |

Consequences worth knowing:

- Editing the **shared prefab or materials changes every scene** that uses them. Make a separate asset
  before experimenting with something that belongs to one scene.
- Updating a template does **not** update scenes already created from it.
- Always create working scenes through **File > New Scene**; opening the template's `.unity` source
  skips the cloning.

## Why it is built this way

- **Neutral by default.** Tonemapping is off and ambient light is flat, with no lighting bake, NavMesh,
  terrain, or global scene loading. Nothing here fights the architecture you pick later.
- **One small assembly.** Everything runtime lives in `UnityStarter.SceneTemplates`; there is no
  static state, so the scripts need no domain-reload handling.
- **Source files stay out of builds.** Maintenance tools live in [Tools~](Tools~/README.md), which Unity
  ignores, so they never reach `Assets`.

## Pressure-tested, October 2026

A fresh URP project received only these files, at a different path from where they were authored,
once on Unity 6000.7.0b4 and once on 6000.6.2f1. Each run:

- **Six scenes generated** through Unity's scene template service (two per template), saved, reopened,
  and checked for missing references. The import log showed no warnings or errors.
- **8 of 8 automated tests passed:** 6 EditMode (independent cloned assets, shared prefab, input and
  materials, UI referencing its own cloned markup) and 2 PlayMode (camera input, blocking, and
  independent input instances; UI selection, modal focus, and re-enable).

Not tested: other GPUs and Windows, input device feel, an interactive pass through the New Scene
dialog, and Editors older than 6.6. A Map Authoring
template is deferred and not included.

For maintainers, [Tools~/README.md](Tools~/README.md) explains how to reproduce authoring and
validation in disposable projects.
