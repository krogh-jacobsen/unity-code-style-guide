# Unity persistence audit

Load when reviewing saved game state, in-game settings persistence, save migrations, or load
reconstruction. Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Use the
project's existing save format and tooling; this guide checks data safety without prescribing a
persistence framework. "Settings" here means the player's in-game options, not Unity Player Settings
(`ProjectSettings`). **Last verified: October 2026.**

## Establish the contract

Identify the snapshot owner, storage location, format/schema version, stable content/entity IDs,
and supported prior versions. Trace capture, write, read, validate, migrate, and reconstruction through
the real save/load entry points. Distinguish a disk save from in-memory state and configuration assets.
Detection and sampling count first-party runtime code, not Editor tools.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Complete snapshot | Saved fields versus player-visible authoritative state | Any field the load path or player-visible UI reads is missing from the snapshot, or transient UI/cache state is treated as authoritative |
| Stable identity | Entity/content references and reconstruction maps | Runtime instance IDs, list positions, names, or cached hashes silently point at different content later |
| Schema evolution | Version dispatch, prior fixtures, unknown/missing fields | Old data is misread, silently overwritten, or accepted with invalid semantics |
| Write failure | Temporary write, replacement strategy, backup and error handling | Partial I/O can destroy the only good save or report success before durable completion |
| Consistent capture | Concurrent mutations and async snapshot/write requests | Live state can mutate after the first `await` of a snapshot, or two overlapping writes can complete in either order and the older one wins |
| Safe reconstruction | Validation, references, registries, dependency order, events | A failed load partly replaces the live session or reconstructed entities register/apply effects twice |
| Missing content | Removed IDs, absent DLC/mods, corrupt/truncated input | Load crashes or silently assigns unrelated defaults without the agreed recovery behavior |
| Platform lifecycle | Pause/focus/quit policy and storage access, for the project's actual targets | On a target that suspends instead of quitting, the only save trigger is graceful quit. Unity documents that `OnApplicationQuit` may not be called on mobile (iOS suspends instead of quitting) and points suspension handling to `OnApplicationPause` and saving to `OnApplicationFocus`; verify other platforms in the installed version. A desktop-only project may rely on quit or explicit-save paths, so record this row Not applicable per target rather than flagging it |
| Settings | The store holding in-game options (settings file, `PlayerPrefs`, or cloud profile), its read path, and each option's runtime owner | After a fresh start an option value is read from its store but never applied to its runtime owner (a mixer parameter, quality level, or binding), or is shown in the UI without being saved |
| `PlayerPrefs` use | `PlayerPrefs.Set*` call sites and the keys they write | Progress/snapshot data or credentials and tokens are stored in `PlayerPrefs`, or a Web build stores more than 1 MB there |

Use a platform-supported safe replacement strategy; renaming a temporary file is not a universal
cross-platform guarantee of atomic or durable writes. Retain the prior good save until the agreed
write/recovery contract succeeds. Report I/O failures with a useful outcome rather than swallowing them.

ℹ️ Unity describes `PlayerPrefs` as storage for player preferences between sessions. It is stored
without encryption, Unity says not to use it for sensitive data, and Web builds keep up to 1 MB in the
browser's IndexedDB. Other platforms list no size limit, so treat large data there as a design
proposal rather than a defect.

## Validation

Test round-trip **behavior**, not just equal field values: save, rebuild a fresh session, then exercise
one command that depends on the saved state. Include a supported older fixture, missing/invalid data,
removed content, write failure, repeated loads, and overlapping saves when those cases apply. Use
temporary storage; verify a failed write leaves recoverable data and a failed load leaves the agreed
session state.

Read [Testing](UnityTestingInstructions.md) for fixture/result standards and
[Scenes](UnityScenesAndLifecycleInstructions.md) for async and platform lifetime. Serialization field
renames and enum migrations in Unity assets belong in [Editor tooling](UnityEditorToolingInstructions.md).

Technical references: [`PlayerPrefs`](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html),
[`MonoBehaviour.OnApplicationQuit`](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnApplicationQuit.html).
