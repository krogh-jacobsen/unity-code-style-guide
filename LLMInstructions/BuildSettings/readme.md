> How it works: give the URL of the guide for your platform to your agent and it will review your
> project's build settings, ask a few questions, and apply the recommended starting choices.

# Build settings

Two agent-ready guides set up the player and build settings of a URP project. Pick the one that
matches where your game ships. They are written for the agent; this page explains the thinking so
you can steer it.

| Ships on | Give your agent |
|---|---|
| Windows and macOS | [DesktopBuilds.md](DesktopBuilds.md) |
| Android and iOS | [MobileBuilds.md](MobileBuilds.md) |

Example prompt: *"Implement the build settings from this document in my Unity project."* The agent
reads your current settings, asks about things it cannot infer, shows what it will change, and
ends with a report of what it applied and what it could not verify.

## What the agent will ask you

Both guides start from a **support contract**: the devices and stores you commit to. The agent
cannot read these from the project, and most other choices follow from them.

- Which platforms and architectures you support, and the oldest OS version.
- A low-end device that must run the game well.
- Your frame-rate target and where you distribute (Steam, direct download, Google Play, App Store).

Answer "use defaults" and the agent proceeds with the guide's starting values.

## The decisions that matter

**Desktop** is forgiving on power and memory, so the hard problems are variety and polish.

- *Graphics API.* Direct3D 11 is the safe Windows baseline; Direct3D 12 pays off only for features
  that need it and must keep D3D11 as a fallback. Metal is the only choice on Mac.
- *Architecture.* Apple Silicon only is the modern Mac default; Intel is deprecated in Unity 6.6.
- *Window and frame pacing.* Borderless fullscreen and vSync on give the fewest surprises.
- *Shader hitches.* First-use shader compilation stutters; the guide warms pipeline states
  during a loading screen.

**Mobile** is constrained by heat, battery, memory, and store rules, so budgets matter more.

- *Frame rate.* 30 fps often beats an unstable 60. Phones throttle after a few minutes, so you
  test with a soak run on a real low-end device.
- *Android.* ARM64, IL2CPP, and an App Bundle are required for Google Play, with a target API level
  that rises every year. The guide marks which values are dated.
- *iOS.* Builds need a Mac with a current Xcode, a privacy manifest, and signing set up. Unity
  produces an Xcode project, and Xcode archives it.
- *Quality tiers.* Low, Mid, and High URP assets keep one project running across very different devices.

## Why the guides look the way they do

- **Starting choices, not laws.** Every value is a proposal until you measure it on a real device.
  The agent keeps settings that already work.
- **Settings change through Unity's own APIs.** The agent never edits project YAML by hand, and it
  leaves a clean `git diff` so you can review everything it touched.
- **Honest reporting.** If a device, toolchain, or module is missing, the check is marked
  *Not verified* rather than assumed to pass.

## Other platforms

These guides do not cover VR, Web, or consoles, but they carry over more than you might expect.

- **VR.** Standalone headsets such as Quest are Android devices: reuse the mobile guide
  (ARM64, IL2CPP, Vulkan, tight thermal and frame budgets) and add the OpenXR plug-in, a fixed
  frame rate matched to the headset, and comfort rules. PC VR reuses the desktop guide, with
  stricter frame-time targets.
- **Web.** WebGL and WebGPU builds share the quality-tier and budget ideas, but download size and
  load time dominate: compression, stripping, and shader variants need their own pass. Use a
  dedicated Unity Web optimization workflow.
- **Console.** Console SDKs are under platform-holder agreements, so setup comes from the
  platform's own documentation. The desktop guide's support contract, quality tiers, shader
  warm-up, and verify-on-hardware approach still apply.
