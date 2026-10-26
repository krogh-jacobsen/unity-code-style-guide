# Custom Unity CLI script command and tests

This example shows both sides of “custom script”: authoring a C# Editor command that Unity CLI can
discover, and using it to generate a small runtime C# script. Then run focused behavioral tests
through the same CLI. It is deliberately one operation, not a project installer.

## Prerequisites and installation

Use a disposable Unity project with a compatible `com.unity.pipeline` package and Test Framework.
Discover installed CLI help and package compatibility first; see the exact [tested versions](../../../Validation.md).
This optional example's Editor assembly references `Unity.Pipeline`; do not install it into a project
without that package. Cancellation/pooling examples have no Pipeline assembly dependency.

Copy this folder's Editor, Generated, Templates, Tests, asmdefs, and metadata to the exact
`Assets/Examples/CliScriptAndTests/` path. Keep this README outside Assets. Generated initially
contains only its runtime asmdef: the custom command creates `SampleScoreCounter.cs`.
Import and require no compiler errors. Preview path/GUID conflicts before installation.

`ScriptGenerationCommand.cs` registers `starter_generate_score_counter` using `[CliCommand]` and
`[CliArg]`. The command defaults to preview. `ScriptGenerator` validates an Assets-relative .cs
path, rejects traversal/symbolic links and orphan metadata, writes new source only, and imports
through AssetDatabase so Unity creates its metadata. Identical reruns report Unchanged; differing
existing scripts fail for manual review. It preserves existing source and GUIDs and does not edit
Unity YAML. Source creation is not an Undo transaction; remove unwanted imported scripts through
AssetDatabase or the Project window. Generated code uses a fixed sample namespace and filename;
customize the template/command deliberately when adapting it.

## Execute the custom command

Set absolute project and result paths. `unity run --command` launches a one-shot Editor or reuses
the target's running Editor; `unity command` is for an already-connected Editor. Discover the live
catalog rather than assuming other commands exist:

```bash
unity --version
unity status --format json
unity command --project-path /absolute/project
unity run /absolute/project --command starter_generate_score_counter --format json \
  -- --dry_run true
unity run /absolute/project --command starter_generate_score_counter --format json \
  -- --dry_run false
```

Expected: WouldCreate from the first preview, Created from generation, then Unchanged on rerun.
If a live Editor recompiles/disconnects while importing, wait for a ready connection and clean
compilation, then rerun the preview to confirm the saved result. Command success means source was
created/imported; the following tests establish its behavior after compilation.

## Run tests and read results

Run the generator safety tests before generation if desired. The complete namespace filter below
also includes generated-script behavior, so execute generation and wait for compilation first:

On the tested CLI beta, save and close the disposable project's Editor before `unity test`; it
starts its own batch Editor and rejects an already-open project. Use an existing output folder
outside Assets. Never close another working project to run this example.

```bash
unity test /absolute/project --mode EditMode \
  --filter UnityBestPractices.Samples.Cli.Tests \
  --output /absolute/results/cli-script-edit.xml --format json
```

Generator tests verify preview creates neither source nor metadata, reruns preserve GUID/metadata,
conflicts preserve existing content, and invalid paths are rejected. They create temporary fixture
folders through AssetDatabase and remove only their owned fixtures. Generated tests verify score
accumulation and rejected negative input without state changes. Reflection keeps the test assembly
compilable before initial generation; missing generation fails with an actionable message rather
than reporting an ignored/pass placeholder. Ordinary runtime tests should prefer direct type access.

Use a fresh output path and inspect the NUnit XML's total/passed/failed/skipped counts and each
failure message, alongside the fresh Editor log. The expected CLI example count is seven tests,
zero failures and zero skipped tests. A filter matching zero tests is not validation. On the tested
CLI, exit 8 means test failures and exit 6 means execution/infrastructure failure; neither is success.
No PlayMode run is needed for this pure score operation; the other examples demonstrate that route.
Manual fallback: invoke the command's public Editor method and use Test Runner.

When changing generated behavior, change its source template and assertions together. The generator
intentionally does not overwrite a modified existing script; reconcile that change explicitly.
