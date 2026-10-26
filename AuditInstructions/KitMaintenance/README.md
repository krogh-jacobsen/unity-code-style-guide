> How it works: give your agent "Update my installed Unity starter kit using UpdateKit.md".
> It compares the old source, your adapted copy, and the new source, then applies only confirmed changes.

| Situation | Document to hand over |
|---|---|
| Update documentation, conventions, or installed resources | [UpdateKit.md](UpdateKit.md) |
| First installation | [Setup workflow](../SetupInstructions/README.md) |

# Keep an adapted kit current

A copied kit becomes part of your project: namespace choices, package versions, conventions, and
import settings may differ intentionally. An upstream replacement can erase those decisions.
A three-way comparison uses the previously installed source as the baseline, separating your local
changes from upstream changes. Overlapping changes need a deliberate merge.

The agent asks for the old and new revisions, selected groups, and the project's installation
record. If the old revision is unknown, preserving current files is the default until each difference
is understood. Source revisions describe provenance, not proof that a target project was tested.

Imported resource updates retain the destination's identities and references. Documentation updates
usually need static checks; resource changes also need Unity validation. This workflow does not
upgrade Unity/packages or migrate saves; those require separate selections. For a release candidate,
use [release readiness](../ReleaseReadiness/README.md).
