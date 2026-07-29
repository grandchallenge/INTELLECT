from __future__ import annotations

import unittest

from grand_intellect import (
    InMemoryFabric,
    MathematicalConstitution,
    MathematicalGrandIntellect,
    Phase,
    ReviewStatus,
)
from grand_intellect.model import Review, WorkPackageState


class MathCertLifecycleAlignmentTests(unittest.TestCase):
    def reviewed_integration_state(self) -> WorkPackageState:
        constitution = MathematicalConstitution()
        state = WorkPackageState(
            work_package_id="WP-INTEGRATION",
            phase=Phase.INTEGRATION,
            mathematical=True,
            specification={"claims": ["C1"]},
            mathematical_claims=[{"claim_id": "C1"}],
            memory_records=[
                {
                    "reasons": ["Preserve the Cert disposition boundary."],
                    "scope": "One synthetic claim.",
                    "limitations": ["No mathematical theorem is established."],
                }
            ],
        )
        for office in constitution.required_offices(Phase.INTEGRATION):
            state.reviews.append(
                Review(
                    office=office,
                    phase=Phase.INTEGRATION,
                    status=ReviewStatus.APPROVED,
                    obligations=tuple(
                        constitution.required_obligations(Phase.INTEGRATION, office)
                    ),
                )
            )
        return state

    def test_integration_rejects_missing_handoff(self) -> None:
        report = MathematicalConstitution().evaluate(self.reviewed_integration_state())
        self.assertFalse(report.ready)
        self.assertIn("MATHCERT handoff missing for claim: C1", report.missing)

    def test_runtime_rejects_ready_without_packet_identity(self) -> None:
        system = MathematicalGrandIntellect(InMemoryFabric())
        system.charter_mathematical(
            "WP",
            campaign_id="TEST-001",
            programme_ref="grandchallenge/MATH-PROGRAMME#123",
            title="Test Cert intake",
            purpose="Exercise fail-closed intake semantics.",
            scope="One synthetic claim.",
            acceptance_criteria=("Ready requires a packet identity.",),
        )
        state = system.state("WP")
        state.mathematical_claims.append({"claim_id": "C1"})
        with self.assertRaisesRegex(ValueError, "requires packet artifact identity"):
            system.record_mathcert_handoff(
                "WP",
                handoff_id="MC-HANDOFF-C1",
                issue="https://github.com/grandchallenge/MATHCERT/issues/1",
                target_claim_ids=("C1",),
                status="ready",
            )

    def test_runtime_rejects_submitted_without_acknowledgement(self) -> None:
        system = MathematicalGrandIntellect(InMemoryFabric())
        system.charter_mathematical(
            "WP",
            campaign_id="TEST-001",
            programme_ref="grandchallenge/MATH-PROGRAMME#123",
            title="Test Cert submission",
            purpose="Exercise fail-closed submission semantics.",
            scope="One synthetic claim.",
            acceptance_criteria=("Submitted requires acknowledgement.",),
        )
        system.state("WP").mathematical_claims.append({"claim_id": "C1"})
        with self.assertRaisesRegex(ValueError, "requires an intake acknowledgement"):
            system.record_mathcert_handoff(
                "WP",
                handoff_id="MC-HANDOFF-C1",
                issue="https://github.com/grandchallenge/MATHCERT/issues/1",
                target_claim_ids=("C1",),
                status="submitted",
                packet_repository="grandchallenge/MATHSOLVE",
                packet_commit_sha="a" * 40,
                packet_artifact_path="cert_handoffs/C1.json",
                packet_digest_algorithm="git_blob_sha1",
                packet_digest="b" * 40,
            )

    def test_runtime_rejects_adjudication_without_cert_output(self) -> None:
        system = MathematicalGrandIntellect(InMemoryFabric())
        system.charter_mathematical(
            "WP",
            campaign_id="TEST-001",
            programme_ref="grandchallenge/MATH-PROGRAMME#123",
            title="Test Cert adjudication",
            purpose="Exercise fail-closed adjudication semantics.",
            scope="One synthetic claim.",
            acceptance_criteria=("Adjudication requires output identity.",),
        )
        system.state("WP").mathematical_claims.append({"claim_id": "C1"})
        with self.assertRaisesRegex(ValueError, "requires Cert output artifact identity"):
            system.record_mathcert_handoff(
                "WP",
                handoff_id="MC-HANDOFF-C1",
                issue="https://github.com/grandchallenge/MATHCERT/issues/1",
                target_claim_ids=("C1",),
                status="qualified",
                packet_repository="grandchallenge/MATHSOLVE",
                packet_commit_sha="a" * 40,
                packet_artifact_path="cert_handoffs/C1.json",
                packet_digest_algorithm="git_blob_sha1",
                packet_digest="b" * 40,
                intake_acknowledgement="MATHCERT-INTAKE-C1",
            )


if __name__ == "__main__":
    unittest.main()
