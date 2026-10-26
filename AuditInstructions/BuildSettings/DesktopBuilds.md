> How it works: give this URL to your agent, for example "Implement the desktop build settings from
> this document in my Unity project". The agent audits the project first, asks about your support
> contract, recommends changes, lets you pick which to carry over, and changes nothing until you
> confirm. It then applies the confirmed settings and reports what it verified. Human overview: [readme](README.md).

# Mac and Windows desktop build setup (agent instructions)

Configure the Windows and macOS standalone players of a URP project on Unity 6.7+. This document is
self-contained. Its values are starting choices: keep a setting that already works unless the user
selects the change, and treat every budget as a proposal until measured on a device.
**Last verified: October 2026** (Unity 6.7 docs era); re-check deprecations and store rules after that.

## Operating rules

- Change settings through Editor APIs or Unity CLI (`PlayerSettings`, `QualitySettings`,
  `EditorUserBuildSettings`, Build Profile assets). Leave ProjectSettings YAML and `.meta` files
  untouched; hand edits corrupt asset identity.
- Start from a clean git tree, so `git diff ProjectSettings` shows exactly what the run changed.
  If the tree is dirty, tell the user and ask before continuing.
- Preserve unsaved scenes and the user's other edits.
- Confirm each API signature against the installed Editor version before calling it; the names
  below are the Unity 6 shape and move between releases.
- Record a check as **Not verified** when its module, host OS, or device is missing. A build that
  succeeds on one platform proves nothing about another.

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
   and obtain explicit user authorization before making them, including saving the report.
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

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

## 1. Preflight

Read (this is the audit), then summarise in one table (setting, current value):

