> How it works: give this URL to your agent, for example "Review my Unity project with this document".
> The agent audits the project, detects which reviews apply (animation, physics, UI, audio and so on),
> lets you pick the reviews to run, reports findings with recommendations, and changes nothing
> before you choose which fixes to carry over and confirm. Human overview: [readme](README.md).

# Unity project review (agent instructions)

Run an evidence-based review of a Unity project, either all of it or only the reviews the user picks.
This document is the router: it holds the workflow, the evidence standard, and the menu of **lenses**
(focused checklists in sibling files in this folder). Load only the lenses the user selects; they hold
failure risks, evidence to inspect, and validation. Implementation recipes, tool setup, and API
catalogs belong in skills or official documentation.
**Last verified: October 2026.** Re-check version-sensitive claims in a lens against the installed
Editor's documentation before reporting them.

## Operating rules

- **Read-only by default.** The review inspects and reports. A review request alone does not select
  any fix; unselected recommendations stay proposals.
- Read the project's `AGENTS.md` first. Its choices and the user's scope govern the review. Establish
  the actual engine version, packages, target platform, and owned code before applying a check; report
  a mismatch with a binding project choice and do not silently change the stack.
- Treat examples and recommendations as guidance. A documented no-asmdef policy, composition-time
  injection, or supported legacy UI is not a defect because a generic template prefers another
  approach. Record unresolved conflicts with both sources.
- Preserve concurrent edits and unsaved scenes. Prefer Unity CLI (`unity:unity-cli`) for Editor
  inspection, tests, and builds; discover its commands and target the intended project explicitly.
  Skills are optional accelerators: if one is unavailable, use project tooling and the official
  documentation for the installed Editor. Skill defaults never override project decisions.
- Load a lens by its link in the table below, from the same folder as this document, and only when it
  is selected. These lenses win over any older copies in the project; a project's own audit guide
  runs alongside them only when the user names it. Cross-links between lenses name the owner of a
  check: follow one only when the finding needs it.

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

How the stages map onto the steps below, and the two different picks:
- Steps 1, 3, and 4 are stage 1 (audit).
- Step 2 is a pick of **which reviews to run**: a read-only scope choice, not stage 3.
- Step 5 holds stages 2, 3, and 4: recommend, pick **which fixes to carry over**, and confirm.
- Step 6 applies, and runs only after stage 4.

## 1. Preflight: sources, scope, and what the project contains

Locate the project's `AGENTS.md`, style guide, `.editorconfig`, and setup or audit guides; the
[style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md) in this starter is the default for naming and
organization, and the [setup index](../SetupInstructions/README.md) is the default only for the
structure-and-settings base check. Missing sources leave the affected conformance checks Not
verified; continue independent review rather than substituting remembered rules.

Record the scope (the user's folder, change, or whole project; if unspecified, state the first-party
scope and the exclusions), the base revision for a change review, starting branch/commit, and an
inventory of staged, unstaged, and untracked files (or the available non-Git source identity). Record
engine and package versions, platform, and selected stack. First-party means everything under `Assets` except
vendor, sample, and generated folders (include project folders such as `Assets/Settings` and
`Editor`), plus embedded packages the team owns; read the folder names and `AGENTS.md` to decide, and
state the result. Check whether an Editor has the project open (`Temp/UnityLockfile`) and say so,
because unsaved scenes must be preserved. Ask only when an unresolved choice materially changes the
review.

Then detect what the project contains, using the signals in the [lens table](#2-choose-the-reviews).
Apply the scope's exclusions to detection as well: count first-party content only (vendor packages,
samples, and generated folders excluded), and state the raw and first-party counts when they differ.
Search by file listing, manifest, and text search first, quoting paths (project folders contain
spaces; use `find -print0` or `grep -r`). If `unity-cli` is unavailable or the user forbids it,
inventory components from saved scenes and prefabs by YAML class ID (enough for detection; use script
GUIDs only to identify a specific component type) instead, and record the live checks Not verified. Record for each lens the evidence you found, or "nothing
detected".

