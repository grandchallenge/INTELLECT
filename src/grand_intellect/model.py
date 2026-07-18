from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Mapping
from uuid import uuid4

JsonObject = dict[str, Any]


class Office(StrEnum):
    POSSIBILITY_MINDER = "possibility_minder"
    REALITY_MINDER = "reality_minder"
    PURPOSE_MINDER = "purpose_minder"
    CONTINUITY_MINDER = "continuity_minder"
    CAPACITY_MINDER = "capacity_minder"

    AXIOMATIST = "axiomatist"
    CARTOGRAPHER = "cartographer"
    VERIFIER = "verifier"
    ADVERSARY = "adversary"
    FORMALIST = "formalist"
    STEWARD = "steward"
    GRAMMARIAN = "grammarian"
    COMPOSER = "composer"
    AMANUENSIS = "amanuensis"
    REFEREE = "referee"

    EXECUTOR = "executor"
    HUMAN_STEWARD = "human_steward"


class Phase(StrEnum):
    CHARTER = "charter"
    GENERATION = "generation"
    SPECIFICATION = "specification"
    REALIZATION = "realization"
    CONFRONTATION = "confrontation"
    JUDGMENT = "judgment"
    INTEGRATION = "integration"
    DISPOSAL = "disposal"
    COMPLETE = "complete"


PHASE_ORDER: tuple[Phase, ...] = (
    Phase.CHARTER,
    Phase.GENERATION,
    Phase.SPECIFICATION,
    Phase.REALIZATION,
    Phase.CONFRONTATION,
    Phase.JUDGMENT,
    Phase.INTEGRATION,
    Phase.DISPOSAL,
    Phase.COMPLETE,
)


class ReviewStatus(StrEnum):
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    ABSTAINED = "abstained"


class Disposition(StrEnum):
    COMPRESSED = "compressed"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"
    INVALIDATED = "invalidated"
    ABANDONED = "abandoned"
    QUARANTINED = "quarantined"
    DELETED = "deleted"


class Decision(StrEnum):
    ACCEPT = "accept"
    REVISE = "revise"
    REJECT = "reject"
    DEFER = "defer"
    COMBINE = "combine"


@dataclass(frozen=True, slots=True)
class IntellectEvent:
    event_type: str
    work_package_id: str
    actor: str
    payload: JsonObject
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    correlation_id: str | None = None
    causation_id: str | None = None
    idempotency_key: str | None = None

    def to_dict(self) -> JsonObject:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "work_package_id": self.work_package_id,
            "actor": self.actor,
            "payload": dict(self.payload),
            "occurred_at": self.occurred_at,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "idempotency_key": self.idempotency_key,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "IntellectEvent":
        payload = value.get("payload")
        if not isinstance(payload, Mapping):
            raise ValueError("event payload must be an object")
        return cls(
            event_id=str(value["event_id"]),
            event_type=str(value["event_type"]),
            work_package_id=str(value["work_package_id"]),
            actor=str(value["actor"]),
            payload=dict(payload),
            occurred_at=str(value["occurred_at"]),
            correlation_id=_optional_str(value.get("correlation_id")),
            causation_id=_optional_str(value.get("causation_id")),
            idempotency_key=_optional_str(value.get("idempotency_key")),
        )


@dataclass(frozen=True, slots=True)
class Review:
    office: Office
    phase: Phase
    status: ReviewStatus
    obligations: tuple[str, ...]
    findings: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "Review":
        return cls(
            office=Office(str(payload["office"])),
            phase=Phase(str(payload["phase"])),
            status=ReviewStatus(str(payload["status"])),
            obligations=tuple(str(x) for x in payload.get("obligations", [])),
            findings=tuple(str(x) for x in payload.get("findings", [])),
            evidence_refs=tuple(str(x) for x in payload.get("evidence_refs", [])),
        )


@dataclass(slots=True)
class WorkPackageState:
    work_package_id: str
    phase: Phase = Phase.CHARTER
    title: str = ""
    purpose: str = ""
    scope: str = ""
    constraints: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    stakeholders: list[str] = field(default_factory=list)
    alternatives: list[JsonObject] = field(default_factory=list)
    specification: JsonObject | None = None
    realizations: list[JsonObject] = field(default_factory=list)
    contacts: list[JsonObject] = field(default_factory=list)
    judgment: JsonObject | None = None
    memory_records: list[JsonObject] = field(default_factory=list)
    disposal_records: list[JsonObject] = field(default_factory=list)
    residual_frontier: list[str] = field(default_factory=list)
    reviews: list[Review] = field(default_factory=list)
    transitions: list[JsonObject] = field(default_factory=list)
    event_ids: list[str] = field(default_factory=list)

    def review_for(self, phase: Phase, office: Office) -> Review | None:
        for review in reversed(self.reviews):
            if review.phase == phase and review.office == office:
                return review
        return None


def project(work_package_id: str, events: list[IntellectEvent]) -> WorkPackageState:
    state = WorkPackageState(work_package_id=work_package_id)
    for event in events:
        if event.work_package_id != work_package_id:
            continue
        state.event_ids.append(event.event_id)
        payload = event.payload
        match event.event_type:
            case "work_package.chartered":
                state.title = str(payload["title"])
                state.purpose = str(payload["purpose"])
                state.scope = str(payload["scope"])
                state.constraints = [str(x) for x in payload.get("constraints", [])]
                state.acceptance_criteria = [
                    str(x) for x in payload.get("acceptance_criteria", [])
                ]
                state.stakeholders = [str(x) for x in payload.get("stakeholders", [])]
            case "alternative.registered":
                state.alternatives.append(dict(payload))
            case "specification.recorded":
                state.specification = dict(payload)
            case "realization.recorded":
                state.realizations.append(dict(payload))
            case "contact.recorded":
                state.contacts.append(dict(payload))
            case "review.submitted":
                state.reviews.append(Review.from_payload(payload))
            case "judgment.recorded":
                state.judgment = dict(payload)
            case "memory.recorded":
                state.memory_records.append(dict(payload))
            case "disposal.recorded":
                state.disposal_records.append(dict(payload))
            case "frontier.recorded":
                state.residual_frontier = [str(x) for x in payload.get("questions", [])]
            case "phase.advanced":
                state.phase = Phase(str(payload["to_phase"]))
                state.transitions.append(dict(payload))
            case "phase.reopened":
                state.phase = Phase.GENERATION
                state.transitions.append(dict(payload))
            case _:
                raise ValueError(f"unsupported event type: {event.event_type}")
    return state


def next_phase(phase: Phase) -> Phase | None:
    index = PHASE_ORDER.index(phase)
    if index + 1 == len(PHASE_ORDER):
        return None
    return PHASE_ORDER[index + 1]


def _optional_str(value: Any) -> str | None:
    return None if value is None else str(value)
