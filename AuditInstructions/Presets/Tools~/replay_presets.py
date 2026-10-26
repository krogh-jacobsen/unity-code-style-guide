"""Generate preset decision prompts; does not execute an agent or mutate a Unity project."""
import argparse
import json
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[1]


def generate():
    cases = json.loads((Path(__file__).with_name('workflow_scenarios.json')).read_text())["cases"]
    fixtures = []
    for case in cases:
        task = case.get("task", "Audit and recommend. Nothing is selected or confirmed for mutation; stop after recommendations.")
        context = "\n".join(f"- {key}: {value}" for key, value in case["context"].items())
        fixtures.append({
            "id": case["id"],
            "document": str(FOLDER / "SetupPresets.md"),
            "prompt": f"Use {FOLDER / 'SetupPresets.md'}. {task}\n"
                      "Fictional disposable target: /fixtures/FixtureRepo/FixtureGame. "
                      "Owned scope is Assets/FixtureGame; other paths exist only where specified below. "
                      "Editor is 6000.7.0b4 and closed unless overridden; no fresh tests have run. "
                      "No real project or mutation authorization is supplied by these fixtures.\n"
                      + context,
            "expected": case["expected"],
            "result": "Not verified",
        })
    return fixtures


def write_fixtures(output):
    output = output.resolve()
    # Keep generated transcripts outside the repository; never replace an existing file.
    if output.is_relative_to(FOLDER.parents[1]):
        raise ValueError("choose a new output file outside the repository")
    fixtures = generate()
    with output.open("x") as stream:
        stream.write(json.dumps(fixtures, indent=2) + "\n")
    return len(fixtures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        count = write_fixtures(args.output)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f"Generated {count} preset fixtures; behavior remains Not verified until observed")
