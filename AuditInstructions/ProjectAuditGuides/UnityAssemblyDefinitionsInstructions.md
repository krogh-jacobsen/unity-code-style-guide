# Unity assembly and build-boundary audit

Load for compilation boundaries, Editor/player isolation, tests, or package references. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Respect the project's assembly policy,
including an explicit no-asmdef choice. Use `unity:unity-cli` (fallback: the Editor's compile and
build commands) for validation. **Last verified: October 2026.**

This lens owns test inclusion, normal-player isolation, and Editor folders under an asmdef. Stripping
and AOT belong to [Assets and memory](UnityAssetsAndMemoryInstructions.md); [Testing](UnityTestingInstructions.md)
links here for inclusion.

## Establish effective boundaries

Map each reviewed script to its effective assembly and platform constraints, including parent
asmdefs, asmrefs, predefined assemblies, package assemblies, and precompiled plugins. Read actual
references and defines. Folder names alone do not establish compilation boundaries once asmdefs apply.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Player isolation | `UnityEditor` usings and types, enclosing `#if UNITY_EDITOR`, effective assembly, platform filter | A `using UnityEditor` (or a `UnityEditor` type) sits in an assembly with no Editor-only filter and no `UNITY_EDITOR` guard; confirm with a compile of a normal player target (needs a build) |
| Editor folder under an asmdef | Scripts in an `Editor` folder and their effective assembly | The folder sits under a runtime asmdef with no Editor-only asmdef or asmref, so only the folder name isolates the code |
| Platform filters | `includePlatforms` and `excludePlatforms` in every `.asmdef` | Both arrays hold values (the file-format reference requires `includePlatforms` to be empty when `excludePlatforms` has values), or an assembly meant to be Editor-only lists any platform besides the Editor |
| Reference resolution | `references` in every `.asmdef` and `.asmref`; the `guid:` in each asmdef `.meta` | A `GUID:<hash>` or an assembly name matches no asmdef in the project or its resolved packages, or one `references` list mixes the GUID and name forms (the reference requires one form per list) |
| Reference direction | The reference graph built from `references`, plus actual source dependencies | A cycle exists in the graph, or a binding project dependency rule is violated |
| Test inclusion | Test asmdefs, every non-test asmdef's `references`, the output of a normal player build or its build report | A normal player build or build report contains a test assembly, or a non-test asmdef lists a test asmdef, NUnit, or `UnityEngine.TestRunner` in `references`; the build-side half needs a build |
| Optional packages | `manifest.json` / `packages-lock.json`, asmdef `references`, `versionDefines`, `defineConstraints` | An asmdef references a package assembly that the project treats as optional, with no `versionDefines` plus `defineConstraints` guard, so it cannot compile when the package is absent |
| Granularity | Editor compile log or `unity:unity-cli` compile timing after a one-file edit | A recorded recompile of one assembly follows an edit that none of its dependents use, and the timing is large enough to matter to the project's iteration goal; report the measurement, never a script count (needs a live compile) |

ℹ️ AOT and stripping findings belong to [Assets and memory](UnityAssetsAndMemoryInstructions.md).

## Interpret with care

- ℹ️ Absence of asmdefs is not itself a correctness defect. Recommend a boundary for a concrete
  dependency or build problem, with migration cost; avoid script-count thresholds.
- ℹ️ `autoReferenced` defaults to true and controls references from predefined assemblies. It does not
  mean every asmdef references the library. Judge the intended visibility rather than requiring one
  global value.
- ℹ️ An empty `rootNamespace` does not make existing namespaces incorrect; verify in the installed
  Editor what the field controls. Naming belongs to [the style guide](../../AgentsInstructions/CodeStyleGuide/UnityStyleGuide.md).
- ⚠️ `UNITY_INCLUDE_TESTS` appears in Unity's file-format reference only as an example
  `defineConstraints` value; the manual does not describe what it does. Unity's manual says test assemblies
  are not part of the regular build pipeline and ship only for Play Mode tests run in a Player, but verify
  that in the installed Editor. A missing or present constraint alone proves nothing: decide by a player
  build or build report.
- ℹ️ Interfaces can resolve dependency cycles, but moving a type to Core is appropriate only if Core
  owns that contract. Sometimes an artificial boundary should be consolidated.

## Validation

Compile both the Editor and a representative normal player target for affected boundaries. Verify
relevant test discovery with [Testing](UnityTestingInstructions.md); test-player inclusion is a
separate case. Report build-only checks as Not verified if no build was run.

Technical references: [Assembly definitions](https://docs.unity3d.com/Manual/assembly-definitions-intro.html),
[file format](https://docs.unity3d.com/Manual/assembly-definition-file-format.html), and
[creating assemblies and test assemblies](https://docs.unity3d.com/Manual/assembly-definitions-creating.html).
Use the installed Test Framework version for exact assembly requirements.
