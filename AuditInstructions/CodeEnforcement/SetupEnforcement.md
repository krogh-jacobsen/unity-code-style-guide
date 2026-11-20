> How it works: give this URL to your agent, for example "Set up code enforcement in my Unity project
> using this document". It audits your assemblies and existing checks, recommends boundary rules and
> tests, and applies only the changes you select and confirm. Human overview: [readme](README.md).

# Set up code enforcement (agent instructions)

Turn the project's architecture and API rules into checks that fail on new violations, so an existing
project can adopt them without fixing everything first. This document is self-contained.
**Last verified: November 2026.** Confirm Unity Editor, Test Framework and analyzer details against the
installed versions before writing configuration.

## Operating rules

- Read the target's instructions, assembly policy and test permissions first. An explicit "no asmdefs"
  choice is respected: enforce the same rules on namespaces and folders instead, and recommend no reversal.
- During audit, read saved files only: `.asmdef`, `.asmref`, `.ruleset`, `.editorconfig`, existing tests.
  Creating assemblies, adding tests, installing analyzers and running tests are listed changes.
- Create and move assets through Unity Editor APIs or Unity CLI so Unity owns metadata. New `.cs` and
  `.asmdef` files may be written while the Editor imports them normally.
- Never weaken a rule or grow a baseline to make a check pass. A failing check is a finding to report.
- Missing Editor, Test Framework or run authorization leaves the affected checks **Not verified**.

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit user confirmation.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Present the exact changes for the picked subset (files, settings, values, commands)
   and obtain explicit user authorization before making them, including saving the report. Give
   each change its undo: a commit checkpoint, a backup copy of a settings file, a log of moves, or
   the trash instead of a permanent delete.
   Confirmation need not contain the literal word "yes": after the concrete scope is presented,
   "implement R1 and R3" can both select and confirm those items. Selection alone ("R1 and R3")
   chooses scope without authorizing implementation. Honor existing authorization for unchanged
   scope without asking again; clarify a delayed reply only when its scope is materially ambiguous.
   Resolve IDs against the presented change list rather than guide defaults. If evidence establishes
   that exact scope was previously presented and authorized but its record is now unavailable,
   retrieve that record before execution; recovered unchanged scope needs no repeat confirmation.
   If concrete changes were never presented, an instruction to implement an ID leaves scope
   unconfirmed: first present the exact changes and obtain confirmation before execution.
   Changed scope needs confirmation for the changed items. In a non-interactive session, or when
   authorization is absent, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. Any
change outside the confirmed list, however small or obviously helpful (an extra `.gitkeep`, a
related setting), is a new recommendation: it returns to stage 3 before it is made. Noting it in a
report is not confirmation.

## 1. Audit the current boundaries

Map every first-party assembly, its `references`, `defineConstraints`, `includePlatforms` and
`noEngineReferences`, plus `.asmref` files. Identify vendor assemblies (Asset Store packs, `3rdParty`,
`Plugins`) and keep them out of judgement. Record existing standards tests, analyzers and rulesets.

Report at least: assemblies that reference presentation or vendor code from core logic; development,
lab, cheat or preview code that a normal player build compiles; test code outside test assemblies; and
the dependency rules the project already states in its documents.

**Done:** every first-party assembly has a row with its references and a stated layer, or "no asmdefs".

## 2. Declare the layering

Propose layers from the project's actual code, not from a template name. The shape that worked in real
projects, from the inside out:

| Layer | Holds | May reference |
|---|---|---|
| Core / Rules | Pure C# rules and data, `noEngineReferences: true` | Nothing first-party |
| Contracts | Interfaces, events, shared data types | Core |
| Features | Gameplay systems | Core, Contracts |
| Presentation | UI, VFX, audio, cameras | Core, Contracts, Features |
| Composition | Bootstrap, scene wiring | Everything above |
| Adapters | Wrappers around vendor packages | Vendor assemblies, Contracts |
| Development | Cheats, debug consoles, lab scenes, benchmarks | Anything; `defineConstraints` such as `UNITY_EDITOR || DEVELOPMENT_BUILD` |

