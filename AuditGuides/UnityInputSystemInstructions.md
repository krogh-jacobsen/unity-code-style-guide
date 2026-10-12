# Unity Input System audit

Load for action/map ownership, UI/gameplay arbitration, one-shot input, device changes, or rebinding.
Apply the [shared evidence standard](README.md#evidence-standard). Inspect existing action assets
through `unity-cli` as needed; retain the project's chosen integration style.

## Establish effective input

Read Active Input Handling, installed package version, update mode, actions/interactions/processors,
PlayerInput/device pairing, and UI input integration. Identify whether an action instance is owned,
shared through an asset/reference, or copied per player. One input asset or one enabled map is not a
universal requirement; the key is intentional ownership and consumption.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Enable ownership | Enable/disable paths and every shared consumer | A required map is disabled, or one consumer disables another's input |
| Callback ownership | Delegate identity, phases, cleanup, registration paths | Re-enable duplicates actions or disabled/destroyed consumers still react |
| Interaction semantics | Button/value/pass-through type and binding interactions | One press triggers twice, a hold/tap completes incorrectly, or cached input sticks |
| Timing | Configured input update mode and render/physics consumption | A one-shot is lost or applied repeatedly, or polling uses the wrong update phase |
| UI/world arbitration | Action modes, focus, picking/capture, input consumers | Menu/text/modal interaction also moves or commands the game world |
| Device scope | PlayerInput copies, control scheme, InputUser pairing | A player's input comes from the wrong device or bypasses pairing through global device access |
| Rebinding | Completion/cancel/error, enable-state restoration, persistence | An operation leaks, triggers gameplay while rebinding, or restores the wrong action state |
| Generated code | Source asset/generation settings and owned wrapper disposal | Code and bindings drift or an owned input instance survives its lifetime |

## Cases worth explicit inspection

- For cached values, handle neutral/canceled state appropriate to the action type, including mode
  changes and device disconnect. A pass-through action's phase behavior differs from a value action.
- Dynamic input updates commonly feed `Update` and latch one-shots for `FixedUpdate`; fixed/manual
  update modes require their own alignment. Do not flag all `ReadValue` in `FixedUpdate` as a bug.
- A stored callback can be detached using the same delegate. Re-creating a lambda in cleanup is not
  the same subscription; follow [Scenes](UnityScenesAndLifecycleInstructions.md) for lifetime ownership.
- Dispose owned generated action instances and rebinding operations. Shared assets need a shared
  owner's policy; a consumer should not blindly dispose or disable them.
- Restore the pre-rebind mode/enable state on all exits rather than always enabling the action.
  Persistence of overrides and settings belongs in [Persistence](UnityPersistenceInstructions.md).
- Do not infer duplicate events merely from two subscribers or PlayerInput plus custom code; verify
  action-instance identity and whether they both execute the same effect.

## Validation

Exercise press/hold/release, disable/re-enable, map changes while held, pause/modal/text entry,
disconnect/reconnect, and rebind success/cancel when applicable. For physics commands, test rendered
frames with zero and multiple physics steps. Verify overrides survive the supported restart path.

Technical reference: [Input System update settings](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/Settings.html).
Use the installed package's settings and behavior when deciding timing findings.
