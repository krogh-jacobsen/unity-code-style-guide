# AGENTS.md — Unity starter conventions

Use this as the target project's canonical instruction file. Adapt the selected stack in
[UnityTechStack.md](LLMInstructions/UnityTechStack/UnityTechStack.md) during setup. This starter repository itself
contains reusable documentation and assets; it is not a Unity project. To change this repository,
follow [Maintaining this repository](#maintaining-this-repository); a target project can drop that section.

## Working rules

- Before the first owned C# change, read [the style policy](CodeStyleGuide/UnityStyleGuide.md).
  Use `m_` private instance fields, `k_` private constants, `s_` private statics, camelCase after the
  prefix, Allman braces, explicit `private`, and properties for access. The policy defines exceptions.
- Read the target's actual engine/packages and selected systems before choosing APIs. Project
  decisions take precedence over generic skill defaults. Change a selected system only within the
  user's scope and update its configuration reference.
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
[folder-only workflow](LLMInstructions/FolderStructure/SetupFolders.md); preserve existing content
and metadata, and let Unity generate new folder metadata on import.

For first installation of selected shipped templates/presets with the target Editor closed, copy
preflighted source asset/metadata pairs intact. Follow the
[resource installation protocol](LLMInstructions/SetupInstructions/InstallResources.md); existing
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
| Folders only in a new project | [Folder-only workflow](LLMInstructions/FolderStructure/SetupFolders.md) |
| Install selected script templates | [Template workflow](LLMInstructions/ScriptTemplates/SetupScriptTemplates.md) |
| Install/apply selected presets or register defaults | [Preset workflow](LLMInstructions/Presets/SetupPresets.md) |
| Create/configure a project | [Setup workflow](LLMInstructions/SetupInstructions/README.md); select its applicable sections |
| Configure Windows/macOS player and build settings | [Desktop build setup](LLMInstructions/BuildSettings/DesktopBuilds.md) |
| Configure Android/iOS player and build settings | [Mobile build setup](LLMInstructions/BuildSettings/MobileBuilds.md) |
| Owned C# authoring or style review | [Style policy](CodeStyleGuide/UnityStyleGuide.md); root `.editorconfig` |
| Stack/API compatibility | [Project configuration](LLMInstructions/UnityTechStack/UnityTechStack.md); installed source/version-matched docs |
| Audit, guide-conformance, or change/subsystem review | [Project review workflow](LLMInstructions/ProjectAuditGuides/ProjectReview.md), then applicable lenses only |
| Relevant implementation example | [CLI script and tests example](LLMInstructions/CliScriptAndTests/readme.md) |

Setup instructions define choices and completion checks; skills own execution. AuditGuides are
review references, not implementation tutorials. Ordinary implementation does not preload them.

For authorized Unity EditMode validation, use a test-runner subagent when delegation is available;
otherwise run through Unity CLI directly. Read fresh XML/logs and report failures, skipped tests,
and checks not performed. Documentation-only changes need static checks rather than an empty Unity run.

`CLAUDE.md` is a thin pointer to this file. When references move, update the relevant indexes and
compatibility pointers. Style changes must keep the policy, `.editorconfig`, templates, and examples
consistent.

## Maintaining this repository

Everything in `LLMInstructions/` serves two readers, and each topic folder carries one file for each:

1. **Agent instructions.** One or more documents a user hands to their LLM by URL ("implement the
   build settings from this document"). The agent works from that document alone.
2. **`readme.md`.** The human explainer for the folder: the key concepts, the decisions that matter,
   and an example prompt. GitHub renders it as the folder's landing page, so write it for someone
   browsing the repository.

Split the content by reader: procedure and exact values belong in the agent document; rationale and
orientation belong in the readme. Neither repeats the other.

### Agent documents

- **Stand alone.** Inline every fact the task needs. Link outward to official docs with
  unversioned URLs. A relative link to a sibling file is an optional pointer, never a prerequisite.
- **Open with the hand-off.** A short `> How it works:` blockquote naming the prompt, then a link
  to the folder's readme.
- **Follow one flow:** operating rules, preflight (read the project), ask (a batch of questions
  with defaults), apply (a table of setting, target, how to set it, and the condition), build or
  execute, verify, report.
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

- Name it `readme.md` and put one in every folder under `LLMInstructions/`. Rename an existing
  `README.md` when you next touch the folder.
- Open with the same `> How it works:` blockquote, then a table that maps each situation to the
  document to hand over.
- Explain the "why" briefly: the decisions that matter, the trade-offs, and what the agent will ask.
  Mention adjacent topics the folder does not cover and say how far its guidance carries over.

### Keeping it consistent

- A new or moved agent document needs a row in [On-demand references](#on-demand-references) and a
  mention in its folder's readme. A renamed folder needs its inbound links fixed.
- Check relative links after any move: every link in this file and in the readmes must resolve.
- Record user-visible changes in `CHANGELOG.md`; record what was validated, and what was not, in
  [Validation.md](Validation.md).
