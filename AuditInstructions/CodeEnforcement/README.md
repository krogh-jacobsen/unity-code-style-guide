> How it works: hand the enforcement document to your agent. It audits your assemblies and existing
> checks, recommends boundary rules and tests, and changes only what you select and confirm.

# Code enforcement

| Situation | Document to use |
|---|---|
| Turn architecture and API rules into tests, or add Roslyn analyzers | [SetupEnforcement.md](SetupEnforcement.md) |
| Review existing assembly boundaries without adding checks | [Assembly lens](../ProjectAuditGuides/UnityAssemblyDefinitionsInstructions.md) through the project-review router |

Rules that live only in documents drift. This folder turns the ones that matter into checks that run
with your EditMode tests, so a broken rule shows up the moment it is broken rather than in the next review.

**Ratchets, not big-bang cleanups.** An existing project rarely starts clean. The banned-API test keeps a
baseline of today's violations: new ones fail, and an entry fails once its violation is fixed, so the
baseline can only shrink. You get enforcement on day one and pay the cleanup down gradually.

**Assembly layers.** The layering in the agent document (engine-free core, contracts, features,
presentation, composition, plus adapters for vendor code and a development-only assembly for cheats and lab
scenes) comes from real projects where it held up. The agent proposes layers from your actual code and
respects a deliberate "no asmdefs" choice.

**What the agent asks:** which dependency rules you want enforced, which APIs to ban, whether to review the
first baseline, and whether to add analyzers. Running the tests needs your permission.

Example prompt: "Audit my assemblies with SetupEnforcement.md and propose boundary rules. Don't change anything yet."

Test setup itself belongs to [Testing](../Testing/README.md); CI that runs the tests belongs to
[ContinuousIntegration](../ContinuousIntegration/README.md).
