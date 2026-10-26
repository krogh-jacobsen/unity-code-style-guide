# Change log

## 2026-10-26 — Fresh-agent project review decision replay

- Executed all 94 new decision cases with fresh agents. Baseline found two failures; an initial correction exposed seven approval regressions before being stopped. After refinement, the full rerun passed 94 cases and all 207 expected outcomes; another 10 cases / 22 outcomes passed after concurrent CI/folder-guide edits.
- Clarified the shared contract and all 18 copies: recover a missing approved change list only when concrete scope was previously presented and authorized; scope never presented must first be presented and confirmed. Guide defaults cannot reconstruct the approved scope.
- Preserved known runtime evidence fields in project review and diagnosis, strengthened duplicate-approval replay expectations and contract regressions, and saved source snapshots, responses, grading evidence, environment, and limitations in the replay report linked from Validation.md.

## 2026-10-26 — Fresh-agent workflow replay fixes

- Executed the original 106 decision-replay cases in separate fresh agents with expected outcomes withheld. The baseline exposed dirty-tree rules that paused independent read-only audit, plus incomplete fixture evidence and several contradictions agents worked around. Final rerun counts and evidence are recorded in `Validation.md`.
- Scoped clean-tree/checkpoint requirements to confirmed execution, clarified CoreCLR checkout isolation and existing-baseline inspection, and made unavailable values/report statuses explicitly Not verified. Existing and older projects retain the observed reload policy during audit; settings reference links now follow unversioned official routes.
- Made desktop/mobile profile creation follow selected platforms, documented CLI-free execution routes, aligned the optional project-root ArtSource completion criterion, and made preset budget tuning a separate handoff. The setup coordinator now reports unavailable delegated topics without claiming a complete cross-topic audit; AGENTS documents both coordinator exceptions.
- Added concrete prerequisite evidence per workflow, explicit CLI-free tool availability and single-platform selection, and three focused fixtures for ArtSource, budget handoff, and unknown settings. The fixed replay checkpoint covers 213 case IDs across the global and topic-owned catalogs; tests check that no published workflow falls back to an unnamed missing-prerequisite case.
- Completed the 103 added cases and 18 focused corrective reruns. Latest results pass all 213 case IDs and 432 expected outcomes across 286 distinct fresh-agent executions; the archive retains all earlier failures and incomplete results. Fixed prior-scope recovery in CI/folder review, continued independent preflight in script templates, future-import reporting for preset updates, and two ambiguous fixture expectations. No live Unity or remote operations are inferred from decision results.

- Labeled earlier publication counts and partial replay status as historical, retaining their original evidence and distinguishing completed decision results from unverified Unity behavior.

## 2026-10-26 — Strengthen review evidence and acceptance

- Added runtime activity/source context, diagnostic cause assessments, checkable acceptance conditions, source freshness and concurrent ownership, and separate implementation/acceptance outcomes to project review and diagnosis guidance.
- Material observations outside selected lenses remain visible without claiming those lenses reviewed. Added four review-specific decision scenarios and routing coverage. Independent publication validation is recorded in Validation.md.

## 2026-10-26 — Clarify authorization across audit workflows

- Updated the canonical review contract and all 18 published copies: explicit implementation instructions authorize already-presented concrete changes, selection alone does not, and unchanged authorization survives duplicate replies. Recover missing previously approved scope; confirm changes that were never concretely presented.
- Aligned human summaries/completion wording and CI recommendation-ID handling. Added five approval scenario families, decision-prompt support, and contract/authorization regressions. Independent publication validation is recorded in Validation.md.


## 2026-10-26 — Preset installation and registration pressure-test refinements

- Expanded preset discovery to active installations, package/reference copies, registrations, and helpers; existing paths are reused. Added baseline/local/upstream update comparison, explicit unknown-baseline handling, effective-policy review, recovery, and tested Editor updates preserving GUIDs and metadata.
- Added version-checked registration APIs, concrete single/alternative glob examples, positive/negative/overlap checks, separate live and saved-file readback, targeted saves, genuine new imports, and no-op reruns. Timestamp changes alone do not establish a configuration write.
- Clarified mixed-folder audio selection, future-import effects of updating registered presets, and corrections within approved scope. Qualified beta compatibility claims with historical and reported conflicting evidence rather than a universal model pass.
- Added nine topic-owned decision scenarios, a topic-local replay generator, regressions for approval boundaries and safe output generation, and a disposable-project validation procedure. Static checks and runtime/replay limitations are recorded in Validation.md; preset assets and metadata are unchanged.

