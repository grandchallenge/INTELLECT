from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from grand_intellect.constitutional_authority import (
    ConstitutionalAuthorityError,
    validate_authority_schedule,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_PATH = ROOT / "governance" / "constitutional_authority_schedule.json"


class ConstitutionalAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))

    def test_proposed_schedule_validates_without_claiming_activation(self) -> None:
        validate_authority_schedule(self.schedule)
        self.assertEqual(self.schedule["status"], "proposed")
        self.assertIsNone(self.schedule["activation"]["human_steward_approval"])

    def test_commentary_cannot_become_constitutional_law(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["commentary"]["authority"] = "normative"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "interpretive and nonbinding"
        ):
            validate_authority_schedule(broken)

    def test_standards_registry_cannot_claim_constitutional_ownership(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["operating_standard"]["registry_role"] = "constitutional_authority"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "subordinate registry"
        ):
            validate_authority_schedule(broken)

    def test_github_cannot_become_semantic_authority(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["github"]["authority"] = "production_semantic_authority"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "operational and evidentiary"
        ):
            validate_authority_schedule(broken)

    def test_activation_fails_without_human_and_independent_review(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["status"] = "active"
        broken["operating_standard"]["status"] = "accepted"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "human_steward_approval"
        ):
            validate_authority_schedule(broken)


if __name__ == "__main__":
    unittest.main()
