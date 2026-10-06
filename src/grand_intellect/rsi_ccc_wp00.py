from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json

WORK_PACKAGE_ID = "RSI-CCC-WP00"
SCHEMA_VERSION = "0.1.0"
DOMAIN = tuple(range(16))
CONTEXT_ID = "parity16-fixed-context-v1"
KERNEL_ID = "rsi-ccc-fixed-kernel-v1"
MAX_SERIALIZED_BYTES = 4096
MAX_DECLARED_COST = 10_000

REJECTION_CODES = {
    "malformed",
    "stale_base",
    "artifact_identity_mismatch",
    "context_substitution",
    "trust_kernel_mutation",
    "resource_bound",
    "unsafe_candidate",
    "non_refinement",
    "non_improvement",
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: object) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def expected_answer(x: int) -> bool:
    return x % 2 == 0


@dataclass(frozen=True, slots=True)
class Candidate:
    candidate_id: str
    answers: tuple[bool | None, ...]
    declared_cost: int
    context_id: str = CONTEXT_ID
    kernel_id: str = KERNEL_ID

    def payload(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "answers": list(self.answers),
            "declared_cost": self.declared_cost,
            "context_id": self.context_id,
            "kernel_id": self.kernel_id,
        }

    @property
    def digest(self) -> str:
        return sha256_json(self.payload())

    @property
    def competence_domain(self) -> frozenset[int]:
        return frozenset(i for i, answer in enumerate(self.answers) if answer is not None)


@dataclass(frozen=True, slots=True)
class Proposal:
    base_digest: str
    candidate: Candidate
    candidate_digest: str
    context_id: str
    kernel_id: str
    mode: str

    def payload(self) -> dict[str, object]:
        return {
            "base_digest": self.base_digest,
            "candidate": self.candidate.payload(),
            "candidate_digest": self.candidate_digest,
            "context_id": self.context_id,
            "kernel_id": self.kernel_id,
            "mode": self.mode,
        }


@dataclass(frozen=True, slots=True)
class Decision:
    accepted: bool
    code: str
    detail: str


def _is_bool_or_none(value: object) -> bool:
    return value is None or isinstance(value, bool)


def candidate_from_raw(raw: object) -> Candidate | None:
    if not isinstance(raw, dict):
        return None
    required = {"candidate_id", "answers", "declared_cost", "context_id", "kernel_id"}
    if set(raw) != required:
        return None
    if not isinstance(raw["candidate_id"], str) or not raw["candidate_id"]:
        return None
    answers = raw["answers"]
    if not isinstance(answers, list) or not all(_is_bool_or_none(v) for v in answers):
        return None
    cost = raw["declared_cost"]
    if not isinstance(cost, int) or isinstance(cost, bool):
        return None
    if not isinstance(raw["context_id"], str) or not isinstance(raw["kernel_id"], str):
        return None
    return Candidate(
        candidate_id=raw["candidate_id"],
        answers=tuple(answers),
        declared_cost=cost,
        context_id=raw["context_id"],
        kernel_id=raw["kernel_id"],
    )


def proposal_from_raw(raw: object) -> Proposal | None:
    if not isinstance(raw, dict):
        return None
    required = {"base_digest", "candidate", "candidate_digest", "context_id", "kernel_id", "mode"}
    if set(raw) != required:
        return None
    if not all(
        isinstance(raw[k], str)
        for k in ("base_digest", "candidate_digest", "context_id", "kernel_id", "mode")
    ):
        return None
    candidate = candidate_from_raw(raw["candidate"])
    if candidate is None:
        return None
    return Proposal(
        base_digest=raw["base_digest"],
        candidate=candidate,
        candidate_digest=raw["candidate_digest"],
        context_id=raw["context_id"],
        kernel_id=raw["kernel_id"],
        mode=raw["mode"],
    )


def safe(candidate: Candidate) -> bool:
    if len(candidate.answers) != len(DOMAIN):
        return False
    for x, answer in enumerate(candidate.answers):
        if answer is not None and answer != expected_answer(x):
            return False
    return True


