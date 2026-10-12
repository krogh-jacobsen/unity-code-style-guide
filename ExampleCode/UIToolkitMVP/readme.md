# UI Toolkit: state and visual-tree ownership

This counter demonstrates a pure C# model/presenter contract and a MonoBehaviour adapter.
The model survives disabling the view or rebuilding the document tree for the host object's
lifetime. A destroyed host starts a new count; this is not save-game persistence or a UI framework.

## Install and run through Unity CLI

Prerequisites: target Editor/URP/Input System profile selected, UI Toolkit enabled; Test Framework
only when running tests. Copy this folder’s code/assets/tests with metadata to `Assets/Examples/UIToolkitMVP/`; retain
this Markdown outside Assets at `ExampleCode/UIToolkitMVP/readme.md`.
Preview path/GUID conflicts first. The scene and PanelSettings were generated through Unity APIs;
the UXML attaches its USS using a relative reference so copying the folder remains portable.

1. Run `unity status --format json` and discover `unity command --project-path /absolute/project`.
2. Import/refresh through the exposed command or a CLI-driven Editor script. Require no C#/UXML/USS
   import errors. Open `CounterSample.unity` using the exposed scene command or EditorSceneManager.
3. Check UIDocument references the supplied CounterPanelSettings and SampleView.uxml. The scene
   uses runtime UI Toolkit input; select Input System in project settings and verify mouse/keyboard
   behavior in the target Editor. No legacy Canvas/EventSystem installation is needed for this sample.
4. Enter Play through the available CLI command. Each Increment activation increases once. Disable
   only SampleView, enable it again, then disable/enable UIDocument: displayed state must remain current.
5. For a player build, include CounterSample in the target project's build scene list through Editor
   APIs; do not replace an existing list. Build the agreed target through Unity CLI.

Manual fallback: import, open CounterSample in the Editor, check PanelSettings, then press Play.
These actions are selections; installing the folder does not modify the target's build/settings.

## Code and tests

`CounterModel` holds count, `ICounterView` exposes request/render operations, `SamplePresenter`
initially renders then subscribes, and `SampleView` owns bind/unbind. Its per-frame root identity
check handles UIDocument recreation and either enable order without querying elements every frame.
Required elements are validated; initialization and detach failures clean up subscriptions.

Run isolated EditMode and PlayMode tests through `unity test /absolute/project --mode EditMode`
(or `PlayMode`) with a fresh output XML path. EditMode tests cover initial render, exactly-once
increment, idempotent disposal, rebind, and failed render. PlayMode covers view/document re-enable
and stale-button cleanup; this fixture uses Editor AssetDatabase and is explicitly skipped in player
test runs. Test asmdefs isolate optional NUnit dependencies from normal player code.

See [tested compatibility and results](../../Validation.md). Adapt the demonstration to actual
screen ownership; do not turn every trivial view into a model/presenter hierarchy.
