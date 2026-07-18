from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .constitution import Constitution
from .engine import GrandIntellect
from .fabric import InMemoryFabric
from .model import IntellectEvent, project


@dataclass(frozen=True, slots=True)
class WorkspacePaths:
    root: Path
    ledger: Path
    review_ledger: Path
    status: Path
    gate_report: Path


class WorkPackageWorkspace:
    """Materializes a reviewable work-package artifact bundle.

    This is a local authoring aid. The JSONL ledger is not production authority;
    production workspaces must reconcile with or be generated from AETHER history.
    """

    def __init__(self, root: Path) -> None:
        self.paths = WorkspacePaths(
            root=root,
            ledger=root / "events.jsonl",
            review_ledger=root / "agent_review.yaml",
            status=root / "STATUS.json",
            gate_report=root / "GATE_REPORT.json",
        )

    def initialize(
        self,
        *,
        work_package_id: str,
        title: str,
        purpose: str,
        scope: str,
        acceptance_criteria: Iterable[str],
        constraints: Iterable[str] = (),
        stakeholders: Iterable[str] = (),
    ) -> WorkspacePaths:
        acceptance_criteria = list(acceptance_criteria)
        constraints = list(constraints)
        stakeholders = list(stakeholders)
        root = self.paths.root
        if root.exists() and any(root.iterdir()):
            raise FileExistsError(f"workspace is not empty: {root}")
        root.mkdir(parents=True, exist_ok=True)
        (root / "IMPLEMENTATION").mkdir(exist_ok=True)

        fabric = InMemoryFabric()
        system = GrandIntellect(fabric)
        system.charter(
            work_package_id,
            title=title,
            purpose=purpose,
            scope=scope,
            acceptance_criteria=acceptance_criteria,
            constraints=constraints,
            stakeholders=stakeholders,
            idempotency_key=f"charter:{work_package_id}",
        )
        events = fabric.history(work_package_id)
        self.paths.ledger.write_text(
            "".join(
                json.dumps(event.to_dict(), sort_keys=True) + "\n"
                for event in events
            ),
            encoding="utf-8",
        )
        self.paths.review_ledger.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "work_package_id": work_package_id,
                    "reviews": [],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "CHARTER.md").write_text(
            _charter_markdown(
                work_package_id,
                title,
                purpose,
                scope,
                stakeholders,
                constraints,
                acceptance_criteria,
            ),
            encoding="utf-8",
        )
        placeholders = {
            "ALTERNATIVES.md": "# Alternatives\n\nRecord materially distinct candidates, assumptions, and discriminating tests.\n",
            "SPEC.md": "# Specification\n\nRecord claims, interfaces, evaluation contract, and reversal conditions.\n",
            "CONTACT_RECORD.md": "# Contact Record\n\nRecord methods capable of disconfirmation, outcomes, uncertainty, and evidence.\n",
            "ADVERSARIAL_REVIEW.md": "# Adversarial Review\n\nRecord counterexamples, brittle regimes, exploit paths, and unresolved failures.\n",
            "JUDGMENT_RECORD.md": "# Judgment Record\n\nRecord decision, rationale, trade-offs, and reversal conditions.\n",
            "MEMORY_RECORD.md": "# Memory Record\n\nRecord retained knowledge, reasons, scope, limitations, and retrieval tags.\n",
            "DISPOSAL_RECORD.md": "# Disposal Record\n\nRecord disposition, reason, recovery path, and authorization.\n",
            "IMPLEMENTATION/README.md": "# Implementation\n\nPlace realized artifacts or stable references here.\n",
        }
        for relative, content in placeholders.items():
            (root / relative).write_text(content, encoding="utf-8")
        self.refresh(work_package_id)
        return self.paths

    def refresh(self, work_package_id: str) -> WorkspacePaths:
        events = _load_jsonl(self.paths.ledger)
        state = project(work_package_id, events)
        report = Constitution().evaluate(state)
        self.paths.status.write_text(
            json.dumps(
                {
                    "work_package_id": work_package_id,
                    "phase": state.phase.value,
                    "title": state.title,
                    "events": len(state.event_ids),
                    "alternatives": len(state.alternatives),
                    "contacts": len(state.contacts),
                    "reviews": len(state.reviews),
                    "authoritative": False,
                    "authority_note": (
                        "Local authoring projection; production truth must be "
                        "replayed from AETHER."
                    ),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        self.paths.gate_report.write_text(
            json.dumps(
                {
                    "phase": report.phase.value,
                    "target_phase": report.target_phase.value,
                    "ready": report.ready,
                    "satisfied": report.satisfied,
                    "missing": report.missing,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return self.paths


def _load_jsonl(path: Path) -> list[IntellectEvent]:
    events: list[IntellectEvent] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                events.append(IntellectEvent.from_dict(json.loads(line)))
    return events


def _charter_markdown(
    work_package_id: str,
    title: str,
    purpose: str,
    scope: str,
    stakeholders: list[str],
    constraints: list[str],
    acceptance_criteria: list[str],
) -> str:
    def bullets(values: list[str], fallback: str) -> str:
        return "\n".join(f"- {value}" for value in values) if values else f"- {fallback}"

    return f"""# {work_package_id} — {title}

## Purpose

{purpose}

## Scope

{scope}

## Stakeholders

{bullets(stakeholders, 'Not yet specified')}

## Constraints

{bullets(constraints, 'No additional constraints recorded')}

## Acceptance criteria

{bullets(acceptance_criteria, 'No criteria recorded')}

## Authority

This directory is a local authoring projection. A production work package is authoritative only when its events are committed to and replayed from AETHER.
"""
