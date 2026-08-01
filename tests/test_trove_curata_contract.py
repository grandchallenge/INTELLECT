from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from grand_intellect.trove_curata_contract import (
    TroveCurataContractError,
    load_and_validate_trove_curata_contract,
    validate_trove_curata_contract,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "governance" / "trove_curata_xref_work_package.json"


class TroveCurataContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def assert_rejected(self, mutate) -> None:
        candidate = copy.deepcopy(self.record)
        mutate(candidate)
        with self.assertRaises(TroveCurataContractError):
            validate_trove_curata_contract(candidate)

    def test_canonical_contract_is_valid(self) -> None:
        validated = load_and_validate_trove_curata_contract(CONTRACT_PATH)
        self.assertEqual(validated["work_package_id"], "TROVE-CURATA-XREF-WP00")

    def test_gcl_cannot_claim_collaborator_repository(self) -> None:
        self.assert_rejected(
            lambda record: record["authority"].__setitem__(
                "collaborator_repository_authority", "gcl_controlled"
            )
        )

    def test_aether_cannot_become_runtime_authority(self) -> None:
        self.assert_rejected(
            lambda record: record["authority"].__setitem__("aether_role", "required_runtime")
        )

    def test_record_contract_cannot_be_omitted(self) -> None:
        self.assert_rejected(lambda record: record["record_contracts"].pop())

    def test_review_tier_semantics_cannot_drift(self) -> None:
        self.assert_rejected(
            lambda record: record["review_tiers"].__setitem__(
                "T3", "ordinary_maintainer_review"
            )
        )

    def test_synthetic_content_cannot_be_enabled(self) -> None:
        self.assert_rejected(
            lambda record: record["fixture"].__setitem__("synthetic_content_allowed", True)
        )

    def test_claim_inflation_is_rejected(self) -> None:
        for claim in self.record["claim_boundary"]:
            with self.subTest(claim=claim):
                self.assert_rejected(
                    lambda record, claim=claim: record["claim_boundary"].__setitem__(claim, True)
                )

    def test_aether_provider_decision_must_remain_deferred(self) -> None:
        def mutate(record):
            for decision in record["provider_decisions"]:
                if decision["capability"] == "aether_provenance_projection":
                    decision["decision"] = "reuse_directly"
                    return
            self.fail("fixture lacks AETHER provider decision")

        self.assert_rejected(mutate)

    def test_mathsolve_routing_cannot_be_imported(self) -> None:
        def mutate(record):
            for decision in record["provider_decisions"]:
                if decision["capability"] == "mathsolve_mathematical_routing":
                    decision["decision"] = "generalize"
                    return
            self.fail("fixture lacks MATHSOLVE provider decision")

        self.assert_rejected(mutate)

    def test_duplicate_provider_capability_is_rejected(self) -> None:
        self.assert_rejected(
            lambda record: record["provider_decisions"].append(
                copy.deepcopy(record["provider_decisions"][0])
            )
        )


if __name__ == "__main__":
    unittest.main()
