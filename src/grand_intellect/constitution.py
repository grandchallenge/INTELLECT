from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from .model import Office, Phase, WorkPackageState


@dataclass(frozen=True, slots=True)
class GateReport:
    phase: Phase
    target_phase: Phase
    ready: bool
    satisfied: tuple[str, ...]
    missing: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Gate:
    phase: Phase
    target_phase: Phase
    required_reviews: Mapping[Office, frozenset[str]]
    checks: tuple[tuple[str, Callable[[WorkPackageState], bool]], ...]


class Constitution:
    """Executable constitution for phase transitions.

    It governs admission to the next phase. AETHER governs authoritative event
    persistence, replay, provenance, and semantic derivation in deployment.
    """

    def __init__(self) -> None:
        self._gates = {gate.phase: gate for gate in _default_gates()}

    def evaluate(self, state: WorkPackageState) -> GateReport:
        try:
            gate = self._gates[state.phase]
        except KeyError as exc:
            raise ValueError(f"phase {state.phase} has no outgoing gate") from exc

        satisfied: list[str] = []
        missing: list[str] = []
        for description, predicate in gate.checks:
            (satisfied if predicate(state) else missing).append(description)

        for office in sorted(gate.required_reviews, key=str):
            review = state.review_for(state.phase, office)
            required = gate.required_reviews[office]
            supplied = set(review.obligations) if review is not None else set()
            absent = sorted(required - supplied)
            if review is not None and review.status.value == "approved" and not absent:
                satisfied.append(f"approved review: {office.value}")
                satisfied.extend(
                    f"obligation: {office.value}/{obligation}"
                    for obligation in sorted(required)
                )
            else:
                missing.append(f"approved review: {office.value}")
                missing.extend(
                    f"obligation: {office.value}/{obligation}" for obligation in absent
                )

        return GateReport(
            phase=gate.phase,
            target_phase=gate.target_phase,
            ready=not missing,
            satisfied=tuple(satisfied),
            missing=tuple(missing),
        )

    def required_offices(self, phase: Phase) -> frozenset[Office]:
        return frozenset(self._gates[phase].required_reviews)

    def required_obligations(self, phase: Phase, office: Office) -> frozenset[str]:
        return self._gates[phase].required_reviews[office]


