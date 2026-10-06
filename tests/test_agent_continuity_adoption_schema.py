from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "agent_continuity_adoption.schema.json"
CONTRACT = ROOT / "governance" / "agent_execution" / "GCL-AGENT-CONTINUITY-001.json"


class AgentContinuityAdoptionSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.valid = {
            "schema_id": "GCL-AGENT-CONTINUITY-ADOPTION-001",
            "schema_version": "1.0.0",
            "adoption_id": "TEST-GCL-AGENT-CONTINUITY-001",
            "policy_id": "GCL-AGENT-CONTINUITY-001",
            "version": "1.0.0",
            "authority_repository": "grandchallenge/INTELLECT",
            "authority_path": "governance/agent_execution/GCL-AGENT-CONTINUITY-001.md",
            "repository": "grandchallenge/TEST",
            "binding_surface": "AGENTS.md",
            "required": True,
            "specialization": None,
            "local_validator": "ci/validate_agent_continuity_adoption.py",
            "authority_preservation": {
                "authority_changed": False,
                "protected_bypass_changed": False,
            },
            "specialization_data": {},
        }

    def assert_invalid(self, mutate) -> None:
        record = copy.deepcopy(self.valid)
        mutate(record)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(record, self.schema, cls=jsonschema.Draft202012Validator)

    def test_schema_is_valid_draft_2020_12(self) -> None:
        jsonschema.Draft202012Validator.check_schema(self.schema)

    def test_valid_common_envelope(self) -> None:
        jsonschema.validate(self.valid, self.schema, cls=jsonschema.Draft202012Validator)

    def test_policy_drift_fails(self) -> None:
        self.assert_invalid(lambda r: r.update(policy_id="OTHER"))

    def test_authority_path_drift_fails(self) -> None:
        self.assert_invalid(lambda r: r.update(authority_path="elsewhere.md"))

    def test_required_false_fails(self) -> None:
        self.assert_invalid(lambda r: r.update(required=False))

    def test_authority_expansion_fails(self) -> None:
        self.assert_invalid(lambda r: r["authority_preservation"].update(authority_changed=True))

    def test_missing_local_validator_fails(self) -> None:
        self.assert_invalid(lambda r: r.pop("local_validator"))

    def test_missing_specialization_data_fails(self) -> None:
        self.assert_invalid(lambda r: r.pop("specialization_data"))

    def test_contract_binds_schema_without_remote_runtime_authority(self) -> None:
        binding = self.contract["downstream_adoption_schema"]
        self.assertEqual("GCL-AGENT-CONTINUITY-ADOPTION-001", binding["schema_id"])
        self.assertEqual("schemas/agent_continuity_adoption.schema.json", binding["path"])
        self.assertFalse(binding["local_snapshot_authoritative"])
        self.assertFalse(binding["mutable_remote_fetch_allowed"])
        self.assertTrue(binding["repository_local_validator_required"])


if __name__ == "__main__":
    unittest.main()
