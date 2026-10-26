> How it works: give the URL of [SetupScriptTemplates.md](SetupScriptTemplates.md) to your agent and it
> will audit your project, recommend templates, and, once you confirm your picks, copy them into your
> project's `Assets/ScriptTemplates/` and confirm Unity picked them up.

# Script templates

Script templates change what Unity writes when you choose **Assets > Create > Scripting**. These
follow this repository's [style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md), so a new script
starts in the right shape instead of being cleaned up afterwards.

| I want to… | Give your agent |
|---|---|
| Install the default or optional templates | [SetupScriptTemplates.md](SetupScriptTemplates.md) |

Example prompts:

- *"Install the starter script templates in my Unity project from this document."* The five defaults.
- *"Install the defaults plus the UI Toolkit editor templates and the Static Event template."*
- *"Install the templates and check that they compile in my project."* Adds the generation check.

## What happens when you hand it over

1. **Audit.** The agent reads your project: Editor version, Root Namespace, packages, and any
   templates already in `Assets/ScriptTemplates/`.
2. **Recommendations.** You get a numbered list of templates worth installing, deferred ones whose
   prerequisites are missing, and the optional compile check, each with a reason, risk, and default.
3. **You pick.** Any subset, "all recommended", or none. One template is a valid choice.
4. **You confirm.** The agent restates the exact files and waits for an explicit yes.
5. **It applies and verifies.** Only the confirmed templates are copied, and the report lists what
   you skipped.

## What is included

**Five defaults.** No packages, no base classes of ours.

| Template | What you get |
|---|---|
| MonoBehaviour | An empty `sealed` component. You add only the lifecycle methods you need |
| ScriptableObject | A configuration asset with a Create menu entry; runtime state belongs elsewhere |
| Empty C# Script | A plain class |
| UI Toolkit View | A `UIDocument` host with a safe `SetVisible` |
| Interface | `IYourContract`, without a doubled `I` |

**Optional.** Pick individual files.

| Group | Templates |
|---|---|
| Editor tooling, IMGUI | Custom Editor, Editor Window, Property Drawer |
| Editor tooling, UI Toolkit | Custom Editor, Editor Window, Property Drawer |
| Tests | EditMode and PlayMode skeletons, ignored until you add an assertion |
| Runtime patterns | Static Event, Object Pool Handler, Awaitable Operation |
| Networking | NetworkBehaviour (needs Netcode for GameObjects) |

## Conventions the templates carry

- **Naming.** `m_` for private fields, `k_` for constants, `s_` for statics, and an explicit `private`.
- **Layout.** Allman braces, usings ordered system then Unity, and guard clauses with braces.
- **Empty on purpose.** A MonoBehaviour has no `Update()`; Unity calls empty ones every frame.
- **Placeholders say so.** Drawers and editors are unregistered until you name a target, and tests are
  `[Ignore]`d until they assert something, so an unfinished template can't pass for a finished one.
- **`sealed` by default.** The templates mark classes `sealed`. This is the starter's choice, not a
  Unity requirement: remove it from a class you plan to inherit from.

## How Unity templates work

- Templates live in the project's `Assets/ScriptTemplates/` folder, which must be a direct child of
  `Assets`. Customize them there, not in the Editor installation, which Unity overwrites on upgrade.
- **Restart the Editor** after adding or changing one; Unity reads them at startup.
- The filename is the menu: `<priority>-<menu path, levels joined by __>-<default filename>.cs.txt`.
- `#SCRIPTNAME#` becomes the class name. `#ROOTNAMESPACEBEGIN#` and `#ROOTNAMESPACEEND#` wrap the
  body in your project's Root Namespace (Project Settings > Editor), and generate plain code when the
  namespace is empty.
- A template is only text. Installing one proves nothing about the C# it later generates, which is why
  the guide offers a generation check.

## Pressure-tested, October 2026

All 14 non-package templates were expanded through Unity's own template engine in a disposable
Unity 6000.7.0b4 project, once with an empty Root Namespace and once with `Sample.Game`, with Enter
Play Mode set to skip domain reload. The result:

- **28 generated scripts, zero compile errors and zero warnings.**
- **One real finding, fixed.** The Static Event template reset its event by hand, and Unity's
  statics analyzer warned about it (`UAL0010`, `UAL0013`: static state needs a lifecycle attribute) in both
  namespace configurations. The template now marks the event with `[AutoStaticsCleanup]` (and the
  class `partial`). The new version compiled with no diagnostics on 6000.7.0b4 and 6000.6.2f1.
  The API is documented from 6.5; those two releases are the compile-tested versions. Before 6.5,
  defer the shipped template or separately select a custom adaptation with a manual reset.
- **Behavior check for Awaitable Operation.** A PlayMode test restarted the operation, disabled and
  re-enabled the object, cancelled twice, and destroyed it mid-run, and logged no errors or exceptions.
  Writing the template also exposed a compiler warning (`CS4014`, an un-awaited call), fixed with an explicit discard.
- **Not tested:** the EditMode and PlayMode test templates and the NetworkBehaviour template (they need
  Test Framework and Netcode, validated earlier in this repository's [validation record](../../Validation.md)),
  the logging path for a faulting operation, and the runtime *behavior* of the Static Event reset
  (two Plays in a row).

Decisions already made:

- **`sealed` everywhere** is now documented in the [style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md).
  Drop it from a class you plan to inherit from.
- **The IMGUI Custom Editor now uses `DrawDefaultInspector()`**, so it shows the Script field like the UI
  Toolkit one.
- **Editor UI.** Unity recommends UI Toolkit for new Editor tools; the IMGUI templates remain for
  projects and drawers that still need them.
