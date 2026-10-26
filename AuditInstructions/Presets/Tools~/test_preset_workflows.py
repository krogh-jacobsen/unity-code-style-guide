"""Regression checks for replay safety and authorization context, not observed agent behavior."""
from pathlib import Path
import tempfile
import unittest

from replay_presets import FOLDER, generate, write_fixtures


class PresetReplayTests(unittest.TestCase):
    def test_decision_cases_retain_approval_and_withhold_grading(self):
        fixtures = {fixture["id"]: fixture for fixture in generate()}
        self.assertEqual(9, len(fixtures))
        decisions = {"preset-approved-update", "preset-unsaved-registration", "preset-correction-and-noop"}
        for name, fixture in fixtures.items():
            self.assertEqual(str(FOLDER / "SetupPresets.md"), fixture["document"])
            self.assertEqual("Not verified", fixture["result"])
            for expected in fixture["expected"]:
                self.assertNotIn(expected, fixture["prompt"])
            if name in decisions:
                self.assertIn("Continue the workflow", fixture["prompt"])
                self.assertNotIn("Nothing is selected or confirmed for mutation", fixture["prompt"])
                self.assertIn("fictional fixture itself authorizes no real workspace changes", fixture["prompt"])
            else:
                self.assertIn("stop after recommendations", fixture["prompt"])

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "fixtures.json"
            self.assertEqual(9, write_fixtures(output))
            before = output.read_bytes()
            with self.assertRaises(FileExistsError):
                write_fixtures(output)
            self.assertEqual(before, output.read_bytes())

    def test_repository_output_is_rejected_before_writing(self):
        with self.assertRaises(ValueError):
            write_fixtures(FOLDER / "Tools~" / "must-not-be-generated.json")


if __name__ == "__main__":
    unittest.main()
