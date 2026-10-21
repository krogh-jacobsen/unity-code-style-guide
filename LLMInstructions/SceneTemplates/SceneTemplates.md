# Strategy scene templates

Install these optional resources when a project needs a strategy-camera sandbox, a UI preview, or an
asset comparison scene. They are configured starting scenes, not a gameplay framework. Map Authoring
is deferred and is not included.

## Prerequisites and installation

1. Confirm the target's exact Editor, URP, Input System, active input handling, and assigned rendering
   pipeline. See [the configuration record](UnityTechStack.md) and [validation](../../Validation.md).
   The initial assets were authored with Unity 6000.7.0b4, URP 17.7.0, and Input System 6.7.0.
   Resolve missing packages through Package Manager Client APIs using the package-management skill.
   These assets use the target's configured URP pipeline; importing them does not change Graphics,
   Quality, build scenes, layers, or Input System project settings.
2. Copy [SceneTemplates](SceneTemplates/) with its matching `.meta` file into the target as
   `Assets/{ProjectName}/SceneTemplates/`. Preserve the complete hierarchy and existing metadata.
   Include the starter's [MIT license](../../LICENSE). Documentation stays outside `Assets`.
   The resources have their own runtime assembly, `UnityStarter.SceneTemplates`, referencing
   `Unity.InputSystem`. Install this identity only once in a project.
3. Import through Unity CLI-driven Editor APIs, then inspect compiler, UXML, USS, and import messages.
   For a smaller selection, keep the root runtime asmdef and `Shared`, and copy only the selected
   template directories. `UIPreview/PreviewScreen.cs` belongs with its UI assets. Keep each selected
   group's metadata; let Unity create metadata for newly introduced parent folders.
4. Choose **File > New Scene**, select a **Strategy /** template, and save the resulting scene into
   the project's normal scene folder. The source `.unity` beside each `.scenetemplate` is its
   authoring source. Create working scenes through the template so dependency cloning is applied.

**Done:** selected templates appear in New Scene, the generated scenes save/reopen with valid
references, and the relevant interaction checks below pass. Importing assets alone does not verify
runtime behavior. Updating a template does not retroactively update scenes already created from it.

## Included scenes

| Template | Starting contents | Intended use |
|---|---|---|
| Strategy / Sandbox | Strategy camera, sun/fill lights, neutral Volume with tonemapping off, 160 m ground plane/collider, 2 m person-scale capsule, building/tower primitives, `World/Experiments` | Prototype camera, scale, placement, and feature behavior without a simulation session |
| Strategy / UI Preview | Screen-space UIDocument, assigned PanelSettings/theme/UXML, resource bar, sidebar controls, scrollable catalogue, status, tooltip appearance sample, working modal | Preview strategy UI and keyboard focus without economy, saving, or game managers |
| Strategy / Asset LookDev | Same camera/lighting conventions, ground, labelled building/prop/vegetation slots, plinths, material samples, 2 m scale reference | Drop in owned/imported assets and compare scale, silhouettes, shadows, and materials |

LookDev's labels use Unity's built-in TextMesh/font, so no TextMesh Pro package or vendor font is
required. Its placeholders are metre-scale primitives, not redistributed Railroad Tycoon art.
The Volume explicitly disables tonemapping for a predictable neutral SDR starting point, and the
scenes use flat ambient fill without a lighting bake. The supplied cameras request post-processing
so later Volume edits can take effect when the target renderer supports them. Rendering quality,
HDR output, and shadow budgets remain target-project choices.

## Camera controls and integration

| Input | Behavior |
|---|---|
| WASD / arrow keys | Pan relative to camera yaw |
| Q / E | Rotate around the ground focus |
| Mouse wheel | Zoom, with movement speed scaling at overview distances |
| Shift | Faster movement and zoom |
| Middle-mouse drag | Change yaw; the new yaw remains after release |
| Tab | Switch perspective / fixed-tilt orthographic projection |

The rig is `StrategyCameraRig/PitchPivot/Main Camera`. Its controller clones the source Input Actions
asset at runtime, enables/disables only its private map, and destroys that instance with the rig.
Two rigs therefore do not share action-map enable state. Use one active camera/listener for a normal
standalone scene. If scenes are loaded additively, the host must choose the active rig and listener.

The compact controller follows Railroad Tycoon's strategy-camera pattern; it is not a copy of the
whole camera system. This initial version has free XZ movement, no terrain bounds/clearance, no
minimap navigation, and no construction or UI dependency. A game host can call `SetInputBlocked(true)`
to stop new input and pending movement when a modal or tool owns input, and inspect `IsDragging` to
avoid conflicting world gestures. It must supply that integration when adding UI to a world scene.
`SetOrthographic(bool)` changes projection while preserving the rig's ground focus.

The UI scene uses Tab for normal focus navigation and contains no strategy camera controller.
Its selection button updates sample status, and opening the modal disables the workspace and moves
focus to Close. Closing it or pressing Escape returns focus to the opener. The tooltip is a static
appearance example; the slider, toggle, and text field have local control state only. Sample data is
not connected to a simulation or persistence system.

## Dependency ownership

| Asset | New-scene behavior | Reason |
|---|---|---|
| Scene-specific Volume Profile and its overrides | Clone | Independent lighting/post-processing tuning |
| UI PanelSettings, UXML, theme, USS | Clone | Editing one preview must not change another |
| Camera prefab, source Input Actions, C# scripts | Reference | One maintained implementation per project |
| Shared ground, stone, accent materials | Reference | Intentional common comparison baseline |
| Preview thumbnails | Template metadata | Represent the shipped starting scene |

Shared-material and prefab edits affect all consumers. Make a separate asset before experimenting
with an appearance that should belong to one scene. Generated UI styles are deliberately independent;
a later project-wide theme can replace those references explicitly. No lighting bake, NavMesh bake,
terrain data, persistent services, or global scene-loading architecture is supplied.

## Validation and maintenance

In a disposable target, create two scenes per selected template. Save and reopen all of them; check
for missing scripts, a single active camera/listener, assigned UI assets, and valid materials. Verify
that editable assets are distinct copies while the camera prefab/input definition remain shared.
Changes to the first scene's cloned assets must leave the second and template source unchanged.

Exercise camera input, input blocking, disable/re-enable, and projection switching. In UI Preview,
check selection, scrolling, Tab navigation, modal focus, Escape, and several window sizes. Build a
normal player with the selected scenes, run it, and inspect logs and rendering. Add real scenes to
build profiles explicitly; installing this kit does not register them as game content.

The [maintenance tools](../../Tools/SceneTemplates/README.md) reproduce authoring and the focused
validation in disposable projects. [Validation.md](../../Validation.md) records exact results and
remaining coverage limits. Assets and metadata are created through Unity, including thumbnails'
import settings; preserve GUIDs when making future changes to the shipped group.
