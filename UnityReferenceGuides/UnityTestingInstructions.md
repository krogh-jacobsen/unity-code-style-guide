# Unity Testing

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Testing a game is not testing a web service. Most of a game is emergent, visual, and subjective —
you can't assert that a jump *feels* right. The value is in the narrow band that is deterministic:
rules, math, state transitions, and serialization.

The most useful thing testing does for a Unity codebase isn't the tests. It's the pressure to
**separate logic from MonoBehaviours**, because logic you can't instantiate without a scene is logic
you can't test — and usually logic you can't reuse either.

Table of contents:
- [What's worth testing](#whats-worth-testing)
- [Edit Mode vs Play Mode](#edit-mode-vs-play-mode)
- [Setting up test assemblies](#setting-up-test-assemblies)
- [Writing testable game code](#writing-testable-game-code)
- [Naming and structure](#naming-and-structure)
- [Testing async and coroutines](#testing-async-and-coroutines)
- [Test doubles](#test-doubles)
- [Running tests](#running-tests)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## What's worth testing

| Test it | Don't bother |
|---|---|
| Damage, economy, and scoring math | Whether a jump feels good |
| State machine transitions | Animation blend weights |
| Save/load round-trips | Particle appearance |
| Inventory rules (stacking, capacity, currency) | Shader output |
| Procedural generation determinism from a seed | Camera framing |
| Data validation on ScriptableObjects | Inspector wiring |
| Pure utility code (math helpers, parsers, grid logic) | UI layout |

- ✅ A test is worth writing when the rule is easy to state and expensive to get wrong.
- ✅ Save/load round-trips earn their keep faster than anything else. A save format regression can
  destroy player data, and it's trivially testable.
- ❌ Don't test that Unity works. `transform.position = x` does not need a test.
- ⚠️ Resist chasing coverage numbers. A game with 30% coverage concentrated on its economy is in far
  better shape than one with 80% spread evenly over getters.

---

## Edit Mode vs Play Mode

| | Edit Mode | Play Mode |
|---|---|---|
| Runs in | Editor, no play session | A real play session |
| Speed | Milliseconds | Seconds — domain reload, scene load |
| Can use | Plain C#, ScriptableObjects, `EditorUtility` | Everything, including `Update` and physics |
| MonoBehaviour lifecycle | ❌ No `Awake`/`Start`/`Update` | ✅ Full lifecycle |
| Coroutines | ❌ | ✅ |
| Use for | Logic, data, math, validation, Editor tools | Integration, physics, timing, scene flow |

- ✅ **Default to Edit Mode.** They're orders of magnitude faster, so you'll actually run them.
- ✅ Reach for Play Mode when the thing under test genuinely needs the engine loop — physics
  settling, a coroutine sequence, `OnTriggerEnter`.
- ⚠️ A Play Mode suite that takes five minutes is a suite nobody runs before pushing. Keep it small
  and keep the Edit Mode suite fast.

---

## Setting up test assemblies

Tests need their own assembly definitions or they'll ship in your build.

- ✅ Create test asmdefs via **Window → General → Test Runner → Create Test Assembly Folder**. It
  generates the right references.
- ✅ Keep Edit Mode and Play Mode tests in separate assemblies — the Edit Mode one needs
  `"includePlatforms": ["Editor"]`.
- ⚠️ `"defineConstraints": ["UNITY_INCLUDE_TESTS"]` is what actually keeps the assembly out of player
  builds. Without it the tests compile into your game.
- ✅ Your runtime code needs its own asmdef for tests to reference it. If everything is in
  `Assembly-CSharp`, tests can't reference it cleanly.
- ✅ Mark internals visible to the test assembly rather than making things `public` for testing:
  `[assembly: InternalsVisibleTo("MyGame.Tests")]`

```
Assets/
├── Scripts/
│   ├── Runtime/
│   │   ├── MyGame.Runtime.asmdef
│   │   └── Combat/DamageCalculator.cs
│   └── Editor/
│       └── MyGame.Editor.asmdef
└── Tests/
    ├── EditMode/
    │   └── MyGame.Tests.EditMode.asmdef   → references MyGame.Runtime
    └── PlayMode/
        └── MyGame.Tests.PlayMode.asmdef   → references MyGame.Runtime
```

```json
{
    "name": "MyGame.Tests.EditMode",
    "references": ["MyGame.Runtime", "UnityEngine.TestRunner", "UnityEditor.TestRunner"],
    "includePlatforms": ["Editor"],
    "defineConstraints": ["UNITY_INCLUDE_TESTS"],
    "precompiledReferences": ["nunit.framework.dll"],
    "autoReferenced": false,
    "overrideReferences": true
}
```

---

## Writing testable game code

This is the part that pays off whether or not you write the tests.

- ✅ **Put rules in plain C# classes.** A `DamageCalculator` that doesn't inherit `MonoBehaviour` can
  be constructed in a test with `new`, needs no scene, and runs in microseconds.
- ✅ Keep the MonoBehaviour as a thin shell: it holds serialized configuration, receives Unity
  callbacks, and delegates.
- ✅ Inject dependencies through the constructor of the plain class rather than reaching for a
  singleton inside it.
- ❌ Don't call `Time.deltaTime`, `Random.value`, or `Physics.Raycast` inside logic you want to test.
  Pass them in.

```csharp
// ❌ Hard to test - needs a GameObject, a scene, and real time
public class Health : MonoBehaviour
{
    [SerializeField] private int m_max = 100;
    private int m_current;

    public void ApplyDamage(int amount, ArmourType armour)
    {
        float multiplier = armour == ArmourType.Heavy ? 0.5f : 1f;
        m_current -= Mathf.RoundToInt(amount * multiplier);

        if (m_current <= 0) GameManager.Instance.HandleDeath(gameObject);
    }
}

// ✅ Testable - the rule lives in a plain class
public class HealthPool
{
    private readonly int m_max;
    private int m_current;

    public int Current => m_current;
    public bool IsAlive => m_current > 0;

    public HealthPool(int max)
    {
        m_max = max;
        m_current = max;
    }

    public void ApplyDamage(int amount, ArmourType armour)
    {
        if (amount <= 0) return;

        float multiplier = armour == ArmourType.Heavy ? 0.5f : 1f;
        m_current = Mathf.Max(0, m_current - Mathf.RoundToInt(amount * multiplier));
    }
}

// The MonoBehaviour becomes a thin shell over it
public class Health : MonoBehaviour
{
    [SerializeField] private int m_max = 100;

    private HealthPool m_pool;

    public event Action Died;

    private void Awake() => m_pool = new HealthPool(m_max);

    public void ApplyDamage(int amount, ArmourType armour)
    {
        bool wasAlive = m_pool.IsAlive;
        m_pool.ApplyDamage(amount, armour);

        if (wasAlive && !m_pool.IsAlive)
        {
            Died?.Invoke();
        }
    }
}
```

```csharp
// The test needs no scene, no GameObject, no play mode
[Test]
public void ApplyDamage_WithHeavyArmour_HalvesIncomingDamage()
{
    var pool = new HealthPool(100);

    pool.ApplyDamage(40, ArmourType.Heavy);

    Assert.AreEqual(80, pool.Current);
}

[Test]
public void ApplyDamage_ExceedingCurrentHealth_ClampsToZero()
{
    var pool = new HealthPool(30);

    pool.ApplyDamage(500, ArmourType.None);

    Assert.AreEqual(0, pool.Current);
    Assert.IsFalse(pool.IsAlive);
}
```

---

## Naming and structure

- ✅ Name tests `MethodName_StateUnderTest_ExpectedBehaviour`. It reads as a sentence in the Test
  Runner and tells you what broke without opening the file.
- ✅ Arrange, Act, Assert — separated by blank lines. One logical assertion per test.
- ✅ One test class per class under test, named `ClassNameTests`.
- ✅ Use `[TestCase]` for the same rule across many inputs rather than copy-pasting the test.
- ❌ Don't share mutable state between tests via fields without `[SetUp]`. Test order is not
  guaranteed.

```csharp
[TestFixture]
public class DamageCalculatorTests
{
    private DamageCalculator m_calculator;

    [SetUp]
    public void SetUp()
    {
        m_calculator = new DamageCalculator();
    }

    [TestCase(100, ArmourType.None,  ExpectedResult = 100)]
    [TestCase(100, ArmourType.Light, ExpectedResult = 75)]
    [TestCase(100, ArmourType.Heavy, ExpectedResult = 50)]
    public int Calculate_ByArmourType_AppliesCorrectMultiplier(int raw, ArmourType armour)
    {
        return m_calculator.Calculate(raw, armour);
    }
}
```

---

## Testing async and coroutines

- ✅ `[UnityTest]` returns `IEnumerator` and runs across frames. This is how you test anything
  time-based.
- ✅ `yield return null` advances one frame. `yield return new WaitForSeconds(t)` waits real time —
  use sparingly, it makes suites slow.
- ✅ For `Awaitable` code, an `async Task` test method works in the Test Framework, or wrap it:

```csharp
[UnityTest]
public IEnumerator Door_AfterOpenDelay_ReportsOpen()
{
    var door = new GameObject("Door").AddComponent<Door>();

    door.BeginOpening();

    // Advance frames rather than sleeping where possible
    yield return new WaitForSeconds(door.OpenDuration + 0.1f);

    Assert.IsTrue(door.IsOpen);

    Object.Destroy(door.gameObject);
}

[Test]
public async Task LoadProfileAsync_WhenFileMissing_ReturnsDefault()
{
    var service = new ProfileService(new InMemoryFileSystem());

    Profile result = await service.LoadProfileAsync("missing.json");

    Assert.AreEqual(Profile.Default, result);
}
```

- ⚠️ Clean up GameObjects you create in Play Mode tests. Leaked objects bleed into later tests and
  produce failures that only reproduce when the whole suite runs.
- ✅ Prefer injecting a clock over waiting on the real one. A logic class that takes a `deltaTime`
  parameter can be tested instantly instead of in real seconds.

---

## Test doubles

- ✅ Interfaces you already have for decoupling double as seams for testing. This is the practical
  payoff of [Interfaces](../UnityStyleGuide.md#interfaces) and
  [Dependency Inversion](UnityDesignPatternsInstructions.md#dependency-inversion-principle).
- ✅ Hand-written fakes are usually clearer than a mocking framework for game logic, and add no
  dependency.
- ✅ Fake the boundary — file system, network, clock, random — not your own domain classes.

```csharp
public interface IRandomSource
{
    float NextFloat();
}

// Production
public class UnityRandomSource : IRandomSource
{
    public float NextFloat() => UnityEngine.Random.value;
}

// Test double - deterministic, no engine dependency
public class FixedRandomSource : IRandomSource
{
    private readonly float m_value;

    public FixedRandomSource(float value) => m_value = value;

    public float NextFloat() => m_value;
}

[Test]
public void RollCrit_WhenRollBelowChance_ReturnsTrue()
{
    var combat = new CombatResolver(new FixedRandomSource(0.05f));

    Assert.IsTrue(combat.RollCrit(critChance: 0.10f));
}
```

---

## Running tests

- ✅ **Window → General → Test Runner** in the Editor.
- ✅ From CI or the command line:

```bash
Unity -runTests -batchmode -projectPath . \
      -testPlatform EditMode \
      -testResults ./TestResults.xml \
      -logFile -
```

- ✅ Run Edit Mode tests on every push; run Play Mode tests on merge to main if they're slow.
- ⚠️ `-batchmode` with Play Mode tests needs `-testPlatform PlayMode` and a graphics device on some
  platforms. Add `-nographics` only if nothing under test renders.
- ✅ Use `-testFilter` to run a single test or fixture while iterating.

---

## Troubleshooting

**Tests don't appear in the Test Runner.**
The test assembly doesn't reference `UnityEngine.TestRunner`, the class isn't `public`, or the
methods lack `[Test]` / `[UnityTest]`. For Edit Mode, the asmdef also needs
`"includePlatforms": ["Editor"]`.

**"The type or namespace name 'X' could not be found" in a test.**
The test asmdef doesn't reference the assembly under test. If the code lives in `Assembly-CSharp`
(no asmdef at all), tests can't reference it — the production code needs its own asmdef first.

**A test passes alone and fails when the whole suite runs.**
Shared state. A static field, a ScriptableObject mutated at runtime, or a leaked GameObject from an
earlier Play Mode test. Reset in `[SetUp]`, and destroy anything you create in `[TearDown]`.

**Play Mode tests leak objects into later tests.**
`Object.Destroy` is deferred to end of frame. Use `Object.DestroyImmediate` in `[TearDown]`, or
yield a frame after destroying.

**`[UnityTest]` never completes.**
The coroutine is waiting on something that never happens. `yield return` on a condition needs a
timeout; the Test Framework won't impose one for you.

**Tests are in the player build.**
Missing `"defineConstraints": ["UNITY_INCLUDE_TESTS"]` on the test asmdef.

**`Time.deltaTime` is 0 in an Edit Mode test.**
There's no player loop in Edit Mode. Logic depending on frame time belongs in a Play Mode test — or
better, take `deltaTime` as a parameter so it can be tested in Edit Mode.
---

## Review checklist

| Check | Look for |
|---|---|
| Assembly setup | Tests without `UNITY_INCLUDE_TESTS` — they're shipping in the build |
| Test location | Play Mode tests that could be Edit Mode tests |
| Testability | Game rules living inside MonoBehaviours with no plain-C# seam |
| Determinism | `Random`, `Time`, or `DateTime.Now` used directly inside logic |
| Naming | Tests named `Test1`, `ItWorks`, or after the bug ticket |
| Isolation | Shared mutable fields without `[SetUp]` |
| Cleanup | Play Mode tests that leak GameObjects |
| Coverage focus | Getters tested; save/load and economy untested |

---

## Learn more

- [Unity Test Framework](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html)
- [Writing and executing tests](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/workflow-create-test.html)
- [NUnit assertion reference](https://docs.nunit.org/articles/nunit/writing-tests/assertions/assertions.html)
