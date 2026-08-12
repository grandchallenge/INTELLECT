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
    / "GI-COUNCIL-OPERATING-BURDEN-002"
)


class OperatingBurdenCouncilTests(unittest.TestCase):
    def test_exact_council_docket_is_ready_with_conditions(self) -> None:
        compiled = compile_docket(MATTER_ROOT / "matter.json", MATTER_ROOT / "reviews")
        retained = json.loads(
            (MATTER_ROOT / "disposition.json").read_text(encoding="utf-8")
        )
        self.assertEqual(compiled.to_dict(), retained)
        self.assertEqual(compiled.procedural_disposition, "ready_with_conditions")
        self.assertTrue(compiled.ready_for_human_disposition)
        self.assertEqual(compiled.review_count, 10)

    def test_effective_staffing_already_excludes_routine_recovery_owner(self) -> None:
        schedule = json.loads(
            (ROOT / "governance" / "constitutional_authority_schedule.json").read_text(
                encoding="utf-8"
            )
        )
        staffing = schedule["staffing"]
        self.assertEqual(staffing["ordinary_human_steward"], "fyremael")
        self.assertEqual(staffing["recovery_owner"], "jimsteeg")
        self.assertEqual(staffing["mandatory_routine_reviewers"], [])
        self.assertEqual(staffing["human_actions_per_governed_decision_target"], 1)

    def test_council_record_does_not_claim_reserved_effect(self) -> None:
        disposition = json.loads(
            (MATTER_ROOT / "disposition.json").read_text(encoding="utf-8")
        )
        boundary = disposition["authority_boundary"]
        for reserved in ("approve", "merge", "activate", "ratify", "certify"):
            self.assertIn(reserved, boundary.lower())


if __name__ == "__main__":
    unittest.main()
