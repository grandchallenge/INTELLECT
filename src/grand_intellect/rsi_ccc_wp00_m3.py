from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from grand_intellect.rsi_ccc_wp00 import (
    Candidate,
    admit,
    baseline_candidate,
    check_proposal,
    sha256_json,
)
from grand_intellect.rsi_ccc_wp00_m2_receipts import (
    CHECKER_DIGEST,
    EVALUATION_CONTEXT_DIGEST,
    FROZEN_FORMAL_OBJECT_SHA256,
    KERNEL_DIGEST,
    POLICY_DIGEST,
    RESOURCE_ENVELOPE_DIGEST,
)
from grand_intellect.rsi_ccc_wp00_m3_proposer import (
    MILESTONE,
    OBJECTIVE_DIGEST,
    ProposerPrivateState,
    clone_with_private_identity,
    generate_committed_envelope,
)

SCHEMA_VERSION = "1.0.0"
ENVELOPE_KEYS = {
    "schema_version",
    "proposer_id",
    "private_state_digest",
    "public_input_digest",
    "objective_digest",
    "proposal",
    "proposal_digest",
    "transcript_digest",
}


class M3ReplayError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    accepted: bool
    code: str
    proposal_digest: str
    certificate_digest: str
    next_state: Candidate


@dataclass(frozen=True, slots=True)
class M3ReplayResult:
    accepted_transition_count: int
    final_candidate_digest: str
    transcript_chain_digest: str
    independent_certificate_chain_digest: str


def public_state_view(candidate: Candidate) -> dict[str, object]:
    return {
        "candidate_id": candidate.candidate_id,
        "candidate_digest": candidate.digest,
        "answers": list(candidate.answers),
        "declared_cost": candidate.declared_cost,
        "context_id": candidate.context_id,
        "kernel_id": candidate.kernel_id,
        "objective_digest": OBJECTIVE_DIGEST,
    }


def _invalid_result(old: Candidate, code: str, raw: object) -> EvaluationResult:
    proposal_digest = sha256_json(raw)
    certificate_body = {
        "current_digest": old.digest,
        "proposal_digest": proposal_digest,
        "decision": {"accepted": False, "code": code},
        "next_state_digest": old.digest,
        "checker_digest": CHECKER_DIGEST,
        "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        "policy_digest": POLICY_DIGEST,
        "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
        "kernel_digest": KERNEL_DIGEST,
        "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
    }
    return EvaluationResult(
        accepted=False,
        code=code,
        proposal_digest=proposal_digest,
        certificate_digest=sha256_json(certificate_body),
        next_state=old,
    )


def evaluate_committed_envelope(old: Candidate, raw: object) -> EvaluationResult:
    if not isinstance(raw, dict) or set(raw) != ENVELOPE_KEYS:
        return _invalid_result(old, "malformed_envelope", raw)

    body = dict(raw)
    transcript_digest = body.pop("transcript_digest")
    if not isinstance(transcript_digest, str) or transcript_digest != sha256_json(body):
        return _invalid_result(old, "transcript_mismatch", raw)

    if raw["objective_digest"] != OBJECTIVE_DIGEST:
        return _invalid_result(old, "objective_mismatch", raw)

    expected_public_digest = sha256_json(public_state_view(old))
    if raw["public_input_digest"] != expected_public_digest:
        return _invalid_result(old, "public_state_mismatch", raw)

    proposal = raw["proposal"]
    if raw["proposal_digest"] != sha256_json(proposal):
        return _invalid_result(old, "proposal_commitment_mismatch", raw)

    decision = check_proposal(old, proposal)
    next_state = admit(old, proposal) if decision.accepted else old
    proposal_digest = str(raw["proposal_digest"])

    certificate_body = {
        "current_digest": old.digest,
        "proposal_digest": proposal_digest,
        "decision": {"accepted": decision.accepted, "code": decision.code},
        "next_state_digest": next_state.digest,
        "checker_digest": CHECKER_DIGEST,
        "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        "policy_digest": POLICY_DIGEST,
        "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
        "kernel_digest": KERNEL_DIGEST,
        "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
    }
    return EvaluationResult(
        accepted=decision.accepted,
        code=decision.code,
        proposal_digest=proposal_digest,
        certificate_digest=sha256_json(certificate_body),
        next_state=next_state,
    )


