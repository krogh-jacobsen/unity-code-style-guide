# Unity testing audit

Load for test quality, behavioral coverage, EditMode/PlayMode selection, or result validation. Apply
[the shared evidence standard](ProjectReview.md#evidence-standard). **Last verified: October 2026.**

Run tests with the repository's runner or `unity-cli` (the `unity:unity-cli` plugin skill); runner
commands live there, not here. Without either, use the Editor's Test Runner window. CI setup lives in
the [CI guide](../ContinuousIntegration/SetupCI.md). Use a test-first workflow skill only when one is
available; this guide checks the tests that exist.

## Establish the baseline

Inventory discovered tests, categories, explicit/expensive exclusions, runner configuration, and
existing failures. Follow current test authorization and any required test-runner subagent. Record
the revision, working-tree changes, engine/package versions, invocation/filter, and result artifacts.
Run the agreed suite; an exit code or "runner started" message alone is insufficient evidence.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Real behavior boundary | Public command, production wiring, assertions | Tests exercise a helper while the broken command path bypasses it |
| Independent expectations | Expected values and fixtures | An assertion's expected value is computed by the production function under test, or a test body contains no assertion (`Assert.*`, `Is.*`, `LogAssert.*`) and calls no helper that throws on failure |
| Failure-sensitive tests | Original bug/rejected operation and asserted consequence | Reverting or breaking the behavior under test leaves the test green. A test with no `Assert` text may assert through a helper: read the helper and confirm it throws on failure before reporting a missing assertion |
| High-value cases | Public commands, state transitions, saves, and lifecycle paths in the reviewed scope | An important supported scenario or prior regression has no failure-sensitive coverage; propose the smallest useful success/rejection/repeat cases where those semantics apply, rather than requiring three tests for every public method |
| Fixture isolation | Objects, scenes, statics, assets, delegates, clocks, randomness | The result changes when the suspect tests run alone, in reverse order, or shuffled (state leaks); list the tests explicitly when the runner has no ordering option |
| Unexpected errors | Console/log handling and allowed messages | Broad suppression hides failures or expected errors are never asserted specifically |
| Asynchronous completion | Timeouts, cancellation, polling conditions, cleanup | A hang is unbounded or success is inferred from a fixed sleep |
| Test discovery | Source inventory of `[Test]`/`[UnityTest]` methods versus the runner's discovered list | A test method in scope is absent from the runner list. Inclusion in a normal player build is owned by [Assemblies](UnityAssemblyDefinitionsInstructions.md); apply its test-inclusion check rather than repeating it here |

## Choose the cheapest meaningful mode

Use EditMode for rules, math, parsers, serialization, and Editor validation when they do not require
a player loop. Use PlayMode for real lifecycle, input integration, scene flow, physics, or runtime UI
wiring. Saved Inspector references and UI command wiring can be valuable integration checks.

EditMode `[UnityTest]` methods advance through `EditorApplication.update`; they can yield `null`
to advance an Editor frame and supported Editor instructions. They do not provide the full PlayMode
coroutine environment. Use `[Test]` for synchronous checks and `[UnityTest]` when yielding is needed.
PlayMode `[UnityTest]` runs as a coroutine. Check the installed Test Framework for supported async
signatures and yield instructions; see the [UnityTest API](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityTestAttribute.html).

## Fixtures and coverage

- Inject time, randomness, and external I/O where needed; keep production domain behavior real.
  Assert related effects together when they define one invariant, such as no state change on rejection.
- Clean up even when an assertion fails. Restore changed global settings, detach delegates, destroy
  test-created objects/runtime assets, and dispose handles/token sources using the runner's mode.
- Test temporary save fixtures without touching real player data. For relevant failures, test
  cancellation, re-enable, pool reuse, stale request completion, and a second Play session.
- Report behavioral coverage by important scenario. Passing test count and code coverage percentages
  do not prove saved scene wiring, migration safety, or player experience.
- Recommend a focused set that catches expensive failures. Avoid tests of getters or reversible
  cosmetic edits solely to increase counts. Prefer existing seams before proposing new infrastructure.

## Validation and handoff

Read fresh result XML/logs and report passed, failed, skipped, excluded, undiscovered, and not-run work
with reasons. Preserve known failures as failures. A regression test should fail on the original
behavior when practical, then pass after the fix. Re-run affected integration paths; expand the suite
only when required by project rules or remaining risk.

⚠️ Licence-free CI checks (Tier A in [SetupCI.md](../ContinuousIntegration/SetupCI.md)) inspect project
files and style; they run no Unity tests. A green Tier A result is not test evidence.

Assembly interpretation belongs in [Assemblies](UnityAssemblyDefinitionsInstructions.md), save
scenarios in [Persistence](UnityPersistenceInstructions.md), and async ownership in
[Scenes](UnityScenesAndLifecycleInstructions.md).

Technical reference: [EditMode and PlayMode tests](https://docs.unity.com/en-us/engine/6000.7/manual/programming-environment/test-framework-introduction/getting-started/edit-mode-vs-play-mode-tests)
Check the project's installed Editor and Test Framework versions before changing test assembly or
async setup.
