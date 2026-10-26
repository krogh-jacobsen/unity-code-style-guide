> How it works: give this URL to your agent, for example "Set up CI for my Unity project from this
> document". The agent audits your repository first and recommends licence-free GitHub checks, a pull
> request template, and optionally a workflow for your own test machine. You pick which to carry over;
> nothing changes before you confirm, and it verifies what it installs locally first.
> Human overview: [readme](README.md).

# Set up CI for a Unity project (agent instructions)

Install continuous integration that works **without a paid Unity licence**. A Personal licence cannot be
activated on a hosted CI runner (the CLI's own generated workflow notes that `unity license activate
--personal` does not work there), so the default design runs everything that needs no Editor on a hosted
runner, and runs Editor tests locally or on a machine the user hosts. This document is self-contained.
It does not commit, push, register a runner, or store a secret. **Last verified: October 2026** (Git
2.54, .NET SDK 10.0, Unity CLI 1.0.0-beta.13, Unity 6000.7.0b4 and 6000.6.2f1).

Source (replace `main` with a commit SHA for a repeatable run):
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/AuditInstructions/ContinuousIntegration/`

## What each tier does

| Tier | Runs where | Needs a Unity licence | Catches |
|---|---|---|---|
| **A. Project checks** (default) | GitHub-hosted runner | No | Missing/orphan metadata, duplicate GUIDs, static test-isolation candidates, ignored-test notices, Git settings, whitespace and naming violations |
| **B. Local test gate** (default) | The developer's machine | Their own | Failing EditMode and PlayMode tests, through `unity test` and a pull request checklist |
| **C. Self-hosted test runner** (opt-in) | A machine the user owns | Their own, already active | The same tests, run on every pull request |
| **D. Licensed hosted CI** (opt-in) | GitHub-hosted runner | Yes: a serial, floating, or offline licence | Tests and player builds. Use `unity ci init`, not these files |

Tier A never runs the Editor, so **a green run does not mean tests pass**. Say so wherever you report it.

## Operating rules

- Never write a licence, serial, token, or password into a workflow or file. Tier A uses no secrets.
- Do not enable Tier C on a public repository without the user's explicit approval of the risk below.
- Copy the shipped files unchanged except for the documented edit points. Do not commit or push.
- Report observed results separately from checks you could not run (**Not verified**).

- Recommendation IDs retain the meaning of the actual prior proposal. The tier IDs below are
  defaults for a new audit, not replacements for an existing approved change list. On resume,
  recover the exact files/settings/commands before planning execution; missing details remain
  Not verified while unchanged authorization is preserved; continue independent read-only preflight
  while recovering that scope. Do not infer Tier A merely from `R1`.

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

This step is the audit input and changes nothing. Identify one Unity project and its repository. Record:

- The **host**. The workflows are GitHub Actions. For another host, install the scripts only and say the
  workflow is not provided (`unity ci init --provider gitlab` covers GitLab for licensed projects).
- **Project root versus repository root.** Tier A takes the project path from `UNITY_PROJECT_PATH`.
- Existing `.github/workflows/`, `.github/unity-ci/`, and `.github/pull_request_template.md`.
- An **`.editorconfig`** in the project or repository root. The style checks measure against it, so if it
  is missing, install the [EditorConfig starter](../../AgentsInstructions/CodeStyleGuide/EditorConfig/README.md) first or skip the style steps.
- Whether the repository is public or private, and `unity license status` on this machine.
- Whether tests exist (`Assets/**/Tests`, test asmdefs). Follow the [test setup guide](../Testing/TestingInstructions.md)
  when they do not.
- How each existing file compares with its shipped version. Fetch the shipped files into a temporary
  folder outside the project (not a project change) and mark each destination absent, identical, or
  different.

**Done:** host, roots, existing files and their comparison, `.editorconfig`, visibility, and test
presence are known, and the audit was shown to the user.

## 2. Ask and select

Ask in one batch, then show each tier as a numbered recommendation (stage 2) so the user can pick any
subset. The defaults below are recommended defaults: they still need the stage 4 confirmation. Apply
the default when the user says "use defaults".

| ID | Question | Recommended default |
|---|---|---|
| R1 | Tier A (licence-free GitHub checks)? | Do |
| R2 | Tier B (pull request template with a test checklist)? | Do |
| R3 | Tier C (self-hosted test workflow)? | Skip. Needs a runner you register, and the security note in the workflow |
| R4 | Style steps blocking from the first run, or report-only until the baseline is clean? | Report-only when the baseline run in step 4 has findings |

Add your own recommendations from the audit, such as a missing `.editorconfig` or a conflicting workflow.

**Done:** the audit and recommendation list were shown, the user's picks are recorded, and an explicit
user authorization for the exact file list was received before any change.

## 3. Install

Only the items confirmed in stage 4. Stage the files, check them, then copy. Files install to these destinations:

| Source | Destination | Tier |
|---|---|---|
| `Workflows/unity-checks.yml` | `.github/workflows/unity-checks.yml` | A |
| `Scripts/check_unity_project.py` | `.github/unity-ci/check_unity_project.py` | A |
| `Scripts/Lint.csproj` | `.github/unity-ci/Lint.csproj` | A |
| `Workflows/pull_request_template.md` | `.github/pull_request_template.md` | B |
| `Workflows/unity-tests-self-hosted.yml` | `.github/workflows/unity-tests-self-hosted.yml` | C |

1. **Stage** into a temporary folder and reject HTML or error responses.
2. **Destinations.** Absent: install. Identical: leave it. Different content: a conflict. Show both and
   resolve it before copying; never overwrite a project's own workflow or template.
3. **Edit points**, and only these: `UNITY_PROJECT_PATH` in both selected workflow files when the
   project is a repository subfolder (and the matching `Lint.csproj` exclusions if the project has more vendor or
   sample folders); the `branches:` list when the default branch is not `main`.
4. If the style gate is report-only, add `continue-on-error: true` to the two `dotnet format` steps and
   say that is temporary.

**Done:** every confirmed file is installed or identical, and the edit points are the only differences.

## 4. Run the checks locally first

Applies to the installed tiers only. A new gate often fails on the existing code. Learn the baseline before the first push. Run from the repository
root (where `.github/` lives), exporting the absolute Unity project path, including any subfolder:

```bash
export UNITY_PROJECT_PATH="/absolute/repository/path/to/UnityProject"
python3 .github/unity-ci/check_unity_project.py --project "$UNITY_PROJECT_PATH"
unity vcs doctor "$UNITY_PROJECT_PATH"
dotnet restore .github/unity-ci/Lint.csproj
dotnet format whitespace .github/unity-ci/Lint.csproj --no-restore --verify-no-changes
dotnet format style .github/unity-ci/Lint.csproj --no-restore --diagnostics IDE1006 --severity info --verify-no-changes
```

Read each exit code. `unity vcs doctor` exits 4 on a finding. `dotnet format` exits 2 when it would
change something. Report the count per check. Offer to fix formatting with
`dotnet format whitespace <Lint.csproj>`, but only on the user's own code and only with approval: it
rewrites files. Without the .NET SDK or the Unity CLI locally, report those checks as **Not verified**.

**Done:** each check has a baseline result, and the style-gate mode is chosen from it.

## 5. The local test gate (Tier B, only when confirmed)

The pull request template tells reviewers what was run. The commands are in the
[test setup guide](../Testing/TestingInstructions.md):

```bash
unity test /absolute/project --mode EditMode --output /absolute/results/editmode.xml
unity test /absolute/project --mode PlayMode --output /absolute/results/playmode.xml
```

Close the project in the Editor first. Exit code 8 means tests failed; 6 means the run itself failed.
Read the result XML, not just the exit code. Run them now if the user agrees, and report passed,
failed, skipped, and `[Ignore]`d counts from the files.

**Done:** the user has the commands, and the suites were run or the gap is stated.

## 6. The self-hosted workflow (Tier C, only when confirmed)

Registering a runner is the user's action: it needs a token from their repository settings. Give these steps and do
not perform them.

1. Settings > Actions > Runners > New self-hosted runner, on the machine that has the Editor, and add the
   label `unity`.
2. The runner service must run as the user whose Editor licence is active. `unity license status` must show it.
3. Set the workflow's `UNITY_PROJECT_PATH` to the intended project under `${{ github.workspace }}`.
   Its `ProjectVersion.txt` selects the required installed Editor; the project must not be open in it.
   Preflight runs in that directory, and both test commands name it explicitly.
4. **Security.** A self-hosted runner executes the code of whatever it checks out. The workflow is limited
   to branches in the same repository and manual dispatch. Keep the repository private, or understand
   that a contributor with write access can run code on that machine.
5. Run the workflow once with **Run workflow** (`workflow_dispatch`) and read the uploaded results.

**Done:** the steps were given, and the first run is observed by the user or reported as **Not verified**.

## 7. Verify

- The Tier A files match the source, and `.github/unity-ci/` holds both scripts.
- Step 4's commands ran (or are reported **Not verified**).
- The workflow files are valid YAML and contain no secret or licence reference.
- A real GitHub run needs a push, which only the user approves. After one, read the run summary: it
  lists errors and states that Editor tests did not run. Until then report the hosted run as **Not verified**.

**Done:** each installed tier has a verification result or a specific Not verified reason.

## 8. Report

| Item | Status | Detail |
|---|---|---|
| Source URL and revision | | |
| Recommendations picked and confirmed | R-IDs applied | The exact change list the user confirmed |
| Recommendations not picked | Proposal | R-IDs left open, with the default and risk |
| Tier A files | Installed / Identical / Conflict | Paths |
| Tier B template | Installed / Identical / Declined | |
| Tier C workflow | Installed / Declined | Runner registered by the user? |
| Baseline per check | Pass / N findings / Not verified | meta and tests, doctor, whitespace, naming |
| Style gate mode | Blocking / Report-only | |
| Editor tests | Run locally / Not run | Counts from the result files |
| Hosted run | Observed / Not verified | |

Put conflicts, a failing baseline, the unpicked recommendations, and the Tier C security choice in a
"Needs your decision" block at the top. Say plainly that Tier A does not run tests.

**Done:** every selected tier and unpicked recommendation is accounted for, including hosted-run limits.

## For users with a licence

Use `unity ci init` (`--provider github` or `gitlab`, `--shards N` to split tests) instead of these
workflows. It generates a complete pipeline: it installs the Editor, restores caches, activates a
licence, runs tests, and builds. Its licence step takes a serial, a floating server, or an offline
licence file as a secret, and it states that `--personal` activation does not work in CI. Tier A files
still complement it as the fast first job.
