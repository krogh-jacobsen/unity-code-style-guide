# Unity UI Toolkit audit

Load for runtime UXML/USS, data binding, UI lifecycle, input routing, or recycled list items. Apply
[the shared evidence standard](ProjectReview.md#evidence-standard). The `unity:ui` and `unity:ui-uitk`
skills, when available, own layout, styling, custom-element, and binding implementation; without them,
use the project's UI conventions and the official manual. Project naming takes precedence over skill defaults.
**Last verified: October 2026.**

## Establish the live and saved UI

Identify the UIDocument or PanelRenderer (see the [Panel Renderer manual](https://docs.unity3d.com/Manual/ui-systems/panel-renderer-component.html)), PanelSettings, source UXML/USS, controller/presenter, runtime data source,
and domain command. Inspect the current visual tree and computed styles when behavior depends on
layout, picking, focus, or propagation (`unity-cli` tree dump, or a live run). Editor binding
(SerializedObject) and runtime binding (data sources) are different systems.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Tree lifetime | Creation/rebuild, query timing, cached references | After a re-enable or source replacement, a cached `VisualElement` or query result is not in the current tree (live run: reopen and compare the tree dump) |
| Wiring | UXML names/classes, query type/scope, required references | A name/class the code queries is absent from the UXML and from every builder that creates elements or class names at runtime (the grep is a candidate only: read the helper functions and string-built names first), or an unscoped `Q` returns the first match from a repeated template instance |
| Callback lifetime | `RegisterCallback`, manipulators, `schedule` items | A registration made in bind/enable has no matching unregister/pause on rebind or detach; count registrations after two reopen cycles. Delegate-identity rules: [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Command ownership | Click/navigation handler path | A handler changes domain state without going through the domain command. Ownership rule: [Design](UnityDesignPatternsInstructions.md) |
| Runtime binding | Data source, property path, binding mode, converter, update trigger | A `DataBinding` has no data source or path that resolves, or the displayed value differs from the source after a change (live run); a two-way write bypasses the command |
| Recycled rows | make/bind/unbind/destroy paths and item identity | A bind path registers item-specific handlers with no unbind counterpart, or the row acts on an item other than the one it shows after sort/remove/scroll (live run) |
| Picking and focus | `picking-mode`, `focusable`/`tabindex`, propagation (`StopPropagation`), pointer capture, picking dump | A `picking-mode: Position` element covers an interactive one, a hidden or transparent element still receives pointer events or focus, or a handler consumes an event another element needs. World/gameplay arbitration: [Input](UnityInputSystemInstructions.md) |
| Layout/style | UXML/USS import log, computed-style dump, shared tokens, inline overrides | The import log shows a UXML/USS warning or error, a selector matches no element in the tree dump (a static USS-class grep is a candidate only: classes built from strings at runtime would be missed or mis-flagged), or inline `style` writes/attributes defeat a shared token (count them). Layout at the project's stated target resolutions needs a live run |
| Update cost | Queries or rebuilds in per-frame callbacks, binding polling, collection growth | A per-frame callback (`schedule`, `Update`) runs `Q`/`Query` or rebuilds the tree, or a capture ties UI refresh/layout time to polling or rebuilds. Cost standards: [Performance](UnityPerformanceOptimizationInstructions.md) |

## Cases worth explicit inspection

- ⚠️ Cache the UIDocument (or PanelRenderer) component independently from its visual tree. Bind when the tree is ready
  through the project's supported lifecycle, and re-query after recreation. Another component's
  `OnEnable` is not by itself proof that an arbitrarily ordered document is ready.
- ⚠️ A template's repeated names are valid when queries are scoped to the instance. BEM and kebab-case
  are project conventions; enforce them from [the style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md).
- ⚠️ For recycled rows, register item-independent handlers once where practical, keep current bound
  identity explicit, and detach item-specific observers on unbind. Verify sorting/removal/rebinding.
- ⚠️ In Unity's manual the `binding-path` attribute belongs to the SerializedObject (Editor) binding
  system; runtime data binding binds plain C# objects. A `binding-path` is therefore not evidence of a
  runtime `DataBinding`. Inspect the target property, source path, actual data source, and update mode.
  Two-way binding is appropriate only where writing that property respects the domain contract.
- ⚠️ Runtime binding can poll without `INotifyBindablePropertyChanged`. If notifications/versioning
  are used, verify invalidation of derived properties and source replacement. See
  [runtime data sources](https://docs.unity3d.com/Manual/UIE-runtime-binding-define-data-source.html).
- ⚠️ Test pointer, keyboard, and controller paths where supported. A `ClickEvent` callback does not
  fire for a gamepad Submit, while `Button.clicked` is invoked for both; a handler on `ClickEvent`
  alone leaves controller users unable to press the button. Closing a modal should restore focus and
  input ownership; opacity alone does not establish that hidden content cannot interact. See the
  [Input System UI support](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/index.html?subfolder=/manual/UISupport.html) page.
- ⚠️ Use `pickingMode` (UXML attribute `picking-mode`) and public class-list APIs such as
  `EnableInClassList` for state. Verify version-sensitive properties against Unity, not a copied CSS
  ban list. See the [VisualElement UXML attributes](https://docs.unity3d.com/Manual/UIE-uxml-element-VisualElement.html).
- ⚠️ USS supports hexadecimal colours (see [USS data types](https://docs.unity3d.com/Manual/UIE-USS-PropertyTypes.html))
  and custom properties (variables); the [custom properties](https://docs.unity3d.com/Manual/UIE-USS-CustomProperties.html)
  page does not state selector-scoping rules, so verify how a variable resolves in the installed
  version before reporting a scope finding. Inline values are legitimate for some computed geometry
  but override stylesheet rules.
- ⚠️ Runtime binding adapters can keep `UnityEngine.UIElements` dependencies out of domain/Core code.
  Use the existing view/callback abstractions after verifying their contracts in the project.

## Validation

Import without relevant UXML/USS errors or warnings. Reopen/re-enable, update and replace the data
source, scroll/sort/remove items, and invoke real commands through supported inputs. Check modal
blocking/focus, empty/error states, target resolutions, and long/localized strings when applicable.
Verify saved UIDocument or PanelRenderer and PanelSettings wiring survives reopening; a runtime-only repair is incomplete
when the feature must ship configured. Static XML parsing is useful but cannot certify Unity rendering.

Use [Scenes](UnityScenesAndLifecycleInstructions.md) for async/tree lifetime,
[Design](UnityDesignPatternsInstructions.md) for domain ownership, and
[Testing](UnityTestingInstructions.md) for integration evidence.
