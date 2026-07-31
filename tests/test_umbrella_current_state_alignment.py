from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from grand_intellect import (
    MATHCERT_PROVIDER_COMMIT,
    MATHCERT_ROUTE_REGISTRY_DIGEST,
    MathSolveProvider,
    PROGRAMME_POLICY_COMMIT,
    PROGRAMME_POLICY_DIGEST,
    PROGRAMME_UMBRELLA_STATE_DIGEST,
)
from grand_intellect.mathsolve_cert_current import current_provider_contract_errors

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "rh_ns_interface_qualifications.json"


class UmbrellaCurrentStateAlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.route = MathSolveProvider().governed_route(
            programme_ref="grandchallenge/MATH-PROGRAMME#159",
            provider_work_package_id="MS-TEST-CURRENT",
            provider_issue="https://github.com/grandchallenge/MATHSOLVE/issues/80",
        )

    def test_provider_exports_exact_current_contracts(self) -> None:
        self.assertEqual(PROGRAMME_POLICY_COMMIT, "6c0b3e55eeca9be1ef5a538b0fb659f3bf1045a2")
        self.assertEqual(PROGRAMME_POLICY_DIGEST, "4a27ec8aaaa60f919ba51028807b83dc522bfcff")
        self.assertEqual(PROGRAMME_UMBRELLA_STATE_DIGEST, "a2a1c3d590f535972c87f57d9b86155a246a61ba")
        self.assertEqual(MATHCERT_PROVIDER_COMMIT, "0258e4f0bca0d90fac05b62aeef108f16dccffdd")
        self.assertEqual(MATHCERT_ROUTE_REGISTRY_DIGEST, "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1")
        self.assertEqual(current_provider_contract_errors(self.route), [])

    def test_provider_route_contains_three_content_addressed_contracts(self) -> None:
        self.assertEqual(
            set(self.route) & {
                "programme_policy",
                "programme_umbrella_state",
                "certification_contract",
            },
            {
                "programme_policy",
                "programme_umbrella_state",
                "certification_contract",
            },
        )
        for field in (
            "programme_policy",
            "programme_umbrella_state",
            "certification_contract",
        ):
            self.assertEqual(self.route[field]["digest_algorithm"], "git_blob_sha1")
            self.assertEqual(len(self.route[field]["digest"]), 40)

    def test_stale_programme_contract_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["programme_policy"]["commit_sha"] = "8182b8a5dc7b157d1a6b2a0f43d66c0598a2b072"
        self.assertIn(
            "mathematical route programme_policy identity drift",
            current_provider_contract_errors(stale),
        )

    def test_missing_umbrella_state_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale.pop("programme_umbrella_state")
        self.assertIn(
            "mathematical route requires content-addressed programme_umbrella_state",
            current_provider_contract_errors(stale),
        )

    def test_stale_cert_registry_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["certification_contract"]["digest"] = "065f0531e4d763b389b207d4922d5a85b4335ee3"
        self.assertIn(
            "mathematical route certification_contract identity drift",
            current_provider_contract_errors(stale),
        )

    def test_rh_and_ns_fixtures_are_interface_only(self) -> None:
        records = {item["campaign_id"]: item for item in self.fixture["qualifications"]}
        self.assertEqual(set(records), {"RH-001", "NS-CI-001"})
        for record in records.values():
            self.assertEqual(record["status"], "qualified")
            self.assertEqual(record["qualification_scope"], "qualified_interface_only")
            self.assertFalse(record["mathematical_target_proved"])
            self.assertTrue(record["blocked_claims"])
            self.assertEqual(len(record["certificate_digest"]), 40)

    def test_qualification_scope_inflation_is_rejected_by_fixture_contract(self) -> None:
        inflated = copy.deepcopy(self.fixture)
        inflated["qualifications"][0]["qualification_scope"] = "theorem_proved"
        invalid = [
            item for item in inflated["qualifications"]
            if item["qualification_scope"] != "qualified_interface_only"
            or item["mathematical_target_proved"] is not False
        ]
        self.assertEqual(len(invalid), 1)


if __name__ == "__main__":
    unittest.main()
