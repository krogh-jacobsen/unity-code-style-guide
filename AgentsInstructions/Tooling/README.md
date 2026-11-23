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
| Apply the Unity rules at review time instead of loading them while writing | [Review subagent](#review-subagent) |
| Keep `Library/` and other generated folders out of searches | [Keep generated folders out of context](#keep-generated-folders-out-of-context) |
| Keep the root file short while a subsystem has its own rules | [Scoped instructions](#scoped-instructions) |
| Load the Unity C# rules only when C# files are touched | [Load the C# rules by path](#load-the-c-rules-by-path) |
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

## Review subagent

Loading every design rule while writing code costs context on every task. A review subagent reads the
rules after the change instead, in its own context, and returns only findings. The main conversation
stays lean, and the review still applies the full rule set.

`.claude/agents/unity-code-reviewer.md`:

```markdown
---
name: unity-code-reviewer
description: Reviews changed C# against the project's Unity rules and style guide, and reports findings without editing.
tools: Read, Grep, Glob, Bash
---

Review only the C# the caller names, or the uncommitted changes from `git diff`. Do not edit files.

Read AGENTS.md, then AgentsInstructions/UnityProjectRules/UnityRules.md and the style guide sections
the change touches. AGENTS.md wins where they conflict.

Report each finding as file:line, the rule, why it matters, and the suggested fix. Group them:
1. Unity bugs the compiler won't catch (from AGENTS.md)
2. Design rules (unmarked rules in UnityRules.md)
3. Preferences (rules marked [opinion]), labelled as optional
Say "No findings" when there are none, and name anything you could not check.
```

The `tools` field cannot limit Bash to read-only commands. If the reviewer must not change files, add a
Bash deny rule or a `PreToolUse` hook, or drop Bash and pass the diff in the request. A skill works the
same way when you would rather start the review by name.

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

### Load the C# rules by path

The [Unity rules](../UnityProjectRules/UnityRules.md) matter for nearly every code task, but a link from
`AGENTS.md` can go unread. A path-scoped rule puts a pointer in front of the agent the moment it reads or
edits C#, and costs nothing on asset or documentation tasks.

`.claude/rules/unity-csharp.md`:

```markdown
---
paths:
  - "Assets/**/*.cs"
---

Before writing or reviewing C#, read AgentsInstructions/UnityProjectRules/UnityRules.md and follow it.
Where it conflicts with AGENTS.md, AGENTS.md wins.
```

Adjust the folder to where you copied the kit. The pointer is a plain instruction because `@path` imports
are documented for `CLAUDE.md`, not for rule files.

- **GitHub Copilot:** the same body in `.github/instructions/unity-csharp.instructions.md`, with
  `applyTo: "Assets/**/*.cs"` as its frontmatter. GitHub documents path-specific files for the Copilot
  cloud agent and code review.
- **Cursor:** project rules can be scoped by file pattern. The format was not verified here; check
  Cursor's documentation.

Imports (`@AGENTS.md`) organize files but do not save context, because the imported file loads with its
parent. Use a thin `CLAUDE.md` that imports `AGENTS.md` so tools share one source of truth:

```markdown
@AGENTS.md

Update shared rules in AGENTS.md. Do not duplicate them here.
```

## Keep generated folders out of context

`Library/`, `Temp/`, `Logs/`, `obj/` and `UserSettings/` are regenerated by Unity and can hold
gigabytes. One search that wanders into them can fill the context. `AGENTS.md` says to skip them; a
deny rule makes the file tools skip them too.

`.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Read(/Library/**)",
      "Read(/Temp/**)",
      "Read(/Logs/**)",
      "Read(/obj/**)",
      "Read(/UserSettings/**)"
    ],
    "allow": [
      "Bash(unity commands *)"
    ]
  }
}
```

- A leading `/` anchors the path at the project that holds the settings file. `./` depends on where the
  session started.
- Claude Code applies `Read` deny rules to Grep and Glob on a best-effort basis. They do not stop a shell
  command such as `grep -r pattern .`, so keep the line in `AGENTS.md`. A `.claudeignore` file has no effect.
- The `allow` entry stops a prompt for listing Unity CLI commands. Add your test command only if routine
  test runs should not ask; the [test-runner subagent](#test-runner-subagent) decides which tests are authorized.

Checked against Claude Code's permissions documentation, November 2026.

## Keep it honest

- Add a rule after the agent repeats a mistake, not in advance.
- Leave naming and formatting to `.editorconfig` and the compiler.
- Do not describe the folder layout. The agent reads the repo.
- A fact lives in one file. Link to it from everywhere else.
