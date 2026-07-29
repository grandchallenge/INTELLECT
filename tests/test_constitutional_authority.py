from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from grand_intellect.constitutional_authority import (
    ConstitutionalAuthorityError,
    validate_authority_schedule,
    validate_review_receipt,
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

    def test_review_receipt_binds_three_distinct_role_signoffs(self) -> None:
        receipt = {
            "schema_version": "1.0.0",
            "campaign_id": "GI-AMEND-0001",
            "packet_sha256": "a" * 64,
            "subjects": [
                {
                    "repository": "grandchallenge/INTELLECT",
                    "pull_request": 13,
                    "head_sha": "b" * 40,
                }
            ],
            "signoffs": [
                {
                    "office": "adversary",
                    "reviewer": "red",
                    "reaction_id": 1,
                    "attestation_comment": "https://example.test/1",
                    "attestation_sha256": "c" * 64,
                },
                {
                    "office": "referee",
                    "reviewer": "ref",
                    "reaction_id": 2,
                    "attestation_comment": "https://example.test/2",
                    "attestation_sha256": "d" * 64,
                },
                {
                    "office": "human_steward",
                    "reviewer": "steward",
                    "reaction_id": 3,
                    "attestation_comment": "https://example.test/3",
                    "attestation_sha256": "e" * 64,
                },
            ],
            "status": "complete",
        }
        validate_review_receipt(receipt)

    def test_same_human_cannot_sign_adversary_and_referee(self) -> None:
        receipt = {
            "schema_version": "1.0.0",
            "campaign_id": "GI-AMEND-0001",
            "packet_sha256": "a" * 64,
            "subjects": [{"head_sha": "b" * 40}],
            "signoffs": [
                {
                    "office": office,
                    "reviewer": "same" if office != "human_steward" else "steward",
                    "reaction_id": index,
                    "attestation_comment": f"https://example.test/{index}",
                    "attestation_sha256": "c" * 64,
                }
                for index, office in enumerate(
                    ["adversary", "referee", "human_steward"], start=1
                )
            ],
            "status": "complete",
        }
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "distinct humans"
        ):
            validate_review_receipt(receipt)


if __name__ == "__main__":
    unittest.main()
