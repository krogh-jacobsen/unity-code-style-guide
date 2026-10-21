# Editor configuration

Merge `EditorConfig/.editorconfig` from this kit into the target project's root `.editorconfig`. It encodes the enforceable
subset of [the style policy](../LLMInstructions/CodeStyleGuide/UnityStyleGuide.md); ownership, serialized migrations,
member order, and architectural choices still require review. C# uses four spaces; UXML/USS two.

## Naming analyzers

Modern Roslyn chooses naming rules by specificity, not declaration order. Constants are also
static, so the private constant group explicitly requires both modifiers. It outranks the static
and plain private field groups. Lookup constants use PascalCase; properties PascalCase; interfaces
an I prefix. Exceptions for external data contracts may need a scoped analyzer suppression.

Severities here are suggestions for IDE feedback. Unity compilation does not automatically enforce
Roslyn IDE naming diagnostics, and setting a naming severity alone does not make every build enforce
it. If CI enforcement is selected, install a compatible analyzer/formatter runner, explicitly select
IDE1006, and verify representative intersections. Use
`python3 Tools/check_naming.py` in this kit checkout for good/bad fixtures against the installed
.NET SDK's Roslyn through `dotnet format`; record its version in [Validation](../Validation.md).
This is separate from Unity CLI compilation/testing, which verifies Unity code and dependencies.

Unity serialized formats, including `.preset`, are excluded from whitespace rewrites. Binary files
also retain their original bytes. These settings guide compatible formatters; still scope formatting
to owned source and inspect the diff. Do not run a general text formatter over Unity assets.

## Git attributes

[Unity.gitattributes](Unity.gitattributes) is an optional starter. Merge it after selecting actual
binary asset categories and verifying team/CI prerequisites. It does not install a merge driver.

Prefer Unity CLI: inspect `unity vcs merge-setup --help` and `unity vcs git --help` for the installed
version's supported setup/status checks. Configure UnityYAMLMerge/SmartMerge using the selected
Editor executable and local Git configuration, then verify an actual scene merge in a disposable
branch. `.meta` stays text; identity conflicts require review, not a binary/LFS rule.

LFS patterns in the starter are commented out. Enable selected ones only after Git LFS is installed
on every workstation and CI (`git lfs install`, then verify tracked paths). Existing large files need
an explicitly planned migration; adding attributes does not rewrite history. Confirm repository host
storage/bandwidth requirements before enabling LFS for all textures/audio/models.

Manual fallback: configure Git attributes, Git LFS, and UnityYAMLMerge following the installed
Editor/Git documentation. Completion: line endings preserve assets, a test SmartMerge invokes the
configured driver, and selected LFS files are pointer files in Git with working checkout content.
