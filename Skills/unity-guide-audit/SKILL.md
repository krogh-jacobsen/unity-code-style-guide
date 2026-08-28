---
name: unity-guide-audit
description: Audit a Unity project for conformance to this repo's style guide and reference guides — naming and prefix conventions, class organization, hot-path violations, event-subscription leaks, ScriptableObject misuse, UI conventions, folder structure, and project settings. Runs static analysis anywhere, and adds a live Editor pass via unity-cli when an Editor is reachable. Use when the user asks to audit, review, or health-check a Unity project against their conventions, or asks "does my project follow my style guide".
---

# Unity Guide Audit

Check a Unity project against the conventions in this repository and report violations with file,
line, and the specific rule broken.

**This is a conformance check, not a general code review.** If the user wants generic Unity pitfall
detection, the `unity-project-review` skill covers that. This skill answers a narrower question:
*does this project follow the documented conventions in `UnityStyleGuide.md` and
`UnityReferenceGuides/`?*

## Before starting

1. **Locate the guides.** Look for `UnityStyleGuide.md`, `AGENTS.md`, or `UnityReferenceGuides/` in
   the project root, a parent directory, or a sibling checkout. If none exist, ask the user where
   they are — do not audit against remembered defaults.
2. **Know which guides exist.** `UnityReferenceGuides/` currently holds: Performance, Assets &
   Memory, Design Patterns, Scenes & Lifecycle, UI Toolkit, uGUI, Input System, Animation, Audio,
   Assembly Definitions, Testing, Editor Tooling, Debugging. Cite the specific one in every finding.
3. **Read the tech stack.** `UnityCustomInstructions/UnityTechStack.md` says which input, UI, and
   render systems are in use. A uGUI finding is noise in a UI Toolkit project.
4. **Confirm the scope** with the user: whole project, one folder, or changes on the current branch.
5. **Establish the naming convention from the guide, not from memory.** The prefixes (`m_`/`k_`/`s_`)
   and their casing are configurable preferences. Read them out of the guide before flagging anything.

## Phase 1 — Static analysis (always runs)

Needs no Unity Editor. Works in CI. Scan `.cs`, `.uxml`, `.uss`, `.asmdef`, and
`ProjectSettings/*.asset`.

Skip `Library/`, `Temp/`, `obj/`, `Build/`, and any `Packages/` cache. Do not report findings inside
third-party plugin folders unless the user asks.

### Asset integrity (check these first)

These detect **damage**, not drift. A finding here is a corrupted project, not a style opinion, so it
outranks everything below it.

| Check | How |
|---|---|
| Duplicate GUIDs | Parse `guid:` from every `.meta`; any GUID appearing twice is a corrupted project — references resolve non-deterministically |
| Orphaned `.meta` | A `.meta` with no matching asset beside it |
| Missing `.meta` | An asset under `Assets/` with no `.meta` (excluding ignored folders) |
| Malformed `.meta` | Missing `guid:`, or a GUID that isn't 32 hex characters |
| Unsafe field rename | In a diff: a serialized field renamed with no `[FormerlySerializedAs]` on it |
| Enum renumbering | In a diff: members of a serialized enum reordered or given new explicit values |
| Unpaired asset editing | `AssetDatabase.StartAssetEditing()` without `StopAssetEditing()` in a `finally` |
| Committed generated data | `Library/`, `Temp/`, `obj/`, `Logs/`, `UserSettings/` tracked in git |

⚠️ Report duplicate GUIDs as 🔴 High regardless of how many there are, and name every affected pair —
this is the one finding where a count is not enough.

### Naming and style

| Check | How |
|---|---|
| Private fields missing the `m_` prefix | Fields declared `private`/implicit without the prefix |
| Wrong casing after a prefix | `m_`/`k_`/`s_` followed by an uppercase letter, when the guide says camelCase |
| `public` fields on MonoBehaviours | Should be `[SerializeField] private` plus a property |
| Constants not using `k_` | `private const` without the prefix (public consts on lookup classes are exempt) |
| Statics not using `s_` | `static` fields without the prefix |
| Interfaces without `I` | `interface` declarations |
| Booleans not reading as predicates | `bool` fields/properties not starting with is/has/can/should |
| Methods not starting with a verb | Especially gerunds (`Walking()`) |
| Missing explicit `private` | Members with no access modifier, if the guide requires it |
| ScriptableObjects without the suffix | Types deriving `ScriptableObject` |

### Class organization

- Member order against the documented execution-order layout (fields → properties → events →
  lifecycle → public → private).
