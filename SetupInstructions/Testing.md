# Test setup

**Prerequisite:** tests are selected, exact Editor/Test Framework compatibility is known, and production
assembly boundaries are understood. Use `unity-package-management` through Unity CLI to add a missing
Test Framework package; inspect the resolved version instead of assuming one.

## Create discoverable isolated tests

1. Create EditMode and/or PlayMode test assemblies with Unity's Test Runner or CLI-driven Editor APIs.
   Reference only the required production assemblies. The bundled UI example includes isolated test
   asmdefs; import those with the example rather than placing NUnit files in Assembly-CSharp.
2. Mark assemblies as test assemblies with the installed framework's supported configuration. Editor
   tests are Editor-only. PlayMode tests require the runtime test configuration. An `Editor` folder
   under a runtime asmdef does not automatically provide isolation.
3. Use EditMode for pure rules/presenters and Editor validation; PlayMode for actual lifecycle/UI wiring.
   Replace ignored template stubs with a meaningful behavioral assertion before counting coverage.
4. Run through CLI (discover current options with `unity test --help`):

```bash
unity test /absolute/target/project --mode EditMode --output /absolute/results/editmode.xml
unity test /absolute/target/project --mode PlayMode --output /absolute/results/playmode.xml
```

Use a runner subagent when the project's instructions and available capabilities support it.
Read fresh XML/logs: passed, failed, skipped/ignored, excluded, and not-run are different outcomes.
Compile a normal player to confirm test-only dependencies do not ship; test-player builds are separate.

**Manual fallback:** Test Runner creates assemblies and runs selected modes; inspect results and
normal-player compilation. **Done:** intended tests are discovered, assertions are failure-sensitive,
fixtures clean up, the agreed suites pass, and normal-player isolation is verified. Framework/tool
unavailability leaves the affected outcome Not verified.

Detailed review criteria belong in [the testing audit](../AuditGuides/UnityTestingInstructions.md)
when reviewing test quality, not in a second test recipe here.
