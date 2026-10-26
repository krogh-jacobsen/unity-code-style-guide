# Unity cameras and cinematics audit

Load for owned camera-follow logic, Cinemachine, Timeline/PlayableDirector or cinematic handoffs.
Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Establish camera/output
owners, target movement clocks, package versions and supported scene entry paths. A plain camera
alone is a weak signal. Render-pass/stack correctness belongs in [Rendering](UnityRenderingInstructions.md).
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Target sampling | Target movement/interpolation, camera/brain update mode and actual frame order | Camera samples the wrong pose and creates visible jitter/latency that violates the intended behavior; no single update mode fits every mover |
| Manual update | Manual brain/update caller relative to target movement | Missing or duplicate update produces an incorrect pose; a documented custom player loop is valid |
| Camera selection | Brain channel masks, priority/activation and split-screen ownership | The wrong camera/player controls an output; highest priority alone does not bypass channel filtering |
| Cinematic wiring | Saved track/scene bindings, supported entry scene and runtime replacements | Required track/target bindings fail in actual playback; preview success alone does not prove player wiring |
| Handoff lifetime | Camera/input authority on completion, skip, interrupt, failure and scene exit | Cinematic exit strands input/camera ownership or restores a stale prior owner; general lifetime rules stay in [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Clock/lens continuity | Pause/time scale, damping, blending, projection, cuts and teleports | A supported transition violates the intended camera/comfort contract or retains stale smoothing; damping values are design choices |

## Interpret with care

Cinemachine recommendations depend on the target's movement and package version. Multiple brains
can be intentional. A camera cut may require different continuity behavior from a smooth follow;
require the project's desired result rather than a universal damping reset. Timeline rows are
behavior/ownership checks, not claims about a particular binding API. Accessibility motion settings
are reviewed in [Localization/accessibility](UnityLocalizationAccessibilityInstructions.md).

## Validation

Use actual gameplay playback: slow/fast render and physics rates, pause, cuts/teleports, cinematic
completion, skip/interrupt and scene unload. Include two outputs where supported. Reopen saved
bindings and run the agreed player path; unavailable live/player checks are Not verified.

Technical references: [Cinemachine Brain](https://docs.unity3d.com/Packages/com.unity.cinemachine@latest/index.html?subfolder=/manual/CinemachineBrain.html)
and [Rigidbody interpolation](https://docs.unity3d.com/ScriptReference/Rigidbody-interpolation.html).
Research inspected Cinemachine 3.1.7; Cinemachine 2 and other systems need their own installed contracts.
