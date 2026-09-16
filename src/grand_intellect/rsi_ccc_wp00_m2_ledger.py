from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from grand_intellect.rsi_ccc_wp00 import sha256_json
from grand_intellect.rsi_ccc_wp00_m2 import SequenceReplayError
from grand_intellect.rsi_ccc_wp00_m2_receipts import generated_strong_sequence_summary

SCHEMA_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class TrustReceiptReplayResult:
    genesis_digest: str
    receipt_chain_digest: str
    event_chain_digest: str
    receipt_count: int


def generated_trust_receipt_ledger() -> dict[str, object]:
    strong = generated_strong_sequence_summary()
    previous_receipt_digest = str(strong["genesis"]["genesis_digest"])
    receipts: list[dict[str, object]] = []

    retained_fields = (
        "event_id",
        "current_digest",
        "candidate_digest",
        "proposal_digest",
        "certificate_digest",
        "checker_digest",
        "formal_object_sha256",
        "policy_digest",
        "evaluation_context_digest",
        "kernel_digest",
        "resource_envelope_digest",
    )

    for event in strong["events"]:
        body: dict[str, object] = {
            "event_id": event["event_id"],
            "previous_receipt_digest": previous_receipt_digest,
        }
        for field in retained_fields[1:]:
            body[field] = event[field]

        receipt_digest = sha256_json(body)
        record = dict(body)
        record["receipt_digest"] = receipt_digest
        receipts.append(record)
        previous_receipt_digest = receipt_digest

    return {
        "schema_version": SCHEMA_VERSION,
        "work_package_id": strong["work_package_id"],
        "milestone": strong["milestone"],
        "trust_bindings": strong["trust_bindings"],
        "genesis_digest": strong["genesis"]["genesis_digest"],
        "receipts": receipts,
        "receipt_chain_digest": previous_receipt_digest,
        "event_chain_digest": "da24637752e285b39e56c39f4a435e9d4b61be44adad813190a1247f9a52d10e",
        "promotion_ready": False,
    }


def replay_trust_receipt_ledger(
    artifact: dict[str, Any],
) -> TrustReceiptReplayResult:
    expected = generated_trust_receipt_ledger()
    if artifact != expected:
        raise SequenceReplayError(
            "M2 trust-receipt ledger does not match exact frozen-checker replay"
        )

    return TrustReceiptReplayResult(
        genesis_digest=str(expected["genesis_digest"]),
        receipt_chain_digest=str(expected["receipt_chain_digest"]),
        event_chain_digest=str(expected["event_chain_digest"]),
        receipt_count=len(expected["receipts"]),
    )
