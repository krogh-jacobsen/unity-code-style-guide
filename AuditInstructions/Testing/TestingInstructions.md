> How it works: give this URL to your agent, for example "Set up tests in my Unity project using
> this document". It audits the current assemblies and tests, recommends a small setup, and applies
> only the changes you select and confirm. Human overview: [readme](README.md).

# Set up Unity tests (agent instructions)

Create discoverable tests for agreed behavior and keep test dependencies out of normal players.
This document is self-contained. **Last verified: October 2026.** Inspect the installed Editor and
Test Framework before choosing assembly configuration or runner options.

## Operating rules

- Read the target's instructions and test permissions. Preserve dirty scenes, existing tests,
  concurrent edits, and the project's assembly decisions.
- During audit, inspect saved files and existing result artifacts only. Starting an Editor, creating
  fixtures, installing a package, running tests, and building are separately listed changes/actions
  in the confirmation. Use an isolated copy when a runner can disturb an active Editor.
- Create imported assets and assemblies through Unity Editor APIs or Test Runner; Unity creates
  metadata. Use available Unity CLI execution with an explicit target project, or the Editor UI.
- Missing tools, framework, build modules, or authorization leave affected checks **Not verified**.

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit user confirmation.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Present the exact changes for the picked subset (files, settings, values, commands)
   and obtain explicit user authorization before making them, including saving the report.
   Confirmation need not contain the literal word "yes": after the concrete scope is presented,
   "implement R1 and R3" can both select and confirm those items. Selection alone ("R1 and R3")
   chooses scope without authorizing implementation. Honor existing authorization for unchanged
   scope without asking again; clarify a delayed reply only when its scope is materially ambiguous.
   Resolve IDs against the presented change list rather than guide defaults. If evidence establishes
   that exact scope was previously presented and authorized but its record is now unavailable,
   retrieve that record before execution; recovered unchanged scope needs no repeat confirmation.
   If concrete changes were never presented, an instruction to implement an ID leaves scope
   unconfirmed: first present the exact changes and obtain confirmation before execution.
   Changed scope needs confirmation for the changed items. In a non-interactive session, or when
   authorization is absent, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

## 1. Preflight

Identify one Unity project and record its exact Editor version, Test Framework source/resolved
version, effective production and test assemblies, tests and existing failures, target platform,
Editor state, and permitted runner. Enumerate the behavior needing coverage and inspect how callers
reach it. Distinguish predefined assemblies, asmdefs, and asmrefs; an Editor folder beneath a runtime
asmdef is not an Editor boundary. A custom test asmdef cannot reference Assembly-CSharp directly.

**Done:** scope, versions, boundaries, existing coverage/results, and unavailable checks are recorded
without writing or launching a test/build.

## 2. Ask and recommend

Use project evidence first; ask remaining material questions together. Present numbered
recommendations with finding, exact proposed change, benefit, risk, and default.

| Question | Default proposal |
|---|---|
| Which behavior needs tests? | One important success, rejection, or lifecycle scenario in the requested scope |
| Which execution mode? | EditMode for pure rules and Editor validation; PlayMode for player-loop/lifecycle integration |
| Change production assembly boundaries? | Keep them; separately recommend a boundary only when tests cannot reach the production code |
| Add a missing Test Framework package? | Defer until a compatible version/source is established; confirm package installation separately |
| Run suites and a normal player build? | Focused agreed suite plus representative normal-player compilation, on an isolated project if needed |

A missing framework is not permission to install a remembered version. Resolve a compatible core or
registry package for the actual Editor, confirm its id and resolution rule, and use the Package
Manager Client API. The [package guide](../PackageInstaller/InstallPackages.md) is an optional fuller workflow.
For every selected item restate the files, assembly references/platform constraints, package operation,
test scenarios, runner actions, temporary outputs, and cleanup, then obtain explicit user confirmation.

**Done:** recommendations and no-change items were shown; selected items and their exact actions are
confirmed, or the run ends with proposals only.

## 3. Apply confirmed setup

| Setting / action | Target | How to set it | Condition |
|---|---|---|---|
| Test Framework | Compatible resolved package | Package Manager Client API; observe completion and lockfile | Only when package installation was confirmed |
| Test assemblies | Installed framework's test configuration; references to required production assemblies only | Test Runner creation UI or Editor asset APIs; read back asmdefs/asmrefs | Confirmed new or changed boundaries |
| EditMode isolation | Editor-only effective assembly | Platform constraints and references appropriate to installed framework | EditMode selected |
| PlayMode configuration | Runtime test assembly excluded from ordinary players | Installed framework's test assembly configuration; a define constraint alone does not prove isolation | PlayMode selected |
| Behavioral fixtures | Failure-sensitive assertions through real production entry points | Minimal success/rejection/repeat scenarios; cleanup on assertion failure | Only selected scenarios |

Replace ignored template stubs with meaningful assertions before calling them coverage. Use temporary
storage rather than real player saves. Preserve existing production boundaries unless their change
was selected. Read back saved configuration; report compile failures and partial setup explicitly.

**Done:** every selected setup item is Applied, Already correct, or Failed with evidence, and saved
assembly configuration matches the confirmed list.

## 4. Execute and verify

Discover runner options with `unity test --help`. On a closed or isolated target project, the basic
commands are:

```bash
unity test /absolute/target/project --mode EditMode --output /absolute/results/editmode.xml
unity test /absolute/target/project --mode PlayMode --output /absolute/results/playmode.xml
```

Run only confirmed modes/scopes. Use a runner subagent when the project's instructions and available
capabilities require it; otherwise use the project runner or Test Runner UI. Read fresh XML/logs and
compare discovered tests with intended scenarios. Passed, failed, skipped/ignored, excluded, and
not-run outcomes are distinct. When practical, break the behavior or expectation in a disposable
fixture and prove the regression test fails; restore it before the final run.

Compile the confirmed representative normal player and inspect that test-only dependencies are absent;
a test-player build is a different output. Re-read saved configuration and verify fixture cleanup.
If a prerequisite is missing, retain that check as Not verified with its reason.

**Done:** each selected suite, failure-sensitivity check, discovery check, cleanup check, and player
isolation check has fresh evidence or a specific Not verified reason.

## 5. Report

Report selected recommendation IDs, changed files/packages/assembly boundaries, scenario coverage,
exact commands and fresh artifact paths, result counts, and normal-player isolation evidence. List
unpicked recommendations as proposals and unresolved choices under **Needs your decision**.

**Done:** every selected item has an outcome; skipped and unperformed work is explicit, and no
static check or ignored placeholder is counted as a passing behavioral test.

CI setup belongs to [the CI guide](../ContinuousIntegration/README.md); deeper test-quality review
belongs to [the testing lens](../ProjectAuditGuides/UnityTestingInstructions.md).
