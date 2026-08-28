# Unity uGUI (Canvas) Best Practices

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Conventions and pitfalls for Canvas-based UI. If your project uses UI Toolkit instead, read
[UnityUIToolkitInstructions.md](UnityUIToolkitInstructions.md) — the two systems share almost no
concepts, and advice from one is usually wrong for the other.

Most uGUI performance problems come from the same place: **something dirtied a Canvas, and Unity had
to rebuild it.** Almost every rule below is a way of rebuilding less often, or rebuilding less.

Table of contents:
- [uGUI or UI Toolkit?](#ugui-or-ui-toolkit)
- [Naming & organization](#naming--organization)
- [Canvas structure](#canvas-structure)
- [The rebuild pipeline](#the-rebuild-pipeline)
- [Performance rules](#performance-rules)
  - [Raycast targets](#raycast-targets)
  - [Layout groups](#layout-groups)
  - [Never animate UI with an Animator](#never-animate-ui-with-an-animator)
  - [Showing and hiding](#showing-and-hiding)
  - [Masking](#masking)
  - [Text](#text)
  - [Lists and pooling](#lists-and-pooling)
  - [Overdraw](#overdraw)
- [Code conventions for UI scripts](#code-conventions-for-ui-scripts)
- [Profiling uGUI](#profiling-ugui)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## uGUI or UI Toolkit?

| Use uGUI when | Use UI Toolkit when |
|---|---|
| UI lives in world space (health bars, diegetic screens) | UI is screen-space HUD or menus |
| You need per-element shaders, materials, or particle effects | You want CSS-like styling and reuse |
| You depend on an asset-store UI package built on Canvas | You're building Editor tooling as well |
| The team already knows RectTransform well | You want layout that scales without manual anchoring |

⚠️ Mixing both in one project is legitimate — world-space uGUI plus a UI Toolkit HUD is a common
split. What's not legitimate is mixing them *for the same screen*. Pick one per screen.

---

## Naming & organization

- ✅ PascalCase for UI GameObject names, matching the [style guide](../UnityStyleGuide.md#naming-files-and-folders):
  `StartButton`, `HealthBar`, `InventoryPanel`.
- ✅ Name by role, not by widget type. `StartButton` beats `Button (1)`; `HealthBarFill` beats `Image`.
- ✅ One prefab per screen or self-contained panel. Screens should be openable in isolation.
- ✅ Group folders by purpose: `Assets/UI/Screens/`, `Assets/UI/Components/`, `Assets/UI/Sprites/`.
- ✅ Give every interactive element a stable name — you will be looking for it in a hierarchy of
  eighty objects at 2am.
- ❌ Don't leave Unity's default names (`Image`, `Text (TMP)`, `Panel`) in a committed prefab.

```
Assets/UI/
├── Screens/
│   ├── MainMenu.prefab
│   ├── PauseMenu.prefab
│   └── InventoryScreen.prefab
├── Components/
│   ├── HealthBar.prefab
│   └── ItemSlot.prefab
└── Sprites/
```

---

## Canvas structure

A Canvas is the unit of batching **and** the unit of rebuilding. That single fact drives the whole
structure.

- ✅ **Split canvases by update frequency, not by visual nesting.** Static chrome on one Canvas,
  periodically-changing elements on another, per-frame elements on a third.
- ✅ A nested Canvas (a "sub-canvas") isolates its children: a dirty child no longer forces the parent
  to rebuild, and vice versa.
- ⚠️ **Don't over-split.** Batching does not cross a Canvas boundary. Every sub-canvas is its own set
  of draw calls. Three well-chosen canvases beat thirty.
- ✅ Keep elements that batch together on the same Canvas: same material, same texture (ideally one
  atlas), same Z.
- ❌ Never put a whole game's UI on one Canvas. Changing one label re-analyses every element on it.
- ✅ Set **Pixel Perfect** off unless you need it — it forces extra layout work.
- ⚠️ World Space canvases need an explicit **Event Camera** assigned, or raycasts silently do nothing.
  This is the single most common "my world-space button doesn't work" cause.

```
HUDCanvas            (Screen Space - Overlay)   ← static frame, never rebuilds
├── Background
├── Borders
│
├── StatsCanvas      (nested Canvas)            ← rebuilds a few times a second
│   ├── HealthBar
│   └── AmmoCounter
│
└── TimerCanvas      (nested Canvas)            ← rebuilds every frame
    └── TimerLabel
```

**Render mode:**

| Mode | Use for | Watch out for |
|---|---|---|
| Screen Space – Overlay | Most HUD and menus | Ignores cameras entirely — no post-processing, no render features |
| Screen Space – Camera | UI that needs post-processing or to sit between scene layers | Needs a camera reference; sensitive to plane distance |
| World Space | Diegetic UI, health bars above units | Needs an Event Camera; scales with distance |

---

## The rebuild pipeline

Understanding these two separate passes explains most uGUI performance advice:

1. **Layout rebuild** — recalculates RectTransform positions and sizes. Triggered by any
   `LayoutGroup`, `ContentSizeFitter`, or a `SetDirty` on a layout element.
2. **Graphic rebuild** — regenerates the vertex mesh and re-batches. Triggered by changing a colour,
   sprite, text, or anything else visual.

Both run in `Canvas.SendWillRenderCanvases` at the end of the frame, **not** at the moment you set
the property. Setting `text` five times in one frame costs one rebuild, not five — but setting it
every frame costs one rebuild every frame.

- ❌ Never call `Canvas.ForceUpdateCanvases()`. It forces the rebuild to happen immediately and
  synchronously, and is almost always covering for an ordering bug elsewhere.
- ✅ If you need a layout value immediately after changing it, call
  `LayoutRebuilder.ForceRebuildLayoutImmediate(rect)` on **that one RectTransform** rather than
  forcing every canvas in the scene.

---

## Performance rules

### Raycast targets

- ✅ **Turn `Raycast Target` off on every non-interactive Graphic.** It's on by default on every
  `Image` and `TextMeshProUGUI` you create.
- ℹ️ Every pointer event walks the list of raycast targets and runs a hit test against each one. A
  screen with 200 decorative images does 200 hit tests per pointer, per frame.
- ✅ This is the cheapest, highest-yield fix in uGUI and nearly every project has it wrong.
- ✅ For an invisible input blocker, don't use a transparent `Image` — it still generates geometry and
  still draws. Use a Graphic that produces no mesh:

```csharp
/// <summary>
/// An invisible, zero-geometry raycast target. Use instead of a transparent Image
/// for full-screen input blockers and drag areas.
/// </summary>
public class NonDrawingGraphic : Graphic
{
    public override void SetMaterialDirty() { }
    public override void SetVerticesDirty() { }

    protected override void OnPopulateMesh(VertexHelper vh)
    {
        vh.Clear();
    }
}
```

### Layout groups

- ⚠️ `HorizontalLayoutGroup`, `VerticalLayoutGroup`, `GridLayoutGroup` and `ContentSizeFitter` are the
  most expensive components in uGUI. Each one adds a layout pass over its children.
- ❌ **Never nest layout groups.** A `ContentSizeFitter` inside a `VerticalLayoutGroup` inside another
  `VerticalLayoutGroup` triggers a cascade of rebuilds — cost grows multiplicatively with depth.
- ✅ Use layout groups for content whose size you genuinely can't know ahead of time (localized text,
  dynamic lists).
- ✅ For layouts that are fixed at design time, **bake the result**: set the anchors and sizes once in
  the Editor and delete the layout group. Anchoring does the same job for free.
- ✅ If a layout only changes when the player does something, disable the group component after the
  first rebuild and re-enable it when the content actually changes.

```csharp
// Static list built once - let the layout group run, then get out of the way
private void Start()
{
    PopulateSlots();
    LayoutRebuilder.ForceRebuildLayoutImmediate(m_contentRect);
    m_layoutGroup.enabled = false;   // No further layout passes
}
```

### Never animate UI with an Animator

- ❌ An `Animator` on a UI element **dirties its graphics every frame it is enabled**, even when every
  animated value is identical to last frame. Animators have no no-op check.
- ✅ Drive UI transitions from code, a tween library, or `Button`'s built-in Color/Sprite transition.
- ✅ If you must use an Animator, disable the component when the animation finishes.
- ⚠️ This applies to Unity's default Button "Animation" transition mode too. Prefer **Color Tint** or
  **Sprite Swap**.

```csharp
// Simple, allocation-free fade that doesn't dirty layout at all
private async Awaitable FadeInAsync(CanvasGroup group, float duration, CancellationToken token)
{
    float elapsed = 0f;

    while (elapsed < duration)
    {
        elapsed += Time.unscaledDeltaTime;
        group.alpha = Mathf.Clamp01(elapsed / duration);
        await Awaitable.NextFrameAsync(token);

        if (this == null) return;
    }

    group.alpha = 1f;
}
```

### Showing and hiding

- ✅ **Disable the `Canvas` component, not the GameObject.** The children stop rendering and stop
  raycasting, but their meshes and batches stay in memory — re-enabling is nearly free.
- ❌ `SetActive(false)` on a canvas subtree destroys the batch. Re-enabling forces a full layout and
  graphic rebuild, which is exactly the hitch you see when opening a menu.
- ✅ `CanvasGroup` with `alpha = 0`, `interactable = false`, `blocksRaycasts = false` is the right tool
  when you want to fade rather than snap. Note alpha 0 still costs a draw unless you also disable the
  Canvas.

| Technique | Stops rendering | Stops raycasts | Keeps batch | Use for |
|---|---|---|---|---|
| Disable `Canvas` component | ✅ | ✅ | ✅ | Screens you reopen often |
| `CanvasGroup.alpha = 0` | ❌ (still drawn) | with `blocksRaycasts=false` | ✅ | Fades |
| `SetActive(false)` | ✅ | ✅ | ❌ rebuild on re-enable | Screens you rarely reopen |

### Masking

- ✅ Prefer **`RectMask2D`** over `Mask`. It clips by rectangle in the shader — no stencil buffer, no
  extra draw calls, and it doesn't break batching the way `Mask` does.
- ⚠️ Use `Mask` only when you genuinely need a non-rectangular mask from a sprite's alpha.
- ⚠️ Every `Mask` costs two extra draw calls (write stencil, clear stencil) *per mask*.

### Text

- ✅ Use **TextMeshPro** (`TextMeshProUGUI`), not the legacy `Text` component.
- ❌ Turn **Auto Size / Best Fit** off. It binary-searches for a font size on every rebuild.
- ⚠️ Assigning `.text` dirties the mesh even if the string is identical. Guard it:

```csharp
private int m_lastScore = -1;

private void UpdateScore(int score)
{
    if (score == m_lastScore) return;   // Skip the rebuild entirely

    m_lastScore = score;
    m_scoreLabel.text = score.ToString();
}
```

- ✅ For counters that change every frame, pre-cache the strings you'll need (`"0"` … `"99"`) so you
  aren't allocating as well as rebuilding.
- ℹ️ For font atlas and fallback configuration, see the `optimize-text-mesh-pro` skill.

### Lists and pooling

- ❌ Never `Instantiate`/`Destroy` list rows as the player scrolls. It allocates, triggers a layout
  rebuild, and causes GC spikes.
- ✅ Pool row prefabs with `UnityEngine.Pool.ObjectPool<T>` — see
  [Object Pooling](UnityDesignPatternsInstructions.md#object-pooling).
- ✅ For long lists, recycle a fixed number of rows and rebind their data as they move offscreen.
  Twenty rows can present ten thousand items.
- ✅ Populate a list while it's hidden, then show it — one rebuild instead of one per row.

### Overdraw

- ⚠️ uGUI draws back-to-front with no depth rejection. Every stacked full-screen panel is a full
  screen of transparent fill, and fill rate is what kills mobile.
- ✅ When a full-screen menu covers the HUD, disable the HUD Canvas rather than leaving it behind.
- ✅ Use the **Overdraw** draw mode in the Scene view to find the hot spots.
- ✅ Avoid large, mostly-transparent images. Nine-slice a small sprite instead.

---

## Code conventions for UI scripts

These follow the same rules as the rest of the codebase — see the
[style guide](../UnityStyleGuide.md) — with a few uGUI specifics:

- ✅ Cache component references in `Awake()`. Never `GetComponentInChildren` per frame.
- ✅ Subscribe to `Button.onClick` in `OnEnable`, unsubscribe in `OnDisable`. `onClick` is a
  `UnityEvent`, so a listener added in `Awake` and never removed will fire on a pooled, reused row.
- ✅ Use `RemoveListener` with a method group, not a lambda — you can't remove a lambda.
- ✅ Keep UI scripts presentational. They read state and render it; they don't own game logic.
- ❌ Don't reach across the hierarchy with `transform.Find("Panel/Row/Label")`. Serialize the
  reference.

```csharp
[RequireComponent(typeof(Button))]
public class ItemSlotView : MonoBehaviour
{
    [SerializeField] private Image m_icon;
    [SerializeField] private TextMeshProUGUI m_countLabel;

    private Button m_button;
    private ItemDataSO m_item;

    public event Action<ItemDataSO> Clicked;

    private void Awake()
    {
        m_button = GetComponent<Button>();
    }

    private void OnEnable()
    {
        m_button.onClick.AddListener(HandleClicked);
    }

    private void OnDisable()
    {
        // Essential for pooled rows - otherwise listeners stack up on reuse
        m_button.onClick.RemoveListener(HandleClicked);
    }

    public void Bind(ItemDataSO item, int count)
    {
        m_item = item;
        m_icon.sprite = item.Icon;
        m_countLabel.text = count.ToString();
    }

    private void HandleClicked()
    {
        Clicked?.Invoke(m_item);
    }
}
```

---

## Profiling uGUI

Open the Profiler and look for these markers under **PlayerLoop → PostLateUpdate**:

| Marker | Means | Usual cause |
|---|---|---|
| `Canvas.SendWillRenderCanvases` | Something dirtied a canvas this frame | Text set every frame, Animator on UI |
| `CanvasUpdateRegistry.PerformUpdate` | Layout and graphic rebuild pass | Layout groups, ContentSizeFitter |
| `Canvas.BuildBatch` | Re-batching geometry | Too much on one Canvas |
| `Graphic.Rebuild` | A specific graphic regenerated its mesh | `.text` or `.sprite` assignment |
| `IndexedSet.Sort` / `Canvas.SortDrawTrees` | Sorting draw order | Many canvases, or changing sibling order |

- ✅ The **UI** and **UI Details** Profiler modules show which canvases rebuilt and why — check the
  batch count and the "rebuild reason" column before you start optimizing blind.
- ✅ Profile on the target device. Canvas rebuild cost is CPU-bound and scales with device, and fill
  rate problems only show up on real mobile hardware.
- ℹ️ See [UnityPerformanceOptimizationInstructions.md](UnityPerformanceOptimizationInstructions.md#profiling-markers)
  for the general profiling workflow.

---

## Troubleshooting

**Button does nothing when clicked.**
Work down in order: is there an `EventSystem` in the scene at all; does the Canvas have a
`GraphicRaycaster`; is the Button's `Raycast Target` on; is something invisible on top of it (a
full-screen panel with `Raycast Target` left on is the usual culprit); is the Button `interactable`.

```csharp
// Diagnostic: what is actually under the pointer?
private void LogRaycastsUnderPointer()
{
    var data = new PointerEventData(EventSystem.current) { position = Input.mousePosition };
    var results = new List<RaycastResult>();
    EventSystem.current.RaycastAll(data, results);

    Debug.Log($"{results.Count} raycast target(s) under pointer, front to back:");
    foreach (RaycastResult r in results)
    {
        Debug.Log($"  {r.gameObject.name}   (sortingOrder {r.sortingOrder})");
    }
}
```

**World-space UI ignores clicks entirely.**
The Canvas has no **Event Camera** assigned. Screen-space canvases find one automatically; world
space does not, and the failure is silent.

**Layout collapses to zero size, or elements pile on top of each other.**
A `ContentSizeFitter` inside a `LayoutGroup` that is itself size-driven — each is waiting for the
other. Give one of them a fixed dimension.

**Opening a screen causes a visible hitch.**
`SetActive(true)` on a canvas subtree forces a full layout and graphic rebuild. Disable the `Canvas`
component instead — see [Showing and hiding](#showing-and-hiding).

**UI flickers or elements draw in the wrong order.**
Elements on one Canvas with different Z values, or sibling order changing at runtime. uGUI draws in
hierarchy order; Z fighting breaks batching and ordering both.

**Text is blurry in world space.**
Canvas `Dynamic Pixels Per Unit` is too low for the scale, or the RectTransform is scaled rather than
sized. Set the rect to the size you want and leave scale at 1.

**Profiler shows constant `Canvas.SendWillRenderCanvases` with nothing visibly changing.**
Something dirties the canvas every frame: an `Animator` on a UI element, or `.text` assigned
unconditionally in `Update`.
---

## Review checklist

When reviewing uGUI work, check these in order — roughly highest impact first:

| Check | Look for |
|---|---|
| Raycast targets | `Raycast Target` ticked on decorative images and labels |
| Canvas count | One giant Canvas, or thirty tiny ones |
| Layout groups | Nested groups, `ContentSizeFitter` inside a layout group |
| Animators | Any `Animator` component on a UI GameObject |
| Show/hide | `SetActive` used where disabling the Canvas would do |
| Masks | `Mask` used where `RectMask2D` would do |
| Text | Auto Size enabled; `.text` assigned unconditionally each frame |
| Lists | `Instantiate` per row, no pooling |
| World space | Missing Event Camera |
| Code | `GetComponent` in `Update`; `onClick` subscribed without a matching removal |

---

## Learn more

- [Unity UI (uGUI) package documentation](https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/index.html)
- [Unity UI optimization tips](https://unity.com/how-to/unity-ui-optimization-tips)
- [Split canvas for dynamic objects](https://support.unity.com/hc/en-us/articles/115000355466-Split-canvas-for-dynamic-objects)
