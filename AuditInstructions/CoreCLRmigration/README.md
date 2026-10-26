> How it works: give the URL of [CoreCLRUpgrade.md](CoreCLRUpgrade.md) to your agent and it will
> audit your project for CoreCLR risks, ask which Editor and platforms you are targeting, recommend
> fixes, and apply only the ones you pick and confirm. It then reports what works, what is
> incompatible, and what it could not verify.

# CoreCLR migration

CoreCLR is coming, and this folder helps you get ready. **It is a work in progress:** the runtime,
its Editor, and its player support are all still moving, so expect this guide to change.

| Situation | Give your agent |
|---|---|
| You want to trial your project on a CoreCLR Editor or experimental player | [CoreCLRUpgrade.md](CoreCLRUpgrade.md) |
| You are setting up a normal new project | Not this folder: start from [SetupInstructions](../SetupInstructions/README.md) |

Example prompt: *"Prepare my Unity project for the CoreCLR migration using this document."*

## What to know first

- **It is not the baseline.** The starter stays on its tested engine and language profile. This
  guide covers an experiment on a branch, and its results stay separate from that baseline.
- **Roadmap is not support.** Unity announces a Unity 7.0 Alpha CoreCLR Editor first targeting C# 9
  and .NET Standard 2.1; full .NET 10 and C# 14 have no committed date. An API in a roadmap does not
  mean your platform supports it.
- **The risk is state, not syntax.** Most breakage comes from static state that survives (or fails to
  reset across) code reload, retained assembly references, runtime writes to source assets, and
  threads or native resources with no clear owner.
- **Dependencies decide the timeline.** A package or `.dll` that targets an unsupported framework, or
  needs an unsupported platform API, blocks you however clean your own code is.
- **Old saves need a real migration.** Swapping a serializer is not safe on its own: keep a saved
  fixture and prove it still loads.

## What happens when you hand it over

1. **Audit.** The agent reads your project and reports its CoreCLR risks. It writes nothing.
2. **Recommendations.** Each fixable finding becomes a numbered recommendation with its risk and a
   default of skip, so the default outcome is a report only.
3. **You pick any subset**, "all recommended", or none.
4. **You confirm** the exact change list before anything changes.
5. **It applies and verifies** only what you confirmed, then reports applied items and the proposals
   you skipped.

## What the agent will ask you

- The exact migration Editor, and the platforms and backends you need tested.
- Whether a branch is ready, which dependencies are third-party, and which saved-data fixtures exist.

## Adjacent topics

This folder does not cover the Mono-era reload policy for normal projects: see
[ProjectSettings](../ProjectSettings/README.md) for domain reload and static-state handling, which
this guide builds on. Platform build setup lives in [BuildSettings](../BuildSettings/README.md).
