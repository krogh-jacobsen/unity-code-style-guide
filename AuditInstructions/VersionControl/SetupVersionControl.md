> How it works: give this URL to your agent, for example "Set up Git for my Unity project from this
> document". The agent audits the project's Git rules, recommends what to install, lets you pick which
> to carry over, and writes nothing until you confirm the exact change list. Then it verifies the
> result with Git. It changes nothing in the Unity project. Human overview: [readme](README.md).

# Set up version control for a Unity project (agent instructions)

Install a Unity `.gitignore` and `.gitattributes` into an existing project, then verify them. This
document is self-contained. It does not commit, push, rewrite history, or untrack files without the
user's approval, and it changes no Unity setting. **Last verified: October 2026** (Git 2.54, Git LFS
3.8.0, Unity CLI 1.0.0-beta.13, Unity 6000.7.0b4 and 6000.6.2f1).

Source (replace `main` with a commit SHA for a repeatable run):
`https://raw.githubusercontent.com/krogh-jacobsen/unity-code-style-guide/main/AuditInstructions/VersionControl/`
Two files: `Unity.gitignore` and `Unity.gitattributes`.

## Operating rules

- **Managed blocks only.** Each file is one block between `# BEGIN unity-code-style-guide: …` and
  `# END unity-code-style-guide: …` lines. Insert it, or replace the previous copy in place, and
  leave every line outside it exactly as it is. A project's own rules stay.
- Never commit, push, `git rm`, `git filter-repo`, or change `.git/config` or hooks without approval.
  Show the command and its effect first.
- Never hand-edit Unity files. Serialization and meta-file settings are read, not changed, here.
- Report observed results separately from checks you could not run (**Not verified**).

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit yes.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Restate the exact changes for the picked subset (files, settings, values, commands)
   and wait for an explicit yes. Make no change before it, including saving the report. In a
   non-interactive session, or when no answer arrives, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

## 1. Preflight

Identify one Unity project (it contains `Assets` and `ProjectSettings/ProjectVersion.txt`) and its Git
repository. Record:

- **Project root versus repository root.** The ignore rules start with `/`, so `.gitignore` goes in the
  **project root**. `.gitattributes` goes in the **repository root**. They are the same folder in most
  projects. If the project sits in a subfolder of a larger repository, say so.
- Whether the folder is a Git repository, and its remote. Do not run `git init` or create a remote
  unless asked; `unity vcs setup` exists for creating one.
- Existing `.gitignore` and `.gitattributes`, and whether either already holds a managed block here.
- `git --version`, `git lfs version` (installed? hooks present in this repository?), and whether the
  `unity` CLI is available (`unity vcs doctor --help`).
- **Settings that decide whether any of this works:** *Asset Serialization* is Force Text and
  *Version Control Mode* is Visible Meta Files (Project Settings > Editor and Version Control; the
  [project settings guide](../ProjectSettings/ProjectSettings.md) owns them). With the CLI,
  `unity vcs doctor` reports both. Without it, read `ProjectSettings/EditorSettings.asset`
  (`m_SerializationMode: 2`) and `ProjectSettings/VersionControlSettings.asset` (`m_Mode: Visible Meta Files`).
- Tracked files these rules would now exclude, after step 3.

**Done:** project root, repository root, existing rules, tool availability, and the two settings are
known, and no file has been written.

## 2. Ask and select

Ask in one batch. The defaults are recommended answers: they become recommendations that still go
through stages 3 and 4, even when the user says "use defaults".

| Question | Default |
|---|---|
| Keep `Assets/ThirdPartyAssets/` out of Git? Contributors then re-import vendor assets, and CI needs a way to fetch them | Yes, the starter's [folder layout](../FolderStructure/SetupFolders.md) convention. **Warn about clean clones and CI before applying** |
| Use Git LFS for textures, models, audio, video and source art? | Yes when `git lfs` is installed, otherwise no (report it) |
| Configure scene and prefab merging (`unity vcs merge-setup`)? | Yes when the `unity` CLI and the project's Editor are present |
| Install LFS hooks in this repository (`git lfs install --local`)? | Yes when LFS is selected |
| Commit the result? | No: leave the files in the working tree |

**Done:** the three choices (ThirdPartyAssets, LFS, merge setup) are explicit recommendations the
user has picked or declined.

## 3. Install

Only the items confirmed in stage 4 are installed.

1. **Stage.** Download both files into a temporary folder outside the project. Reject HTML or error
   responses. Each file must contain exactly one `BEGIN unity-code-style-guide` and one `END` line.
2. **Trim by choice.** If the user declined a section, delete it with its marker lines from the
   staged copy: `# BEGIN ThirdPartyAssets` to `# END ThirdPartyAssets` in the ignore file, and
   `# BEGIN LFS` to `# END LFS` in the attributes file. Nothing else is removed.