## 2026-10-26 — Audit pressure-test corrections and coverage (R1–R10, R12)

- Corrected static cleanup semantics (`NoAutoStaticsCleanup` preserves state, generated cleanup needs a `partial` type, mutable `static readonly` contents need inspection), reconciled the Static Event template's documented 6.5 minimum with its 6.6/6.7 compile-tested versions, and made older-Editor adaptations separate custom resources.
- Corrected Android/iOS frame-rate guidance and made thermal advice measurement-based. Desktop/mobile completion now follows the selected platforms. Animation, uGUI layout/hiding, and input-timing checks require a broken behavior contract rather than flagging valid configurations.
- Reworked CI assembly classification to resolve named/GUID asmrefs and embedded-package definitions, distinguish predefined Editor assemblies, and reject constraint-only/NUnit-only assumptions. Unavailable registry/git package identities are explicitly Not verified; ignored tests are reported as skipped rather than passed. Added valid and broken regression fixtures, including framework GUIDs and a Unity project nested in a repository path with spaces.
- Made local and self-hosted CI target the same explicit Unity project while keeping workflow/script paths relative to the repository root. Added mobile and package-audit routes to end-to-end setup.
- Rebuilt test setup as a standalone audit/recommend/select/confirm/apply/verify workflow with a human README. Published entry points are discovered independently of their preamble and checked against the complete canonical review contract. Added contract-corruption/routing regressions and a reusable replay-fixture catalog for older Editors, dirty workspaces, missing tools/prerequisites, partial installs, repeat runs, and single-platform scope.
- Added a conditional rendering-correctness lens for renderer/pass wiring, Render Graph resources, camera stacks, and shader compatibility; connected the router, overview, diagnosis route, and AGENTS index. Reviews now identify navigation, networking, Physics2D, DOTS, and other detected systems outside lens coverage. R11 (a localization/accessibility lens) remains unselected.
- Verification and remaining limits are recorded in `Validation.md`; replay prompts are not represented as observed agent behavior.

## 2026-10-26 — Installation, updates, testing, releases, and repository CI

- Replaced stale installation destinations with a reference snapshot outside Assets, a machine-readable snapshot manifest, and explicit root-instruction/EditorConfig merge rules. Selected Unity resources remain separate imports. Added a temporary-destination checker for link closure, anchors, exact case, root routing, and EditorConfig, with four deliberate broken-link probes.
- Added KitMaintenance instructions for three-way updates, unknown-baseline handling, local adaptations, per-group source revisions, identity-preserving resource updates, and target validation.
- Completed Testing with its human README, standard review contract, assembly-boundary choices, fresh test evidence, and ordinary-player isolation checks; removed the stale UI example reference.
- Added ReleaseReadiness instructions and human guidance tying acceptance, save compatibility, diagnostics, notices, and recovery to a specific candidate artifact. Publishing remains a separately authorized action.
- Added this repository's GitHub Actions workflow for pull requests, main pushes, and manual runs. It runs repository/topic/installation checks plus the real naming fixture, without Unity. Required .NET checks now fail when unavailable; style failures include command diagnostics and have a bounded command timeout.
- Updated routing and corrected obsolete scene-template maintenance commands. See Validation.md for observed checks and remaining limits.

## 2026-10-26 — Validator moved into AuditInstructions

- Moved `Tools/validate_all.py` to `AuditInstructions/Tools/validate_all.py` and removed the root `Tools/` folder. Run `python3 AuditInstructions/Tools/validate_all.py`. It still checks the whole repository, and the live instructions that mention it were updated. Older entries keep the old path as history.

## 2026-10-26 — README.md everywhere

- Renamed the 18 lowercase `readme.md` files to `README.md`, so every folder uses one spelling, and updated the links and the contributor rule in `AGENTS.md`. Older entries keep the old spelling as history.
- `Tools/validate_all.py` now fails a link whose letter case differs from the file on disk. macOS and Windows hide that mismatch, and Linux (including CI) breaks on it.

