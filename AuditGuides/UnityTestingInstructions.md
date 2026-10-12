# Unity testing audit

Load for test quality, behavioral coverage, EditMode/PlayMode selection, or result validation. Apply
[the shared evidence standard](README.md#evidence-standard). Use `tdd` for test-first implementation
and the repository's runner or `unity-cli` for execution; runner commands and CI setup belong there.

## Establish the baseline

Inventory discovered tests, categories, explicit/expensive exclusions, runner configuration, and
existing failures. Follow current test authorization and any required test-runner subagent. Record
the revision, working-tree changes, engine/package versions, invocation/filter, and result artifacts.
Run the agreed suite; an exit code or "runner started" message alone is insufficient evidence.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Real behavior boundary | Public command, production wiring, assertions | Tests exercise a helper while the broken command path bypasses it |
| Independent expectations | Expected values and fixtures | Assertions repeat the implementation's calculation or only assert that nothing threw |
| Failure-sensitive tests | Original bug/rejected operation and asserted consequence | The test would stay green if the relevant behavior were broken |
| High-value cases | Economy, construction/scheduling, state transitions, saves, lifecycle | Important successful, rejected, repeated, or canceled operations lack meaningful coverage |
| Fixture isolation | Objects, scenes, statics, assets, delegates, clocks, randomness | Tests pass alone but leak state or depend on ordering/timing in the suite |
| Unexpected errors | Console/log handling and allowed messages | Broad suppression hides failures or expected errors are never asserted specifically |
| Asynchronous completion | Timeouts, cancellation, polling conditions, cleanup | A hang is unbounded or success is inferred from a fixed sleep |
| Test discovery/build isolation | Effective assembly, runner list, normal player build | Important tests are never discovered or test code reaches a normal player |

## Choose the cheapest meaningful mode

Use EditMode for rules, math, parsers, serialization, and Editor validation when they do not require
a player loop. Use PlayMode for real lifecycle, input integration, scene flow, physics, or runtime UI
wiring. Saved Inspector references and UI command wiring can be valuable integration checks.

`[UnityTest]` supports yielding in EditMode via the Editor update loop as well as PlayMode. EditMode
is not a normal player loop, but some callbacks run there; avoid declaring all lifecycle behavior
absent. Use the installed Test Framework's supported async signatures and yield instructions.

## Fixtures and coverage

- Inject time, randomness, and external I/O where needed; keep production domain behavior real.
  Assert related effects together when they define one invariant, such as no charge on rejection.
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

Assembly interpretation belongs in [Assemblies](UnityAssemblyDefinitionsInstructions.md), save
scenarios in [Persistence](UnityPersistenceInstructions.md), and async ownership in
[Scenes](UnityScenesAndLifecycleInstructions.md).

Technical reference: [EditMode and PlayMode tests](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/edit-mode-vs-play-mode-tests.html).
Check the project's installed package version before changing test assembly or async setup.
