from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from grand_intellect import (
    MATHCERT_PROVIDER_COMMIT,
    MATHCERT_ROUTE_REGISTRY_DIGEST,
    MATHSOLVE_CURRENT_CERT_ROUTES_DIGEST,
    MATHSOLVE_CURRENT_CERT_ROUTES_PATH,
    MATHSOLVE_PROVIDER_COMMIT,
    MathSolveProvider,
    PROGRAMME_CANDIDATE_ADMISSION_DIGEST,
    PROGRAMME_CANDIDATE_ADMISSION_PATH,
    PROGRAMME_POLICY_COMMIT,
    PROGRAMME_POLICY_DIGEST,
    PROGRAMME_RUNTIME_CONTRACT_DIGEST,
    PROGRAMME_RUNTIME_CONTRACT_PATH,
    PROGRAMME_UMBRELLA_STATE_DIGEST,
    PROGRAMME_UMBRELLA_STATE_PATH,
)
from grand_intellect.mathsolve_cert_current import current_provider_contract_errors

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "rh_ns_interface_qualifications.json"


class UmbrellaCurrentStateAlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        self.route = MathSolveProvider().governed_route(
            programme_ref="grandchallenge/MATH-PROGRAMME#170",
            provider_work_package_id="MS-TEST-CURRENT",
            provider_issue="https://github.com/grandchallenge/MATHSOLVE/issues/87",
        )

    def test_provider_exports_exact_current_contracts(self) -> None:
        self.assertEqual(PROGRAMME_POLICY_COMMIT, "54816c1525f0370cfbb0bfaa4ba8617cbb05fcb9")
        self.assertEqual(PROGRAMME_POLICY_DIGEST, "6fb8dce8f1b4f11f8994798840e72b09ad862575")
        self.assertEqual(PROGRAMME_RUNTIME_CONTRACT_PATH, "governance/umbrella_runtime_contract_v5.json")
        self.assertEqual(PROGRAMME_RUNTIME_CONTRACT_DIGEST, "2f304cbf07f934e97cdd2fbac7a6ccece2ac4a5a")
        self.assertEqual(PROGRAMME_CANDIDATE_ADMISSION_PATH, "governance/campaign_admission_registry.json")
        self.assertEqual(PROGRAMME_CANDIDATE_ADMISSION_DIGEST, "c724d1174c2e1caa8a74297a21a46aa9d1910962")
        self.assertEqual(PROGRAMME_UMBRELLA_STATE_PATH, PROGRAMME_RUNTIME_CONTRACT_PATH)
        self.assertEqual(PROGRAMME_UMBRELLA_STATE_DIGEST, PROGRAMME_RUNTIME_CONTRACT_DIGEST)
        self.assertEqual(MATHSOLVE_PROVIDER_COMMIT, "26c1060c2e40b170570fcf2fccc88539fa5b26e6")
        self.assertEqual(MATHSOLVE_CURRENT_CERT_ROUTES_PATH, "contracts/mathcert_current_routes.json")
        self.assertEqual(MATHSOLVE_CURRENT_CERT_ROUTES_DIGEST, "2f6bb27a453a8615ba3af75ca77452ceb7b83ca8")
        self.assertEqual(MATHCERT_PROVIDER_COMMIT, "0258e4f0bca0d90fac05b62aeef108f16dccffdd")
        self.assertEqual(MATHCERT_ROUTE_REGISTRY_DIGEST, "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1")
        self.assertEqual(current_provider_contract_errors(self.route), [])

    def test_provider_route_contains_five_content_addressed_contracts(self) -> None:
        expected = {
            "programme_policy",
            "programme_runtime_contract",
            "programme_candidate_admission",
            "mathsolve_current_cert_routes",
            "certification_contract",
        }
        self.assertEqual(set(self.route) & expected, expected)
        self.assertNotIn("programme_umbrella_state", self.route)
        for field in expected:
            self.assertEqual(self.route[field]["digest_algorithm"], "git_blob_sha1")
            self.assertEqual(len(self.route[field]["digest"]), 40)

    def test_stale_programme_contract_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["programme_policy"]["commit_sha"] = "d56edc23152f3ccde4c7db272b7af37f6cf698b9"
        self.assertIn(
            "mathematical route programme_policy identity drift",
            current_provider_contract_errors(stale),
        )

    def test_missing_runtime_contract_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale.pop("programme_runtime_contract")
        self.assertIn(
            "mathematical route requires content-addressed programme_runtime_contract",
            current_provider_contract_errors(stale),
        )

    def test_stale_runtime_contract_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["programme_runtime_contract"]["digest"] = "02cdfabb04f5d273fcb7531c515a73baab2bc52d"
        self.assertIn(
            "mathematical route programme_runtime_contract identity drift",
            current_provider_contract_errors(stale),
        )

    def test_missing_candidate_admission_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale.pop("programme_candidate_admission")
        self.assertIn(
            "mathematical route requires content-addressed programme_candidate_admission",
            current_provider_contract_errors(stale),
        )

    def test_stale_candidate_admission_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["programme_candidate_admission"]["digest"] = "a6bffaa197aa3921e3eb9d4f8a02b5dc2bbded24"
        self.assertIn(
            "mathematical route programme_candidate_admission identity drift",
            current_provider_contract_errors(stale),
        )

    def test_missing_current_solve_route_contract_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale.pop("mathsolve_current_cert_routes")
        self.assertIn(
            "mathematical route requires content-addressed mathsolve_current_cert_routes",
            current_provider_contract_errors(stale),
        )

    def test_stale_current_solve_route_contract_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["mathsolve_current_cert_routes"]["digest"] = "0" * 40
        self.assertIn(
            "mathematical route mathsolve_current_cert_routes identity drift",
            current_provider_contract_errors(stale),
        )

    def test_superseded_umbrella_field_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["programme_umbrella_state"] = copy.deepcopy(stale["programme_runtime_contract"])
        self.assertIn(
            "mathematical route contains superseded programme_umbrella_state",
            current_provider_contract_errors(stale),
        )

    def test_stale_cert_registry_is_rejected(self) -> None:
        stale = copy.deepcopy(self.route)
        stale["certification_contract"]["digest"] = "065f0531e4d763b389b207d4922d5a85b4335ee3"
        self.assertIn(
            "mathematical route certification_contract identity drift",
            current_provider_contract_errors(stale),
        )

    def test_fixture_pins_runtime_campaign_candidate_and_solve_contracts(self) -> None:
        programme = self.fixture["programme_contract"]
        self.assertEqual(programme["commit_sha"], PROGRAMME_POLICY_COMMIT)
        self.assertEqual(programme["routing_path"], "governance/mathsolve_routing_audit_vgse.json")
        self.assertEqual(programme["routing_digest"], PROGRAMME_POLICY_DIGEST)
        self.assertEqual(programme["runtime_path"], PROGRAMME_RUNTIME_CONTRACT_PATH)
        self.assertEqual(programme["runtime_digest"], PROGRAMME_RUNTIME_CONTRACT_DIGEST)
        self.assertEqual(programme["candidate_admission_path"], PROGRAMME_CANDIDATE_ADMISSION_PATH)
        self.assertEqual(programme["candidate_admission_digest"], PROGRAMME_CANDIDATE_ADMISSION_DIGEST)
        self.assertEqual(programme["campaign_registry_digest"], "4cabbd820097029d01430f9f8a0c02653321e5af")

        solve = self.fixture["solve_current_cert_contract"]
        self.assertEqual(solve["commit_sha"], MATHSOLVE_PROVIDER_COMMIT)
        self.assertEqual(solve["path"], MATHSOLVE_CURRENT_CERT_ROUTES_PATH)
        self.assertEqual(solve["digest"], MATHSOLVE_CURRENT_CERT_ROUTES_DIGEST)
        self.assertTrue(solve["producer_handoff_status_is_immutable"])
        self.assertTrue(solve["route_state_is_current_adjudication"])
        self.assertEqual(solve["judgment_gate_uses"], "route_state")

    def test_runtime_transitively_binds_vgse_solve_and_cert_artifacts(self) -> None:
        activation = self.fixture["vgse_activation_contract"]
        self.assertEqual(activation["programme_issue"], 170)
        self.assertEqual(activation["programme_pull_request"], 218)
        self.assertEqual(activation["programme_merge_commit"], PROGRAMME_POLICY_COMMIT)
        self.assertEqual(
            activation["solve_manifest"],
            {
                "repository": "grandchallenge/MATHSOLVE",
                "merge_commit": "1ebc9ace360e453fbc3707f6b23032b1c3c561eb",
                "path": "campaign_manifests/VGSE-001.json",
                "digest_algorithm": "git_blob_sha1",
                "digest": "3bb6b18052f5754e9ae9aa4f813d9b43dcd4e3b4",
            },
        )
        self.assertEqual(activation["pending_cert_handoff"]["state"], "pending")
        self.assertEqual(
            activation["pending_cert_handoff"]["digest"],
            "42cfa84978fd63c75f074b388afd8b1fcbd56091",
        )
        self.assertEqual(activation["cert_route"]["route_state"], "registered_pending_evidence")
        self.assertFalse(activation["cert_route"]["may_adjudicate"])
        self.assertIsNone(activation["cert_route"]["cert_output"])
        self.assertEqual(
            activation["cert_route"]["digest"],
            "de56bfb0544b27b6237a68ac87044d3f0ba2e445",
        )
        self.assertTrue(
            activation["runtime_consumer_obligation"]["intellect_repin_required"]
        )

    def test_fixture_declares_repository_authority(self) -> None:
        authority = self.fixture["authority_model"]
        self.assertEqual(authority["state_authority"], "protected_branch_repository_records")
        self.assertEqual(authority["github_issue_role"], "mutable_navigational_mirror")
        self.assertFalse(authority["issue_mutation_can_change_state"])
        self.assertTrue(authority["candidate_registry_is_separate_from_active_registry"])
        self.assertTrue(authority["runtime_overlay_transitively_binds_vgse_upstream_artifacts"])
        self.assertTrue(authority["unchanged_consumed_blobs_do_not_require_repin"])

    def test_candidate_portfolio_records_bounded_active_vgse(self) -> None:
        candidate = self.fixture["candidate_portfolio"]
        self.assertEqual(candidate["pre_admission"], ["NSOF-001"])
        self.assertEqual(candidate["reviewed_candidate_work_packages"], ["VGSE-001"])
        self.assertEqual(candidate["admitted_active"], ["VGSE-001"])
        self.assertEqual(candidate["candidate_execution_state"], "admitted_active_bounded")
        self.assertEqual(
            candidate["active_portfolio_effect"],
            "VGSE-001_bounded_active_pending_cert_evidence",
        )
        self.assertEqual(candidate["source_provenance_state"], "provider_verified")
        self.assertEqual(candidate["certification_state"], "registered_pending_evidence")
        self.assertTrue(candidate["candidate_campaign_admitted"])
        self.assertFalse(candidate["candidate_work_can_self_admit"])
        self.assertFalse(candidate["may_adjudicate"])
        self.assertIsNone(candidate["certificate_output"])

    def test_bounded_activation_cannot_be_inflated_to_adjudication(self) -> None:
        inflated = copy.deepcopy(self.fixture)
        inflated["candidate_portfolio"]["may_adjudicate"] = True
        inflated["candidate_portfolio"]["certificate_output"] = {
            "status": "certified"
        }
        invalid = (
            inflated["candidate_portfolio"]["candidate_work_can_self_admit"] is not False
            or inflated["candidate_portfolio"]["may_adjudicate"] is not False
            or inflated["candidate_portfolio"]["certificate_output"] is not None
        )
        self.assertTrue(invalid)

    def test_rh_and_ns_fixtures_separate_handoff_from_route_state(self) -> None:
        records = {item["campaign_id"]: item for item in self.fixture["qualifications"]}
        self.assertEqual(set(records), {"RH-001", "NS-CI-001"})
        self.assertEqual(records["RH-001"]["handoff_state"], "pending")
        self.assertEqual(records["NS-CI-001"]["handoff_state"], "ready")
        for record in records.values():
            self.assertEqual(record["route_state"], "qualified")
            self.assertEqual(record["status"], "qualified")
            self.assertEqual(record["qualification_scope"], "qualified_interface_only")
            self.assertFalse(record["mathematical_target_proved"])
            self.assertTrue(record["blocked_claims"])
            self.assertEqual(len(record["certificate_digest"]), 40)

    def test_route_state_cannot_be_replaced_by_producer_handoff_state(self) -> None:
        mutated = copy.deepcopy(self.fixture)
        mutated["qualifications"][0]["route_state"] = mutated["qualifications"][0]["handoff_state"]
        invalid = [
            item for item in mutated["qualifications"]
            if item["route_state"] != "qualified"
        ]
        self.assertEqual(len(invalid), 1)

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
