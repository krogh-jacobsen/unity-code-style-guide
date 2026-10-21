# Change log

## 2026-10-21 — Agent-ready build settings

- Added `LLMInstructions/BuildSettings/` with agent documents for desktop (Windows/macOS) and mobile (Android/iOS) setup, plus a human `readme.md` covering the key decisions and VR, Web, and console carry-over.
- Rewrote the desktop guide as an executable flow: preflight, support-contract questions, settings table with Editor API names, build profiles and CLI, verification, and a required report. Added Intel Mac deprecation, Windows Arm64 limits, D3D12 fallback, PSO warm-up, and Windows toolchain guidance.
- Added a top-level `LLMInstructions/readme.md` topic index and a "Maintaining this repository" section in `AGENTS.md` defining the agent-document plus readme convention; repaired seven stale links in `AGENTS.md`.
- Restructured `LLMInstructions/FolderStructure/` into a self-contained agent document (`SetupFolders.md`) and a human `readme.md`; the former `FolderStructure.md` policy now lives in those two files. Repointed the root README and setup index to the new paths.
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
