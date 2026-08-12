from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import jsonschema

from grand_intellect.council_motion import compile_motion


ROOT = Path(__file__).resolve().parents[1]
MATTER = ROOT / "governance/council_matters/GI-COUNCIL-PROXY-DELEGATION-SCHEDULE-001"
COMMITTEE = ROOT / "governance/committees/GI-PROXY-DELEGATION-COMMITTEE-001.json"
SCHEDULE = ROOT / "governance/committees/GI-PROXY-DELEGATION-COMMITTEE-001-SCHEDULE-001.json"
RECEIPT = ROOT / "governance/committees/GI-PROXY-DELEGATION-COMMITTEE-001-SCHEDULE-001-RECEIPT.json"
RECEIPT_SCHEMA = ROOT / "schemas/human_steward_schedule_receipt.schema.json"


def test_accelerated_schedule_disposition_matches_exact_compiler_readback() -> None:
    compiled = compile_motion(MATTER / "motion.json", MATTER / "reviews").to_dict()
    stored = json.loads((MATTER / "disposition.json").read_text(encoding="utf-8"))
    assert compiled == stored
    assert compiled["full_quorum"] is True
    assert compiled["unanimous"] is True
    assert compiled["procedural_disposition"] == "table_for_human_steward_disposition"


def test_acceleration_is_ratified_with_exact_future_opening() -> None:
    committee = json.loads(COMMITTEE.read_text(encoding="utf-8"))
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    assert committee["deadline"] == "2026-09-10T23:59:59Z"
    assert schedule["requested_duration"] == "PT72H"
    assert schedule["status"] == "ratified_scheduled"
    assert schedule["effective_at"] == "2026-08-12T09:00:00Z"
    assert schedule["deadline"] == "2026-08-15T09:00:00Z"
    assert schedule["authority"]["current_rules_remain_effective"] is True
    assert schedule["authority"]["may_create_live_proxy_authority"] is False


def test_authenticated_schedule_receipt_is_valid_and_exactly_72_hours() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        receipt,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )
    start = datetime.fromisoformat(receipt["schedule"]["effective_at"])
    deadline = datetime.fromisoformat(receipt["schedule"]["deadline"])
    assert (deadline - start).total_seconds() == 72 * 60 * 60
    assert [event["kind"] for event in receipt["authentication_events"]] == [
        "ratification",
        "opening",
    ]
    assert all(event["edited"] is False for event in receipt["authentication_events"])


def test_accelerated_scope_is_narrower_than_original_committee_limit() -> None:
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    assert schedule["scope"] == {
        "task_classes": 1,
        "repositories": 1,
        "live_proxy_acts": 0,
        "protected_integrations": 0,
        "human_review_replacements": 0,
    }
