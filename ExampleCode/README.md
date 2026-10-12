# Selected implementation examples

Load or install an example only for its demonstrated problem. These are optional demonstrations,
not a shared framework or a required project architecture. Preserve the sample folder layout and
metadata; adapt namespaces deliberately when adopting code.

| Example | Problem demonstrated | Dependencies |
|---|---|---|
| [UI Toolkit counter](UIToolkitMVP/readme.md) | Pure presentation contract, object state versus visual-tree lifetime, rebind/dispose | Unity 6.7 UI Toolkit; Test Framework for optional tests |
| [Screen cancellation](ScreenCancellation/readme.md) | Request cancellation, stale completion rejection, close/reopen ownership | Unity 6 Awaitable; Test Framework for optional tests |
| [Pooled notifications](PooledNotifications/readme.md) | Checkout identity, reset/unsubscribe/cancel on return, owned teardown | Unity 6 Awaitable and ObjectPool; Test Framework for optional tests |
| [Custom CLI script and tests](CliScriptAndTests/readme.md) | Register a custom Editor command, preview/generate source safely, run behavioral tests | Compatible Pipeline package and Test Framework |

Keep examples small, runnable, and verified on a recorded Editor. Add another only for a distinct
recurring failure with prerequisites and behavioral checks. Load individual examples when those
problems arise; the library is not part of the baseline project installation. Versioned save/load
is a possible later topic, not a supplied example. See [Validation](../Validation.md).

For CLI test runs on the tested beta, save and close the disposable target project's Editor first;
`unity test` starts its own batch Editor and rejects an already-open project. Keep fresh XML/log
outputs outside Assets. Never close an unrelated working project to run an example's tests.
