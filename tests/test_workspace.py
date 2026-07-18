from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from grand_intellect.cli import main
from grand_intellect.workspace import WorkPackageWorkspace


class WorkspaceTests(unittest.TestCase):
    def test_initialize_materializes_complete_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "WP-LOCAL"
            paths = WorkPackageWorkspace(root).initialize(
                work_package_id="WP-LOCAL",
                title="Local authoring bundle",
                purpose="Make the workflow tangible.",
                scope="One charter.",
                acceptance_criteria=("Bundle exists",),
            )
            self.assertTrue(paths.ledger.exists())
            self.assertTrue((root / "IMPLEMENTATION" / "README.md").exists())
            status = json.loads(paths.status.read_text(encoding="utf-8"))
            self.assertEqual(status["phase"], "charter")
            self.assertFalse(status["authoritative"])
            gate = json.loads(paths.gate_report.read_text(encoding="utf-8"))
            self.assertFalse(gate["ready"])

    def test_cli_init(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "WP-CLI-INIT"
            code = main(
                [
                    "init",
                    str(root),
                    "WP-CLI-INIT",
                    "--title",
                    "CLI init",
                    "--purpose",
                    "Exercise materialization",
                    "--scope",
                    "One workspace",
                    "--criterion",
                    "Files exist",
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue((root / "CHARTER.md").exists())


if __name__ == "__main__":
    unittest.main()