- More than one MonoBehaviour in a file, or a file name not matching its MonoBehaviour.
- `#region` used outside the sanctioned event-handler grouping.

### Hot paths

Inside `Update`, `FixedUpdate`, `LateUpdate`, and `OnGUI`:

- `GetComponent`, `GetComponentInChildren`, `AddComponent`
- `FindObjectsByType`, `FindFirstObjectByType`, `GameObject.Find`, `Camera.main`
- `new` on any reference type; collection or array construction
- LINQ (`.Where`, `.Select`, `.OrderBy`, `.ToList`, `.Any`, `.First`)
- String concatenation or `$"..."` interpolation
- `Physics.*` queries without a layer mask, or using the allocating overload
- `Debug.Log` calls
- `SetBool`/`SetFloat`/`SetTrigger` with a string literal instead of a cached hash

### Lifecycle and leaks

- `+=` in `OnEnable` with no matching `-=` in `OnDisable` (the highest-value check in this list).
- Event subscriptions using a lambda — impossible to unsubscribe.
- `AddListener` on a `UnityEvent` with no matching `RemoveListener`, especially on pooled prefabs.
- `static` fields or `static event` on a class with no `[RuntimeInitializeOnLoadMethod]` reset, when
  Domain Reload is disabled in `ProjectSettings/EditorSettings.asset`.
- `NativeArray`/`NativeList` allocated without a `Dispose`.
- `Addressables.LoadAssetAsync` without a matching `Release`; `Destroy` used on an instance created
  by `InstantiateAsync`.

### Unity 6 API currency

- `FindObjectOfType` / `FindObjectsOfType` (deprecated).
- Coroutines used for simple delays where `Awaitable` fits, if the tech stack prefers `Awaitable`.
- `async void` on anything other than an event handler.
- `.material` where `.sharedMaterial` was intended.
- Legacy `Input.GetKey` / `Input.GetAxis` when the project uses the Input System.

### ScriptableObjects

- Fields mutated at runtime (writes outside `OnEnable`/`OnValidate`/Editor code).
- Missing `[CreateAssetMenu]`.
- Public fields instead of serialized-private plus properties.

### UI

**UI Toolkit** (`.uxml`, `.uss`):
- Class or name values not in kebab-case BEM.
- `classList.Add` / `classList.Remove` / `classList.Toggle` — not valid; must be `AddToClassList`,
  `RemoveFromClassList`, `EnableInClassList`.
- USS using CSS-only features: `gap`, `calc()`, `z-index`, hex colours, `em`/`rem`, `@media`,
  `display: grid`, `:nth-child`.
- `RegisterCallback` without a matching `UnregisterCallback`.

**uGUI** (`.prefab`, `.unity`, `.cs`) — only if the project uses uGUI:
- `Animator` component on a GameObject that also has a `Graphic`.
- `.text` assigned unconditionally inside `Update`.
- `Instantiate` of a row prefab inside a loop with no pooling.
- `Canvas.ForceUpdateCanvases()` anywhere.

### Input System

Only if the tech stack says Input System.

- Legacy `Input.GetKey`, `Input.GetAxis`, `Input.mousePosition` anywhere.
- `InputAction` / map `.Enable()` with no matching `.Disable()`.
- `performed +=` / `started +=` / `canceled +=` with no matching `-=` in `OnDisable`.
- Lambda subscriptions to input callbacks (unremovable).
- Generated input class not disposed in `OnDestroy`.
- `ReadValue<T>()` called in `FixedUpdate` rather than `Update`.
- Both `started` and `performed` subscribed for the same button action.

### Animation

- String literals passed to `SetBool` / `SetFloat` / `SetTrigger` / `GetBool` instead of a cached hash.
- `Animator.StringToHash` called per instance rather than in a `static readonly` field.
- `SetTrigger` with no `ResetTrigger` on any interruption path.
- More than one component writing the same animator parameter.
- `Animator` on a GameObject that also has a `Graphic` (uGUI projects).
- Editor pass: Culling Mode left at `AlwaysAnimate`; `Has Exit Time` on gameplay transitions.

### Audio

- `AudioSource.PlayClipAtPoint` anywhere in a per-frame or frequently-called path.
- `Instantiate` of an `AudioSource` per sound instead of pooling.
- A linear slider value written to a mixer parameter without `Mathf.Log10(v) * 20`.
- `Mathf.Log10` on a volume value with no guard against zero.
- Pooled `AudioSource` released without resetting `loop` / `pitch` / `volume`.
- Editor pass: more than one active `AudioListener`; `AudioSource` with no `outputAudioMixerGroup`;
  `spatialBlend` at 0 on a positional source; `maxDistance` left at the 500 default.

