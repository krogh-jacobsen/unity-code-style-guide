# Unity Editor Tooling

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Custom inspectors, property drawers, menu items and Gizmos — and, more importantly, keeping all of
it out of your player build.

Editor code has one rule that outranks every style consideration: **it must not compile into the
game.** `UnityEditor` does not exist in a build, so a single stray reference in runtime code turns
into a build error at the worst possible moment.

Table of contents:
- [Keeping Editor code out of builds](#keeping-editor-code-out-of-builds)
- [Custom inspectors](#custom-inspectors)
- [Property drawers](#property-drawers)
- [SerializedProperty, Undo and dirtying](#serializedproperty-undo-and-dirtying)
- [Menu items and context menus](#menu-items-and-context-menus)
- [Gizmos and Handles](#gizmos-and-handles)
- [Validation tooling](#validation-tooling)
- [Never edit these by hand](#never-edit-these-by-hand)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## Keeping Editor code out of builds

Two mechanisms, for two different situations:

| Situation | Use |
|---|---|
| A whole class is Editor-only | Put it in an `Editor/` folder |
| A few members on a runtime class are Editor-only | Wrap in `#if UNITY_EDITOR` |

- ✅ Any folder named `Editor` anywhere under `Assets/` is excluded from builds automatically. No
  asmdef required, though an Editor asmdef makes the boundary explicit and speeds up compilation.
- ✅ An Editor asmdef needs `"includePlatforms": ["Editor"]`.
- ⚠️ **`#if UNITY_EDITOR` around a field changes serialization.** The field exists in the Editor and
  not in the build, so anything referencing it breaks. Wrap methods and `using UnityEditor;`
  directives, not serialized fields.
- ⚠️ A runtime class cannot inherit from or expose an Editor type in its public API, even inside
  `#if UNITY_EDITOR` — the signature still has to resolve.

```csharp
// ✅ Editor-only helper on a runtime component
public class SpawnPoint : MonoBehaviour
{
    [SerializeField] private float m_radius = 1f;

#if UNITY_EDITOR
    // Only compiled in the Editor - safe, because nothing at runtime calls it
    [ContextMenu("Snap To Ground")]
    private void SnapToGround()
    {
        if (Physics.Raycast(transform.position + Vector3.up * 10f, Vector3.down, out RaycastHit hit))
        {
            UnityEditor.Undo.RecordObject(transform, "Snap To Ground");
            transform.position = hit.point;
        }
    }
#endif
}
```

- ✅ Fully-qualify (`UnityEditor.Undo`) inside a guarded block rather than adding a top-level
  `using UnityEditor;`, so you can't accidentally use an Editor type in unguarded code.

---

## Custom inspectors

- ✅ **For new work, use UI Toolkit `CreateInspectorGUI()`.** It's the direction Unity is going, it
  composes better, and it gives you the same UXML/USS skills you use elsewhere.
- ⚠️ Keep IMGUI `OnInspectorGUI()` for maintaining existing tools. Don't rewrite working IMGUI just
  to modernize it.
- ✅ Write a custom inspector only when the default one is genuinely inadequate. `[Header]`,
  `[Tooltip]`, `[Range]`, and `[SerializeField]` handle most cases with zero code and zero
  maintenance.
- ✅ Call `CreateInspectorGUI` on the base first if you want the default fields plus additions.
- ⚠️ `[CanEditMultipleObjects]` is not automatic. Without it, selecting two objects shows nothing —
  and if you edit fields directly instead of via `SerializedProperty`, multi-edit silently corrupts
  data.

```csharp
using UnityEditor;
using UnityEditor.UIElements;
using UnityEngine.UIElements;

[CustomEditor(typeof(WeaponDataSO))]
[CanEditMultipleObjects]
public class WeaponDataSOEditor : Editor
{
    public override VisualElement CreateInspectorGUI()
    {
        var root = new VisualElement();

        // Binding by property path gives Undo and multi-object editing for free
        root.Add(new PropertyField(serializedObject.FindProperty("m_weaponName")));
        root.Add(new PropertyField(serializedObject.FindProperty("m_damage")));

        var dps = new Label();
        root.Add(dps);

        root.TrackSerializedObjectValue(serializedObject, so =>
        {
            var weapon = (WeaponDataSO)so.targetObject;
            dps.text = $"DPS: {weapon.Damage * weapon.RateOfFire:F1}";
        });

        return root;
    }
}
```

- ✅ Name the file after the class: `WeaponDataSOEditor.cs`, in an `Editor/` folder.
- ✅ Prefer `PropertyField` bound to a property path over drawing controls by hand. You get Undo,
  prefab override indicators, and multi-object editing without writing any of it.

---

## Property drawers

- ✅ A `PropertyDrawer` is the better choice when you want a *type* or *attribute* to render
  consistently everywhere it appears, rather than customizing one component.
- ✅ `[CustomPropertyDrawer(typeof(MyType))]` for a type; `[CustomPropertyDrawer(typeof(MyAttribute))]`
  for an attribute.
- ✅ Use `CreatePropertyGUI()` (UI Toolkit) for new drawers.
- ⚠️ A drawer for a type applies to every field of that type in the whole project. Scope carefully.

```csharp
// Runtime - the attribute lives with the code that uses it
public class RequiredAttribute : PropertyAttribute { }

// Editor/RequiredDrawer.cs
[CustomPropertyDrawer(typeof(RequiredAttribute))]
public class RequiredDrawer : PropertyDrawer
{
    public override VisualElement CreatePropertyGUI(SerializedProperty property)
    {
        var field = new PropertyField(property);
        var warning = new HelpBox("This reference is required.", HelpBoxMessageType.Error);

        var root = new VisualElement();
        root.Add(field);
        root.Add(warning);

        void Refresh()
        {
            bool isMissing = property.propertyType == SerializedPropertyType.ObjectReference
                             && property.objectReferenceValue == null;
            warning.style.display = isMissing ? DisplayStyle.Flex : DisplayStyle.None;
        }

        Refresh();
        field.TrackPropertyValue(property, _ => Refresh());

        return root;
    }
}
```

---

## SerializedProperty, Undo and dirtying

This is where most custom Editor code goes wrong, and the symptoms — changes not saving, Undo not
working, prefab overrides behaving strangely — look unrelated to the cause.

- ✅ **Always go through `SerializedObject` / `SerializedProperty` in an inspector.** Setting fields
  directly on `target` skips Undo, skips dirtying, and breaks multi-object editing.
- ✅ The IMGUI pattern is always: `serializedObject.Update()` → modify properties →
  `serializedObject.ApplyModifiedProperties()`.
- ✅ Outside an inspector — a menu item or a utility — use `Undo.RecordObject` **before** the change,
  then `EditorUtility.SetDirty` after.
- ⚠️ `Undo.RecordObject` must be called before modification. Calling it afterwards records the
  already-changed state and Undo does nothing.
- ⚠️ For prefab instances, use `PrefabUtility.RecordPrefabInstancePropertyModifications` so the change
  registers as an override rather than being lost.
- ⚠️ Scene changes need `EditorSceneManager.MarkSceneDirty`; `SetDirty` alone doesn't mark a scene.

```csharp
// ✅ Correct order for a non-inspector edit
private static void AlignSelectionToGrid()
{
    foreach (Transform t in Selection.transforms)
    {
        Undo.RecordObject(t, "Align To Grid");   // BEFORE the change

        t.position = new Vector3(
            Mathf.Round(t.position.x),
            Mathf.Round(t.position.y),
            Mathf.Round(t.position.z));

        // Prefab instances need this or the change won't stick as an override
        PrefabUtility.RecordPrefabInstancePropertyModifications(t);
        EditorUtility.SetDirty(t);
    }
}
```

---

## Menu items and context menus

| Attribute | Where it appears | Notes |
|---|---|---|
| `[MenuItem("Tools/…")]` | Main menu bar | Static method. Use a project-named top-level menu |
| `[MenuItem("CONTEXT/Component/…")]` | Component gear menu | Takes a `MenuCommand` |
| `[ContextMenu("…")]` | Gear menu of the declaring component | Instance method, runtime class |
| `[ContextMenuItem("…", "Method")]` | Right-click on a specific field | On the field |
| `[InitializeOnLoad]` | — | Static constructor runs on every domain reload |

- ✅ Group your tools under one top-level menu named after the project, not scattered in `Tools/`.
- ✅ Provide a validate function (`[MenuItem("...", true)]`) so the item greys out when it can't run,
  rather than erroring.
- ⚠️ `[InitializeOnLoad]` runs on **every** domain reload — every script compile and every Play with
  domain reload on. Keep it cheap or it will make the whole Editor feel slow.
- ✅ `[ContextMenu]` on a runtime MonoBehaviour is the cheapest possible Editor tool. Wrap the body in
  `#if UNITY_EDITOR` if it touches `UnityEditor`.

```csharp
public static class ProjectTools
{
    [MenuItem("MyGame/Validate All ScriptableObjects", priority = 100)]
    private static void ValidateAll() { /* … */ }

    [MenuItem("MyGame/Align Selection To Grid")]
    private static void AlignToGrid() { /* … */ }

    // Validate function - same path, second arg true. Greys the item out when nothing is selected.
    [MenuItem("MyGame/Align Selection To Grid", true)]
    private static bool ValidateAlignToGrid() => Selection.transforms.Length > 0;
}
```

---

## Gizmos and Handles

| | Gizmos | Handles |
|---|---|---|
| Purpose | Draw visual aids | Draw *and* allow interaction |
| Where | `OnDrawGizmos` / `OnDrawGizmosSelected` on the component | `OnSceneGUI` in a custom editor |
| Interactive | ❌ | ✅ drag, rotate, scale |

- ⚠️ **`OnDrawGizmos` runs every Editor frame for every object that has it, selected or not.** On a
  scene with hundreds of such components it visibly slows the Editor.
- ✅ Prefer `OnDrawGizmosSelected` — same visual aid, cost only when the object is selected.
- ✅ Use `Gizmos.DrawWireSphere` and friends over `Gizmos.DrawSphere`; wireframes don't obscure the
  scene.
- ✅ Set `Gizmos.matrix = transform.localToWorldMatrix` to draw in local space rather than doing the
  transform maths yourself.
- ⚠️ Gizmo code is stripped in builds, but any *field* it reads is not. Don't add serialized fields
  that exist only for Gizmos without noting it.

```csharp
private void OnDrawGizmosSelected()
{
    // Local space - respects rotation and scale automatically
    Gizmos.matrix = transform.localToWorldMatrix;

    Gizmos.color = new Color(0f, 1f, 0f, 0.35f);
    Gizmos.DrawWireSphere(Vector3.zero, m_detectionRadius);

    Gizmos.color = Color.yellow;
    Gizmos.DrawLine(Vector3.zero, Vector3.forward * m_facingRange);
}
```

---

## Validation tooling

Editor tooling earns its keep fastest when it catches broken data before it reaches a build.

- ✅ `OnValidate()` runs in the Editor whenever a serialized value changes. Use it to clamp values and
  warn about impossible configurations.
- ⚠️ `OnValidate` runs on load, on every Inspector edit, and during some import operations. Keep it
  cheap and never do anything destructive in it.
- ⚠️ Don't call `Destroy`, instantiate objects, or touch other scene objects from `OnValidate` — Unity
  logs errors for that.
- ✅ For project-wide checks, write a `[MenuItem]` that walks assets with `AssetDatabase.FindAssets`
  and reports problems in one pass.

```csharp
private void OnValidate()
{
    // Clamp nonsense values as they're typed
    m_maxHealth = Mathf.Max(1, m_maxHealth);
    m_detectionRadius = Mathf.Max(0f, m_detectionRadius);

    if (m_projectilePrefab != null && !m_projectilePrefab.TryGetComponent(out Projectile _))
    {
        Debug.LogWarning($"[{name}] Projectile prefab has no Projectile component.", this);
    }
}
```

```csharp
// Project-wide sweep - run it from the menu, or from CI
[MenuItem("MyGame/Validate All ScriptableObjects")]
private static void ValidateAllScriptableObjects()
{
    string[] guids = AssetDatabase.FindAssets("t:WeaponDataSO");
    int problems = 0;

    foreach (string guid in guids)
    {
        string path = AssetDatabase.GUIDToAssetPath(guid);
        var weapon = AssetDatabase.LoadAssetAtPath<WeaponDataSO>(path);

        if (weapon.Damage <= 0)
        {
            Debug.LogError($"{path}: damage must be positive.", weapon);
            problems++;
        }
    }

    Debug.Log($"Validated {guids.Length} weapons, {problems} problem(s).");
}
```

---

## Never edit these by hand

Everything above assumes you're changing Unity data *through Unity*. This section is about what
happens when you don't — and it's the one category in this whole repo where a mistake corrupts the
project rather than just making it untidy.

Unity's asset database is a graph of GUIDs and fileIDs. A `.meta` file assigns a stable GUID to an
asset; every reference anywhere in the project stores that GUID rather than a path. That's why you
can move and rename assets freely inside the Editor — and why touching the files from outside breaks
things that look unrelated.

### The rules

| Never | Why | Instead |
|---|---|---|
| Create or hand-edit a `.meta` file | Unity generates the GUID. A duplicate GUID makes two assets indistinguishable to every reference in the project | Let Unity create it on import |
| Edit `.asset` / `.prefab` / `.unity` / `.controller` / `.mat` / `.anim` YAML | `fileID` and GUID pairs must stay internally consistent; hand edits desynchronise them | An Editor script via `SerializedObject` |
| `mv` / `rm` / `git mv` an asset | The `.meta` is left behind or orphaned; references break | Project window, or `AssetDatabase.MoveAsset` / `DeleteAsset` |
| Rename a serialized field | Serialization is keyed on name — values are silently lost | Add `[FormerlySerializedAs("oldName")]` |
| Reorder or renumber a serialized enum | Values persist as ints; existing assets remap to whatever now holds that number | Append new members at the end |
| Edit `ProjectSettings/` or `manifest.json` with the Editor open | The Editor may rewrite the file on focus | Close the Editor, or use the Settings UI |

⚠️ **A duplicate GUID is the worst of these** because it produces no error. Two assets claim the same
identity and references resolve to whichever Unity indexed last — often differently on another
machine, which is how it turns into "works on my machine" bug reports.

### Renaming a serialized field safely

```csharp
using UnityEngine.Serialization;

public class Health : MonoBehaviour
{
    // Renamed from m_hp. Without this attribute every prefab and scene
    // silently reverts to the default value on next deserialization.
    [FormerlySerializedAs("m_hp")]
    [SerializeField] private int m_maxHealth = 100;
}
```

✅ Leave the attribute in place for at least one release cycle, until every asset has been
re-serialized. Then it's safe to delete.

### Bulk changes go through an Editor script

When serialized data genuinely has to change across many assets, script it against `AssetDatabase`
rather than editing files. This is the same code path the Inspector uses, so GUIDs, prefab
overrides, and Undo all stay correct.

```csharp
[MenuItem("MyGame/Migrate Weapon Damage To Int")]
private static void MigrateWeaponDamage()
{
    string[] guids = AssetDatabase.FindAssets("t:WeaponDataSO");

    AssetDatabase.StartAssetEditing();   // Batch the import work
    try
    {
        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            var asset = AssetDatabase.LoadAssetAtPath<WeaponDataSO>(path);

            var so = new SerializedObject(asset);
            SerializedProperty legacy = so.FindProperty("m_damageFloat");
            SerializedProperty target = so.FindProperty("m_damage");

            if (legacy != null && target != null)
            {
                target.intValue = Mathf.RoundToInt(legacy.floatValue);
                so.ApplyModifiedProperties();      // Writes through Unity, not the file
                EditorUtility.SetDirty(asset);
            }
        }
    }
    finally
    {
        AssetDatabase.StopAssetEditing();          // Always paired, even on exception
        AssetDatabase.SaveAssets();
    }
}
```

⚠️ `StartAssetEditing` / `StopAssetEditing` must be paired in a `try`/`finally`. If an exception
escapes between them, the asset database stays locked and the Editor appears to hang.

---

## Troubleshooting

**An Inspector change doesn't persist after entering Play Mode or restarting.**
The change bypassed serialization. Set values through `SerializedProperty` and call
`serializedObject.ApplyModifiedProperties()`, or `EditorUtility.SetDirty(target)` for a non-inspector
edit. Scene objects also need `EditorSceneManager.MarkSceneDirty`.

**Undo does nothing after a custom tool runs.**
`Undo.RecordObject` was called after the modification instead of before, or not at all. It records
the state at the moment you call it.

**A change to a prefab instance disappears on reload.**
Missing `PrefabUtility.RecordPrefabInstancePropertyModifications`. Without it the change isn't
registered as an override.

**Custom inspector shows nothing when two objects are selected.**
Missing `[CanEditMultipleObjects]`. Add it — and make sure every field goes through
`SerializedProperty`, or multi-edit will write the same value to all of them.

**Build fails with "The type or namespace name 'UnityEditor' could not be found".**
Editor code compiled into a runtime assembly. Move it into an `Editor/` folder, or wrap it in
`#if UNITY_EDITOR`. See
[Assembly Definitions](UnityAssemblyDefinitionsInstructions.md#editor-only-assemblies).

**A serialized field is null in the build but fine in the Editor.**
The field is wrapped in `#if UNITY_EDITOR`, so it exists in one and not the other. Never guard a
serialized field.

**The Editor hangs after running a tool.**
`AssetDatabase.StartAssetEditing()` without a paired `StopAssetEditing()` — an exception escaped
between them. Always use `try`/`finally`.

**The Editor feels sluggish generally.**
Expensive work in `[InitializeOnLoad]`, `OnValidate`, or `OnDrawGizmos` — all of which run far more
often than people expect.
---

## Review checklist

| Check | Look for |
|---|---|
| Build safety | `using UnityEditor;` in a runtime script outside `#if UNITY_EDITOR` |
| Build safety | Editor scripts outside an `Editor/` folder or Editor asmdef |
| Serialization | `#if UNITY_EDITOR` wrapped around a serialized field |
| Multi-edit | `[CustomEditor]` without `[CanEditMultipleObjects]` |
| Undo | Fields set on `target` directly instead of via `SerializedProperty` |
| Undo | `Undo.RecordObject` called after the modification instead of before |
| Prefabs | Missing `RecordPrefabInstancePropertyModifications` on prefab instance edits |
| Editor speed | `OnDrawGizmos` where `OnDrawGizmosSelected` would do |
| Editor speed | Expensive work in `[InitializeOnLoad]` or `OnValidate` |
| Necessity | A custom inspector that only reproduces the default one |
| Asset safety | Hand-edited `.meta` files, or `.meta` without a matching asset |
| Asset safety | Serialized field renamed with no `[FormerlySerializedAs]` |
| Asset safety | Serialized enum members reordered or renumbered |
| Asset safety | `StartAssetEditing` without a `finally { StopAssetEditing(); }` |

---

## Learn more

- [Extending the Editor](https://docs.unity3d.com/6000.3/Documentation/Manual/ExtendingTheEditor.html)
- [Custom Editors](https://docs.unity3d.com/6000.3/Documentation/Manual/editor-CustomEditors.html)
- [SerializedObject and SerializedProperty](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/SerializedObject.html)
