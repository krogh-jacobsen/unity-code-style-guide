# Unity assembly and build-boundary audit

Load for compilation boundaries, Editor/player isolation, tests, or package references. Apply the
[shared evidence standard](README.md#evidence-standard). Respect the project's assembly policy,
including an explicit no-asmdef choice. Use project build tooling or `unity-cli` for validation.

## Establish effective boundaries

Map each reviewed script to its effective assembly and platform constraints, including parent
asmdefs, asmrefs, predefined assemblies, package assemblies, and precompiled plugins. Read actual
references and defines. Folder names alone do not establish compilation boundaries once asmdefs apply.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Player isolation | `UnityEditor` types/usings, enclosing defines, effective assembly | Editor code or API dependencies are compiled into a normal player |
| Editor folder under an asmdef | Inherited assembly and Editor-only child asmdef | Folder naming is incorrectly relied on to isolate Editor code |
| Reference direction | Assembly references and actual source/asset dependencies | A cycle exists or a binding project dependency rule is violated |
| Test inclusion | Test assembly marking, platform/define constraints, runner, build settings | A normal player actually includes tests or references test-only APIs |
| Optional packages | Package presence, assembly references, version/define constraints | A supposedly optional package is required by an unguarded assembly or API |
| AOT and stripping | Reflection, generated code, preservation, target backend | A used runtime type/member is absent in a representative stripped build |
| Granularity | Change/recompile scope and dependency fan-out | Boundaries produce measured iteration cost or enforce no useful separation |

## Interpret with care

- Absence of asmdefs is not itself a correctness defect. Recommend a boundary for a concrete
  dependency or build problem, with migration cost; avoid script-count thresholds.
- `autoReferenced` controls references from predefined assemblies. It does not mean every asmdef
  references the library. Judge the intended visibility rather than requiring one global value.
- `rootNamespace` assists new-script creation; leaving it empty does not make existing namespaces
  incorrect. Naming belongs to [the style guide](../CodeStyleGuide/UnityStyleGuide.md).
- A missing `UNITY_INCLUDE_TESTS` constraint alone does not prove tests ship. Account for test-assembly
  marking, Editor-only platform restrictions, other defines, and normal versus test-player builds.
- Interfaces can resolve dependency cycles, but moving a type to Core is appropriate only if Core
  owns that contract. Sometimes an artificial boundary should be consolidated.

## Validation

Compile both the Editor and a representative normal player target for affected boundaries. Verify
relevant test discovery with [Testing](UnityTestingInstructions.md); test-player inclusion is a
separate case. Report build-only checks as Not verified if no build was run.

Technical references: [Assembly definitions](https://docs.unity3d.com/6000.0/Documentation/Manual/assembly-definitions-intro.html)
and [test modes and assembly setup](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/edit-mode-vs-play-mode-tests.html).
Use the installed Test Framework version for exact assembly requirements.
