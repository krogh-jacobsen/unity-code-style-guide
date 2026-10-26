"""Cross-folder regressions for published entry points and workflow replay fixtures."""
from pathlib import Path
import tempfile
import unittest

from audit_contract import canonical_contract, contract_errors, published_entry_points
from replay_workflows import generate

ROOT = Path(__file__).resolve().parents[2]


class ReviewContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = canonical_contract((ROOT / "AGENTS.md").read_text())
        self.valid = "> How it works: review first.\n\n" + self.contract + "\n\n## 1. Preflight\n"

    def test_valid_contract(self):
        self.assertEqual([], contract_errors(self.valid, self.contract))

    def test_truncated_contract(self):
        self.assertTrue(contract_errors(self.valid.replace("Read-only.", ""), self.contract))

    def test_changed_confirmation(self):
        self.assertTrue(contract_errors(self.valid.replace("wait for an explicit yes", "proceed by default"), self.contract))

    def test_duplicate_contract(self):
        self.assertTrue(contract_errors(self.valid + self.contract, self.contract))

    def test_contract_after_step(self):
        self.assertIn("review contract must come before step 1", contract_errors(
            "> How it works: review first.\n\n## 1. Apply\n" + self.contract, self.contract))

    def test_published_guide_without_preamble_is_still_discovered(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            (root / "AuditInstructions/Testing").mkdir(parents=True)
            (root / "AGENTS.md").write_text("## On-demand references\n| Task | Read |\n| Test | [Setup](AuditInstructions/Testing/TestingInstructions.md) |\n")
            (root / "AuditInstructions/README.md").write_text("| Task | Hand your agent | Read first |\n| Test | [Setup](Testing/TestingInstructions.md) | same |\n")
            path = root / "AuditInstructions/Testing/TestingInstructions.md"
            path.write_text("# Setup\n\n## 1. Install\n")
            self.assertIn(path, published_entry_points(root))
            self.assertTrue(contract_errors(path.read_text(), self.contract))

    def test_current_published_contracts(self):
        for path in published_entry_points(ROOT):
            with self.subTest(path=path):
                self.assertEqual([], contract_errors(path.read_text(), self.contract))

    def test_replay_fixture_coverage(self):
        fixtures = generate()
        self.assertEqual(len(fixtures), len({f["id"] for f in fixtures}))
        for path in published_entry_points(ROOT):
            selected = [f for f in fixtures if f["document"] == path.relative_to(ROOT).as_posix()]
            self.assertGreaterEqual(len(selected), 5)
            for fixture in selected:
                self.assertTrue(fixture["expected"])
                self.assertEqual("Not verified", fixture["result"])
                self.assertIn("stop after recommendations", fixture["prompt"])
        for scenario in ("partial-install", "repeat-run", "single-platform"):
            self.assertTrue(any(f["id"].endswith(":" + scenario) for f in fixtures))

    def test_setup_routes_mobile_and_packages(self):
        setup = (ROOT / "AuditInstructions/SetupInstructions/README.md").read_text()
        self.assertIn("../BuildSettings/MobileBuilds.md", setup)
        self.assertIn("../PackageInstaller/InstallPackages.md", setup)

    def test_rendering_and_uncovered_systems_are_routed(self):
        router = (ROOT / "AuditInstructions/ProjectAuditGuides/ProjectReview.md").read_text()
        self.assertIn("UnityRenderingInstructions.md", router)
        self.assertIn("Outside coverage", router)
        for system in ("Navigation", "Networking", "Physics2D", "DOTS"):
            self.assertIn("| " + system + " |", router)


if __name__ == "__main__":
    result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(ReviewContractTests))
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(f"PASS audit workflow regressions: {result.testsRun} tests")
