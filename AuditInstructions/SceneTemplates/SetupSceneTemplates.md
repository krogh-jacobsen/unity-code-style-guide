> How it works: give this URL to your agent, for example "Install the strategy scene templates in my
> Unity project from this document". The agent audits your project first and recommends
> templates, lets you pick which to carry over, and changes nothing before you confirm the exact
> list. It then copies the templates you picked into your project, checks that Unity can create
> scenes from them, and reports what it verified. Human overview: [readme](README.md).

# Set up scene templates (agent instructions)

Install selected Strategy scene templates (starting scenes offered under **File > New Scene**) into an
existing Unity project. This document is self-contained. It installs template assets and one small
runtime assembly; it changes no project setting, build scene list, layer, or package. **Last verified:
October 2026** (Unity 6000.7.0b4 with URP 17.7.0 and Input System 6.7.0; Unity 6000.6.2f1 with URP
17.6.0 and Input System 1.20.0).

Source (replace `main` with a commit SHA for a repeatable run):
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/AuditInstructions/SceneTemplates/`
Every path in the file table below is that base plus the path, and each has a `<path>.meta` beside
it (folders too). Binary files (`.png`) must be downloaded as bytes. The license is
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/LICENSE`.

## Operating rules

- Copy shipped bytes and metadata unchanged. Never author or edit a `.unity`, `.scenetemplate`,
  `.asset`, `.prefab`, `.mat`, `.inputactions` or `.meta` file, invent GUIDs, or hand-write Unity YAML.
  The templates' dependencies reference each other by GUID, so a changed GUID breaks them silently.
- Install the shared runtime assembly `UnityStarter.SceneTemplates` once per project.
- Resolve a missing prerequisite by asking first. Install a package only after the user agrees, through
  the project's Package Manager workflow, and say which version resolved.
- Importing is not proof. Report what you observed separately from what you could not run
  (**Not verified**).

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

Here, steps 1 and 2 are the audit and the recommendations; steps 3 and 4 run only for confirmed items.

## 1. Preflight

Identify one Unity project (the user's destination or the current workspace, containing `Assets` and
`ProjectSettings/ProjectVersion.txt`). Record:

- **Editor version**, and whether that Editor is open.
- **Render pipeline.** The templates need **URP** installed *and* assigned: a default render pipeline
  asset in Graphics settings, or a per-quality-level override. Their materials, Volume, and cameras
  are URP assets. Built-in and HDRP projects are out of scope: stop and tell the user.
- **Input System package** installed, and **Active Input Handling** (Project Settings > Player) set to
  *Input System Package (New)* or *Both*. With *Input Manager (Old)* the camera rig fails at runtime.
  The runtime assembly references `Unity.InputSystem`, so even the UI Preview needs the package.
- **UI Toolkit** is in the box; nothing to install.
- **Existing resources:** an assembly named `UnityStarter.SceneTemplates`, any of the GUIDs below
  already in the project, and the project's content root (see destination).
- The source revision you will use; resolve `main` to a commit when you can.

**Done:** the target, Editor, pipeline, Input System state, existing identities, and revision are
known, any missing prerequisite is a question for the user, and the audit (stage 1) was reported
without writing anything.

## 2. Ask and select

Ask in one batch. Each default is the recommendation for that question; it takes effect only after
stage 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Which scenes: Sandbox, UI Preview, Asset LookDev? | All three |
| Destination folder | `Assets/{ProjectName}/SceneTemplates/`, or the project's established content root |
| Run the verification (generate scenes, reopen, and tests)? | Generate and reopen only |

Group dependencies:

- **Core** is always installed.
- **Shared** (camera rig, input actions, materials) is required by Sandbox and Asset LookDev.
- **UI Preview** is independent of Shared.

Selected groups install together under one destination; keep the relative layout.

