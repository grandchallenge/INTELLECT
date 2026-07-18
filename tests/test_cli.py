from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from grand_intellect.cli import main
from grand_intellect.model import IntellectEvent


class CliTests(unittest.TestCase):
    def test_status_projects_jsonl(self) -> None:
        event = IntellectEvent(
            event_type="work_package.chartered",
            work_package_id="WP-CLI",
            actor="human_steward",
            payload={
                "title": "CLI test",
                "purpose": "Projection",
                "scope": "One ledger",
                "acceptance_criteria": ["Readable"],
                "constraints": [],
                "stakeholders": [],
            },
        )
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "events.jsonl"
            ledger.write_text(json.dumps(event.to_dict()) + "\n", encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(["status", str(ledger), "WP-CLI"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["phase"], "charter")


if __name__ == "__main__":
    unittest.main()
