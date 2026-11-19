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

**A copy with no record can still be updated.** Teams often copy the kit's files by hand into their
own folders and never record where they came from. The agent then reconstructs the baseline: it
finds the upstream commit whose files are most similar to your copy and classifies each file as
near-pristine, adapted, or a local fork. This matters because the copy can look heavily rewritten
when compared with today's upstream while really being an untouched older snapshot. In one real
project, 17 copied review documents scored 0.44 against the current upstream and 0.99 against the
commit they were copied from: almost every difference was upstream progress, safe to merge.

**Overlay, not edit-in-place.** For files you really have rewritten, the agent recommends keeping an
unmodified pinned snapshot plus one short overrides file listing your deliberate differences. The
next update replaces the snapshot and only the overrides need review. It also recommends writing the
installation record, so the next update starts from a known baseline.

Imported resource updates retain the destination's identities and references. Documentation updates
usually need static checks; resource changes also need Unity validation. This workflow does not
upgrade Unity/packages or migrate saves; those require separate selections. For a release candidate,
use [release readiness](../ReleaseReadiness/README.md).
