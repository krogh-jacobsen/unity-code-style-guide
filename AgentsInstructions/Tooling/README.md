# Agent tooling for Unity projects

> **Applying this to an existing project:** audit first. Report where the project differs, list each
> proposed change, and let the user pick and confirm the exact list before editing anything, whether
> they handed over the whole kit or only this document. Writing new code under these rules needs no audit.

Instructions are advice. Use them for judgment calls, and use the tools below when a rule has no exceptions or a task is better delegated. Everything here is a copy-paste example: nothing is installed for you, and each snippet is yours to adapt. Last verified: November 2026, against Claude Code hooks,
subagents and memory docs. Check them again before relying on a detail.

| I want to… | Use |
|---|---|
| Stop the agent hand-editing Unity YAML or `.meta` files | [Block raw asset edits](#block-raw-asset-edits) |
| Run tests without flooding the main conversation | [Test-runner subagent](#test-runner-subagent) |
| Keep the root file short while a subsystem has its own rules | [Scoped instructions](#scoped-instructions) |
| Drive a live Editor, run builds, edit scenes | The official `unity-cli` skill. Do not restate its manual in `AGENTS.md` |

## Block raw asset edits

A `PreToolUse` hook enforces "never hand-edit `*.unity`, `*.prefab`, `*.asset` or `*.meta`" where a
sentence in `AGENTS.md` can be ignored. Exit code 2 blocks the call and sends the message to the agent.

`.claude/hooks/block-unity-yaml.sh`:

```sh
#!/bin/sh
# Requires jq. Reads the tool call as JSON on stdin.
file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  *.unity|*.prefab|*.asset|*.meta|*.mat|*.controller)
    echo "Blocked: edit Unity assets through Editor APIs or Unity CLI, not as text. Do not edit .meta files." >&2
    exit 2 ;;
esac
exit 0
```

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [{ "type": "command", "command": ".claude/hooks/block-unity-yaml.sh" }]
      }
    ]
  }
}
```

Limit: this guards the file-editing tools only. A shell command such as `sed -i` bypasses it, so keep
the written rule in `AGENTS.md` as well.

## Test-runner subagent

A subagent runs the tests and returns only the verdict and failures, so logs stay out of the main conversation. The authorization table is the part worth copying: it stops routine validation from becoming an approval request, and stops expensive suites from running unasked.

`.claude/agents/unity-test-runner.md`:

```markdown
---
name: unity-test-runner
description: Runs authorized Unity tests through Unity CLI and reports only the verdict and failures.
tools: Bash, Read
---

Run only the test category the caller names, using the project's documented test command.

| Situation | May run |
|---|---|
| Ordinary code change | EditMode unit tests |
| Issue implementation | The tests for the touched feature |
| Named request from the user | Exactly what was named |
| Anything else | Nothing. Reply `Deferred: <filter>; <effect> is outside the authorized scope.` |

Read the fresh results file or log. Zero tests run, cached output, command acceptance and an
interrupted run are not a pass. Report: command, counts, failing test names with the first error line,
and what was not run.
```

Find the exact test command with `unity commands --grep test` rather than copying one from a blog.
A Unity forum post suggests `unity test . --mode EditMode --output results.xml`. Not verified here.

## Scoped instructions

Context files cost tokens in every session, and long files lower adherence. Keep the root file short
and push subsystem rules down. Two supported ways:

- **Nested file.** Put a `CLAUDE.md` inside the subsystem folder (for example
  `Assets/Game/Networking/CLAUDE.md`). It loads only when the agent reads files below that folder.
- **Path-scoped rule.** A file under `.claude/rules/` loads only when matching files are touched:

```markdown
---
paths:
  - "Assets/**/Editor/**/*.cs"
---

Editor code stays in an Editor assembly or behind `#if UNITY_EDITOR`. Tools that change assets
support Undo and refuse to run in Play Mode.
```

Imports (`@AGENTS.md`) organize files but do not save context, because the imported file loads with its
parent. Use a thin `CLAUDE.md` that imports `AGENTS.md` so tools share one source of truth:

```markdown
@AGENTS.md

Update shared rules in AGENTS.md. Do not duplicate them here.
```

## Keep it honest

- Add a rule after the agent repeats a mistake, not in advance.
- Leave naming and formatting to `.editorconfig` and the compiler.
- Do not describe the folder layout. The agent reads the repo.
- A fact lives in one file. Link to it from everywhere else.
