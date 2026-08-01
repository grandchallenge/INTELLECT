from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from grand_intellect import (
    ACCELERATION_FACTOR,
    ADOPTION_ID,
    EXPECTED_DURATIONS,
    MAINTENANCE_PROGRAMME_CONTROL_ID,
    MAINTENANCE_PROGRAMME_DECISION_ID,
    MAINTENANCE_PROGRAMME_MIRROR_POLICY_ID,
    PHASE_A,
    maintenance_adoption_errors,
)

ROOT = Path(__file__).resolve().parents[1]
ADOPTION_PATH = ROOT / "governance" / "math_programme_maintenance_adoption.json"
SCHEMA_PATH = ROOT / "schemas" / "math_programme_maintenance_adoption.schema.json"


class MathProgrammeMaintenanceAdoptionTests(unittest.TestCase):
    def load_adoption(self) -> dict:
        return json.loads(ADOPTION_PATH.read_text(encoding="utf-8"))

    def schema_errors(self, record: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        return [error.message for error in validator.iter_errors(record)]

    def test_phase_a_adoption_is_valid_commitment(self) -> None:
        record = self.load_adoption()
        self.assertEqual(self.schema_errors(record), [])
        self.assertEqual(maintenance_adoption_errors(record), [])
        self.assertEqual(record["phase"], PHASE_A)
        self.assertFalse(record["effective"])

    def test_phase_a_fails_closed_when_effective_adoption_is_required(self) -> None:
        errors = maintenance_adoption_errors(
            self.load_adoption(), require_effective_protected_adoption=True
        )
        self.assertIn("protected Programme maintenance adoption is not complete", errors)

    def test_exported_identifiers_are_exact(self) -> None:
        self.assertEqual(ADOPTION_ID, "GI-ADMIN-MAINT-001")
        self.assertEqual(MAINTENANCE_PROGRAMME_CONTROL_ID, "MP-ADMIN-MAINT-001")
        self.assertEqual(MAINTENANCE_PROGRAMME_DECISION_ID, "MP-ADMIN-DECISION-001")
        self.assertEqual(MAINTENANCE_PROGRAMME_MIRROR_POLICY_ID, "MP-ADMIN-MIRROR-001")

    def test_acceleration_and_all_durations_are_exact(self) -> None:
        record = self.load_adoption()
        semantics = record["accepted_semantics"]
        self.assertEqual(ACCELERATION_FACTOR, 0.1)
        self.assertEqual(semantics["acceleration_factor"], ACCELERATION_FACTOR)
        for field, expected in EXPECTED_DURATIONS.items():
            self.assertEqual(semantics[field], expected)

    def test_existing_mathematical_provider_identities_are_not_rewritten(self) -> None:
        record = self.load_adoption()
        self.assertFalse(
            record["provider_identity_disposition"][
                "existing_mathematical_provider_identities_changed"
            ]
        )

    def test_mutation_rejects_candidate_authority_inflation(self) -> None:
        record = self.load_adoption()
        record["programme_candidate"]["candidate_can_create_authority"] = True
        self.assertTrue(self.schema_errors(record))
        self.assertIn(
            "candidate Programme reference cannot create authority",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_unaccelerated_pilot(self) -> None:
        record = self.load_adoption()
        record["accepted_semantics"]["pilot_duration"] = "P90D"
        self.assertTrue(self.schema_errors(record))
        self.assertIn(
            "maintenance duration drift: pilot_duration",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_delayed_material_synchronization(self) -> None:
        record = self.load_adoption()
        record["accepted_semantics"][
            "event_triggered_material_synchronization_is_immediate"
        ] = False
        self.assertTrue(self.schema_errors(record))
        self.assertIn(
            "maintenance semantic invariant failed: event_triggered_material_synchronization_is_immediate",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_missing_protected_artifact(self) -> None:
        record = self.load_adoption()
        record["required_protected_artifacts"].pop()
        self.assertTrue(self.schema_errors(record))
        self.assertIn(
            "maintenance protected artifact set drift",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_fabricated_phase_b_identity_in_phase_a(self) -> None:
        record = self.load_adoption()
        record["phase_b_requirements"]["exact_programme_merge_commit"] = "0" * 40
        self.assertTrue(self.schema_errors(record))
        self.assertIn(
            "Phase A maintenance adoption must not fabricate exact_programme_merge_commit",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_claim_inflation(self) -> None:
        record = self.load_adoption()
        record["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(self.schema_errors(record))
        self.assertIn(
            "maintenance adoption cannot promote mathematical or external claims",
            maintenance_adoption_errors(record),
        )


if __name__ == "__main__":
    unittest.main()
