from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-cc007ca6fe04.json"
)
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


class GIAmend0001ReceiptTests(unittest.TestCase):
    def receipt(self) -> dict[str, object]:
        value = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def test_exact_packet_and_path_identity(self) -> None:
        receipt = self.receipt()
        self.assertEqual(receipt["schema_version"], "1.1.0")
        self.assertEqual(receipt["campaign_id"], "GI-AMEND-0001")
        self.assertEqual(receipt["status"], "complete")
        self.assertEqual(
            receipt["packet_sha256"],
            "cc007ca6fe0437d5906d84beada789852ab048e398bfb15924e3516e4c0c9d79",
        )
        self.assertRegex(receipt["packet_sha256"], DIGEST_RE)
        self.assertEqual(RECEIPT_PATH.stem.rsplit("-", 1)[1], receipt["packet_sha256"][:12])

    def test_exact_subjects_are_bound(self) -> None:
        receipt = self.receipt()
        subjects = {item["repository"]: item for item in receipt["subjects"]}
        self.assertEqual(
            set(subjects),
            {"grandchallenge/INTELLECT", "grandchallenge/gcl-standards"},
        )
        self.assertEqual(subjects["grandchallenge/INTELLECT"]["pull_request"], 32)
        self.assertEqual(
            subjects["grandchallenge/INTELLECT"]["head_sha"],
            "e0bca408b1a846f73daed2bb8164e7f085d2fbe1",
        )
        self.assertEqual(subjects["grandchallenge/gcl-standards"]["pull_request"], 18)
        self.assertEqual(
            subjects["grandchallenge/gcl-standards"]["head_sha"],
            "fa90ffc2bd23a6b0c8e184c7da2dd6ef1174a4ee",
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
        self.assertEqual(adversary["reviewer_kind"], "agent")
        self.assertEqual(referee["reviewer_kind"], "agent")
        self.assertEqual(steward["reviewer_kind"], "human")
        self.assertNotEqual(adversary["reviewer"], referee["reviewer"])
        self.assertNotEqual(adversary["session_id"], referee["session_id"])
        self.assertNotIn(adversary["reviewer"], receipt["proposal_authors"])
        self.assertNotIn(referee["reviewer"], receipt["proposal_authors"])
        self.assertEqual(steward["reviewer"], "fyremael")
        self.assertEqual(steward["authentication_id"], "391888540")
        self.assertIsNone(steward["session_id"])

        expected_digests = {
            "adversary": "8c90a1059e4392ea15453256e02dd9883922f8d88d6610d10442865418d2b2bc",
            "referee": "6460765a79d5768929776f8f436fd4f280bdecbadc49b1d7ff500ea63e1ab841",
            "human_steward": "0dc5c527dc7b6c7230c7e5cca7dbd5e70d2015527ed780bf3a1512d447d3cef0",
        }
        for office, expected in expected_digests.items():
            self.assertEqual(signoffs[office]["attestation_sha256"], expected)
            self.assertRegex(signoffs[office]["attestation_sha256"], DIGEST_RE)

    def test_receipt_does_not_claim_activation(self) -> None:
        receipt = self.receipt()
        boundary = receipt["authority_boundary"]
        self.assertIn("does not merge or activate", boundary)
        serialized = json.dumps(receipt, sort_keys=True)
        for prohibited in (
            '"amendment_status": "effective"',
            '"decision_status": "accepted"',
            '"adoption_status": "active"',
        ):
            self.assertNotIn(prohibited, serialized)


if __name__ == "__main__":
    unittest.main()
