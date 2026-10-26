> How it works: give this URL to your agent, for example "Check which of these packages my Unity
> project is missing and install the ones I pick". The agent audits your manifest and code first,
> recommends only the packages your project needs, lets you pick, and changes nothing before you
> confirm the exact list. Human overview: [readme](README.md).

# Install packages (agent instructions)

Review which Unity packages a project has, recommend the missing ones it needs, and install only the
ones the user picks and confirms. This document is self-contained. **Last verified: October 2026**
(core package list checked against the 6000.6 and 6000.7 manuals).

## Operating rules

- Never remove, downgrade, or replace a package. Report packages you would remove as findings; the
  user must ask for a removal explicitly, and then it is a separate recommendation.
- Install with the Package Manager Client API (`UnityEditor.PackageManager.Client`), which resolves
  dependencies. Do not hand-edit `Packages/manifest.json` or `packages-lock.json` unless the user
  explicitly asks for that after you have explained the risk. A lockfile that looks hand-written or
  inconsistent is a finding to report; the Editor normalises it on open, so do not repair it.
- Treat a package from the project's own `Packages/` folder, a `file:` or git reference, a scoped
  registry, or a pre-release or experimental version already in the manifest as the user's choice.
  Report it; do not change it.
- Do not change settings a package adds, for example Active Input Handling after installing the
  Input System. Report the follow-up and point to the
  [project settings guide](../ProjectSettings/ProjectSettings.md).
- Installing a package proves it resolved, not that the project uses it correctly. Report what you
  checked and what you could not (**Not verified**).

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

Here, steps 1 to 3 are stages 1 and 2 (audit and recommend), step 4 holds stages 3 and 4 (choose and
confirm), and steps 5 and 6 run only for confirmed items. Stage 2 also lists the step 4 questions with
their defaults, so a non-interactive run still shows them. Findings that propose no change (a note, a
fact, a follow-up) go in the report as notes; only a proposed change gets a numbered recommendation.
When nothing differs, report "no change needed" for each package and stop: there is nothing to pick.

## 1. Preflight

Identify one Unity project (it contains `Assets` and `ProjectSettings/ProjectVersion.txt`). Read only
files; do not open the project in an Editor to audit it, because that imports assets and can rewrite
`manifest.json`. Record:

- The Editor version from `ProjectSettings/ProjectVersion.txt`. A `Temp/UnityLockfile` means an
  Editor has the project open, unless a crash left it behind (look for `mono_crash.*.json` in the
  project root). Treat it as open, say so, and let the user correct you in step 4.
- Every `Packages/manifest.json` dependency, and for each its entry in `Packages/packages-lock.json`:
  `version`, `source`, and `depth`. `depth` 0 is a direct dependency; a higher depth is present only
  because another package needs it. Also note scoped registries, `file:` or git references, and
  pre-release (`-pre`) or experimental (`-exp`) versions.
- The owned scope. Owned code is everything under `Assets` that the project authored, including
  `Editor` folders and test code, whether or not it has an assembly definition. Vendor code is
  `3rdPartyAssets`-style folders, `Plugins`, `Samples`, `TextMesh Pro`, imported asset-store
  folders, and generated folders. If a folder is unclear, count it and say so. Report evidence as
  "raw / owned" counts, for example `22 / 13`.
- Source-control state (uncommitted changes to `Packages/`).

**Done:** the Editor version and state, every direct dependency with its source, and the owned scope
are recorded, and nothing was written.

## 2. Decide how each package is versioned

Do this for every package you will mention, before any version logic.

| Package source | How to recognise it | Version rule |
|---|---|---|
| **Core package** | `source` is `builtin` in the lockfile. The lockfile wins. For a package that is not installed, the id is on the Core packages page for the Editor version: `https://docs.unity3d.com/<major.minor>/Documentation/Manual/pack-core.html`, where `<major.minor>` is the first two parts of the Editor version (`6000.0` for `6000.0.30f1`). If that page does not exist for a beta, use `https://docs.unity3d.com/Manual/pack-core.html` and say so. | Fixed to the Editor version. Unity documents that you cannot pick a version for a core package in the Package Manager window or API, so do not pin `id@version` and do not use registry versions. |
| **Registry package** | `source` is `registry`, or the id is not a core package. | Use `versions.recommended` from `Client.Search` when it is non-empty, otherwise `versions.latestCompatible`. Both are available only through the Editor API; a bare `Client.Add("<id>")` installs the latest compatible released version. Before the Editor can run, report "resolved at install time" and show the registry's latest only as a hint. Never pick a pre-release or experimental version unless the user asks. |

A direct registry lookup (`https://packages.unity.com/<id>`) lists versions but not compatibility
with this Editor, so use it only to confirm that an id exists. For a core package it can show a
version that differs from the Editor's, and that version must not be used.

Whether an id is a core package depends on the Editor version. A package that is a registry package in
an older Editor can be a core package in a newer one, so check this project's Editor version instead
of assuming.

**Done:** every package named in the report has a source class and a version rule.

## 3. Choose what to recommend

Recommend a package only when the project's own evidence calls for it. Labels: **Already direct**
(evidence or not, the package is a direct dependency: no change), **Recommended** (the evidence is
present and the package is not a direct dependency), **Optional** (the user asked for the capability,
or the evidence is weak: a single `.inputactions` asset with no code, one reference in a comment, or
a signal only in unclear folders), **Not detected** (no owned evidence; do not recommend). If the
user gave a list of extra packages, offer those as candidates and verify each id exists; otherwise
skip this.

