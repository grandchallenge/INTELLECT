from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .constitution import Constitution
from .model import Phase, ReviewStatus, WorkPackageState


@dataclass(frozen=True, slots=True)
class WorkPackageMetrics:
    work_package_id: str
    phase: str
    event_count: int
    transition_count: int
    reopening_count: int
    alternative_count: int
    contact_count: int
    disconfirmable_contact_ratio: float
    review_count: int
    changes_requested_count: int
    current_required_office_count: int
    current_satisfied_office_count: int
    current_review_coverage: float
    memory_record_count: int
    complete_memory_ratio: float
    disposal_record_count: int
    residual_frontier_count: int
    gate_ready: bool
    gate_target: str | None
    unresolved_gate_items: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def calculate_metrics(
    state: WorkPackageState, constitution: Constitution | None = None
) -> WorkPackageMetrics:
    constitution = constitution or Constitution()
    contacts = len(state.contacts)
    disconfirmable = sum(bool(item.get("could_disconfirm")) for item in state.contacts)
    memories = len(state.memory_records)
    complete_memories = sum(
        bool(item.get("reasons") and item.get("scope") and item.get("limitations"))
        for item in state.memory_records
    )
    latest_reviews = {}
    for review in state.reviews:
        if review.phase == state.phase:
            latest_reviews[review.office] = review

    if state.phase == Phase.COMPLETE:
        required_offices = frozenset()
        satisfied_offices = 0
        gate_ready = True
        gate_target = None
        unresolved: tuple[str, ...] = ()
    else:
        required_offices = constitution.required_offices(state.phase)
        satisfied_offices = 0
        for office in required_offices:
            review = latest_reviews.get(office)
            required = constitution.required_obligations(state.phase, office)
            if (
                review is not None
                and review.status == ReviewStatus.APPROVED
                and required.issubset(review.obligations)
            ):
                satisfied_offices += 1
        report = constitution.evaluate(state)
        gate_ready = report.ready
        gate_target = report.target_phase.value
        unresolved = report.missing

    required_count = len(required_offices)
    reopening_count = sum(
        item.get("from_phase") == Phase.COMPLETE.value
        and item.get("to_phase") == Phase.GENERATION.value
        for item in state.transitions
    )
    return WorkPackageMetrics(
        work_package_id=state.work_package_id,
        phase=state.phase.value,
        event_count=len(state.event_ids),
        transition_count=len(state.transitions) - reopening_count,
        reopening_count=reopening_count,
        alternative_count=len(state.alternatives),
        contact_count=contacts,
        disconfirmable_contact_ratio=(disconfirmable / contacts if contacts else 0.0),
        review_count=len(state.reviews),
        changes_requested_count=sum(
            review.status == ReviewStatus.CHANGES_REQUESTED for review in state.reviews
        ),
        current_required_office_count=required_count,
        current_satisfied_office_count=satisfied_offices,
        current_review_coverage=(
            satisfied_offices / required_count if required_count else 1.0
        ),
        memory_record_count=memories,
        complete_memory_ratio=(complete_memories / memories if memories else 0.0),
        disposal_record_count=len(state.disposal_records),
        residual_frontier_count=len(state.residual_frontier),
        gate_ready=gate_ready,
        gate_target=gate_target,
        unresolved_gate_items=unresolved,
    )