### Assembly definitions

- No asmdefs in a project large enough to need them (rough threshold: 100+ scripts).
- Circular references between assemblies.
- An `Editor/` folder inside a runtime assembly's tree with no asmdef of its own.
- Editor assembly missing `"includePlatforms": ["Editor"]`.
- Test assembly missing `"defineConstraints": ["UNITY_INCLUDE_TESTS"]` — it ships in builds.
- `rootNamespace` unset.
- `autoReferenced: true` on a library assembly.
- Core/Data assemblies referencing UI or Gameplay (dependency direction inverted).

### Structure and settings

- Folder and file names not PascalCase; spaces or special characters in paths.
- Editor scripts outside an `Editor/` folder or Editor-only asmdef.
- `using UnityEditor;` in a runtime script outside `#if UNITY_EDITOR`.
- Test assemblies missing `UNITY_INCLUDE_TESTS` in `defineConstraints` — they are shipping in builds.
- Any `Resources/` folder.
- `ProjectSettings/` values worth reporting: colour space, scripting backend, managed stripping
  level, Enter Play Mode / Domain Reload, physics collision matrix left fully enabled, quality tiers.

## Phase 2 — Live Editor pass (optional)

Only for findings static analysis genuinely cannot reach. **Delegate Editor control to the
`unity-cli` skill** — do not reimplement it.

1. Check whether a Unity Editor is reachable. If not, say so plainly, report Phase 1, and stop. Do
   not treat an unavailable Editor as a failure.
2. Ask the user before running anything in a live Editor — it can modify project state.
3. Use `unity-cli` to execute C# in the Editor and return findings as data.

What to check here:

| Area | Check |
|---|---|
| Canvas structure | Canvas count per scene; nesting depth; elements per Canvas |
| Raycast targets | `Graphic.raycastTarget` true on non-interactive elements |
| Layout | Nested `LayoutGroup`s; `ContentSizeFitter` inside a layout group |
| References | Serialized `[SerializeField]` fields that are null in a scene or prefab |
| Prefabs | Instances with unexpected override drift |
| Textures | `isReadable` true (doubles memory); oversized `maxTextureSize`; mip maps on UI sprites |
| Audio | Long clips not set to Streaming; 3D sources not Force-To-Mono |
| Scene cost | Count of components implementing `Update` per scene |
| Build | Scenes in Build Settings that no longer exist |
| Animation | Animator Culling Mode at `AlwaysAnimate`; `Has Exit Time` on responsive transitions |
| Audio | Active `AudioListener` count; sources with no mixer group; `spatialBlend` 0 on 3D sources |
| Lighting | Scenes with no baked lighting data where it was expected |

## Reporting

Group findings by severity, most severe first. For each:

- **What** — the rule, quoted or paraphrased from the guide.
- **Where** — `path/to/File.cs:42`.
- **Why it matters** — one clause, not a paragraph.
- **Source** — which guide and section the rule comes from.

| Severity | Means |
|---|---|
| 🔴 High | Correctness, leaks, or a build-breaking issue. Event never unsubscribed; Editor code in a build; test assembly shipping. |
| 🟠 Medium | Real performance or maintenance cost. Allocation in `Update`; monolithic Canvas; Read/Write textures. |
| 🟡 Low | Convention drift with no functional impact. Prefix casing; member ordering. |

Rules for the report:

- **Cap the noise.** If one rule is violated 200 times, report the rule once with a count and three
  representative locations — not 200 findings.
- **Separate "the guide says" from "I think".** If you spot a genuine problem the guide doesn't
  cover, list it in a short "Not in the guide, but worth noting" section at the end.
- Lead with a one-paragraph summary: how many findings, in which categories, and the single most
  important thing to fix.
- If the project is clean, say so in one line. Don't manufacture findings.
- Say explicitly whether Phase 2 ran.

## Fixing

Do not fix anything unless the user asks. When they do:

- Batch mechanical fixes (prefix renames, member reordering) and apply them in one pass per rule.
- Treat behavioural fixes (adding a missing unsubscribe, restructuring a Canvas) as individual
  changes to review.
- Never bulk-rename across a project without confirming — Unity serialized data references field
  names by string, and renaming a serialized field **loses its Inspector value** unless you add
  `[FormerlySerializedAs("oldName")]`. Flag this every time it applies.