## 2026-10-26 — Repository split: AgentsInstructions and AuditInstructions

- The repository is now two folders. `AgentsInstructions/` is the copy-and-paste starter for new projects (AGENTS.md, the code style guide and EditorConfig, UnityTechStack, UnityProjectRules). `AuditInstructions/` (formerly `LLMInstructions/`) holds the audits: each topic has a human `readme.md` plus an agent document you hand to your agent by URL. Entries below keep the old `LLMInstructions/` paths as history.
- Repointed 88 relative links and every plain-text path, the five raw GitHub source URLs in the install guides, `Tools/validate_all.py`, and two folder scripts that read `.editorconfig` (`validate_ci.py`, `check_naming.py`). `python3 Tools/validate_all.py` passes again (430 links, 6 folder validators).
- The raw GitHub URLs in the install guides resolve only after the new folder names are pushed.

## 2026-10-26 — Package installer rewritten

- Rewrote `PackageInstaller/InstallPackages.md` from a two-line stub into an agent document in the standard flow with the review contract: a read-only preflight of the manifest, lockfile and owned code, a core-or-registry check per package, evidence-based recommendations (Test Framework, Cinemachine, Input System, Addressables, or a package the user names), the user's picks, and an Editor-API install with lockfile verification. Added the folder `readme.md` and an index row.
- Unity 6.6 and later ship Cinemachine, Test Framework, Input System and more as core packages whose version is fixed to the Editor. The guide checks the lockfile `source` first and never pins or looks up registry versions for them; registry packages use `versions.recommended`, else `latestCompatible`. `Client.Add` with a bare id installs the latest compatible released version, not Unity's recommended one.
- It never removes or downgrades a package, and edits `manifest.json` only on an explicit user request. A Cinemachine 2 project is reported, not upgraded.
- Two read-only dry-runs (a real project and a synthetic one with missing packages, an older Editor, Cinemachine 2 code and a transitive-only dependency) found 25 document defects (vocabulary, undefined owned scope, Cinemachine 2 rule, transitive handling, URL placeholder, empty-result output); all were fixed.

## 2026-10-26 — Project review: pick-your-own reviews

- Rebuilt `LLMInstructions/ProjectAuditGuides/ProjectReview.md` as an agent-document router: hand-off blockquote, operating rules, the review contract, preflight with detection, a menu of lenses with a detection signal each (Recommended, Optional, or Not detected), shortcuts (Quick health check, Full review, Custom), the selected reviews, live-evidence gaps, a report with numbered recommendations, and apply-after-confirm. Reviews are read-only; the contract gates every fix. Added the folder `readme.md`, an AGENTS.md row and exception for the router pattern, and an index row.
- Pressure-tested all 15 lenses with five independent reviewers (fact-check, audit-worthiness, overlap, hygiene), then applied the approved triage: every vague `Finding when` is now a checkable trigger, duplicated checks point to one owner (Scenes: async and destroyed objects; Input: UI/world arbitration; Physics: query completeness; Performance: all cost; Assets: stripping and `.material`; Assemblies: test inclusion; Persistence: settings save), pinned doc links are unversioned, and nonexistent skills (`tdd`, `codebase-design`, `diagnosing-bugs`, `prepare-unity-3d-asset`) are gone.
- Converted the Debugging file into a defect-diagnosis mode (symptom in, owning lens out) instead of an audit lens; split Editor tooling into an always-on Integrity pass and a conditional Tool authoring part; made uGUI, Physics, Animation, and Audio conditional on detection. Audio stays its own lens.
- Corrected the `[AutoStaticsCleanup]` version: documented from Unity 6.5, not 6.6 (ProjectSettings guide and readme, ScriptTemplates guide and readme). Removed the "6.6+ analyzer" wording.
- Fixed 16 links in `Testing/IntroductionToTesting.md` that pointed at another project's files; the repository validator now ends in PASS.
- A read-only dry-run against a real project found 11 defects in the first hub draft (a uGUI signal that matched UI Toolkit, vendor counts, paths with spaces, overlapping stage and step numbering, no scope home, no CLI-forbidden fallback) and 7 lens gaps; all were fixed.

## 2026-10-26 — Audit-first, confirm-before-change contract

