> How it works: give this URL to your agent, for example "Prepare my Unity project for the CoreCLR
> migration using this document". The agent audits your project, asks which Editor and platforms you
> are targeting, and recommends fixes. You pick which to carry over; nothing changes before you
> confirm, and it works on an isolated branch and reports what it verified. Human overview:
> [readme](README.md).

# CoreCLR migration (agent instructions)

**This guide is work in progress.** It prepares a project for Unity's move from Mono to CoreCLR. This
document is self-contained and experimental: load it for an actual runtime migration, not for normal
starter setup. The selected starter stays on the engine and language profile in
[UnityTechStack.md](../../AgentsInstructions/UnityTechStack/UnityTechStack.md).
**Last verified: October 2026** (sources read 2026-10-12). The roadmap moves often, so re-read the
two linked Unity posts before relying on any date or version below.

## Current evidence versus roadmap

Unity's [October 2026 update](https://discussions.unity.com/t/coreclr-scripting-and-net-update-october-2026/1738338)
announces a Unity 7.0 Alpha CoreCLR Editor initially targeting C# 9 and .NET Standard 2.1. Full .NET 10
and C# 14 remain a staged target with no committed public date. Unity 6.7 experimental players are
separate compatibility options. Do not turn an earlier 6.8 forecast into a baseline guarantee.

