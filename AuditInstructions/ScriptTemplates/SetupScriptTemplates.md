> How it works: give this URL to your agent, for example "Install the starter script templates in my
> Unity project from this document". The agent audits your project first and recommends
> templates, lets you pick which to carry over, and changes nothing before you confirm the exact
> list. It then copies the templates you picked into `Assets/ScriptTemplates/`, confirms Unity picked
> them up, and reports what it verified. Human overview: [readme](README.md).

# Set up script templates (agent instructions)

Install selected script templates (`.cs.txt` files that Unity offers in the Create menu) into an
existing Unity project. This document is self-contained and installs template text only: no
generated gameplay scripts, packages, asmdefs, or project settings. **Last verified: October 2026**
(Unity 6000.7.0b4; the Static Event template also on 6000.6.2f1).

Source (replace `main` with a commit SHA for a repeatable run):
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/AuditInstructions/ScriptTemplates/`
Each template is two files, `<name>.cs.txt` and `<name>.cs.txt.meta`. Filenames contain spaces, so
URL-encode them. The license is
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/LICENSE`.

## Operating rules

- Copy shipped bytes and metadata unchanged. Never author or edit a template or its `.meta`, invent
  GUIDs, rename the files, or delete metadata. The filename sets the menu entry, so a rename moves it.
- Install into the project's `Assets/ScriptTemplates/`, never into the Editor installation: Unity
  overwrites that folder on upgrade.
- Keep a target's different UI, async, or assembly choices; install only templates whose
  prerequisites the project meets, and defer the rest instead of installing packages.
- Report observed results separately from checks you could not run (**Not verified**). A template is a
  text asset: a successful import does not prove the C# it generates compiles.
- Missing recommendation details do not block independent read-only preflight. Inspect the Editor,
  packages, namespace, and existing templates while recovering the prior change list or gathering
  the evidence needed to present concrete changes; keep execution pending until scope is known.

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

Here, steps 1 and 2 are the audit and the recommendations; steps 3 to 5 run only for confirmed items.

## 1. Preflight

Read the target's instructions. Identify one Unity project (the user's destination or the current
workspace, containing `Assets` and `ProjectSettings/ProjectVersion.txt`). Record:

- Editor version, and whether that Editor is open. Unity 6.5 or later is needed for the Static Event
  template as shipped (the attribute is documented from 6.5; tested on 6000.6 and 6000.7; see its row below).
- The Root Namespace (Project Settings > Editor), packages already installed (Test Framework,
  Netcode for GameObjects), and any assembly definitions.
- The contents of `Assets/ScriptTemplates/`, including customized templates.
- The source revision you will use; resolve `main` to a commit when you can.

**Done:** the target, Editor version, namespace, packages, and existing templates are known, and the
audit (stage 1) was reported without writing anything.

## 2. Ask and select

Ask in one batch. Each default is the recommendation for that question; it takes effect only after
stage 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Which templates: the five defaults, plus which optional ones? | The five defaults only |
| Run generation checks (expand each template and compile)? | No: install and menu readiness only |

Select from this inventory. Fetch only selected pairs; the optional folder and the retired folder are
not install groups. All selected files install flat into `Assets/ScriptTemplates/`.

