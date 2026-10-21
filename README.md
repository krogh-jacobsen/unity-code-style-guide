# A Unity C# Style Guide for LLMs

While there's no single "correct" way to format Unity C# code, agreeing on a consistent style makes it much easier to build a clean, readable, and scalable codebase as a team. It's about removing the guesswork and deciding on a standard that works best for your needs. It also helps your favorite LLMs  provide specific context on your preferences so they can match it.

That said, a style guide is only valuable if it's actually put into practice. This repo is my attempt at making that easy and LLM friendly too. It's a set of instruction files you can drop into a new Unity project so your assistant follows your conventions from the first script.

### The repo has since expanded

What started as "just" some C# guidelines mostly for users has since evolved to be optimized for LLM usage and so the repo now also contains a number of additional LLM instructions and resources I find helpful when starting a new project. With the current and latest update you will notfice some signicant changes from earlier versions

The basic idea is that you just pick and choose what works for you.  Many of the rules  are stylistic preferences, not industry consensus. Change them freely as
long as you change them everywhere.

### How to "install"

Simply copy files you are interested in into your Unity project.  It is ready to use as-is and as long as you include the agent.md file the LLM will pickup on the rest.


However, feel free to adapt agent.md  and everything else as you want to your specific needs.


## How this repo is organised

| Area | Role | Adaptation |
|---|---|---|
| [AGENTS.md](AGENTS.md) | Default project conventions, guardrails, and on-demand pointers | Set the project's stack and decisions |
| [CodeStyleGuide](CodeStyleGuide/UnityStyleGuide.md) | Naming and formatting preferences, with examples | Adapt taste and keep `.editorconfig` aligned |
| [AuditGuides](AuditGuides/README.md) | Focused review lenses: risks, evidence, and validation | Load only the applicable subsystems |
| [SetupInstructions](SetupInstructions/README.md) | One-time stack, settings, structure, and import configuration | Tailor to the actual project |
| [EditorConfig](EditorConfig/README.md) | The shipped `.editorconfig` and its explanation | Copy `.editorconfig` to the target root |
| [Base audit workflow](Skills/unity-guide-audit/UnityProjectReview.md) | Checks documented project conformance | Reference from the project's audit workflow |

[AuditGuides](AuditGuides/README.md) complement installed Unity skills. Skills own implementation,
diagnosis, and tool execution; the guides identify what evidence a review needs and the recurring
failure cases to verify. They do not require a particular plugin and are not loaded wholesale for
a small change. Project choices take precedence over generic skill defaults.

## Using it with your assistant

| Tool | Instruction entry point |
|---|---|
| **Claude Code** | `CLAUDE.md`, pointing to `AGENTS.md` |
| **OpenAI Codex** | `AGENTS.md` in the repo root |
| **GitHub Copilot** | `.github/copilot-instructions.md` |
| **Cursor** | `.cursorrules` or a file under `.cursor/rules/` |
| **JetBrains AI / Junie** | `.junie/guidelines.md` |

Copy the folders you need and put `AGENTS.md` at your project's instruction entry point. Keep copied
references together or update their paths. `CLAUDE.md` points back to the canonical `AGENTS.md`.
Adapt the Project Setup block and [tech-stack template](SetupInstructions/UnityTechStack.md) to the
same actual engine/packages and systems before using them in a Unity project.

For an audit, `AGENTS.md` points to [the audit index](AuditGuides/README.md), which selects the
relevant subsystem lenses. The [base workflow](Skills/unity-guide-audit/UnityProjectReview.md) adds
conformance to your style and setup rules; a broader project-audit skill can add architecture,
behavioral coverage, documentation drift, and unfinished-plan reconciliation.

## What goes in agents.md

The rule of thumb is that AGENTS.md should only hold what's true in every session, such as the non-negotiable rules, universal code style, and pointers. Anything that's true only when working on one subsystem, running one workflow, or investigating one historical question belongs in the complementary files.

Copy the agent.md  file into your own repo and edit the
**Project Setup** block below — everything else is ready to use as-is.

Rules marked `[opinion]` are stylistic preferences, not industry consensus. Change them freely as
long as you change them everywhere. Other guidance includes technical guardrails and defaults; apply it to the actual
project and validate version-sensitive behavior.

