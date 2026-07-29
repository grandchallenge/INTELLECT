from __future__ import annotations

import unittest

from grand_intellect import GitHubArtifactRef, MathematicalConstitution, Office, Phase, ReviewStatus
from grand_intellect.model import Review, WorkPackageState


def reviewed_judgment_state(*, status: str, include_artifact: bool = True) -> WorkPackageState:
    constitution = MathematicalConstitution()
    handoff = {
        "handoff_id": "MC-C1",
        "repository": "grandchallenge/MATHCERT",
        "issue": "https://github.com/grandchallenge/MATHCERT/issues/1",
        "target_claim_ids": ["C1"],
        "status": status,
    }
    if include_artifact:
        handoff.update(
            {
                "commit_sha": "a" * 40,
                "artifact_path": "handoffs/MC-C1.json",
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
            "decision": "accept",
            "rationale": "The certified claim is admitted.",
            "tradeoffs": ["Restricted scope"],
            "reversal_conditions": ["Certificate withdrawal"],
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

    def test_complete_handoff_requires_artifact_identity(self) -> None:
        report = MathematicalConstitution().evaluate(
            reviewed_judgment_state(status="qualified", include_artifact=False)
        )
        self.assertFalse(report.ready)
        self.assertIn(
            "MATHCERT handoff for C1 lacks commit-and-artifact identity",
            report.missing,
        )

    def test_rejected_handoff_cannot_promote_accepted_claim(self) -> None:
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
                "commit_sha": "c" * 40,
                "artifact_path": "handoffs/MC-C2.json",
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
