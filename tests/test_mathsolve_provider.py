from __future__ import annotations

import unittest

from grand_intellect import (
    GitHubArtifactRef,
    InMemoryFabric,
    MATHCERT_PROVIDER_COMMIT,
    MATHCERT_ROUTE_REGISTRY_DIGEST,
    MathematicalConstitution,
    MathematicalGrandIntellect,
    MathSolveProvider,
    Office,
    PROGRAMME_POLICY_COMMIT,
    PROGRAMME_POLICY_DIGEST,
    Phase,
    ReviewStatus,
)
from grand_intellect.engine import GateBlocked
from grand_intellect.model import Review, WorkPackageState


class MathSolveProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.system = MathematicalGrandIntellect(InMemoryFabric())
        self.wp = "GI-MS-TEST-001"
        self.system.charter_mathematical(
            self.wp,
            campaign_id="TEST-001",
            programme_ref="grandchallenge/MATH-PROGRAMME#1",
            title="Govern a mathematical campaign",
            purpose="Prove that ungoverned mathematics fails closed.",
            scope="One synthetic theorem-bearing work package.",
            acceptance_criteria=("Missing Solve routing blocks promotion",),
        )

    def approve_phase(self) -> None:
        phase = self.system.state(self.wp).phase
        for office in self.system.constitution.required_offices(phase):
            self.system.submit_review(
                self.wp,
                office=office,
                status=ReviewStatus.APPROVED,
                obligations=tuple(
                    sorted(
                        self.system.constitution.required_obligations(phase, office)
                    )
                ),
                evidence_refs=("test-evidence",),
            )

    def reach_specification(self) -> None:
        self.approve_phase()
        self.system.advance(self.wp)
        self.system.register_alternative(
            self.wp,
            alternative_id="A",
            summary="Direct argument",
            mechanism="Deduction",
            assumptions=("ZFC",),
            discriminating_test="Derivation closes",
        )
        self.system.register_alternative(
            self.wp,
            alternative_id="B",
            summary="Exact finite screen",
            mechanism="Enumeration",
            assumptions=("Finite reduction is adequate",),
            discriminating_test="Certificate replays",
        )
        self.approve_phase()
        self.system.advance(self.wp)
        self.system.record_specification(
            self.wp,
            claims=("TEST-C001",),
            evaluation_contract={"failure_condition": "checker rejects"},
            reversal_conditions=("counterexample",),
        )
        self.approve_phase()

    def test_ungoverned_mathematics_fails_closed(self) -> None:
        self.reach_specification()
        report = self.system.gate_report(self.wp)
        self.assertFalse(report.ready)
        self.assertIn(
            "mathematics requires a governed MATHSOLVE route or waiver",
            report.missing,
        )
        with self.assertRaises(GateBlocked):
            self.system.advance(self.wp)

    def test_provider_records_exact_programme_and_cert_contracts(self) -> None:
        route = MathSolveProvider().governed_route(
            programme_ref="grandchallenge/MATH-PROGRAMME#123",
            provider_work_package_id="MS-TEST-WP00",
            provider_issue="https://github.com/grandchallenge/MATHSOLVE/issues/73",
        )
        self.assertEqual(route["programme_policy"]["commit_sha"], PROGRAMME_POLICY_COMMIT)
        self.assertEqual(route["programme_policy"]["digest"], PROGRAMME_POLICY_DIGEST)
        self.assertEqual(
            route["certification_contract"]["commit_sha"], MATHCERT_PROVIDER_COMMIT
        )
        self.assertEqual(
            route["certification_contract"]["digest"],
            MATHCERT_ROUTE_REGISTRY_DIGEST,
        )

    def test_route_must_be_commit_and_digest_complete_before_confrontation(self) -> None:
        self.reach_specification()
        self.system.register_mathsolve_route(
            self.wp,
            programme_ref="grandchallenge/MATH-PROGRAMME#1",
            provider_work_package_id="MS-TEST-WP00",
            provider_issue="https://github.com/grandchallenge/MATHSOLVE/issues/1",
        )
        self.assertTrue(self.system.gate_report(self.wp).ready)
        self.system.advance(self.wp)
        self.system.record_realization(
            self.wp,
            realization_id="R1",
            artifact_refs=("work_packages/MS_TEST_WP00.md",),
            verification_commands=("python ci/validate_solve.py",),
        )
        self.approve_phase()
        incomplete = self.system.gate_report(self.wp)
        self.assertFalse(incomplete.ready)
        self.assertIn(
            "MATHSOLVE route requires an exact provider commit", incomplete.missing
        )

        artifact = GitHubArtifactRef(
            repository="grandchallenge/MATHSOLVE",
            commit_sha="a" * 40,
            artifact_path="work_packages/MS_TEST_WP00.md",
            sha256="b" * 64,
        )
        claim_ledger = GitHubArtifactRef(
            repository="grandchallenge/MATHSOLVE",
            commit_sha="a" * 40,
            artifact_path="work_packages/MS_TEST_CLAIMS.yaml",
            sha256="c" * 64,
        )
        dag = GitHubArtifactRef(
            repository="grandchallenge/MATHSOLVE",
            commit_sha="a" * 40,
            artifact_path="work_packages/MS_TEST_DAG.yaml",
            sha256="d" * 64,
        )
        self.system.register_mathsolve_route(
            self.wp,
            programme_ref="grandchallenge/MATH-PROGRAMME#1",
            provider_work_package_id="MS-TEST-WP00",
            provider_issue="https://github.com/grandchallenge/MATHSOLVE/issues/1",
            provider_commit="a" * 40,
            artifact_manifest=(artifact,),
            claim_ledger=claim_ledger,
            proof_obligation_dag=dag,
        )
        self.assertTrue(self.system.gate_report(self.wp).ready)

    def judgment_state(self) -> WorkPackageState:
        constitution = MathematicalConstitution()
        phase = Phase.JUDGMENT
        state = WorkPackageState(
            work_package_id="WP",
            phase=phase,
            mathematical=True,
            judgment={
                "decision": "reject",
                "rationale": "No adjudicated evidence is available.",
                "tradeoffs": ["Restricted scope"],
                "reversal_conditions": ["New evidence"],
            },
        )
        for office in constitution.required_offices(phase):
            state.reviews.append(
                Review(
                    office=office,
                    phase=phase,
                    status=ReviewStatus.APPROVED,
                    obligations=tuple(
                        constitution.required_obligations(phase, office)
                    ),
                )
            )
        return state

    def test_every_registered_claim_requires_mathcert_adjudication(self) -> None:
        constitution = MathematicalConstitution()
        state = self.judgment_state()
        state.specification = {"claims": ["C1"]}
        state.mathematical_claims.append({"claim_id": "C1"})
        report = constitution.evaluate(state)
        self.assertFalse(report.ready)
        self.assertIn("MATHCERT handoff missing for claim: C1", report.missing)

        state.mathcert_handoffs.append(
            {
                "handoff_id": "MC-C1",
                "repository": "grandchallenge/MATHCERT",
                "target_claim_ids": ["C1"],
                "status": "pending",
            }
        )
        report = constitution.evaluate(state)
        self.assertFalse(report.ready)
        self.assertIn(
            "MATHCERT adjudicated disposition missing for claim: C1",
            report.missing,
        )

    def test_specification_claim_cannot_bypass_registration_and_adjudication(self) -> None:
        constitution = MathematicalConstitution()
        state = self.judgment_state()
        state.specification = {
            "claims": ["C-SPEC"],
            "evaluation_contract": {"failure_condition": "checker rejects"},
            "reversal_conditions": ["counterexample"],
        }

        report = constitution.evaluate(state)
        self.assertFalse(report.ready)
        self.assertIn(
            "mathematical claim records missing for specification claims: C-SPEC",
            report.missing,
        )
        self.assertIn("MATHCERT handoff missing for claim: C-SPEC", report.missing)

        state.mathematical_claims.append({"claim_id": "C-SPEC"})
        state.mathcert_handoffs.append(
            {
                "handoff_id": "MC-C-SPEC",
                "repository": "grandchallenge/MATHCERT",
                "target_claim_ids": ["C-SPEC"],
                "status": "ready",
                "packet_repository": "grandchallenge/MATHSOLVE",
                "packet_commit_sha": "a" * 40,
                "packet_artifact_path": "cert_handoffs/C-SPEC.json",
                "packet_digest_algorithm": "git_blob_sha1",
                "packet_digest": "b" * 40,
            }
        )
        report = constitution.evaluate(state)
        self.assertFalse(report.ready)
        self.assertIn(
            "MATHCERT adjudicated disposition missing for claim: C-SPEC",
            report.missing,
        )

    def test_exemption_requires_referee_steward_and_human_authority(self) -> None:
        provider = MathSolveProvider()
        with self.assertRaises(ValueError):
            provider.exemption(
                waiver_id="W1",
                reason="Administrative-only change",
                scope="No mathematical claim",
                risks=("Misclassification",),
                approving_offices=(Office.STEWARD,),
                human_steward_authorization="HS-1",
                review_condition="Reopen if a claim is added",
            )

        waiver = provider.exemption(
            waiver_id="W1",
            reason="Administrative-only change",
            scope="No mathematical claim",
            risks=("Misclassification",),
            approving_offices=(Office.STEWARD, Office.REFEREE),
            human_steward_authorization="HS-1",
            review_condition="Reopen if a claim is added",
        )
        self.assertEqual(waiver["status"], "exempted")
        self.assertTrue(waiver["cert_handoff_required"])
        self.assertIn("programme_policy", waiver)
        self.assertIn("certification_contract", waiver)


if __name__ == "__main__":
    unittest.main()
