# Unity Input System audit

Load for action/map ownership, UI/gameplay arbitration, one-shot input, device changes, or rebinding.
Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Inspect existing action assets
through `unity-cli` (the `unity:unity-cli` skill, when available) as needed; retain the project's
chosen integration style. This lens owns UI/world arbitration; the UI lenses link here.
**Last verified: October 2026.**

## Establish effective input

Read Active Input Handling, installed package version, update mode, actions/interactions/processors,
PlayerInput/device pairing, and UI input integration. Identify whether an action instance is owned,
shared through an asset/reference, or copied per player. One input asset or one enabled map is not a
universal requirement; the key is intentional ownership and consumption.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Enable ownership | Enable/disable paths and every shared consumer | A required map is disabled, or one consumer disables another's input |
| Callback ownership | Delegate identity, phases, cleanup, registration paths | A `performed +=`/`canceled +=` registration has no matching removal with the same delegate, or a disabled/destroyed consumer still reacts after re-enable (delegate-lifetime rules: [Scenes](UnityScenesAndLifecycleInstructions.md)) |
| Interaction semantics | Action type (Button/Value/PassThrough) against its binding interactions and processors | An interaction is configured on an action whose type the installed package does not apply it to (list each action type against its interactions in the asset, then confirm in the package manual), or cached input is read without handling the canceled/neutral phase |
| Timing | Configured update mode (Dynamic, Fixed, Manual) and where each action is read | The installed package reports an unsupported direct action read for the configured update mode, or the capture/latch/consume path loses or repeats a one-shot (live run: frames with zero and multiple fixed steps). Capturing in Update and consuming a latched value in FixedUpdate is valid when each input is consumed exactly once |
| UI/world arbitration | Action maps/modes, focus, UI input integration, input consumers | A menu, text field, or modal interaction also triggers a gameplay action (live run), or UI integration deviates from the checks below. Element-side picking/focus: [UI Toolkit](UnityUIToolkitInstructions.md) or [uGUI](UnityUGUIInstructions.md) |
| Device scope | PlayerInput copies, control scheme, InputUser pairing | A global device read serves the wrong player/device or violates the documented pairing contract; an intentional global shortcut or diagnostic read is valid |
| Rebinding | Completion/cancel/error, enable-state restoration, persistence | A `RebindingOperation` is not disposed on every exit, gameplay actions fire during rebinding, or the action's pre-rebind enable state is not restored |
| Generated code | Source asset/generation settings and owned wrapper disposal | The generated wrapper differs from the action asset, or an owned wrapper instance has no `Dispose` at its owner's end |

## UI integration checks

These come from Unity's [Input System UI support](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/index.html?subfolder=/manual/UISupport.html)
manual (checked against package version 1.14); confirm against the installed package's manual.

- ⚠️ From Unity 2023.2 UI Toolkit does not need the UI Input Module component. If a module is present,
  its settings take priority over the UI settings in the project-wide actions, so a stale module can
  silently override them.
- ⚠️ To stay compatible with UI Toolkit, keep the UI action map's name, its action names, and its
  action types unchanged. Pointer and tracked-device actions are PassThrough; Submit and Cancel must be
  Button.
- ⚠️ Calling `EventSystem.IsPointerOverGameObject` from an action callback such as `performed`
  produces a warning because UI state reflects the previous frame; poll it in `Update` instead.
- ⚠️ Do not feed one gamepad to both the Virtual Mouse and the UI module's navigation actions: the UI
  receives the input on two channels and triggers twice.
- ⚠️ Nothing automatically stops gameplay from also receiving input the UI consumed. Check for an
  explicit mechanism: split controls, or a mode switch that disables gameplay actions while UI is active.

## Cases worth explicit inspection

- ⚠️ For cached values, handle neutral/canceled state appropriate to the action type, including mode
  changes and device disconnect. A pass-through action's phase behavior differs from a value action.
- ℹ️ Unity's update-mode setting offers Process Events In Dynamic Update, In Fixed Update, or Manually;
  the manual does not say how to read or latch one-shot input between them. Latching a one-shot from
  `Update` for use in `FixedUpdate` is a common project convention, not a documented rule: verify it
  in the installed version and do not flag all `ReadValue` in `FixedUpdate` as a bug.
- ⚠️ A stored callback can be detached using the same delegate. Re-creating a lambda in cleanup is not
  the same subscription; follow [Scenes](UnityScenesAndLifecycleInstructions.md) for lifetime ownership.
- ⚠️ Dispose owned generated action instances and rebinding operations (Unity's manual says to dispose
  each `RebindingOperation` so it does not leak unmanaged memory). Shared assets need a shared owner's
  policy; a consumer should not blindly dispose or disable them.
- ⚠️ Restore the pre-rebind mode/enable state on all exits rather than always enabling the action.
  Persistence of overrides and settings belongs in [Persistence](UnityPersistenceInstructions.md).
- ⚠️ Do not infer duplicate events merely from two subscribers or PlayerInput plus custom code; verify
  action-instance identity and whether they both execute the same effect.

## Validation

Exercise press/hold/release, disable/re-enable, map changes while held, pause/modal/text entry,
disconnect/reconnect, and rebind success/cancel when applicable. For commands applied in the physics
step, follow the timing evidence in [Physics](UnityPhysicsInstructions.md). Verify overrides survive
the supported restart path.

Technical reference: [Input System settings](https://docs.unity3d.com/Packages/com.unity.inputsystem@latest/index.html?subfolder=/manual/Settings.html).
Use the installed package's settings and behavior when deciding timing findings.
