from __future__ import annotations

import json
import unittest
from pathlib import Path

from grand_intellect import (
    ACCELERATION_FACTOR,
    ADOPTION_ID,
    EXPECTED_DURATIONS,
    MAINTENANCE_PROGRAMME_CONTROL_ID,
    MAINTENANCE_PROGRAMME_DECISION_ID,
    MAINTENANCE_PROGRAMME_MIRROR_POLICY_ID,
    PHASE_B,
    maintenance_adoption_errors,
)
from grand_intellect.maintenance_contract import (
    DECISION_RECORD_BLOB,
    MAINTENANCE_CONTROL_BLOB,
    MIRROR_POLICY_BLOB,
    PROGRAMME_MERGE_COMMIT,
)

ROOT = Path(__file__).resolve().parents[1]
ADOPTION_PATH = ROOT / "governance" / "math_programme_maintenance_adoption.json"
SCHEMA_PATH = ROOT / "schemas" / "math_programme_maintenance_adoption.schema.json"


class MathProgrammeMaintenanceAdoptionTests(unittest.TestCase):
    def load_adoption(self) -> dict:
        return json.loads(ADOPTION_PATH.read_text(encoding="utf-8"))

    def load_schema(self) -> dict:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_schema_is_strict_and_phase_bound(self) -> None:
        schema = self.load_schema()
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["adoption_id"]["const"], ADOPTION_ID)
        self.assertEqual(
            schema["properties"]["accepted_semantics"]["properties"][
                "acceleration_factor"
            ]["const"],
            0.1,
        )
        self.assertEqual(len(schema["allOf"]), 2)

    def test_phase_b_adoption_is_effective_and_valid(self) -> None:
        record = self.load_adoption()
        self.assertEqual(maintenance_adoption_errors(record), [])
        self.assertEqual(
            maintenance_adoption_errors(
                record, require_effective_protected_adoption=True
            ),
            [],
        )
        self.assertEqual(record["phase"], PHASE_B)
        self.assertTrue(record["effective"])
        self.assertEqual(
            record["authority_status"], "PROTECTED_CONTENT_ADDRESSED_AUTHORITY"
        )

    def test_exported_identifiers_are_exact(self) -> None:
        self.assertEqual(ADOPTION_ID, "GI-ADMIN-MAINT-001")
        self.assertEqual(MAINTENANCE_PROGRAMME_CONTROL_ID, "MP-ADMIN-MAINT-001")
        self.assertEqual(MAINTENANCE_PROGRAMME_DECISION_ID, "MP-ADMIN-DECISION-001")
        self.assertEqual(MAINTENANCE_PROGRAMME_MIRROR_POLICY_ID, "MP-ADMIN-MIRROR-001")

    def test_protected_programme_identities_are_exact(self) -> None:
        record = self.load_adoption()
        phase_b = record["phase_b_requirements"]
        self.assertEqual(phase_b["exact_programme_merge_commit"], PROGRAMME_MERGE_COMMIT)
        self.assertEqual(phase_b["maintenance_control_blob"], MAINTENANCE_CONTROL_BLOB)
        self.assertEqual(phase_b["decision_record_blob"], DECISION_RECORD_BLOB)
        self.assertEqual(phase_b["mirror_policy_blob"], MIRROR_POLICY_BLOB)

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
        self.assertIn(
            "candidate Programme reference cannot create authority",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_unaccelerated_pilot(self) -> None:
        record = self.load_adoption()
        record["accepted_semantics"]["pilot_duration"] = "P90D"
        self.assertIn(
            "maintenance duration drift: pilot_duration",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_delayed_material_synchronization(self) -> None:
        record = self.load_adoption()
        record["accepted_semantics"][
            "event_triggered_material_synchronization_is_immediate"
        ] = False
        self.assertIn(
            "maintenance semantic invariant failed: event_triggered_material_synchronization_is_immediate",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_missing_protected_artifact(self) -> None:
        record = self.load_adoption()
        record["required_protected_artifacts"].pop()
        self.assertIn(
            "maintenance protected artifact set drift",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_stale_programme_merge(self) -> None:
        record = self.load_adoption()
        record["phase_b_requirements"]["exact_programme_merge_commit"] = "0" * 40
        self.assertIn(
            "Phase B maintenance adoption stale identity: exact_programme_merge_commit",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_stale_control_blob(self) -> None:
        record = self.load_adoption()
        record["phase_b_requirements"]["maintenance_control_blob"] = "0" * 40
        self.assertIn(
            "Phase B maintenance adoption stale identity: maintenance_control_blob",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_missing_phase_b_identity(self) -> None:
        record = self.load_adoption()
        record["phase_b_requirements"]["decision_record_blob"] = None
        self.assertIn(
            "Phase B maintenance adoption requires exact decision_record_blob",
            maintenance_adoption_errors(record),
        )

    def test_mutation_rejects_claim_inflation(self) -> None:
        record = self.load_adoption()
        record["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertIn(
            "maintenance adoption cannot promote mathematical or external claims",
            maintenance_adoption_errors(record),
        )


if __name__ == "__main__":
    unittest.main()
