# Unity uGUI audit

Load only for existing or explicitly selected Canvas-based UI (a Canvas, an EventSystem, or
`UnityEngine.UI` usage found in saved scenes, prefabs, or code). In a UI Toolkit project, finding a
Canvas is first a stack/scope question, not authorization to build another UI system. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). The `unity:ui-ugui` skill, when
available, owns hierarchy/layout work and `unity:optimize-text-mesh-pro` owns font/atlas
implementation; without them, use the project's UI conventions and the official manual.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Input wiring | EventSystem and its input module component, raycasters, camera, blocking graphics | The project uses the Input System package and the EventSystem carries a legacy `StandaloneInputModule` (or no module) instead of `InputSystemUIInputModule`, or a Canvas has no raycaster/camera, and a live click or navigation does not reach the control (confirm with `unity-cli` scene inspection plus a live run) |
| Layout ownership | Anchors, CanvasScaler, LayoutGroups, ContentSizeFitters, LayoutElements | Trace which enabled controllers actually drive each RectTransform property and their axis settings. Report competing writes that cause unstable or incorrect layout (confirm live). LayoutElement supplies sizing information; it is not a second size controller. Stretch anchors and a layout controller can cooperate |
| Listener/row lifetime | Bind/unbind, pool activation, current item identity | A pooled row adds `onClick`/listeners on activate with no removal on deactivate, or acts on an item other than the one it shows (live run: reuse a row twice). Lifetime rules: [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Hide behavior | Canvas/CanvasGroup/GameObject state, nested canvases, scripts | A hidden panel unexpectedly consumes input or performs an action the hide contract forbids, or a shown panel cannot be clicked (confirm live). Background scripts and transparent input blockers may be intentional |
| Domain boundary | UI handler path into authoritative commands | A handler changes domain state without going through the domain command. Ownership rule: [Design](UnityDesignPatternsInstructions.md) |
| Rebuild cost | `Canvas.SendWillRenderCanvases`/`Canvas.BuildBatch` in a capture, per-frame UI writes | A capture shows these markers repeating on frames where a script writes text/transform/layout every frame (live profile). Cost standards: [Performance](UnityPerformanceOptimizationInstructions.md) |
| Drawing cost | Canvas boundaries, materials/atlases, masking, overdraw | A capture or frame debugger ties a draw-call or fill-cost bottleneck to a named canvas, mask, or material; otherwise record Not verified. Cost standards: [Performance](UnityPerformanceOptimizationInstructions.md) |

## Interpret with care

- ℹ️ Nested layout groups, UI Animators, Auto Size, forced layout updates, and GameObject deactivation
  can be valid choices. Confirm behavior and cost before recommending alternatives; a universal ban
  hides the cases that need them.
- ℹ️ Splitting canvases can isolate rebuilds but adds batching boundaries. Measure the relevant workload
  before prescribing counts or one canvas per panel. Unity's guidance is to move frequently changing
  elements into their own canvas and profile after each change; see
  [Optimizing Unity UI](https://learn.unity.com/topics/best-practices/guide-optimizing-unity-ui).
- ℹ️ Decorative raycast targets are candidates for removal; a transparent input blocker is intentional.
  Check the actual event path, including nested canvases and the active input module.
- ℹ️ Unity's Input System manual calls `InputSystemUIInputModule` the equivalent of the older
  `StandaloneInputModule`; whether both can coexist is not stated there, so inspect which module the
  EventSystem actually carries. See [Input System UI support](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/index.html?subfolder=/manual/UISupport.html).
- ℹ️ Disabling a Canvas does not disable all child scripts, listeners, or nested UI behavior. Verify
  input and lifetime separately. CanvasGroup alpha is not an interaction policy.
- ℹ️ UI updates should reflect changed state through an existing presentation owner. For large lists,
  verify row reuse and current data identity rather than recommending pooling by item-count threshold.
- ℹ️ In Unity's auto layout manual a layout group does not control its own size and a Content Size
  Fitter controls its own element's size per axis; use that to decide which component owns an axis. See
  [auto layout](https://docs.unity3d.com/Packages/com.unity.ugui@latest/index.html?subfolder=/manual/UIAutoLayout.html).

## Validation

Exercise pointer and navigation input, hide/show, scene transitions, pooled/rebound rows, and target
resolutions. Include long strings where localization is supported. Inspect saved prefab overrides
and camera/input references, then profile any claimed rebuild/draw improvement on the target device.

Use [Input](UnityInputSystemInstructions.md) for action ownership and UI/world arbitration,
[Design](UnityDesignPatternsInstructions.md) for command rules, and
[Performance](UnityPerformanceOptimizationInstructions.md) for measurement standards.
