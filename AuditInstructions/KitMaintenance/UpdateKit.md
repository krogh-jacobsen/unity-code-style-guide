> How it works: give this URL to your agent with "Update my installed Unity starter kit".
> It audits differences, recommends a subset, and applies only confirmed merges. Human overview: [README](README.md).

# Update an installed starter kit

## Operating rules

- Work from immutable old and new source revisions plus the destination's actual files. Treat local
  conventions, importer values, and selected packages as deliberate until reviewed.
- Preserve concurrent edits and dirty scenes. Keep recovery copies outside Assets; restore only
  this operation's changes. Use Editor APIs for imported assets and preserve destination GUIDs.
- This workflow updates selected kit material. Engine/package upgrades and publishing are separate
  tasks. Use installed tooling; unavailable validation remains Not verified.

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
   and obtain explicit user authorization before making them, including saving the report. Give
   each change its undo: a commit checkpoint, a backup copy of a settings file, a log of moves, or
   the trash instead of a permanent delete.
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

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. Any
change outside the confirmed list, however small or obviously helpful (an extra `.gitkeep`, a
related setting), is a new recommendation: it returns to stage 3 before it is made. Noting it in a
report is not confirmation.

## 1. Preflight the installation

Read project instructions, version/package records, working-tree state, selected resources, Editor
state, and `Documentation/UnityStarterKit-installation.json` if present. Resolve source snapshots from
one old commit and one proposed new commit. Locate the reference snapshot (default:
`Documentation/UnityStarterKit`) and active copies such as root AGENTS.md, .editorconfig, templates,
and presets. Resolve any missing source or path before planning replacement.

Compare baseline → local and baseline → upstream for every selected file. Classify each as unchanged,
upstream-only, local-only, overlapping, added, removed, local fork, or unknown baseline. When kit
material is present but no installation record names its source revision (an adapted copy), run
step 2 first and classify against the reconstructed baseline. Include moved files and
inbound links. Match imported resources by destination GUID as well as path. An upstream deletion is
not automatic permission to delete a local asset.

**Done:** every selected destination has a classification, source revisions, and recovery/validation needs.

## 2. Reconstruct a missing baseline

Run this step, read-only, when kit material sits in the project without a recorded source revision:
files copied by hand, renamed folders (for example lenses under `Docs/AgentGuides/AuditGuides/`),
or a record that lacks the revision for a group. Recognize kit files by name, by the
`> How it works:` opening, or by the project's own mention of the kit. Without a baseline every file
classifies as unknown, and the copy can never be updated safely, so reconstruct one.

1. **Inventory the copy.** List each local file and its upstream candidates. Upstream paths move
   between revisions, so match on file name across the upstream history (`git ls-tree -r <commit>`),
   not on the current path. For a name that occurs in several upstream folders (`README.md`), compare
   every candidate and keep the best match.
2. **Bound the search.** If the project's history shows when the copy arrived
   (`git log --diff-filter=A --format=%cs -- <copied path>`), upstream commits after that date
   cannot be the source; skip them.
3. **Score every candidate commit.** For each upstream commit on the default branch
   (`git rev-list --first-parent <default branch>`), compute a line similarity between each local
   file and its upstream candidate at that commit (for example Python
   `difflib.SequenceMatcher(None, upstream_lines, local_lines, autojunk=False).ratio()`; cache by
   blob ID, since most files are unchanged between commits). The baseline is the commit with the
   highest mean similarity over the matched files. Commits with identical content tie; record the
   newest commit of the tie. When one file's best commit differs from the group's and scores
   clearly higher there, record a per-file baseline.
4. **Classify each file against its baseline.** These thresholds are starting values; report the
   scores so the user can move them.

| Similarity to baseline | Class | Update method |
|---|---|---|
| 0.95 or more | Near-pristine | Normal three-way merge; local edits are small |
| 0.60 to 0.95 | Adapted | Three-way merge, each overlapping hunk reviewed |
| Below 0.60, or no upstream match | Local fork | No automatic merge. Upstream changes since the baseline become proposals read by hand; a file with no upstream match is a local addition |

5. **Recommend a layout that stays updatable.** For forks and heavily adapted files, recommend the
   overlay pattern: a pinned, unmodified snapshot of upstream at one revision, plus one short local
   overrides file (for example `LocalOverrides.md` beside the snapshot) that lists each deliberate
   deviation as a rule with its reason, referenced from `AGENTS.md` as "the snapshot governs except
   where the overrides file says otherwise". Future updates then replace the snapshot and only the
   overrides need review. A fork the user keeps stays a declared fork that updates skip.
6. **Recommend the installation record.** Propose writing `Documentation/UnityStarterKit-installation.json`
   (step 4) with the reconstructed revision, the method and scores, and every fork, so the next update
   starts from a known baseline:

```json
{
  "installed_revision": "1bceb25",
  "baseline_method": "reconstructed: mean line similarity 0.99 over 17 files; copy added 2026-10-12",
  "snapshot_path": "Docs/AgentGuides/AuditGuides",
  "local_forks": [ { "path": "Docs/AgentGuides/AuditGuides/ProjectReview.md", "reason": "project router" } ]
}
```

Report a reconstructed baseline as reconstructed, with its scores, never as a recorded fact.

**Done:** every copied file has a baseline commit (or "no upstream match"), a similarity score, and a
class, and the overlay and installation-record recommendations are listed for step 3.

## 3. Ask and recommend

Ask one batch: target revision, groups to update, local decisions to retain, and acceptable validation
scope. Defaults: retain local decisions; merge upstream-only documentation; skip overlapping or
unknown-baseline changes until individually resolved; offer local forks upstream changes as proposals
only, plus the overlay conversion; preserve removed resources pending reference review.
For each recommendation state the exact source/destination, merge strategy, expected values, commands,
risk, and default. A missing old snapshot means manual comparison, never an assumed clean baseline.

**Done:** all differences have a recommendation or no-change result, and the exact selected edits are confirmed.

## 4. Apply selected merges

| Material | Target | How to set it | Condition |
|---|---|---|---|
| Reference snapshot | Recorded snapshot path | Merge selected new source files and fix inbound links; keep local adaptations | Confirmed document/source changes |
| Root instructions and EditorConfig | Existing active paths | Merge selected rules; rebase file links to the snapshot; preserve project-specific instructions | Confirmed rules only |
| Imported assets | Existing GUID-owned destinations | Edit through Unity APIs, preserving metadata, references, and importer customizations; import new pairs only after conflict preflight | Confirmed asset update with a safe Editor route |
| Local fork kept as an overlay | Snapshot path plus a local overrides file | Restore the selected file to the pinned upstream revision; move each deliberate local difference into the overrides file as a rule with its reason; reference the overrides file from `AGENTS.md` | Confirmed overlay conversion for that file |
| Removed/moved files | Confirmed paths | Fix references; use AssetDatabase for imported moves/deletes | Explicitly selected removal/move |
| Installation record | Documentation/UnityStarterKit-installation.json | Record upstream repository URL, old/new immutable commits (and `baseline_method` with scores and `local_forks` when step 2 reconstructed them), snapshot path, selected groups, source-to-destination mappings, local adaptations, per-group revisions, and validation results | After selected updates are accounted for |

A compact record looks like this; keep the keys, add groups as installed:

```json
{
  "upstream": "https://github.com/<owner>/unity-code-style-guide",
  "installed_revision": "d803c89",
  "previous_revision": null,
  "snapshot_path": "Documentation/UnityStarterKit",
  "groups": [
    { "group": "root-instructions", "source": "AGENTS.md", "destination": "AGENTS.md",
      "method": "merged; links rebased to the snapshot", "revision": "d803c89" },
    { "group": "script-templates", "source": "AuditInstructions/ScriptTemplates/",
      "destination": "Assets/ScriptTemplates/", "method": "copied pairs, Editor closed", "revision": "d803c89",
      "files": [
        { "path": "Assets/ScriptTemplates/7-Scripting__Editor Window-NewEditorWindow.cs.txt",
          "guid": "<guid from its .meta>" }
      ] }
  ],
  "not_installed": [ { "group": "presets", "reason": "skipped by profile: Editor tooling" } ],
  "local_adaptations": [ "UnityTechStack.md: URP only, Editor-only repository" ],
  "validation": [
    { "check": "check_installation.py --target .", "result": "Passed" },
    { "check": "template compile", "result": "Not verified", "reason": "no Editor run" }
  ]
}
```

Keep per-group revisions when only part of the kit is updated. Retain the baseline needed for the
next comparison (an accessible immutable source revision or archived source bytes). A partial failure
records the actual per-file/group outcome; it does not advance the whole installation to the new revision.

**Done:** every confirmed item is merged, unchanged, or explicitly failed; unrelated content is preserved.

## 5. Verify the installed result

Check all local links and anchors in changed instructions at their actual destinations. Confirm the
active .editorconfig and root routing agree with the chosen layout. Compare installed bytes and GUIDs
with the planned result and check for duplicate identities. Repeating the comparison should propose
no additional writes for completed items.

For changed templates, generate and compile selected scripts with their prerequisites. For changed
presets/scenes, import through the target Editor, read settings/references back, reopen saved content,
and exercise affected behavior. Run focused tests and a normal player build when the change can
affect runtime or test isolation. Missing tools/devices leave those checks Not verified.

**Done:** every changed group has observed validation results, and the installation record reflects them.

## 6. Report

Report source revisions, changed and retained paths, local adaptations, test/build counts, skipped
and unavailable checks, recovery location, and proposals not selected. Put unresolved choices in a
**Needs your decision** block. Save reports or commit only within the confirmed scope.

**Done:** every recommendation and confirmed item has a final status, with no unverified pass claims.