| Group | Path | GUID |
|---|---|---|
| Core | `SceneTemplates.Runtime.asmdef` | `2b84a9673ac7c43cd860252636da1ff4` |
| Shared | `Shared` | `2943c2ae655364a2caeb184706f9a126` |
| Shared | `Shared/Camera` | `8acd1a91d7c19488abebe265b00fe712` |
| Shared | `Shared/Camera/StrategyCameraActions.inputactions` | `3f5680884727240e1910dded77012e54` |
| Shared | `Shared/Camera/StrategyCameraController.cs` | `e448baf448e1a4f868479156d5091fdc` |
| Shared | `Shared/Camera/StrategyCameraRig.prefab` | `6c9458c10231c4d55b1b4840ba5e3f69` |
| Shared | `Shared/Materials` | `f17fe13f3d7eb46a3af48ea90b6b3482` |
| Shared | `Shared/Materials/Accent.mat` | `4480bad88dad94ea9965740fcee5c4a0` |
| Shared | `Shared/Materials/Ground.mat` | `96eca2ff2f1c8439981f129bab956019` |
| Shared | `Shared/Materials/Stone.mat` | `d724f4061a15a416a80de1b7813948f0` |
| Strategy / Sandbox | `StrategySandbox` | `11a48bb6f838b4f6d8e601766cf0ed40` |
| Strategy / Sandbox | `StrategySandbox/NeutralVolume.asset` | `362c7eaf56fc94190805c1fe1087e150` |
| Strategy / Sandbox | `StrategySandbox/Preview.png` | `bea0596296d3e494a8d608d0b3906450` |
| Strategy / Sandbox | `StrategySandbox/StrategySandbox.scenetemplate` | `6aa198eada12d465d8e7370962a15874` |
| Strategy / Sandbox | `StrategySandbox/StrategySandbox.unity` | `d255c768e2e0b49c8b5b8d6081f7fd59` |
| Strategy / UI Preview | `UIPreview` | `360e1c433a536407786977afb4fddfcd` |
| Strategy / UI Preview | `UIPreview/Preview.png` | `797bd8794222e4d22b90fda4b58c1e2a` |
| Strategy / UI Preview | `UIPreview/PreviewPanelSettings.asset` | `7c089d13bdbda413ba84b2dc81334e51` |
| Strategy / UI Preview | `UIPreview/PreviewScreen.cs` | `b79985d7a47044962a6cd9cd373eea13` |
| Strategy / UI Preview | `UIPreview/PreviewScreen.uss` | `4903d2db22b5543cb8be6fe0eb305696` |
| Strategy / UI Preview | `UIPreview/PreviewScreen.uxml` | `0013bd2f76bd14cdf953e002c1838134` |
| Strategy / UI Preview | `UIPreview/PreviewTheme.tss` | `9f4dd1786a9ec416bad60817ebdaba67` |
| Strategy / UI Preview | `UIPreview/UIPreview.scenetemplate` | `c2577ea13fbf64e96b6b401b0f546342` |
| Strategy / UI Preview | `UIPreview/UIPreview.unity` | `fb28afd29c4c04670b09cfd4853ba823` |
| Strategy / Asset LookDev | `AssetLookDev` | `51af7974d097742eab347136eaba65c4` |
| Strategy / Asset LookDev | `AssetLookDev/AssetLookDev.scenetemplate` | `21eb2e792726b4fa0af005e6425c00c6` |
| Strategy / Asset LookDev | `AssetLookDev/AssetLookDev.unity` | `04b06482fa6e3464ea47feb5b4764e22` |
| Strategy / Asset LookDev | `AssetLookDev/NeutralVolume.asset` | `2bad5f90e35c743ad953f70ae59c7f4b` |
| Strategy / Asset LookDev | `AssetLookDev/Preview.png` | `c5192cd697f934038808eb1abac1a28f` |

Turn the answers into numbered recommendations (stage 2): one per scene group (Sandbox, UI Preview,
Asset LookDev), one for the destination folder, one for the verification level, and one for each
missing prerequisite. Give each its finding from the audit, why it matters, risk, and a default. Shared
and Core follow the scenes that need them. The user may pick any subset (stage 3), then confirms the
exact list (stage 4).

**Done:** the recommendations were shown, the user picked from them, and the selected groups,
destination, and verification level were confirmed before any file was written.

## 3. Install

Only the groups confirmed in stage 4. Stage first, then check, then copy.

1. **Stage.** Download every file of the selected groups plus each `.meta`, and the license, into a
   temporary folder outside the target's `Assets`. Reject HTML or error responses and any half pair.
2. **Verify.** Each `.meta` must contain the `guid:` from the table. Stop on a mismatch.
3. **Preflight destinations.** Reject path traversal, symlinks, and case-only collisions, and check
   each GUID against the project's existing assets.

   | Destination state | Action |
   |---|---|
   | Absent and the GUID unused | New: install |
   | Same bytes and GUID at the path | Already installed: leave it |
   | Different content or GUID, a half pair, or the GUID elsewhere | Conflict: report both and resolve before copying. Never overwrite a project's own scene or asset |

