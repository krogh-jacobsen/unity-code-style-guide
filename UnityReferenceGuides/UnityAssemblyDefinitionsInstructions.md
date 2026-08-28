# Unity Assembly Definitions

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Assembly definitions (`.asmdef`) split your scripts into separate compiled assemblies instead of one
monolithic `Assembly-CSharp.dll`.

They buy two things: **compile time** (change a leaf assembly, only it and its dependents rebuild)
and **enforced architecture** (a reference that doesn't exist is a compile error, not a code review
comment). They cost you a dependency graph to maintain — which is the point, but it is real work.

Table of contents:
- [When to use them](#when-to-use-them)
- [When not to](#when-not-to)
- [Naming](#naming)
- [A starting structure](#a-starting-structure)
- [Dependency rules](#dependency-rules)
- [Circular references](#circular-references)
- [Editor-only assemblies](#editor-only-assemblies)
- [Test assemblies](#test-assemblies)
- [rootNamespace](#rootnamespace)
- [Version defines for optional packages](#version-defines-for-optional-packages)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## When to use them

- ✅ Script compilation after a one-line change takes more than about **5 seconds**.
- ✅ You want to stop gameplay code referencing Editor code, or UI referencing data-layer internals,
  and you want the compiler to enforce it.
- ✅ You need `InternalsVisibleTo` for tests — see [Test assemblies](#test-assemblies).
- ✅ You're shipping a package or reusable module.
- ✅ You need per-platform compilation (`includePlatforms` / `excludePlatforms`).

## When not to

- ❌ **Fewer than ~10 scripts.** The dependency management costs more than the compile time saves.
- ❌ One assembly per folder, or per script. Group by *system*, not by directory.
- ❌ Purely to organise code — namespaces already do that. Assemblies are compilation and dependency
  boundaries.
- ⚠️ Adding asmdefs to a large existing project is disruptive: everything in `Assembly-CSharp` can
  see everything else today, and splitting it will surface every hidden dependency at once. Do it
  incrementally, starting with leaf systems that nothing depends on.

---

## Naming

- ✅ Name the assembly the same as its root namespace: `MyGame.Combat`, `MyGame.UI`.
- ✅ Name the `.asmdef` file to match the assembly name.
- ✅ Suffix Editor assemblies `.Editor` and test assemblies `.Tests` / `.Tests.EditMode`.
- ⚠️ The **Name** field inside the file is what matters, not the filename. Unity uses the field; a
  mismatch just confuses humans.
- ✅ Prefix everything with your project or company name so a package you import later can't collide.

---

## A starting structure

```
Assets/Scripts/
├── Core/            MyGame.Core.asmdef          — no dependencies
├── Data/            MyGame.Data.asmdef          — ScriptableObjects, plain models
├── Gameplay/        MyGame.Gameplay.asmdef      — → Core, Data
├── UI/              MyGame.UI.asmdef            — → Core, Data   (NOT Gameplay)
└── Editor/          MyGame.Editor.asmdef        — → everything, Editor platform only

Tests/
├── EditMode/        MyGame.Tests.EditMode.asmdef
└── PlayMode/        MyGame.Tests.PlayMode.asmdef
```

```json
{
    "name": "MyGame.Gameplay",
    "rootNamespace": "MyGame.Gameplay",
    "references": ["MyGame.Core", "MyGame.Data", "Unity.InputSystem"],
    "includePlatforms": [],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false,
    "autoReferenced": true,
    "defineConstraints": [],
    "versionDefines": [],
    "noEngineReferences": false
}
```

- ✅ Note **UI does not reference Gameplay.** UI observes state through events or an interface defined
  in Core. That one constraint prevents most of the coupling that makes UI painful to change later.
- ✅ `Core` should reference nothing of yours. If it needs something, that something belongs in Core.

---

## Dependency rules

- ✅ Dependencies point **inward**: UI and Gameplay depend on Core and Data; nothing depends on UI.
- ✅ When two assemblies need to talk both ways, put the interface (or the event) in the one they both
  already depend on.
- ⚠️ `autoReferenced: true` means *predefined* assemblies (`Assembly-CSharp`) can see this one. Set it
  to `false` on library assemblies you want explicitly referenced.
- ⚠️ `noEngineReferences: true` drops the `UnityEngine` reference. Useful for pure C# domain logic —
  and a good forcing function for testability, per
  [Testing](UnityTestingInstructions.md#writing-testable-game-code).
- ✅ Adding a reference is cheap to type and expensive to remove. Question every one.

---

## Circular references

Unity refuses to compile a cycle: *"Assembly with name 'X' has a circular reference to 'Y'"*. There
are three ways out, in order of preference:

1. **Extract the shared piece.** If `Gameplay` and `UI` both need `IPlayerStats`, it belongs in
   `Core`. This is nearly always the right answer.
2. **Invert with an interface.** The lower assembly defines the interface; the higher one implements
   it and registers itself.
3. **Decouple with events.** The lower assembly raises; the higher subscribes. No reference needed in
   the raising direction. See
   [the observer pattern](UnityDesignPatternsInstructions.md#observer-pattern).

❌ Merging the two assemblies to make the error go away is not a fix — it's deleting the boundary that
just told you something useful about your architecture.

---

## Editor-only assemblies

- ✅ Editor assemblies set `"includePlatforms": ["Editor"]`. That's what keeps them out of the build.
- ✅ An Editor assembly may reference runtime assemblies. Never the reverse.
- ⚠️ A folder named `Editor` is excluded from builds even without an asmdef — but once you introduce
  asmdefs, an `Editor` folder *inside* an assembly's folder tree is compiled into that assembly
  unless it has its own Editor asmdef. This is a common way Editor code ends up in a player build.
- ℹ️ For what belongs in Editor code, see
  [Editor Tooling](UnityEditorToolingInstructions.md#keeping-editor-code-out-of-builds).

---

## Test assemblies

Covered in depth in [Testing](UnityTestingInstructions.md#setting-up-test-assemblies). The
assembly-level points:

- ✅ `"defineConstraints": ["UNITY_INCLUDE_TESTS"]` is what keeps tests out of player builds. Without
  it they ship.
- ✅ Edit Mode tests also need `"includePlatforms": ["Editor"]`.
- ✅ Reference `UnityEngine.TestRunner` and `UnityEditor.TestRunner`, plus `nunit.framework.dll` under
  `precompiledReferences` with `"overrideReferences": true`.
- ✅ Use `[assembly: InternalsVisibleTo("MyGame.Tests.EditMode")]` in the assembly under test rather
  than widening members to `public` for testing.

---

## rootNamespace

- ✅ Set `rootNamespace` on every asmdef. Unity then auto-inserts the correct `namespace` when you
  create a script in that folder.
- ✅ Match it to the assembly name. Consistency here is what makes the codebase navigable.
- ⚠️ It only affects newly created scripts. Existing files aren't touched.

---

## Version defines for optional packages

`versionDefines` lets one assembly compile with or without an optional package, instead of hard
-failing when it's absent. This is how you write code that supports Addressables *if installed*.

```json
{
    "name": "MyGame.Loading",
    "rootNamespace": "MyGame.Loading",
    "references": ["MyGame.Core"],
    "versionDefines": [
        {
            "name": "com.unity.addressables",
            "expression": "1.21",
            "define": "ADDRESSABLES_1_21_OR_NEWER"
        }
    ]
}
```

```csharp
#if ADDRESSABLES_1_21_OR_NEWER
    return await Addressables.LoadAssetAsync<GameObject>(key).Task;
#else
    return m_directReference;
#endif
```

- ⚠️ The `expression` is a version range, and an empty string means "any version". Getting the range
  wrong means the define silently never appears.

---

## Troubleshooting

**"The type or namespace name 'X' could not be found" after adding an asmdef.**
The assembly containing `X` isn't in this asmdef's `references`. The code was fine before because
everything shared `Assembly-CSharp`.

**"Assembly with name 'X' has a circular reference to 'Y'".**
See [Circular references](#circular-references). Extract the shared type rather than merging.

**Editor code causes a build error, but it's in an `Editor` folder.**
The folder sits inside another assembly's tree, so it's compiled into that assembly. It needs its own
asmdef with `"includePlatforms": ["Editor"]`.

**Tests compile into the player build.**
Missing `"defineConstraints": ["UNITY_INCLUDE_TESTS"]`.

**A package's types aren't visible.**
Package assemblies must be referenced explicitly by name (`Unity.InputSystem`,
`Unity.Addressables`). Being installed isn't enough once you have asmdefs.

**Compile times got *worse* after adding asmdefs.**
Too many small assemblies, or a widely-referenced assembly near the bottom of the graph — changing it
rebuilds everything above. Merge over-split assemblies and check what `Core` actually contains.

**A `[MenuItem]` or custom inspector disappeared.**
It's now in a runtime assembly that can't reference `UnityEditor`, so it silently didn't compile, or
it's in an Editor assembly the rest of the project can't see. Check the Console with all filters on.

---

## Review checklist

| Check | Look for |
|---|---|
| Necessity | Asmdefs in a project with a handful of scripts |
| Granularity | One assembly per folder rather than per system |
| Direction | Core or Data referencing UI or Gameplay |
| Coupling | UI referencing Gameplay directly |
| Editor safety | `Editor` folder inside a runtime assembly with no asmdef of its own |
| Editor safety | Editor assembly without `"includePlatforms": ["Editor"]` |
| Tests | Test asmdef missing `UNITY_INCLUDE_TESTS` |
| Namespaces | `rootNamespace` unset |
| Exposure | `autoReferenced: true` on a library assembly |
| Testability | Members made `public` for tests instead of `InternalsVisibleTo` |

---

## Learn more

- [Assembly definitions, Unity manual](https://docs.unity3d.com/6000.3/Documentation/Manual/assembly-definition-files.html)
- [Assembly definition reference properties](https://docs.unity3d.com/6000.3/Documentation/Manual/class-AssemblyDefinitionImporter.html)
