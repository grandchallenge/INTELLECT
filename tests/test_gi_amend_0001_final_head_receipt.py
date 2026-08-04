from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

from grand_intellect.constitutional_authority import (
    ConstitutionalAuthorityError,
    validate_review_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-22dbfa0ea0e6.json"
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


class GIAmend0001FinalHeadReceiptTests(unittest.TestCase):
    def receipt(self) -> dict[str, object]:
        value = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def test_receipt_is_valid_and_content_addressed(self) -> None:
        receipt = self.receipt()
        validate_review_receipt(receipt)
        self.assertEqual(receipt["schema_version"], "1.1.0")
        self.assertEqual(receipt["campaign_id"], "GI-AMEND-0001")
        self.assertEqual(receipt["status"], "complete")
        self.assertEqual(
            receipt["packet_sha256"],
            "22dbfa0ea0e652161126dd4647477036b89e6c13ecbd9101cda60ce00e9f95c5",
        )
        self.assertRegex(receipt["packet_sha256"], DIGEST_RE)
        self.assertEqual(
            RECEIPT_PATH.stem.rsplit("-", 1)[1],
            receipt["packet_sha256"][:12],
        )

    def test_final_subject_heads_are_exact(self) -> None:
        receipt = self.receipt()
        subjects = {item["repository"]: item for item in receipt["subjects"]}
        self.assertEqual(
            set(subjects),
            {"grandchallenge/INTELLECT", "grandchallenge/gcl-standards"},
        )
        self.assertEqual(
            subjects["grandchallenge/INTELLECT"],
            {
                "repository": "grandchallenge/INTELLECT",
                "pull_request": 32,
                "head_sha": "f1f5c4459def29139240c67ca858126021d1f12f",
            },
        )
        self.assertEqual(
            subjects["grandchallenge/gcl-standards"],
            {
                "repository": "grandchallenge/gcl-standards",
                "pull_request": 18,
                "head_sha": "fa90ffc2bd23a6b0c8e184c7da2dd6ef1174a4ee",
            },
        )
        for subject in subjects.values():
            self.assertRegex(subject["head_sha"], COMMIT_RE)

    def test_signoffs_are_separated_and_exact(self) -> None:
        receipt = self.receipt()
        self.assertEqual(receipt["human_steward"], "fyremael")
        self.assertEqual(receipt["proposal_authors"], ["fyremael"])
        signoffs = {item["office"]: item for item in receipt["signoffs"]}
        self.assertEqual(set(signoffs), {"adversary", "referee", "human_steward"})

        adversary = signoffs["adversary"]
        referee = signoffs["referee"]
        steward = signoffs["human_steward"]
        self.assertEqual(
            adversary["reviewer"],
            "openai-gpt-5.6-thinking-final-head-adversary",
        )
        self.assertEqual(
            referee["reviewer"],
            "openai-gpt-5.6-thinking-final-head-referee",
        )
        self.assertNotEqual(adversary["reviewer"], referee["reviewer"])
        self.assertNotEqual(adversary["session_id"], referee["session_id"])
        self.assertNotIn(adversary["reviewer"], receipt["proposal_authors"])
        self.assertNotIn(referee["reviewer"], receipt["proposal_authors"])
        self.assertEqual(steward["reviewer"], "fyremael")
        self.assertEqual(steward["authentication_id"], "391939851")
        self.assertEqual(
            steward["attestation_record"],
            "https://github.com/grandchallenge/INTELLECT/pull/32"
            "#issuecomment-5164721769",
        )
        self.assertIsNone(steward["session_id"])
        for signoff in signoffs.values():
            self.assertRegex(signoff["attestation_sha256"], DIGEST_RE)

    def test_mutated_agent_separation_fails_closed(self) -> None:
        receipt = self.receipt()
        mutated = copy.deepcopy(receipt)
        signoffs = {item["office"]: item for item in mutated["signoffs"]}
        signoffs["referee"]["reviewer"] = signoffs["adversary"]["reviewer"]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError,
            "Adversary and Referee must be distinct agents",
        ):
            validate_review_receipt(mutated)

    def test_receipt_does_not_claim_activation(self) -> None:
        receipt = self.receipt()
        self.assertIn("does not merge or activate", receipt["authority_boundary"])
        serialized = json.dumps(receipt, sort_keys=True)
        for prohibited in (
            '"amendment_status": "effective"',
            '"decision_status": "accepted"',
            '"adoption_status": "active"',
        ):
            self.assertNotIn(prohibited, serialized)


if __name__ == "__main__":
    unittest.main()
