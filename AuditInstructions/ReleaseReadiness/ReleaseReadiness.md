> How it works: give this URL to your agent with "Review my release candidate".
> It audits evidence, recommends checks and fixes, and executes only confirmed work. Human overview: [README](README.md).

# Release readiness

## Operating rules

- Identify one candidate by source revision, build configuration, toolchain, artifact path, and
  checksum. Tie evidence to that candidate; relevant rebuilds invalidate affected acceptance results.
- Preserve local work and player data. Use copies of save fixtures and disposable test installations.
  Make project/asset changes through the project's approved tools, preserving metadata and references.
- Treat signing credentials as secrets. Record signing status and artifact identity, not private keys
  or tokens. Verify current distribution requirements from the chosen platform's official sources.
- Prepare a candidate and handoff within the user's scope. Publishing, uploading, store submission,
  account changes, and notifying others require explicit authorization for those actions.

## Review, recommend, confirm

This document always runs in four stages. Nothing is written to the project until stage 4 ends in an
explicit user confirmation.

1. **Audit.** Read the project and report what already matches this document, what differs, and what
   could not be checked. Read-only.
2. **Recommend.** List every difference as a numbered recommendation: ID, finding, proposed change,
   why it matters, risk (low, medium, high), and a default (do or skip). List items that already
   match as "no change needed". Add recommendations of your own from what you found, including ones
   this document does not mention.
3. **Choose.** The user picks any subset of IDs, "all recommended", or none. Carry over only the
   picked items; unpicked items stay proposals in the report.
4. **Confirm.** Present the exact changes for the picked subset (files, settings, values, commands)
   and obtain explicit user authorization before making them, including saving the report.
   Confirmation need not contain the literal word "yes": after the concrete scope is presented,
   "implement R1 and R3" can both select and confirm those items. Selection alone ("R1 and R3")
   chooses scope without authorizing implementation. Honor existing authorization for unchanged
   scope without asking again; clarify a delayed reply only when its scope is materially ambiguous.
   Resolve IDs against the presented change list rather than guide defaults. If evidence establishes
   that exact scope was previously presented and authorized but its record is now unavailable,
   retrieve that record before execution; recovered unchanged scope needs no repeat confirmation.
   If concrete changes were never presented, an instruction to implement an ID leaves scope
   unconfirmed: first present the exact changes and obtain confirmation before execution.
   Changed scope needs confirmation for the changed items. In a non-interactive session, or when
   authorization is absent, stop after stage 2 and change nothing.

Steps below that apply, install, or build run only after stage 4, and only for confirmed items. A new
finding during those steps becomes a new recommendation and returns to stage 3.

## 1. Audit the candidate and evidence

Read project instructions, source/dirty state, exact Editor/packages, target/backend/architecture,
build profile and scene list, existing release process, fresh test/build logs, known issues, and the
candidate artifact if present. Distinguish a reproducible committed build from a build with local
changes; record the latter's exact patch when selected. Inventory prior validation rather than
silently treating it as evidence for this candidate.

Record each acceptance area below as Passed, Failed, Not verified, or Not applicable with a reason.
Report differences as recommendations; collecting evidence is read-only until checks are confirmed.

**Done:** candidate identity and every acceptance area's existing evidence/gap are recorded.

## 2. Ask the release contract

Ask one batch: supported platforms/hardware, distribution route and version identifiers, blocking
criteria, primary player journeys, required save/settings compatibility, supported upgrade path,
known issues allowed to ship, human acceptance owner, and rollback/recovery policy.
Defaults: use the documented support contract; unresolved required evidence blocks a ready verdict;
keep all data tests on copies; prepare locally without publishing. Confirm exact fixes, commands,
output paths, evidence files, and acceptance checks before execution.

**Done:** required gates, optional checks, owners, exclusions, and exact work are confirmed.

## 3. Prepare selected fixes and acceptance checks

| Area | Target outcome | How to establish it | Condition |
|---|---|---|---|
| Provenance | Candidate identifies source, toolchain, profile, version and content | Record commit/patch, resolved packages, build logs and artifact checksum | Every candidate |
| Build/configuration | Intended platform, scenes, runtime dependencies and release options | Inspect saved configuration; build using the project's discovered commands; record diagnostics | Each supported target selected |
| Automated checks | Relevant tests pass with no unexplained missing discovery | Read fresh XML/logs and report executed, failed and skipped tests; verify ordinary-player test isolation | Selected suites |
| First run/install | Delivered package installs, launches, and exits under supported conditions | Use a fresh test account/install or equivalent isolated environment without Editor dependencies | Each required OS/device |
| Player journeys | Agreed core journey and failure/recovery paths work | Run the built candidate; record inputs, observations, and human acceptance where needed | Required gameplay/UI paths |
| Data compatibility | Existing saves/settings survive the agreed upgrade | Copy supported old fixtures, upgrade, reopen, verify behavior, test invalid/missing data and recovery | Persistence used |
| Performance/visuals | Meets agreed budgets and presentation expectations | Measure representative workload on named target hardware; record conditions and captures | Required support tiers |
| Diagnostics | Failures can be traced to this build | Preserve matching symbols and build logs; verify diagnostic output avoids credentials/player secrets | Platform/toolchain applicable |
| Distribution materials | Selected notices, content inventory, and platform requirements are accounted for | Inventory third-party dependencies/notices; record platform requirement source/date and responsible review owner | Distribution route selected |
| Recovery | Previous artifact and compatible data recovery path are known | Retain prior artifact/fixtures; rehearse selected recovery without touching live player data | Update release |

Use the project's existing settings, testing, persistence, and platform workflows for detailed fixes.
Aggregate their findings into this confirmed scope; unselected work stays proposed. If no candidate
exists, build only after confirmation. Run a fresh normal player rather than relying on an Editor
PlayMode session for install/runtime acceptance.

**Done:** every confirmed fix/check is executed or explicitly unavailable, with evidence tied to the candidate.

## 4. Verify the handoff and recovery

Recheck artifact checksum after packaging and confirm evidence matches the delivered bytes. Any
change that affects behavior, packaging, signatures, or dependencies requires affected checks again.
Ensure the installation/upgrade test used the intended package and isolated data. Check that prior
artifacts and the agreed data recovery path are accessible. Record unsupported rollback when an older
binary cannot read the new save format; require an explicit recovery decision rather than claiming
that retaining the old executable solves it.

**Done:** all required gates pass for this artifact or the readiness result explicitly names each blocker.

## 5. Report readiness

Produce a candidate handoff in the confirmed location: source/toolchain identity, artifact/checksum,
configuration, evidence matrix, test/build counts, human acceptance, known issues, unverified checks,
release notes, and recovery instructions. Use Ready, Blocked, or Ready with explicitly accepted
exceptions; name the owner and evidence for any exception. Optional checks remain follow-up QA.
Place unresolved choices in **Needs your decision**. Stop at the handoff unless publishing was
separately authorized; release readiness alone authorizes no external upload or message.

**Done:** every gate has evidence or an explicit exception/blocker, and the handoff identifies the exact candidate.
