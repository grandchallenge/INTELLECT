from __future__ import annotations

from hashlib import sha1
import json
from pathlib import Path
import unittest

from grand_intellect.rsi_ccc_wp00 import sha256_json
from grand_intellect.rsi_ccc_wp00_m2_ledger import (
    generated_trust_receipt_ledger,
    replay_trust_receipt_ledger,
)
from grand_intellect.rsi_ccc_wp00_m2_receipts import (
    CHECKER_DIGEST,
    EVALUATION_CONTEXT_DIGEST,
    KERNEL_DIGEST,
    POLICY_DIGEST,
    RESOURCE_ENVELOPE_DIGEST,
    generated_strong_sequence_summary,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "m2_trust_receipts.json"
MANIFEST_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "manifest.json"
LEAN_RECEIPTS_PATH = ROOT / "lean" / "RSICCCM2Receipts.lean"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


class RsiCccWp00M2ReceiptTests(unittest.TestCase):
    def load_ledger(self) -> dict[str, object]:
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    def test_ledger_is_exact_frozen_checker_replay(self) -> None:
        ledger = self.load_ledger()
        self.assertEqual(ledger, generated_trust_receipt_ledger())
        replay = replay_trust_receipt_ledger(ledger)
        self.assertEqual(replay.receipt_count, 15)
        self.assertEqual(
            replay.genesis_digest,
            "6981d788da4f47be73c17d7cd52686eb3eb0491089b4e55f59a189361463d834",
        )
        self.assertEqual(
            replay.receipt_chain_digest,
            "980a63cd95fe091b756e583da2970c5bf233576c5ea8da57c024d83bbe11393b",
        )
        self.assertEqual(
            replay.event_chain_digest,
            "da24637752e285b39e56c39f4a435e9d4b61be44adad813190a1247f9a52d10e",
        )

    def test_each_receipt_recomputes_and_keeps_trust_identities_fixed(self) -> None:
        ledger = self.load_ledger()
        previous = ledger["genesis_digest"]

        for receipt in ledger["receipts"]:
            self.assertEqual(receipt["previous_receipt_digest"], previous)
            self.assertEqual(receipt["checker_digest"], CHECKER_DIGEST)
            self.assertEqual(receipt["policy_digest"], POLICY_DIGEST)
            self.assertEqual(
                receipt["evaluation_context_digest"], EVALUATION_CONTEXT_DIGEST
            )
            self.assertEqual(receipt["kernel_digest"], KERNEL_DIGEST)
            self.assertEqual(
                receipt["resource_envelope_digest"], RESOURCE_ENVELOPE_DIGEST
            )

            body = dict(receipt)
            retained = body.pop("receipt_digest")
            self.assertEqual(sha256_json(body), retained)
            previous = retained

        self.assertEqual(previous, ledger["receipt_chain_digest"])

    def test_each_certificate_digest_recomputes_from_event_decision(self) -> None:
        ledger = self.load_ledger()
        strong = generated_strong_sequence_summary()
        strong_by_id = {event["event_id"]: event for event in strong["events"]}

        for receipt in ledger["receipts"]:
            event = strong_by_id[receipt["event_id"]]
            certificate_body = {
                "event_id": event["event_id"],
                "current_digest": event["current_digest"],
                "candidate_digest": event["candidate_digest"],
                "proposal_digest": event["proposal_digest"],
                "decision": event["expected_decision"],
                "next_state_digest": event["expected_state_digest_after"],
                "checker_digest": event["checker_digest"],
                "formal_object_sha256": event["formal_object_sha256"],
                "policy_digest": event["policy_digest"],
                "evaluation_context_digest": event["evaluation_context_digest"],
                "kernel_digest": event["kernel_digest"],
                "resource_envelope_digest": event["resource_envelope_digest"],
            }
            self.assertEqual(
                sha256_json(certificate_body), receipt["certificate_digest"]
            )

    def test_lean_binds_terminal_trust_receipt_identities(self) -> None:
        ledger = self.load_ledger()
        lean = LEAN_RECEIPTS_PATH.read_text(encoding="utf-8")
        expected = {
            ledger["genesis_digest"],
            ledger["receipt_chain_digest"],
            CHECKER_DIGEST.removeprefix("git-sha1:"),
            POLICY_DIGEST,
            EVALUATION_CONTEXT_DIGEST,
            KERNEL_DIGEST,
            RESOURCE_ENVELOPE_DIGEST,
        }
        for digest in expected:
            self.assertIn(digest, lean)

    def test_receipt_artifacts_are_manifest_bound_and_non_promotable(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertFalse(manifest["promotion_ready"])
        m2 = manifest["mechanization"]["m2_tranche"]
        self.assertEqual(
            m2["trust_receipt_chain_digest"],
            "980a63cd95fe091b756e583da2970c5bf233576c5ea8da57c024d83bbe11393b",
        )
        paths = {record["path"] for record in m2["evidence_artifacts"]}
        required = {
            "governance/rsi_ccc_wp00/m2_trust_receipts.json",
            "src/grand_intellect/rsi_ccc_wp00_m2_receipts.py",
            "src/grand_intellect/rsi_ccc_wp00_m2_ledger.py",
            "lean/RSICCCM2Receipts.lean",
            "tests/test_rsi_ccc_wp00_m2_receipts.py",
        }
        self.assertTrue(required.issubset(paths))

        for record in m2["evidence_artifacts"]:
            data = (ROOT / record["path"]).read_bytes()
            self.assertEqual(git_blob_sha(data), record["git_blob_sha"])


if __name__ == "__main__":
    unittest.main()