4. **Copy.** With the target's Editor closed, create only the missing destination folders (Unity
   generates their metadata) and copy the staged files with their `.meta` intact. With the Editor open,
   use an approved route that keeps each file and `.meta` together, or ask the user to close it.
5. **License.** Place the MIT license in the project's existing third-party notices location outside
   `Assets`, or at `ThirdPartyNotices/UnityCodeStyleGuide-LICENSE.txt`. Reuse an identical notice.
6. **Import and read back.** Let Unity import, then confirm each installed file's bytes and GUID, and
   read the console and import log for new errors, warnings, and missing script or reference
   messages. A repeat run must plan no copies.

**Done:** every selected file is installed or already present, the license is placed, the import is
clean, and a repeat run does nothing.

## 4. Verify the templates

Unity registers every imported `.scenetemplate` asset for **File > New Scene**; no restart is needed.
Scene generation below uses the same service. Seeing the entries in the dialog needs an interactive
Editor: if that is not possible, report the dialog as **Not verified**. This step covers only the
templates installed in step 3, at the verification level confirmed in stage 4.

1. Create **two** scenes from each installed template with
   `UnityEditor.SceneTemplate.SceneTemplateService.Instantiate(template, false, path)`, saving into a
   scratch folder (for example `Assets/Generated/`), and remove them afterward through Editor APIs.
2. Save, reopen, and check each scene: no missing scripts or references, one active camera and one
   audio listener, assigned UI assets (UI Preview), valid materials.
3. Check dependency ownership (table below): editable assets are **distinct copies** between the two
   scenes, while the camera prefab, input definition, scripts, and shared materials stay **shared**.
   Edit a cloned asset in the first scene and confirm the second and the template source are unchanged.
4. Only when the user chose the full verification: exercise camera input, `SetInputBlocked`,
   disable/re-enable, and projection switching, and in UI Preview selection, scrolling, Tab, the
   modal, Escape, and a small window. These are PlayMode checks; importing proves none of them.

| Asset | New-scene behavior |
|---|---|
| Scene-specific Volume Profile | Clone |
| UI PanelSettings, UXML, theme, USS | Clone |
| Camera prefab, input actions, C# scripts | Reference |
| Shared ground, stone, accent materials | Reference |
| Preview thumbnails | Template metadata |

Delete the scratch scenes. Do not add any scene to Build Settings or build profiles, and do not change
Graphics, Quality, layers, or input settings.

**Done:** each installed template generated, saved, and reopened with valid references, and the
dependency ownership matches, or the unperformed check is stated.

## 5. Report

| Item | Status | Detail |
|---|---|---|
| Source URL and revision | | |
| Prerequisites | Met / Question raised | URP assigned, Input System and handling |
| Each installed group | Installed / Already installed / Conflict / Not selected | Path and GUIDs |
| License | Placed / Already present | Location |
| Repeat run | Nothing to do / Work found | |
| Unity import | Verified / Not verified | Console result |
| Scene generation and reopen | Passed / Not verified | Two per template |
| Dependency ownership | Passed / Not verified | |
| Runtime interaction | Passed / Not selected / Not verified | |
| Unpicked recommendations | Proposal | IDs, with the reason each was skipped |

Put conflicts, missing prerequisites, unanswered choices, and unpicked recommendations in a "Needs your
decision" block at the top. End with the next step for the user: **File > New Scene**, choose a **Strategy /** template, and
save the result into the project's scene folder. Scenes already created from a template are not
updated when the template changes.

## Known limits

Say these when relevant instead of working around them.

- The strategy camera has free XZ movement, with no terrain bounds, clearance, or minimap. A host that
  adds UI to a world scene calls `SetInputBlocked(true)` while a modal or tool owns input and checks
  `IsDragging` to avoid conflicting gestures.
- With additively loaded scenes, the host must choose the active rig and audio listener.
- Rendering quality, HDR output, shadow budgets, and lighting bakes are the project's choices; the
  scenes use flat ambient fill and a Volume with tonemapping off.
- The UI Preview's tooltip, slider, toggle, and text field are appearance samples with local state only.
- Installation does not register any scene as game content.