- Editor version (`ProjectSettings/ProjectVersion.txt`) and installed Windows/macOS build modules.
- Render pipeline and the URP asset assigned to every quality level; installed Input System package.
- Current values of every row in step 3, plus existing Build Profiles and scripting define symbols.
- Host OS. macOS builds need a Mac. A Windows IL2CPP build needs Visual Studio with the C++ tools
  component and a Windows SDK at or above the minimum in the
  [Windows requirements](https://docs.unity3d.com/Manual/windows-requirements-and-compatibility.html);
  a Mac IL2CPP build needs Xcode.

**Done:** the table exists, every step 3 row has a current value or "not set", and nothing was changed.

## 2. Ask the support contract

Ask all questions in one batch; the project cannot answer them. When the user says "use defaults",
the default becomes a recommended answer that still goes through stages 2 to 4.

| Question | Default |
|---|---|
| Which targets ship? | Windows x64 and macOS Apple Silicon |
| Support Windows Arm64? | No. It has no Vulkan, only GPU lightmapping, and needs Arm64 builds of every native dependency |
| Support Intel Macs? | No. Unity deprecates Intel Mac from 6.6; Intel or Universal output is possible only on Unity 6.7 LTS or earlier |
| Minimum Windows/macOS release, GPU, CPU, RAM? | No default; record unanswered values as "unspecified" |
| Need D3D12-only features (for example ray tracing)? | No: D3D11 baseline |
| Frame budget? | 60 fps (16.7 ms) on the minimum device |
| Delivery channel (Steam, store, direct download)? | Direct download |
| Run builds now? | Yes when the host and modules exist; otherwise configure only |

**Done:** every question has an answer or a stated default, repeated back to the user, one line each.

## 3. Apply the settings

Only the items confirmed in stage 4. Go row by row. When a row's current value already matches its
target, record **Already correct**; a row the user did not pick is **Skipped** and stays a proposal.

| Setting | Target | Set via | Condition |
|---|---|---|---|
| Company and Product name | Final names, set before any shipping build | `PlayerSettings.companyName`, `productName` | They determine `persistentDataPath` and the Player.log path, so a later rename moves player data |
| Color space | Linear | `PlayerSettings.colorSpace` | |
| Render pipeline | URP asset assigned in every quality level | `QualitySettings.renderPipeline` per level | |
| Windows graphics APIs | D3D11 first; Auto Graphics API off when the order is manual | `PlayerSettings.SetUseDefaultGraphicsAPIs`, `SetGraphicsAPIs` | With D3D12 selected, keep D3D11 in the list: Unity [blocks D3D12 on some devices](https://docs.unity3d.com/Manual/allow-deny-d3d12-usage.html), and a build without a fallback does not launch there |
| Mac graphics API | Metal | same | |
| Mac architecture | Apple Silicon (`OSArchitecture.ARM64`) | `OSXStandalone.UserBuildSettings.architecture` | Intel only when selected in step 2 |
| Windows architecture | x64 | Build Profile or Player Settings architecture field; find the API for the installed Editor | Arm64 only when selected |
| Fullscreen mode | Fullscreen Window (borderless) | `PlayerSettings.fullScreenMode` | Offer Exclusive Fullscreen (Windows only) as a user option, never the default |
| Resizable window | On | `PlayerSettings.resizableWindow` | |
| Run in background | Off for an offline game; on only when online or background simulation requires it | `PlayerSettings.runInBackground` | |
| High DPI | Retina/high-DPI support on, plus a user render-scale option | `PlayerSettings.macRetinaSupport`; Windows per Player Settings | |
| vSync | 1 in every quality level | `QualitySettings.vSyncCount` | `Application.targetFrameRate` is ignored while vSync is above 0. With vSync off, offer a frame limiter; avoid an unlimited default on laptops |
| Scripting backend | Mono for development, IL2CPP for release | `PlayerSettings.SetScriptingBackend(NamedBuildTarget.Standalone, …)` | IL2CPP for both when a dependency requires it. IL2CPP is not faster by default; measure |
| Managed stripping | Minimal in both profiles | `PlayerSettings.SetManagedStrippingLevel` | Raise one level at a time, only after reflection, serialization, and dynamic-content tests pass on the release player |
| Input | Keep the project's active input handling; prefer the Input System package for new projects | Player Settings | |

### Quality tiers

Create Laptop and Desktop tiers (add High only when it serves a distinct device class). Each tier
gets its own URP asset and an explicit budget. Treat shadows, render scale, anti-aliasing,
additional lights, and post-processing as tier choices driven by GPU timing. Keep a renderer
feature that already works; enabling every feature is not a baseline.

### Texture and audio budgets (proposals)

Apply through `TextureImporter` platform settings on owned assets only, after previewing the paths.
The Standalone override is shared by Windows and macOS; split content when their budgets diverge.
Keep color textures sRGB and data textures linear.

| Role | Starting budget | Inspect before accepting |
|---|---|---|
| World albedo | Max 2048; BC7 for quality, BC1 for opaque | Compare at gameplay distance; small props 512–1024 |
| Normal maps | Max 2048; evaluate BC5 | Tangent-space shading and the shader's normal decoding |
| Packed masks | 1024–2048; BC7 when several channels are needed | Required channels, metallic/smoothness artifacts |
| Close-up hero surfaces | 4096 only where a comparison justifies it | Imported memory size and total residency |
| Screen-space UI | Match displayed size; compare BC7 with RGBA32 | Alpha edges at high DPI; keep slicing and atlas identity |

Audio: music and long ambience stream (Vorbis); short SFX decompress on load; keep sample rate
content-driven. Existing platform overrides take precedence and need their own audit.

### Shader and pipeline-state warm-up

First-use shader compilation causes desktop hitches. Use `GraphicsStateCollection` (experimental):
trace pipeline states in a test build, then warm the collection during a loading screen. It covers
D3D12, Vulkan, and Metal, and falls back to shader warm-up elsewhere. Re-trace after content
changes; OS and driver updates invalidate driver caches. See
[PSO tracing and warm-up](https://docs.unity3d.com/Manual/shader-pso-introduction.html).

**Done:** the audit and numbered recommendations were shown and the user's explicit confirmation was received
before any change; every row has a status (Applied, Already correct, or Skipped with reason), and
re-reading the settings through the Editor API returns the target values.

## 4. Build profiles and CLI

Only the items confirmed in stage 4. Create Windows Development, Windows Release, Mac Development, and Mac Release profiles through the
Editor or CLI. Not every setting is isolated per profile in every Editor version, so inspect shared
Player Settings after saving.

| Choice | Development | Release |
|---|---|---|
| Development Build | On | Off |
| Script debugging / profiler | On only when needed; Deep Profiling off | Off |
| Backend | Mono (step 3) | IL2CPP (step 3), exercised in acceptance |
| Output | `Builds/<Platform>-<Profile>/`, outside `Assets` | Same; clean distributable |

Build from the CLI, one target per invocation (`-projectPath` and `-quit` are required;
`-batchmode` and `-logFile` are recommended):

```
Unity -batchmode -quit -projectPath <abs path> -activeBuildProfile <profile asset> -build <output path> -logFile <log>
```

Use `-buildTarget` when no profile asset exists, or `-executeMethod` for a custom build script.
Without either, Unity loads the last-used configuration. Prefer the installed `unity` CLI when
present and read its help for exact flags.

Preserve debug symbols separately. For Mac distribution, plan signing and notarization for the
chosen channel and test the result on another Mac. For Windows, record the code-signing and
packaging requirements of the chosen channel.

**Done:** each selected release profile builds on a suitable host, or its build is marked Not verified
with the missing prerequisite. Unselected platforms are Not applicable.

## 5. Verify

Run the project's tests and read fresh results. In the release player of each selected platform,
check:

- keyboard/mouse input and UI focus; controller input when the game supports controllers
- resize, fullscreen switching, Alt-Tab/Cmd-Tab, and saved display preferences
- Retina/high-DPI and an ordinary display, with UI inspected and GPU frame time noted
- 60 Hz, a high-refresh display, and on Mac a variable-refresh (ProMotion) display
- first audio playback and overlapping voices, scene transitions, save/load, quit and relaunch
- a cold shader cache (clear the driver cache) shows no first-use hitches in each scene
- the minimum quality tier on the minimum hardware, with frame time and memory recorded
- Player.log shows no missing shaders, assets, native libraries, or runtime types

Player.log: Windows `%USERPROFILE%\AppData\LocalLow\<Company>\<Product>\Player.log`; macOS
`~/Library/Logs/<Company>/<Product>/Player.log` ([log files](https://docs.unity3d.com/Manual/LogFiles.html)).

**Done:** each check is Passed, Failed, or Not verified, with resolution, API, refresh rate, and
hardware recorded beside every measurement.

## 6. Report

End with this table and a `git diff --stat ProjectSettings` summary:

| Item | Status | Detail |
|---|---|---|
| Each step 3 row | Applied / Already correct / Skipped | Old value → new value |
| Each unpicked recommendation | Proposal | Finding, proposed change, and risk |
| Each step 5 check | Passed / Failed / Not verified | Evidence, or the missing module, host, or device |

Put unanswered support-contract items, unpicked recommendations that need a decision, and failed
checks in a separate block labelled "Needs your decision" at the top of the report.

## References

- [Windows Player settings](https://docs.unity3d.com/Manual/playersettings-windows.html)
- [Windows requirements and compatibility](https://docs.unity3d.com/Manual/windows-requirements-and-compatibility.html)
- [macOS build settings and architectures](https://docs.unity3d.com/Manual/macosbuildsettings.html)
- [Intel Mac deprecation](https://discussions.unity.com/t/unity-to-deprecate-intel-based-mac-support-starting-with-unity-6-6/1721740)
- [D3D12 device filtering](https://docs.unity3d.com/Manual/allow-deny-d3d12-usage.html)
- [PSO tracing and warm-up](https://docs.unity3d.com/Manual/shader-pso-introduction.html)
- [vSync and frame limiting](https://docs.unity3d.com/ScriptReference/QualitySettings-vSyncCount.html)
- [Build profiles](https://docs.unity3d.com/Manual/build-profiles.html)
- [Build from the command line](https://docs.unity3d.com/Manual/build-command-line.html)
- [Log files](https://docs.unity3d.com/Manual/LogFiles.html)

Links are unversioned and resolve to the current docs; use version-matched docs for the installed Editor.
