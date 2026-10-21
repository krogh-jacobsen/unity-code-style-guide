# Install selected starter resources

Shared installation protocol for the script-template and preset entry points. Read it before copying
selected resources; selection and resource-specific validation belong to the invoking workflow.
Use available file/Editor tools without installing a package, CLI, interpreter, or permanent helper.

## 1. Establish the source and target

Read the target project's instructions first. Identify one existing Unity project by the user's
destination or current workspace, `Assets`, and `ProjectSettings/ProjectVersion.txt`; resolve any
ambiguity before writing. Inspect its exact Editor, relevant packages, existing resources, dirty
state, and whether that project's Editor is open. Preserve unrelated edits and unsaved work.

Read the invoking workflow, its policy guide, the [resource inventory](../../Tools/resource-inventory.json),
and [MIT license](../../LICENSE) from one source revision. Resolve relative source links against the
supplied URL or local checkout, not against the target project. Prefer a commit- or release-pinned
URL; resolve a moving branch to one commit when possible so later downloads use the same snapshot.
Report the source URL/path and revision, including any unpinned-source limitation.

Stage only selected resource files, their matching `.meta` files, and the license in a temporary
location outside the target's `Assets`. Fetch raw file bytes; URL-encode filenames containing spaces.
Require every selected pair to be complete and each metadata GUID to match its inventory entry.
Reject HTML/error responses or inconsistent source files before copying. Preserve shipped bytes,
template tokens, filenames, and identities; do not recreate resources or author metadata from prose.

**Done:** the intended target, source snapshot, selected resource pairs, and license are known and readable.

## 2. Preflight every destination

Build a source-to-destination list using the invoking workflow's placement rules. Resolve asset paths
inside the intended `Assets`, reject traversal, symlinked entries, case-only collisions, and files
blocking required directories. Check the complete selection before changing the target.

Check selected GUIDs against existing target asset identities, including imported package assets.
Use the asset database when available or inspect available target metadata before import. If the
required identity/conflict checks cannot be completed, keep the files staged and report the missing
check instead of importing an unchecked selection.

| Destination state | Action |
|---|---|
| Asset and metadata absent; source GUID unused | Plan a first installation |
| Same asset bytes and same GUID already at the intended path | Already installed; preserve destination metadata and importer values |
| Different content/identity, an incomplete pair, or the GUID at another path | Report both paths/identities and resolve the conflict before copying |

Existing customized assets and metadata are not replacement targets by default. An update or migration
needs an explicitly selected Editor workflow that preserves destination GUIDs and references. Do not
invent new GUIDs, delete metadata, rename Create-menu files, or add suffixed copies to bypass a conflict.

**Done:** each selected pair is New or Already installed; blocking conflicts have been resolved.

## 3. Copy intact pairs and import

For first installation with the target Editor confirmed closed, create only required missing destination
directories and copy the staged resource/metadata pairs intact. This is an initial-import exception,
not permission to overwrite imported assets. Leave existing destination folder metadata in place;
Unity generates metadata for new directories. Follow stricter target-project instructions.

With the Editor open, use an already available, project-approved import route that preserves the
preflighted identities and prevents partial pairs being imported. Otherwise ask the user to close
that Editor when ready. Preserve dirty work; install no bridge or package to make this workflow run.

Include the source MIT license in the project's existing third-party notices location outside `Assets`,
or use `ThirdPartyNotices/UnityCodeStyleGuide-LICENSE.txt`. Reuse an identical notice; preserve unrelated
notices and resolve a differing file before replacement. Copy selected resource files individually:
documentation, optional/retired resources, and source folder metadata are not wholesale install groups.

Read back each installed asset's bytes and GUID. Re-run the comparison: a completed install must plan
no further copies or metadata replacement. Report any partial installation and retain its source
snapshot for recovery; do not repair it by generating a new identity.

Import/refresh through existing Editor access or open the target with its installed Editor when safe
and within scope. Inspect fresh logs, saved GUID-to-path mappings, and generated folder metadata.
Verify no identity conflicts and no unintended authored changes; distinguish ordinary Editor caches
from project content. With no safe import route, report Files copied and Import Not verified, with
the next action needed. Copying source text is not proof that Unity accepted it.

**Done:** selected file pairs and license are installed or unchanged, repeated comparison finds no
work, and import verification has an observed result or an explicit pending check.

## 4. Report resource-specific readiness

Finish the invoking workflow's validation. Report the target, source revision, selected files,
Created/Already installed/conflicting paths, license location, and before/after changes. Separate
file-copy verification, Unity import, and resource-specific behavior; list checks not performed.
Default registration, application to existing assets, code generation, and package/assembly changes
are separate selections governed by that workflow. Save no permanent installer or setup report unless
requested, and commit only within the user's source-control scope.

**Done:** the report states what is installed, what was exercised in Unity, and what still needs validation.