| Pri | Menu entry | Source path | Prerequisite | GUID |
|---|---|---|---|---|
| 1 | MonoBehaviour Script | `1-Scripting__MonoBehaviour Script-NewMonoBehaviourScript` | None | `c46dbac4eeff44229cf74fd90b8afdcc` |
| 2 | ScriptableObject | `2-Scripting__ScriptableObject Script-NewConfigDataSO` | None; name generated types `…DataSO` | `674e6d0417244fa6b22c8465a67e4633` |
| 3 | Empty C# Script | `3-Scripting__Empty C# Script-NewEmptyCSharpScript` | None | `9c336b9cefce4fbb90440f55ab1b63b5` |
| 4 | UI Toolkit View | `4-Scripting__UI Toolkit View-NewUIToolkitViewScript` | Assign PanelSettings and UXML to run it | `4bf5568eb6d74dc2a45ead460b09044e` |
| 5 | Interface | `5-Scripting__Interface-INewInterface` | None; name `IYourContract` | `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6` |
| 6 | IMGUI Custom Editor | `OptionalScriptTemplates/6-Scripting__Custom Editor-NewCustomEditor` | Editor-only folder or assembly | `b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7` |
| 7 | IMGUI Editor Window | `OptionalScriptTemplates/7-Scripting__Editor Window-NewEditorWindow` | Editor-only; choose a unique menu path | `c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8` |
| 8 | IMGUI Property Drawer | `OptionalScriptTemplates/8-Scripting__Property Drawer-NewPropertyDrawer` | Editor-only; supply the target type | `d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9` |
| 9 | EditMode test | `OptionalScriptTemplates/9-Scripting__Unit Test EditMode-NewEditModeTest` | Test Framework and an isolated EditMode asmdef | `e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0` |
| 10 | PlayMode test | `OptionalScriptTemplates/10-Scripting__Unit Test PlayMode-NewPlayModeTest` | Test Framework and an isolated PlayMode asmdef | `f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1` |
| 11 | Static Event | `OptionalScriptTemplates/11-Scripting__Static Event-NewStaticEvent` | **Unity 6.5+** (`Unity.Scripting.LifecycleManagement`) | `a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2` |
| 12 | Object Pool Handler | `OptionalScriptTemplates/12-Scripting__Object Pool Handler-NewObjectPoolHandler` | An inactive prefab; host-lifetime owner | `b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3` |
| 14 | NetworkBehaviour | `OptionalScriptTemplates/14-Scripting__NetworkBehaviour-NewNetworkBehaviour` | Netcode for GameObjects with the universal `[Rpc]` API (validated 3.1.0) | `c9a4204bb6b834fbcb54e64df11762ef` |
| 15 | UI Toolkit Custom Editor | `OptionalScriptTemplates/15-Scripting__UI Toolkit Custom Editor-NewUIToolkitEditor` | Editor-only | `fa761b9db816d440abab41024553c89b` |
| 16 | UI Toolkit Editor Window | `OptionalScriptTemplates/16-Scripting__UI Toolkit Editor Window-NewUIToolkitWindow` | Editor-only; choose a unique menu path | `6a9841d6af62642e1a5366591f611729` |
| 17 | UI Toolkit Property Drawer | `OptionalScriptTemplates/17-Scripting__UI Toolkit Property Drawer-NewUIToolkitDrawer` | Editor-only; supply the target type | `adcf1d46ad9e54b5ea5836c18000a892` |
| 18 | Awaitable Operation | `OptionalScriptTemplates/18-Scripting__Awaitable Operation-NewAwaitableOperation` | Unity 6 (`Awaitable`, `destroyCancellationToken`); replace the sample wait with real work | `406ed49d3c7214eb1a541e7cb061acb1` |

Notes on choosing:

- Awaitable Operation is the async pattern: one cancellable operation owned by the component, cancelled on disable, destroy, or restart, with every outcome observed.
- The five defaults need no package and no project-specific base class. Everything else is opt-in.
- Choose one Inspector approach per target: IMGUI (6 to 8) or UI Toolkit (15 to 17). Unity recommends
  UI Toolkit for new Editor UI; IMGUI still works. Drawer and Editor templates are deliberately
  unregistered placeholders: the user adds `[CustomEditor]` or `[CustomPropertyDrawer]` with a real target.
- Test templates are `[Ignore]`d placeholders until real assertions replace them; report them as
  unfinished.
- A retired priority-13 state sketch exists in `ReferenceOnly/`. Do not install it.
- **Static Event compatibility:** the attribute is documented from Unity 6.5; the shipped template
  was compiled on 6000.6.2f1 and 6000.7.0b4. Confirm API/code-generator availability on other patches.
  On an Editor before 6.5, defer this shipped template. If the user separately selects an adapted
  custom template, preserve the shipped pair and create the adaptation through the target
  project's Editor workflow with its own identity. Remove the unavailable lifecycle namespace and
  attribute from that adaptation, and reset its event with:

  ```csharp
  [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
  private static void ResetStatics()
  {
      EventRaised = null;
  }
  ```

Turn the answers into numbered recommendations (stage 2): one per template worth installing (the five
defaults first, then optional ones whose prerequisites the project meets), one for deferring each
template whose prerequisite is missing, and one for the generation checks. Give each its finding from
the audit, why it matters, risk, and a default. The user may pick any subset (stage 3), then confirms
the exact list (stage 4).

**Done:** the recommendations were shown, the user picked from them, and the selected templates,
deferred prerequisites, and Editor-version decisions were confirmed before any file was written.

## 3. Install

Only the templates confirmed in stage 4. Stage first, then check, then copy.

1. **Stage.** Download each selected `.cs.txt` and `.cs.txt.meta` into a temporary folder outside
   the target's `Assets`, plus the license. Reject HTML or error responses and any half pair.
