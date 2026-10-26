# Script-template maintenance tools

Maintainer notes, not an agent document. Unity ignores this `Tools~` folder, so copying the parent
folder into `Assets` never imports it.

- `validate_scripttemplates.py` is the static check (tokens, prefixes, GUID table versus metadata,
  static state needs a lifecycle attribute). `python3 -I Tools~/validate_scripttemplates.py`.
- `inventory.json` freezes each template's GUID.
- `AwaitableOperationTests.cs.txt` is a PlayMode test for the Awaitable Operation template (renamed so Unity never imports it from the repository).
- `GenerateTemplates.cs` expands every template through Unity's own engine so the output can be
  compiled and read for diagnostics.

## Reproduce the generation check

Use a disposable project, never a real one. Last run: October 2026, Unity 6000.7.0b4 (and the Static
Event template on 6000.6.2f1).

1. Create a project containing only a `Packages/manifest.json` (modules `ui`, `uielements`, `imgui`,
   `physics`, `jsonserialize`, `audio`), `ProjectSettings/ProjectVersion.txt`, and this
   `GenerateTemplates.cs` under `Assets/Editor/`. The EditMode, PlayMode, and NetworkBehaviour
   templates need Test Framework and Netcode, so the script skips them; add those packages and
   remove the skip to cover them.
2. Generate: `TEMPLATE_DIR=<this folder's parent> unity run <project> --editor-version <version> -- -executeMethod GenerateTemplates.Run -logFile gen.log`.
   It sets Enter Play Mode to skip domain reload (so the statics analyzer runs), expands each template
   under an empty and a populated Root Namespace into `Assets/Generated/{Global,Namespaced}`, and uses
   reflection to call `ProjectWindowUtil.CreateScriptAssetFromTemplate` (non-public).
3. Compile: run again with `-executeMethod GenerateTemplates.Report -logFile compile.log`.
4. Read `compile.log` for `error CS`, `warning CS`, and `UAL`. Expect none.

Set `ONLY=<text>` to expand only templates whose path contains that text.
