from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .engine import GrandIntellect
from .model import Office, Phase, ReviewStatus, WorkPackageState


@dataclass(frozen=True, slots=True)
class AgentContext:
    work_package: WorkPackageState
    office: Office
    phase: Phase
    mandate: str
    required_obligations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AgentReviewDecision:
    status: ReviewStatus
    obligations: tuple[str, ...]
    findings: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()


class OfficeAgent(Protocol):
    agent_id: str
    office: Office

    def review(self, context: AgentContext) -> AgentReviewDecision: ...


OFFICE_MANDATES: dict[Office, str] = {
    Office.POSSIBILITY_MINDER: "Preserve materially distinct alternatives before convergence.",
    Office.REALITY_MINDER: "Demand contact with evidence capable of changing the decision.",
    Office.PURPOSE_MINDER: "Make purpose, trade-offs, and reversal conditions explicit.",
    Office.CONTINUITY_MINDER: "Preserve reasons, scope, provenance, and inheritance context.",
    Office.CAPACITY_MINDER: "Retire what no longer earns active cognitive space.",
    Office.AXIOMATIST: "Expose primitives, assumptions, invariants, and boundaries.",
    Office.CARTOGRAPHER: "Map dependencies, precedents, routes, and unresolved territory.",
    Office.VERIFIER: "Check correctness, reproducibility, and claim-evidence correspondence.",
    Office.ADVERSARY: "Seek counterexamples, exploits, hidden assumptions, and brittle regimes.",
    Office.FORMALIST: "Convert intuition into explicit statements, contracts, and obligations.",
    Office.STEWARD: "Protect scope, resources, maintainability, and institutional purpose.",
    Office.GRAMMARIAN: "Preserve meaning across terminology, syntax, interfaces, and artifacts.",
    Office.COMPOSER: "Ensure valid parts form a coherent architecture or argument.",
    Office.AMANUENSIS: "Maintain lineage, ledgers, terminology, and review provenance.",
    Office.REFEREE: "Apply declared acceptance criteria and control closure.",
    Office.EXECUTOR: "Realize specified artifacts without silently changing the contract.",
    Office.HUMAN_STEWARD: "Retain accountable authority over irreversible and constitutional acts.",
}


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[Office, OfficeAgent] = {}
        self._agent_ids: set[str] = set()

    def register(self, agent: OfficeAgent) -> None:
        if agent.office in self._agents:
            raise ValueError(f"office already registered: {agent.office.value}")
        if agent.agent_id in self._agent_ids:
            raise ValueError(f"agent id already holds another office: {agent.agent_id}")
        self._agents[agent.office] = agent
        self._agent_ids.add(agent.agent_id)

    def get(self, office: Office) -> OfficeAgent:
        try:
            return self._agents[office]
        except KeyError as exc:
            raise KeyError(f"no agent registered for office: {office.value}") from exc


class AgentCouncil:
    """Dispatches constitution-required reviews; it cannot advance gates itself."""

    def __init__(self, system: GrandIntellect, registry: AgentRegistry) -> None:
        self.system = system
        self.registry = registry

    def conduct_gate_review(self, work_package_id: str) -> list[AgentReviewDecision]:
        state = self.system.state(work_package_id)
        decisions: list[AgentReviewDecision] = []
        for office in sorted(
            self.system.constitution.required_offices(state.phase),
            key=lambda item: item.value,
        ):
            agent = self.registry.get(office)
            context = AgentContext(
                work_package=state,
                office=office,
                phase=state.phase,
                mandate=OFFICE_MANDATES[office],
                required_obligations=tuple(
                    sorted(
                        self.system.constitution.required_obligations(
                            state.phase, office
                        )
                    )
                ),
            )
            decision = agent.review(context)
            if not decision.obligations:
                raise ValueError(
                    f"agent {agent.agent_id} returned no discharged obligations"
                )
            self.system.submit_review(
                work_package_id,
                office=office,
                status=decision.status,
                obligations=decision.obligations,
                findings=decision.findings,
                evidence_refs=decision.evidence_refs,
                actor=agent.agent_id,
            )
            decisions.append(decision)
        return decisions