The [official upgrade guide](https://discussions.unity.com/t/path-to-coreclr-2026-upgrade-guide/1714279)
is a living source. Compare it with the exact chosen Editor's assemblies and documentation before
writing migration code. Availability of an API in a roadmap does not establish player or platform support.

## Operating rules

- Audit saved project evidence read-only, including on a dirty tree, with existing work preserved.
  Perform confirmed migration execution in an isolated copy or checkout; a branch alone does not
  isolate files from an active Editor. Resolve isolation before execution, without blocking independent audit.
- Use `unity-cli` for compilation, repeated Play, tests, and builds. Resolve packages through
  CLI-invoked Package Manager Client operations. Leave ProjectSettings YAML and `.meta` files untouched.
- Preserve unsaved scenes and the user's other edits. Keep experimental results separate from the
  starter's tested baseline.
- Confirm each API, namespace, and attribute against the **installed** Editor's assemblies before
  using it. Prefer evidence of a supported API over a guessed define; do not invent
  `UNITY_6_8_OR_NEWER`, because engine defines follow actual version numbering.
- Do not promise performance gains. Record a check as **Not verified** when its Editor, platform
  module, or device is missing.

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

## 1. Preflight

This step is the audit input and changes nothing. Read the project, then summarise it in one table
(item, current value):

- Editor version (`ProjectSettings/ProjectVersion.txt`) and the migration Editor to install or use.
- Scripting backend and API Compatibility Level per platform; installed platform modules.
- Every package in `Packages/manifest.json` and `Packages/packages-lock.json`, plus native plugins and
  precompiled assemblies (`.dll`) under `Assets`.
- Assembly definitions, so each finding in step 3 maps to an owning assembly.
- Baseline evidence already available: compile result, EditMode and PlayMode test results, and one
  normal player build on the current Editor, with their revision/freshness. Do not launch these during
  read-only preflight. Missing results are Not verified; propose fresh baseline runs in the confirmation
  list. Without comparable results, later failures cannot be attributed.

**Done:** the table exists, every row has a known value, observed absence, or Not verified reason; baseline results are recorded
or marked Not verified with the reason, and the audit was shown to the user.

## 2. Ask the migration contract

Ask all questions in one batch; the project cannot answer them. Apply the default when the user says
"use defaults"; defaults are recommended defaults that still need the stage 4 confirmation.

| Question | Default |
|---|---|
| Which exact migration Editor (Unity 7.0 Alpha CoreCLR Editor, or a 6.7 experimental player)? | No default; ask, and record the version |
| Which platforms and scripting backends must be tested? | The Editor plus one normal player build on the host platform |
| Isolated checkout or copy ready? | Propose a separate checkout or copy; defer migration execution if declined, while completing independent read-only audit |
| Which dependencies are third-party, and who owns each? | Every non-Unity entry in `packages-lock.json` and every `.dll` |
| Which saved-data fixtures exist (old saves, serialized ScriptableObjects)? | None: persistence checks become Not verified |

**Done:** every question has an answer or a stated default, repeated back to the user, one line each.

## 3. Inventory and apply

Scan owned code first, then dependencies. The scan is the audit: report every finding with its file
and owning assembly, and give each fixable finding a recommendation ID (stage 2) with a default of
skip, so the default outcome is a report and no fix. Apply a fix only for findings the user picked and
confirmed in stage 4, one assembly at a time.

| Area | Find | Resolve | Condition |
|---|---|---|---|
| Mutable statics and events | `static` fields that are not `readonly` or `const`; `static event` declarations; static collections | Reset at a lifecycle boundary chosen after inspecting the installed lifecycle APIs (below); prove the reset across Play and code reload | Fix when picked and confirmed |
| Retained assembly references | `Assembly.Load`, cached `Type` or reflection results, `AppDomain` use | Release at teardown; use `BeforeCodeUnloading` only if the installed Editor exposes it | Fix when picked and confirmed |
| Source-asset runtime writes | ScriptableObject or prefab fields written during Play | Copy to runtime state, or reset on teardown, so the source asset stays clean | Fix when picked and confirmed |
| Owned threads and native resources | `Thread`, `Task.Run`, native handles, `NativeArray`, `ComputeBuffer`, other `IDisposable` owners | Dispose at the owner's lifetime end; observe async errors | Fix when picked and confirmed |
| Dependency framework targets | Each package and `.dll` target framework; native plugins; platform and AOT restrictions | Update, replace, or record as incompatible; never silently drop a dependency | Report always |
| Persisted data | Serializers an unsupported API depends on (`BinaryFormatter` is the usual case) | A format and ownership migration with a versioned save fixture; a JSON rename alone is not a safe old-save migration | Fix when picked and confirmed |
| New lifecycle attributes | Any attribute from the next paragraph | Compile with its required namespace and the exact supported Editor/version gate | When used |

**Lifecycle APIs.** The official guide demonstrates `Unity.Scripting.LifecycleManagement.AfterCodeReloadSerialization`
and discusses `AutoStaticsCleanup` and `BeforeCodeUnloading`. These are not blanket instructions to
annotate every static class: read the installed API, choose per field, and compile. The repository's
[static-state policy](../ProjectSettings/ProjectSettings.md) is an optional pointer for the reload decision.

**Done:** the audit and recommendation list were shown and explicit user confirmation was received before any
change, every finding is listed with its assembly and a disposition (fixed, proposal, or
incompatible), and every attribute used compiles on the target Editor.

## 4. Verify

Run through `unity-cli` against the migration Editor, reading fresh XML and logs:

- Compile with zero errors and no new warnings for owned assemblies.
- EditMode and PlayMode tests; compare counts and ignored tests with the step 1 baseline.
- Enter and exit Play at least twice, then trigger a code reload: owned state resets and a static
  counter or subscriber from the previous run is gone.
- Load every saved-data fixture from step 2 and read back the values.
- Exercise async and resource teardown, and the project's Editor tools.
- Build each agreed player target and run it.

**Manual fallback:** the selected Editor, Package Manager, Test Runner, and build settings.

**Done:** each check above has a result or a Not verified reason, backed by a fresh log or XML file.

## 5. Report

Report in this shape:

```
<One sentence: what now works on which Editor.>

| Component | Status | Evidence |
|---|---|---|
| <assembly, package, or system> | Works / Incompatible / Not verified | <command → result> |

Applied (confirmed): <recommendation IDs, with the change list the user confirmed>
Proposals (not picked): <recommendation IDs, with default and risk>
Measured: <numbers, or "none taken">
Not verified: <check → why>
```

Record incompatible and unverified components explicitly, with measured results. Do not claim a
performance gain unless it was measured on the migration Editor.

**Done:** the report covers every component from step 1, lists confirmed items as applied and
unpicked recommendations as proposals, and no row is blank.

## Rollback

If the migration Editor cannot open the project, or the baseline cannot be restored, stop and revert
the branch. Report the Editor version, the first failing step, and the log lines; leave the user's
original working tree untouched.

## Needs your decision

Put these in a "Needs your decision" block in the report, one bullet each, with the recommendation inline:

- **Which unpicked recommendations to carry over later.** Recommended: keep them as proposals until
  the migration Editor is chosen and the baseline is known.
- **Which migration Editor to target.** Recommended: the Unity 7.0 Alpha CoreCLR Editor for an
  Editor-side trial; a 6.7 experimental player only to probe player compatibility.
- **Whether to accept an incompatible dependency.** Recommended: no; replace it or defer the migration.
- **Whether to merge fixes made for the migration.** Recommended: merge only changes that also pass
  on the current Editor.
