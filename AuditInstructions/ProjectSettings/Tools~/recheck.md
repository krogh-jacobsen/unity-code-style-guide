# Re-check checklist for ProjectSettings.md

Maintainer notes, not an agent document (Unity ignores this `Tools~` folder). Run this when the
Unity 6.7 manual publishes its "What's new" and upgrade pages, when 6.7 reaches release, and at
least every six months. `python3 AuditInstructions/Tools/validate_all.py` warns when a "Last verified" date is older
than that.

After re-checking, update the **Last verified** line in `ProjectSettings.md` and the CHANGELOG.

## Claims that rest on thin evidence

These were the weakest sources when the guide was written (October 2026, 6.7 beta manual). Re-read
each source and either confirm, correct, or remove the claim.

| Claim in `ProjectSettings.md` | Why it is weak | Source to re-read |
|---|---|---|
| Domain reload is off by default for **new** projects from 6.6 | Taken from a summarized part of the 6.6 "What's new" page; the upgrade guide and API pages do not repeat it | [What's new in 6.6](https://docs.unity.com/en-us/engine/6000.7/manual/whats-new/unity66), then the 6.7 page |
| Existing projects keep their saved Enter Play Mode value | Not stated anywhere | Create a project on the old and new Editor, compare `ProjectSettings/EditorSettings.asset` |
| Dropdown option to `EnterPlayModeOptions` flag mapping | The manual does not map them | [EnterPlayModeOptions](https://docs.unity.com/en-us/engine/6000.7/script-reference/unityeditor/enterplaymodeoptions); set via API, read the dropdown |
| Templates ship the same Enter Play Mode value | No page says | Create a Universal 3D project and read the value |
| Burst is a built-in module from 6.6 (no package) | Summarized text only; Burst absent from the core and built-in package lists read | 6.6 and 6.7 "What's new"; the resolved package list of a fresh project |
| `[AutoStaticsCleanup]` guidance, `UAL0010` to `UAL0014` | Read from the 6.7 manual; attribute choices come from a table the agent summarized | [Enter Play mode without domain reload](https://docs.unity.com/en-us/engine/6000.7/manual/programming-environment/code-reload-serialization/code-reload/code-reloading-editor/domain-reloading) |
| Active Input Handling default and the legacy deprecation | The manual lists the options and calls the legacy page "deprecated"; no default stated | 6.7 Player settings, the Input pages; a fresh project |
| API Compatibility Level default | Options listed, no default stated | 6.7 Player settings |
| `UNITY_64`, `DEVELOPMENT_BUILD` deprecated; removal in 6.8 | From the 6.6 upgrade guide; the removal plan can move | [Upgrade to 6.6](https://docs.unity.com/en-us/engine/6000.7/manual/upgrade-guides/upgrade-guide-unity66), then the 6.7 guide |
| CoreCLR (Experimental) backend, not a baseline | Listed on the Windows page; macOS page not read | 6.7 Windows and macOS Player settings pages |
| Project Auditor | Package exists (3.1.x); what it checks is not documented where read | The package manual |

## Claims to re-confirm on every release

- Force Text and Visible Meta Files are the defaults (Editor settings reference).
- URP package version matches the Editor (core packages list).
- The Built-in pipeline is still described as deprecated.
- Dynamic batching is obsolete; SRP Batcher remains the recommended path.
- The reload dropdown labels and the default option.

## When 6.7 ships

1. Read the 6.7 "What's new" and upgrade guide for any item touching Editor settings, Player
   settings, input, scripting runtime, or Enter Play Mode.
2. Move rows marked **6.6+** to plain rows, or add **6.7+** where behavior changed again.
3. Check whether CoreCLR changes the reset attributes or the `RuntimeInitializeOnLoadMethod` fallback.
4. Update the readme's "Good to know" version note.
