> How it works: give the URL of [InstallPackages.md](InstallPackages.md) to your agent and it will
> audit which packages your project has, recommend only the missing ones it needs, and install the
> ones you pick and confirm.

# Package installer

Unity packages add capabilities such as camera control, input, or testing. This folder holds an agent
guide that reviews your project's packages and installs only the ones you choose. It recommends from
evidence in your project, so a project that has no tests is not told to install a test framework.

| I want to… | Give your agent |
|---|---|
| Review my packages and install the missing ones I need | [InstallPackages.md](InstallPackages.md) |

Example prompts:

- *"Check which of these packages my Unity project is missing and install the ones I pick."*
- *"Install Cinemachine and the test framework if my project needs them."*
- *"Does my project use any package it has not installed?"* The agent audits and stops with
  recommendations.

## What happens when you hand it over

1. **Audit.** The agent reads `manifest.json`, the lockfile, and your code. It does not open the
   project in an Editor.
2. **Recommendations.** Each missing package gets the evidence for it, a risk, and a default.
3. **You pick.** Any subset, "all recommended", or none.
4. **You confirm.** The agent restates the package ids and how each is versioned, and waits for an
   explicit yes.
5. **It installs and verifies.** Through the Package Manager API, then checks the lockfile.

## Why versions work differently per package

Some packages ship inside the Unity Editor. Unity calls them
[core packages](https://docs.unity3d.com/Manual/pack-core.html), and their version is fixed to your
Editor version, so you cannot pick one. Other packages come from the registry, where the agent uses
Unity's recommended version, or the latest compatible release when none is recommended. Which packages
are core depends on your Editor version, so the agent checks your project instead of assuming. For
example, Cinemachine is a core package from Unity 6.6, and a Cinemachine 2 project moves to
Cinemachine 3, which has a different API.

## What it will not do

- Remove, downgrade, or replace a package.
- Edit `manifest.json` by hand unless you explicitly ask.
- Change settings a package adds, such as Active Input Handling.

## Customize

The package list is an example and the part most likely to differ per project. Add rows for the
packages you always want, each with the code or asset signal that shows a project needs it.
