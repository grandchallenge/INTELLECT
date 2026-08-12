from __future__ import annotations

import json
from pathlib import Path

from grand_intellect.council_motion import compile_motion


ROOT = Path(__file__).resolve().parents[1]
MATTER = ROOT / "governance/council_matters/GI-COUNCIL-PROXY-DELEGATION-SCHEDULE-001"
COMMITTEE = ROOT / "governance/committees/GI-PROXY-DELEGATION-COMMITTEE-001.json"
SCHEDULE = ROOT / "governance/committees/GI-PROXY-DELEGATION-COMMITTEE-001-SCHEDULE-001.json"


def test_accelerated_schedule_disposition_matches_exact_compiler_readback() -> None:
    compiled = compile_motion(MATTER / "motion.json", MATTER / "reviews").to_dict()
    stored = json.loads((MATTER / "disposition.json").read_text(encoding="utf-8"))
    assert compiled == stored
    assert compiled["full_quorum"] is True
    assert compiled["unanimous"] is True
    assert compiled["procedural_disposition"] == "table_for_human_steward_disposition"


def test_acceleration_is_pending_and_does_not_replace_current_deadline() -> None:
    committee = json.loads(COMMITTEE.read_text(encoding="utf-8"))
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    assert committee["deadline"] == "2026-09-10T23:59:59Z"
    assert schedule["requested_duration"] == "PT72H"
    assert schedule["effective_at"] is None
    assert schedule["deadline"] is None
    assert schedule["authority"]["current_rules_remain_effective"] is True
    assert schedule["authority"]["may_create_live_proxy_authority"] is False


def test_accelerated_scope_is_narrower_than_original_committee_limit() -> None:
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    assert schedule["scope"] == {
        "task_classes": 1,
        "repositories": 1,
        "live_proxy_acts": 0,
        "protected_integrations": 0,
        "human_review_replacements": 0,
    }
