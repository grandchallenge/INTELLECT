from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from grand_intellect.council_review import GRAND_ASSEMBLY_OFFICES, canonical_sha256
from grand_intellect.grand_assembly_motion import assess_motion, compile_motion


ROOT = Path(__file__).resolve().parents[1]
MATTER = ROOT / "governance/grand_assembly_matters/GI-GRAND-ASSEMBLY-PROXY-DELEGATION-001"


def _motion() -> dict[str, object]:
    return json.loads((MATTER / "motion.json").read_text(encoding="utf-8"))


def _reviews() -> list[dict[str, object]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted((MATTER / "reviews").glob("*.json"))]


class GrandAssemblyMotionTests(unittest.TestCase):
    def test_canonical_grand_assembly_disposition_exactly_reproduces(self) -> None:
        compiled = compile_motion(MATTER / "motion.json", MATTER / "reviews").to_dict()
        stored = json.loads((MATTER / "disposition.json").read_text(encoding="utf-8"))
        self.assertEqual(compiled, stored)
        self.assertEqual(compiled["required_office_count"], 15)
        self.assertTrue(compiled["full_quorum"])
        self.assertTrue(compiled["unanimous"])
        self.assertEqual(compiled["procedural_disposition"], "adopt_fifteen_office_terminal_gate")

    def test_exact_five_minders_and_ten_council_offices_are_required(self) -> None:
        self.assertEqual(len(GRAND_ASSEMBLY_OFFICES), 15)
        records = _reviews()
        with self.assertRaisesRegex(ValueError, "missing Grand assembly reviews"):
            assess_motion(_motion(), records[:-1])

    def test_duplicate_session_identity_fails_closed(self) -> None:
        records = deepcopy(_reviews())
        records[1]["session_id"] = records[0]["session_id"]
        with self.assertRaisesRegex(ValueError, "session identity"):
            assess_motion(_motion(), records)

    def test_dissent_produces_no_unanimous_disposition(self) -> None:
        motion = _motion()
        records = deepcopy(_reviews())
        records[0]["disposition"] = "reject"
        result = assess_motion(motion, records)
        self.assertFalse(result.unanimous)
        self.assertEqual(result.procedural_disposition, "no_unanimous_disposition")

    def test_wrong_office_order_is_rejected(self) -> None:
        motion = _motion()
        required = motion["required_offices"]
        self.assertIsInstance(required, list)
        required[0], required[1] = required[1], required[0]
        with self.assertRaisesRegex(ValueError, "all five Minders"):
            assess_motion(motion, _reviews())


if __name__ == "__main__":
    unittest.main()
