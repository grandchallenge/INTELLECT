from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from grand_intellect.rsi_ccc_wp00 import (
    CONTEXT_ID,
    DOMAIN,
    KERNEL_ID,
    MAX_DECLARED_COST,
    MAX_SERIALIZED_BYTES,
    admit,
    baseline_candidate,
    canonical_json,
    check_proposal,
    sha256_json,
)
from grand_intellect.rsi_ccc_wp00_m2 import (
    FROZEN_CHECKER_GIT_BLOB,
    FROZEN_FORMAL_OBJECT_GIT_BLOB,
    FROZEN_FORMAL_OBJECT_SHA256,
    MILESTONE,
    SequenceReplayError,
    build_trajectory,
)

SCHEMA_VERSION = "1.1.0"
CHECKER_DIGEST = f"git-sha1:{FROZEN_CHECKER_GIT_BLOB}"
FORMAL_OBJECT_GIT_BLOB = f"git-sha1:{FROZEN_FORMAL_OBJECT_GIT_BLOB}"

POLICY_DESCRIPTOR: dict[str, object] = {
    "checker_schema_version": "0.1.0",
    "admission_order": [
        "exact_schema",
        "base_identity",
        "candidate_identity",
        "fixed_context",
        "fixed_kernel",
        "resource_envelope",
        "safety",
        "semantic_refinement",
        "strict_improvement",
    ],
    "improvement_modes": [
        "capability_extension",
        "semantics_preserving_optimization",
    ],
}

EVALUATION_CONTEXT_DESCRIPTOR: dict[str, object] = {
    "context_id": CONTEXT_ID,
    "task": "parity",
    "domain": list(DOMAIN),
    "expected_answer": "x % 2 == 0",
}

RESOURCE_ENVELOPE_DESCRIPTOR: dict[str, object] = {
    "max_serialized_bytes": MAX_SERIALIZED_BYTES,
    "max_declared_cost": MAX_DECLARED_COST,
}

KERNEL_DESCRIPTOR: dict[str, object] = {
    "kernel_id": KERNEL_ID,
    "checker_digest": CHECKER_DIGEST,
    "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
    "self_replacement_allowed": False,
}

POLICY_DIGEST = sha256_json(POLICY_DESCRIPTOR)
EVALUATION_CONTEXT_DIGEST = sha256_json(EVALUATION_CONTEXT_DESCRIPTOR)
RESOURCE_ENVELOPE_DIGEST = sha256_json(RESOURCE_ENVELOPE_DESCRIPTOR)
KERNEL_DIGEST = sha256_json(KERNEL_DESCRIPTOR)


@dataclass(frozen=True, slots=True)
class StrongSequenceReplayResult:
    final_candidate_digest: str
    accepted_transition_count: int
    rejected_event_count: int
    event_chain_digest: str
    genesis_digest: str
    accepted_state_digests: tuple[str, ...]


def trust_bindings() -> dict[str, object]:
    return {
        "checker_digest": CHECKER_DIGEST,
        "formal_object_git_blob": FORMAL_OBJECT_GIT_BLOB,
        "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        "policy": {
            "descriptor": POLICY_DESCRIPTOR,
            "digest": POLICY_DIGEST,
        },
        "evaluation_context": {
            "descriptor": EVALUATION_CONTEXT_DESCRIPTOR,
            "digest": EVALUATION_CONTEXT_DIGEST,
        },
        "kernel": {
            "descriptor": KERNEL_DESCRIPTOR,
            "digest": KERNEL_DIGEST,
        },
        "resource_envelope": {
            "descriptor": RESOURCE_ENVELOPE_DESCRIPTOR,
            "digest": RESOURCE_ENVELOPE_DIGEST,
        },
    }


def _genesis_payload() -> dict[str, object]:
    initial = baseline_candidate()
    return {
        "candidate": initial.payload(),
        "candidate_digest": initial.digest,
        "checker_digest": CHECKER_DIGEST,
        "formal_object_git_blob": FORMAL_OBJECT_GIT_BLOB,
        "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        "policy_digest": POLICY_DIGEST,
        "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
        "kernel_digest": KERNEL_DIGEST,
        "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
    }


