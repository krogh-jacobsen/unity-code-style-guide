# Set up script templates

Agent entry point for installing selected starter templates from a URL or local checkout into an
existing Unity project. Use available tools; add no setup package or permanent installer. This run
installs template text assets, not gameplay scripts or a replacement project configuration.

## 1. Read the guides and select templates

Read the target's instructions, the [template policy](../ScriptTemplates.md), and the
[shared installation protocol](../InstallResources.md) before copying. Resolve source files and guides
against the supplied URL/local checkout and use one source revision as the shared protocol requires.

Use the default and optional tables in the template policy as the selection/prerequisite authority.
For a request for starter defaults, select its compatible default set. Preserve a target's different
UI/async/assembly choices; ask only about unresolved compatibility, optional selections, or conflicts.
Install individual optional templates only after checking their stated package/assembly prerequisites.
Defer unavailable options rather than installing dependencies implicitly.

Retired `ReferenceOnly` content is outside the selectable set. Documentation and the optional source
directory are not install groups. Keep the source menu filenames, priorities, and Unity substitution
tokens intact; installing a template does not expand `#SCRIPTNAME#` or namespace tokens.

**Done:** the compatible template list and any deferred prerequisites are explicit.

## 2. Install selected pairs

Follow the shared protocol for source staging, license, GUID checks, conflict handling, copying,
and import. Map every selected `.cs.txt` file and its matching metadata directly into
`Assets/ScriptTemplates/`, including selected optional files. Do not nest the source optional directory
there or modify the Editor installation's built-in templates.

Keep existing customized template files and identities unless an update is explicitly selected.
After a successful install, a repeated comparison must report Already installed without rewriting
destination metadata. Package installation, asmdefs, generated scripts, and project-wide namespace
changes remain outside installation scope.

**Done:** selected template pairs and license are installed or unchanged, with copy/import results recorded.

## 3. Verify Create-menu readiness

Follow the template policy's refresh requirement: restart the target Editor safely to refresh the
Create menu, preserving unsaved work. Prefer already available Unity CLI access; otherwise the user
can restart through the Editor/Hub. Inspect the selected menu entries and fresh import/compiler logs.
An unchanged rerun needs no extra restart if menu readiness was already observed for those files.

If restart or menu inspection cannot be completed, report those checks as Not verified and provide
the next action. File presence alone does not establish menu readiness. A template is a text asset;
successful import does not establish that its generated C# compiles.

**Done:** each selected menu entry is observed, or menu readiness is explicitly pending.

## 4. Separate generation validation from installation

When template generation/compilation validation is selected, follow the template policy's validation
section using Unity's actual substitutions under both empty and populated root namespaces. Use a
disposable project or agreed temporary fixture; preserve the target's namespace/settings and dirty
scenes. Follow the target style policy before authoring owned C#.

Place generated Editor code in Editor-only assemblies/folders and tests in configured test assemblies.
Keep optional package dependencies scoped to selected templates. Remove temporary imported fixtures
through Editor APIs, preserving pre-existing assets and metadata. Verify selected runtime dependencies
when exercising generated behavior; ignored test placeholders and unregistered drawers remain unfinished.
If the required packages, assemblies, or fixture are unavailable, report generation/behavior checks as
Not verified rather than expanding installation scope.

Report source revision, chosen/deferred templates, installed paths, identity/conflict results, and
license location. Give separate results for file copy, Unity import, Create-menu readiness, generated
C# compilation, and exercised runtime/Editor behavior. Include the next action for every pending check.

**Done:** installation and observed readiness are reported separately from any unperformed generation
or behavior validation; no permanent generated sample or installer is left behind by this workflow.
