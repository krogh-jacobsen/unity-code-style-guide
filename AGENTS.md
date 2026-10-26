# AGENTS.md — Unity starter conventions

Use this as the target project's canonical instruction file. Adapt the selected stack in
[UnityTechStack.md](AgentsInstructions/UnityTechStack/UnityTechStack.md) during setup. This starter repository itself
contains reusable documentation and assets; it is not a Unity project. To change this repository,
follow [Maintaining this repository](#maintaining-this-repository); a target project can drop that section.

## Working rules

- Before the first owned C# change, read [the style policy](AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md).
  Use `m_` private instance fields, `k_` private constants, `s_` private statics, camelCase after the
  prefix, Allman braces, explicit `private`, and properties for access. The policy defines exceptions.
- Read the target's actual engine/packages and selected systems before choosing APIs. Project
  decisions take precedence over generic skill defaults. Change a selected system only within the
  user's scope and update its configuration reference.
- Run every [AuditInstructions](AuditInstructions/README.md) document audit-first: report what is in
  place, recommend changes, let the user pick which to carry over, and change nothing before an
  explicit user authorization for the exact change list. Unpicked recommendations stay proposals.
- Prefer available Unity CLI skills for Editor control, project creation, testing, and builds.
  Discover installed CLI help and the connected Editor's command catalog; target the project
  explicitly. Use the Package Manager Client API for package changes through the Editor.
- Pair subscriptions, requests, resources, and registrations with cleanup at their owning lifetime.
  Observe async errors; source configuration assets must not accumulate unintended session state.
- Keep frequent paths free of avoidable allocations/lookups. Cache with an explicit invalidation
  contract; measure before introducing an optimization framework.
- Preserve concurrent edits and unsaved scenes. Make the smallest useful change and validate its
  behavior plus saved authoring state when it must ship configured.
- Follow the target project's documented plan location/status convention. Mark selected work done
  only after its required validation; unselected proposals remain proposals.

## Asset and serialization safety

Unity owns asset identity. Create, move, rename, and delete imported assets through Unity CLI-driven
Editor APIs (`AssetDatabase`, `SerializedObject`, scene/prefab APIs) or the Editor. Preserve existing
`.meta` files and GUIDs; import new assets so Unity creates their metadata. Do not author metadata,
edit serialized Unity YAML by hand, or delete metadata to reset import settings.

For new-project folder scaffolding with the target Editor confirmed closed, ordinary filesystem
creation of selected missing directories is allowed. Follow the
[folder-only workflow](AuditInstructions/FolderStructure/SetupFolders.md); preserve existing content
and metadata, and let Unity generate new folder metadata on import.

For first installation of selected shipped templates/presets with the target Editor closed, copy
preflighted source asset/metadata pairs intact. Follow the
[resource installation protocol](AuditInstructions/SetupInstructions/InstallResources.md); existing
imported assets and customized metadata remain subject to the Editor rules above.

Preserve serialized field names with `[FormerlySerializedAs]` when renaming existing data. Keep
serialized enum numeric values stable. Editor tools must preserve prefab overrides and persist the
correct assets/scenes; direct tool mutations need appropriate Undo support.

Use Editor APIs for ProjectSettings while the Editor is open. Commit `Assets` with metadata,
`Packages/manifest.json`, `Packages/packages-lock.json`, and project settings; generated `Library`,
`Temp`, `obj`, `Logs`, and `UserSettings` stay out of source control.

## On-demand references

| Task | Read |
|---|---|
| Folders only in a new project | [Folder-only workflow](AuditInstructions/FolderStructure/SetupFolders.md) |
| Review or reorganize an existing project's folders | [Folder review workflow](AuditInstructions/FolderStructure/ReviewFolders.md) |
| Install selected script templates | [Template workflow](AuditInstructions/ScriptTemplates/SetupScriptTemplates.md) |
| Capture/implement GitHub issues, review PRs, or complete merge/cleanup | [GitHub workflow](AuditInstructions/Github/GithubInstructions.md) |
| Set up or repair test assemblies and discoverable tests | [Test setup](AuditInstructions/Testing/TestingInstructions.md) |
| Set up GitHub CI or a test gate (no paid licence needed) | [CI workflow](AuditInstructions/ContinuousIntegration/SetupCI.md) |
| Set up `.gitignore`, `.gitattributes`, LFS, or scene merging | [Version control workflow](AuditInstructions/VersionControl/SetupVersionControl.md) |
| Install/apply selected presets or register defaults | [Preset workflow](AuditInstructions/Presets/SetupPresets.md) |
| Review packages and install missing ones | [Package installer](AuditInstructions/PackageInstaller/InstallPackages.md) |
| Install instructions or update an adapted kit | [Installation layout](README.md#how-to-install); [update workflow](AuditInstructions/KitMaintenance/UpdateKit.md) |
| Set up test assemblies and useful suites | [Testing workflow](AuditInstructions/Testing/TestingInstructions.md) |
| Assess a release candidate and prepare its handoff | [Release readiness](AuditInstructions/ReleaseReadiness/ReleaseReadiness.md) |
| Create/configure a project | [Setup workflow](AuditInstructions/SetupInstructions/README.md); select its applicable sections |
| Review or set core project settings (reload policy, input, serialization) | [Project settings](AuditInstructions/ProjectSettings/ProjectSettings.md) |
| Configure Windows/macOS player and build settings | [Desktop build setup](AuditInstructions/BuildSettings/DesktopBuilds.md) |
| Configure Android/iOS player and build settings | [Mobile build setup](AuditInstructions/BuildSettings/MobileBuilds.md) |
| Owned C# authoring or style review | [Style policy](AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md); root `.editorconfig` |
| Stack/API compatibility | [Project configuration](AgentsInstructions/UnityTechStack/UnityTechStack.md); installed source/version-matched docs |
| Audit, guide-conformance, or change/subsystem review | [Project review workflow](AuditInstructions/ProjectAuditGuides/ProjectReview.md) detects, offers, and loads only the lenses the user picks; human overview in its [readme](AuditInstructions/ProjectAuditGuides/README.md) |
| Review rendering correctness (renderer features, Render Graph, cameras, shaders) | [Rendering lens](AuditInstructions/ProjectAuditGuides/UnityRenderingInstructions.md), selected through the project-review workflow |
| Prepare a project for the experimental CoreCLR migration | [CoreCLR migration](AuditInstructions/CoreCLRmigration/CoreCLRUpgrade.md) |
| Relevant implementation example | [CLI script and tests example](AuditInstructions/UnityCLI/CliScriptAndTests/README.md) |

Setup instructions define choices and completion checks; skills own execution. The audit lenses are
review references, not implementation tutorials. Ordinary implementation does not preload them.

For authorized Unity EditMode validation, use a test-runner subagent when delegation is available;
otherwise run through Unity CLI directly. Read fresh XML/logs and report failures, skipped tests,
and checks not performed. Documentation-only changes need static checks rather than an empty Unity run.

`CLAUDE.md` is a thin pointer to this file. When references move, update the relevant indexes and
compatibility pointers. Style changes must keep the policy, `.editorconfig`, templates, and examples
consistent.

## Maintaining this repository

Everything in `AuditInstructions/` serves two readers, and each topic folder carries one file for each:

1. **Agent instructions.** One or more documents a user hands to their LLM by URL ("implement the
   build settings from this document"). The agent works from that document alone.
2. **`README.md`.** The human explainer for the folder: the key concepts, the decisions that matter,
   and an example prompt. GitHub renders it as the folder's landing page, so write it for someone
   browsing the repository.

Split the content by reader: procedure and exact values belong in the agent document; rationale and
orientation belong in the readme. Neither repeats the other.

### Agent documents

- **Stand alone.** Inline every fact the task needs. Link outward to official docs with
  unversioned URLs. A relative link to a sibling file is an optional pointer, never a prerequisite.
  One exception: [ProjectReview.md](AuditInstructions/ProjectAuditGuides/ProjectReview.md) is a router, and its
  lens files load on demand, so only the lenses the user picks are read.
- **Open with the hand-off.** A short `> How it works:` blockquote naming the prompt, then a link
  to the folder's readme.
- **Carry the review contract.** Every document that can change a project has the section below,
  verbatim, between its operating rules and step 1. `AuditInstructions/Tools/validate_all.py` fails a document that
  lacks or changes it. Published handoff targets in this file and the audit index are checked even
  when their opening blockquote is missing; additional agent documents are discovered by that
  blockquote. Human readmes and router-loaded read-only lenses are excluded; the setup README is
  an explicit workflow exception. Contract regressions and replay fixtures live in
  [audit maintenance tools](AuditInstructions/Tools/README.md).
- **Follow one flow:** operating rules, the review contract, preflight (read the project), ask (a
  batch of questions with defaults), apply (a table of setting, target, how to set it, and the
  condition), build or execute, verify, report. Preflight and ask feed the audit and the
  recommendations; apply, build, and install steps run only for confirmed items.

```markdown
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
```
- **End every step on a `**Done:**` criterion** that an agent can check. Strong criteria are both
  checkable and exhaustive ("every row has a status").
- **Report honestly.** A check that lacks its module, host, or device is *Not verified*. Starting
  values stay proposals until measured. Anything waiting on the user goes in a "Needs your decision" block.
- **Date the volatile facts.** Store deadlines, version support, and deprecations carry the month
  they were verified. Confirm API signatures and doc claims against current sources before writing
  them; mark anything unconfirmed as such.
- **Write for the agent.** Keep one source of truth per fact, state the positive target
  behaviour instead of prohibitions, and push reference an agent needs only sometimes behind a link
  (see the `writing-for-agents` skill).

### Readmes

- Name it `README.md` and put one in every folder under `AuditInstructions/`. Rename an existing
  `README.md` when you next touch the folder.
- Open with the same `> How it works:` blockquote, then a table that maps each situation to the
  document to hand over.
- Explain the "why" briefly: the decisions that matter, the trade-offs, and what the agent will ask.
  Mention adjacent topics the folder does not cover and say how far its guidance carries over.

### Tools stay with their folder

- Each topic folder owns its maintenance tools in a `Tools~/` subfolder: its validator
  (`validate_*.py`), its GUID `inventory.json`, and any authoring or test harness. Unity ignores
  folders ending in `~`, so copying the topic folder into `Assets` never imports the tools.
- A folder validator reads only its own folder and runs on its own
  (`python3 AuditInstructions/Presets/Tools~/validate_presets.py`). Keep inventory keys relative to
  the folder; use `"."` for the folder's own `.meta`.
- `AuditInstructions/Tools/validate_all.py` holds only checks that span folders (Markdown links, GUID uniqueness, the
  AGENTS contract) and runs every `*/Tools~/validate_*.py`. A new folder needs no root change.
- Agent documents that state version-dependent facts carry a `Last verified: <Month Year>` line.
  `AuditInstructions/Tools/validate_all.py` warns when one is older than six months. A folder may keep a
  `Tools~/recheck.md` listing its weakest claims and where to re-read them.
- When an agent document embeds identities (such as the GUID table in `SetupPresets.md`), its
  validator must compare them with the metadata.

### Keeping it consistent

- A new or moved agent document needs a row in [On-demand references](#on-demand-references) and a
  mention in its folder's readme. A renamed folder needs its inbound links fixed.
- Check relative links after any move: every link in this file and in the readmes must resolve.
- Record user-visible changes in `CHANGELOG.md`; record what was validated, and what was not, in
  [Validation.md](Validation.md).
