from __future__ import annotations

from hashlib import sha1, sha256
import json
from pathlib import Path
import unittest

from grand_intellect.rsi_ccc_wp00 import (
    baseline_candidate,
    capability_candidate,
    canonical_json,
    check_proposal,
    make_proposal,
    optimized_candidate,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "manifest.json"
LEAN_M1_PATH = ROOT / "lean" / "RSICCCM1.lean"
FROZEN_FORMAL_OBJECT_SHA256 = "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def sha256_json(value: object) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


class RsiCccWp00M1BindingTests(unittest.TestCase):
    def test_m1_remains_bound_to_frozen_m0_object(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        formal = manifest["formal_object"]
        formal_data = (ROOT / formal["path"]).read_bytes()

        self.assertEqual(formal["sha256"], FROZEN_FORMAL_OBJECT_SHA256)
        self.assertEqual(sha256(formal_data).hexdigest(), FROZEN_FORMAL_OBJECT_SHA256)
        self.assertEqual(git_blob_sha(formal_data), formal["git_blob_sha"])
        self.assertEqual(
            manifest["mechanization"]["must_bind_to_formal_object_sha256"],
            FROZEN_FORMAL_OBJECT_SHA256,
        )

    def test_m1_proof_artifacts_are_content_bound_and_non_promotable(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        mechanization = manifest["mechanization"]

        self.assertEqual(mechanization["status"], "pending")
        self.assertEqual(mechanization["active_tranche"]["id"], "M1")
        self.assertEqual(
            mechanization["active_tranche"]["status"],
            "proof_complete_exact_head_replayed_pending_review",
        )
        self.assertFalse(manifest["promotion_ready"])
        self.assertEqual(mechanization["issue"], 104)
        self.assertEqual(mechanization["lean_toolchain"], "leanprover/lean4:v4.34.0")
        self.assertEqual(
            mechanization["open_targets"],
            [
                "perform independent non-authoring Formalist/Adversary/Referee review of the exact compiled head before any promotion decision"
            ],
        )

        records = mechanization["proof_artifacts"]
        self.assertGreaterEqual(len(records), 6)
        paths = {record["path"] for record in records}
        self.assertIn("lean/RSICCC.lean", paths)
        self.assertIn("lean/RSICCCM1.lean", paths)

        for record in records:
            data = (ROOT / record["path"]).read_bytes()
            self.assertEqual(git_blob_sha(data), record["git_blob_sha"])

    def test_m1_candidate_closure_targets_are_named(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        completed = set(manifest["mechanization"]["completed_on_current_proof_surface"])
        self.assertIn("concrete Kripke exponential witness with beta and eta laws", completed)
        self.assertIn("typed run interpretation connected to the concrete exponential layer", completed)
        self.assertIn("non-vacuous finite parity refinement domain with exact capability and optimization transitions", completed)
        self.assertIn("frozen checker certificate semantics bridged to AdmissionEvidence", completed)
        self.assertFalse(manifest["promotion_ready"])

    def test_lean_checker_constants_replay_from_frozen_python_checker(self) -> None:
        baseline = baseline_candidate()
        capability = capability_candidate()
        optimized = optimized_candidate()
        capability_proposal = make_proposal(baseline, capability, "capability_extension")
        optimization_proposal = make_proposal(
            capability,
            optimized,
            "semantics_preserving_optimization",
        )

        self.assertTrue(check_proposal(baseline, capability_proposal).accepted)
        self.assertTrue(check_proposal(capability, optimization_proposal).accepted)

        capability_bytes = len(canonical_json(capability_proposal).encode("utf-8"))
        optimization_bytes = len(canonical_json(optimization_proposal).encode("utf-8"))
        self.assertEqual(capability_bytes, 527)
        self.assertEqual(optimization_bytes, 540)

        expected_constants = {
            baseline.digest,
            capability.digest,
            optimized.digest,
            sha256_json(capability_proposal),
            sha256_json(optimization_proposal),
        }
        lean_source = LEAN_M1_PATH.read_text(encoding="utf-8")
        for value in expected_constants:
            self.assertIn(value, lean_source)
        self.assertIn("serializedBytes := 527", lean_source)
        self.assertIn("serializedBytes := 540", lean_source)


if __name__ == "__main__":
    unittest.main()
