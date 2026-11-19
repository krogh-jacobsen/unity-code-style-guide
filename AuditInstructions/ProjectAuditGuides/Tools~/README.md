> How it works: run the lens detector against a Unity project to draft the review menu, or the local
> validator to catch checklist rows detached from their Markdown tables.

# Audit guide tools

| Situation | Tool |
|---|---|
| Draft the lens menu for a project (read-only) | `python3 AuditInstructions/ProjectAuditGuides/Tools~/detect_lenses.py <project>` |
| Check checklist table rendering, parser and detector regressions | `python3 AuditInstructions/ProjectAuditGuides/Tools~/validate_audit_guides.py` |

## Lens detection

`detect_lenses.py` applies the detection rules of `ProjectReview.md` steps 1 and 2 the same way every
time. It prints a Markdown table (lens, raw count, first-party count, label, why, evidence, up to three
representative paths) and, with `--format json` or `--json-out FILE`, the same result as JSON. It
writes nothing to the project.

Evidence comes from the Unity CLI first, and the report names every rung it dropped:

1. `unity projects info --json`: engine version, render pipeline, packages. Without it the script reads
   `Packages/manifest.json` and `ProjectSettings/ProjectVersion.txt`.
2. `unity projects verify --json`: the integrity summary shown on the integrity-pass row.
3. `unity command find_assets --type <fully qualified type>`: asset types (Animator Controllers,
   mixers, TerrainData, UXML, Input Action assets, Timelines, scenes), only when `unity status` shows a
   ready Editor with this project open and its authoring root is `Assets`. Bare type names such as
   `AnimatorController` return nothing, so the script passes full names.
4. Files: extensions, YAML class IDs in scenes and prefabs (`54` Rigidbody, `82` AudioSource, `95`
   Animator, `223` Canvas, and so on), and C# text search. No CLI command exposes component or API
   usage, so these signals always come from files.

How it reads the rules:

- **First-party** excludes any folder named `ThirdParty`, `ThirdPartyAssets`, `3rdParty`,
  `3rdPartyAssets`, `Vendor`, `Plugins`, `Samples`, `Sample`, `TextMesh Pro`, `AssetStoreTools`,
  `_Recovery`, `AI Toolkit`, or ending in `~`. Add names with `--exclude`, or replace the list with
  `--no-default-excludes`. Raw counts include excluded folders.
- **Code scope.** C# under a `Tests` folder or with `[Test]` is test code; under `Editor` or opening
  with `#if UNITY_EDITOR` it is tooling. Only runtime code gives a strong signal, except for the Testing
  and Editor tooling lenses.
- **Package presence alone is weak**, and `com.unity.ugui` is not counted at all, because it ships with
  every template. `UnityEngine.EventSystems` alone is not uGUI; UI Toolkit uses it too.
- **Physics** is strong for `CharacterController`, contact callbacks, force-driven bodies, or physics
  queries in runtime code. Rigidbodies or colliders in content alone are weak, and so is a query in a
  file that builds its ray with `ScreenPointToRay` or `ViewportPointToRay` (pointer picking).
- **Audio** needs two distinct signals for Recommended; one is Optional.
- **Assemblies.** A missing asmdef is never a signal. A project rule in `AGENTS.md`, `CLAUDE.md`, or
  `README.md` that relies on the predefined assemblies makes the lens Optional and cites the line.
  `--policy-doc FILE` scans another document for that rule.
- **Other documented decisions.** `--optional "Rendering=lighting decision in AGENTS.md"` limits a
  detected lens to Optional with that reason. A decision never turns Not detected into a label.

The labels draft the menu; they are not a verdict. The agent still reads the evidence and may move a
lens with a stated reason. `--self-test` runs the detector against a synthetic project with vendor
content, pointer-picking raycasts, an Editor-only probe, and a no-asmdef policy; the folder validator
runs the same tests.

## Table structure

A blank line ends a GitHub Markdown table. Rows added after that line need a new header and separator;
otherwise the checklist becomes plain text. The validator checks this structure and runs positive and
negative parser fixtures. It does not judge technical claims or simulate an agent following a guide.
The repository validator discovers and runs it automatically.
