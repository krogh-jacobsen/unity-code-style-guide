# Optional CoreCLR migration reference

**Checked: 2026-10-12.** Load for an actual runtime migration, not normal starter setup. The selected
starter remains on the engine/language profile in [UnityTechStack.md](UnityTechStack.md).

## Current evidence versus roadmap

Unity's [October 2026 update](https://discussions.unity.com/t/coreclr-scripting-and-net-update-october-2026/1738338)
announces a Unity 7.0 Alpha CoreCLR Editor initially targeting C# 9 and .NET Standard 2.1. Full .NET 10
and C# 14 remain a staged target with no committed public date. Unity 6.7 experimental players are
separate compatibility options. Do not turn an earlier 6.8 forecast into a baseline guarantee.

The [official upgrade guide](https://discussions.unity.com/t/path-to-coreclr-2026-upgrade-guide/1714279)
is a living source; compare it with the exact chosen Editor's assemblies and documentation before
writing migration code. Availability of an API in a roadmap does not establish player/platform support.

## CLI-first migration checks

**Prerequisite:** isolated copy/branch, exact migration Editor, platform/backend, dependencies, and
baseline results are known. Use `unity-cli` for compilation, repeated Play, tests, and builds; use
CLI-invoked Package Manager Client operations to resolve selected packages.

- Inventory mutable statics/events, retained assembly references, source-asset runtime writes, and
  owned threads/native resources. Prove reset and teardown across Play and code reload.
- Verify dependency framework targets and platform/AOT restrictions. Replace unsupported APIs with
  a format/ownership migration; a JSON rename alone is not a safe old-save migration.
- Inspect installed lifecycle APIs before choosing attributes. The official guide demonstrates
  `Unity.Scripting.LifecycleManagement.AfterCodeReloadSerialization` and discusses `AutoStaticsCleanup`
  and `BeforeCodeUnloading`; these are not blanket instructions to annotate every static class.
- Compile any new attribute with the required namespace and the exact supported Editor/version gate.
  Do not invent `UNITY_6_8_OR_NEWER`; Unity engine defines follow actual version numbering. Prefer
  evidence of supported APIs over a guessed define.
- Re-run supported save fixtures, async/resource teardown, Editor tools, and normal-player tests.

Manual fallback: the selected Editor, Package Manager, Test Runner, and build settings. **Done:**
real API availability is established; owned state resets; dependencies, persisted data, and selected
platform builds work. Record incompatible/unverified components and measured results. Keep experimental
migration results separate from the starter's tested baseline; do not promise performance gains.
