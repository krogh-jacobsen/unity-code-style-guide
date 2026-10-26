> How it works: give this URL to your agent, for example "Implement the mobile build settings from
> this document in my Unity project". The agent audits the project first, asks about your target
> devices and stores, recommends changes, lets you pick which to carry over, and changes nothing
> until you confirm. It then applies the confirmed settings and reports what it verified. Human
> overview: [readme](README.md).

# Android and iOS mobile build setup (agent instructions)

Configure the Android and iOS players of a URP project on Unity 6.7+. This document is
self-contained. Its values are starting choices: keep a setting that already works unless the user
selects the change, and treat every budget as a proposal until measured on a physical device.
**Last verified: October 2026.** Store rules change yearly, so re-check the linked Google Play and
Apple pages before a release.

## Operating rules

- Change settings through Editor APIs or Unity CLI (`PlayerSettings`, `QualitySettings`,
  `EditorUserBuildSettings`, Build Profile assets). Leave ProjectSettings YAML and `.meta` files
  untouched; hand edits corrupt asset identity.
- Continue read-only auditing on a dirty tree while preserving existing edits and unsaved scenes.
  Before confirmed changes, establish an attributable before/after baseline or an isolated checkout.
  Ask before execution only when existing work conflicts with it; a dirty tree alone does not gate the audit.
- Preserve unsaved scenes and the user's other edits.
- Without CLI/bridge access, inspect saved files read-only and mark unavailable live checks Not verified.
  After confirmation, use the Editor's Player Settings, Quality, and Build Profiles windows and
  importer Inspectors as the manual route; install no bridge merely to complete this guide.
- Keep signing material out of the project and out of the report: keystores, passwords, and
  provisioning profiles stay in the user's secure storage. Ask the user to supply them at build time.
- Confirm each API signature against the installed Editor version before calling it; the names
  below are the Unity 6 shape and move between releases.
- Record a check as **Not verified** when its module, host OS, or physical device is missing.
  Simulators and emulators do not establish performance, thermals, or driver behavior.

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

- Editor version (`ProjectSettings/ProjectVersion.txt`) and installed Android and iOS build modules.
- Render pipeline and the URP asset assigned to every quality level; installed Input System package.
- Current values of every row in step 3, plus existing Build Profiles and scripting define symbols.
- Host OS and toolchains. Android needs the SDK, NDK, and JDK that Unity Hub installs with the
  module. iOS builds need a Mac with Xcode: the Unity build produces an Xcode project, and
  Xcode compiles, signs, and archives it.

**Done:** the table exists, every step 3 row has a known value, an observed "not set", or Not verified with a reason,
and nothing was changed.

## 2. Ask the target contract

Ask all questions in one batch; the project cannot answer them. When the user says "use defaults",
the default becomes a recommended answer that still goes through stages 2 to 4.

| Question | Default |
|---|---|
| Which platforms ship? | Android and iOS |
| Store or distribution channel? | Google Play (App Bundle) and the App Store |
| Minimum Android API level and minimum iOS version? | No default; propose the Editor's current minimum and ask |
| Representative low-end device per platform? | No default; record "unspecified" and mark device checks Not verified |
| Orientation? | Keep the project's current setting; ask only when none is set |
| Frame-rate target? | 30 fps for a low tier, 60 fps for mid and high tiers |
| Need 32-bit Android (ARMv7)? | No: ARM64 only |
| Which permissions does the game use (camera, microphone, location, notifications)? | None; every unused permission stays out of the manifest and Info.plist |
| iOS build method: Replace or Append the Xcode project? | Replace for clean CI; Append when the user hand-edits the Xcode project |
| Run builds now? | Yes when toolchains and modules exist; otherwise configure only |

**Done:** every question has an answer or a stated default, repeated back to the user, one line each.

## 3. Apply the settings

Only the items confirmed in stage 4. Go row by row. When a row's current value already matches its
target, record **Already correct**; a row the user did not pick is **Skipped** and stays a proposal.

