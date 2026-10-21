# Unity UI Toolkit audit

Load for runtime UXML/USS, data binding, UI lifecycle, input routing, or recycled list items. Apply
[the shared evidence standard](ProjectReview.md#evidence-standard). `ui` / `ui-uitk` own layout, styling,
custom-element, and binding implementation. Project naming takes precedence over skill defaults.

## Establish the live and saved UI

Identify the UIDocument, PanelSettings, source UXML/USS, controller/presenter, runtime data source,
and domain command. Inspect the current visual tree and computed styles when behavior depends on
layout, picking, focus, or propagation. Editor binding and runtime binding are different systems.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Tree lifetime | Creation/rebuild, query timing, cached references | Re-enable or source replacement leaves queries/callbacks bound to an obsolete tree |
| Wiring | UXML names/classes, query type/scope, required references | A required element is absent/wrong or a first-match query selects the wrong template instance |
| Callback lifetime | Delegate identity, register/unregister, manipulators, schedules | Reopen/rebind duplicates callbacks or detached/disabled UI keeps reacting |
| Command ownership | Click/navigation path into the domain | UI duplicates business validation, bypasses the command, or publishes success on rejection |
| Runtime binding | Source, property bag/path, mode, converter, update trigger | The displayed value is stale/wrong or a write bypasses domain validation |
| Recycled rows | make/bind/unbind/destroy paths and item identity | A recycled row acts on its old item, leaks subscriptions, or accumulates listeners |
| Input arbitration | Picking, propagation, focus, pointer capture, action modes | One gesture triggers both UI and world actions or a hidden element captures input |
| Layout/style | Import warnings, computed values, shared tokens, inline overrides | A supported target layout fails, a rule never applies, or a local override defeats theming |
| Update cost | Queries, rebuilds, binding work, collection growth | Measured refresh/layout cost or project hot-path violations have an inspected cause |

## Cases worth explicit inspection

- ⚠️ Cache the UIDocument component independently from its visual tree. Bind when the tree is ready
  through the project's supported lifecycle, and re-query after recreation. Another component's
  `OnEnable` is not by itself proof that an arbitrarily ordered document is ready.
- ⚠️ A template's repeated names are valid when queries are scoped to the instance. BEM and kebab-case
  are project conventions; enforce them from [the style guide](../CodeStyleGuide/UnityStyleGuide.md).
- ⚠️ For recycled rows, register item-independent handlers once where practical, keep current bound
  identity explicit, and detach item-specific observers on unbind. Verify sorting/removal/rebinding.
- ⚠️ `binding-path` used for Editor serialization is not sufficient evidence of a runtime DataBinding.
  Inspect its target property, source path, actual data source, and update mode. Two-way binding is
  appropriate only where writing that property respects the domain contract.
- ⚠️ Runtime binding can poll without `INotifyBindablePropertyChanged`. If notifications/versioning
  are used, verify invalidation of derived properties and source replacement. See
  [runtime data sources](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-runtime-binding-define-data-source.html).
- ⚠️ Test pointer, keyboard, and controller paths where supported. Closing a modal should restore
  focus and input ownership; opacity alone does not establish that hidden content cannot interact.
- ⚠️ Use `pickingMode` or the supported UXML attribute for picking, and public class-list APIs such as
  `EnableInClassList` for state. Verify version-sensitive properties against Unity, not a copied CSS ban list.
- ⚠️ USS supports hexadecimal colours, and custom properties can be scoped to selectors. Inline
  values are legitimate for some computed geometry but override stylesheet rules. See
  [USS data types](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-PropertyTypes.html) and
  [custom properties](https://docs.unity3d.com/6000.0/Documentation/Manual/UIE-USS-CustomProperties.html).
- ⚠️ Runtime binding adapters can keep `UnityEngine.UIElements` dependencies out of domain/Core code.
  Use the existing view/callback abstractions after verifying their contracts in the project.

## Validation

Import without relevant UXML/USS errors or warnings. Reopen/re-enable, update and replace the data
source, scroll/sort/remove items, and invoke real commands through supported inputs. Check modal
blocking/focus, empty/error states, target resolutions, and long/localized strings when applicable.
Verify saved UIDocument/PanelSettings wiring survives reopening; a runtime-only repair is incomplete
when the feature must ship configured. Static XML parsing is useful but cannot certify Unity rendering.

Use [Scenes](UnityScenesAndLifecycleInstructions.md) for async/tree lifetime,
[Design](UnityDesignPatternsInstructions.md) for domain ownership, and
[Testing](UnityTestingInstructions.md) for integration evidence.
