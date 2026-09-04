from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

from grand_intellect.multi_role_staffing import MultiRoleReviewError, validate_review_set


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/multi_role_review.schema.json").read_text())


def review(role: str, pass_id: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0", "work_class": "substantive",
        "reviewer_system_id": "codex-system", "logical_pass_id": pass_id,
        "role": role, "mode": "non_authoring_read_only",
        "subject": {"repository": "grandchallenge/INTELLECT", "commit": "a" * 40,
                    "tree": "b" * 40, "material_evidence_sha256": "c" * 64},
        "criteria": [f"{role} criteria"], "finding": "approved",
        "evidence": ["exact evidence"], "unresolved_obligations": [],
        "reserved_authority_ref": None,
    }


class MultiRoleStaffingTests(unittest.TestCase):
    def test_same_system_may_staff_distinct_roles(self) -> None:
        reviews = [review("Adversary", "pass-a"), review("Referee", "pass-r")]
        for item in reviews:
            jsonschema.validate(item, SCHEMA)
        validate_review_set(reviews)

    def test_duplicate_pass_rejected(self) -> None:
        with self.assertRaises(MultiRoleReviewError):
            validate_review_set([review("Adversary", "same"), review("Referee", "same")])

    def test_authoring_review_and_drift_rejected(self) -> None:
        bad = review("Referee", "pass-r")
        bad["mode"] = "authoring"
        with self.assertRaises(MultiRoleReviewError):
            validate_review_set([bad])
        drift = review("Referee", "pass-r")
        drift["subject"] = copy.deepcopy(drift["subject"])
        drift["subject"]["material_evidence_sha256"] = "d" * 64
        with self.assertRaises(MultiRoleReviewError):
            validate_review_set([review("Adversary", "pass-a"), drift])

    def test_reserved_authority_is_explicit(self) -> None:
        bad = review("Referee", "pass-r")
        bad["work_class"] = "reserved"
        with self.assertRaises(MultiRoleReviewError):
            validate_review_set([bad])

    def test_schema_rejects_unknown_and_missing_fields(self) -> None:
        bad = review("Referee", "pass-r")
        bad["green_ci_is_certification"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(bad, SCHEMA)