2. **Verify.** Each `.meta` must contain the `guid:` from the table above. Stop on a mismatch.
3. **Preflight destinations.** Each file installs to `Assets/ScriptTemplates/<filename>` with its
   `.meta` beside it. Reject path traversal, symlinks, and case-only collisions, and check each GUID
   against existing project assets.

   | Destination state | Action |
   |---|---|
   | Absent and the GUID unused | New: install |
   | Same bytes and GUID at the path | Already installed: leave it |
   | Different content or GUID, a half pair, or the GUID elsewhere | Conflict: report both and resolve before copying. A customized template is never overwritten |

4. **Copy.** With the target's Editor closed, create only the missing `Assets/ScriptTemplates/`
   directory and copy the staged pairs intact; Unity generates metadata for the new folder. With the
   Editor open, use an approved route that keeps the pairs together, or ask the user to close it.
5. **License.** Place the MIT license in the project's existing third-party notices location outside
   `Assets`, or at `ThirdPartyNotices/UnityCodeStyleGuide-LICENSE.txt`. Reuse an identical notice.
6. **Read back.** Confirm each installed file's bytes and GUID, and check the import log for fresh
   errors. A repeat run must plan no copies.

**Done:** every selected pair is installed or already present, the license is placed, and a repeat run
does nothing.

## 4. Confirm the Create menu

Unity reads templates when the Editor starts. Restart the target Editor (preserving unsaved work), or
ask the user to, then check that each selected entry appears under Assets > Create > Scripting. File
presence alone does not prove readiness. If a restart or inspection is not possible, report menu
readiness as **Not verified** with the next action.

**Done:** each selected menu entry is observed, or readiness is explicitly pending.

## 5. Generation checks (only when selected and confirmed)

Run in a disposable project or an agreed temporary fixture, and remove it through Editor APIs
afterward. For each selected template:

1. Expand it twice, once with an empty Root Namespace and once with a populated one, using Unity's own
   expansion. Unity's non-public `ProjectWindowUtil.CreateScriptAssetFromTemplate(path, templateFile)`
   works through reflection (verified on 6000.7.0b4); the public `CreateScriptAssetFromTemplateFile`
   is interactive.
2. Place Editor templates in an `Editor` folder or Editor-only assembly, and tests in isolated test
   assemblies.
3. Import, then read the compiler output. Expect zero errors **and zero warnings**: with Enter Play
   Mode set to skip domain reload, the `UAL` analyzer warns about any unprotected static state.
4. Exercise the selected runtime dependencies (a UIDocument with PanelSettings, a pool with an
   inactive prefab, Netcode set up) before claiming the behavior works.

**Done:** each template compiles cleanly under both namespace settings, or the unperformed check is
stated.

## 6. Report

| Item | Status | Detail |
|---|---|---|
| Source URL and revision | | |
| Each selected template | Installed / Already installed / Conflict / Deferred | Path and GUID |
| License | Placed / Already present | Location |
| Repeat run | Nothing to do / Work found | |
| Unity import | Verified / Not verified | |
| Create menu | Observed / Not verified | Next action |
| Generation and compile | Passed / Not selected / Not verified | Editor version, diagnostics |
| Unpicked recommendations | Proposal | IDs, with the reason each was skipped |

Put conflicts, version gates, unanswered choices, and unpicked recommendations in a "Needs your
decision" block at the top.

## Adapting a template

Templates are plain text with Unity substitutions. Keep these when editing a copy in the project:

- `#SCRIPTNAME#` becomes the class name; `#ROOTNAMESPACEBEGIN#` and `#ROOTNAMESPACEEND#` wrap the
  body in the project's Root Namespace, and an empty namespace generates valid code. The whitespace
  before `#ROOTNAMESPACEBEGIN#` sets the indent inside a populated namespace (verified: four spaces
  indent the body one level).
- The filename is `<priority>-<menu path with __ between levels>-<default filename>.cs.txt`.
  Changing it moves or replaces the menu entry.
- Customize in the project, not the Editor installation.

## References

- [Customize Unity script templates](https://support.unity.com/hc/en-us/articles/210223733-How-to-customize-Unity-script-templates) (Unity Support)
- [AutoStaticsCleanup API](https://docs.unity3d.com/ScriptReference/Unity.Scripting.LifecycleManagement.AutoStaticsCleanupAttribute.html) (documented from 6.5; compile-tested releases listed above)
- [Enter Play mode without domain reload](https://docs.unity.com/en-us/engine/6000.7/manual/programming-environment/code-reload-serialization/code-reload/code-reloading-editor/domain-reloading)
- [ObjectPool&lt;T&gt;](https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1-ctor.html)
- [Netcode for GameObjects RPCs](https://mp-docs.dl.it.unity3d.com/netcode/current/advanced-topics/message-system/rpc-params/)
