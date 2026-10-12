# Script template setup

Select the [default templates](#default-templates) and any justified
[optional templates](#optional-templates). These are starting points: add only the lifecycle methods
and behavior the target project needs. The default set has no project-specific base classes or
optional package dependencies.

## Installation and Unity CLI workflow

Prerequisites: target project imported, root namespace chosen, and selected optional package and
assembly dependencies resolved.

1. Select files from [ScriptTemplates](ScriptTemplates/) and, when needed,
   [OptionalScriptTemplates](OptionalScriptTemplates/) using the tables below. Copy selected
   `.cs.txt` files with matching metadata into `Assets/ScriptTemplates/`, a direct child of Assets.
   Copy individual optional files rather than the optional folder wholesale. Preserve metadata
   when updating existing templates; let Unity import new files and create any missing metadata.
   Keep customization in the project rather than modifying the Editor installation's templates.
2. Restart the target Editor through Unity CLI to refresh its Create menu. Confirm the selected
   menu entries are available.
3. Generate scripts through CLI-driven Editor APIs using
   `ProjectWindowUtil.CreateScriptAssetFromTemplateFile` or the installed Editor's exposed
   equivalent. Discover CLI help and the connected Editor's API/command catalog first; target
   the project explicitly. Generate Editor scripts into Editor-only folders/assemblies and tests
   into isolated test assemblies.
4. Import generated scripts and check compiler errors through Unity CLI. Complete the validation
   below, including each selected template's runtime requirements.

Manual fallback: the Project window Create menu for generation and the Test Runner for tests.

`#SCRIPTNAME#`, `#ROOTNAMESPACEBEGIN#`, and `#ROOTNAMESPACEEND#` are Unity substitutions.
The whitespace before namespace-begin tells Unity how to indent a populated namespace. Empty
namespaces must also generate valid code. Menu filenames use priority, `__` submenu separators,
and default filename; actual built-in override names depend on the installed Editor.

## Default templates

The five templates in [ScriptTemplates](ScriptTemplates/) compile without optional packages or
project-specific contracts. Compilation alone does not configure the UI view's runtime dependencies.

| Priority | Default template | Purpose and requirements |
|---|---|---|
| 1 | MonoBehaviour | Minimal component; add only needed lifecycle methods. |
| 2 | ScriptableObject | Configuration; name generated types with `DataSO`. |
| 3 | Plain class | Pure C# responsibility. |
| 4 | UI Toolkit view | Standalone UIDocument host; assign PanelSettings and UXML to run it. |
| 5 | Interface | Name generated files/types `IYourContract`; avoid a duplicate I prefix. |

## Optional templates

Select individual files from [OptionalScriptTemplates](OptionalScriptTemplates/) after resolving
the prerequisites below. They are opt-in starting points, not complete gameplay systems.

| Priority | Template | Prerequisites and completion |
|---|---|---|
| 6 | Custom Editor | Generate into Editor-only folder/assembly; add CustomEditor for an owned target. It is unregistered until then. Use SerializedProperty for edits. |
| 7 | Editor Window | Editor-only assembly/folder; choose a unique menu path before adoption. |
| 8 | Property Drawer | Editor-only assembly/folder; supply owned data/attribute type, registration, and actual field layout. Unregistered placeholder avoids recursive default drawing. |
| 9 | EditMode test | Test Framework and isolated EditMode asmdef; ignored until real assertions replace placeholder. |
| 10 | PlayMode test | Test Framework and isolated PlayMode asmdef; ignored until runtime fixture, cleanup, and assertions are supplied. |
| 11 | Static event | Explicit session/lifetime choice; reset clears subscribers each Play session. Listeners pair subscriptions with their ownership boundary. |
| 12 | Object pool | Inactive prefab, host-lifetime ownership, selected reset/cleanup policy. Acquire/Release must be paired; host teardown destroys retained and borrowed items. |
| 14 | NetworkBehaviour | Netcode for GameObjects with universal Rpc API (tested 3.1.0); configure NetworkObject and transport separately. Validate request authority before implementation. |

Pool clients return live leases once to their owner rather than independently destroying leased
objects. A retained capacity is not a limit on concurrent leases. The raw pool is intentionally
private so clients cannot bypass tracking.

## Validation

Generate each selected template with both empty and populated root namespaces using Unity's actual
substitutions. Confirm import without compiler errors, the intended assembly placement, and menu
availability after restart. Verify the selected runtime dependencies and ownership/cleanup behavior
listed above. Run completed tests through Unity CLI and inspect fresh results; report ignored
placeholders as unfinished, never successful validation.

See the [validation record](../Validation.md) for generated-script coverage and exact tested versions.

## Retired templates

The former priority-13 state template remains in
[ReferenceOnly](OptionalScriptTemplates/ReferenceOnly/) as a retired sketch outside the selectable
set. It supplies no IState/StateMachine contract. Design that contract for the target project before
introducing a state template; no missing framework is implied by the kit.
