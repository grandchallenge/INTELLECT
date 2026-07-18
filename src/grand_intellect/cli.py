from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .constitution import Constitution
from .metrics import calculate_metrics
from .model import IntellectEvent, project
from .workspace import WorkPackageWorkspace


def _load_events(path: Path) -> list[IntellectEvent]:
    events: list[IntellectEvent] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                events.append(IntellectEvent.from_dict(value))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError(f"{path}:{line_number}: invalid event: {exc}") from exc
    return events


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intellect", description="Inspect Grand Intellect event ledgers"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser(
        "init", help="Create a governed work-package workspace"
    )
    init.add_argument("root", type=Path)
    init.add_argument("work_package_id")
    init.add_argument("--title", required=True)
    init.add_argument("--purpose", required=True)
    init.add_argument("--scope", required=True)
    init.add_argument("--criterion", action="append", required=True)
    init.add_argument("--constraint", action="append", default=[])
    init.add_argument("--stakeholder", action="append", default=[])

    status = subparsers.add_parser("status", help="Project a work package ledger")
    status.add_argument("ledger", type=Path)
    status.add_argument("work_package_id")
    status.add_argument("--pretty", action="store_true")

    gate = subparsers.add_parser("gate", help="Evaluate the current phase gate")
    gate.add_argument("ledger", type=Path)
    gate.add_argument("work_package_id")

    metrics = subparsers.add_parser(
        "metrics", help="Calculate work-package governance metrics"
    )
    metrics.add_argument("ledger", type=Path)
    metrics.add_argument("work_package_id")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            paths = WorkPackageWorkspace(args.root).initialize(
                work_package_id=args.work_package_id,
                title=args.title,
                purpose=args.purpose,
                scope=args.scope,
                acceptance_criteria=args.criterion,
                constraints=args.constraint,
                stakeholders=args.stakeholder,
            )
            print(
                json.dumps(
                    {"workspace": str(paths.root), "ledger": str(paths.ledger)},
                    sort_keys=True,
                )
            )
            return 0
        events = _load_events(args.ledger)
        state = project(args.work_package_id, events)
        if args.command == "status":
            payload = {
                "work_package_id": state.work_package_id,
                "phase": state.phase.value,
                "title": state.title,
                "alternatives": len(state.alternatives),
                "contacts": len(state.contacts),
                "reviews": len(state.reviews),
                "events": len(state.event_ids),
            }
            print(
                json.dumps(
                    payload,
                    indent=2 if args.pretty else None,
                    sort_keys=True,
                )
            )
            return 0
        if args.command == "gate":
            report = Constitution().evaluate(state)
            print(
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
            )
            return 0 if report.ready else 2
        if args.command == "metrics":
            print(
                json.dumps(
                    calculate_metrics(state).to_dict(), indent=2, sort_keys=True
                )
            )
            return 0
        raise AssertionError("unreachable")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
