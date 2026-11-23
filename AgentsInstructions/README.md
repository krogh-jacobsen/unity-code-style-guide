# Agent instructions

Material you copy into a Unity project so your LLM follows the same conventions every session. For
audits and setup workflows that you hand to an LLM by URL, see [AuditInstructions](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AuditInstructions/README.md).

| Folder or file | What it is |
|---|---|
| [AGENTS.md](AGENTS.md) | A short starter file for your project root: a fill-in block for your stack choices, Unity safety rules, verification rules, and a routing table |
| [UnityProjectRules](UnityProjectRules/UnityRules.md) | Coding principles: naming, state, class design, architecture, Unity pragmatism, error handling. Opinionated rules carry an `[opinion]` marker |
| [CodeStyleGuide](CodeStyleGuide/README.md) | The full Unity C# style guide, a ready-made `.editorconfig`, and a naming checker |
| [UnityTechStack](UnityTechStack/UnityTechStack.md) | The Unity 6.7 stack profile your LLM should assume, and a deprecated-API table |
| [Tooling](Tooling/README.md) | Copy-paste hooks, a test-runner subagent and scoped instructions, for rules a sentence cannot enforce |

## Using the starter AGENTS.md

1. Copy [AGENTS.md](AGENTS.md) to your project root, fill in **This project decides**, and adapt or
   delete **How to work with me**.
2. Copy this `AgentsInstructions` folder into your project too (for example next to it), and prefix the
   links in your `AGENTS.md` with the folder's location, such as `AgentsInstructions/`.
3. If your tool reads `CLAUDE.md`, add one containing `@AGENTS.md` so both share a single source of truth.
4. Add a rule only after the agent gets something wrong. A short file is followed better than a long one.

## Starter or root AGENTS.md?

This repository has two `AGENTS.md` files on purpose, and a project uses **one** of them.

- **This folder's [AGENTS.md](AGENTS.md)** is the lean starter above. Use it when you only want the
  agent instructions. Its links stay inside this folder, so it works without the rest of the kit.
- **The root [AGENTS.md](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/AGENTS.md)** is the full-kit version. It also holds the instructions for
  maintaining this repository, and the install workflow merges it into a project that adopts the audit
  and setup documents. See [which AGENTS.md to use](https://github.com/krogh-jacobsen/unity-code-style-guide/blob/main/README.md#which-agentsmd-to-use).
