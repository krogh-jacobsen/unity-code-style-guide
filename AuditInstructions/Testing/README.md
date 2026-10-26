> How it works: hand the test-setup document to your agent. It audits your current tests and
> assemblies, recommends a small setup, and changes only what you select and confirm.

# Testing

| Situation | Document to use |
|---|---|
| Create or repair a test setup | [TestingInstructions.md](TestingInstructions.md) |
| Learn test types, runners, and the daily workflow | [IntroductionToTesting.md](IntroductionToTesting.md) |
| Review whether existing tests catch meaningful failures | [Testing lens](../ProjectAuditGuides/UnityTestingInstructions.md) through the project-review router |

Start from an expensive mistake the game could make, then choose the cheapest environment that can
reveal it. EditMode is useful for rules and Editor validation; actual lifecycle and runtime wiring
usually need PlayMode. A test's value comes from its assertion, not its execution mode or count.

Assembly boundaries matter because a custom test assembly must be able to reference the production
code it exercises. Existing predefined Editor assemblies can be legitimate; an asmref inherits the
configuration of its target definition. The agent inspects those boundaries before suggesting new ones.

The agent asks which scenarios and modes matter, whether a missing framework or assembly change is
wanted, and which runs/builds are permitted. Isolated runs protect an active workspace. A green
static CI check does not establish discovery, passing tests, or exclusion from the shipped player.

Hosted workflows belong to [ContinuousIntegration](../ContinuousIntegration/README.md); package
selection belongs to [PackageInstaller](../PackageInstaller/README.md). This folder establishes test
setup and evidence, rather than prescribing gameplay architecture or a coverage percentage.