3. **Apply.**

   | Destination state | Action |
   |---|---|
   | File absent | Write the staged block as the file |
   | File exists, no block | Append the block after a blank line |
   | Block present and identical | Already installed: leave it |
   | Block present and different | Replace only the lines from `BEGIN` to `END` |

   If a project rule outside the block contradicts the block (for example `!*.log` or a rule that
   ignores `.meta` files), keep it and report it: a project may override, but an ignored `.meta` file
   breaks references.
4. **Merge setup (if selected).** `unity vcs merge-setup` writes a managed block of
   `merge=unityyamlmerge` attributes to `.gitattributes` and the merge driver to the repository's
   `.git/config`, then proves it with a test merge. The driver names an absolute Editor path, so it is
   **per clone** and each contributor runs it once. Run `--check` first. Without the CLI, report merge
   setup as **Not verified** and point to the manual route in the
   [Unity manual](https://docs.unity.com/en-us/engine/6000.7/manual/get-started/project-configuration/version-control/smart-merge)
   (the tool is `Contents/Helpers/UnityYAMLMerge` in a macOS Editor and
   `Editor\Data\Tools\UnityYAMLMerge.exe` on Windows).
5. **LFS hooks (if selected).** Run `git lfs install --local` once approved.

**Done:** the audit and recommendation list were shown and confirmed before any write, both files
hold the current block for the confirmed items, the declined sections are absent, and a repeat run
changes nothing.

## 4. Files Git already tracks

Run `git ls-files -ci --exclude-standard`. It lists tracked files that the new rules exclude. Group the
output (generated folders, vendor content, captures, other) and propose, per group, the safe fix:
`git rm -r --cached <path>`. That removes the files from Git and keeps them on disk, but **on the next
pull every teammate's working copy of those files is deleted**. Spell that out for vendor content
(`Assets/ThirdPartyAssets`) before asking. Apply nothing without approval.

Large binaries already in history remain there after an ignore or LFS change. If the repository has
them, report it and point to `unity vcs git migrate-lfs`, which prints a history-rewriting command.
Do not run it: rewriting shared history needs the whole team's agreement.

**Done:** every tracked-but-excluded group is reported with its proposed action, or none exist.

## 5. Verify

1. **Ignore behavior.** `git check-ignore -v` on these sample paths must match: `Library/x`,
   `Logs/x`, `ProfilerCaptures/capture.data`, `MemoryCaptures/a.snap`, `Builds/Win/Game.exe`,
   and, when selected, `Assets/ThirdPartyAssets/Vendor/x.cs`. These must not match:
   `Assets/<Root>/Scripts/x.cs`, its `.cs.meta`, `ProjectSettings/ProjectSettings.asset`,
   `Packages/manifest.json`, and `Packages/packages-lock.json`.
2. **Attributes.** `git check-attr filter eol -- <path>` shows `filter: lfs` for a PNG, FBX and WAV
   (when LFS is selected), and `eol: lf` for a `.cs` and `.unity` file.
3. **Unity's checker.** `unity vcs doctor` should report nothing. With ThirdPartyAssets excluded it also
   reports `META_FILES_IGNORED` while that folder's `.meta` exists locally; that finding is expected (a
   clean clone does not trigger it), and any other finding is real. Without the CLI, report this as **Not verified**.
4. **Working tree.** `git status --short` lists the new or changed files and no Unity-generated folder.
5. **Settings.** Force Text and Visible Meta Files are confirmed in the preflight, or reported as gaps.

**Done:** each check is observed, or its absence is stated.

## 6. Report

| Item | Status | Detail |
|---|---|---|
| Source URL and revision | | |
| Audit and recommendations shown, confirmation received | Yes / Stopped before confirming | Items picked |
| Unpicked recommendations | Proposal | ID and reason |
| `.gitignore` | Installed / Updated / Already installed | Path |
| `.gitattributes` | Installed / Updated / Already installed | Path |
| ThirdPartyAssets excluded | Yes / No | Folder present? |
| LFS section and hooks | Applied / Declined / Not available | Git LFS version |
| Merge setup | Configured / Declined / Not verified | Editor used |
| Tracked-but-excluded files | None / N groups | Proposed commands |
| Ignore and attribute behavior | Passed / Not verified | |
| `unity vcs doctor` | Clean / Findings / Not verified | |
| Force Text and Visible Meta Files | Confirmed / Gap | |

Put the tracked-but-excluded groups, the ThirdPartyAssets warning, any contradicting project rule, and
unpicked recommendations that need a ruling in a "Needs your decision" block at the top. Close with what each contributor does once after cloning:
`git lfs install`, `unity vcs merge-setup`, and re-importing the excluded vendor assets. Continuous
integration needs Git LFS on its checkout step and a source for the excluded assets.