Unity starter kit

A selectable starter kit for Unity 6.7 projects: compact agent conventions, setup contracts,
on-demand review guides, reusable import presets and script templates, and a small UI Toolkit example.
This repository is documentation/resources, not a Unity project. Your project's actual version
and resolved packages govern implementation; see [the profile](SetupInstructions/UnityTechStack.md)
and [tested compatibility](Validation.md).

## Installation

Start with [SetupInstructions](SetupInstructions/README.md). Prefer Unity CLI for Editor discovery,
project creation, imported-asset changes, tests, and builds. Available Unity skills supply execution
mechanics; manual Editor steps remain a fallback. Copy only selected material. Preview destination
conflicts and merge existing configuration; do not overwrite a project's settings, conventions, or
asset identities silently. Preserve existing `.meta` files when installing/updating reusable assets.

| Source here | Destination in a target project | Selection |
|---|---|---|
| README.md, LICENSE | Project root (merge README; retain kit license attribution) | Installation index and resource license |
| AGENTS.md | Project root/AGENTS.md | Merge essential conventions and routing |
| CLAUDE.md | Project root/CLAUDE.md | Optional compatibility pointer |
| CodeStyleGuide/ | Project root/CodeStyleGuide/ | Owned C# conventions |
| SetupInstructions/**/*.md | Project root/SetupInstructions/ matching paths | Setup contract and all small resource indexes |
| AuditGuides/ | Project root/AuditGuides/ | On-demand review references |
| EditorConfig/.editorconfig | Project root/.editorconfig | Merge rules; do not overwrite existing config |
| EditorConfig/Unity.gitattributes | Project root/.gitattributes | Optional; configure tools first |
| EditorConfig/README.md | Project root/EditorConfig/README.md | Config rationale and prerequisites |
| SetupInstructions/ScriptTemplates/*.cs.txt + matching .meta | Assets/ScriptTemplates/ | Five default templates |
| SetupInstructions/OptionalScriptTemplates/ | Selected files only into Assets/ScriptTemplates/ | Prerequisites listed in template index |
| SetupInstructions/Presets/{Textures,Audio,Models,Animations}/ | Assets/Settings/Presets/ matching subfolders | Selected preset categories, preserve metadata |
| ExampleCode/UIToolkitMVP/ except Markdown | Assets/Examples/UIToolkitMVP/ | Optional runnable assets and isolated tests |
| ExampleCode/**/*.md | Project root/ExampleCode/ matching paths | Small example index and setup documentation |
| Validation.md, CHANGELOG.md | Project root or retained kit checkout | Compatibility and update evidence |

The instruction installation includes the linked documentation/indexes even when asset resources
are not selected. Keep Markdown outside Assets. Root `.editorconfig` is the installed config. When changing the copy layout, adapt links in AGENTS
and indexes.
Import asset resources into the target through the Editor, driven by CLI; imported moves use
AssetDatabase. Installing the example preserves its internal relative stylesheet and GUID references.

## Loading model

| Material | When loaded |
|---|---|
| AGENTS.md | Every session: essentials and routing |
| CodeStyleGuide | First relevant task authoring/reviewing owned C# |
| SetupInstructions | New project/configuration work |
| AuditGuides | Requested project/change/subsystem review |
| ExampleCode | Implementation relevant to a selected demonstration |
| Unity skills | Matching execution task; obey target project/user choices |

Examples demonstrate specific failure cases, not a required architecture. Keep a small verified
library; see [example index](ExampleCode/README.md). Audit guides describe risks/evidence rather
than copying Unity skill tutorials.

## Maintenance

Run `python3 Tools/validate_starter.py` for local references, anchors, inventory, template tokens,
GUID uniqueness, and policy drift. Run `python3 Tools/check_naming.py` for actual naming
analyzer intersections. Neither substitutes for Unity import/runtime validation. Follow
[Validation.md](Validation.md) when changing assets, templates, or the example; update the short
[change log](CHANGELOG.md) and record exact tested versions. Keep setup optional and rerunnable.

License: [MIT](LICENSE).