### Shared

| Setting | Target | Set via | Condition |
|---|---|---|---|
| Company and Product name, bundle identifier | Final values, set before any shipping build | `PlayerSettings.companyName`, `productName`, `SetApplicationIdentifier` | A later change breaks store identity and moves `persistentDataPath` |
| Version and build number | Set both; the build number increases with every store upload | `PlayerSettings.bundleVersion`, `Android.bundleVersionCode`, `iOS.buildNumber` | |
| Color space | Linear | `PlayerSettings.colorSpace` | Gamma only when the minimum device list requires it |
| Scripting backend | IL2CPP | `PlayerSettings.SetScriptingBackend(NamedBuildTarget.Android / .iOS, …)` | |
| Managed stripping | Minimal while iterating; raise one level at a time for release | `PlayerSettings.SetManagedStrippingLevel` | Only after reflection, serialization, and dynamic-content tests pass on the release player |
| Frame rate | `Application.targetFrameRate` = the user's target, set at startup; `QualitySettings.vSyncCount` = 0 | Code plus `QualitySettings` | Android and iOS ignore positive `vSyncCount` values and use `targetFrameRate`; setting vSync to 0 is not a prerequisite on these platforms. Test pacing and refresh-rate changes on devices |
| Incremental GC | On | `PlayerSettings.gcIncremental` | |
| Input | Input System package with touch support | Package Manager and Player Settings | |
| Safe area | Read `Screen.safeArea` and anchor HUD inside it | Code | Notches and rounded corners cut content on both platforms |

### Android