Tests can sit next to their module: an `.asmref` in each module's `Tests/EditMode` folder points at one
shared EditMode test assembly. Record the agreed rules in the project's `AGENTS.md` so they have one owner.

**Done:** the user has confirmed a rule list, each rule stated as "assembly A never references B, because …".

## 3. Add the assembly boundary test

An EditMode test reads Unity's compiled assembly graph and fails on any confirmed rule that is broken.
Put it in an EditMode test assembly. Replace the patterns with the confirmed rules.

```csharp
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEditor.Compilation;

namespace Game.Tests.EditMode
{
    public class AssemblyBoundaryTests
    {
        // From: assemblies the rule applies to. Forbidden: references they must not have.
        private static readonly (string From, string Forbidden, string Reason)[] s_rules =
        {
            (@"^Game\.Core$", @"^Game\.", "Core references nothing first-party"),
            (@"^Game\.Gameplay$", @"^Game\.Presentation$", "Gameplay does not depend on presentation"),
            (@"^Game\.(?!Adapters$)", @"^Vendor\.", "Only the adapter assembly references vendor code"),
        };

        private static readonly string[] s_engineFreeAssemblies = { "Game.Core" };

        [Test]
        public void AssemblyReferencesFollowDeclaredRules()
        {
            Assembly[] assemblies = CompilationPipeline.GetAssemblies(AssembliesType.PlayerWithoutTestAssemblies);
            var violations = new List<string>();
            foreach ((string from, string forbidden, string reason) in s_rules)
            {
                Assembly[] matches = assemblies.Where(assembly => Regex.IsMatch(assembly.name, from)).ToArray();
                Assert.That(matches, Is.Not.Empty, $"Rule '{from}' matches no assembly; fix the rule");
                foreach (Assembly assembly in matches)
                {
                    foreach (Assembly reference in assembly.assemblyReferences)
                    {
                        if (Regex.IsMatch(reference.name, forbidden))
                        {
                            violations.Add($"{assembly.name} -> {reference.name}: {reason}");
                        }
                    }
                }
            }

            Assert.That(violations, Is.Empty, string.Join("\n", violations));
        }

        [Test]
        public void EngineFreeAssembliesDoNotReferenceUnityEngine()
        {
            Assembly[] assemblies = CompilationPipeline.GetAssemblies(AssembliesType.PlayerWithoutTestAssemblies);
            foreach (string name in s_engineFreeAssemblies)
            {
                Assembly assembly = assemblies.SingleOrDefault(candidate => candidate.name == name);
                Assert.That(assembly, Is.Not.Null, $"{name} not found");
                string[] engineReferences = assembly.compiledAssemblyReferences
                    .Where(path => Path.GetFileName(path).StartsWith("UnityEngine"))
                    .ToArray();
                Assert.That(engineReferences, Is.Empty, $"{name} references the engine; set noEngineReferences");
            }
        }
    }
}
```

A rule that matches no assembly fails on purpose, so a renamed assembly cannot silently disable it.
Without asmdefs, write the same rules as a source search instead: files under the core folder must not
contain the game's namespaces or type names.

**Done:** the test passes on the current project, and fails when one forbidden reference is added
temporarily (then removed).

## 4. Add the banned-API ratchet

A second EditMode test searches first-party source for banned patterns. Existing violations go in a
baseline so the test passes on day one. New violations fail, and so do baseline entries that no longer
occur, which forces the baseline to shrink as code is fixed.

