from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

from grand_intellect.trove_curata_bootstrap_close_001_t3_review_remedy import (
    TroveCurataBootstrapCloseT3ReviewRemedyError,
    load_and_validate_trove_curata_bootstrap_close_t3_review_remedy,
    validate_trove_curata_bootstrap_close_t3_review_remedy,
)


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "trove_curata_bootstrap_close_001_t3_review_remedy.json"
SCHEMA = ROOT / "schemas" / "trove_curata_bootstrap_close_001_t3_review_remedy.schema.json"


class TroveCurataBootstrapCloseT3ReviewRemedyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def reject(self, mutate, pattern: str) -> None:
        broken = copy.deepcopy(self.record)
        mutate(broken)
        with self.assertRaisesRegex(TroveCurataBootstrapCloseT3ReviewRemedyError, pattern):
            validate_trove_curata_bootstrap_close_t3_review_remedy(broken)

    def test_canonical_remedy_validates(self) -> None:
        self.assertEqual(load_and_validate_trove_curata_bootstrap_close_t3_review_remedy(RECORD), self.record)

    def test_schema_is_closed_and_accepts_canonical_record(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(self.record, schema, cls=jsonschema.Draft202012Validator)

    def test_historical_gate_cannot_be_promoted(self) -> None:
        self.reject(lambda r: r["historical_subject"].update({"historical_t3_gate_satisfied": True}), "historical subject drift")

    def test_missing_adversary_cannot_be_relabelled(self) -> None:
        self.reject(lambda r: r["observed_evidence"].update({"bound_non_author_adversary_finding": {"status": "approved"}}), "missing historical evidence relabelled")

    def test_github_approval_cannot_substitute_for_t3(self) -> None:
        self.reject(lambda r: r["observed_evidence"]["exact_head_github_approval"].update({"is_t3_substitute": True}), "historical GitHub review drift")

    def test_workflow_cannot_substitute_for_t3(self) -> None:
        self.reject(lambda r: r["observed_evidence"].update({"workflow_success_is_t3_substitute": True}), "workflow substituted for T3")

    def test_merge_cannot_substitute_for_t3(self) -> None:
        self.reject(lambda r: r["observed_evidence"].update({"mechanical_merge_is_t3_substitute": True}), "merge substituted for T3")

    def test_unexpected_observed_evidence_field_rejected(self) -> None:
        self.reject(lambda r: r["observed_evidence"].update({"invented_evidence": None}), "observed evidence field set drift")

    def test_recovery_owner_cannot_become_mandatory(self) -> None:
        self.reject(lambda r: r["remedy_contract"].update({"mandatory_routine_human_reviewers": ["jimsteeg"]}), "remedy contract drift")

    def test_self_merge_cannot_be_enabled(self) -> None:
        self.reject(lambda r: r["remedy_contract"].update({"agent_may_merge_own_work": True}), "remedy contract drift")

    def test_destination_cannot_be_unblocked_early(self) -> None:
        self.reject(lambda r: r["remedy_contract"].update({"destination_acceptance_blocked_until_remedy_protected_merge": False}), "remedy contract drift")

    def test_bootstrap_artifacts_cannot_change(self) -> None:
        self.reject(lambda r: r["authority_boundary"].update({"bootstrap_artifacts_changed": True}), "authority boundary drift")

    def test_claim_inflation_rejected(self) -> None:
        self.reject(lambda r: r["claim_boundary"].update({"dataset_quality_certified": True}), "claim boundary drift or inflation")

    def test_claim_key_substitution_rejected(self) -> None:
        def substitute_claim_key(record) -> None:
            del record["claim_boundary"]["corpus_admitted"]
            record["claim_boundary"]["invented_claim"] = False

        self.reject(substitute_claim_key, "claim boundary drift or inflation")


if __name__ == "__main__":
    unittest.main()
