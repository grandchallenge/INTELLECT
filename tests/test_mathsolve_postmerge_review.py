from __future__ import annotations

import unittest

from grand_intellect import GitHubArtifactRef, MathematicalConstitution, Phase, ReviewStatus
from grand_intellect.model import Review, WorkPackageState


def reviewed_judgment_state(
    *,
    status: str,
    include_packet: bool = True,
    include_acknowledgement: bool = True,
    include_output: bool = True,
    decision: str = "accept",
) -> WorkPackageState:
    constitution = MathematicalConstitution()
    handoff = {
        "handoff_id": "MC-C1",
        "repository": "grandchallenge/MATHCERT",
        "issue": "https://github.com/grandchallenge/MATHCERT/issues/1",
        "target_claim_ids": ["C1"],
        "status": status,
    }
    if include_packet and status != "pending":
        handoff.update(
            {
                "packet_repository": "grandchallenge/MATHSOLVE",
                "packet_commit_sha": "c" * 40,
                "packet_artifact_path": "cert_handoffs/C1.json",
                "packet_digest_algorithm": "git_blob_sha1",
                "packet_digest": "d" * 40,
            }
        )
    if include_acknowledgement and status in {
        "submitted",
        "certified",
        "qualified",
        "rejected",
        "proof_debt",
    }:
        handoff["intake_acknowledgement"] = "MATHCERT-INTAKE-C1"
    if include_output and status in {"certified", "qualified", "rejected", "proof_debt"}:
        handoff.update(
            {
                "commit_sha": "a" * 40,
                "artifact_path": "dispositions/MC-C1.json",
                "digest_algorithm": "git_blob_sha1",
                "digest": "b" * 40,
            }
        )
    state = WorkPackageState(
        work_package_id="WP",
        phase=Phase.JUDGMENT,
        mathematical=True,
        specification={"claims": ["C1"]},
        judgment={
            "decision": decision,
            "rationale": "The disposition is applied under its exact scope.",
            "tradeoffs": ["Restricted scope"],
            "reversal_conditions": ["Disposition withdrawal"],
        },
        mathematical_claims=[{"claim_id": "C1"}],
        mathcert_handoffs=[handoff],
    )
    for office in constitution.required_offices(Phase.JUDGMENT):
        state.reviews.append(
            Review(
                office=office,
                phase=Phase.JUDGMENT,
                status=ReviewStatus.APPROVED,
                obligations=tuple(
                    constitution.required_obligations(Phase.JUDGMENT, office)
                ),
            )
        )
    return state


class PostMergeMathSolveReviewTests(unittest.TestCase):
    def test_git_blob_identity_is_first_class(self) -> None:
        artifact = GitHubArtifactRef(
            repository="grandchallenge/MATHSOLVE",
            commit_sha="a" * 40,
            artifact_path="claim_ledger.yaml",
            digest_algorithm="git_blob_sha1",
            digest="b" * 40,
        )
        self.assertEqual(artifact.to_dict()["digest_algorithm"], "git_blob_sha1")

    def test_ready_packet_is_not_an_adjudication(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="ready", include_acknowledgement=False, include_output=False)
        )
        self.assertFalse(report.ready)
        self.assertIn(
            "MATHCERT adjudicated disposition missing for claim: C1",
            report.missing,
        )

    def test_submitted_packet_is_not_an_adjudication(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="submitted", include_output=False)
        )
        self.assertFalse(report.ready)
        self.assertIn(
            "MATHCERT adjudicated disposition missing for claim: C1",
            report.missing,
        )

    def test_adjudicated_handoff_requires_output_identity(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="qualified", include_output=False)
        )
        self.assertFalse(report.ready)
        self.assertIn(
            "MATHCERT disposition for C1 lacks output artifact identity",
            report.missing,
        )

    def test_rejected_handoff_closes_lineage_but_cannot_promote(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="rejected")
        )
        self.assertFalse(report.ready)
        self.assertTrue(
            any(
                "accepted mathematical claims require certified or qualified" in item
                for item in report.missing
            )
        )

    def test_rejected_handoff_allows_nonpositive_judgment(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="rejected", decision="reject")
        )
        self.assertTrue(report.ready, report.missing)

    def test_qualified_handoff_can_support_accepted_claim(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="qualified")
        )
        self.assertTrue(report.ready, report.missing)

    def test_registered_claim_must_be_declared_in_specification(self) -> None:
        state = reviewed_judgment_state(status="qualified")
        state.mathematical_claims.append({"claim_id": "C2"})
        state.mathcert_handoffs.append(
            {
                "handoff_id": "MC-C2",
                "repository": "grandchallenge/MATHCERT",
                "issue": "https://github.com/grandchallenge/MATHCERT/issues/2",
                "target_claim_ids": ["C2"],
                "status": "qualified",
                "packet_repository": "grandchallenge/MATHSOLVE",
                "packet_commit_sha": "e" * 40,
                "packet_artifact_path": "cert_handoffs/C2.json",
                "packet_digest_algorithm": "git_blob_sha1",
                "packet_digest": "f" * 40,
                "intake_acknowledgement": "MATHCERT-INTAKE-C2",
                "commit_sha": "c" * 40,
                "artifact_path": "dispositions/MC-C2.json",
                "digest_algorithm": "git_blob_sha1",
                "digest": "d" * 40,
            }
        )
        report = MathematicalConstitution().evaluate(state)
        self.assertFalse(report.ready)
        self.assertIn(
            "registered mathematical claims absent from specification: C2",
            report.missing,
        )


if __name__ == "__main__":
    unittest.main()
