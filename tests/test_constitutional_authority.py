from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from grand_intellect.constitutional_authority import (
    ConstitutionalAuthorityError,
    load_and_validate,
    validate_authority_schedule,
    validate_review_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_PATH = ROOT / "governance" / "constitutional_authority_schedule.json"


class ConstitutionalAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))

    def active_schedule(self) -> dict[str, object]:
        active = copy.deepcopy(self.schedule)
        active["status"] = "active"
        active["amendment"]["status"] = "effective"
        active["activation"] = {
            "proposal_author_ids": ["author"],
            "human_steward_approval": {
                "status": "approved",
                "record_ref": "https://example.test/steward",
                "reviewer_kind": "human",
                "reviewer_id": "fyremael",
            },
            "independent_adversary_review": {
                "status": "approved",
                "record_ref": "https://example.test/adversary",
                "reviewer_kind": "agent",
                "reviewer_id": "agent-adversary",
                "session_id": "session-adversary",
            },
            "independent_referee_review": {
                "status": "approved",
                "record_ref": "https://example.test/referee",
                "reviewer_kind": "agent",
                "reviewer_id": "agent-referee",
                "session_id": "session-referee",
            },
            "review_receipt": {
                "campaign_id": "GI-AMEND-0001",
                "status": "complete",
                "record_ref": "governance/reviews/GI-AMEND-0001-aaaaaaaaaaaa.json",
                "packet_sha256": "a" * 64,
            },
            "intellect_commit": "b" * 40,
            "standards_commit": "c" * 40,
            "effective_at": "2026-08-03T00:00:00Z",
        }
        return active

    def review_receipt(self) -> dict[str, object]:
        return {
            "schema_version": "1.1.0",
            "campaign_id": "GI-AMEND-0001",
            "staffing_mode": "steward_supervised_agents",
            "human_steward": "fyremael",
            "proposal_authors": ["author"],
            "packet_sha256": "a" * 64,
            "subjects": [
                {
                    "repository": "grandchallenge/INTELLECT",
                    "pull_request": 32,
                    "head_sha": "b" * 40,
                },
                {
                    "repository": "grandchallenge/gcl-standards",
                    "pull_request": 18,
                    "head_sha": "c" * 40,
                },
            ],
            "signoffs": [
                {
                    "office": "adversary",
                    "reviewer": "agent-adversary",
                    "reviewer_kind": "agent",
                    "session_id": "session-adversary",
                    "authentication_id": "agent-session-adversary",
                    "attestation_record": "https://example.test/adversary",
                    "attestation_sha256": "d" * 64,
                },
                {
                    "office": "referee",
                    "reviewer": "agent-referee",
                    "reviewer_kind": "agent",
                    "session_id": "session-referee",
                    "authentication_id": "agent-session-referee",
                    "attestation_record": "https://example.test/referee",
                    "attestation_sha256": "e" * 64,
                },
                {
                    "office": "human_steward",
                    "reviewer": "fyremael",
                    "reviewer_kind": "human",
                    "session_id": None,
                    "authentication_id": "github-reaction-3",
                    "attestation_record": "https://example.test/steward",
                    "attestation_sha256": "f" * 64,
                },
            ],
            "recorded_at": "2026-08-03T00:00:00Z",
            "status": "complete",
        }

    def test_proposed_schedule_validates_without_claiming_activation(self) -> None:
        validate_authority_schedule(self.schedule)
        self.assertEqual(self.schedule["status"], "proposed")
        self.assertEqual(self.schedule["schema_version"], "1.3.0")
        self.assertEqual(
            self.schedule["staffing"]["mode"], "steward_supervised_agents"
        )
        self.assertFalse(
            self.schedule["staffing"]["external_human_review_required"]
        )
        self.assertEqual(
            len(self.schedule["staffing"]["agent_staffed_offices"]), 16
        )
        self.assertIn(
            "executor", self.schedule["staffing"]["agent_staffed_offices"]
        )
        self.assertIsNone(self.schedule["activation"]["human_steward_approval"])
        self.assertIsNone(self.schedule["activation"]["review_receipt"])

    def test_commentary_cannot_become_constitutional_law(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["commentary"]["authority"] = "normative"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "interpretive and nonbinding"
        ):
            validate_authority_schedule(broken)

    def test_agent_staffing_roster_cannot_omit_an_office(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["staffing"]["agent_staffed_offices"].remove("adversary")
        with self.assertRaisesRegex(ConstitutionalAuthorityError, "staffing roster"):
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

    def test_activation_fails_without_steward_and_agent_review(self) -> None:
        broken = copy.deepcopy(self.schedule)
        broken["status"] = "active"
        broken["amendment"]["status"] = "effective"
        broken["activation"]["proposal_author_ids"] = ["author"]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "human_steward_approval"
        ):
            validate_authority_schedule(broken)

    def test_amendment_activation_allows_reviewed_candidate_standard(self) -> None:
        active = self.active_schedule()
        self.assertEqual(active["operating_standard"]["status"], "candidate")
        validate_authority_schedule(active, review_receipt=self.review_receipt())

    def test_active_schedule_requires_effective_amendment(self) -> None:
        broken = self.active_schedule()
        broken["amendment"]["status"] = "proposed"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "amendment to be effective"
        ):
            validate_authority_schedule(broken, review_receipt=self.review_receipt())

    def test_active_schedule_requires_loaded_review_receipt(self) -> None:
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "loaded constitutional review receipt"
        ):
            validate_authority_schedule(self.active_schedule())

    def test_activation_rejects_packet_digest_substitution(self) -> None:
        broken = self.active_schedule()
        broken["activation"]["review_receipt"]["packet_sha256"] = "9" * 64
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "packet digest mismatch"
        ):
            validate_authority_schedule(broken, review_receipt=self.review_receipt())

    def test_activation_rejects_subject_commit_substitution(self) -> None:
        broken = self.active_schedule()
        broken["activation"]["standards_commit"] = "9" * 40
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "standards_commit"
        ):
            validate_authority_schedule(broken, review_receipt=self.review_receipt())

    def test_activation_rejects_proposal_author_drift(self) -> None:
        broken = self.active_schedule()
        broken["activation"]["proposal_author_ids"] = ["other-author"]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "proposal authors drift"
        ):
            validate_authority_schedule(broken, review_receipt=self.review_receipt())

    def test_activation_rejects_agent_session_drift(self) -> None:
        broken = self.active_schedule()
        broken["activation"]["independent_referee_review"]["session_id"] = (
            "different-session"
        )
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "referee record"
        ):
            validate_authority_schedule(broken, review_receipt=self.review_receipt())

    def test_activation_rejects_unexpected_receipt_reference(self) -> None:
        broken = self.active_schedule()
        broken["activation"]["review_receipt"]["record_ref"] = "../other.json"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "requires review_receipt"
        ):
            validate_authority_schedule(broken, review_receipt=self.review_receipt())

    def test_activation_rejects_fixed_receipt_filename(self) -> None:
    broken = self.active_schedule()
    broken["activation"]["review_receipt"]["record_ref"] = (
        "governance/reviews/GI-AMEND-0001.json"
    )
    with self.assertRaisesRegex(
        ConstitutionalAuthorityError, "requires review_receipt"
    ):
        validate_authority_schedule(
        broken, review_receipt=self.review_receipt()
        )

    def test_activation_rejects_receipt_path_digest_drift(self) -> None:
    broken = self.active_schedule()
    broken["activation"]["review_receipt"]["record_ref"] = (
        "governance/reviews/GI-AMEND-0001-bbbbbbbbbbbb.json"
    )
    with self.assertRaisesRegex(
        ConstitutionalAuthorityError, "packet digest prefix"
    ):
        validate_authority_schedule(
        broken, review_receipt=self.review_receipt()
        )

    def test_activation_rejects_malformed_receipt_suffix(self) -> None:
    broken = self.active_schedule()
    broken["activation"]["review_receipt"]["record_ref"] = (
        "governance/reviews/GI-AMEND-0001-AAAAAAAAAAAA.json"
    )
    with self.assertRaisesRegex(
        ConstitutionalAuthorityError, "requires review_receipt"
    ):
        validate_authority_schedule(
        broken, review_receipt=self.review_receipt()
        )

    def test_review_receipt_binds_exact_campaign_subjects_and_signoffs(self) -> None:
        validate_review_receipt(self.review_receipt())

    def test_review_receipt_rejects_wrong_campaign(self) -> None:
        broken = self.review_receipt()
        broken["campaign_id"] = "OTHER"
        with self.assertRaisesRegex(ConstitutionalAuthorityError, "wrong campaign"):
            validate_review_receipt(broken)

    def test_review_receipt_rejects_incomplete_subject_set(self) -> None:
        broken = self.review_receipt()
        broken["subjects"] = broken["subjects"][:1]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "exact INTELLECT and gcl-standards"
        ):
            validate_review_receipt(broken)

    def test_same_agent_cannot_sign_adversary_and_referee(self) -> None:
        broken = self.review_receipt()
        broken["signoffs"][1]["reviewer"] = "agent-adversary"
        with self.assertRaisesRegex(ConstitutionalAuthorityError, "distinct agents"):
            validate_review_receipt(broken)

    def test_proposal_author_cannot_supply_agent_review(self) -> None:
        broken = self.review_receipt()
        broken["signoffs"][0]["reviewer"] = "author"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "must not be a proposal author"
        ):
            validate_review_receipt(broken)

    def test_load_and_validate_reads_content_addressed_receipt(self) -> None:
        active = self.active_schedule()
        receipt = self.review_receipt()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            governance = root / "governance"
            reviews = governance / "reviews"
            reviews.mkdir(parents=True)
            schedule_path = governance / "constitutional_authority_schedule.json"
            schedule_path.write_text(json.dumps(active), encoding="utf-8")
            (reviews / "GI-AMEND-0001-aaaaaaaaaaaa.json").write_text(
                json.dumps(receipt), encoding="utf-8"
            )
            loaded = load_and_validate(schedule_path)
            self.assertEqual(loaded["status"], "active")


if __name__ == "__main__":
    unittest.main()
