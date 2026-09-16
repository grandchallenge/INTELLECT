from __future__ import annotations

import json
import unittest
from pathlib import Path

from grand_intellect.council_review import compile_docket


ROOT = Path(__file__).resolve().parents[1]
MATTER_ROOT = (
    ROOT
    / "governance"
    / "council_matters"
    / "GI-COUNCIL-RSI-CCC-001"
)


class RsiCccCouncilTests(unittest.TestCase):
    def test_exact_council_docket_is_ready_with_conditions(self) -> None:
        compiled = compile_docket(MATTER_ROOT / "matter.json", MATTER_ROOT / "reviews")
        retained = json.loads(
            (MATTER_ROOT / "disposition.json").read_text(encoding="utf-8")
        )
        self.assertEqual(compiled.to_dict(), retained)
        self.assertEqual(compiled.procedural_disposition, "ready_with_conditions")
        self.assertTrue(compiled.ready_for_human_disposition)
        self.assertEqual(compiled.review_count, 10)

    def test_council_record_preserves_reserved_authority_boundary(self) -> None:
        disposition = json.loads(
            (MATTER_ROOT / "disposition.json").read_text(encoding="utf-8")
        )
        boundary = disposition["authority_boundary"].lower()
        for reserved in ("approve", "merge", "activate", "ratify", "certify"):
            self.assertIn(reserved, boundary)


if __name__ == "__main__":
    unittest.main()
