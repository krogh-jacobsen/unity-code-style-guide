# Project settings

**Prerequisite:** exact Editor, platforms/backend, existing settings, and selected stack are known.
Use Unity CLI to read values before mutation and verify them after saving. Values below express a
safe starting policy, not universal performance claims.

## Baseline

| Setting | Desired outcome | Verification |
|---|---|---|
| Asset serialization | Force Text | Read EditorSettings; inspect saved assets |
| Asset identity | Visible metadata, preserved GUIDs | Metadata exists and is committed with assets |
| Input handling | Selected Input System integration | Read PlayerSettings; exercise a real action/UI click |
| API compatibility | Selected release's .NET Standard 2.1 baseline | Read target PlayerSettings; compile |
| Rendering | Compatible URP asset/renderer assigned | Read Graphics/Quality settings; render a scene |
| Scene reload | Enabled | Read Enter Play Mode settings; second Play returns to intended state |
| Domain/code reload | Selected Editor's supported default | Record actual value; validate mutable statics/subscribers |
| Package graph | Manifest and lockfile committed | Read completed resolved list and source-control diff |

Do not rewrite working settings merely because the imported starter differs. Preserve existing
occupied layer slots, tags, quality entries, and pipeline assets. Report an actual policy conflict
before selecting a migration outside the user's scope.

## Explicit options

| Option | Choose when | Completion check |
|---|---|---|
| Disable domain reload | Supported faster iteration with explicit session reset | Two Plays have clean mutable state and subscribers |
| Disable scene reload | Project deliberately supports object-state restoration | Repeated Plays plus enable/disable tests pass |
| asmdefs | Concrete compile/dependency boundary needed | Editor/player compile; tests discover in isolated assemblies |
| Quality tiers / volumes | Target hardware needs distinct budgets | Each selected tier works in a representative device build |
| Tags / layers / sorting | Gameplay actually consumes them | Add missing names only; preserve existing slots; test collision/render ordering |
| Backend / stripping | Target platform and dependencies support it | Representative normal player build, AOT/reflection checks as applicable |
| Burst/jobs | Actual workload uses supported facilities | Compile/run selected job; do not assume a separate package on newer releases |
| Frame cap / vSync | Platform's intended pacing established | Measure frame pacing on the target |

Development and release profiles must describe actual differences. Mono is not available on every
platform; IL2CPP is not universally a faster runtime. Preserve the chosen backend until a compatible
alternative is selected and tested. Build profiles and supported per-platform settings vary by Editor.

## Machine-local preferences

Auto Refresh, worker count, and script-change-during-Play preferences are user/machine choices.
Recommend refresh outside Play and deferred recompilation if useful; do not pretend preferences are
portable project settings or alter another person's workstation as part of copying the starter.
Remove unused modules only when explicitly requested, not as project setup cleanup.

## CLI/manual application

Inspect CLI help and `unity command --project-path <target> --format json`; use supported commands or
CLI-invoked Editor scripts for EditorSettings, PlayerSettings, QualitySettings, and SerializedObject
operations. Save affected assets only. Use the Package Manager Client API for packages. Manual fallback:
Project Settings and Preferences/Settings for the appropriate ownership.

**Done:** selected values read back correctly, saved scene/pipeline references survive reopening,
repeated Play matches the selected reload contract, and an agreed platform build completes. Record
unperformed device/backend checks as Not verified. Source control setup is in
[the installation guide](../README.md#how-to-install) and [Git attributes](../EditorConfig/README.md#git-attributes).
