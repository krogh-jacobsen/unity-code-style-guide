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
explicit yes.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Restate the exact changes for the picked subset (files, settings, values, commands)
   and wait for an explicit yes. Make no change before it, including saving the report. In a
   non-interactive session, or when no answer arrives, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

## 1. Preflight the installation

Read project instructions, version/package records, working-tree state, selected resources, Editor
state, and `Documentation/UnityStarterKit-installation.json` if present. Resolve source snapshots from
one old commit and one proposed new commit. Locate the reference snapshot (default:
`Documentation/UnityStarterKit`) and active copies such as root AGENTS.md, .editorconfig, templates,
and presets. Resolve any missing source or path before planning replacement.

Compare baseline → local and baseline → upstream for every selected file. Classify each as unchanged,
upstream-only, local-only, overlapping, added, removed, or unknown baseline. Include moved files and
inbound links. Match imported resources by destination GUID as well as path. An upstream deletion is
not automatic permission to delete a local asset.

**Done:** every selected destination has a classification, source revisions, and recovery/validation needs.

## 2. Ask and recommend

Ask one batch: target revision, groups to update, local decisions to retain, and acceptable validation
scope. Defaults: retain local decisions; merge upstream-only documentation; skip overlapping or
unknown-baseline changes until individually resolved; preserve removed resources pending reference review.
For each recommendation state the exact source/destination, merge strategy, expected values, commands,
risk, and default. A missing old snapshot means manual comparison, never an assumed clean baseline.

**Done:** all differences have a recommendation or no-change result, and the exact selected edits are confirmed.

## 3. Apply selected merges

| Material | Target | How to set it | Condition |
|---|---|---|---|
| Reference snapshot | Recorded snapshot path | Merge selected new source files and fix inbound links; keep local adaptations | Confirmed document/source changes |
| Root instructions and EditorConfig | Existing active paths | Merge selected rules; rebase file links to the snapshot; preserve project-specific instructions | Confirmed rules only |
| Imported assets | Existing GUID-owned destinations | Edit through Unity APIs, preserving metadata, references, and importer customizations; import new pairs only after conflict preflight | Confirmed asset update with a safe Editor route |
| Removed/moved files | Confirmed paths | Fix references; use AssetDatabase for imported moves/deletes | Explicitly selected removal/move |
| Installation record | Documentation/UnityStarterKit-installation.json | Record upstream repository URL, old/new immutable commits, snapshot path, selected groups, source-to-destination mappings, local adaptations, per-group revisions, and validation results | After selected updates are accounted for |

Keep per-group revisions when only part of the kit is updated. Retain the baseline needed for the
next comparison (an accessible immutable source revision or archived source bytes). A partial failure
records the actual per-file/group outcome; it does not advance the whole installation to the new revision.

**Done:** every confirmed item is merged, unchanged, or explicitly failed; unrelated content is preserved.

## 4. Verify the installed result

Check all local links and anchors in changed instructions at their actual destinations. Confirm the
active .editorconfig and root routing agree with the chosen layout. Compare installed bytes and GUIDs
with the planned result and check for duplicate identities. Repeating the comparison should propose
no additional writes for completed items.

For changed templates, generate and compile selected scripts with their prerequisites. For changed
presets/scenes, import through the target Editor, read settings/references back, reopen saved content,
and exercise affected behavior. Run focused tests and a normal player build when the change can
affect runtime or test isolation. Missing tools/devices leave those checks Not verified.

**Done:** every changed group has observed validation results, and the installation record reflects them.

## 5. Report

Report source revisions, changed and retained paths, local adaptations, test/build counts, skipped
and unavailable checks, recovery location, and proposals not selected. Put unresolved choices in a
**Needs your decision** block. Save reports or commit only within the confirmed scope.

**Done:** every recommendation and confirmed item has a final status, with no unverified pass claims.
