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
ACTIVE_RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-22dbfa0ea0e6.json"
)
STALE_RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-cc007ca6fe04.json"
)


class ConstitutionalAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.canonical = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(ACTIVE_RECEIPT_PATH.read_text(encoding="utf-8"))

    def proposed_schedule(self) -> dict[str, object]:
        proposed = copy.deepcopy(self.canonical)
        proposed["status"] = "proposed"
        proposed["constitution"]["effective_version"] = "1.0.0"
        proposed["amendment"]["status"] = "proposed"
        proposed["activation"] = {
            "proposal_author_ids": [],
            "human_steward_approval": None,
            "independent_adversary_review": None,
            "independent_referee_review": None,
            "review_receipt": None,
            "intellect_commit": None,
            "standards_commit": None,
            "effective_at": None,
        }
        return proposed

    def synthetic_active(self) -> tuple[dict[str, object], dict[str, object]]:
        active = self.proposed_schedule()
        active["status"] = "active"
        active["constitution"]["effective_version"] = "1.1.0"
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
            "effective_at": "2026-08-03T10:00:00Z",
        }
        receipt = {
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
        return active, receipt

    def test_canonical_schedule_activates_exact_final_head_packet(self) -> None:
        validate_authority_schedule(self.canonical, review_receipt=self.receipt)
        loaded = load_and_validate(SCHEDULE_PATH)
        activation = loaded["activation"]

        self.assertEqual(loaded["status"], "active")
        self.assertEqual(loaded["constitution"]["effective_version"], "1.1.0")
        self.assertEqual(loaded["amendment"]["status"], "effective")
        self.assertEqual(loaded["operating_standard"]["status"], "candidate")
        self.assertEqual(activation["proposal_author_ids"], ["fyremael"])
        self.assertEqual(
            activation["review_receipt"]["packet_sha256"],
            "22dbfa0ea0e652161126dd4647477036b89e6c13ecbd9101cda60ce00e9f95c5",
        )
        self.assertEqual(
            activation["intellect_commit"],
            "f1f5c4459def29139240c67ca858126021d1f12f",
        )
        self.assertEqual(
            activation["standards_commit"],
            "fa90ffc2bd23a6b0c8e184c7da2dd6ef1174a4ee",
        )
        self.assertEqual(activation["effective_at"], "2026-08-03T10:00:00Z")

    def test_proposed_form_remains_valid_without_activation(self) -> None:
        proposed = self.proposed_schedule()
        validate_authority_schedule(proposed)
        self.assertEqual(proposed["status"], "proposed")
        self.assertIsNone(proposed["activation"]["human_steward_approval"])
        self.assertIsNone(proposed["activation"]["review_receipt"])

    def test_core_authority_boundaries_fail_closed(self) -> None:
        mutations = (
            ("commentary", "authority", "normative", "interpretive and nonbinding"),
            (
                "operating_standard",
                "registry_role",
                "constitutional_authority",
                "subordinate registry",
            ),
            (
                "github",
                "authority",
                "production_semantic_authority",
                "operational and evidentiary",
            ),
        )
        for section, key, value, message in mutations:
            with self.subTest(section=section):
                broken = self.proposed_schedule()
                broken[section][key] = value
                with self.assertRaisesRegex(ConstitutionalAuthorityError, message):
                    validate_authority_schedule(broken)

    def test_agent_staffing_roster_cannot_omit_an_office(self) -> None:
        broken = self.proposed_schedule()
        broken["staffing"]["agent_staffed_offices"].remove("adversary")
        with self.assertRaisesRegex(ConstitutionalAuthorityError, "staffing roster"):
            validate_authority_schedule(broken)

    def test_activation_requires_complete_separated_authority(self) -> None:
        broken = self.proposed_schedule()
        broken["status"] = "active"
        broken["amendment"]["status"] = "effective"
        broken["activation"]["proposal_author_ids"] = ["author"]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "human_steward_approval"
        ):
            validate_authority_schedule(broken)

    def test_activation_keeps_standard_candidate(self) -> None:
        active, receipt = self.synthetic_active()
        self.assertEqual(active["operating_standard"]["status"], "candidate")
        validate_authority_schedule(active, review_receipt=receipt)

    def test_activation_rejects_receipt_subject_author_and_session_drift(self) -> None:
        cases = (
            (
                "packet",
                lambda active: active["activation"]["review_receipt"].__setitem__(
                    "packet_sha256", "9" * 64
                ),
                "packet digest",
            ),
            (
                "subject",
                lambda active: active["activation"].__setitem__(
                    "standards_commit", "9" * 40
                ),
                "standards_commit",
            ),
            (
                "author",
                lambda active: active["activation"].__setitem__(
                    "proposal_author_ids", ["other-author"]
                ),
                "proposal authors drift",
            ),
            (
                "session",
                lambda active: active["activation"][
                    "independent_referee_review"
                ].__setitem__("session_id", "different-session"),
                "referee record",
            ),
        )
        for name, mutate, message in cases:
            with self.subTest(name=name):
                active, receipt = self.synthetic_active()
                mutate(active)
                with self.assertRaisesRegex(ConstitutionalAuthorityError, message):
                    validate_authority_schedule(active, review_receipt=receipt)

    def test_activation_rejects_unsafe_or_non_content_addressed_receipts(self) -> None:
        cases = (
            ("../other.json", "requires review_receipt"),
            ("governance/reviews/GI-AMEND-0001.json", "requires review_receipt"),
            (
                "governance/reviews/GI-AMEND-0001-bbbbbbbbbbbb.json",
                "packet digest prefix",
            ),
            (
                "governance/reviews/GI-AMEND-0001-AAAAAAAAAAAA.json",
                "requires review_receipt",
            ),
        )
        for record_ref, message in cases:
            with self.subTest(record_ref=record_ref):
                active, receipt = self.synthetic_active()
                active["activation"]["review_receipt"]["record_ref"] = record_ref
                with self.assertRaisesRegex(ConstitutionalAuthorityError, message):
                    validate_authority_schedule(active, review_receipt=receipt)

    def test_stale_prior_receipt_is_rejected_before_subject_reuse(self) -> None:
        stale = json.loads(STALE_RECEIPT_PATH.read_text(encoding="utf-8"))
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "packet digest mismatch"
        ):
            validate_authority_schedule(self.canonical, review_receipt=stale)

    def test_receipt_requires_exact_subjects_and_distinct_non_author_agents(self) -> None:
        validate_review_receipt(self.receipt)

        same_agent = copy.deepcopy(self.receipt)
        same_agent["signoffs"][1]["reviewer"] = same_agent["signoffs"][0][
            "reviewer"
        ]
        with self.assertRaisesRegex(ConstitutionalAuthorityError, "distinct agents"):
            validate_review_receipt(same_agent)

        author_agent = copy.deepcopy(self.receipt)
        author_agent["signoffs"][0]["reviewer"] = "fyremael"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "must not be a proposal author"
        ):
            validate_review_receipt(author_agent)

        incomplete = copy.deepcopy(self.receipt)
        incomplete["subjects"] = incomplete["subjects"][:1]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "exact INTELLECT and gcl-standards"
        ):
            validate_review_receipt(incomplete)

    def test_load_and_validate_reads_content_addressed_receipt(self) -> None:
        active, receipt = self.synthetic_active()
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
