# Scene-template maintenance tools

These explicit authoring and validation entry points run in **disposable Unity projects**. Keep
them outside normal resource installation. They create scenes/assets, replace the current scene,
set the disposable build scene list, and build a player. Use Unity CLI discovery and the exact
Editor/packages in the [validation record](../../Validation.md). The [setup guide](../../LLMInstructions/SetupInstructions/SceneTemplates.md)
owns user installation and runtime contracts.

## Validate a resource delivery

1. Create a fresh Universal 3D project with Unity CLI. Import the shipped `SceneTemplates` directory
   and its metadata at exactly `Assets/StrategyStarter/SceneTemplates` for this harness. This different
   path from authoring also checks relocation. Import only these resources, not Railroad Tycoon.
2. Copy `SceneTemplateValidation.cs` into that disposable project's `Assets/Editor`. Run
   `UnityStarter.SceneTemplates.Authoring.SceneTemplateValidation.Prepare` through `unity run` with
   `-executeMethod`. It creates `Assets/Generated/{StrategySandbox,UIPreview,AssetLookDev}{0,1}.unity`
   through SceneTemplateService, saves/reopens each, checks dependencies, and configures build scenes.
   Use a fresh project for each preparation: output paths are fixture-owned and must be empty.
3. Invoke `...SceneTemplateValidation.InstallTests`. It installs Test Framework with Package Manager
   Client, checks completion, and records the resolved version. Then copy this directory's `Tests`
   into the disposable project's `Assets/SceneTemplateTests` and import. Their asmdefs isolate them
   from normal players. Close the disposable Editor before using the batch test runner.
4. Run the focused suites, with paths expanded to absolute paths:

   ```sh
   unity test /absolute/Consumer --mode EditMode --filter UnityStarter.SceneTemplates.Tests --output /absolute/editmode.xml
   unity test /absolute/Consumer --mode PlayMode --filter UnityStarter.SceneTemplates.Tests --output /absolute/playmode.xml
   ```

   Inspect fresh XML and logs, including failures/skipped tests. Follow the target's runner-subagent
   instruction when available. The PlayMode fixture temporarily changes Input System background/editor
   focus behavior so synthetic devices work in a batch Editor, and restores both values in teardown.
5. Invoke `...SceneTemplateValidation.Build` to build an ordinary macOS player containing the three
   generated scenes. Results are written under the disposable project's `ValidationResults`, outside
   Assets. Confirm the player Managed directory excludes `SceneTemplates.*Tests` and NUnit.
6. For graphical acceptance, copy `CaptureSceneTemplates.cs` to the disposable project's Assets
   before building. Run the resulting executable with `-scene-template-capture` and
   `-sceneTemplateCaptures /absolute/Captures`; use a graphical desktop session, without `-nographics`.
   The probe is inactive without the explicit capture flag. It captures the three scenes, modal,
   and an 800x600 UI window, writes `complete.txt`, and quits. Inspect images and player logs.
   Remove the probe from consumer content after validation; it is never part of the shipped asset group.

`Prepare` reports every template dependency and its Clone/Reference mode. The tests check independent
editable assets, shared prefab/input/material references, actual camera input/blocking/projection,
and UI selection/modal focus across disable/re-enable. Device feel, all target GPUs, and Windows
acceptance remain separate checks. Test fixtures are maintenance sources outside Assets and need
no shipped Unity metadata; Unity generates their identities when imported into the disposable project.

## Author new resources or edit existing ones

For edits to shipped assets, copy them with metadata into a disposable authoring project, edit through
Unity APIs, and copy back only intended changes with the same GUIDs. Revalidate the delivered group.

`AuthorSceneTemplates.Create` is a one-time recipe for creating a fresh group, not an updater. Its
fixed source root is `Assets/StarterSceneTemplates`. Seed that root with the delivered runtime `.cs`
files/asmdef and the UI `.uxml`, `.uss`, `.tss` files, preserving their metadata. Leave generated
scenes, templates, profiles, materials, input definitions, and prefabs absent. Copy
`AuthorSceneTemplates.cs` into `Assets/Editor` and invoke
`UnityStarter.SceneTemplates.Authoring.AuthorSceneTemplates.Create`. The recipe refuses existing
templates; Unity creates all generated asset identities.

After rendering the resulting scenes, put their `StrategySandbox.png`, `UIPreview.png`, and
`AssetLookDev.png` captures in the authoring project's root `Captures` directory. Invoke
`...AuthorSceneTemplates.AttachPreviews` to import them and assign template preview textures.
It uses Unity importers for thumbnail settings. A completely regenerated group has new generated
GUIDs: do not replace an existing delivery wholesale when preserving downstream references matters.

Run `python3 Tools/validate_starter.py --resources-only` in the starter checkout after copying back.
For focused documentation checking, repeat `--markdown-path` with each repository-relative Markdown
file; without it, the checker scans all documentation. Append Unity-generated identities to
`Tools/resource-inventory.json`, keep existing entries intact, and record actual checks/limits in
`Validation.md`. No tool in this directory edits Unity YAML or authors metadata.
