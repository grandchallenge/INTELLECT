from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIRECTIVE = ROOT / "governance/steward_directives/GI-STEWARD-0003.md"
PACKET = ROOT / "governance/staffing_transitions/GI-MULTI-ROLE-STAFFING-001"


class MultiRoleStaffingCandidateTests(unittest.TestCase):
    def test_candidate_contains_article_xi_package(self) -> None:
        self.assertTrue(DIRECTIVE.is_file())
        for name in ("ADR.md", "THREAT_ANALYSIS.md", "MIGRATION.md"):
            self.assertTrue((PACKET / name).is_file())

    def test_candidate_separates_logical_pass_from_system_identity(self) -> None:
        text = DIRECTIVE.read_text(encoding="utf-8")
        for phrase in (
            "reviewer_system_id",
            "logical_pass_id",
            "non_authoring_read_only",
            "routine_bounded",
            "substantive",
            "reserved",
        ):
            self.assertIn(phrase, text)
        self.assertIn("not by multiplying people", text)

    def test_candidate_preserves_reserved_authority(self) -> None:
        text = DIRECTIVE.read_text(encoding="utf-8")
        self.assertIn("Human Steward retains the powers in Article X", text)
        self.assertIn("MATHCERT", text)
        self.assertIn("must not invent", text)

    def test_current_schedule_remains_effective_until_exact_activation(self) -> None:
        schedule = (
            ROOT / "governance/constitutional_authority_schedule.json"
        ).read_text(encoding="utf-8")
        self.assertIn('"identifier": "GI-STEWARD-0002"', schedule)
        self.assertNotIn('"identifier": "GI-STEWARD-0003"', schedule)


if __name__ == "__main__":
    unittest.main()
