# Unity persistence audit

Load when reviewing saved game state, settings persistence, save migrations, or load reconstruction.
Apply the [shared evidence standard](README.md#evidence-standard). Use the project's existing save
format and tooling; this guide checks data safety without prescribing a persistence framework.

## Establish the contract

Identify the snapshot owner, storage location, format/schema version, stable content/entity IDs,
and supported prior versions. Trace capture, write, read, validate, migrate, and reconstruction through
the real save/load entry points. Distinguish a disk save from in-memory state and configuration assets.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Complete snapshot | Saved fields versus player-visible authoritative state | Important progress/state is omitted or transient UI/cache state is treated as authoritative |
| Stable identity | Entity/content references and reconstruction maps | Runtime instance IDs, list positions, names, or cached hashes silently point at different content later |
| Schema evolution | Version dispatch, prior fixtures, unknown/missing fields | Old data is misread, silently overwritten, or accepted with invalid semantics |
| Write failure | Temporary write, replacement strategy, backup and error handling | Partial I/O can destroy the only good save or report success before durable completion |
| Consistent capture | Concurrent mutations and async snapshot/write requests | One snapshot mixes incompatible states or an older write replaces newer progress |
| Safe reconstruction | Validation, references, registries, dependency order, events | A failed load partly replaces the live session or reconstructed entities register/apply effects twice |
| Missing content | Removed IDs, absent DLC/mods, corrupt/truncated input | Load crashes or silently assigns unrelated defaults without the agreed recovery behavior |
| Platform lifecycle | Pause/focus/quit policy and storage access | The only save opportunity is graceful quit on a platform that can terminate without it |
| Settings | Save/apply path and defaults | UI values appear saved but are neither restored nor applied to their runtime owner |

Use a platform-supported safe replacement strategy; renaming a temporary file is not a universal
cross-platform guarantee of atomic or durable writes. Retain the prior good save until the agreed
write/recovery contract succeeds. Report I/O failures with a useful outcome rather than swallowing them.

## Validation

Test round-trip **behavior**, not just equal field values: save, rebuild a fresh session, then exercise
one important command. Include a supported older fixture, missing/invalid data, removed content,
write failure, repeated loads, and overlapping saves when those cases apply. Use temporary storage;
verify a failed write leaves recoverable data and a failed load leaves the agreed session state.

Read [Testing](UnityTestingInstructions.md) for fixture/result standards and
[Scenes](UnityScenesAndLifecycleInstructions.md) for async and platform lifetime. Serialization field
renames and enum migrations in Unity assets belong in [Editor tooling](UnityEditorToolingInstructions.md).