def generated_m3_artifact() -> dict[str, object]:
    current = baseline_candidate()
    previous_transcript_receipt = sha256_json(
        {
            "milestone": MILESTONE,
            "genesis_candidate_digest": current.digest,
            "objective_digest": OBJECTIVE_DIGEST,
            "checker_digest": CHECKER_DIGEST,
            "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        }
    )
    previous_certificate = previous_transcript_receipt
    events: list[dict[str, object]] = []

    for generation_counter in range(8):
        private = ProposerPrivateState(
            proposer_id="bounded-search-proposer-A",
            strategy_revision="m3-prefix-cost-v1",
            generation_counter=generation_counter,
        )
        public = public_state_view(current)
        envelope = generate_committed_envelope(public, private)
        if envelope is None:
            break

        result = evaluate_committed_envelope(current, envelope)
        if not result.accepted:
            raise M3ReplayError(
                f"bounded proposer generated rejected step {generation_counter}: {result.code}"
            )

        receipt_body = {
            "event_index": generation_counter,
            "previous_transcript_receipt_digest": previous_transcript_receipt,
            "current_digest": current.digest,
            "proposer_id": envelope["proposer_id"],
            "private_state_digest": envelope["private_state_digest"],
            "public_input_digest": envelope["public_input_digest"],
            "objective_digest": OBJECTIVE_DIGEST,
            "transcript_digest": envelope["transcript_digest"],
            "proposal_digest": result.proposal_digest,
            "certificate_digest": result.certificate_digest,
            "previous_certificate_digest": previous_certificate,
            "next_state_digest": result.next_state.digest,
            "checker_digest": CHECKER_DIGEST,
            "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
            "policy_digest": POLICY_DIGEST,
            "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
            "kernel_digest": KERNEL_DIGEST,
            "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
        }
        receipt_digest = sha256_json(receipt_body)
        event = dict(receipt_body)
        event["receipt_digest"] = receipt_digest
        events.append(event)
        previous_transcript_receipt = receipt_digest
        previous_certificate = result.certificate_digest
        current = result.next_state

    if len(events) != 5:
        raise M3ReplayError(f"expected five accepted generated transitions, got {len(events)}")

    baseline = baseline_candidate()
    public0 = public_state_view(baseline)
    envelope_a = generate_committed_envelope(
        public0,
        ProposerPrivateState("bounded-search-proposer-A", "m3-prefix-cost-v1", 0),
    )
    if envelope_a is None:
        raise M3ReplayError("failed to generate independence witness proposal")
    envelope_b = clone_with_private_identity(
        envelope_a,
        ProposerPrivateState("bounded-search-proposer-B", "unrelated-private-revision", 991),
    )
    eval_a = evaluate_committed_envelope(baseline, envelope_a)
    eval_b = evaluate_committed_envelope(baseline, envelope_b)
    if (
        eval_a.accepted != eval_b.accepted
        or eval_a.code != eval_b.code
        or eval_a.proposal_digest != eval_b.proposal_digest
        or eval_a.certificate_digest != eval_b.certificate_digest
    ):
        raise M3ReplayError("proposer-private identity changed independent admission evidence")
    if envelope_a["transcript_digest"] == envelope_b["transcript_digest"]:
        raise M3ReplayError("independence witness did not vary proposer transcript identity")

    return {
        "schema_version": SCHEMA_VERSION,
        "work_package_id": "RSI-CCC-WP00",
        "milestone": MILESTONE,
        "promotion_ready": False,
        "genesis_candidate_digest": baseline_candidate().digest,
        "objective_digest": OBJECTIVE_DIGEST,
        "checker_digest": CHECKER_DIGEST,
        "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        "policy_digest": POLICY_DIGEST,
        "evaluation_context_digest": EVALUATION_CONTEXT_DIGEST,
        "kernel_digest": KERNEL_DIGEST,
        "resource_envelope_digest": RESOURCE_ENVELOPE_DIGEST,
        "accepted_transition_count": len(events),
        "events": events,
        "final_candidate_digest": current.digest,
        "transcript_chain_digest": previous_transcript_receipt,
        "independent_certificate_chain_digest": previous_certificate,
        "independence_witness": {
            "proposal_digest": eval_a.proposal_digest,
            "certificate_digest": eval_a.certificate_digest,
            "transcript_digest_a": envelope_a["transcript_digest"],
            "transcript_digest_b": envelope_b["transcript_digest"],
            "decision": {"accepted": eval_a.accepted, "code": eval_a.code},
        },
    }


def replay_m3_artifact(artifact: dict[str, Any]) -> M3ReplayResult:
    expected = generated_m3_artifact()
    if artifact != expected:
        raise M3ReplayError("M3 artifact does not match exact proposer/evaluator replay")
    return M3ReplayResult(
        accepted_transition_count=int(expected["accepted_transition_count"]),
        final_candidate_digest=str(expected["final_candidate_digest"]),
        transcript_chain_digest=str(expected["transcript_chain_digest"]),
        independent_certificate_chain_digest=str(
            expected["independent_certificate_chain_digest"]
        ),
    )
