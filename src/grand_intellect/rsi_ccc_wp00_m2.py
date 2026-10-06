from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from grand_intellect.rsi_ccc_wp00 import (
    CONTEXT_ID,
    KERNEL_ID,
    MAX_DECLARED_COST,
    MAX_SERIALIZED_BYTES,
    Candidate,
    admit,
    baseline_candidate,
    canonical_json,
    check_proposal,
    expected_answer,
    sha256_json,
)

FROZEN_FORMAL_OBJECT_SHA256 = "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc"
FROZEN_FORMAL_OBJECT_GIT_BLOB = "8baee8d3a1f50a4d527afdc29747a0fa563451bb"
FROZEN_CHECKER_GIT_BLOB = "e4ad8cef6fdf514c2aad0dbac372b3a42f5e6dbb"
MILESTONE = "M2-compositional-guarded-replacement-sequence"


class SequenceReplayError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TrajectoryEventSpec:
    event_id: str
    scenario: str
    proposal: dict[str, object]
    expected_accepted: bool
    expected_code: str


@dataclass(frozen=True, slots=True)
class SequenceReplayResult:
    final_candidate_digest: str
    accepted_transition_count: int
    rejected_event_count: int
    event_chain_digest: str
    accepted_state_digests: tuple[str, ...]


def prefix_candidate(
    candidate_id: str,
    exclusive_stop: int,
    declared_cost: int,
    *,
    context_id: str = CONTEXT_ID,
    kernel_id: str = KERNEL_ID,
) -> Candidate:
    answers: list[bool | None] = [None] * 16
    for x in range(exclusive_stop):
        answers[x] = expected_answer(x)
    return Candidate(
        candidate_id,
        tuple(answers),
        declared_cost,
        context_id=context_id,
        kernel_id=kernel_id,
    )


def _proposal(
    old: Candidate,
    candidate: Candidate,
    mode: str,
    *,
    base_digest: str | None = None,
    context_id: str = CONTEXT_ID,
    kernel_id: str = KERNEL_ID,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "base_digest": base_digest or old.digest,
        "candidate": candidate.payload(),
        "candidate_digest": candidate.digest,
        "context_id": context_id,
        "kernel_id": kernel_id,
        "mode": mode,
    }
    if extra:
        payload.update(extra)
    return payload


def accepted_candidates() -> tuple[Candidate, ...]:
    return (
        baseline_candidate(),
        prefix_candidate("m2-capability-0-7", 8, 40),
        prefix_candidate("m2-optimized-0-7", 8, 20),
        prefix_candidate("m2-capability-0-11", 12, 20),
        prefix_candidate("m2-capability-0-15", 16, 20),
        prefix_candidate("m2-optimized-0-15", 16, 10),
    )


def build_trajectory() -> tuple[TrajectoryEventSpec, ...]:
    s0, s1, s2, s3, s4, s5 = accepted_candidates()

    unsafe = prefix_candidate("m2-unsafe-0-8", 9, 40)
    unsafe_answers = list(unsafe.answers)
    unsafe_answers[8] = not expected_answer(8)
    unsafe = Candidate(
        unsafe.candidate_id,
        tuple(unsafe_answers),
        unsafe.declared_cost,
        context_id=unsafe.context_id,
        kernel_id=unsafe.kernel_id,
    )

    context_drift = prefix_candidate(
        "m2-context-drift",
        16,
        20,
        context_id="parity16-drifted-context-v2",
    )
    kernel_drift = prefix_candidate(
        "m2-kernel-drift",
        16,
        20,
        kernel_id="rsi-ccc-mutated-kernel-v2",
    )
    resource_launder = prefix_candidate("m2-resource-launder", 16, 10_001)
    noop = prefix_candidate("m2-noop-full", 16, 20)

    return (
        TrajectoryEventSpec(
            "A1-capability-0-7",
            "accepted_capability",
            _proposal(s0, s1, "capability_extension"),
            True,
            "accepted",
        ),
        TrajectoryEventSpec(
            "R1-unsafe",
            "unsafe_candidate",
            _proposal(s1, unsafe, "capability_extension"),
            False,
            "unsafe_candidate",
        ),
        TrajectoryEventSpec(
            "A2-optimize-0-7",
            "accepted_optimization",
            _proposal(s1, s2, "semantics_preserving_optimization"),
            True,
            "accepted",
        ),
        TrajectoryEventSpec(
            "R2-stale-ancestry",
            "stale_ancestry",
            _proposal(s0, s3, "capability_extension"),
            False,
            "stale_base",
        ),
        TrajectoryEventSpec(
            "A3-capability-0-11",
            "accepted_capability",
            _proposal(s2, s3, "capability_extension"),
            True,
            "accepted",
        ),
        TrajectoryEventSpec(
            "R3-context-drift",
            "context_drift",
            _proposal(
                s3,
                context_drift,
                "capability_extension",
                context_id="parity16-drifted-context-v2",
            ),
            False,
            "context_substitution",
        ),
        TrajectoryEventSpec(
            "R4-trust-boundary-creep",
            "trust_boundary_creep",
            _proposal(s3, kernel_drift, "capability_extension"),
            False,
            "trust_kernel_mutation",
        ),
        TrajectoryEventSpec(
            "A4-capability-0-15",
            "accepted_capability",
            _proposal(s3, s4, "capability_extension"),
            True,
            "accepted",
        ),
        TrajectoryEventSpec(
            "R5-ratcheting-regression",
            "ratcheting_regression",
            _proposal(s4, s1, "capability_extension"),
            False,
            "non_refinement",
        ),
        TrajectoryEventSpec(
            "R6-metric-gaming",
            "metric_gaming",
            _proposal(
                s4,
                s5,
                "semantics_preserving_optimization",
                extra={"metric": {"name": "candidate-defined", "score": 0}},
            ),
            False,
            "malformed",
        ),
        TrajectoryEventSpec(
            "R7-resource-laundering",
            "resource_laundering",
            _proposal(s4, resource_launder, "semantics_preserving_optimization"),
            False,
            "resource_bound",
        ),
        TrajectoryEventSpec(
            "R8-no-op",
            "no_op_succession",
            _proposal(s4, noop, "semantics_preserving_optimization"),
            False,
            "non_improvement",
        ),
        TrajectoryEventSpec(
            "A5-optimize-0-15",
            "accepted_optimization",
            _proposal(s4, s5, "semantics_preserving_optimization"),
            True,
            "accepted",
        ),
        TrajectoryEventSpec(
            "R9-reused-old-proposal",
            "certificate_receipt_reuse",
            _proposal(s0, s1, "capability_extension"),
            False,
            "stale_base",
        ),
        TrajectoryEventSpec(
            "R10-oscillation",
            "cycling_oscillation",
            _proposal(s5, s4, "semantics_preserving_optimization"),
            False,
            "non_improvement",
        ),
    )