def _default_gates() -> tuple[Gate, ...]:
    return (
        Gate(
            phase=Phase.CHARTER,
            target_phase=Phase.GENERATION,
            required_reviews={
                Office.PURPOSE_MINDER: frozenset(
                    {"purpose.explicit", "purpose.stakeholders_legible"}
                ),
                Office.AXIOMATIST: frozenset({"axioms.exposed"}),
                Office.STEWARD: frozenset({"stewardship.proportionate"}),
                Office.REFEREE: frozenset({"referee.acceptance_testable"}),
            },
            checks=(
                ("charter title", lambda s: bool(s.title.strip())),
                ("explicit purpose", lambda s: bool(s.purpose.strip())),
                ("bounded scope", lambda s: bool(s.scope.strip())),
                ("acceptance criteria", lambda s: bool(s.acceptance_criteria)),
            ),
        ),
        Gate(
            phase=Phase.GENERATION,
            target_phase=Phase.SPECIFICATION,
            required_reviews={
                Office.POSSIBILITY_MINDER: frozenset(
                    {"alternatives.materially_distinct"}
                ),
                Office.CARTOGRAPHER: frozenset({"terrain.mapped"}),
                Office.COMPOSER: frozenset({"composition.common_frame"}),
            },
            checks=(
                ("at least two alternatives", lambda s: len(s.alternatives) >= 2),
                (
                    "every alternative has a discriminating test",
                    lambda s: bool(s.alternatives)
                    and all(
                        str(item.get("discriminating_test", "")).strip()
                        for item in s.alternatives
                    ),
                ),
                (
                    "alternatives declare assumptions",
                    lambda s: bool(s.alternatives)
                    and all(item.get("assumptions") for item in s.alternatives),
                ),
            ),
        ),
        Gate(
            phase=Phase.SPECIFICATION,
            target_phase=Phase.REALIZATION,
            required_reviews={
                Office.FORMALIST: frozenset({"claims.explicit"}),
                Office.GRAMMARIAN: frozenset({"language.semantic_consistency"}),
                Office.VERIFIER: frozenset({"evaluation.detects_failure"}),
            },
            checks=(
                ("specification exists", lambda s: s.specification is not None),
                (
                    "claims are explicit",
                    lambda s: bool((s.specification or {}).get("claims")),
                ),
                (
                    "evaluation contract is explicit",
                    lambda s: bool(
                        (s.specification or {}).get("evaluation_contract")
                    ),
                ),
                (
                    "reversal conditions are explicit",
                    lambda s: bool(
                        (s.specification or {}).get("reversal_conditions")
                    ),
                ),
            ),
        ),
        Gate(
            phase=Phase.REALIZATION,
            target_phase=Phase.CONFRONTATION,
            required_reviews={
                Office.EXECUTOR: frozenset({"artifact.exists"}),
                Office.COMPOSER: frozenset({"integration.coherent"}),
                Office.VERIFIER: frozenset({"verification.executable"}),
            },
            checks=(
                ("at least one realization", lambda s: bool(s.realizations)),
                (
                    "realizations identify artifacts",
                    lambda s: bool(s.realizations)
                    and all(item.get("artifact_refs") for item in s.realizations),
                ),
                (
                    "realizations define verification commands",
                    lambda s: bool(s.realizations)
                    and all(
                        item.get("verification_commands") for item in s.realizations
                    ),
                ),
            ),
        ),
        Gate(
            phase=Phase.CONFRONTATION,
            target_phase=Phase.JUDGMENT,
            required_reviews={
                Office.REALITY_MINDER: frozenset({"evidence.disconfirmable"}),
                Office.VERIFIER: frozenset({"evidence.method_correspondence"}),
                Office.ADVERSARY: frozenset({"adversary.failure_search"}),
            },
            checks=(
                ("at least one contact record", lambda s: bool(s.contacts)),
                (
                    "contact can disconfirm",
                    lambda s: any(
                        bool(item.get("could_disconfirm")) for item in s.contacts
                    ),
                ),
                (
                    "uncertainty is recorded",
                    lambda s: bool(s.contacts)
                    and all(
                        str(item.get("uncertainty", "")).strip()
                        for item in s.contacts
                    ),
                ),
            ),
        ),
        Gate(
            phase=Phase.JUDGMENT,
            target_phase=Phase.INTEGRATION,
            required_reviews={
                Office.PURPOSE_MINDER: frozenset({"judgment.purpose_aligned"}),
                Office.STEWARD: frozenset({"judgment.tradeoffs_acceptable"}),
                Office.REFEREE: frozenset({"referee.burden_met"}),
            },
            checks=(
                ("judgment exists", lambda s: s.judgment is not None),
                (
                    "judgment states rationale",
                    lambda s: bool((s.judgment or {}).get("rationale")),
                ),
                (
                    "judgment states trade-offs",
                    lambda s: bool((s.judgment or {}).get("tradeoffs")),
                ),
                (
                    "judgment states reversal conditions",
                    lambda s: bool((s.judgment or {}).get("reversal_conditions")),
                ),
            ),
        ),
        Gate(
            phase=Phase.INTEGRATION,
            target_phase=Phase.DISPOSAL,
            required_reviews={
                Office.CONTINUITY_MINDER: frozenset({"memory.reasons_preserved"}),
                Office.AMANUENSIS: frozenset({"ledger.complete"}),
                Office.COMPOSER: frozenset({"integration.coherent"}),
                Office.GRAMMARIAN: frozenset({"language.consistent"}),
            },
            checks=(
                ("memory record exists", lambda s: bool(s.memory_records)),
                (
                    "memory preserves reasons",
                    lambda s: bool(s.memory_records)
                    and all(item.get("reasons") for item in s.memory_records),
                ),
                (
                    "memory states scope and limitations",
                    lambda s: bool(s.memory_records)
                    and all(
                        item.get("scope") and item.get("limitations")
                        for item in s.memory_records
                    ),
                ),
            ),
        ),
        Gate(
            phase=Phase.DISPOSAL,
            target_phase=Phase.COMPLETE,
            required_reviews={
                Office.CAPACITY_MINDER: frozenset(
                    {"disposal.active_set_governed"}
                ),
                Office.AMANUENSIS: frozenset({"disposal.provenance_preserved"}),
                Office.STEWARD: frozenset({"disposal.proportionate"}),
            },
            checks=(
                ("disposal record exists", lambda s: bool(s.disposal_records)),
                (
                    "disposal has recovery or deletion authority",
                    lambda s: bool(s.disposal_records)
                    and all(
                        item.get("recovery_path") or item.get("authorized_by")
                        for item in s.disposal_records
                    ),
                ),
                ("residual frontier exists", lambda s: bool(s.residual_frontier)),
            ),
        ),
    )
