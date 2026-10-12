# AGENTS.md — Unity starter conventions

Use this as the target project's canonical instruction file. Adapt the selected stack in
[UnityTechStack.md](SetupInstructions/UnityTechStack.md) during setup. This starter repository itself
contains reusable documentation and assets; it is not a Unity project.

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

Preserve serialized field names with `[FormerlySerializedAs]` when renaming existing data. Keep
serialized enum numeric values stable. Editor tools must preserve prefab overrides and persist the
correct assets/scenes; direct tool mutations need appropriate Undo support.

Use Editor APIs for ProjectSettings while the Editor is open. Commit `Assets` with metadata,
`Packages/manifest.json`, `Packages/packages-lock.json`, and project settings; generated `Library`,
`Temp`, `obj`, `Logs`, and `UserSettings` stay out of source control.

## On-demand references

| Task | Read |
|---|---|
| Create/configure a project | [Setup workflow](SetupInstructions/README.md); select its applicable sections |
| Owned C# authoring or style review | [Style policy](CodeStyleGuide/UnityStyleGuide.md); root `.editorconfig` |
| Stack/API compatibility | [Project configuration](SetupInstructions/UnityTechStack.md); installed source/version-matched docs |
| Requested audit or change/subsystem review | [Audit index](AuditGuides/README.md), then applicable lenses only |
| Guide-conformance review | [Project review workflow](AuditGuides/ProjectReview.md) |
| Relevant implementation example | [Example index](ExampleCode/README.md), then the selected example |

Setup instructions define choices and completion checks; skills own execution. AuditGuides are
review references, not implementation tutorials. Ordinary implementation does not preload them.

For authorized Unity EditMode validation, use a test-runner subagent when delegation is available;
otherwise run through Unity CLI directly. Read fresh XML/logs and report failures, skipped tests,
and checks not performed. Documentation-only changes need static checks rather than an empty Unity run.

`CLAUDE.md` is a thin pointer to this file. When references move, update the relevant indexes and
compatibility pointers. Style changes must keep the policy, `.editorconfig`, templates, and examples
consistent.
