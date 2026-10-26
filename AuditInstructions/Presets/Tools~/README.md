> How it works: use the static validator for resource integrity, replay prompts for agent decisions,
> and the disposable-project procedure below for observed Unity behavior.

# Preset maintenance and pressure tests

| Situation | Tool or document |
|---|---|
| Validate preset identities, partial policies, and scenario structure | `python3 AuditInstructions/Presets/Tools~/validate_presets.py` |
| Review preset decision cases and expected outcomes | [workflow_scenarios.json](workflow_scenarios.json) |
| Generate nine preset prompts with expected outcomes withheld | `python3 AuditInstructions/Presets/Tools~/replay_presets.py --output /absolute/temp/preset-fixtures.json` |
| Grade fresh-agent decisions and record transcripts | [Shared replay protocol](../../Tools/README.md) |
| Run observed import, update, and persistence checks | Disposable-project procedure below |
| Review recorded compatibility evidence | [Validation record](../../../Validation.md#preset-compatibility-evidence) |

The static validator and replay generator read only this topic folder. Focused regressions check
that the nine scenarios retain authorization/evidence boundaries and that generation leaves fixture
results unverified and protects existing outputs. Generated cases stay Not verified until replayed and graded.

## Disposable-project procedure

Run only with explicit authorization for the concrete disposable project, fixtures, configuration
changes, and cleanup. These instructions define validation; they do not claim a tested updater or
universal save API. Discover the installed Editor's command catalog, APIs, matcher, and targeted
Preset Manager save route before executing. Keep working games and their open scenes untouched.

### 1. Capture the environment and baseline

Record Editor/platform, exact preset source revision and file hashes, helper source/commands, and
fixture identities. Use representative source WAV, PNG, and model files; record actual model format,
rig/static role, and source fixture hash rather than treating one ModelImporter fixture as every FBX.
Keep known crash combinations isolated from successful cases and retain fresh logs/crash artifacts.

Create an active preset installation at `Assets/Presets`, a different-GUID reference copy through
Editor APIs, unrelated/default-disabled rules, and unrelated dirty assets and a scene. Record their
GUIDs, order/enabled states, saved bytes, and live dirty flags. Use only disposable copies for these
negative cases. Verify discovery selects the active registered installation without moving anything.

**Done:** source, fixtures, exact target, recovery data, and live/saved baseline are recorded.

### 2. Exercise updates and identity preservation

Prepare old-source, local, and new-source preset versions through Unity; include one local policy
change and one upstream-only change, plus an unknown-baseline case. Check recommendations distinguish
identity from customization, expose included/excluded property changes, and preserve the local policy.

Test the proposed Editor update route on a disposable destination before the approved active copy.
Read the saved/reloaded preset's effective properties and exclusions, metadata, GUID, existing asset
references, and registrations. Updating a registered preset must expose its future-import consequence;
it must leave existing content importers untouched when Apply was not selected. Include a failed or
unavailable route: it must leave the active destination unchanged and report Not verified/incomplete.

**Done:** each update case has comparison, identity/policy/preservation readback, recovery outcome,
and a repeat comparison requiring no further writes for successful updates.

### 3. Check matching and genuinely new imports

Use the target Unity matcher and actual imports, not another language's glob implementation. Include:

| Case | Expected observation |
|---|---|
| Quoted single SFX pattern | Direct and nested SFX paths match |
| Grouped quoted SFX/UI alternatives | Both approved role paths match |
| Parentheses inside one quoted pattern | Does not stand in for the intended alternatives syntax |
| Sibling `SFXExtra`, case variant, vendor path | No selected owned-folder rule matches |
| Generic audio and narrower role rule overlap | Effective included properties follow preserved list order |
| Disabled rule | Remains disabled and does not apply |
| Mixed Ambience content | Long beds, tiny positional calls, and stereo loops receive separately selected policies |

For every distinct selected rule/policy and relevant overlap, import a fixture with no pre-existing
metadata. Use vendor-negative fixtures only in this disposable project. Assert actual included policy
and preserved platform overrides after import. Existing-asset reimport is a separate test. Remove only
created test assets through Editor APIs after readback; retain source fixtures/logs outside Assets.

**Done:** every row and distinct selected rule has observed matching/import results or Not verified;
fixture cleanup preserves unrelated assets and metadata.

### 4. Prove persistence, correction scope, and no-op behavior

Include a test condition where live rules differ from disk (for example an in-memory serialized
configuration change through a supported Editor route without saving). Confirm readback detects it
as incomplete even when an import follows the live rule. Apply the verified targeted persistence
route; separately compare preset GUIDs, filter text, enabled state, and order in memory and on disk.
If a safe unsaved-state injection is unavailable, record that case Not verified; do not edit YAML.

Verify unrelated dirty flags and saved bytes remain unchanged. Reload/reopen the disposable project
when safe and compare configuration again. Correct a filter syntax/save-mechanism failure within the
already approved scope; a proposed additional folder must remain unimplemented without authorization.

After fixture cleanup and Editor saves settle, run configuration twice. Instrument or log setter/save
calls: matching configuration must issue none and preserve saved bytes and rule count/order. Record
mtime, but an external same-byte touch must not alone fail the run. Test successful first import and
successful persisted configuration as separate outcomes.

**Done:** live/disk/reload, correction-scope, no-op, and unrelated-work checks each have an outcome.

### 5. Record evidence

Append results to Validation.md with Editor, preset revision, importer, operation, fixture, result,
and limitations. Keep contradictory observations together; unknown fields stay unknown. Record
static checks, decision replays, and Unity tool runs separately. Preserve failed checks and skipped
or unavailable operations; no generated fixture is a passing behavioral result.

**Done:** every executed case has source-bound evidence and every unexecuted case is Not verified.
