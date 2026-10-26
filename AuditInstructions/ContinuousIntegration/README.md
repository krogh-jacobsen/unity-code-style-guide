> How it works: give the URL of [SetupCI.md](SetupCI.md) to your agent and it audits your repository,
> recommends the CI files below, and installs only the ones you pick and confirm. It runs the checks
> locally first and reports what it verified.

# Continuous integration without a paid Unity licence

Most Unity users have a Personal licence, and a Personal licence cannot be activated on a hosted CI
runner: the Unity CLI's own generated workflow says so, and no workaround is officially supported. That
shapes everything here. **GitHub's free runners run the checks that need no Editor, your own machine
runs the tests**, and a pull request checklist connects the two.

| I want to… | Give your agent |
|---|---|
| Add CI to my Unity project | [SetupCI.md](SetupCI.md) |

Example prompts:

- *"Set up CI for my Unity project from this document."* Tiers A and B.
- *"Set up CI and also a workflow that runs my tests on my own PC."* Adds tier C.
- *"Check my project against the CI checks, but don't install anything."*

## What happens when you hand it over

1. **Audit.** The agent reads your repository and compares any existing CI files with the shipped ones. It writes nothing.
2. **Recommendations.** Each tier, and the style-gate mode, becomes a numbered recommendation with a risk and a default.
3. **You pick any subset**, "all recommended", or none. Tier A alone is a fine choice.
4. **You confirm** the exact file list before anything is copied.
5. **It installs, checks locally, and reports** the items you confirmed, plus the proposals you skipped.

## The tiers

| Tier | Where it runs | Needs a licence | What it gives you |
|---|---|---|---|
| **A. Project checks** | GitHub's free runner, on every pull request | No | The checks below. Takes minutes: no Editor to download, no Library to import |
| **B. Local test gate** | Your machine | Your own | `unity test` plus a pull request checklist that says what you ran |
| **C. Self-hosted runner** | A PC you own, optional | Your own, already active | The same tests on every pull request, automatically |
| **D. Licensed hosted CI** | GitHub's runner | Serial, floating, or offline file | Tests and builds. `unity ci init` writes it for you |

## What tier A catches

Each check maps to a way a Unity project quietly rots:

| Check | Catches |
|---|---|
| **`.meta` pairing** | An asset without its `.meta` (references break for everyone else), or an orphan `.meta` (its asset was deleted or ignored) |
| **Duplicate GUIDs** | Two assets claiming one identity, usually from a bad merge or a copied folder |
| **Test isolation candidates** | Resolves asmrefs to definitions in Assets and embedded packages; flags runtime test code without recognized framework configuration. Predefined Editor assemblies are reported separately. Discovery and normal-player inclusion still need Unity |
| **Ignored tests** | Reports `[Ignore]` attributes for inspection. Ignored tests are skipped, not passing tests; legitimate reasons and unfinished skeletons need different follow-up |
| **`unity vcs doctor`** | Missing ignore rules, LFS patterns or hooks, line-ending policy, floating package references |
| **Whitespace and naming** | Code that breaks your [style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md), measured against the shipped `.editorconfig` with the .NET SDK |

Everything runs from a plain checkout. The style checks work because `dotnet format` reads Unity's C#
through a small lint project that never compiles your game, so the Editor is not involved.

### What a green check means

**It does not mean your tests pass.** Tier A never starts Unity, so no EditMode or PlayMode test runs. Each
run says so in its summary. This is why tier B exists.

## Running tests

Your tests are described in the [test setup guide](../Testing/TestingInstructions.md). Run them before you
open a pull request:

```bash
unity test --mode EditMode --output /absolute/results/editmode.xml
unity test --mode PlayMode --output /absolute/results/playmode.xml
```

The Editor must not have the project open. Exit code 8 means tests failed, 6 means the run itself failed;
read the XML, because skipped and `[Ignore]`d tests are not passes. The pull request template asks you to
tick what you ran and paste the summary, so a reviewer can tell "tests passed" from "tests not run".

### Optional: run them for you (tier C)

If you want every pull request tested automatically, register your own PC as a
[self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners) with the label `unity`.
The workflow runs the same two commands with your already-active licence. Know the trade-off:

- **A self-hosted runner runs the code in the branch it checks out**, on your machine. The workflow only
  runs for branches in your own repository and manual runs, never for forks, but a collaborator with
  write access can still run code on your PC. Use it with a private repository.
- The PC must be on, with the Editor version installed, and the project closed.
- You register the runner. The agent gives the steps and does not do it.

### If you do have a licence

Run `unity ci init`. It generates a full pipeline: installs the Editor, caches the Library, activates a
serial, floating, or offline licence from a secret, runs tests (optionally split with `--shards`), and
builds. Keep tier A as the fast first job.

## Adopting this in an existing project

The first run usually finds things. Run the commands locally first, which the agent does, and then
choose:

- **Report-only** for the style steps until the baseline is clean, then flip them to blocking.
- **Fix** whitespace with `dotnet format whitespace`, on code you own, as its own commit.

Vendor code is excluded from the style checks (`ThirdPartyAssets`, `Plugins`, `Samples`, `TextMesh Pro`,
`TutorialInfo`). Add your own vendor folders to `Lint.csproj`.

## Pressure-tested, October 2026

- **Project check script** on a real Unity 6000.7.0b4 URP project: 87 assets paired with their `.meta`
  files, 8 tests in 2 files, all inside test assemblies (earlier validation). The expanded fixture suite
  covers valid and broken metadata, named/GUID asmrefs, embedded-package targets, predefined and
  explicit Editor assemblies, runtime asmdefs containing Editor folders, constraint-only and
  NUnit-only configurations, explicit framework references, and a nested project path with spaces.
  These are static classification checks; they do not establish discovery or player inclusion.
- **Style gates** with the shipped `.editorconfig` and .NET SDK 10.0: pass on the shipped sample scripts
  and fail on a script with bad whitespace and a missing `m_` prefix.
- **Unity CLI with no sign-in or licence** (an empty home directory): `unity vcs doctor` runs and exits
  4 on a genuine finding, 0 when clean.
- **The whole tier A sequence** ran on a fresh clone with no licence: all steps passed on clean code, and
  each failed when I introduced its kind of violation.
- **Workflow safety rules** are checked by `AuditInstructions/Tools/validate_all.py`: no secrets and no licence in tier A,
  read-only permissions, no `pull_request_target`, no fork runs on the self-hosted workflow, valid YAML.

Not tested: a run on a real GitHub-hosted runner (the commands were run locally, not in Actions), a
real self-hosted runner, `unity ci init` end to end with a licence, and Windows or macOS runners. The
checks are file based and should behave the same, but that was not observed.