```csharp
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;

namespace Game.Tests.EditMode
{
    public class StandardsRatchetTests
    {
        private static readonly string[] s_firstPartyRoots = { "Assets/_Project" };

        private static readonly (string Id, string Pattern, string Fix)[] s_rules =
        {
            ("find-object-of-type", @"\bFindObjects?OfType\s*[<(]", "Use a serialized reference, or FindAnyObjectByType / FindObjectsByType"),
            ("draw-mesh", @"\bGraphics\.DrawMesh(Instanced)?\s*\(", "Use the RenderMesh family"),
            ("uxml-factory", @"\bUxml(Factory|Traits)\b", "Use [UxmlElement] and [UxmlAttribute]"),
            ("lambda-subscription", @"\+=\s*(\([^)]*\)|\w+)\s*=>", "Subscribe a named method so it can be unsubscribed"),
        };

        // Known violations as "path|rule-id". Delete a line when its violation is fixed; never add one.
        private static readonly HashSet<string> s_baseline = new HashSet<string>
        {
        };

        [Test]
        public void NoNewViolations()
        {
            string[] added = FindViolations().Where(violation => !s_baseline.Contains(violation)).ToArray();
            Assert.That(added, Is.Empty, "New violations:\n" + string.Join("\n", added));
        }

        [Test]
        public void BaselineHasNoFixedEntries()
        {
            HashSet<string> found = FindViolations();
            string[] stale = s_baseline.Where(entry => !found.Contains(entry)).ToArray();
            Assert.That(stale, Is.Empty, "Fixed; delete from the baseline:\n" + string.Join("\n", stale));
        }

        private static HashSet<string> FindViolations()
        {
            var violations = new HashSet<string>();
            foreach (string root in s_firstPartyRoots)
            {
                foreach (string file in Directory.EnumerateFiles(root, "*.cs", SearchOption.AllDirectories))
                {
                    string[] codeLines = File.ReadAllLines(file)
                        .Where(line => !line.TrimStart().StartsWith("//"))
                        .ToArray();
                    foreach ((string id, string pattern, string _) in s_rules)
                    {
                        if (codeLines.Any(line => Regex.IsMatch(line, pattern)))
                        {
                            violations.Add(file.Replace('\\', '/') + "|" + id);
                        }
                    }
                }
            }

            return violations;
        }
    }
}
```

Seed the rules from the deprecated-API table in the project's tech stack document and from rules the
project has already been bitten by. Keep each pattern narrow: a rule with false positives gets ignored.
The search reads text and skips only whole comment lines, so a match inside a string literal or a
trailing comment also counts; baseline those or tighten the pattern.
Generate the first baseline from the test's own failure output, then review it with the user.

**Done:** the test passes with the reviewed baseline, fails when one new violation is added temporarily,
and fails when one baseline line is left after its violation is fixed.

## 5. Optional: Roslyn analyzers

Analyzers catch at compile time what the ratchet catches by text. Unity runs an analyzer DLL that carries
the asset label `RoslynAnalyzer` (exact, case sensitive). A DLL inside an asmdef folder applies only to
that assembly and the assemblies that reference it, which keeps vendor code out of scope.

- **Microsoft.Unity.Analyzers** adds Unity-specific diagnostics and suppresses false "unused" warnings on
  Unity messages. Visual Studio and the VS Code Unity extension already apply it in the IDE; adding the DLL
  with the label makes Unity's own compiler report it too.
- **Severity:** set per diagnostic in `.editorconfig` (`dotnet_diagnostic.<ID>.severity = error`), or in a
  `.ruleset`: `Default.ruleset` in `Assets` for all assemblies, a ruleset next to an `.asmdef` for that
  assembly. Raise severity for first-party assemblies only.
- Project-wide warnings-as-errors through compiler response files is **Not verified** in Unity 6; prefer
  per-diagnostic severity.

**Done:** a seeded diagnostic appears in Unity's console at the configured severity, and vendor assemblies
report none.

## Report

List per check: added, already present, skipped, or Not verified, with the baseline size at the start.
Put open choices (layer names, rule list, baseline review) in a "Needs your decision" block.
