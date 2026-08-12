from __future__ import annotations

import unittest

from grand_intellect.council_motion import assess_motion
from grand_intellect.council_review import COUNCIL_OFFICES, canonical_sha256


def motion() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "matter_id": "MOTION-001",
        "title": "Test motion",
        "status": "before_council",
        "proposal_path": "proposal.md",
        "proposal_sha256": "a" * 64,
        "passage_rule": "full_quorum_unanimous_consent",
        "required_offices": [office.value for office in COUNCIL_OFFICES],
        "affirmative_dispositions": ["table_for_human_steward_disposition", "convene_governance_rework_committee"],
        "allowed_dispositions": ["table_for_human_steward_disposition", "convene_governance_rework_committee", "reject", "abstain"],
        "authority": {
            "effect": "advisory",
            "current_rules_remain_effective": True,
            "human_steward_action_required": True,
            "article_xi_process_required": True,
            "automation_may_impersonate_human": False,
            "automation_may_activate": False,
            "automation_may_certify_mathematics": False,
        },
        "review_directory": "reviews",
        "disposition_path": "disposition.json",
    }


def reviews(value: dict[str, object], disposition: str) -> list[dict[str, object]]:
    digest = canonical_sha256(value)
    return [
        {
            "schema_version": "1.0",
            "matter_id": value["matter_id"],
            "motion_sha256": digest,
            "office": office.value,
            "reviewer_id": f"motion-{office.value}",
            "disposition": disposition,
            "deliberation": f"Independent {office.value} deliberation.",
            "discharged_obligations": [f"Discharged {office.value}."],
            "findings": [],
            "amendments": [],
            "residual_uncertainty": [],
            "evidence_refs": ["proposal.md"],
        }
        for office in COUNCIL_OFFICES
    ]


class CouncilMotionTests(unittest.TestCase):
    def test_unanimous_tabling_passes(self) -> None:
        value = motion()
        result = assess_motion(value, reviews(value, "table_for_human_steward_disposition"))
        self.assertTrue(result.full_quorum)
        self.assertTrue(result.unanimous)
        self.assertEqual(result.procedural_disposition, "table_for_human_steward_disposition")

    def test_unanimous_committee_referral_passes(self) -> None:
        value = motion()
        result = assess_motion(value, reviews(value, "convene_governance_rework_committee"))
        self.assertEqual(result.procedural_disposition, "convene_governance_rework_committee")

    def test_split_vote_fails_closed(self) -> None:
        value = motion()
        records = reviews(value, "convene_governance_rework_committee")
        records[0]["disposition"] = "table_for_human_steward_disposition"
        result = assess_motion(value, records)
        self.assertFalse(result.unanimous)
        self.assertEqual(result.procedural_disposition, "no_unanimous_disposition")
        self.assertTrue(result.current_rules_remain_effective)

    def test_abstention_cannot_pass(self) -> None:
        value = motion()
        result = assess_motion(value, reviews(value, "abstain"))
        self.assertTrue(result.unanimous)
        self.assertEqual(result.procedural_disposition, "no_unanimous_disposition")

    def test_unanimous_rejection_cannot_pass(self) -> None:
        value = motion()
        result = assess_motion(value, reviews(value, "reject"))
        self.assertTrue(result.unanimous)
        self.assertEqual(result.procedural_disposition, "no_unanimous_disposition")

    def test_stale_review_fails_closed(self) -> None:
        value = motion()
        records = reviews(value, "convene_governance_rework_committee")
        records[0]["motion_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale"):
            assess_motion(value, records)

    def test_authority_relaxation_fails_closed(self) -> None:
        value = motion()
        authority = value["authority"]
        assert isinstance(authority, dict)
        authority["automation_may_impersonate_human"] = True
        with self.assertRaisesRegex(ValueError, "authority boundary"):
            assess_motion(value, reviews(value, "convene_governance_rework_committee"))

    def test_missing_office_fails_closed(self) -> None:
        value = motion()
        with self.assertRaisesRegex(ValueError, "missing Council motion reviews"):
            assess_motion(value, reviews(value, "convene_governance_rework_committee")[:-1])

    def test_duplicate_reviewer_fails_closed(self) -> None:
        value = motion()
        records = reviews(value, "convene_governance_rework_committee")
        records[1]["reviewer_id"] = records[0]["reviewer_id"]
        with self.assertRaisesRegex(ValueError, "two Council offices"):
            assess_motion(value, records)


if __name__ == "__main__":
    unittest.main()
