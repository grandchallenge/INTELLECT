from __future__ import annotations

import unittest

from grand_intellect import (
    InMemoryFabric,
    MathematicalConstitution,
    MathematicalGrandIntellect,
    Office,
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

    def system_with_claim(self) -> MathematicalGrandIntellect:
        system = MathematicalGrandIntellect(InMemoryFabric())
        system.charter_mathematical(
            "WP",
            campaign_id="TEST-001",
            programme_ref="grandchallenge/MATH-PROGRAMME#123",
            title="Test Cert lifecycle",
            purpose="Exercise fail-closed certification semantics.",
            scope="One synthetic claim.",
            acceptance_criteria=("Invalid Cert state is rejected.",),
        )
        system._append(
            "mathematical.claim.registered",
            "WP",
            Office.FORMALIST.value,
            {
                "claim_id": "C1",
                "statement": "Synthetic claim for lifecycle validation.",
                "claim_type": "test",
                "support_type": "test",
                "source_refs": ["test-fixture"],
            },
        )
        return system

    def test_integration_rejects_missing_handoff(self) -> None:
        report = MathematicalConstitution().evaluate(self.reviewed_integration_state())
        self.assertFalse(report.ready)
        self.assertIn("MATHCERT handoff missing for claim: C1", report.missing)

    def test_runtime_rejects_ready_without_packet_identity(self) -> None:
        system = self.system_with_claim()
        with self.assertRaisesRegex(ValueError, "requires packet artifact identity"):
            system.record_mathcert_handoff(
                "WP",
                handoff_id="MC-HANDOFF-C1",
                issue="https://github.com/grandchallenge/MATHCERT/issues/1",
                target_claim_ids=("C1",),
                status="ready",
            )

    def test_runtime_rejects_submitted_without_acknowledgement(self) -> None:
        system = self.system_with_claim()
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
        system = self.system_with_claim()
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
