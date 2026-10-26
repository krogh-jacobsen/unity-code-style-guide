> How it works: run the repository validator for structural checks; use the replay fixtures to
> evaluate how an agent follows a published workflow in a fresh session.

# Audit maintenance tools

| Situation | Tool or reference |
|---|---|
| Check repository links, GUIDs, review contracts, and topic validators | `python3 AuditInstructions/Tools/validate_all.py` |
| Run contract-discovery and wording regressions | `python3 AuditInstructions/Tools/test_audit_contract.py` |
| Generate audit and decision replay prompts per applicable scenario | `python3 AuditInstructions/Tools/replay_workflows.py --output /absolute/temp/workflow-fixtures.json` |
| Review replay contexts and expected decisions | [workflow_scenarios.json](workflow_scenarios.json) |
| Inspect observed fresh-agent results, frozen sources, and grading evidence | [2026-10-26 replay results](replay_results_2026-10-26.json) |

The canonical review contract remains in root AGENTS.md. The validator discovers entry points from
published handoff tables independently of a document's opening text, then requires the complete
contract verbatim. Read-only lenses remain behind the project-review router.

## Behavioral replay protocol

Generate the fixtures outside the repository, then give each prompt to a fresh agent session with
only the named entry document and the fixture's target project/evidence. Use its `prompt` without
`expected` outcomes, then grade against those outcomes separately. Default cases stop after
recommendations; decision cases carry scenario-specific selection, approval, evidence freshness, or
acceptance state instead. Fictional authorization applies only inside the fixture, never to a real
workspace. For an actual tool replay,
prepare an isolated disposable target with the stated state and record its before/after files,
metadata identities, settings, and commands. Never use a working game for destructive negative cases.

Grade every expected outcome Pass, Fail, or Not verified. Record the model/tool environment, source
revision or working-tree snapshot, transcript, observed writes/actions, and the smallest contradictory
instruction for failures. A fabricated context tests decision-making only; an observed disposable
project tests the tool behavior too. Re-run relevant cases after changing a gate, route, prerequisite,
or repeat-run rule.

The Python tests validate fixture generation, discovery, contract corruption, and routing invariants.
They do not execute an LLM or prove that an agent follows the prose. Generated prompts and expected
outcomes are a replay suite, not a record of passing agent behavior.

The catalog supplies a canonical nested project/repository baseline and workflow-specific prerequisite
evidence. Source and case snapshots keep earlier attempts reproducible while later wording changes.
Observed replay results distinguish decisions from actual Unity or remote-tool execution.