| Setting | Target | Set via | Condition |
|---|---|---|---|
| App icons | Adaptive icons only | Android Player Settings > Icons | Unity 6.6 removed Legacy and Round icon support |
| Target architectures | ARM64 only | `PlayerSettings.Android.targetArchitectures` | ARMv7 only when selected; Google Play requires 64-bit support alongside it |
| Target API level | At least API 36 (Android 16) | `PlayerSettings.Android.targetSdkVersion` | New apps and updates on Google Play need it from 31 August 2026 (extensions to 1 November 2026 exist). Existing apps need at least API 35. [Check the requirement](https://developer.android.com/google/play/requirements/target-sdk) before release |
| Minimum API level | The user's answer | `PlayerSettings.Android.minSdkVersion` | Never below the Editor's supported floor |
| Release output | Android App Bundle (`.aab`) | `EditorUserBuildSettings.buildAppBundle` = true | Google Play requires it; use `.apk` for development and side-loading |
| Graphics APIs | Vulkan first, OpenGL ES 3.1 as fallback | `PlayerSettings.SetGraphicsAPIs(BuildTarget.Android, …)` | Unity 6.6 raised the minimum OpenGL ES version from 3.0 to 3.1 (upgrade guide). Test both on the low-end device. Use Vulkan device filter lists when a driver misbehaves |
| Optimized Frame Pacing | On | `PlayerSettings.Android.optimizedFramePacing` | With it on, Unity can clamp `targetFrameRate` to a divisor of the refresh rate (for example 25 → 20 on 60 Hz); pick targets that divide 60 |
| Texture compression | ASTC | Player Settings Android texture compression | ETC2 only when the minimum device lacks ASTC |
| Application entry point | Keep the project's current entry; ship a single entry in store builds | Android Player Settings | |
| 16 KB page size | Every native library aligned for 16 KB pages | Unity 6 supports it; inspect the built bundle (APK Analyzer) | Play rejects apps targeting Android 15+ that fail it. If a rejection persists on a supported Editor, update the `com.unity.appbundle` package (it updates bundletool) |
| Signing | Release keystore from the user's secure storage; Play App Signing for the upload key | `PlayerSettings.Android.useCustomKeystore` and keystore fields, supplied at build time | |

### iOS

| Setting | Target | Set via | Condition |
|---|---|---|---|
| Architecture | ARM64 | Player Settings (Unity iOS builds are ARM64) | |
| Minimum iOS version | The user's answer | `PlayerSettings.iOS.targetOSVersionString` | Never below the Editor's supported floor |
| Target SDK | Device SDK for release; Simulator SDK only for simulator runs | `PlayerSettings.iOS.sdkVersion` | |
| Graphics API | Metal (leave Auto Graphics API on) | `PlayerSettings.SetUseDefaultGraphicsAPIs` | |
| Xcode and SDK | Build with Xcode 26 and the iOS 26 SDK or newer | Mac host | App Store Connect has required it for uploads since 28 April 2026; [check Apple's requirements](https://developer.apple.com/news/upcoming-requirements/) |
| Privacy manifest | `PrivacyInfo.xcprivacy` declaring required-reason APIs; every third-party SDK ships its own | Xcode project / Unity privacy manifest policy | Missing declarations get uploads rejected. [Unity's policy](https://docs.unity3d.com/Manual/apple-privacy-manifest-policy.html) |
| Usage descriptions | A purpose string for each permission the game actually uses (step 2) | `PlayerSettings.iOS.cameraUsageDescription`, `microphoneUsageDescription`, `locationUsageDescription` | Leave unused strings empty |
| Signing | Apple Developer Team ID set; automatic signing for development, explicit provisioning for release | `PlayerSettings.iOS.appleDeveloperTeamID`, `appleEnableAutomaticSigning` | Certificates and profiles stay in the user's keychain |
| Output | Xcode project under `Builds/iOS/`, outside `Assets` | Build Profile / `BuildPlayerOptions` | Use the build method chosen in step 2 |

### Quality tiers and budgets (proposals)

Create Low, Mid, and High tiers, each with its own URP asset. Assign the tier from device
capability at startup, and give each tier a frame and memory budget. Start from these URP choices
and let GPU timing on the low-end device decide:

- HDR off and MSAA 0 or 2 on Low; shadows off or a single low-resolution cascade; at most a few
  additional lights; render scale below 1 on Low if the budget requires it.
- Post-processing minimal; leave the depth texture and opaque texture off unless a feature needs
  them; keep SRP Batcher on.
- Measure on the device, not the Editor: the Editor's GPU and driver differ from the phone's.

Texture and audio budgets apply through `TextureImporter` platform settings on owned assets only,
after previewing the paths. Keep color textures sRGB and data textures linear.

| Role | Starting budget | Inspect before accepting |
|---|---|---|
| World albedo | Max 1024 (2048 for hero assets); ASTC 6x6 | Compare on the device at gameplay distance |
| Normal maps | Max 1024; ASTC 5x5 or 4x4 | Shading artifacts on the low-end device |
| Packed masks | Max 512–1024; ASTC 6x6 | Required channels, metallic/smoothness artifacts |
| Screen-space UI | Match displayed size; ASTC 4x4 or RGBA32 for gradients | Edges at the device's density; keep slicing and atlas identity |

Mipmaps stay on for world textures. Audio: music and long ambience stream; short SFX decompress on
load; force mono for positional effects; keep sample rate content-driven; total installed size
stays inside the store's limits for the selected distribution.

### Thermals and battery

Sustained workloads can trigger thermal throttling depending on device, rendering cost, and ambient
conditions. Measure a soak run before choosing a 30 or 60 fps tier; consider the Adaptive Performance
package when measured behavior calls for runtime quality scaling. Its
automatic and manual performance modes work on Android providers; iOS controls CPU and GPU levels
itself. Test with a soak run (see step 5).

**Done:** the audit and numbered recommendations were shown and the user's explicit confirmation was received
before any change; every row has a status (Applied, Already correct, or Skipped with reason), and
re-reading the settings through the Editor API returns the target values.

## 4. Build profiles and CLI

Only the items confirmed in stage 4. Create Development and Release profiles only for the selected
platforms (Android and/or iOS) through the Editor or CLI. Unselected platforms need no profiles or hosts. Not every setting is isolated per profile in every Editor version, so inspect shared
Player Settings after saving.

| Choice | Development | Release |
|---|---|---|
| Development Build | On | Off |
| Script debugging / profiler | On only when needed; Deep Profiling off | Off |
| Output (Android) | `.apk`, `Builds/Android-Dev/` | `.aab`, `Builds/Android-Release/` |
| Output (iOS) | Xcode project, Debug configuration | Xcode project, archived in Release configuration |

Build from the CLI, one target per invocation (`-projectPath` and `-quit` are required;
`-batchmode` and `-logFile` are recommended):

```
Unity -batchmode -quit -projectPath <abs path> -activeBuildProfile <profile asset> -build <output path> -logFile <log>
```

Use `-buildTarget Android` or `iOS` when no profile asset exists, or `-executeMethod` for a custom
build script. Prefer the installed `unity` CLI when present and read its help for exact flags. An
iOS build only produces the Xcode project; archive and sign it with `xcodebuild` or Xcode on a Mac.

Preserve debug symbols for crash reporting (Android native symbols, iOS dSYMs).

**Done:** each selected release output builds on a suitable host (`.aab` on any supported host; the iOS Xcode
project archives on a Mac), or each missing host is marked Not verified.

## 5. Verify

Run the project's tests and read fresh results. On each selected platform, install the **release**
build on a physical low-end device and check:

- cold start time, then pause/resume, a phone call or notification interruption, and a screen lock
- orientation changes, safe-area layout on a notched device, and touch input at screen edges
- scene transitions, save/load, and quit and relaunch
- audio on first playback, with the silent switch (iOS) and with headphones plugged in and removed
- a 15–30 minute soak run on the Low tier showing stable frame time and no thermal throttling
- peak memory on the device (Memory Profiler) and install size against the store limit
- every permission prompt fires once, with the right description, only for permissions in use
- logs (`adb logcat` on Android, Xcode console on iOS) show no missing shaders, assets, or libraries

Android additionally: inspect the `.aab` for 16 KB alignment, and install through an internal test
track or `bundletool` rather than the Editor. iOS additionally: archive in Xcode, read the privacy
report, and validate the archive with App Store Connect (TestFlight).

**Done:** each check is Passed, Failed, or Not verified, with device model, OS version, graphics
API, and quality tier recorded beside every measurement.

## 6. Report

End with this table and a `git diff --stat ProjectSettings` summary:

| Item | Status | Detail |
|---|---|---|
| Each step 3 row | Applied / Already correct / Skipped | Old value → new value |
| Each unpicked recommendation | Proposal | Finding, proposed change, and risk |
| Each step 5 check | Passed / Failed / Not verified | Evidence, or the missing device, toolchain, or account |

Put unanswered target-contract items, store-requirement deadlines, unpicked recommendations that
need a decision, and failed checks in a separate block labelled "Needs your decision" at the top of
the report.

## References

- [Android Player settings](https://docs.unity3d.com/Manual/class-PlayerSettingsAndroid.html)
- [iOS Player settings](https://docs.unity3d.com/Manual/class-PlayerSettingsiOS.html)
- [Google Play target API requirement](https://developer.android.com/google/play/requirements/target-sdk)
- [Unity on Android: 16 KB page size](https://developer.android.com/games/develop/build-in-unity)
- [Apple SDK minimum requirements](https://developer.apple.com/news/upcoming-requirements/)
- [Apple privacy manifest policy in Unity](https://docs.unity3d.com/Manual/apple-privacy-manifest-policy.html)
- [Application.targetFrameRate](https://docs.unity3d.com/ScriptReference/Application-targetFrameRate.html)
- [Adaptive Performance](https://docs.unity3d.com/Manual/adaptive-performance/introduction.html)
- [Build profiles](https://docs.unity3d.com/Manual/build-profiles.html)
- [Build from the command line](https://docs.unity3d.com/Manual/build-command-line.html)

Links are unversioned and resolve to the current docs; use version-matched docs for the installed Editor.
