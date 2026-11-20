# AGENTS.md

Copy this file to your Unity project root, fill in **This project decides**, and delete what does not apply.
Keep it short: add a rule only after the agent got something wrong, and leave out anything it can
discover by reading the repo or that `.editorconfig` and the compiler already enforce.

The links below are written for this file inside the `AgentsInstructions` folder. After you copy it to
your project root, prefix them with that folder's location, for example `AgentsInstructions/`.

## This project decides

These choices beat the generic examples in the linked documents. Fill in every row you know.

| Decision | Value |
|---|---|
| Unity version | _From `ProjectSettings/ProjectVersion.txt`; record the date you checked it_ |
| Render pipeline | _URP, HDRP or Built-in_ |
| Input | _Input System or legacy_ |
| Runtime UI | _UI Toolkit or uGUI_ |
| Async | _Awaitable, coroutines or both_ |
| Domain reload on Enter Play Mode | _On or off. Static resets must work either way_ |
| Protected folders | _Vendor code, `Packages/`, generated output. Wrap, do not edit_ |
| Test command | _The exact command that runs EditMode tests_ |

## Unity safety

- **Assets go through Unity.** Create, move, rename and delete assets with Editor APIs or Unity CLI.
  Never hand-edit `*.unity`, `*.prefab`, `*.asset` or `*.meta`, and never delete a `.meta` to reset
  import settings. Raw YAML edits can break GUID and fileID references without a compile error.
- **Generated assets have an owner.** If a builder or tool generates a prefab, change the builder and
  regenerate. Do not patch the output.
- **Preserve what is not yours.** Keep concurrent edits, unsaved scenes and existing serialized field
  names (`[FormerlySerializedAs]` when renaming).
- **Prefer the project's Unity CLI skill** for compiling, testing and Editor control instead of
  guessing commands.

## Verification

- Before saying "done": compile, run the EditMode tests, and confirm the console is clean.
- Zero tests run, a cached result, or "command accepted" is not a pass. Read the fresh result.
- Editor compilation does not prove the player build compiles.
- Report automated checks and what a player would see as separate results. A UI object existing
  does not mean it is visible.
- Say what you did not verify.

## Working rules

- **Reproduce first.** Before changing tuning or settings to fix a bug, reproduce the symptom.
- **Fix at the owner.** Correct the prefab, tool or data that owns the problem, not the scene-local symptom.
- **Smallest useful change.** Return anything outside the requested scope as a suggestion.
- **Audit before changing an existing project.** Report differences, list the proposed changes, and
  wait for the exact list to be confirmed.

## Where to read more

| When you are… | Read |
|---|---|
| Writing or reviewing C# | [Unity rules](UnityProjectRules/UnityRules.md), then the [style guide](CodeStyleGuide/UnityStyleGuide.md) |
| Choosing APIs or packages | [Tech stack](UnityTechStack/UnityTechStack.md) |
| Enforcing a rule with a hook, or delegating tests | [Tooling](Tooling/README.md) |

Add a document here only for a distinct, recurring task, and give it one loading condition.

## Precedence

When instructions conflict: the user's request, then this file, then the linked documents, then
skill defaults.
