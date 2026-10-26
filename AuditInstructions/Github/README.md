> How it works: give this URL to your agent with an issue or pull request URL, for example
> "Implement this issue using this workflow". The agent reads the evidence, resolves material
> questions upfront, recommends a concrete change list for your selection and confirmation, then verifies each requested transition.

# GitHub workflow

| I want to… | Give your agent |
|---|---|
| Capture a playtest bug or feature idea | [GithubInstructions.md](GithubInstructions.md), with the destination and observation |
| Implement an issue with an upfront interview | [GithubInstructions.md](GithubInstructions.md), with the issue URL |
| Prepare or review a PR | [GithubInstructions.md](GithubInstructions.md), with the issue/PR URL and requested scope |
| Merge validated work and retire its branches/worktrees | [GithubInstructions.md](GithubInstructions.md), with explicit merge/cleanup scope |

## The decisions that matter

A useful ticket captures the player's problem quickly. Choosing the technical solution belongs to
implementation, when the agent can inspect the project and clarify the desired outcome. This keeps
playtest capture light while avoiding expensive work based on an ambiguous brief.

The guide carries forward lessons from UnityTycoonManager: read screenshots and comments before
coding, agree observable acceptance, keep an accountable owner, and review both project standards
and the requested behavior. It also carries the shared-checkout lessons from the ticket and commit
skills: another chat's edits are not automatically part of the current task, even in the same file.
Repository IDs, board numbers, special test categories and machine paths stay in each target project.

Issue completion, merge and playtest are separate milestones. The user's convention closes a completed
implementation issue once its requested PR is linked, while non-blocking playtest QA stays unchecked.
The board should reflect its own agreed meaning of Done. A target project can explicitly authorize a
full review/fix/merge workflow; this reusable guide asks agents to discover that policy before acting.

A green check applies to a particular revision and a particular kind of validation. Static checks
cannot establish that Unity tests pass, and passing code tests cannot establish that a saved scene is
wired correctly. After review fixes, the agent refreshes the affected evidence for the final revision.

Cleanup also has a definition of done. Squash merges can make integrated work look unmerged by commit
ancestry, and old branches can contain useful unpublished changes. The agent verifies integration,
protects active work, and preserves useful ignored evidence before retiring a checkout. Keeping an
uncertain branch costs some storage; deleting the only copy of unfinished work costs much more.

## What the agent will ask

Questions focus on missing player outcomes, reproduction, scope, acceptance and validation. The agent
uses the issue and project first, then asks short rounds with suggested defaults. A complete issue
needs no ritual interview. Capture accepts unknown details; implementation resolves choices that
would change what gets built. The repository's review contract adds a separate selection and explicit confirmation of the concrete
change list before project writes or GitHub mutations. Existing authorization defines the scope of
that list; product questions and this execution confirmation serve different purposes.

Example prompts:

- *"Capture this station-placement bug in our GitHub project's Backlog using this guide."*
- *"Implement this issue using this guide. Interview me about material gaps before coding."*
- *"Review this PR using this guide; report findings only."*
- *"Review, fix and merge this PR when its required validation passes, then safely clean up its worktrees."*

This folder covers collaboration and completion. [Version control](../VersionControl/README.md)
configures ignore rules, attributes and LFS; [continuous integration](../ContinuousIntegration/README.md)
configures automated checks; [testing](../Testing/TestingInstructions.md) covers Unity test setup.
The workflow's ownership and evidence principles carry over to other GitHub repositories, while Unity
asset safety and Editor validation apply specifically to Unity projects. App-specific stale-attachment
recovery and history/storage migrations need their own current, environment-specific instructions.
