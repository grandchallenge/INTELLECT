from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from grand_intellect.trove_curata_bootstrap_closure import (
    TroveCurataBootstrapClosureError,
    load_and_validate_trove_curata_bootstrap_closure,
    validate_trove_curata_bootstrap_closure,
)


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "trove_curata_bootstrap_closure.json"


class TroveCurataBootstrapClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def reject(self, mutate, pattern: str) -> None:
        broken = copy.deepcopy(self.record)
        mutate(broken)
        with self.assertRaisesRegex(TroveCurataBootstrapClosureError, pattern):
            validate_trove_curata_bootstrap_closure(broken)

    def test_canonical_record_validates(self) -> None:
        self.assertEqual(load_and_validate_trove_curata_bootstrap_closure(RECORD), self.record)

    def test_unknown_root_field_rejected(self) -> None:
        self.reject(lambda record: record.update({"extra": True}), "field set drift")

    def test_source_head_drift_rejected(self) -> None:
        self.reject(
            lambda record: record["source"].update({"protected_head_at_preparation": "0" * 40}),
            "source identity drift",
        )

    def test_source_tree_drift_rejected(self) -> None:
        self.reject(
            lambda record: record["source"].update({"protected_tree_at_preparation": "0" * 40}),
            "source identity drift",
        )

    def test_destination_cannot_be_preactivated(self) -> None:
        self.reject(
            lambda record: record["destination"].update({"activation_state": "active"}),
            "destination boundary drift",
        )

    def test_destination_existence_cannot_be_rewritten(self) -> None:
        self.reject(
            lambda record: record["destination"].update(
                {"repository_observed_existing_at_preparation": True}
            ),
            "destination boundary drift",
        )

    def test_ladder_head_drift_rejected(self) -> None:
        self.reject(
            lambda record: record["bootstrap_ladder"][7].update({"exact_head": "0" * 40}),
            "ladder identity drift",
        )

    def test_ladder_merge_drift_rejected(self) -> None:
        self.reject(
            lambda record: record["bootstrap_ladder"][0].update(
                {"protected_merge": "0" * 40}
            ),
            "ladder identity drift",
        )

    def test_ladder_role_escalation_rejected(self) -> None:
        self.reject(
            lambda record: record["bootstrap_ladder"][7].update(
                {"role": "corpus_admission"}
            ),
            "ladder role drift",
        )

    def test_review_remedy_cannot_rewrite_history(self) -> None:
        self.reject(
            lambda record: record["review_remedies"]["fixture_004"].update(
                {"historical_state_rewritten": True}
            ),
            "review remedy history drift",
        )

    def test_artifact_blob_drift_rejected(self) -> None:
        self.reject(
            lambda record: record["artifact_inventory"][0].update({"blob_sha": "0" * 40}),
            "inventory digest drift",
        )

    def test_artifact_path_reordering_rejected(self) -> None:
        self.reject(
            lambda record: record["artifact_inventory"].reverse(),
            "path ordering drift",
        )

    def test_inventory_digest_rewrite_rejected(self) -> None:
        self.reject(
            lambda record: record.update({"artifact_inventory_sha256": "0" * 64}),
            "inventory digest drift",
        )

    def test_schema_projection_drift_rejected(self) -> None:
        self.reject(lambda record: record["schema_paths"].pop(), "schema identity projection drift")

    def test_workflow_projection_drift_rejected(self) -> None:
        self.reject(
            lambda record: record["workflow_paths"].pop(),
            "workflow identity projection drift",
        )

    def test_destination_may_not_invent_authority(self) -> None:
        self.reject(
            lambda record: record["migration_contract"].update(
                {"destination_may_invent_bootstrap_authority": True}
            ),
            "migration authority escalation",
        )

    def test_fixture_006_cannot_begin_before_activation(self) -> None:
        self.reject(
            lambda record: record["migration_contract"].update(
                {"fixture_006_may_begin_before_activation": True}
            ),
            "migration authority escalation",
        )

    def test_intellect_cannot_keep_substantive_implementation(self) -> None:
        self.reject(
            lambda record: record["migration_contract"].update(
                {"fixture_006_may_be_implemented_in_intellect_after_activation": True}
            ),
            "migration authority escalation",
        )

    def test_provider_authority_rejected(self) -> None:
        self.reject(
            lambda record: record["authority_boundary"].update(
                {"providers_have_admission_authority": True}
            ),
            "authority escalation",
        )

    def test_closure_cannot_activate_destination(self) -> None:
        self.reject(
            lambda record: record["authority_boundary"].update(
                {"bootstrap_closure_activates_destination": True}
            ),
            "authority escalation",
        )

    def test_claim_inflation_rejected(self) -> None:
        self.reject(
            lambda record: record["claim_boundary"].update(
                {"production_corpus_admitted": True}
            ),
            "claim inflation",
        )

    def test_record_digest_drift_rejected(self) -> None:
        self.reject(
            lambda record: record.update({"closure_record_sha256": "0" * 64}),
            "closure record digest drift",
        )


if __name__ == "__main__":
    unittest.main()
