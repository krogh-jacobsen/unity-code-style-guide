"""Cross-document review-contract checks; canonical wording remains in AGENTS.md."""
from pathlib import Path
import re

REVIEW_HEADING = "## Review, recommend, confirm"
WORKFLOW_READMES = {"AuditInstructions/SetupInstructions/README.md"}


def canonical_contract(agents):
    for block in re.findall(r"```markdown\n(.*?)\n```", agents, re.S):
        if block.startswith(REVIEW_HEADING):
            return block
    raise ValueError("AGENTS.md has no canonical review-contract block")


def published_entry_points(root):
    """Discover handoff targets from published tables even when a target loses its preamble."""
    root = Path(root)
    result = {root / name for name in WORKFLOW_READMES}
    for name in ("AGENTS.md", "AuditInstructions/README.md"):
        source = root / name
        text = source.read_text()
        if name == "AGENTS.md":
            text = text.split("## On-demand references", 1)[1].split("\n## ", 1)[0]
        for line in text.splitlines():
            if not line.startswith("|"):
                continue
            columns = line.split("|")
            if len(columns) < 4:
                continue
            # The second column is the handoff in both published indexes.
            for target in re.findall(r"\[[^]]*\]\(([^)#]+)(?:#[^)]*)?\)", columns[2]):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                path = (source.parent / target).resolve()
                if path.is_relative_to(root.resolve() / "AuditInstructions") and path.suffix == ".md":
                    if path.name.lower() != "readme.md" or str(path.relative_to(root.resolve())) in WORKFLOW_READMES:
                        # Lenses are read-only references loaded through the router, not setup entry points.
                        if path.parent.name != "ProjectAuditGuides" or path.name == "ProjectReview.md":
                            result.add(path)
    for path in (root / "AuditInstructions").rglob("*.md"):
        if path.name.lower() != "readme.md" and "> How it works:" in "\n".join(path.read_text().splitlines()[:6]):
            result.add(path)
    return sorted(result)


def contract_errors(text, contract):
    errors = []
    if "> How it works:" not in "\n".join(text.splitlines()[:6]):
        errors.append("missing opening handoff blockquote")
    if text.count(contract) != 1:
        errors.append("review contract must match AGENTS.md verbatim exactly once")
    first_step = re.search(r"^## 1\.\s", text, re.M)
    if first_step and (contract not in text or text.index(contract) > first_step.start()):
        errors.append("review contract must come before step 1")
    return errors