**Done:** scope, versions, and the source documents are recorded, and every lens has detection
evidence or "nothing detected", and detected systems without a matching lens are listed Outside coverage.

## 2. Choose the reviews

Show the user one menu, headed by the scope, exclusions, engine and package versions, and the binding
project choices from `AGENTS.md` that bear on the lenses, one line each. Label every lens:
- **Recommended**: a strong signal, meaning a component, asset, or API used in first-party runtime
  content or code.
- **Optional**: a weak or partial signal (found only in tools, tests, or imported model prefabs, or one
  lone asset), or a strong signal where a documented project policy limits the lens.
- **Not detected**: no signal. Record it as Not applicable in the report.

List the base checks and the integrity pass as included, each lens with its evidence. The integrity pass is Part A of the Editor tooling file and
Part B is a separate lens. Offer these shortcuts and accept any custom subset:

| Shortcut | Runs |
|---|---|
| Quick health check | Integrity pass, base checks, Performance, Scenes and lifecycle, Assets and memory |
| Full review | Integrity pass, base checks, and every lens marked Recommended |
| Custom | Exactly the lenses the user names, including a Not detected one when they insist |

A narrow request (a button edit, a single subsystem) selects only the behavior it touches and its
dependencies, so do not load the whole folder. If the user already named the lenses, confirm the list
and go on. If no one can answer the menu (a non-interactive session), run the Quick health check,
which is read-only, and stop after stage 2.

