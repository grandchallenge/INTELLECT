from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from grand_intellect.constitutional_authority import (
    ConstitutionalAuthorityError,
    _RECOVERY_PROTOCOLS,
    load_and_validate,
    validate_authority_schedule,
    validate_organization_2fa_evidence,
    validate_review_receipt,
    validate_staffing_transition_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_PATH = ROOT / "governance" / "constitutional_authority_schedule.json"
ACTIVE_RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-22dbfa0ea0e6.json"
)
TRANSITION_RECEIPT_PATH = (
    ROOT
    / "governance"
    / "reviews"
    / "GI-HUMAN-GOVERNANCE-TRANSITION-001-47b0d9e0e61a.json"
)
STALE_RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-cc007ca6fe04.json"
)
TWO_FACTOR_EVIDENCE_PATH = (
    ROOT / "governance" / "evidence" / "GCL-ORG-2FA-001.json"
)


class ConstitutionalAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.canonical = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(ACTIVE_RECEIPT_PATH.read_text(encoding="utf-8"))
        self.transition_receipt = json.loads(
            TRANSITION_RECEIPT_PATH.read_text(encoding="utf-8")
        )
        self.two_factor_evidence = json.loads(
            TWO_FACTOR_EVIDENCE_PATH.read_text(encoding="utf-8")
        )

    def proposed_schedule(self) -> dict[str, object]:
        proposed = copy.deepcopy(self.canonical)
        proposed["schema_version"] = "1.4.0"
        proposed["status"] = "proposed"
        proposed["staffing"] = {
            "mode": "steward_supervised_agents",
            "directive": {
                "identifier": "GI-STEWARD-0001",
                "path": "governance/steward_directives/GI-STEWARD-0001.md",
                "status": "effective",
                "issued_at": "2026-07-29",
            },
            "human_steward": "fyremael",
            "external_human_review_required": False,
            "agent_staffed_offices": [
                "possibility_minder",
                "reality_minder",
                "purpose_minder",
                "continuity_minder",
                "capacity_minder",
                "axiomatist",
                "cartographer",
                "verifier",
                "adversary",
                "formalist",
                "steward",
                "grammarian",
                "composer",
                "amanuensis",
                "referee",
                "executor",
            ],
            "separation_controls": [
                "non_author_adversary",
                "distinct_agent_referee",
                "distinct_agent_sessions",
                "exact_revision_findings",
                "human_steward_reserved_authority",
            ],
        }
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

    def synthetic_transition_receipt(self) -> dict[str, object]:
        return {
            "schema_version": "1.1.0",
            "campaign_id": "GI-HUMAN-GOVERNANCE-TRANSITION-001",
            "staffing_mode": "steward_supervised_agents",
            "human_steward": "fyremael",
            "proposal_authors": ["fyremael"],
            "packet_sha256": "a" * 64,
            "subjects": [
                {
                    "repository": "grandchallenge/INTELLECT",
                    "pull_request": 54,
                    "head_sha": "b" * 40,
                }
            ],
            "signoffs": [
                {
                    "office": "adversary",
                    "reviewer": "agent-adversary-phase2",
                    "reviewer_kind": "agent",
                    "session_id": "phase2-adversary-session",
                    "authentication_id": "phase2-adversary-auth",
                    "attestation_record": "https://example.test/phase2-adversary",
                    "attestation_sha256": "c" * 64,
                },
                {
                    "office": "referee",
                    "reviewer": "agent-referee-phase2",
                    "reviewer_kind": "agent",
                    "session_id": "phase2-referee-session",
                    "authentication_id": "phase2-referee-auth",
                    "attestation_record": "https://example.test/phase2-referee",
                    "attestation_sha256": "d" * 64,
                },
                {
                    "office": "human_steward",
                    "reviewer": "fyremael",
                    "reviewer_kind": "human",
                    "session_id": None,
                    "authentication_id": "github-reaction-phase2",
                    "attestation_record": "https://example.test/phase2-steward",
                    "attestation_sha256": "e" * 64,
                },
            ],
            "recorded_at": "2026-08-09T06:00:00Z",
            "status": "complete",
        }

    def test_canonical_schedule_activates_exact_final_head_packet(self) -> None:
        validate_authority_schedule(
            self.canonical,
            review_receipt=self.receipt,
            staffing_transition_receipt=self.transition_receipt,
            organization_2fa_evidence=self.two_factor_evidence,
        )
        loaded = load_and_validate(SCHEDULE_PATH)
        activation = loaded["activation"]
        staffing = loaded["staffing"]

        self.assertEqual(loaded["status"], "active")
        self.assertEqual(loaded["schema_version"], "1.6.0")
        self.assertEqual(loaded["constitution"]["effective_version"], "1.2.0")
        self.assertEqual(loaded["amendment"]["status"], "effective")
        self.assertEqual(
            loaded["operating_standard"]["status_at_activation"], "candidate"
        )
        self.assertEqual(
            loaded["operating_standard"]["current_status_source"]["repository"],
            "grandchallenge/gcl-standards",
        )
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
        self.assertEqual(
            staffing["mode"], "streamlined_multi_role_agent_staffing"
        )
        self.assertEqual(staffing["directive"]["identifier"], "GI-STEWARD-0003")
        self.assertEqual(staffing["ordinary_human_steward"], "fyremael")
        self.assertEqual(staffing["recovery_owner"], "jimsteeg")
        self.assertEqual(staffing["mandatory_routine_reviewers"], [])
        self.assertEqual(staffing["human_actions_per_governed_decision_target"], 1)
        self.assertEqual(
            staffing["supersession"]["review_packet_sha256"],
            "47b0d9e0e61a50b302c3470da9c27ef0b1f0a17453a955d15bd5fe81e0f13171",
        )
        self.assertEqual(
            staffing["supersession"]["review_receipt"],
            "governance/reviews/"
            "GI-HUMAN-GOVERNANCE-TRANSITION-001-47b0d9e0e61a.json",
        )
        self.assertEqual(
            staffing["supersession"]["reviewed_source_head"],
            "4948714275da49bc3c2933f460dedaea4d0ef3a5",
        )
        self.assertEqual(
            staffing["supersession"]["effective_at"], "2026-08-09T06:27:00Z"
        )

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

    def test_minimum_steady_state_staffing_accepts_only_exact_supersession(self) -> None:
        steady = copy.deepcopy(self.canonical)
        steady["schema_version"] = "1.5.0"
        steady["staffing"].update(
            {
                "mode": "minimum_steady_state_human_authorization",
                "directive": {
                    "identifier": "GI-STEWARD-0002",
                    "path": "governance/steward_directives/GI-STEWARD-0002.md",
                    "status": "effective",
                    "issued_at": "2026-08-09",
                },
                "ordinary_human_steward": "fyremael",
                "recovery_owner": "jimsteeg",
                "mandatory_routine_reviewers": [],
                "human_actions_per_governed_decision_target": 1,
                "authorization_action": "authenticated_role_bound_exact_packet_authorization",
                "recovery_protocols": copy.deepcopy(_RECOVERY_PROTOCOLS),
                "supersession": {
                    "operation_id": "GI-HUMAN-GOVERNANCE-TRANSITION-001",
                    "predecessor": "GI-STEWARD-0001",
                    "review_packet_sha256": "a" * 64,
                    "review_receipt": "governance/reviews/GI-HUMAN-GOVERNANCE-TRANSITION-001-aaaaaaaaaaaa.json",
                    "reviewed_source_head": "b" * 40,
                    "effective_at": "2026-08-09T06:00:00Z",
                    "rollback": "later_exact_human_steward_directive_required",
                    "grandfathering": "completed_decisions_retain_recorded_rules_inflight_packets_finish_or_restart",
                    "organization_2fa": {
                        "evidence_path": "governance/evidence/GCL-ORG-2FA-001.json",
                        "evidence_sha256": "dcf18dabdafe717045188cfed7d3a0ccbc59c44707296045d69d5736c9b55611",
                        "evidence_url": "https://github.com/grandchallenge/.github/issues/47#issuecomment-5229847460"
                    },
                },
            }
        )
        steady["staffing"]["separation_controls"] = [
            "non_author_adversary", "distinct_agent_referee",
            "distinct_agent_sessions", "exact_revision_findings",
            "human_steward_reserved_authority",
        ]
        transition_receipt = self.synthetic_transition_receipt()
        two_factor_evidence = json.loads(
            TWO_FACTOR_EVIDENCE_PATH.read_text(encoding="utf-8")
        )
        validate_authority_schedule(
            steady,
            review_receipt=self.receipt,
            staffing_transition_receipt=transition_receipt,
            organization_2fa_evidence=two_factor_evidence,
        )

        mutations = (
            ("recovery_owner", "fyremael"),
            ("mandatory_routine_reviewers", ["jimsteeg"]),
            ("human_actions_per_governed_decision_target", 2),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                broken = copy.deepcopy(steady)
                broken["staffing"][field] = value
                with self.assertRaisesRegex(
                    ConstitutionalAuthorityError, "exact supersession sequence"
                ):
                    validate_authority_schedule(
                        broken,
                        review_receipt=self.receipt,
                        staffing_transition_receipt=transition_receipt,
                        organization_2fa_evidence=two_factor_evidence,
                    )

        broken_receipt = copy.deepcopy(transition_receipt)
        broken_receipt["packet_sha256"] = "f" * 64
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "transition receipt binding drift"
        ):
            validate_authority_schedule(
                steady,
                review_receipt=self.receipt,
                staffing_transition_receipt=broken_receipt,
                organization_2fa_evidence=two_factor_evidence,
            )

        broken_evidence = copy.deepcopy(two_factor_evidence)
        broken_evidence["disabled_members"] = ["jimsteeg"]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "2FA evidence digest drift"
        ):
            validate_authority_schedule(
                steady,
                review_receipt=self.receipt,
                staffing_transition_receipt=transition_receipt,
                organization_2fa_evidence=broken_evidence,
            )

        validate_staffing_transition_receipt(transition_receipt)
        validate_organization_2fa_evidence(two_factor_evidence)

    def test_bootstrap_schedule_cannot_smuggle_steady_state_fields(self) -> None:
        broken = self.proposed_schedule()
        broken["staffing"]["recovery_owner"] = "jimsteeg"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "exact bootstrap staffing sequence"
        ):
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

    def test_activation_records_standard_as_candidate_at_activation(self) -> None:
        active, receipt = self.synthetic_active()
        self.assertEqual(
            active["operating_standard"]["status_at_activation"], "candidate"
        )
        validate_authority_schedule(active, review_receipt=receipt)

    def test_current_standard_status_cannot_be_asserted_by_intellect(self) -> None:
        broken = self.proposed_schedule()
        broken["operating_standard"]["status"] = "candidate"
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "current status must come from"
        ):
            validate_authority_schedule(broken)

    def test_current_status_source_cannot_move_authority_into_intellect(self) -> None:
        broken = self.proposed_schedule()
        broken["operating_standard"]["current_status_source"]["repository"] = (
            "grandchallenge/INTELLECT"
        )
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError, "subordinate gcl-standards projection"
        ):
            validate_authority_schedule(broken)

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
            validate_authority_schedule(
                self.canonical,
                review_receipt=stale,
                staffing_transition_receipt=self.transition_receipt,
                organization_2fa_evidence=self.two_factor_evidence,
            )

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
