> How it works: run the local validator to catch checklist rows detached from their Markdown tables.

# Audit guide maintenance

| Situation | Tool |
|---|---|
| Check checklist table rendering and parser regressions | `python3 AuditInstructions/ProjectAuditGuides/Tools~/validate_audit_guides.py` |

A blank line ends a GitHub Markdown table. Rows added after that line need a new header and separator;
otherwise the checklist becomes plain text. The validator checks this structure and runs positive and
negative parser fixtures. It does not judge technical claims or simulate an agent following a guide.
The repository validator discovers and runs it automatically.