| Lens | Detect (load only if the project has) | Related skills (optional) |
|---|---|---|
| **Integrity pass**: [Editor tooling, Part A](UnityEditorToolingInstructions.md) | Always on for a whole-project review and for any change touching `.meta` files, serialized assets, or renamed fields | `unity:unity-cli` |
| [Performance](UnityPerformanceOptimizationInstructions.md) | Owned runtime C# code | `unity-project-review`, `unity:optimize-web` |
| [Rendering correctness](UnityRenderingInstructions.md) | Owned `ScriptableRendererFeature`/`ScriptableRenderPass` or Render Graph code, custom `.shader`/`.shadergraph` assets, or a configured camera stack; a pipeline package alone is only Optional | `validate-urp-render-graph-renderer-feature` (URP Render Graph only) |
| [Assets and memory](UnityAssetsAndMemoryInstructions.md) | Imported assets; `com.unity.addressables` for the Addressables rows | `unity:optimize-audio`, `unity:manage-sprite-atlas` |
| [Scenes and lifecycle](UnityScenesAndLifecycleInstructions.md) | Scenes or MonoBehaviours; async code (`Awaitable`, `Task`, `StartCoroutine`; `IEnumerator` alone is not a signal) | `unity:unity-cli`, `unity-project-review` |
| [Design](UnityDesignPatternsInstructions.md) | Owned C# with commands, services, or shared state (findings are proposals unless a rejected or repeated operation corrupts state) | `unity-project-review` |
| [Persistence](UnityPersistenceInstructions.md) | Save or load code in first-party runtime scripts (not Editor tools): writes under `persistentDataPath`, `PlayerPrefs`, settings sliders; `JsonUtility` or other file I/O alone is a weak signal | Project save tooling |
| [UI Toolkit](UnityUIToolkitInstructions.md) | `.uxml` or `.uss` files, `UIDocument` or `PanelRenderer` components, `PanelSettings` assets, `UnityEngine.UIElements` usage in first-party code | `unity:ui`, `unity:ui-uitk` |
| [uGUI](UnityUGUIInstructions.md) | `Canvas` (YAML class 223) or `EventSystem` in first-party scenes or prefabs, or `using UnityEngine.UI;` in scripts (not `UnityEngine.UIElements`) | `unity:ui`, `unity:ui-ugui`, `unity:optimize-text-mesh-pro` |
| [Input](UnityInputSystemInstructions.md) | `com.unity.inputsystem`, `.inputactions` assets, or `UnityEngine.InputSystem` usage | `unity:unity-cli` |
| [Physics](UnityPhysicsInstructions.md) | In first-party content (vendor colliders do not count). Strong: `Rigidbody` (YAML class 54) or `CharacterController` (143), `OnCollision*`/`OnTrigger*`, `Physics.Raycast`/`Physics.Overlap*` in runtime code. Weak: collider components alone (`BoxCollider` 65, `MeshCollider` 64, `SphereCollider` 135, `CapsuleCollider` 136) or a `Collider` type used as data; 3D PhysX only | `unity:physics-3d-collision` |
| [Animation](UnityAnimationInstructions.md) | `.controller` or `.overrideController` assets and Animator API use in runtime code; `Animator` components (class 95) only on imported model prefabs are a weak signal | `unity:unity-cli` |
| [Audio](UnityAudioInstructions.md) | `.mixer` assets, `AudioSource` components (class 82), `AudioMixer` or `AudioSource` use in runtime code, volume sliders; one lone signal is Optional, two or more are Recommended | `unity:audio-setup-mixers`, `unity:optimize-audio` |
| [Assemblies](UnityAssemblyDefinitionsInstructions.md) | First-party `.asmdef` or `.asmref` files, or test code (for the test-inclusion row); a project that documents relying on the predefined assemblies is Optional | `unity-project-review` |
| [Testing](UnityTestingInstructions.md) | Test code: `com.unity.test-framework` plus `[Test]`/`[UnityTest]` (not scene or documentation folders named Test); a whole-project review also reports "no tests" as a scope fact | `unity:unity-cli` |
| [Editor tooling, Part B](UnityEditorToolingInstructions.md#tool-authoring) | Owned `Editor/` code with the attributes `[MenuItem`, `[InitializeOnLoad`, or `[CustomEditor`, or editor base classes, plus migration tools (match the attribute, not the word) | `unity:unity-cli`, `unity:ui-uitk`, `unity:ui-imgui` |

### Detected systems outside lens coverage

During detection, also inventory the following signals within the same first-party scope. Record
**Outside coverage** with evidence and consequence, rather than treating an uncovered system as
Not applicable or reviewed by a neighboring lens. Package presence alone is a weak signal: separate
installed capability from first-party usage. This inventory does not add or load a new lens.

| System | Detection evidence | Review limit |
|---|---|---|
| Navigation | AI Navigation package, NavMesh data/surfaces, `NavMeshAgent` or `NavMesh` usage | No dedicated pathfinding/bake/link correctness lens |
| Networking | Netcode, transport or other networking packages plus owned RPC/session/replication code | No authority, replication, transport, or multiplayer security lens |
| Physics2D | `Rigidbody2D`, `Collider2D`, `Physics2D`, or 2D callback usage | The Physics lens covers 3D PhysX only |
| DOTS | Entities/Unity Physics packages plus owned ECS/system/job usage | No ECS world/system-order or DOTS Physics lens; generic ownership/cost checks cover only their stated rows |
| Other first-party systems | Content/code with no matching lens, found while inventorying the project | Name the system and the absent review; do not infer exhaustive coverage from the menu |

For each detected uncovered system, list the owning files/assets, applicable generic checks, and the
specific specialist work not performed. Offer a separate scoped review against installed official
docs when the user wants it. **Full review** means all selected applicable lenses, not all possible
subsystem risks. Include this coverage boundary in the menu and final report.

Physics2D and DOTS projects are outside the Physics lens; use their matching official documentation. [Debugging](UnityDebuggingInstructions.md) is not an audit lens. It is the
[diagnose mode](#diagnose-a-reported-defect) for a user-reported symptom.

**Done:** the user has picked, or confirmed a shortcut for, the reviews to run, and the list is
recorded with a reason for every lens left out.

## 3. Run the selected reviews

Run the integrity pass first, because asset identity comes before conventions. Inspect vendor metadata
only for database-wide integrity, and exclude vendor and generated source from style review unless
the user scoped it in.

These base checks have no lens of their own; run them in a whole-project review and in the Quick
health check:

| Check family | Source of truth | Evidence to inspect |
|---|---|---|
| Naming and formatting | [Style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md) and project `.editorconfig` | Prefix and casing exceptions, modifiers, fields and properties, braces, actual code |
| Class organization | Project and style guide | Member order, MonoBehaviour and file identity, approved region usage |
| API and stack compatibility | Project tech stack and installed source or official docs | Actual versions, obsolete API availability, selected input, UI, and pipeline |
| Structure and settings | Project rules, [folder review](../FolderStructure/ReviewFolders.md), [project settings](../ProjectSettings/ProjectSettings.md) | Intended folder and settings policy versus actual state |

⚠️ Every search pattern is a candidate. Read the enclosing code and the callers, and honor documented
project choices. Do not report every lambda, every static, a missing asmdef, any `Resources` folder,
or a version-independent API ban list as a finding. Confirm the actual failure or the binding rule.

Then load each selected lens, one at a time, and record **Checked**, **Finding**, **Not applicable**,
or **Not verified** for each of its rows. State the sample for every lens, and how many files you read
out of how many exist. Cover every file when the check is a search or a count. For rows that need
reading, start with the largest, most recently changed (`git log --since` churn), and highest-risk
owned files.

**Done:** every selected lens and base check has an outcome for each row, with the inspected scope or
sample stated.

## 4. Fill live and test evidence gaps

Use `unity-cli` for Editor inspection and the project's runner for authorized tests; follow any
required test-runner delegation. Read-only queries of the current state do not need repeated
permission when already authorized. Preserve dirty scenes; use saved-asset inspection or isolated
scenes for checks that need different content. Obtain new authorization before any additional
disruptive live action.

If the Editor, runner, device, or build is unavailable, record the specific checks **Not verified**
and continue static work. In a static-only run, state each lens's live-only rows once as **Not
verified (live)** with the checks to run later, instead of repeating it row by row. Parse fresh test
results and logs, and distinguish failures, exclusions, and not-run tests.

For each runtime evidence collection, record scene/content identity, Play state, compilation/reload
state, activity (gameplay, script recompilation, preview, or test fixture), log cursor or timestamp
range, and source revision plus relevant dirty-file state. Record shared context once and differences
per finding. Retain supplied or measured context as known; mark only unavailable fields Not verified.
An exception establishes what occurred in that
context; check whether it was expected by a test or preview before calling it a product defect.
Its cause remains a hypothesis until supporting evidence distinguishes alternatives.

- ❌ Do not call an unopened prefab correct from source alone.
- ❌ Do not claim a live repair is saved.

**Done:** each live or test check has fresh evidence and its collection context, or is listed Not
verified with its reason and any unavailable context.

## 5. Report and recommend

Separate confirmed defects, measured costs, convention drift, and design proposals. Each finding
meets the [evidence standard](#evidence-standard). Group one repeated cause with counts and
representative locations, and list every affected duplicate-GUID pair. Record conflicts and limits,
including inspected samples, systems Outside coverage, and whether the live, test, and build checks ran.

Put material observations encountered outside selected lenses in **Incidental observations**, with
location, evidence, consequence, and the narrow inspection performed. Inspect only enough to explain
the observation; offer further investigation as a separate scope choice. An incidental observation
does not mark that lens reviewed or authorize a fix.

Then turn the findings into the numbered recommendations of stage 2: for each, the smallest useful
fix, intended outcome, checkable acceptance condition, validation method and known constraints, why
it matters, its risk, and a default of do or skip. Let the user pick any subset (stage 3), then apply
the shared confirmation rules to its exact changes (stage 4). Ask whether
to save the report as a file and where; saving is itself a change and waits for stage 4.

**Done:** the report distinguishes selected-lens findings from incidental observations, every
recommendation has an acceptance condition and validation method, and the user's selection and
confirmation status are explicit; nothing was written before authorization.

## 6. Apply confirmed fixes

Apply only the items confirmed in stage 4. Before editing each item's target files, re-read them and
check that its supporting evidence and approved scope still apply. Recheck affected source before
validation and record the state actually validated. A branch/commit change or relevant dirty edit
requires reassessment of affected findings; unrelated edits do not restart the audit. Mark explicitly
assigned work in another chat **Externally owned** and exclude it from edits unless handed over;
a dirty file alone does not establish ownership. Preserve concurrent changes and re-confirm changed
scope under the shared contract.

Selected fixes preserve serialized identity and follow the matching implementation skill or project
workflow. Report each selected item with separate implementation and acceptance results:

| Item | Implemented change | Acceptance result | Remaining validation |
|---|---|---|---|
| R1 | Missing-session guard added | Not verified | Recompile during Play and exercise callbacks |

Run relevant validation against the agreed acceptance condition. Compilation establishes compatibility,
not gameplay recovery. An item can be implemented while its behavior remains Not verified; close it
as resolved only when its acceptance conditions pass. Name missing checks and their tooling,
authorization, or environment constraints. Attribute results to the actual source state; mixed-revision
validation cannot establish that a single commit passed.

**Done:** every selected item records its implementation state, acceptance evidence or Not verified
with the missing check and constraint, and validated source state where applicable; externally owned
items are identified, and every unpicked recommendation remains a proposal. Unverified acceptance
keeps the item open even when the implementation work is done.

## Diagnose a reported defect

When the user hands over a symptom (a bug, a build-only failure, a repeated-Play problem) instead of a
review scope, use [the diagnosis guide](UnityDebuggingInstructions.md): capture the failing context,
route the symptom to the owning lens above, and follow its reproduce, hypothesize, probe, fix, and
regression-test loop. The same read-only and confirm-before-change rules apply.

## Evidence standard

A search hit is a candidate. Read the enclosing code, callers, ownership, and applicable settings
before reporting it. Follow per-frame helper calls; inspect release, cancellation, and failure paths.
Exclude generated and vendor code from style review unless scoped in. Vendor metadata may still
matter to a project-wide GUID integrity check.

For each selected check family or lens, record **Checked**, **Finding**, **Not applicable**, or
**Not verified**. State the inspected scope or sample and any missing evidence.

⚠️ Static inspection does not establish runtime behavior, target-device performance, or correct
saved scene and prefab wiring.

A finding needs:
- **Location** and **trigger**
- **Observed evidence** and **consequence**; runtime observations carry the collection context from step 4
- **Cause assessment**, for diagnostic findings: established, suspected, or unknown, with supporting evidence
- **Governing source**: a project rule or a technical source
- **Smallest useful fix**, **intended outcome**, and **checkable acceptance condition**
- **Validation method** and **known constraints**

A reproduced runtime failure is not required for an inspected static defect, convention drift, or
design proposal; label the finding's evidence and category accurately. For diagnostic fixes,
distinguish containment from recovery: suppressing an invalid callback and restoring a running game
after recompilation have different acceptance conditions. A symptom disappearing alone does not
establish the proposed cause.

Rank confirmed corruption, data loss, bugs, and leaks ahead of measured performance problems; label
convention drift and design proposals separately. Combine repeated instances of one cause while
preserving affected locations.

The review is complete when every selected check family and lens has an outcome, each finding has
inspected evidence, and unverified work is explicit. A clean static review means no confirmed findings
in that scope; it does not imply unperformed runtime checks passed.

## Maintenance

- ✅ Keep one owner per check: general frame cost in Performance, rendering correctness in Rendering, resource residency in Assets, async
  lifetime and destroyed-object checks in Scenes, command ownership in Design, persisted state in
  Persistence, UI and world input arbitration in Input, test inclusion in Assemblies. Other lenses
  link there and add only subsystem-specific failure cases.
- ✅ Keep each lens focused on one recurring risk. Add a lens only for a distinct recurring risk with a
  detection signal and a clear loading condition; update the table above, the readme, and `AGENTS.md`
  together.
- ✅ Keep existing lens filenames stable for consumers.
- ✅ Verify version-sensitive claims against engine or package source or official Unity docs, link
  official docs by unversioned URL, and keep each lens's `Last verified` line current.
- ❌ Keep tutorial examples, historical project class names, and review logs outside this folder.
