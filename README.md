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
