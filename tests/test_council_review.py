from __future__ import annotations

import unittest

from grand_intellect.council_review import (
    ALLOWED_DECISIONS,
    COUNCIL_OFFICES,
    assess_council,
    canonical_sha256,
)


def matter() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "matter_id": "TEST-COUNCIL-001",
        "title": "Test matter",
        "status": "before_council",
        "decision_class": "test",
        "proposal_path": "proposal.md",
        "proposal_sha256": "a" * 64,
        "authority": {
            "council_effect": "advisory",
            "reserved_disposition": "human_steward",
            "automation_may_activate": False,
            "automation_may_certify_mathematics": False,
        },
        "required_offices": [office.value for office in COUNCIL_OFFICES],
        "allowed_decisions": sorted(ALLOWED_DECISIONS),
        "review_directory": "reviews",
        "disposition_path": "disposition.json",
    }


def reviews(value: dict[str, object], decision: str = "approve") -> list[dict[str, object]]:
    digest = canonical_sha256(value)
    return [
        {
            "schema_version": "1.0",
            "matter_id": value["matter_id"],
            "matter_sha256": digest,
            "office": office.value,
            "reviewer_id": f"agent-{office.value}",
            "decision": decision,
            "deliberation": f"Independent {office.value} deliberation.",
            "discharged_obligations": [f"Discharged {office.value} mandate."],
            "findings": [],
            "conditions": ["Meet the recorded condition."] if decision == "approve_with_conditions" else [],
            "residual_uncertainty": [],
            "evidence_refs": ["proposal.md"],
        }
        for office in COUNCIL_OFFICES
    ]


class CouncilReviewTests(unittest.TestCase):
    def test_complete_council_is_ready(self) -> None:
        value = matter()
        result = assess_council(value, reviews(value))
        self.assertEqual(result.review_count, 10)
        self.assertEqual(len(result.review_sha256), 10)
        self.assertEqual(result.procedural_disposition, "ready")
        self.assertTrue(result.ready_for_human_disposition)

    def test_conditions_are_preserved(self) -> None:
        value = matter()
        result = assess_council(value, reviews(value, "approve_with_conditions"))
        self.assertEqual(result.procedural_disposition, "ready_with_conditions")
        self.assertEqual(len(result.conditions), 1)

    def test_missing_office_fails_closed(self) -> None:
        value = matter()
        with self.assertRaisesRegex(ValueError, "missing Council reviews"):
            assess_council(value, reviews(value)[:-1])

    def test_stale_review_fails_closed(self) -> None:
        value = matter()
        records = reviews(value)
        records[0]["matter_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "stale"):
            assess_council(value, records)

    def test_one_identity_cannot_hold_two_offices(self) -> None:
        value = matter()
        records = reviews(value)
        records[1]["reviewer_id"] = records[0]["reviewer_id"]
        with self.assertRaisesRegex(ValueError, "two Council offices"):
            assess_council(value, records)

    def test_changes_request_blocks_human_disposition(self) -> None:
        value = matter()
        records = reviews(value)
        records[0]["decision"] = "changes_requested"
        result = assess_council(value, records)
        self.assertEqual(result.procedural_disposition, "returned_for_revision")
        self.assertFalse(result.ready_for_human_disposition)

    def test_automation_authority_fails_closed(self) -> None:
        value = matter()
        authority = value["authority"]
        assert isinstance(authority, dict)
        authority["automation_may_activate"] = True
        with self.assertRaisesRegex(ValueError, "may not activate"):
            assess_council(value, reviews(value))


if __name__ == "__main__":
    unittest.main()
