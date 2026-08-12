from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from grand_intellect.council_review import GRAND_ASSEMBLY_OFFICES, canonical_sha256
from grand_intellect.grand_assembly_motion import assess_motion, compile_motion


ROOT = Path(__file__).resolve().parents[1]
MATTER = ROOT / "governance/grand_assembly_matters/GI-GRAND-ASSEMBLY-PROXY-DELEGATION-001"


def _motion() -> dict[str, object]:
    return json.loads((MATTER / "motion.json").read_text(encoding="utf-8"))


def _reviews() -> list[dict[str, object]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted((MATTER / "reviews").glob("*.json"))]


def test_canonical_grand_assembly_disposition_exactly_reproduces() -> None:
    compiled = compile_motion(MATTER / "motion.json", MATTER / "reviews").to_dict()
    stored = json.loads((MATTER / "disposition.json").read_text(encoding="utf-8"))
    assert compiled == stored
    assert compiled["required_office_count"] == 15
    assert compiled["full_quorum"] is True
    assert compiled["unanimous"] is True
    assert compiled["procedural_disposition"] == "adopt_fifteen_office_terminal_gate"


def test_exact_five_minders_and_ten_council_offices_are_required() -> None:
    assert len(GRAND_ASSEMBLY_OFFICES) == 15
    records = _reviews()
    with pytest.raises(ValueError, match="missing Grand assembly reviews"):
        assess_motion(_motion(), records[:-1])


def test_duplicate_session_identity_fails_closed() -> None:
    records = deepcopy(_reviews())
    records[1]["session_id"] = records[0]["session_id"]
    with pytest.raises(ValueError, match="session identity"):
        assess_motion(_motion(), records)


def test_dissent_produces_no_unanimous_disposition() -> None:
    motion = _motion()
    records = deepcopy(_reviews())
    records[0]["disposition"] = "reject"
    result = assess_motion(motion, records)
    assert result.unanimous is False
    assert result.procedural_disposition == "no_unanimous_disposition"


def test_wrong_office_order_is_rejected() -> None:
    motion = _motion()
    required = motion["required_offices"]
    assert isinstance(required, list)
    required[0], required[1] = required[1], required[0]
    with pytest.raises(ValueError, match="all five Minders"):
        assess_motion(motion, _reviews())