Search owned code for the namespace anywhere, not only in `using` lines: a fully qualified
`Unity.Cinemachine.CinemachineBrain` counts.

| Package | Recommended when | Notes |
|---|---|---|
| Test Framework `com.unity.test-framework` | Owned code uses `NUnit.Framework`, `[Test]`, or `[UnityTest]` and the package is not direct. Optional when the user wants tests. | An assembly definition is not required: Editor tests compile into the project's Editor assembly. Installing creates no tests; the [testing guide](../Testing/TestingInstructions.md) covers assemblies. Report "installed, tests without a test assembly" as a fact, not a defect. |
| Cinemachine `com.unity.cinemachine` | Owned code uses `Unity.Cinemachine` (Cinemachine 3) and the package is not direct. Optional when the user wants a camera rig. | Code using the `Cinemachine` namespace or `CinemachineVirtualCamera` is Cinemachine 2, which a registry install of the latest version would break. Recommend nothing; report it and ask the user whether to stay on 2.x (pin an explicit 2.x version) or migrate to 3 with Unity's [upgrade guide](https://docs.unity3d.com/Packages/com.unity.cinemachine@3.1/manual/CinemachineUpgradeFrom2.html). Default: skip. |
| Input System `com.unity.inputsystem` | Owned code uses `UnityEngine.InputSystem` and the package is not direct. An `.inputactions` asset alone is Optional. | Does not change Active Input Handling. That change needs an Editor restart and belongs to the [project settings guide](../ProjectSettings/ProjectSettings.md). |
| Addressables `com.unity.addressables` | Owned code uses `UnityEngine.AddressableAssets`, or Addressables settings exist in owned folders, and the package is not direct. Optional when the user selects it. | A registry package: apply the registry version rule. |
| Another package the user names | The user asks for it. | Confirm the id exists and its source class (step 2), and read its manual page for setup that installing does not do. |

A package that is only a transitive dependency (`depth` above 0) and is used by owned code is a
low-risk recommendation to make it a direct dependency; otherwise no change. If the code resolves a
package's namespace from a copy bundled inside a vendor folder, report it and recommend nothing:
installing the package could create duplicate types.

**Done:** every candidate is labelled with its evidence and its raw / owned counts.

## 4. Ask and select

Ask in one batch. Each default is the recommendation for that question; it takes effect only after
the stage 4 confirmation, even when the user says "use defaults".

| Question | Default |
|---|---|
| Which recommended or optional packages to install? | Only the Recommended ones that are low risk. A package with a medium or high risk, such as Cinemachine 2, is skipped until the user decides |
| Is an Editor open on this project now? | The answer from step 1; ask when `Temp/UnityLockfile` exists |
| Allow a pre-release version of a registry package? | No |
| Keep the helper script after the run? | No: remove it (see step 5) |

**Done:** the user's picks are recorded, and the confirm list names each package id, its source class,
and the version rule. A registry version is resolved at install time; the user can pin `id@version`
for a registry package, and the confirm list says which.

## 5. Install

Run only for confirmed packages. Pick the first route that works and say which you used. To make a
core or transitive package a direct dependency, call `Client.Add("<id>")` with no version; Unity
resolves the Editor's version, which step 6 checks.

1. **Editor open with a command channel** (Unity CLI or MCP execution): call
   `Client.AddAndRemove(packagesToAdd, packagesToRemove: null)` once for the whole set. Requests
   complete on later Editor update ticks, so poll `IsCompleted` instead of blocking.
2. **Editor closed:** use a short Editor-only helper under `Assets/Editor/ProjectBootstrap/` that runs
   the same call and ends with `EditorApplication.Exit(code)`. Launch the Editor binary directly in
   `-batchmode` **without** `-quit` (the `unity run` default adds `-quit`, which ends the Editor
   before the request finishes). The confirm list names the helper; remove it and its `.meta` after
   the run unless the user kept it.
3. **Neither is available:** stop and give the user the exact ids and the Package Manager steps.

An install triggers a script reload, so with the Editor open ask the user to save their scenes first.

**Done:** the Client request finished with a success status for every confirmed package, or the
failure message is in the report and nothing partial was left unreported.

## 6. Verify and report

- `Packages/packages-lock.json` lists each installed id at `depth` 0, with the version and `source`
  you expected. For a core package the version is the Editor's.
- The `manifest.json` diff contains exactly the confirmed ids, and no other dependency changed.
- Wait for the compile and domain reload to finish, then read the Console for compile errors that
  came from the install. When no Editor ran, mark compilation **Not verified**.
- Tell the user to commit `Packages/manifest.json` and `Packages/packages-lock.json`.

Report: what was already in place, what you installed (id, source, version, route used), what the
user skipped, what you could not verify, and any follow-up the package needs that you did not do.
Anything that waits on the user goes in a "Needs your decision" block.

**Done:** every confirmed package has a verified lockfile entry, and every recommendation is marked
installed, skipped, or failed.

## References

- [Core packages](https://docs.unity3d.com/Manual/pack-core.html) and
  [package states](https://docs.unity3d.com/Manual/upm-lifecycle.html)
- [`Client.Add`](https://docs.unity3d.com/ScriptReference/PackageManager.Client.Add.html) and
  [`VersionsInfo`](https://docs.unity3d.com/ScriptReference/PackageManager.VersionsInfo.html)
- [Upgrade to Unity 6.6](https://docs.unity.com/en-us/engine/7000.0/manual/upgrade-guides/upgrade-guide-unity66):
  Cinemachine became a core package, and Cinemachine 2 projects move to Cinemachine 3.
