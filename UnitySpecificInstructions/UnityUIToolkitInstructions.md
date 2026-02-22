# Unity UI Toolkit — Complete Reference

**Target: Unity 6.3.4f1 exclusively.** All APIs here are Unity 6.3. Do not use or reference pre-Unity 6 alternatives.

> For C# code style within UI controllers, follow the conventions in `CLAUDE.md` (`m_` prefix, PascalCase properties, Allman braces, etc.)

Official documentation (fetch on demand if an API is not covered here):
→ https://docs.unity3d.com/6000.3/Documentation/Manual/UIElements.html

---

## Table of Contents

1. [File Naming & Organization](#file-naming--organization)
2. [Critical USS vs CSS Differences](#critical-uss-vs-css-differences)
3. [USS Naming Conventions (BEM)](#uss-naming-conventions-bem)
4. [Flexbox Layout System](#flexbox-layout-system)
5. [USS Common Properties Reference](#uss-common-properties-reference)
6. [USS Variables (Design Tokens)](#uss-variables-design-tokens)
7. [USS Pseudo-Classes](#uss-pseudo-classes)
8. [Transitions & Animations](#transitions--animations)
9. [UXML Structure & Best Practices](#uxml-structure--best-practices)
10. [UXML Elements Cheat Sheet](#uxml-elements-cheat-sheet)
11. [Data Binding (Unity 6+)](#data-binding-unity-6)
12. [Custom VisualElements — Unity 6 API](#custom-visualelements--unity-6-api)
13. [Querying Elements](#querying-elements)
14. [Show/Hide Patterns](#showhide-patterns)
15. [Button & Event Handling](#button--event-handling)
16. [ListView & Template Spawning](#listview--template-spawning)
17. [TabView & Tab Styling](#tabview--tab-styling)
18. [Common Patterns & Examples](#common-patterns--examples)
19. [MVP Design Pattern with Data Binding](#mvp-design-pattern-with-data-binding)
20. [Performance Tips](#performance-tips)
21. [Quick Reference: Common Mistakes](#quick-reference-common-mistakes)
22. [Troubleshooting](#troubleshooting)

---

## File Naming & Organization

- ✅ Use **PascalCase** for UXML/USS filenames to align with Unity conventions (e.g., `MainMenu.uxml`, `InventoryPanel.uxml`, `PlayerHUD.uss`).
- ✅ Organize UXML and USS files in a consistent folder structure (e.g., `Assets/UI/UXML/` and `Assets/UI/USS/`).
- ✅ Name USS files to match their corresponding UXML files (e.g., `MainMenu.uss` for `MainMenu.uxml`).

---

## Critical: USS vs CSS Differences

**USS (Unity Style Sheets) is NOT standard CSS.** It is a subset with Unity-specific extensions.

### Full Comparison Table

| Feature | CSS | USS |
|---|---|---|
| Layout model | Flexbox **and** Grid | Flexbox **only** — no `display: grid` |
| Length units | `px`, `%`, `em`, `rem`, `vw`, `vh` | `px` and `%` **only** — no `em`, `rem`, `vw`, `vh` |
| `calc()` | ✅ Supported | ❌ Not supported |
| `z-index` | ✅ Supported | ❌ Not supported — use UXML element order |
| `transform` shorthand | `transform: scale(1.1) rotate(45deg)` | Individual properties: `scale: 1.1;` `rotate: 45deg;` `translate: 10px 0;` |
| `:nth-child()` | ✅ | ❌ Not supported |
| `:not()` | ✅ | ❌ Not supported |
| `:first-child`, `:last-child` | ✅ | ❌ Not supported |
| `:hover`, `:active`, `:focus` | ✅ | ✅ Supported |
| `:checked`, `:disabled`, `:enabled` | ✅ | ✅ Supported |
| Custom pseudo-classes | `:is()`, `:where()` etc. | ❌ Only USS built-in pseudo-classes |
| CSS variables | `--color: red;` on any selector | `--color: red;` in `:root {}` **only** |
| `@media` queries | ✅ | ❌ Not supported |
| `@import` | ✅ | ❌ — use `<Style src="..."/>` in UXML instead |
| Font relative sizing | `em`, `rem` | ❌ — use `px` |
| Color values | Hex `#FF6432`, `rgb()`, `rgba()` | `rgb()` and `rgba()` **only** — ❌ hex values do NOT work |
| Text alignment | `text-align: center` | `-unity-text-align: middle-center` |
| Font style | `font-style: bold` | `-unity-font-style: bold` |
| Background scale | `background-size` | `-unity-background-scale-mode: scale-to-fit` etc. |
| 9-slice borders | No equivalent | `-unity-slice-left/right/top/bottom: Npx` |
| Box model | configurable | `box-sizing: border-box` by default |

### Color Values — Critical

```css
/* ✅ USS - use rgb() or rgba() only */
background-color: rgb(255, 100, 50);
background-color: rgba(255, 100, 50, 0.8);
color: rgb(200, 200, 200);

/* ❌ Hex values do NOT work in USS */
background-color: #FF6432;
```

### Unity-Specific Properties

```css
/* Text */
-unity-font-style: bold;              /* normal, italic, bold, bold-and-italic */
-unity-text-align: middle-center;     /* upper/middle/lower + left/center/right */
-unity-font-definition: url('...');   /* reference to a FontAsset */
-unity-text-outline-width: 1px;
-unity-text-outline-color: rgb(0, 0, 0);

/* Background */
-unity-background-scale-mode: scale-to-fit;  /* scale-and-crop, stretch-to-fill */
-unity-background-image-tint-color: rgb(255, 0, 0);

/* 9-slice for sprite borders */
-unity-slice-left: 10;
-unity-slice-right: 10;
-unity-slice-top: 10;
-unity-slice-bottom: 10;
-unity-slice-scale: 1px;

/* Overflow */
overflow: hidden;    /* USS uses this to clip children */
```

### URL Path Formats

```css
/* Project database path (recommended for assets) */
background-image: url('project://database/Assets/UI/Icons/icon.png');

/* Resource path */
background-image: resource('UI/Icons/icon');

/* Relative path (from USS file location) */
background-image: url('../Icons/icon.png');
```

### Picking Mode

```css
/* Allow element to receive pointer events (default) */
picking-mode: position;

/* Ignore pointer events — pass through to elements behind */
picking-mode: ignore;
```

---

## USS Naming Conventions (BEM)

### Guidelines

- ✅ Use **kebab-case** for UXML `name` and `class` values (e.g., `navbar-menu`, `shop-button`).
- ✅ Use **BEM** (Block-Element-Modifier) for maintainability and consistency.
- ✅ Use `name` for unique identifiers (elements queried in C#) and `class` for reusable styles.
- ✅ Keep `name` unique within its block to improve query performance.
- ✅ Keep selectors **flat and specific**: prefer `.block__element` over deep descendant chains.
- ✅ Use **modifiers** as additive classes (e.g., `.button--small`).
- ✅ Centralize selector string constants in C# to avoid typos.
- ❌ Don't rely on deep descendant selectors (e.g., `.a .b .c`) — they become brittle.
- ❌ Don't overload elements with many unrelated classes.

### BEM Pattern

Pattern: `block-name__element-name--modifier-name`

| Part | Description | Examples |
|------|-------------|----------|
| **Block** | Standalone component | `navbar-menu`, `sidebar`, `login-form` |
| **Element** | Part of a block (use `__`) | `__item`, `__button`, `__input-field` |
| **Modifier** | Variation/state (use `--`) | `--active`, `--collapsed`, `--error` |

### BEM Examples

**Block Names:**
- ✅ `navbar-menu`, `sidebar`, `login-form`
- ❌ `menu` (too generic), `navBarMenu` (camelCase), `navbar_menu` (underscores)

**Element Names:**
- ✅ `navbar-menu__item`, `sidebar__toggle-button`, `login-form__input-field`
- ❌ `navbar-item` (missing block), `sidebar-button` (missing `__`)

**Modifier Names:**
- ✅ `navbar-menu__item--active`, `button--primary`, `login-form__input-field--error`
- ❌ `navbar-menu__item-active` (missing `--`), `sidebar__toggleButton--collapsed` (camelCase)

### UXML Example with BEM

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <!-- Block container -->
  <ui:VisualElement name="navbar-menu" class="navbar-menu">
    <!-- Element with modifier -->
    <ui:Button name="navbar-menu__shop-button"
               class="navbar-menu__shop-button button button--primary"
               text="Shop" />
    <!-- Variant via modifier -->
    <ui:Button name="navbar-menu__settings-button"
               class="navbar-menu__settings-button button button--small"
               text="Settings" />
  </ui:VisualElement>
</ui:UXML>
```

### USS Example with BEM

```css
/* Block base */
.navbar-menu { padding: 8px; }
.navbar-menu > * { margin-right: 8px; }  /* gap: 8px not supported — use margin on children */

/* Element base */
.navbar-menu__shop-button { min-width: 120px; }

/* Generic button system with modifiers */
.button { height: 32px; padding-left: 12px; padding-right: 12px; }
.button--primary { background-color: rgb(40, 120, 240); color: rgb(255, 255, 255); }
.button--small { height: 24px; font-size: 11px; }

/* State classes (toggled from C#) */
.is-selected { border-color: rgb(255, 200, 0); border-width: 2px; }
.is-disabled { opacity: 0.5; }
```

### Centralizing Selectors in C#

```csharp
// Centralize selectors as constants to avoid typos
private const string k_navbarMenu = "navbar-menu";
private const string k_shopButton = "navbar-menu__shop-button";
private const string k_settingsButton = "navbar-menu__settings-button";

// Usage
var navbar = root.Q<VisualElement>(k_navbarMenu);
var shopButton = root.Q<Button>(k_shopButton);
```

### Toggling Classes from C#

```csharp
var btn = root.Q<Button>(k_shopButton);

// Add/remove modifiers
btn.AddToClassList("button--primary");
btn.RemoveFromClassList("button--small");

// Toggle state classes (EnableInClassList sets state directly — more explicit than Toggle)
btn.EnableInClassList("is-selected", true);
btn.EnableInClassList("is-disabled", false);

// Toggle (flips current state)
btn.ToggleInClassList("button--primary");
```

---

## Flexbox Layout System

Unity UI Toolkit uses the **Yoga layout engine**, implementing a subset of CSS Flexbox. There is no grid — every container is a row or a column.

### Container Properties (Parent)

```css
/* Main axis direction */
flex-direction: column;         /* Default - vertical stacking */
flex-direction: row;            /* Horizontal layout */
flex-direction: column-reverse;
flex-direction: row-reverse;

/* Wrapping */
flex-wrap: nowrap;              /* Default - no wrapping */
flex-wrap: wrap;
flex-wrap: wrap-reverse;

/* Main axis alignment */
justify-content: flex-start;   /* Default */
justify-content: flex-end;
justify-content: center;
justify-content: space-between;
justify-content: space-around;

/* Cross axis alignment */
align-items: stretch;          /* Default */
align-items: flex-start;
align-items: flex-end;
align-items: center;

/* ⚠️ gap is NOT supported in USS — use margin on children instead */
/* margin: 0 4px; applied to children achieves spacing */
```

> ❌ **`gap` is not a supported USS property.** To space flex children, use `margin` on the child elements (e.g., `margin-right: 8px;` or `margin-bottom: 8px;`).

### Item Properties (Children)

```css
/* Flexibility */
flex-grow: 1;                  /* Grow to fill available space */
flex-shrink: 1;                /* Default - can shrink */
flex-basis: auto;              /* Default - based on content */
flex-basis: 100px;             /* Fixed basis size */

/* Shorthand */
flex: 1;                       /* flex-grow: 1; flex-shrink: 1; flex-basis: 0; */

/* Individual alignment override */
align-self: center;
```

### Common Layout Patterns

```css
/* Full-screen container */
.fullscreen { flex-grow: 1; }

/* Horizontal toolbar */
.toolbar {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
}

/* Space toolbar children — gap not supported in USS, use margin instead */
.toolbar > * {
    margin-right: 8px;
}

/* Centered content */
.centered-container {
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex-grow: 1;
}

/* Item that fills remaining space */
.content-area {
    flex-grow: 1;
    flex-shrink: 1;
}

/* Item with fixed size */
.sidebar {
    width: 240px;
    flex-shrink: 0;
}
```

### Positioning Modes

```css
/* Relative (Default) - participates in flexbox */
position: relative;
left: 10px;
top: 10px;

/* Absolute - removed from flexbox flow */
position: absolute;
left: 0; right: 0; top: 0; bottom: 0;
```

---

## USS Common Properties Reference

### Display & Visibility

```css
display: flex;                 /* Default - visible */
display: none;                 /* Hidden, removed from layout */

visibility: visible;           /* Default */
visibility: hidden;            /* Hidden, keeps space */

opacity: 1;                    /* 0 to 1 */

overflow: visible;             /* Default */
overflow: hidden;              /* Clip content */
```

### Sizing

```css
width: 100px;
width: 50%;
width: auto;

height: 100px;
min-width: 50px;
max-width: 200px;
min-height: 50px;
max-height: 200px;

flex-grow: 1;                  /* Fill available space */
flex-shrink: 0;                /* Don't shrink */
```

### Spacing

```css
padding: 10px;
padding: 10px 20px;            /* top/bottom left/right */
padding: 10px 20px 15px 25px;  /* top right bottom left */

margin: 10px;
margin-left: auto;             /* Push to right */
```

### Borders

```css
border-width: 2px;
border-color: rgb(0, 0, 0);
border-radius: 8px;
border-top-left-radius: 8px;
```

### Backgrounds

```css
background-color: rgb(50, 50, 50);
background-color: rgba(255, 255, 255, 0.1);
background-image: url('project://database/Assets/UI/background.png');
-unity-background-scale-mode: stretch-to-fill;
-unity-background-scale-mode: scale-to-fit;
-unity-background-image-tint-color: rgb(255, 255, 255);
```

### Text

```css
color: rgb(0, 0, 0);
font-size: 16px;
-unity-font-style: bold;
-unity-text-align: middle-center;
white-space: nowrap;
-unity-text-outline-width: 1px;
-unity-text-outline-color: rgb(0, 0, 0);
```

---

## USS Variables (Design Tokens)

USS variables must be declared in `:root {}`. They cannot be scoped to other selectors.

```css
:root {
    --color-primary: rgb(72, 144, 226);
    --color-secondary: rgb(100, 150, 200);
    --color-surface: rgb(40, 40, 40);
    --color-text: rgb(210, 210, 210);
    --color-text-muted: rgb(140, 140, 140);
    --color-border: rgba(255, 255, 255, 0.15);

    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;

    --radius-sm: 4px;
    --radius-md: 8px;

    --font-size-sm: 12px;
    --font-size-md: 14px;
    --font-size-lg: 18px;

    --border-radius: 4px;
}

.card {
    background-color: var(--color-surface);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    border-width: 1px;
    border-color: var(--color-border);
}

.button--primary {
    background-color: var(--color-primary);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
}
```

---

## USS Pseudo-Classes

Only these pseudo-classes are supported in USS:

| Pseudo-class | Trigger |
|---|---|
| `:hover` | Mouse is over the element |
| `:active` | Element is being pressed |
| `:focus` | Element has keyboard focus |
| `:disabled` | Element has `SetEnabled(false)` |
| `:enabled` | Element is enabled (default) |
| `:checked` | Toggle/RadioButton is on |
| `:selected` | Item is selected in a list |
| `:root` | The root visual element |

```css
.button--primary:hover {
    background-color: rgb(90, 160, 240);
}

.button--primary:active {
    background-color: rgb(55, 120, 200);
    scale: 0.97;
}

.toggle:checked > .toggle__checkmark {
    background-color: var(--color-primary);
}

.input:disabled {
    opacity: 0.4;
}

/* Unity built-in element classes */
.unity-button:disabled {
    opacity: 0.5;
    background-color: rgb(128, 128, 128);
}
```

> ❌ `:nth-child()`, `:not()`, `:first-child`, `:last-child`, `:is()`, `:where()` are **not supported**.

---

## Transitions & Animations

```css
.button {
    background-color: rgb(70, 130, 200);
    scale: 1;
    transition-property: background-color, scale;
    transition-duration: 0.15s, 0.1s;
    transition-timing-function: ease, ease-out;
}

.button:hover {
    background-color: rgb(90, 155, 225);
    scale: 1.05 1.05;
}

.button:active {
    scale: 0.97;
}
```

Animatable properties include: `background-color`, `color`, `opacity`, `scale`, `translate`, `rotate`, `width`, `height`, `margin`, `padding`, `border-color`, `border-width`.

### Transform Properties

```css
scale: 1.5 1.5;
rotate: 45deg;
translate: 10px 20px;
```

---

## UXML Structure & Best Practices

### File Structure

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements"
         editor-extension-mode="False">

    <!-- Reference stylesheets -->
    <Style src="project://database/Assets/UI/Styles/MainStyles.uss" />

    <!-- Root container -->
    <ui:VisualElement name="root" class="container">
        <!-- Content -->
    </ui:VisualElement>

</ui:UXML>
```

### Naming Summary

- **`name`**: kebab-case, unique within its block (`player-panel`, `health-label`) — used for C# queries
- **`class`**: BEM for reusable styles (`card`, `card__title`, `button--primary`)
- **Files**: PascalCase (`MainMenu.uxml`, `InventoryPanel.uss`)

### Data Binding Setup in UXML

```xml
<ui:VisualElement data-source-type="MyDataClass, Assembly-CSharp" name="data-root">
    <ui:Label binding-path="PropertyName" />
</ui:VisualElement>
```

---

## UXML Elements Cheat Sheet

A quick reference for all common UI Toolkit elements with UXML examples and key attributes.

---

### Text Elements

#### Label
Static, non-editable text display.
```xml
<ui:Label text="Hello World" name="my-label" />
<ui:Label text="Styled Label" class="title-text" />
```

#### TextField
Single-line editable text input.
```xml
<ui:TextField label="Username" value="Player1" name="username-field" />
<ui:TextField placeholder-text="Enter name..." />
<ui:TextField password="true" label="Password" />
<ui:TextField multiline="true" label="Description" />
```

---

### Button Elements

#### Button
Clickable button element.
```xml
<ui:Button text="Click Me" name="action-button" />
<ui:Button text="Submit" class="button--primary" />
<ui:Button name="icon-button" class="icon-button">
    <ui:Image class="button-icon" />
</ui:Button>
```

#### Toggle
Checkbox-style on/off control.
```xml
<ui:Toggle label="Enable Sound" value="true" name="sound-toggle" />
<ui:Toggle label="Auto-Save" value="false" />
```

#### RadioButton & RadioButtonGroup
Mutually exclusive selection.
```xml
<ui:RadioButtonGroup value="0" name="difficulty-group">
    <ui:RadioButton label="Easy" />
    <ui:RadioButton label="Normal" />
    <ui:RadioButton label="Hard" />
</ui:RadioButtonGroup>
```

---

### Numeric Input Elements

#### IntegerField
Integer number input.
```xml
<ui:IntegerField label="Count" value="10" name="count-field" />
```

#### FloatField
Decimal number input.
```xml
<ui:FloatField label="Speed" value="1.5" name="speed-field" />
```

#### Slider
Horizontal slider for selecting a float value within a range.
```xml
<ui:Slider label="Volume" low-value="0" high-value="100" value="50" name="volume-slider" />
<ui:Slider low-value="0" high-value="1" value="0.5" show-input-field="true" />
```

#### SliderInt
Integer-only slider.
```xml
<ui:SliderInt label="Level" low-value="1" high-value="10" value="5" name="level-slider" />
<ui:SliderInt low-value="0" high-value="100" value="50" show-input-field="true" />
```

#### MinMaxSlider
Slider with two handles for selecting a range.
```xml
<ui:MinMaxSlider label="Price Range"
                 low-limit="0"
                 high-limit="1000"
                 min-value="100"
                 max-value="500"
                 name="price-range" />
```

---

### Selection Elements

#### DropdownField
Dropdown menu for selecting from a list of options.
```xml
<ui:DropdownField label="Weapon"
                  choices="Sword,Axe,Bow,Staff"
                  index="0"
                  name="weapon-dropdown" />
```

#### EnumField
Dropdown populated from a C# enum type.
```xml
<ui:EnumField label="Direction"
              type="UnityEngine.TextAnchor, UnityEngine.CoreModule"
              value="MiddleCenter" />
```

#### PopupField
Similar to dropdown, configured programmatically.
```xml
<ui:PopupField label="Select Option" name="popup-field" />
```

---

### Display Elements

#### ProgressBar
Visual progress indicator.
```xml
<ui:ProgressBar title="Health"
                low-value="0"
                high-value="100"
                value="75"
                name="health-bar" />
```

#### Image
Displays a sprite or texture.
```xml
<ui:Image name="player-portrait" class="portrait-image" />
<ui:Image name="icon" style="width: 64px; height: 64px;" />
```

#### HelpBox
Information/warning/error message display.
```xml
<ui:HelpBox text="This is an informational message." message-type="Info" />
<ui:HelpBox text="Warning: Low health!" message-type="Warning" />
<ui:HelpBox text="Error: Invalid input" message-type="Error" />
```

---

### Container Elements

#### VisualElement
Base container for grouping and layout.
```xml
<ui:VisualElement name="container" class="panel">
    <ui:Label text="Content here" />
</ui:VisualElement>

<!-- Horizontal row -->
<ui:VisualElement style="flex-direction: row;">
    <ui:Button text="A" />
    <ui:Button text="B" />
</ui:VisualElement>
```

#### ScrollView
Scrollable container for content larger than its viewport.
```xml
<!-- Vertical scrolling (default) -->
<ui:ScrollView name="content-scroll">
    <ui:Label text="Item 1" />
    <ui:Label text="Item 2" />
</ui:ScrollView>

<!-- Horizontal scrolling -->
<ui:ScrollView mode="Horizontal" name="horizontal-scroll">
    <ui:VisualElement style="flex-direction: row;">
        <ui:Image name="img1" />
        <ui:Image name="img2" />
    </ui:VisualElement>
</ui:ScrollView>

<!-- Both directions -->
<ui:ScrollView mode="VerticalAndHorizontal"
               horizontal-scroller-visibility="Auto"
               vertical-scroller-visibility="AlwaysVisible">
    <!-- Large content -->
</ui:ScrollView>
```

**ScrollView Attributes:**
| Attribute | Values | Description |
|-----------|--------|-------------|
| `mode` | `Vertical`, `Horizontal`, `VerticalAndHorizontal` | Scroll direction |
| `horizontal-scroller-visibility` | `Auto`, `AlwaysVisible`, `Hidden` | Scrollbar display |
| `vertical-scroller-visibility` | `Auto`, `AlwaysVisible`, `Hidden` | Scrollbar display |
| `touch-scroll-type` | `Unrestricted`, `Elastic`, `Clamped` | Touch behavior |

#### GroupBox
Visually grouped container with a label.
```xml
<ui:GroupBox text="Player Settings" name="player-settings-group">
    <ui:TextField label="Name" />
    <ui:Slider label="Volume" low-value="0" high-value="100" value="50" />
    <ui:Toggle label="Mute" value="false" />
</ui:GroupBox>
```

#### Foldout
Collapsible/expandable container.
```xml
<ui:Foldout text="Advanced Options" value="false" name="advanced-foldout">
    <ui:Toggle label="Debug Mode" value="false" />
    <ui:IntegerField label="Max FPS" value="60" />
</ui:Foldout>

<!-- Starts expanded -->
<ui:Foldout text="Basic Settings" value="true">
    <ui:Slider label="Brightness" low-value="0" high-value="100" value="50" />
</ui:Foldout>
```

#### Box
Simple container with default styling (border).
```xml
<ui:Box name="content-box">
    <ui:Label text="Boxed content" />
</ui:Box>
```

#### TemplateContainer
Placeholder for instantiated UXML templates.
```xml
<ui:TemplateContainer name="card-slot" />
```

#### IMGUIContainer
Embed legacy IMGUI rendering. **Editor UI only.**
```xml
<ui:IMGUIContainer name="imgui-preview" />
```

---

### List & Tree Elements

#### ListView
Virtualized list for displaying large data sets efficiently. Populated via C# with `makeItem`/`bindItem`.
```xml
<ui:ListView name="inventory-list"
             fixed-item-height="50"
             virtualization-method="FixedHeight"
             selection-type="Single"
             show-alternating-row-backgrounds="ContentOnly"
             show-border="true" />

<!-- Multiple selection -->
<ui:ListView name="multi-select-list"
             fixed-item-height="40"
             selection-type="Multiple" />

<!-- Reorderable list -->
<ui:ListView name="reorderable-list"
             fixed-item-height="30"
             reorderable="true" />
```

**ListView Attributes:**
| Attribute | Values | Description |
|-----------|--------|-------------|
| `fixed-item-height` | `30`, `50`, etc. | Height of each item (pixels) |
| `virtualization-method` | `FixedHeight`, `DynamicHeight` | Performance mode |
| `selection-type` | `None`, `Single`, `Multiple` | Selection behavior |
| `show-alternating-row-backgrounds` | `None`, `ContentOnly`, `All` | Zebra striping |
| `show-border` | `true`, `false` | Border visibility |
| `reorderable` | `true`, `false` | Drag to reorder |

**C# Setup:**
```csharp
var listView = root.Q<ListView>("inventory-list");
listView.makeItem = () => new Label();
listView.bindItem = (element, index) => ((Label)element).text = m_items[index].Name;
listView.itemsSource = m_items;

// Refresh when data changes
listView.RefreshItems();
```

#### TreeView
Hierarchical tree structure for nested data.
```xml
<ui:TreeView name="file-tree"
             fixed-item-height="24"
             selection-type="Single"
             show-border="true" />
```

**C# Setup:**
```csharp
var treeView = root.Q<TreeView>("file-tree");
treeView.makeItem = () => new Label();
treeView.bindItem = (element, index) =>
{
    var item = treeView.GetItemDataForIndex<FileItem>(index);
    ((Label)element).text = item.Name;
};
treeView.SetRootItems(m_rootItems);
```

#### MultiColumnListView
Table-like list with multiple sortable columns.
```xml
<ui:MultiColumnListView name="data-table"
                        fixed-item-height="30"
                        show-border="true"
                        show-alternating-row-backgrounds="ContentOnly"
                        sorting-enabled="true">
    <ui:Columns>
        <ui:Column name="name-column" title="Name" width="150" />
        <ui:Column name="type-column" title="Type" width="100" />
        <ui:Column name="value-column" title="Value" width="80" stretchable="true" />
    </ui:Columns>
</ui:MultiColumnListView>
```

**Column Attributes:**
| Attribute | Description |
|-----------|-------------|
| `name` | Unique identifier for the column |
| `title` | Header text displayed |
| `width` | Initial width in pixels |
| `min-width` | Minimum width |
| `max-width` | Maximum width |
| `stretchable` | Whether column stretches to fill space |
| `sortable` | Enable sorting by this column |
| `resizable` | Allow user to resize |

**C# Setup:**
```csharp
var table = root.Q<MultiColumnListView>("data-table");
table.columns["name-column"].makeCell = () => new Label();
table.columns["name-column"].bindCell = (element, index) =>
    ((Label)element).text = m_data[index].Name;
table.itemsSource = m_data;
```

#### MultiColumnTreeView
Hierarchical tree with multiple columns (e.g., file explorer).
```xml
<ui:MultiColumnTreeView name="hierarchy-view"
                        fixed-item-height="24"
                        show-border="true">
    <ui:Columns>
        <ui:Column name="name" title="Name" width="200" />
        <ui:Column name="size" title="Size" width="80" />
        <ui:Column name="date" title="Modified" width="120" />
    </ui:Columns>
</ui:MultiColumnTreeView>
```

---

### Tab Elements

#### TabView & Tab
Tabbed interface for switching between content panels. See [TabView & Tab Styling](#tabview--tab-styling) for USS selectors.

```xml
<ui:TabView name="main-tabs" reorderable="false">
    <ui:Tab label="Inventory" name="inventory-tab">
        <ui:ScrollView>
            <ui:Label text="Inventory content here" />
        </ui:ScrollView>
    </ui:Tab>
    <ui:Tab label="Skills" name="skills-tab">
        <ui:Label text="Skills content here" />
    </ui:Tab>
</ui:TabView>

<!-- With icons -->
<ui:TabView>
    <ui:Tab label="Home" icon-image="project://database/Assets/Icons/home.png">
        <ui:Label text="Home content" />
    </ui:Tab>
</ui:TabView>

<!-- Closeable tabs -->
<ui:TabView>
    <ui:Tab label="Document 1" closeable="true">
        <ui:Label text="Document content" />
    </ui:Tab>
</ui:TabView>
```

**Tab Attributes:**
| Attribute | Description |
|-----------|-------------|
| `label` | Text displayed on the tab |
| `icon-image` | Path to icon image |
| `closeable` | Show close button on tab |
| `view-data-key` | Key for persistence |

---

### Bound Input Elements

These elements commonly bind to data properties using `binding-path`:

```xml
<!-- Bind to int property -->
<ui:IntegerField label="Health" binding-path="Health" />

<!-- Bind to float property -->
<ui:FloatField label="Speed" binding-path="Speed" />

<!-- Bind to string property -->
<ui:TextField label="Name" binding-path="PlayerName" />

<!-- Bind to bool property -->
<ui:Toggle label="Active" binding-path="IsActive" />

<!-- Bind slider to float property -->
<ui:Slider label="Volume" low-value="0" high-value="1" binding-path="Volume" />

<!-- Progress bar bound to value with explicit binding mode -->
<ui:ProgressBar low-value="0" high-value="100" binding-path="HealthPercent">
    <Bindings>
        <ui:DataBinding property="value" binding-mode="ToTarget" />
    </Bindings>
</ui:ProgressBar>
```

---

### Quick Reference Table

| Element | Purpose | Key Attributes |
|---------|---------|----------------|
| `Label` | Display text | `text` |
| `TextField` | Text input | `value`, `placeholder-text`, `multiline`, `password` |
| `Button` | Clickable action | `text` |
| `Toggle` | Checkbox | `label`, `value` |
| `RadioButtonGroup` | Exclusive selection | `value` (index) |
| `IntegerField` | Integer input | `label`, `value` |
| `FloatField` | Decimal input | `label`, `value` |
| `Slider` | Float range | `low-value`, `high-value`, `value` |
| `SliderInt` | Integer range | `low-value`, `high-value`, `value` |
| `MinMaxSlider` | Range selection | `low-limit`, `high-limit`, `min-value`, `max-value` |
| `DropdownField` | Selection list | `choices`, `index` |
| `ProgressBar` | Progress display | `value`, `high-value`, `title` |
| `Image` | Display image | (set via C# or USS) |
| `ScrollView` | Scrollable area | `mode`, `*-scroller-visibility` |
| `GroupBox` | Grouped container | `text` |
| `Foldout` | Collapsible | `text`, `value` (expanded state) |
| `ListView` | Virtualized list | `fixed-item-height`, `selection-type` |
| `TreeView` | Hierarchical list | `fixed-item-height` |
| `MultiColumnListView` | Table view | `<ui:Columns>` children |
| `TabView` | Tab container | `reorderable` |
| `Tab` | Tab content | `label`, `closeable`, `icon-image` |
| `Box` | Bordered container | — |
| `HelpBox` | Info/Warning/Error | `text`, `message-type` |

---

## Data Binding (Unity 6+)

Unity 6 introduced a full **runtime** data binding system. This is entirely separate from `SerializedObject.Bind()` which is **Editor-only**.

### Reactive Data Source (Runtime Updates)

Implement `INotifyBindablePropertyChanged` for automatic UI updates when data changes at runtime:

```csharp
using System;
using Unity.Properties;
using UnityEngine;
using UnityEngine.UIElements; // Required for INotifyBindablePropertyChanged and BindablePropertyChangedEventArgs

[CreateAssetMenu(fileName = "PlayerData", menuName = "Game Data/Player")]
public class PlayerDataSO : ScriptableObject, INotifyBindablePropertyChanged
{
    public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;

    [SerializeField] private int m_health = 100;
    [SerializeField] private string m_playerName = "Player";

    [CreateProperty]
    public int Health
    {
        get => m_health;
        set
        {
            if (m_health != value)
            {
                m_health = value;
                Notify(nameof(Health));
            }
        }
    }

    [CreateProperty]
    public string PlayerName
    {
        get => m_playerName;
        set
        {
            if (m_playerName != value)
            {
                m_playerName = value;
                Notify(nameof(PlayerName));
            }
        }
    }

    private void Notify(string propertyName)
    {
        propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(propertyName));
    }
}
```

> ⚠️ **Without `INotifyBindablePropertyChanged`**, bindings only update on initial assignment — UI will not react to subsequent data changes.

### Simple Data Source (Read-Only / One-Time)

For static or one-time binding, `INotifyBindablePropertyChanged` is not required:

```csharp
using Unity.Properties;
using UnityEngine;

[CreateAssetMenu(fileName = "ItemData", menuName = "Game Data/Item")]
public class ItemDataSO : ScriptableObject
{
    [SerializeField] private string m_itemName;
    [SerializeField] private int m_cost;

    [CreateProperty]
    public string ItemName => m_itemName;

    [CreateProperty]
    public int Cost => m_cost;
}
```

This pattern works when data doesn't change at runtime, or when you manually reassign `dataSource` to trigger a refresh.

### Binding in UXML

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement data-source-type="PlayerDataSO, Assembly-CSharp" name="player-panel">
        <ui:Label binding-path="PlayerName" name="name-label" />
        <ui:ProgressBar binding-path="Health" low-value="0" high-value="100" />
    </ui:VisualElement>
</ui:UXML>
```

> ⚠️ `binding-path` is **case-sensitive** — it must match the exact C# property name.

### Setting the Data Source in C#

```csharp
public class UIController : MonoBehaviour
{
    [SerializeField] private UIDocument m_uiDocument;
    [SerializeField] private PlayerDataSO m_playerData;

    private void OnEnable()
    {
        var root = m_uiDocument.rootVisualElement;
        var playerPanel = root.Q<VisualElement>("player-panel");

        // Assign data source — resolves all UXML binding-path declarations
        playerPanel.dataSource = m_playerData;
    }
}
```

### Manual Binding via SetBinding() (C#)

For programmatic bindings not declared in UXML:

```csharp
using UnityEngine.UIElements;
using Unity.Properties;

var label = root.Q<Label>("player-name");

// One-way: data → UI
label.SetBinding("text", new DataBinding
{
    dataSourcePath = new PropertyPath(nameof(PlayerDataSO.PlayerName)),
    bindingMode = BindingMode.ToTarget
});

// Two-way binding
var slider = root.Q<Slider>("health-bar");
slider.SetBinding("value", new DataBinding
{
    dataSourcePath = new PropertyPath(nameof(PlayerDataSO.Health)),
    bindingMode = BindingMode.TwoWay
});
```

### Binding Modes

| Mode | Direction | Use Case |
|---|---|---|
| `BindingMode.ToTarget` | Data → UI | Display-only (health bar, score display) |
| `BindingMode.ToSource` | UI → Data | Input that writes back to data |
| `BindingMode.TwoWay` | Both | Settings, editable fields |
| `BindingMode.ToTargetOnce` | Data → UI (once) | Initial value only, no further updates |

---

## Data Binding — Editor / SerializedObject

`SerializedObject.Bind()` is for **Editor windows and custom Inspectors only**. It does not work at runtime.

❌ **Never use `SerializedObject.Bind()` for runtime UIDocument:**
```csharp
// Wrong for runtime — editor-only API
var so = new SerializedObject(targetObject);
rootVisualElement.Bind(so);
```

✅ **Use this for Editor windows only:**
```csharp
// Correct — EditorWindow or custom Inspector context only
var so = new SerializedObject(targetObject);
rootVisualElement.Bind(so);

// Bind a specific property to a specific field
var property = so.FindProperty("fieldName");
var field = new PropertyField(property);
field.BindProperty(property);
rootVisualElement.Add(field);
```

For runtime UI, use `SetBinding()` and `binding-path` — see [Data Binding (Unity 6+)](#data-binding-unity-6) above.

---

## Custom VisualElements — Unity 6 API

Unity 6 replaced the old `UxmlFactory`/`UxmlTraits` registration system entirely.

❌ **Never use this — deprecated, generates compiler warnings in Unity 6:**
```csharp
// Pre-Unity 6 — do not write this
public new class UxmlFactory : UxmlFactory<MyElement, UxmlTraits> { }
public new class UxmlTraits : VisualElement.UxmlTraits
{
    public override void Init(VisualElement ve, IUxmlAttributes bag, CreationContext cc) { }
}
```

✅ **Always use this — Unity 6.3 API:**
```csharp
using UnityEngine.UIElements;

/// <summary>
/// A custom health bar element usable directly in UXML.
/// </summary>
[UxmlElement]
public partial class HealthBar : VisualElement
{
    // Exposed as an attribute in UXML — Unity 6.3 generates the registration code automatically
    [UxmlAttribute]
    public float maxHealth { get; set; } = 100f;

    [UxmlAttribute]
    public string label { get; set; } = "HP";

    private Label m_label;
    private VisualElement m_fill;

    public HealthBar()
    {
        AddToClassList("health-bar");

        m_label = new Label(label);
        m_label.AddToClassList("health-bar__label");

        m_fill = new VisualElement();
        m_fill.AddToClassList("health-bar__fill");

        Add(m_label);
        Add(m_fill);
    }

    public void SetValue(float current)
    {
        float pct = Mathf.Clamp01(current / maxHealth) * 100f;
        m_fill.style.width = Length.Percent(pct);
    }
}
```

Use in UXML:
```xml
<MyNamespace.HealthBar max-health="100" label="HP" name="player-health" />
```

---

## Querying Elements

### Basic Queries

```csharp
// By name
var button = root.Q<Button>("submit-button");

// By type only (first match)
var firstLabel = root.Q<Label>();

// By USS class
var cards = root.Query<VisualElement>(className: "card").ToList();

// By name AND class
var specificCard = root.Q<VisualElement>("my-card", "card--highlighted");

// All of a type
var allButtons = root.Query<Button>().ToList();

// Chained — find within a subsection
var panelButton = root.Q<VisualElement>("settings-panel").Q<Button>("close-button");

// With predicate (avoid in hot paths — allocates)
var activeItems = root.Query<VisualElement>()
    .Where(e => e.ClassListContains("card--active"))
    .ToList();
```

### Null Safety

```csharp
var button = root.Q<Button>("optional-button");
if (button != null)
{
    button.clicked += OnClicked;
}

// Null-conditional for one-liners
root.Q<Button>("optional-button")?.SetEnabled(false);
```

### Cache Queries — Never Call in Update

```csharp
// ✅ Good — cached in OnEnable (preferred for UIDocument MonoBehaviours)
private Button m_submitButton;

private void OnEnable()
{
    var root = m_uiDocument.rootVisualElement;
    m_submitButton = root.Q<Button>("submit-button");
    m_submitButton.clicked += OnSubmitClicked;
}

private void OnDisable()
{
    m_submitButton.clicked -= OnSubmitClicked;
}

// ❌ Bad — queried every frame
private void Update()
{
    m_uiDocument.rootVisualElement.Q<Button>("submit-button").SetEnabled(false);
}
```

### Query Timing

```csharp
// ✅ OnEnable is the recommended place to query for UIDocument MonoBehaviours.
//    UIDocument is guaranteed to have its rootVisualElement populated here.
private void OnEnable()
{
    var root = m_uiDocument.rootVisualElement;
    m_button = root.Q<Button>("my-button");
    m_button.clicked += OnButtonClicked;
}

private void OnDisable()
{
    m_button.clicked -= OnButtonClicked;
}

/// ⚠️ Awake: querying rootVisualElement here works if UIDocument is on the
//    same GameObject (it initialises synchronously in Awake), but it means
//    queries and subscriptions happen in different lifecycle methods.
//    Prefer OnEnable so queries and event registration stay together.
private void Awake()
{
    m_uiDocument = GetComponent<UIDocument>(); // Component lookup is fine in Awake
}

// ✅ CreateGUI is the correct method for EditorWindows
public void CreateGUI()
{
    visualTree.CloneTree(rootVisualElement);
    var button = rootVisualElement.Q<Button>(); // Always safe here
}
```

---

## Show/Hide Patterns

### Display Property (Removes from Layout)

```csharp
// Hide — removes from layout (element takes no space)
element.style.display = DisplayStyle.None;

// Show — returns to layout
element.style.display = DisplayStyle.Flex;

// Helper method pattern
public void SetPanelVisible(bool isVisible)
{
    m_panel.style.display = isVisible ? DisplayStyle.Flex : DisplayStyle.None;
}
```

### Visibility Property (Keeps Layout Space)

```csharp
// Hide but keep space
element.style.visibility = Visibility.Hidden;

// Show
element.style.visibility = Visibility.Visible;
```

> Use `display` to completely remove an element from layout. Use `visibility` when you need the space preserved (e.g., to avoid layout shifts).

---

## Button & Event Handling

### Button Click Events

```csharp
private Button m_actionButton;

private void OnEnable()
{
    var root = m_uiDocument.rootVisualElement;
    m_actionButton = root.Q<Button>("action-button");
    m_actionButton.clicked += OnActionButtonClicked;
}

private void OnDisable()
{
    // Always unsubscribe to prevent memory leaks
    m_actionButton.clicked -= OnActionButtonClicked;
}

private void OnActionButtonClicked()
{
    Debug.Log("Action button clicked");
}
```

### Enable/Disable Buttons

```csharp
button.SetEnabled(false);  // Disable (grayed out)
button.SetEnabled(true);   // Enable

if (button.enabledSelf) { /* Button is enabled */ }
```

### Other Event Types

```csharp
// Generic event registration
button.RegisterCallback<ClickEvent>(OnClick);

// Pointer events
element.RegisterCallback<PointerEnterEvent>(evt => Debug.Log("Mouse entered"));
element.RegisterCallback<PointerLeaveEvent>(evt => Debug.Log("Mouse left"));

// Value changed
textField.RegisterValueChangedCallback(evt =>
{
    Debug.Log($"Value changed to {evt.newValue}");
});
slider.RegisterValueChangedCallback(evt =>
{
    Debug.Log($"Changed: {evt.previousValue} → {evt.newValue}");
});

// Keyboard
element.RegisterCallback<KeyDownEvent>(evt =>
{
    if (evt.keyCode == KeyCode.Return) Submit();
});

// Event propagation
button.RegisterCallback<ClickEvent>(evt =>
{
    evt.StopPropagation();
});

// Cleanup — OnDisable for MonoBehaviour, OnDestroy for EditorWindow
private void OnDisable()
{
    button.clicked -= OnButtonClicked;
    button.UnregisterCallback<ClickEvent>(OnClick);
}
```

### Using EventRegistry (Project Standard)

The project's `EventRegistry` utility (in `GameSystems` namespace) provides centralised cleanup — prefer this over manual subscribe/unsubscribe:

```csharp
using GameSystems;

private readonly EventRegistry m_eventRegistry = new();

private void OnEnable()
{
    m_eventRegistry.RegisterCallback<ClickEvent>(m_submitButton, OnSubmitClicked);
    m_eventRegistry.RegisterCallback<ClickEvent>(m_cancelButton, OnCancelClicked);
    m_eventRegistry.RegisterValueChangedCallback<float>(m_volumeSlider, OnVolumeChanged);
}

private void OnDisable()
{
    m_eventRegistry.Dispose(); // Unregisters everything at once
}
```

---

## ListView & Template Spawning

### VisualTreeAsset Instantiation (Manual Grid/List)

```csharp
public class CardGridController : MonoBehaviour
{
    [SerializeField] private UIDocument m_uiDocument;
    [SerializeField] private VisualTreeAsset m_cardTemplate;
    [SerializeField] private List<CardDataSO> m_cards;

    private VisualElement m_cardContainer;

    private void OnEnable()
    {
        var root = m_uiDocument.rootVisualElement;
        m_cardContainer = root.Q<VisualElement>("card-container");
        PopulateCards();
    }

    private void PopulateCards()
    {
        m_cardContainer.Clear();

        foreach (var cardData in m_cards)
        {
            // Instantiate template
            var cardElement = m_cardTemplate.Instantiate();

            // Populate via queries or data binding
            cardElement.Q<Label>("card-title").text = cardData.Title;
            cardElement.Q<Label>("card-cost").text = cardData.Cost.ToString();
            cardElement.dataSource = cardData;

            // Setup button (capture loop variable)
            var data = cardData;
            var actionButton = cardElement.Q<Button>("action-button");
            if (actionButton != null)
            {
                actionButton.clicked += () => OnCardActionClicked(data);
            }

            m_cardContainer.Add(cardElement);
        }
    }

    private void OnCardActionClicked(CardDataSO cardData)
    {
        Debug.Log($"Card clicked: {cardData.Title}");
    }
}
```

### ListView with makeItem/bindItem (Virtualized)

```csharp
private void SetupListView()
{
    m_listView.makeItem = () => m_itemTemplate.Instantiate();

    m_listView.bindItem = (element, index) =>
    {
        var item = m_items[index];
        element.Q<Label>("item-name").text = item.ItemName;
        element.Q<Label>("item-cost").text = $"{item.Cost} gold";
        element.dataSource = item;
    };

    m_listView.itemsSource = m_items;
}

// Refresh when data changes
public void RefreshList() => m_listView.RefreshItems();
```

**ListView UXML:**
```xml
<ui:ListView name="inventory-list"
             fixed-item-height="60"
             virtualization-method="FixedHeight"
             selection-type="Single" />
```

---

## TabView & Tab Styling

### USS Selectors

```css
/* TabView container */
.unity-tab-view { }
.unity-tab-view__content-container { }

/* Tab headers */
.unity-tab { }
.unity-tab__header { }
.unity-tab__header:checked { }      /* Active tab */
.unity-tab__header:hover { }
.unity-tab__header-label { }
.unity-tab__header-underline { }
```

### Styling Tabs

```css
.unity-tab__header {
    background-color: rgb(230, 230, 230);
    padding: 10px 20px;
    border-radius: 4px 4px 0 0;
    -unity-font-style: bold;
    color: rgb(0, 0, 0);
}

.unity-tab__header:checked {
    background-color: rgb(100, 150, 200);
    color: rgb(255, 255, 255);
}

.unity-tab__header:hover {
    background-color: rgb(200, 200, 200);
}

/* Hide underline */
.unity-tab__header-underline {
    opacity: 0;
}
```

### C# Tab Events

```csharp
private TabView m_tabView;

private void OnEnable()
{
    m_tabView = root.Q<TabView>("main-tabs");
    m_tabView.activeTabChanged += OnActiveTabChanged;
}

private void OnDisable()
{
    m_tabView.activeTabChanged -= OnActiveTabChanged;
}

private void OnActiveTabChanged(Tab previousTab, Tab newTab)
{
    Debug.Log($"Tab changed to {newTab?.label}");
}
```

---

## Common Patterns & Examples

### Full-Screen UI

```xml
<ui:VisualElement name="root" style="flex-grow: 1;">
    <!-- Content -->
</ui:VisualElement>
```

### Header / Content / Footer

```xml
<ui:VisualElement style="flex-grow: 1;">
    <ui:VisualElement class="header" style="height: 60px;" />
    <ui:VisualElement class="content" style="flex-grow: 1;" />
    <ui:VisualElement class="footer" style="height: 40px;" />
</ui:VisualElement>
```

### Centered Modal

```css
.overlay {
    position: absolute;
    left: 0; top: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
}

.modal {
    width: 400px;
    background-color: rgb(255, 255, 255);
    border-radius: 8px;
    padding: 20px;
}
```

### Two-Column Layout

```xml
<ui:VisualElement style="flex-direction: row; flex-grow: 1;">
    <ui:VisualElement class="sidebar" style="width: 200px;" />
    <ui:VisualElement class="main-content" style="flex-grow: 1;" />
</ui:VisualElement>
```

---

## MVP Design Pattern with Data Binding

This section demonstrates a clean **Model-View-Presenter (MVP)** architecture using Unity 6 runtime data binding, separating data (Model), UI display (View), and game logic (Presenter).

### View Naming Convention

**View classes use the `*View` suffix** to clearly distinguish UI presentation layer classes from controllers:

| Class Type | Example | Location | Responsibility |
|------------|---------|----------|-----------------|
| View | `BuildingsView.cs` | `Assets/UI Toolkit/Scripts/Map/` | UI display and event subscription only (inherits `UITKBaseClass`) |
| View | `DiplomacyView.cs` | `Assets/UI Toolkit/Scripts/Diplomacy/` | Render relationship data, subscribe to diplomacy events |
| View | `ArmyRecruitView.cs` | `Assets/UI Toolkit/Scripts/Army/` | Display recruitable units, handle recruitment UI |
| Presenter/Controller | `BuildingsController.cs` | `Assets/Scripts/Map/` | Game logic, data manipulation, event orchestration |
| Presenter/Controller | `DiplomacyController.cs` | `Assets/Scripts/Diplomacy/` | Manage relationships, treaties, AI decisions |
| Model | `FactionDataSO.cs` | `Assets/Scripts/Core/` | Pure data — no UI or logic |

**Why this convention?**
- ✅ Immediately communicates: "This class handles UI presentation"
- ✅ Easy to distinguish from Controllers/Presenters (which contain game logic)
- ✅ Consistent with industry MVP/MVC conventions
- ✅ All `*View` classes inherit `UITKBaseClass` and use the Template Method pattern

**View Responsibilities (Pure MVP View):**
- Cache UI element references via `InitializeElements()`
- Subscribe to events for reactive updates
- Populate UI from data sources
- Emit user input back to Presenter via events
- **No business logic** — only UI rendering and event handling

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    dataSource    ┌──────────────────────┐    │
│  │    MODEL     │ ───────────────▶ │        VIEW          │    │
│  │ (Data Class) │                  │ (MonoBehaviour +     │    │
│  │              │ ◀─────────────── │  UIDocument + UXML)  │    │
│  └──────────────┘  INotifyBindable │                      │    │
│         ▲          PropertyChanged └──────────────────────┘    │
│         │                                    │                  │
│         │ Modifies                           │ User Input       │
│         │                                    ▼                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    PRESENTER / CONTROLLER                 │  │
│  │                  (MonoBehaviour - Game Logic)             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Complete Example: Player Stats Panel

#### 1. Model (Data Class)

```csharp
// PlayerStatsModel.cs
using System;
using Unity.Properties;
using UnityEngine;
using UnityEngine.UIElements; // Required for INotifyBindablePropertyChanged and BindablePropertyChangedEventArgs

namespace Game.Models
{
    /// <summary>
    /// Model: Holds player stats data with reactive binding support.
    /// </summary>
    [CreateAssetMenu(fileName = "PlayerStats", menuName = "Game Data/Player Stats")]
    public class PlayerStatsModel : ScriptableObject, INotifyBindablePropertyChanged
    {
        public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;

        [Header("Stats Configuration")]
        [SerializeField] private int m_maxHealth = 100;
        [SerializeField] private int m_maxStamina = 100;

        [Header("Current Values")]
        [SerializeField] private int m_currentHealth = 100;
        [SerializeField] private int m_currentStamina = 100;
        [SerializeField] private int m_gold = 0;
        [SerializeField] private string m_playerName = "Hero";

        [CreateProperty]
        public int MaxHealth => m_maxHealth;

        [CreateProperty]
        public int MaxStamina => m_maxStamina;

        [CreateProperty]
        public int CurrentHealth
        {
            get => m_currentHealth;
            set
            {
                int clampedValue = Mathf.Clamp(value, 0, m_maxHealth);
                if (m_currentHealth != clampedValue)
                {
                    m_currentHealth = clampedValue;
                    Notify(nameof(CurrentHealth));
                    Notify(nameof(HealthPercent)); // Notify derived property too
                }
            }
        }

        [CreateProperty]
        public int CurrentStamina
        {
            get => m_currentStamina;
            set
            {
                int clampedValue = Mathf.Clamp(value, 0, m_maxStamina);
                if (m_currentStamina != clampedValue)
                {
                    m_currentStamina = clampedValue;
                    Notify(nameof(CurrentStamina));
                    Notify(nameof(StaminaPercent));
                }
            }
        }

        [CreateProperty]
        public int Gold
        {
            get => m_gold;
            set
            {
                if (m_gold != value)
                {
                    m_gold = Mathf.Max(0, value);
                    Notify(nameof(Gold));
                }
            }
        }

        [CreateProperty]
        public string PlayerName
        {
            get => m_playerName;
            set
            {
                if (m_playerName != value)
                {
                    m_playerName = value;
                    Notify(nameof(PlayerName));
                }
            }
        }

        // Derived properties for progress bars (0-100 range)
        [CreateProperty]
        public float HealthPercent => m_maxHealth > 0 ? (float)m_currentHealth / m_maxHealth * 100f : 0f;

        [CreateProperty]
        public float StaminaPercent => m_maxStamina > 0 ? (float)m_currentStamina / m_maxStamina * 100f : 0f;

        private void Notify(string propertyName)
        {
            propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(propertyName));
        }

        public void ResetStats()
        {
            CurrentHealth = m_maxHealth;
            CurrentStamina = m_maxStamina;
        }
    }
}
```

#### 2. View (UI Controller)

```csharp
// PlayerStatsView.cs
using GameSystems;
using UnityEngine;
using UnityEngine.UIElements;

namespace Game.Views
{
    /// <summary>
    /// View: Handles UI display and user input for player stats.
    /// </summary>
    [RequireComponent(typeof(UIDocument))]
    public class PlayerStatsView : MonoBehaviour
    {
        [Header("Data Source")]
        [SerializeField] private PlayerStatsModel m_playerStats;

        [Header("References")]
        [SerializeField] private PlayerStatsPresenter m_presenter;

        private UIDocument m_uiDocument;
        private VisualElement m_rootPanel;
        private Button m_healButton;
        private Button m_damageButton;
        private Button m_restButton;

        // EventRegistry handles cleanup automatically — avoids lambda unregister issues
        private readonly EventRegistry m_eventRegistry = new();

        private void Awake()
        {
            m_uiDocument = GetComponent<UIDocument>();
        }

        private void OnEnable()
        {
            // Query elements in OnEnable — UIDocument is guaranteed ready here
            var root = m_uiDocument.rootVisualElement;
            m_rootPanel = root.Q<VisualElement>("player-stats-panel");

            if (m_rootPanel != null && m_playerStats != null)
            {
                m_rootPanel.dataSource = m_playerStats;
            }

            m_healButton = root.Q<Button>("heal-button");
            m_damageButton = root.Q<Button>("damage-button");
            m_restButton = root.Q<Button>("rest-button");

            if (m_healButton != null)
                m_eventRegistry.RegisterCallback<ClickEvent>(m_healButton, OnHealClicked);
            if (m_damageButton != null)
                m_eventRegistry.RegisterCallback<ClickEvent>(m_damageButton, OnDamageClicked);
            if (m_restButton != null)
                m_eventRegistry.RegisterCallback<ClickEvent>(m_restButton, OnRestClicked);
        }

        private void OnDisable()
        {
            m_eventRegistry.Dispose(); // Unregisters all callbacks at once
        }

        private void OnHealClicked(ClickEvent evt) => m_presenter?.OnHealClicked();
        private void OnDamageClicked(ClickEvent evt) => m_presenter?.OnDamageClicked();
        private void OnRestClicked(ClickEvent evt) => m_presenter?.OnRestClicked();

        public void ShowPanel(bool show)
        {
            if (m_rootPanel != null)
            {
                m_rootPanel.style.display = show ? DisplayStyle.Flex : DisplayStyle.None;
            }
        }
    }
}
```

#### 3. Presenter (Game Logic)

```csharp
// PlayerStatsPresenter.cs
using UnityEngine;

namespace Game.Presenters
{
    /// <summary>
    /// Presenter: Contains game logic for player stats.
    /// Modifies the Model in response to game events and user actions.
    /// </summary>
    public class PlayerStatsPresenter : MonoBehaviour
    {
        [Header("Model Reference")]
        [SerializeField] private PlayerStatsModel m_playerStats;

        [Header("Game Settings")]
        [SerializeField] private int m_healAmount = 25;
        [SerializeField] private int m_damageAmount = 10;
        [SerializeField] private int m_staminaCost = 15;

        private void Start()
        {
            m_playerStats?.ResetStats();
        }

        public void OnHealClicked()
        {
            if (m_playerStats == null) return;

            if (m_playerStats.CurrentStamina >= m_staminaCost)
            {
                m_playerStats.CurrentHealth += m_healAmount;
                m_playerStats.CurrentStamina -= m_staminaCost;
            }
            else
            {
                Debug.Log("Not enough stamina to heal!");
            }
        }

        public void OnDamageClicked()
        {
            if (m_playerStats == null) return;

            m_playerStats.CurrentHealth -= m_damageAmount;

            if (m_playerStats.CurrentHealth <= 0)
            {
                OnPlayerDeath();
            }
        }

        public void OnRestClicked()
        {
            if (m_playerStats == null) return;

            m_playerStats.CurrentStamina = m_playerStats.MaxStamina;
        }

        public void ApplyDamage(int amount)
        {
            if (m_playerStats == null) return;

            m_playerStats.CurrentHealth -= amount;

            if (m_playerStats.CurrentHealth <= 0)
            {
                OnPlayerDeath();
            }
        }

        public void AddGold(int amount)
        {
            if (m_playerStats == null) return;

            m_playerStats.Gold += amount;
        }

        private void OnPlayerDeath()
        {
            Debug.Log("Player has died!");
        }
    }
}
```

#### 4. UXML (UI Layout with Bindings)

```xml
<!-- PlayerStatsPanel.uxml -->
<ui:UXML xmlns:ui="UnityEngine.UIElements" editor-extension-mode="False">
    <Style src="project://database/Assets/UI/Styles/PlayerStats.uss" />

    <ui:VisualElement name="player-stats-panel"
                      class="stats-panel"
                      data-source-type="Game.Models.PlayerStatsModel, Assembly-CSharp">

        <ui:Label name="player-name" class="stats-panel__title" binding-path="PlayerName">
            <Bindings>
                <ui:DataBinding property="text" binding-mode="ToTarget" />
            </Bindings>
        </ui:Label>

        <!-- Health Bar -->
        <ui:VisualElement class="stats-panel__stat-row">
            <ui:Label text="Health" class="stats-panel__label" />
            <ui:ProgressBar name="health-bar"
                            class="stats-panel__progress stats-panel__progress--health"
                            low-value="0"
                            high-value="100"
                            binding-path="HealthPercent">
                <Bindings>
                    <ui:DataBinding property="value" binding-mode="ToTarget" />
                </Bindings>
            </ui:ProgressBar>
            <ui:Label name="health-text" class="stats-panel__value">
                <Bindings>
                    <ui:DataBinding property="text"
                                    data-source-path="CurrentHealth"
                                    binding-mode="ToTarget" />
                </Bindings>
            </ui:Label>
        </ui:VisualElement>

        <!-- Stamina Bar -->
        <ui:VisualElement class="stats-panel__stat-row">
            <ui:Label text="Stamina" class="stats-panel__label" />
            <ui:ProgressBar name="stamina-bar"
                            class="stats-panel__progress stats-panel__progress--stamina"
                            low-value="0"
                            high-value="100"
                            binding-path="StaminaPercent">
                <Bindings>
                    <ui:DataBinding property="value" binding-mode="ToTarget" />
                </Bindings>
            </ui:ProgressBar>
            <ui:Label name="stamina-text" class="stats-panel__value">
                <Bindings>
                    <ui:DataBinding property="text"
                                    data-source-path="CurrentStamina"
                                    binding-mode="ToTarget" />
                </Bindings>
            </ui:Label>
        </ui:VisualElement>

        <!-- Gold Display -->
        <ui:VisualElement class="stats-panel__stat-row">
            <ui:Label text="Gold" class="stats-panel__label" />
            <ui:Label name="gold-value" class="stats-panel__value stats-panel__value--gold">
                <Bindings>
                    <ui:DataBinding property="text"
                                    data-source-path="Gold"
                                    binding-mode="ToTarget" />
                </Bindings>
            </ui:Label>
        </ui:VisualElement>

        <!-- Action Buttons -->
        <ui:VisualElement class="stats-panel__buttons">
            <ui:Button name="heal-button" text="Heal" class="stats-panel__button" />
            <ui:Button name="damage-button" text="Take Damage" class="stats-panel__button" />
            <ui:Button name="rest-button" text="Rest" class="stats-panel__button" />
        </ui:VisualElement>

    </ui:VisualElement>
</ui:UXML>
```

#### 5. USS (Styling)

```css
/* PlayerStats.uss */
.stats-panel {
    padding: 16px;
    background-color: rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    min-width: 300px;
}

.stats-panel__title {
    font-size: 24px;
    -unity-font-style: bold;
    color: rgb(255, 255, 255);
    margin-bottom: 16px;
    -unity-text-align: middle-center;
}

.stats-panel__stat-row {
    flex-direction: row;
    align-items: center;
    margin-bottom: 8px;
}

.stats-panel__label {
    width: 80px;
    color: rgb(200, 200, 200);
    font-size: 14px;
}

.stats-panel__progress {
    flex-grow: 1;
    height: 20px;
    margin: 0 8px;
}

.stats-panel__progress--health .unity-progress-bar__progress {
    background-color: rgb(200, 50, 50);
}

.stats-panel__progress--stamina .unity-progress-bar__progress {
    background-color: rgb(50, 150, 50);
}

.stats-panel__value {
    width: 50px;
    color: rgb(255, 255, 255);
    -unity-text-align: middle-right;
}

.stats-panel__value--gold {
    color: rgb(255, 215, 0);
    -unity-font-style: bold;
}

.stats-panel__buttons {
    flex-direction: row;
    justify-content: space-around;
    margin-top: 16px;
}

.stats-panel__button {
    padding: 8px 16px;
    background-color: rgb(60, 60, 60);
    border-radius: 4px;
    color: rgb(255, 255, 255);
}

.stats-panel__button:hover {
    background-color: rgb(80, 80, 80);
}
```

### Key Points

1. **Model implements `INotifyBindablePropertyChanged`** — required for automatic UI updates when data changes at runtime
2. **Use `[CreateProperty]` on all bound properties** — makes properties visible to the binding system
3. **Call `Notify()` in property setters** — triggers UI updates when values change
4. **Set `dataSource` in the View** — connects the Model to UXML bindings
5. **View forwards user input to Presenter** — maintains separation of concerns
6. **Presenter modifies Model only** — UI updates automatically via bindings

---

## Performance Tips

1. **Cache VisualElement references** in `OnEnable` — never call `Q<>()` in `Update`; `OnEnable` is preferred over `Awake` so queries and subscriptions are in the same method
2. **Use USS classes** for style changes, not inline `element.style.*` assignments — USS is batched and optimized
3. **Use `ListView`** for any list with more than ~20 items — virtualized rendering avoids per-frame work for off-screen items
4. **Avoid `Query<>().ToList()`** in per-frame or frequent code — it allocates garbage
5. **Use USS variables** for colours and sizes — reduces redundancy and simplifies theming
6. **Minimise UXML nesting** — each level adds traversal cost
7. **Avoid toggling `display: none` every frame** — use `visibility: hidden` if the element must remain in layout
8. **Use `EventRegistry`** for bulk cleanup — avoids manual subscribe/unsubscribe bookkeeping

---

## Quick Reference: Common Mistakes

| ❌ Wrong | ✅ Correct | Notes |
|----------|-----------|-------|
| `color: #FF0000;` | `color: rgb(255, 0, 0);` | USS doesn't support hex |
| `text-align: center;` | `-unity-text-align: middle-center;` | Unity prefix required |
| `font-weight: bold;` | `-unity-font-style: bold;` | Different property |
| `background: url(...)` | `background-image: url(...)` | No shorthand |
| `element.visible = false` | `element.style.display = DisplayStyle.None` | Use style property |
| `binding-path="health"` | `binding-path="Health"` | Case-sensitive |
| `button.onClick += ...` | `button.clicked += ...` | Use `clicked` |
| `button.enabled = false` | `button.SetEnabled(false)` | Use the method |
| Missing `[CreateProperty]` | Add `[CreateProperty]` attribute | Required for binding |
| Missing `INotifyBindablePropertyChanged` | Implement the interface | Required for reactive updates |
| `root.Q("name")` | `root.Q<VisualElement>("name")` | Always include type |
| Querying + subscribing in `Awake` | Query and subscribe in `OnEnable` | Keeps lifecycle consistent; OnEnable pairs with OnDisable for cleanup |
| Not unsubscribing events | Unsubscribe in `OnDisable` | Memory leaks |
| `element.Add(template)` | `element.Add(template.Instantiate())` | Must call `Instantiate()` |
| `navBarMenu` | `navbar-menu` | Use kebab-case |
| `navbar-item` | `navbar-menu__item` | Use BEM with `__` |
| `display: grid` | flexbox only | No CSS grid in USS |
| `calc(50% - 10px)` | Hardcode or use `flex-grow` | No `calc()` in USS |
| `UxmlFactory`/`UxmlTraits` | `[UxmlElement]` / `[UxmlAttribute]` | Deprecated in Unity 6 |
| `OnDestroy` for runtime MonoBehaviour | `OnDisable` | `OnDestroy` fires too late |
| `SerializedObject.Bind()` for runtime | `binding-path` + `dataSource` | Editor API only |

---

## Troubleshooting

### Binding Not Updating

1. ✅ Property has `[CreateProperty]`
2. ✅ Class implements `INotifyBindablePropertyChanged`
3. ✅ `Notify()` is called when the property changes
4. ✅ `dataSource` is assigned in C#
5. ✅ `binding-path` matches the property name exactly (case-sensitive)

### Element Not Visible

1. Check `display` is not `None`
2. Check `visibility` is not `Hidden`
3. Check parent has `flex-grow: 1` or explicit size
4. Open the **UI Toolkit Debugger** (Window → UI Toolkit → Debugger)

### Button Not Responding

1. Verify subscription is in `OnEnable` (not constructor)
2. Check not disabled (`button.SetEnabled(false)`)
3. Check no overlay element blocking pointer events
4. Check `picking-mode` is `position` (not `ignore`)

### Query Returns Null

1. Verify `name` attribute is set in UXML
2. Query in `OnEnable`, not `Awake` (for UIDocument)
3. Use the correct type (`Q<Button>` not `Q<VisualElement>`)
4. Check for typos — name matching is case-sensitive

### Template Not Rendering

1. `VisualTreeAsset` is assigned in the Inspector
2. Call `Instantiate()` before adding to the hierarchy
3. Check the Console for UXML parse errors

### ListView Not Showing

1. `itemsSource` is set
2. `makeItem` and `bindItem` are both assigned
3. Call `RefreshItems()` after data changes

### USS Not Applied

1. USS file is referenced in UXML: `<Style src="..." />`
2. Class names match exactly (case-sensitive)
3. Inspect with the UI Toolkit Debugger to verify computed styles

---

## Additional Resources

- **UI Builder:** Window → UI Toolkit → UI Builder
- **Samples:** Window → UI Toolkit → Samples
- **Debugger:** Window → UI Toolkit → Debugger
- **Official Documentation:** https://docs.unity3d.com/6000.3/Documentation/Manual/UIElements.html

Fetch the official documentation on demand when a question involves an API or behaviour not covered in this file. This reference targets **Unity 6.3.4f1** — do not consult or generate code for older Unity versions.
