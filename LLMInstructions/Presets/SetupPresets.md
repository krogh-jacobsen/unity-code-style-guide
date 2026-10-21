# Set up presets

Agent entry point for installing selected import presets from a URL or local checkout into an existing
Unity project. Use available tools; add no setup package or permanent installer. The default scope is
installation only: copying a preset does not select assets to change or register a default import rule.

## 1. Read the guides and select scope

Read the target's instructions, the [preset policy](readme.md), and the
[shared installation protocol](../InstallResources.md) before copying. Resolve source guides/files
against the supplied URL/local checkout and use one source revision as the shared protocol requires.

Use the policy's inventory and role guidance to select presets for actual content. Ask one short round
when roles are unknown, offering relevant texture, audio, static-model, or animation-only choices.
Choose one audio policy per clip; its alternatives are not layers to apply in sequence. Keep the
animation-only preset distinct from a character/rig import policy.

Select the operation as well as the files:

| Operation | Scope |
|---|---|
| Install only — default | Copy selected preset pairs and verify import; change no existing asset importers or default rules |
| Apply to selected assets | Also preview and apply explicit preset-to-asset mappings, then verify preservation |
| Register scoped defaults | Also configure selected future-import rules on a verified Editor and test a genuinely new import |

Infer an explicitly requested operation from the user's instruction; ask only when it is unresolved.
Desktop compression/resolution tuning and persistent import enforcement are separate selections;
reading their policy does not authorize applying them. Keep unrelated project settings and vendor
assets outside the selected scope.

**Done:** selected presets, operation, and any exact target assets/owned-folder filters are known.

## 2. Install selected pairs

Follow the shared protocol for staging, license, GUID checks, conflicts, copying, and import.
Map each selected preset's inventory-relative path under `Assets/Settings/Presets/`, retaining its
role subfolder, filename, and matching metadata. Copy files individually; do not install this workflow,
the policy README, or all presets merely because they share a source directory.

Use the shared protocol's handling for existing customized assets. After installation, repeated
comparison must leave matching assets and metadata untouched. Verify that Unity imports the selected
files as usable presets; report unresolved Editor/version compatibility rather than rewriting the YAML.
For Install only, finish with the report in step 5; steps 3 and 4 require their selected operations.

**Done:** selected preset pairs and license are installed or unchanged, with import results recorded.

## 3. Apply only selected preset-to-asset mappings

Run this step only when application is selected. Preview the exact owned asset paths and preset roles;
resolve incompatible or overlapping mappings before changing importers. Follow the preset policy's
Editor application/readback procedure, checking applicability and included properties first.

Record target GUIDs and authoring values before application. Preserve the documented slices, pivots,
borders, material mappings, rigs, clips, platform overrides, and unrelated values; account for each
preset's deliberate exceptions, including the spatial SFX mono policy. A fresh UI texture also needs
an explicit Single/Multiple selection when not already configured. Read back after saved reimport and
check representative saved references. Expected importer-setting changes are separate from preset
installation; target GUIDs and unselected properties must be preserved.

Do not use metadata deletion or Inspector Reset to apply policies. On reruns, compare included values
and skip already-matching targets instead of forcing unnecessary reimports. With no available Editor
application route, leave target importers untouched and report application as Not verified.

**Done:** each selected target matches its chosen policy after reimport, preserved values remain intact,
and failures or unperformed applications are explicit.

## 4. Register defaults only when selected and verified

Follow the preset policy's current Editor restrictions and default-import procedure. Its recorded
texture-default crash on Unity 6000.7.0b4 prohibits that route on the affected version; use initial
import followed by explicit application instead. A different Editor release needs its own verification,
not an assumption that the crash is fixed.

Preview owned-folder filter matches and rule order before registration. Preserve unrelated rules;
reuse matching registrations and resolve overlapping precedence without accumulating duplicate rules
on reruns. Register only selected compatible defaults through Editor settings/APIs. Verify their effect
on a genuinely new import; existing assets are not retroactively configured. Keep test fixtures outside
vendor content and clean temporary imported assets through Editor APIs.

No AssetPostprocessor or other persistent enforcer is installed by this workflow. If safe default-import
validation is unavailable, retain the files and report registration/validation pending.

**Done:** selected rules are saved, a new import demonstrates the intended policy, and unrelated rules
are preserved, or the unperformed registration/check is explicitly reported.

## 5. Report the actual result

Report source revision, selected presets and operation, installed/conflicting paths, license location,
and repeat-run comparison. Separate file-copy verification, Unity import, existing-asset application,
and default registration/new-import validation. Mark unselected operations Not selected and unavailable
checks Not verified, including the next action needed. Copying presets alone is an installation result,
not proof of applied policy, platform quality, memory budgets, or enforcement.

**Done:** the user can distinguish installed resources from observed importer/default behavior and
remaining validation, with no unselected operation applied.
