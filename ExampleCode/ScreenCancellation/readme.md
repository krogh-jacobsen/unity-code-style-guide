# Screen cancellation and stale results

Use this example when a screen owns asynchronous requests that can finish after it closes or after
another request starts. It complements the [UI tree-lifetime example](../UIToolkitMVP/readme.md):
this sample focuses on work ownership, without adding another UI architecture or visual asset set.

## Contract

One enabled screen owns one `SearchSession`; disabling disposes it and reopening creates a new one.
Each request cancels its predecessor. Cancellation asks the provider to stop; request identity also
prevents a noncooperative provider from publishing a late result. Requests own disposal of their
cancellation sources when work actually exits. Result callbacks and Unity access stay on the main
thread; a real background provider must switch back before returning.

`SearchScreenExample` supplies an attachable adapter and a local delayed preview service. UI code
can call `RequestSearch(query)` and render `DisplayedResult`; it does not require the MVP example.
The `async void` UI boundary awaits the operation and logs unexpected failures. The local provider
is a demonstration, not network code, a debounce policy, or a cache. A provider that ignores
cancellation forever still retains its pending operation; the identity guard prevents stale writes,
but does not make that provider release resources.

## Install and exercise through Unity CLI

Requires Unity 6 Awaitable; tested versions are recorded in [Validation](../../Validation.md).
Test Framework is needed only for the isolated test assemblies. Copy this folder's code, asmdefs,
and metadata to `Assets/Examples/ScreenCancellation/`; keep this README outside Assets. Inspect
path/GUID conflicts first and preserve the layout when copying the optional tests.

Discover the target Editor's commands with `unity status --format json` and
`unity command --project-path /absolute/project`. Import/refresh and require no compiler errors.
For a live demonstration, use the discovered GameObject/component commands or CLI-driven Editor
APIs to attach `SearchScreenExample` in an isolated scene. Enter Play and invoke
`RequestSearch("old")`, disable/re-enable the component before completion, then request `"new"`.
The displayed result must become `Preview: new`. Invoke from the Editor main thread and read the
property through the CLI. A current session starts with an empty display.

On the tested CLI beta, save and close the disposable project's Editor before `unity test`; it
starts its own batch Editor. Choose fresh result paths outside Assets in an existing output folder:

```bash
unity test /absolute/project --mode EditMode \
  --filter UnityBestPractices.Samples.Cancellation.Tests --output /absolute/results/search-edit.xml
unity test /absolute/project --mode PlayMode \
  --filter UnityBestPractices.Samples.Cancellation.Tests --output /absolute/results/search-play.xml
```

EditMode tests control completion order and deliberately ignore cancellation: the newer result
wins, a closed session cannot affect a reopened one, and provider failures reach the caller.
PlayMode covers actual Awaitable cancellation on disable and destruction. Read XML counts/failures
and fresh logs; missing/discovered-zero tests are not a passing verification.
Manual fallback: attach the component, use its Request Preview context menu in Play, and Test Runner.

See Unity's [Awaitable continuation guidance](https://docs.unity.com/en-us/engine/6000.0/manual/scripting/optimization/async-await-support/async-awaitable-continuations).
