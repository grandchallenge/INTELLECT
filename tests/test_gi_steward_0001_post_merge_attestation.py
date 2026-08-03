from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATTESTATION = (
    ROOT
    / "governance"
    / "attestations"
    / "GI-STEWARD-0001-HUMAN-STEWARD-ROSTER-001.md"
)


class GIStweardRosterPostMergeAttestationTests(unittest.TestCase):
    def text(self) -> str:
        return ATTESTATION.read_text(encoding="utf-8")

    def test_exact_merge_identity_is_bound(self) -> None:
        text = self.text()
        self.assertIn("`grandchallenge/INTELLECT`", text)
        self.assertIn("`#35`", text)
        self.assertIn("`fac641298b7762d4e9a4e5faa98468af5b756463`", text)
        self.assertIn("`f479737bb1440505b21a00693c10fb96b244501a`", text)

    def test_both_stewards_and_one_acting_signer_are_recorded(self) -> None:
        text = self.text()
        self.assertIn("`fyremael` and `jimsteeg`", text)
        self.assertIn("names one acting Human Steward", text)
        self.assertIn(
            "one person may not count as both independent reviewer and acting Human Steward",
            text,
        )
        self.assertIn("The appointment is prospective", text)
        self.assertIn("does not retroactively relabel", text)

    def test_missing_review_is_not_concealed(self) -> None:
        text = self.text()
        self.assertIn("no mechanically attributable non-appointee `APPROVED` review", text)
        self.assertIn("unmet review condition", text)
        self.assertIn("Closure becomes effective only", text)
        self.assertIn("receives a mechanically attributable independent approval", text)

    def test_current_packet_remains_bound_to_existing_acting_steward(self) -> None:
        text = self.text()
        self.assertIn(
            "continues to name `fyremael` as its acting Human Steward",
            text,
        )
        self.assertIn("does not alter that packet", text)

    def test_no_authority_claim_is_promoted(self) -> None:
        text = self.text()
        for boundary in (
            "does not:",
            "create or admit a constitutional review receipt",
            "activate `GI-AMEND-0001`",
            "accept ADR-0001 or admit GCL-GHOS",
            "certify mathematics",
            "authorize novelty, priority, deployment, product, or commercial claims",
        ):
            self.assertIn(boundary, text)


if __name__ == "__main__":
    unittest.main()