def _genesis_payload() -> dict[str, object]:
    initial = baseline_candidate()
    return {
        "candidate": initial.payload(),
        "candidate_digest": initial.digest,
        "checker_git_blob": FROZEN_CHECKER_GIT_BLOB,
        "context_id": CONTEXT_ID,
        "formal_object_git_blob": FROZEN_FORMAL_OBJECT_GIT_BLOB,
        "formal_object_sha256": FROZEN_FORMAL_OBJECT_SHA256,
        "kernel_id": KERNEL_ID,
        "max_declared_cost": MAX_DECLARED_COST,
        "max_serialized_bytes": MAX_SERIALIZED_BYTES,
    }


def generated_sequence_summary() -> dict[str, object]:
    current = baseline_candidate()
    genesis_payload = _genesis_payload()
    previous_event_digest = sha256_json(genesis_payload)
    event_records: list[dict[str, object]] = []
    accepted_state_digests: list[str] = []
    accepted_count = 0
    rejected_count = 0

    for spec in build_trajectory():
        decision = check_proposal(current, spec.proposal)
        if decision.accepted != spec.expected_accepted or decision.code != spec.expected_code:
            raise SequenceReplayError(
                f"unexpected checker decision for {spec.event_id}: "
                f"{decision.accepted}/{decision.code}"
            )

        if decision.accepted:
            current = admit(current, spec.proposal)
            accepted_count += 1
            accepted_state_digests.append(current.digest)
        else:
            rejected_count += 1

        body: dict[str, object] = {
            "event_id": spec.event_id,
            "scenario": spec.scenario,
            "previous_event_digest": previous_event_digest,
            "proposal_digest": sha256_json(spec.proposal),
            "serialized_bytes": len(canonical_json(spec.proposal).encode("utf-8")),
            "expected_decision": {
                "accepted": decision.accepted,
                "code": decision.code,
            },
            "expected_state_digest_after": current.digest,
        }
        event_digest = sha256_json(body)
        record = dict(body)
        record["event_digest"] = event_digest
        event_records.append(record)
        previous_event_digest = event_digest

    return {
        "accepted_transition_count": accepted_count,
        "checker": {
            "git_blob_sha": FROZEN_CHECKER_GIT_BLOB,
            "path": "src/grand_intellect/rsi_ccc_wp00.py",
        },
        "event_chain_digest": previous_event_digest,
        "events": event_records,
        "final_candidate_digest": current.digest,
        "fixed_context": {
            "context_id": CONTEXT_ID,
            "kernel_id": KERNEL_ID,
            "max_declared_cost": MAX_DECLARED_COST,
            "max_serialized_bytes": MAX_SERIALIZED_BYTES,
        },
        "formal_object": {
            "git_blob_sha": FROZEN_FORMAL_OBJECT_GIT_BLOB,
            "sha256": FROZEN_FORMAL_OBJECT_SHA256,
        },
        "genesis": {
            "candidate_digest": baseline_candidate().digest,
            "candidate_id": baseline_candidate().candidate_id,
            "genesis_digest": sha256_json(genesis_payload),
        },
        "milestone": MILESTONE,
        "promotion_ready": False,
        "rejected_event_count": rejected_count,
        "schema_version": "1.0.0",
        "work_package_id": "RSI-CCC-WP00",
    }


def replay_sequence_artifact(artifact: dict[str, Any]) -> SequenceReplayResult:
    expected = generated_sequence_summary()
    if artifact != expected:
        raise SequenceReplayError("sequence artifact does not match exact frozen-checker replay")

    accepted_state_digests = tuple(
        event["expected_state_digest_after"]
        for event in expected["events"]
        if event["expected_decision"]["accepted"]
    )
    return SequenceReplayResult(
        final_candidate_digest=str(expected["final_candidate_digest"]),
        accepted_transition_count=int(expected["accepted_transition_count"]),
        rejected_event_count=int(expected["rejected_event_count"]),
        event_chain_digest=str(expected["event_chain_digest"]),
        accepted_state_digests=accepted_state_digests,
    )
