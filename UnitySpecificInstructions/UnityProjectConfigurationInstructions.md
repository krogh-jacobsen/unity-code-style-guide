---
description: Unity Editor and project configuration for optimal workflow
applyTo: "**/*.cs"
---

# Unity Project Configuration

This document covers Unity Editor settings and project configuration optimized for faster iteration and consistent asset imports.

## Table of Contents

- [Enter Play Mode Options](#enter-play-mode-options)
- [Asset Pipeline Settings](#asset-pipeline-settings)
- [Burst Compiler Settings](#burst-compiler-settings)
- [Presets](#presets)
- [Rendering Configuration](#rendering-configuration)
- [Build Settings](#build-settings)

---

## Enter Play Mode Options

**Location:** Edit → Project Settings → Editor

| Setting | Value | Why |
|---------|-------|-----|
| Enter Play Mode Options | ✅ Enabled | Allows customizing what reloads on play |
| Reload Domain | ❌ Disabled | Skips C# domain reload, saves 2-5 seconds per play |
| Reload Scene | ❌ Disabled | Keeps scene state, faster iteration |

### Caveats When Domain Reload is Disabled

With domain reload disabled, **static fields persist between play sessions**:

```csharp
// This value WON'T reset when you stop and start play mode
private static int s_playerCount = 0;

// Fix: Reset in RuntimeInitializeOnLoadMethod
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
private static void ResetStatics()
{
    s_playerCount = 0;
}
```

**Also affected:**
- Static events (subscribers accumulate across plays)
- Singleton instances
- Static collections and caches

See [Unity Documentation: Domain Reloading](https://docs.unity3d.com/Manual/DomainReloading.html) for details.

---

## Asset Pipeline Settings

**Location:** Unity → Settings (macOS) or Edit → Preferences (Windows)

| Setting | Value | Why |
|---------|-------|-----|
| Auto Refresh | ❌ Disabled | Manual control over when assets reimport |

**Manual refresh:** Press `Cmd+R` (macOS) or `Ctrl+R` (Windows) to refresh assets.

**Benefits:**
- No unexpected pauses during work
- Control when large imports happen
- Faster switching between IDE and Unity

---

## Burst Compiler Settings

**Location:** Edit → Project Settings → Burst AOT Settings

| Setting | Value | Why |
|---------|-------|-----|
| Enable Burst Compilation | ✅ Enabled | Significant performance gains for Jobs |
| Synchronous Compilation | ✅ Enabled | Compiles Burst jobs immediately, avoids first-frame stutters |

---

## Presets

Presets standardize import settings for assets. Located at `Assets/Settings/Presets/`.

### Texture Import Presets

| Preset | Use Case | Key Settings |
|--------|----------|--------------|
| `AlbedoTextureImporter` | Diffuse/color textures | sRGB, compressed |
| `NormalTextureImporter` | Normal maps | Linear, normal map format |
| `SingleSpriteTextureImporter` | Individual UI sprites | Sprite mode single |
| `SpriteAtlasTextureImporter` | Sprite atlas textures | Sprite mode multiple |

### Audio Import Presets

Located at `Assets/Settings/Presets/Audio/`:

| Preset | Use Case | Typical Settings |
|--------|----------|------------------|
| `MusicAudioImporter` | Background music | Streaming, high quality, no compression |
| `AmbienceAudioImporter` | Environmental loops | Compressed in memory, loop-friendly |
| `SFXAudioImporter` | Sound effects | Decompress on load, low latency |
| `UIAudioImporter` | UI feedback sounds | Small files, decompress on load |

### Applying Presets

**Automatic (via Preset Manager):**
1. Edit → Project Settings → Preset Manager
2. Add filter (e.g., folder path or name pattern)
3. Assign preset to filter

**Manual:**
1. Select asset in Project window
2. In Inspector, click preset icon (slider bars) at top right
3. Choose preset from dropdown

### Creating New Presets

1. Configure an asset's import settings as desired
2. Click preset icon → Save Current To...
3. Save to `Assets/Settings/Presets/`

---

## Rendering Configuration

**Location:** `Assets/Settings/Rendering/`

### URP Quality Tiers

Three quality levels for different target hardware:

| Asset | Target | Use Case |
|-------|--------|----------|
| `URP-Performant` | Mobile, low-end | Maximum performance, reduced features |
| `URP-Balanced` | Mid-range, default | Good balance of quality and performance |
| `URP-HighFidelity` | Desktop, high-end | Maximum visual quality |

Each quality tier has a matching Renderer asset (e.g., `URP-Balanced-Renderer`).

### Volume Profiles

| Asset | Purpose |
|-------|---------|
| `DefaultVolumeProfile` | Global post-processing defaults |
| `SampleSceneProfile` | Scene-specific overrides |

### Switching Quality at Runtime

```csharp
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

// Switch to high quality
QualitySettings.SetQualityLevel(2); // Index depends on quality settings order
```

---

## Build Settings

### Platform Modules

Remove unused platform modules to reduce Editor overhead:

**Location:** Unity Hub → Installs → Add Modules

Keep only platforms you're targeting. Common setups:
- **Desktop only:** Windows, macOS, Linux
- **Mobile:** Android, iOS
- **Console:** Platform-specific SDKs

### Build Profiles

Located at `Assets/Settings/Build Profiles/`:

Build profiles store platform-specific build configurations including:
- Target platform
- Development/Release mode
- Scripting backend (Mono/IL2CPP)
- Compression settings

---

## Assembly Definitions

This project currently uses Unity's default assembly compilation (all scripts in one assembly).

For larger projects, consider adding assembly definitions to:
- Reduce recompilation scope
- Enforce code boundaries
- Speed up iteration time

Recommended structure for this project:
```
Assets/
├── _HowToExamples/HowToExamples.asmdef
├── _StartMenu/StartMenu.asmdef
├── _DemoGame/DemoGame.asmdef
└── Scripts/Utilities/Utilities.asmdef
```

---

## Quick Reference

### Keyboard Shortcuts

| Action | macOS | Windows |
|--------|-------|---------|
| Refresh Assets | `Cmd+R` | `Ctrl+R` |
| Enter Play Mode | `Cmd+P` | `Ctrl+P` |
| Pause | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| Step Frame | `Cmd+Alt+P` | `Ctrl+Alt+P` |

### Settings Locations Summary

| Setting | Path |
|---------|------|
| Enter Play Mode | Edit → Project Settings → Editor |
| Auto Refresh | Unity → Settings (Preferences) |
| Burst | Edit → Project Settings → Burst AOT Settings |
| Quality Levels | Edit → Project Settings → Quality |
| Preset Manager | Edit → Project Settings → Preset Manager |
| URP Assets | Assets/Settings/Rendering/ |
| Presets | Assets/Settings/Presets/ |

---

## Version Information

- **Target Unity Version:** Unity 6.3 (6000.3.x)
- **Render Pipeline:** URP 17.3.0
- **Last Updated:** February 2026
