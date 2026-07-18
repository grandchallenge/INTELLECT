from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable

from .constitution import Constitution, GateReport
from .fabric import AppendReceipt, CoordinationFabric
from .model import (
    Decision,
    Disposition,
    IntellectEvent,
    Office,
    Phase,
    ReviewStatus,
    WorkPackageState,
    next_phase,
    project,
)


class GateBlocked(RuntimeError):
    def __init__(self, report: GateReport) -> None:
        self.report = report
        super().__init__(
            f"transition {report.phase.value}->{report.target_phase.value} blocked: "
            + "; ".join(report.missing)
        )


class GrandIntellect:
    def __init__(
        self,
        fabric: CoordinationFabric,
        *,
        constitution: Constitution | None = None,
        require_authoritative_fabric: bool = False,
    ) -> None:
        if require_authoritative_fabric and not fabric.authoritative:
            raise ValueError("authoritative deployment requires an AETHER-backed fabric")
        self.fabric = fabric
        self.constitution = constitution or Constitution()

    def state(self, work_package_id: str) -> WorkPackageState:
        return project(work_package_id, self.fabric.history(work_package_id))

    def charter(
        self,
        work_package_id: str,
        *,
        title: str,
        purpose: str,
        scope: str,
        acceptance_criteria: Iterable[str],
        constraints: Iterable[str] = (),
        stakeholders: Iterable[str] = (),
        actor: str = Office.HUMAN_STEWARD.value,
        idempotency_key: str | None = None,
    ) -> AppendReceipt:
        if self.fabric.history(work_package_id):
            raise ValueError(f"work package already exists: {work_package_id}")
        payload = {
            "title": _required(title, "title"),
            "purpose": _required(purpose, "purpose"),
            "scope": _required(scope, "scope"),
            "acceptance_criteria": _nonempty_list(
                acceptance_criteria, "acceptance_criteria"
            ),
            "constraints": [str(x) for x in constraints],
            "stakeholders": [str(x) for x in stakeholders],
        }
        return self._append(
            "work_package.chartered",
            work_package_id,
            actor,
            payload,
            idempotency_key=idempotency_key,
        )

    def register_alternative(
        self,
        work_package_id: str,
        *,
        alternative_id: str,
        summary: str,
        mechanism: str,
        assumptions: Iterable[str],
        discriminating_test: str,
        actor: str = Office.POSSIBILITY_MINDER.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.GENERATION)
        return self._append(
            "alternative.registered",
            work_package_id,
            actor,
            {
                "alternative_id": _required(alternative_id, "alternative_id"),
                "summary": _required(summary, "summary"),
                "mechanism": _required(mechanism, "mechanism"),
                "assumptions": _nonempty_list(assumptions, "assumptions"),
                "discriminating_test": _required(
                    discriminating_test, "discriminating_test"
                ),
            },
        )

    def record_specification(
        self,
        work_package_id: str,
        *,
        claims: Iterable[str],
        evaluation_contract: dict[str, Any],
        reversal_conditions: Iterable[str],
        interfaces: Iterable[str] = (),
        actor: str = Office.FORMALIST.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.SPECIFICATION)
        return self._append(
            "specification.recorded",
            work_package_id,
            actor,
            {
                "claims": _nonempty_list(claims, "claims"),
                "evaluation_contract": _nonempty_object(
                    evaluation_contract, "evaluation_contract"
                ),
                "reversal_conditions": _nonempty_list(
                    reversal_conditions, "reversal_conditions"
                ),
                "interfaces": [str(x) for x in interfaces],
            },
        )

    def record_realization(
        self,
        work_package_id: str,
        *,
        realization_id: str,
        artifact_refs: Iterable[str],
        verification_commands: Iterable[str],
        deviations: Iterable[str] = (),
        actor: str = Office.EXECUTOR.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.REALIZATION)
        return self._append(
            "realization.recorded",
            work_package_id,
            actor,
            {
                "realization_id": _required(realization_id, "realization_id"),
                "artifact_refs": _nonempty_list(artifact_refs, "artifact_refs"),
                "verification_commands": _nonempty_list(
                    verification_commands, "verification_commands"
                ),
                "deviations": [str(x) for x in deviations],
            },
        )

    def record_contact(
        self,
        work_package_id: str,
        *,
        contact_id: str,
        claim: str,
        method: str,
        outcome: str,
        uncertainty: str,
        could_disconfirm: bool,
        evidence_refs: Iterable[str] = (),
        actor: str = Office.REALITY_MINDER.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.CONFRONTATION)
        return self._append(
            "contact.recorded",
            work_package_id,
            actor,
            {
                "contact_id": _required(contact_id, "contact_id"),
                "claim": _required(claim, "claim"),
                "method": _required(method, "method"),
                "outcome": _required(outcome, "outcome"),
                "uncertainty": _required(uncertainty, "uncertainty"),
                "could_disconfirm": bool(could_disconfirm),
                "evidence_refs": [str(x) for x in evidence_refs],
            },
        )

    def record_judgment(
        self,
        work_package_id: str,
        *,
        decision: Decision,
        rationale: str,
        selected_alternative_ids: Iterable[str],
        tradeoffs: Iterable[str],
        reversal_conditions: Iterable[str],
        actor: str = Office.PURPOSE_MINDER.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.JUDGMENT)
        return self._append(
            "judgment.recorded",
            work_package_id,
            actor,
            {
                "decision": decision.value,
                "rationale": _required(rationale, "rationale"),
                "selected_alternative_ids": [
                    str(x) for x in selected_alternative_ids
                ],
                "tradeoffs": _nonempty_list(tradeoffs, "tradeoffs"),
                "reversal_conditions": _nonempty_list(
                    reversal_conditions, "reversal_conditions"
                ),
            },
        )

    def record_memory(
        self,
        work_package_id: str,
        *,
        knowledge: str,
        reasons: Iterable[str],
        scope: str,
        limitations: Iterable[str],
        retrieval_tags: Iterable[str],
        actor: str = Office.CONTINUITY_MINDER.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.INTEGRATION)
        return self._append(
            "memory.recorded",
            work_package_id,
            actor,
            {
                "knowledge": _required(knowledge, "knowledge"),
                "reasons": _nonempty_list(reasons, "reasons"),
                "scope": _required(scope, "scope"),
                "limitations": _nonempty_list(limitations, "limitations"),
                "retrieval_tags": _nonempty_list(retrieval_tags, "retrieval_tags"),
            },
        )

    def record_disposal(
        self,
        work_package_id: str,
        *,
        object_id: str,
        disposition: Disposition,
        reason: str,
        recovery_path: str | None = None,
        authorized_by: str | None = None,
        actor: str = Office.CAPACITY_MINDER.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.DISPOSAL)
        if disposition == Disposition.DELETED and not authorized_by:
            raise ValueError("deletion requires explicit authorization")
        return self._append(
            "disposal.recorded",
            work_package_id,
            actor,
            {
                "object_id": _required(object_id, "object_id"),
                "disposition": disposition.value,
                "reason": _required(reason, "reason"),
                "recovery_path": recovery_path,
                "authorized_by": authorized_by,
            },
        )

    def record_frontier(
        self,
        work_package_id: str,
        *,
        questions: Iterable[str],
        actor: str = Office.CARTOGRAPHER.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.DISPOSAL)
        return self._append(
            "frontier.recorded",
            work_package_id,
            actor,
            {"questions": _nonempty_list(questions, "questions")},
        )

    def submit_review(
        self,
        work_package_id: str,
        *,
        office: Office,
        status: ReviewStatus,
        obligations: Iterable[str],
        findings: Iterable[str] = (),
        evidence_refs: Iterable[str] = (),
        actor: str | None = None,
    ) -> AppendReceipt:
        state = self.state(work_package_id)
        return self._append(
            "review.submitted",
            work_package_id,
            actor or office.value,
            {
                "office": office.value,
                "phase": state.phase.value,
                "status": status.value,
                "obligations": _nonempty_list(obligations, "obligations"),
                "findings": [str(x) for x in findings],
                "evidence_refs": [str(x) for x in evidence_refs],
            },
        )

    def gate_report(self, work_package_id: str) -> GateReport:
        return self.constitution.evaluate(self.state(work_package_id))

    def advance(
        self,
        work_package_id: str,
        *,
        actor: str = Office.REFEREE.value,
    ) -> AppendReceipt:
        state = self.state(work_package_id)
        report = self.constitution.evaluate(state)
        if not report.ready:
            raise GateBlocked(report)
        target = next_phase(state.phase)
        if target != report.target_phase:
            raise RuntimeError("constitution and phase order disagree")
        return self._append(
            "phase.advanced",
            work_package_id,
            actor,
            {
                "from_phase": state.phase.value,
                "to_phase": report.target_phase.value,
                "satisfied": list(report.satisfied),
            },
        )

    def reopen(
        self,
        work_package_id: str,
        *,
        reason: str,
        actor: str = Office.HUMAN_STEWARD.value,
    ) -> AppendReceipt:
        self._require_phase(work_package_id, Phase.COMPLETE)
        return self._append(
            "phase.reopened",
            work_package_id,
            actor,
            {
                "from_phase": Phase.COMPLETE.value,
                "to_phase": Phase.GENERATION.value,
                "reason": _required(reason, "reason"),
            },
        )

    def export_state(self, work_package_id: str) -> dict[str, Any]:
        state = self.state(work_package_id)
        result = asdict(state)
        result["phase"] = state.phase.value
        result["reviews"] = [
            {
                **asdict(review),
                "office": review.office.value,
                "phase": review.phase.value,
                "status": review.status.value,
            }
            for review in state.reviews
        ]
        return result

    def _append(
        self,
        event_type: str,
        work_package_id: str,
        actor: str,
        payload: dict[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> AppendReceipt:
        event = IntellectEvent(
            event_type=event_type,
            work_package_id=_required(work_package_id, "work_package_id"),
            actor=_required(actor, "actor"),
            payload=payload,
            correlation_id=work_package_id,
            idempotency_key=idempotency_key,
        )
        return self.fabric.append([event])

    def _require_phase(self, work_package_id: str, expected: Phase) -> None:
        actual = self.state(work_package_id).phase
        if actual != expected:
            raise ValueError(
                f"operation requires phase {expected.value}; current phase is {actual.value}"
            )


def _required(value: str, name: str) -> str:
    normalized = str(value).strip()
    if not normalized:
        raise ValueError(f"{name} is required")
    return normalized


def _nonempty_list(values: Iterable[str], name: str) -> list[str]:
    result = [str(value).strip() for value in values if str(value).strip()]
    if not result:
        raise ValueError(f"{name} must contain at least one value")
    return result


def _nonempty_object(value: dict[str, Any], name: str) -> dict[str, Any]:
    if not value:
        raise ValueError(f"{name} must not be empty")
    return dict(value)
