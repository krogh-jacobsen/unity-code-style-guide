"""Generate review-only workflow replay prompts; never executes an agent or edits a target project."""
import argparse
import json
from pathlib import Path
from audit_contract import published_entry_points

ROOT = Path(__file__).resolve().parents[2]


def generate(root=ROOT):
    cases = json.loads((root / "AuditInstructions/Tools/workflow_scenarios.json").read_text())["cases"]
    fixtures = []
    for path in published_entry_points(root):
        relative = path.relative_to(root / "AuditInstructions").as_posix()
        for case in cases:
            if case["entry_points"] != "all" and relative not in case["entry_points"]:
                continue
            context = "\n".join(f"- {key}: {value}" for key, value in case["context"].items())
            fixtures.append({
                "id": f"{relative}:{case['id']}",
                "document": path.relative_to(root).as_posix(),
                "prompt": f"Audit and recommend using {path}. Treat the following as fixture evidence. "
                          "Nothing is selected or confirmed for mutation; stop after recommendations.\n" + context,
                "expected": case["expected"],
                "result": "Not verified",
            })
    return fixtures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New temporary JSON file outside the repository")
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(ROOT) or args.output.exists():
        parser.error("choose a new output file outside the repository")
    fixtures = generate()
    args.output.write_text(json.dumps(fixtures, indent=2) + "\n")
    print(f"Generated {len(fixtures)} replay fixtures; behavior remains Not verified until observed")
