from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

from grand_intellect.constitutional_authority import (
    ConstitutionalAuthorityError,
    validate_staffing_transition_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = (
    ROOT
    / "governance"
    / "reviews"
    / "GI-HUMAN-GOVERNANCE-TRANSITION-001-47b0d9e0e61a.json"
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


class GIHumanGovernanceTransitionFinalReceiptTests(unittest.TestCase):
    def receipt(self) -> dict[str, object]:
        value = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def test_receipt_is_valid_and_content_addressed(self) -> None:
        receipt = self.receipt()
        validate_staffing_transition_receipt(receipt)
        self.assertEqual(receipt["schema_version"], "1.1.0")
        self.assertEqual(
            receipt["campaign_id"], "GI-HUMAN-GOVERNANCE-TRANSITION-001"
        )
        self.assertEqual(receipt["status"], "complete")
        self.assertEqual(
            receipt["packet_sha256"],
            "47b0d9e0e61a50b302c3470da9c27ef0b1f0a17453a955d15bd5fe81e0f13171",
        )
        self.assertRegex(receipt["packet_sha256"], DIGEST_RE)
        self.assertEqual(
            RECEIPT_PATH.stem.rsplit("-", 1)[1],
            receipt["packet_sha256"][:12],
        )

    def test_exact_reviewed_subject_is_bound(self) -> None:
        receipt = self.receipt()
        self.assertEqual(
            receipt["subjects"],
            [
                {
                    "repository": "grandchallenge/INTELLECT",
                    "pull_request": 54,
                    "head_sha": "4948714275da49bc3c2933f460dedaea4d0ef3a5",
                }
            ],
        )
        self.assertRegex(receipt["subjects"][0]["head_sha"], COMMIT_RE)

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
            "openai-gpt-5.6-sol-gi-human-governance-adversary-r4",
        )
        self.assertEqual(
            referee["reviewer"],
            "codex-gpt5-gi-human-governance-referee-r4",
        )
        self.assertNotEqual(adversary["reviewer"], referee["reviewer"])
        self.assertNotEqual(adversary["session_id"], referee["session_id"])
        self.assertNotIn(adversary["reviewer"], receipt["proposal_authors"])
        self.assertNotIn(referee["reviewer"], receipt["proposal_authors"])
        self.assertEqual(steward["reviewer"], "fyremael")
        self.assertEqual(steward["authentication_id"], "394993397")
        self.assertEqual(
            steward["attestation_record"],
            "https://github.com/grandchallenge/INTELLECT/pull/54"
            "#issuecomment-5230121570",
        )
        self.assertIsNone(steward["session_id"])
        for signoff in signoffs.values():
            self.assertRegex(signoff["attestation_sha256"], DIGEST_RE)

    def test_mutated_agent_separation_fails_closed(self) -> None:
        receipt = self.receipt()
        mutated = copy.deepcopy(receipt)
        signoffs = {item["office"]: item for item in mutated["signoffs"]}
        signoffs["referee"]["session_id"] = signoffs["adversary"]["session_id"]
        with self.assertRaisesRegex(
            ConstitutionalAuthorityError,
            "transition Adversary and Referee must be distinct",
        ):
            validate_staffing_transition_receipt(mutated)

    def test_receipt_does_not_claim_activation(self) -> None:
        receipt = self.receipt()
        self.assertIn("does not activate GI-STEWARD-0002", receipt["authority_boundary"])
        serialized = json.dumps(receipt, sort_keys=True)
        self.assertNotIn('"schema_version": "1.5.0"', serialized)
        self.assertNotIn('"directive": "GI-STEWARD-0002"', serialized)


if __name__ == "__main__":
    unittest.main()