def refines(old: Candidate, new: Candidate) -> bool:
    if not safe(new):
        return False
    for x in old.competence_domain:
        if new.answers[x] != old.answers[x]:
            return False
    return old.competence_domain.issubset(new.competence_domain)


def denotationally_equal(old: Candidate, new: Candidate) -> bool:
    return old.answers == new.answers


def strictly_improves(old: Candidate, new: Candidate, mode: str) -> bool:
    if mode == "capability_extension":
        return old.competence_domain < new.competence_domain
    if mode == "semantics_preserving_optimization":
        return denotationally_equal(old, new) and new.declared_cost < old.declared_cost
    return False


def _resource_ok(candidate: Candidate, proposal_payload: dict[str, object]) -> bool:
    if len(candidate.answers) != len(DOMAIN):
        return False
    if candidate.declared_cost < 0 or candidate.declared_cost > MAX_DECLARED_COST:
        return False
    return len(canonical_json(proposal_payload).encode("utf-8")) <= MAX_SERIALIZED_BYTES


def check_proposal(old: Candidate, raw: object) -> Decision:
    proposal = proposal_from_raw(raw)
    if proposal is None:
        return Decision(False, "malformed", "proposal does not satisfy the exact bounded schema")

    if proposal.base_digest != old.digest:
        return Decision(False, "stale_base", "proposal is not bound to the admitted base artifact")

    if proposal.candidate_digest != proposal.candidate.digest:
        return Decision(False, "artifact_identity_mismatch", "candidate digest does not match candidate content")

    if proposal.context_id != CONTEXT_ID or proposal.candidate.context_id != CONTEXT_ID:
        return Decision(False, "context_substitution", "evaluation context is fixed by the trust kernel")

    if proposal.kernel_id != KERNEL_ID or proposal.candidate.kernel_id != KERNEL_ID:
        return Decision(False, "trust_kernel_mutation", "candidate attempts to substitute the fixed trust kernel")

    if not _resource_ok(proposal.candidate, proposal.payload()):
        return Decision(False, "resource_bound", "candidate exceeds fixed bounded-checker resources")

    if not safe(proposal.candidate):
        return Decision(False, "unsafe_candidate", "candidate returns an incorrect answer on the finite task domain")

    if not refines(old, proposal.candidate):
        return Decision(False, "non_refinement", "candidate does not preserve the admitted competence domain")

    if not strictly_improves(old, proposal.candidate, proposal.mode):
        return Decision(False, "non_improvement", "candidate does not satisfy the fixed improvement rule")

    return Decision(True, "accepted", proposal.mode)


def admit(old: Candidate, raw: object) -> Candidate:
    decision = check_proposal(old, raw)
    if not decision.accepted:
        return old
    proposal = proposal_from_raw(raw)
    assert proposal is not None
    return proposal.candidate


def make_proposal(old: Candidate, candidate: Candidate, mode: str) -> dict[str, object]:
    proposal = Proposal(
        base_digest=old.digest,
        candidate=candidate,
        candidate_digest=candidate.digest,
        context_id=CONTEXT_ID,
        kernel_id=KERNEL_ID,
        mode=mode,
    )
    return proposal.payload()


def baseline_candidate() -> Candidate:
    answers: list[bool | None] = [None] * len(DOMAIN)
    for x in range(4):
        answers[x] = expected_answer(x)
    return Candidate("baseline", tuple(answers), declared_cost=40)


def capability_candidate() -> Candidate:
    return Candidate(
        "capability-extension",
        tuple(expected_answer(x) for x in DOMAIN),
        declared_cost=40,
    )


def optimized_candidate() -> Candidate:
    return Candidate(
        "optimized-equivalent",
        tuple(expected_answer(x) for x in DOMAIN),
        declared_cost=10,
    )


def bounded_trace() -> tuple[Candidate, ...]:
    s0 = baseline_candidate()
    p1 = make_proposal(s0, capability_candidate(), "capability_extension")
    s1 = admit(s0, p1)
    p2 = make_proposal(s1, optimized_candidate(), "semantics_preserving_optimization")
    s2 = admit(s1, p2)
    return (s0, s1, s2)