def _candidate_digest(proposal: dict[str, object]) -> str:
    value = proposal.get("candidate_digest")
    if not isinstance(value, str):
        raise SequenceReplayError("M2 event proposal lacks a string candidate digest")
    return value


def generated_strong_sequence_summary() -> dict[str, object]:
    current = baseline_candidate()
    genesis_payload = _genesis_payload()
    genesis_digest = sha256_json(genesis_payload)
    previous_event_digest = genesis_digest
    event_records: list[dict[str, object]] = []
    accepted_state_digests: list[str] = []
    accepted_count = 0
    rejected_count = 0

    for spec in build_trajectory():
        current_digest = current.digest
        proposal_digest = sha256_json(spec.proposal)
        candidate_digest = _candidate_digest(spec.proposal)
        serialized_bytes = len(canonical_json(spec.proposal).encode("utf-8"))
        decision = check_proposal(current, spec.proposal)

        if decision.accepted != spec.expected_accepted or decision.code != spec.expected_code:
            raise SequenceReplayError(
                f"unexpected checker decision for {spec.event_id}: "
                f"{decision.accepted}/{decision.code}"
            )

        next_state = admit(current, spec.proposal)
        next_state_digest = next_state.digest

        certificate_body: dict[str, object] = {
            "event_id": spec.event_id,
            "current_digest": current_digest,
            "candidate_digest": candidate_digest,
            "proposal_digest": proposal_digest,
            "decision": {
                "accepted": decision.accepted,
                "code": decision.code,
            },
            "next_state_digest": next_state_digest,
            "checker_digest": CHECKER_DIGEST,
            "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
            "policy_digest": POLICY_DIGEST,
            "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
            "kernel_digest": KERNEL_DIGEST,
            "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
        }
        certificate_digest = sha256_json(certificate_body)

        event_body: dict[str, object] = {
            "event_id": spec.event_id,
            "scenario": spec.scenario,
            "previous_event_digest": previous_event_digest,
            "current_digest": current_digest,
            "candidate_digest": candidate_digest,
            "proposal_digest": proposal_digest,
            "serialized_bytes": serialized_bytes,
            "checker_digest": CHECKER_DIGEST,
            "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
            "policy_digest": POLICY_DIGEST,
            "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
            "kernel_digest": KERNEL_DIGEST,
            "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
            "certificate_digest": certificate_digest,
            "expected_decision": {
                "accepted": decision.accepted,
                "code": decision.code,
            },
            "expected_state_digest_after": next_state_digest,
        }
        event_digest = sha256_json(event_body)
        record = dict(event_body)
        record["event_digest"] = event_digest
        event_records.append(record)
        previous_event_digest = event_digest

        if decision.accepted:
            accepted_count += 1
            accepted_state_digests.append(next_state_digest)
        else:
            rejected_count += 1
        current = next_state

    return {
        "schema_version": SCHEMA_VERSION,
        "work_package_id": "RSI-CCC-WP00",
        "milestone": MILESTONE,
        "promotion_ready": False,
        "trust_bindings": trust_bindings(),
        "genesis": {
            "candidate_digest": baseline_candidate().digest,
            "candidate_id": baseline_candidate().candidate_id,
            "genesis_digest": genesis_digest,
        },
        "events": event_records,
        "accepted_transition_count": accepted_count,
        "rejected_event_count": rejected_count,
        "final_candidate_digest": current.digest,
        "event_chain_digest": previous_event_digest,
    }


def replay_strong_sequence_artifact(
    artifact: dict[str, Any],
) -> StrongSequenceReplayResult:
    expected = generated_strong_sequence_summary()
    if artifact != expected:
        raise SequenceReplayError(
            "strong M2 sequence artifact does not match exact frozen-checker replay"
        )

    accepted_state_digests = tuple(
        event["expected_state_digest_after"]
        for event in expected["events"]
        if event["expected_decision"]["accepted"]
    )
    return StrongSequenceReplayResult(
        final_candidate_digest=str(expected["final_candidate_digest"]),
        accepted_transition_count=int(expected["accepted_transition_count"]),
        rejected_event_count=int(expected["rejected_event_count"]),
        event_chain_digest=str(expected["event_chain_digest"]),
        genesis_digest=str(expected["genesis"]["genesis_digest"]),
        accepted_state_digests=accepted_state_digests,
    )
