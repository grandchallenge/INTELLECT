from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

SCHEMA_VERSION = "1.0.0"
MILESTONE = "M3-proposer-evidence-independence"

PUBLIC_OBJECTIVE: dict[str, object] = {
    "task": "parity16",
    "objective": "maximize_prefix_coverage_then_reduce_fixed_context_cost",
    "coverage_targets": [8, 12, 16],
    "optimization_cost_targets": {"8": 20, "16": 10},
    "claim_boundary": "bounded_proposer_only",
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: object) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


OBJECTIVE_DIGEST = sha256_json(PUBLIC_OBJECTIVE)


@dataclass(frozen=True, slots=True)
class ProposerPrivateState:
    proposer_id: str
    strategy_revision: str
    generation_counter: int

    def digest(self) -> str:
        return sha256_json(
            {
                "proposer_id": self.proposer_id,
                "strategy_revision": self.strategy_revision,
                "generation_counter": self.generation_counter,
            }
        )


def _parity_answer(x: int) -> bool:
    return x % 2 == 0


def _candidate_digest(candidate: dict[str, object]) -> str:
    return sha256_json(candidate)


def _prefix_coverage(answers: list[bool | None]) -> int:
    prefix = 0
    for answer in answers:
        if answer is None:
            break
        prefix += 1
    if any(answer is not None for answer in answers[prefix:]):
        raise ValueError("public state is not a contiguous prefix candidate")
    return prefix


def _candidate_id(prefix: int, cost: int) -> str:
    exact = {
        (8, 40): "m2-capability-0-7",
        (8, 20): "m2-optimized-0-7",
        (12, 20): "m2-capability-0-11",
        (16, 20): "m2-capability-0-15",
        (16, 10): "m2-optimized-0-15",
    }
    try:
        return exact[(prefix, cost)]
    except KeyError as exc:
        raise ValueError(f"no bounded M3 candidate identity for prefix={prefix}, cost={cost}") from exc


def _build_candidate(public_state: dict[str, object], prefix: int, cost: int) -> dict[str, object]:
    answers: list[bool | None] = [None] * 16
    for x in range(prefix):
        answers[x] = _parity_answer(x)
    candidate = {
        "candidate_id": _candidate_id(prefix, cost),
        "answers": answers,
        "declared_cost": cost,
        "context_id": public_state["context_id"],
        "kernel_id": public_state["kernel_id"],
    }
    return candidate


def _next_target(coverage: int, cost: int) -> tuple[int, int, str] | None:
    if coverage < 8:
        return (8, cost, "capability_extension")
    if coverage == 8 and cost > 20:
        return (8, 20, "semantics_preserving_optimization")
    if coverage < 12:
        return (12, cost, "capability_extension")
    if coverage < 16:
        return (16, cost, "capability_extension")
    if coverage == 16 and cost > 10:
        return (16, 10, "semantics_preserving_optimization")
    return None


def validate_public_state(public_state: object) -> dict[str, object]:
    if not isinstance(public_state, dict):
        raise ValueError("public state must be an object")
    required = {
        "candidate_id",
        "candidate_digest",
        "answers",
        "declared_cost",
        "context_id",
        "kernel_id",
        "objective_digest",
    }
    if set(public_state) != required:
        raise ValueError("public state does not satisfy the exact M3 proposer schema")
    answers = public_state["answers"]
    if not isinstance(answers, list) or len(answers) != 16:
        raise ValueError("public state answers must contain exactly 16 entries")
    if not all(answer is None or isinstance(answer, bool) for answer in answers):
        raise ValueError("public state answers contain an invalid value")
    if public_state["objective_digest"] != OBJECTIVE_DIGEST:
        raise ValueError("public objective digest mismatch")
    if not isinstance(public_state["declared_cost"], int):
        raise ValueError("public state declared cost must be an integer")
    return public_state


def generate_committed_envelope(
    public_state_raw: object,
    private_state: ProposerPrivateState,
) -> dict[str, object] | None:
    public_state = validate_public_state(public_state_raw)
    answers = public_state["answers"]
    assert isinstance(answers, list)
    coverage = _prefix_coverage(answers)
    cost = int(public_state["declared_cost"])
    target = _next_target(coverage, cost)
    if target is None:
        return None

    target_prefix, target_cost, mode = target
    candidate = _build_candidate(public_state, target_prefix, target_cost)
    proposal: dict[str, object] = {
        "base_digest": public_state["candidate_digest"],
        "candidate": candidate,
        "candidate_digest": _candidate_digest(candidate),
        "context_id": public_state["context_id"],
        "kernel_id": public_state["kernel_id"],
        "mode": mode,
    }

    envelope_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "proposer_id": private_state.proposer_id,
        "private_state_digest": private_state.digest(),
        "public_input_digest": sha256_json(public_state),
        "objective_digest": OBJECTIVE_DIGEST,
        "proposal": proposal,
        "proposal_digest": sha256_json(proposal),
    }
    envelope = dict(envelope_body)
    envelope["transcript_digest"] = sha256_json(envelope_body)
    return envelope


def clone_with_private_identity(
    envelope: dict[str, Any],
    private_state: ProposerPrivateState,
) -> dict[str, object]:
    body = dict(envelope)
    body.pop("transcript_digest", None)
    body["proposer_id"] = private_state.proposer_id
    body["private_state_digest"] = private_state.digest()
    body["transcript_digest"] = sha256_json(body)
    return body