- Every agent document that changes a project now runs the same four stages: audit (read-only), numbered recommendations (finding, why, risk, default), the user picks any subset or none, and the exact change list needs an explicit yes before anything is written. Unpicked items stay proposals in the report; a non-interactive session stops after the recommendations.
- The canonical block lives in `AGENTS.md` ("Maintaining this repository") and is inlined verbatim into 13 documents: GithubInstructions, DesktopBuilds, MobileBuilds, ProjectSettings, SetupFolders, ReviewFolders, SetupVersionControl, SetupPresets, SetupScriptTemplates, SetupSceneTemplates, SetupCI, CoreCLRUpgrade, and the SetupInstructions README. Their ask steps now gather inputs, "use defaults" produces recommended answers that still need confirmation, and apply steps run only for confirmed items.
- `SetupInstructions/README.md` merges the delegated workflows' recommendations into one list, so the user picks and confirms once across topics.
- `Tools/validate_all.py` fails a document that opens with `> How it works:` (readmes excluded) or sits in its extra list but lacks the section, or places it after step 1. Folder readmes and the topic index gained a "What happens when you hand it over" section.
- `Github/GithubInstructions.md` carries the contract too (13 documents in all). Its gate covers every repository change and outward GitHub action (comment, push, PR, merge, close, board move); read-only retrieval and capture-only drafts stay frictionless.
- Not covered: the read-only `ProjectAuditGuides` and unfinished drafts.

## 2026-10-26 — GitHub collaboration workflow

- Expanded the GitHub draft into a self-contained capture, interview, implementation, PR review/publication, merge and cleanup workflow based on UnityTycoonManager sessions, project workflows and ticket/commit skills. Kept target-specific permissions, board IDs and test policies discoverable rather than hard-coded.
- Added the human GitHub readme and routing in AGENTS.md and the topic index. Distinguished issue closure, merge and follow-up QA; required current-revision validation and verified preservation/cleanup.
- Checked GitHub rendered-body, issue-linking and merge-method claims against official documentation; static validation and limits are recorded in Validation.md.

## 2026-10-26 — CoreCLR migration guide

- Restructured `LLMInstructions/CoreCLRmigration/CoreCLRUpgrade.md` into the standard agent-document flow: hand-off blockquote, operating rules, preflight with a baseline, an ask batch with defaults, an inventory-and-apply table (statics, retained assembly references, source-asset writes, threads and native resources, dependency targets, persisted data, lifecycle attributes), verification, a report template, rollback, and a "Needs your decision" block. Every existing claim is kept; the "Last verified: October 2026" line now feeds the staleness warning.
- Expanded the folder's `readme.md` (human overview, situation table, what to know first, what the agent asks) and added `Tools~/recheck.md` listing the weakest claims. Added the row to the `AGENTS.md` on-demand table and pointed the topic index at the readme.
- Not yet validated: the workflow has not been run against a real project or a CoreCLR Editor.

## 2026-10-21 — Agent-ready build settings

