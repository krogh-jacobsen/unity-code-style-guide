# Unity uGUI audit

Load only for existing or explicitly selected Canvas-based UI. In a UI Toolkit project, finding a
Canvas is first a stack/scope question, not authorization to build another UI system. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). `ui-ugui` owns hierarchy/layout work and
`optimize-text-mesh-pro` owns font/atlas implementation.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Input wiring | EventSystem/input module, raycaster, camera, blocking graphics | The supported pointer/navigation path cannot reach the intended control |
| Layout ownership | Anchors, scaler, LayoutGroups, fitters, target sizes | Two owners fight over a dimension or supported resolutions/text clip content |
| Listener/row lifetime | Bind/unbind, pool activation, current item identity | Reuse duplicates actions, retains old item handlers, or acts on removed content |
| Hide behavior | Canvas/CanvasGroup/GameObject state, nested canvases, scripts | Hidden UI still receives input or updates, or shown UI no longer receives input |
| Domain boundary | UI handlers into authoritative commands | UI bypasses rules, repeats business validation, or displays rejected actions as successful |
| Rebuild cost | Dirty sources and measured layout/batch work | Repeated assignments, animation, or forced rebuilds cause material frame cost |
| Drawing cost | Canvas boundaries, materials/atlases, masking, overdraw | An inspected capture ties a bottleneck to batching, geometry, or fill cost |

## Interpret with care

- ℹ️ Nested layout groups, UI Animators, Auto Size, forced layout updates, and GameObject deactivation
  can be valid choices. Confirm behavior and cost before recommending alternatives; a universal ban
  hides the cases that need them.
- ℹ️ Splitting canvases can isolate rebuilds but adds batching boundaries. Measure the relevant workload
  before prescribing counts or one canvas per panel.
- ℹ️ Decorative raycast targets are candidates for removal; a transparent input blocker is intentional.
  Check the actual event path, including nested canvases and the active input module.
- ℹ️ Disabling a Canvas does not disable all child scripts, listeners, or nested UI behavior. Verify
  input and lifetime separately. CanvasGroup alpha is not an interaction policy.
- ℹ️ UI updates should reflect changed state through an existing presentation owner. For large lists,
  verify row reuse and current data identity rather than recommending pooling by item-count threshold.

## Validation

Exercise pointer and navigation input, hide/show, scene transitions, pooled/rebound rows, and target
resolutions. Include long strings where localization is supported. Inspect saved prefab overrides
and camera/input references, then profile any claimed rebuild/draw improvement on the target device.

Use [Input](UnityInputSystemInstructions.md) for action ownership,
[Design](UnityDesignPatternsInstructions.md) for command rules, and
[Performance](UnityPerformanceOptimizationInstructions.md) for measurement standards.
