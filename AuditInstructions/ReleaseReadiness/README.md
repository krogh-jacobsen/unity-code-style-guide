> How it works: give your agent "Review my release candidate using ReleaseReadiness.md".
> It gathers evidence, recommends fixes and acceptance checks, and changes only what you confirm.

| Situation | Document to hand over |
|---|---|
| Assess a candidate and prepare its release handoff | [ReleaseReadiness.md](ReleaseReadiness.md) |
| Configure platform build settings | [BuildSettings](../BuildSettings/README.md) |
| Establish test infrastructure | [Testing](../Testing/README.md) |

# A build is one part of release evidence

A release candidate is a particular artifact from a known source revision and toolchain. A successful
compile does not establish first-run behavior, save compatibility, installation, or performance on
the supported hardware. Tie acceptance evidence to the artifact you intend to distribute.

The agent asks about platforms, distribution route, blocking criteria, saved-data compatibility,
known issues, and recovery. Checks unavailable on the current host stay visible. Human playtest and
visual acceptance remain useful evidence rather than implied passes from automation.

Recovery includes player data: an older binary may not understand data written by a newer version.
Decide that policy before promising rollback. This workflow prepares a reviewable handoff; uploading,
publishing, store submission, signing-account administration, and legal clearance need their own
scope and owner. It links existing setup and audit topics rather than duplicating their settings.