- Added `LLMInstructions/BuildSettings/` with agent documents for desktop (Windows/macOS) and mobile (Android/iOS) setup, plus a human `readme.md` covering the key decisions and VR, Web, and console carry-over.
- Rewrote the desktop guide as an executable flow: preflight, support-contract questions, settings table with Editor API names, build profiles and CLI, verification, and a required report. Added Intel Mac deprecation, Windows Arm64 limits, D3D12 fallback, PSO warm-up, and Windows toolchain guidance.
- Added a top-level `LLMInstructions/readme.md` topic index and a "Maintaining this repository" section in `AGENTS.md` defining the agent-document plus readme convention; repaired seven stale links in `AGENTS.md`.
- Restructured `LLMInstructions/FolderStructure/` into a self-contained agent document (`SetupFolders.md`) and a human `readme.md`; the former `FolderStructure.md` policy now lives in those two files. Repointed the root README and setup index to the new paths.
- Added `LLMInstructions/FolderStructure/ReviewFolders.md`: a read-only review of an existing project's folders against the layout, with optional move batches rated by risk, checkpointed, and verified (GUIDs, compile, assembly membership, references, path-dependent loads). Not yet run against a real project.
- Rewrote `LLMInstructions/Presets/` as a self-contained agent document (`SetupPresets.md`: inventory with GUIDs, staged install, optional apply, optional Preset Manager registration, platform budgets by pointer) and a human `readme.md`. Desktop texture budgets now live only in the build guides.
- Made each folder self-encapsulated for tooling: validators, GUID inventories, and maintenance tools now live in `<folder>/Tools~/` (Presets, ScriptTemplates, SceneTemplates, CliScriptAndTests; `check_naming.py` under CodeStyleGuide). `Tools/validate_all.py` keeps only repo-wide checks and runs every folder validator. The inventory dropped 45 entries for the removed `ExampleCode` samples, and the presets validator checks that the `SetupPresets.md` GUID table matches each preset's metadata. Restored the `CliScriptAndTests` and `SceneTemplates` folder `.meta` files (original GUIDs) beside their folders.
- Rewrote `LLMInstructions/ProjectSettings/` as a review-first agent document and a human `readme.md`, pressure-tested against the Unity 6.7 beta manual and the 6.6 release notes. Domain reload is now off by default for new projects, so the guide replaces "disable domain reload" with a static-state reset policy (`[AutoStaticsCleanup]`, analyzer, `SubsystemRegistration` fallback). Also noted Burst built-in, dynamic batching obsolete, `UNITY_64`/`DEVELOPMENT_BUILD` deprecated, and the Android ES 3.1 and adaptive-icon changes in the mobile guide.
- Linked the static-state audit to the Scenes and lifecycle lens (both ways), added `ProjectSettings/Tools~/recheck.md` for the thinly sourced 6.6/6.7 claims, and made `Tools/validate_all.py` warn when a "Last verified" date is older than six months.
- Rewrote `LLMInstructions/ScriptTemplates/` as a self-contained agent document (`SetupScriptTemplates.md`: inventory with GUIDs, staged install, menu readiness, optional generation check) and a human `readme.md`; the former `ScriptTemplates.md` policy is folded into them. Pressure-tested all non-package templates on Unity 6000.7.0b4 (26 generated scripts, zero errors) and fixed the Static Event template, which triggered `UAL0010`/`UAL0013`; it now uses `[AutoStaticsCleanup]` (Unity 6.6+). Added an Awaitable Operation template (priority 18; cancellable, owner-observed, Unity-generated metadata) after a compile check caught a `CS4014` warning, switched the IMGUI Custom Editor to `DrawDefaultInspector()`, documented `sealed` and static events with `[AutoStaticsCleanup]` in the style guide, and fixed the style guide's stale audit links. The validator now checks the GUID table and that static state carries a lifecycle attribute; the generation harness lives in `ScriptTemplates/Tools~`.
- Added `LLMInstructions/ContinuousIntegration/`, designed for users without a paid Unity licence (the Unity CLI's generated workflow documents that `unity license activate --personal` cannot run in CI). `SetupCI.md` (agent) and `readme.md` (human) describe four tiers: licence-free GitHub checks, a local test gate with a pull request template, an optional self-hosted test workflow, and a pointer to `unity ci init` for licensed projects. Shipped: `Workflows/unity-checks.yml`, `Workflows/unity-tests-self-hosted.yml`, `Workflows/pull_request_template.md`, `Scripts/check_unity_project.py` (meta pairing, GUID uniqueness, test isolation, `[Ignore]` count), and `Scripts/Lint.csproj` (lets `dotnet format` check whitespace and naming without the Editor). The validator runs the script against 8 fixture projects and the style gates against clean and bad code. Corrected the version-control guide: `unity vcs doctor`'s `META_FILES_IGNORED` finding appears only while the ignored `.meta` exists locally, so CI does not hit it. Linked the Testing guides to the CI guide.
- Added `LLMInstructions/VersionControl/`: a self-contained agent document (`SetupVersionControl.md`: preflight, ask, managed-block install, tracked-but-excluded report, verification, report) and a human `readme.md`, with the ignore and attribute starters moved in (`Unity.gitignore`, and `Unity.gitattributes` from `EditorConfig/`). The ignore block now carries GitHub's current Unity template, build-side Burst and IL2CPP folders, profiling and diagnostic captures (`ProfilerCaptures/`, `*.pdata`, `*.snap`, `*.rdc`, `*.diagsession`, `*.etl`), and an optional `Assets/ThirdPartyAssets/` exclusion matching the folder guide. The attributes file adds line-ending policy and an optional LFS section; merge drivers are left to `unity vcs merge-setup`. The repository's own root `.gitignore` is now a minimal repo-specific file. The validator checks real Git behavior in a throwaway repository; `unity vcs doctor` on Unity 6000.7.0b4 reports only the expected ThirdPartyAssets meta finding.
- Rewrote `LLMInstructions/SceneTemplates/` as a self-contained agent document (`SetupSceneTemplates.md`: preflight for URP and Input System handling, group dependencies, GUID table for all 29 files and folders, staged install, scene-generation and dependency-ownership checks, report) and a human `readme.md` (what is included, requirements, camera contract, clone-versus-reference). The former `SceneTemplates.md` is split between them and no longer mentions the private source project. Re-ran the delivery harness on a fresh URP project at a relocated path on Unity 6000.7.0b4 and 6000.6.2f1: six scenes generated and reopened, 8 of 8 tests passing, no diagnostics. The validator now checks that the GUID table matches the metadata.
- Extended the folder guide, checked against Unity docs: template leftovers (`Assets/Settings`, samples), naming and path-length rules, source art in `ArtSource` and `~`/dot hidden folders, local packages, Android plugin folders, namespaces versus folders.
- Not yet validated in a Unity project: API names, mobile defaults, and the agent workflow end to end.

## 2026-10-17 — Strategy scene templates

- Added optional Strategy Sandbox, UI Preview, and Asset LookDev scenes/templates, authored through Unity in disposable projects.
- Added a standalone strategy camera/input prefab, neutral URP materials and scene-specific volumes, and an interactive UI Toolkit preview.
- Defined cloning for editable UI/volume assets and shared references for camera/input/material resources; kept Map Authoring deferred.
- Added installation guidance, reproducible maintenance/validation tools, and focused scene/input/UI checks. See the dated validation record for verified results and limits.

## 2026-10-17 — Mac and Windows starter improvements

- Added optional UI Toolkit Inspector, EditorWindow, and PropertyDrawer templates alongside the IMGUI choices; enabled multi-object editing in the Inspector scaffolds.
- Added pool Inspector tooltips and expanded its guard clauses to match the brace convention.
- Added PCM UI clicks, mono ADPCM spatial SFX, and compressed-in-memory layered ambience presets, authored through Unity with new metadata.
- Made the static-model preset disable generated colliders as documented, preserving its GUID and unrelated importer settings.
- Added Mac/Windows architecture, texture/audio budget, frame-pacing, quality-tier, and development/release guidance with explicit device acceptance.
- Updated resource identities and static inventory checks; see the dated validation record for fresh checks and remaining limits.

## 2026-10-12 — Optional ownership and CLI examples

- Added screen cancellation with request identity guards, an enabled-screen adapter, and controlled/PlayMode tests.
- Added pooled notification leases with state reset, subscription/timer cleanup, safe reuse, and owner teardown tests.
- Added a custom Pipeline CLI command that previews/generates a C# script, preserves existing files/GUIDs, and demonstrates focused behavioral test execution.
- Kept examples optional, recorded 15 EditMode and 4 PlayMode passes and a normal player build, and inventoried Unity-generated resource identities.
- Repaired four setup/preset links after documentation restoration; preserved the restored style guide and READMEs.

## 2026-10-12 — Starter kit restructuring

- Reduced AGENTS.md to conventions, asset safety, CLI execution, and on-demand routing; added CLAUDE pointer.
- Made Unity 6.7 the intended profile with exact compatibility tracked separately; removed migration forecasts from normal setup.
- Replaced setup assumptions with an ordered CLI-first contract and manual fallback; filled test setup.
- Reduced style policy and corrected Roslyn rule specificity, formatter exclusions, and enforcement claims.
- Kept five minimal default script templates; separated eight optional templates and retired the undefined state sketch.
- Regenerated ten partial presets through Unity while preserving GUIDs; unified their inventory/application procedure and documented the tested-beta texture-default limitation.
- Repaired UI counter model/presenter/view ownership, stylesheet attachment, runnable scene/PanelSettings, and isolated tests.
- Added copy destinations, optional Git attributes, local-reference/resource checks, and a real naming analyzer fixture.

See [validation evidence](Validation.md) for exact versions and acceptance results. Installation remains
selective; merge configuration and preserve metadata when updating a copied project.
