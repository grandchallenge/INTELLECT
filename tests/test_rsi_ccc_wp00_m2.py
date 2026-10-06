from __future__ import annotations

import copy
from hashlib import sha1, sha256
import json
from pathlib import Path
import unittest

from grand_intellect.rsi_ccc_wp00 import refines, sha256_json
from grand_intellect.rsi_ccc_wp00_m2 import (
    FROZEN_CHECKER_GIT_BLOB,
    FROZEN_FORMAL_OBJECT_GIT_BLOB,
    FROZEN_FORMAL_OBJECT_SHA256,
    SequenceReplayError,
    accepted_candidates,
    generated_sequence_summary,
    replay_sequence_artifact,
)


ROOT = Path(__file__).resolve().parents[1]
FORMAL_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "formal_object.json"
MANIFEST_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "manifest.json"
SEQUENCE_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "m2_sequence.json"
CHECKER_PATH = ROOT / "src" / "grand_intellect" / "rsi_ccc_wp00.py"
LEAN_M2_PATH = ROOT / "lean" / "RSICCCM2.lean"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


class RsiCccWp00M2Tests(unittest.TestCase):
    def load_sequence(self) -> dict[str, object]:
        return json.loads(SEQUENCE_PATH.read_text(encoding="utf-8"))

    def test_frozen_formal_object_and_checker_are_byte_stable(self) -> None:
        formal = FORMAL_PATH.read_bytes()
        checker = CHECKER_PATH.read_bytes()

        self.assertEqual(sha256(formal).hexdigest(), FROZEN_FORMAL_OBJECT_SHA256)
        self.assertEqual(git_blob_sha(formal), FROZEN_FORMAL_OBJECT_GIT_BLOB)
        self.assertEqual(git_blob_sha(checker), FROZEN_CHECKER_GIT_BLOB)

    def test_whole_chain_replays_from_genesis_to_exact_final_state(self) -> None:
        artifact = self.load_sequence()
        result = replay_sequence_artifact(artifact)

        self.assertEqual(result.accepted_transition_count, 5)
        self.assertEqual(result.rejected_event_count, 10)
        self.assertEqual(
            result.final_candidate_digest,
            "4f0b7070b8e32d839f2d296bea9bb4ce3981aa0100e71605f4cf3dc45fe02b03",
        )
        self.assertEqual(
            result.event_chain_digest,
            "da24637752e285b39e56c39f4a435e9d4b61be44adad813190a1247f9a52d10e",
        )
        self.assertEqual(
            artifact,
            generated_sequence_summary(),
            "retained sequence must equal a fresh replay through the frozen checker",
        )

    def test_accumulated_obligations_never_shrink(self) -> None:
        states = accepted_candidates()
        previous_domain = states[0].competence_domain

        for old, new in zip(states, states[1:]):
            self.assertTrue(refines(old, new))
            self.assertTrue(previous_domain.issubset(new.competence_domain))
            for x in previous_domain:
                self.assertEqual(new.answers[x], old.answers[x])
            previous_domain = new.competence_domain

        self.assertEqual(previous_domain, frozenset(range(16)))

    def test_trajectory_exercises_sequence_level_adversaries(self) -> None:
        artifact = self.load_sequence()
        outcomes = {
            event["scenario"]: event["expected_decision"]["code"]
            for event in artifact["events"]
        }
        self.assertEqual(outcomes["unsafe_candidate"], "unsafe_candidate")
        self.assertEqual(outcomes["stale_ancestry"], "stale_base")
        self.assertEqual(outcomes["context_drift"], "context_substitution")
        self.assertEqual(outcomes["trust_boundary_creep"], "trust_kernel_mutation")
        self.assertEqual(outcomes["ratcheting_regression"], "non_refinement")
        self.assertEqual(outcomes["metric_gaming"], "malformed")
        self.assertEqual(outcomes["resource_laundering"], "resource_bound")
        self.assertEqual(outcomes["no_op_succession"], "non_improvement")
        self.assertEqual(outcomes["certificate_receipt_reuse"], "stale_base")
        self.assertEqual(outcomes["cycling_oscillation"], "non_improvement")

    def test_event_receipt_reuse_or_tamper_fails_closed(self) -> None:
        artifact = self.load_sequence()

        tampered_previous = copy.deepcopy(artifact)
        tampered_previous["events"][4]["previous_event_digest"] = artifact["genesis"][
            "genesis_digest"
        ]
        with self.assertRaises(SequenceReplayError):
            replay_sequence_artifact(tampered_previous)

        reused_receipt = copy.deepcopy(artifact)
        reused_receipt["events"][-1]["event_digest"] = artifact["events"][0][
            "event_digest"
        ]
        with self.assertRaises(SequenceReplayError):
            replay_sequence_artifact(reused_receipt)

    def test_every_retained_event_digest_is_canonical_and_chained(self) -> None:
        artifact = self.load_sequence()
        previous = artifact["genesis"]["genesis_digest"]

        for event in artifact["events"]:
            self.assertEqual(event["previous_event_digest"], previous)
            body = dict(event)
            retained = body.pop("event_digest")
            self.assertEqual(sha256_json(body), retained)
            previous = retained

        self.assertEqual(previous, artifact["event_chain_digest"])

    def test_lean_proof_is_bound_to_same_accepted_chain(self) -> None:
        artifact = self.load_sequence()
        lean = LEAN_M2_PATH.read_text(encoding="utf-8")

        accepted = [
            event for event in artifact["events"] if event["expected_decision"]["accepted"]
        ]
        candidate_digests = [
            "8b00933f5ccf3d497f12b4d11ea547bede001afc95508548b097ad5d593d677c",
            *[event["expected_state_digest_after"] for event in accepted],
        ]
        for digest in candidate_digests:
            self.assertIn(digest, lean)
        for event in accepted:
            self.assertIn(event["proposal_digest"], lean)
            self.assertIn(f"serializedBytes := {event['serialized_bytes']}", lean)

        self.assertIn(FROZEN_FORMAL_OBJECT_SHA256, lean)
        self.assertIn(artifact["genesis"]["genesis_digest"], lean)
        self.assertIn(artifact["event_chain_digest"], lean)

    def test_manifest_keeps_m2_non_promotable_and_content_bound(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        mechanization = manifest["mechanization"]
        m2 = mechanization["m2_tranche"]

        self.assertFalse(manifest["promotion_ready"])
        self.assertEqual(mechanization["must_bind_to_formal_object_sha256"], FROZEN_FORMAL_OBJECT_SHA256)
        self.assertEqual(m2["id"], "M2")
        self.assertEqual(m2["issue"], 106)

        m1_paths = {record["path"] for record in mechanization["proof_artifacts"]}
        self.assertIn("lakefile.toml", m1_paths)
        self.assertIn(".github/workflows/rsi-ccc-lean.yml", m1_paths)
        self.assertNotIn("governance/rsi_ccc_wp00/m1_retained/lakefile.toml", m1_paths)
        self.assertNotIn("governance/rsi_ccc_wp00/m1_retained/rsi-ccc-lean.yml", m1_paths)

        records = m2["evidence_artifacts"]
        paths = {record["path"] for record in records}
        self.assertIn("lean/RSICCCM2.lean", paths)
        self.assertIn("governance/rsi_ccc_wp00/m2_sequence.json", paths)
        self.assertIn("src/grand_intellect/rsi_ccc_wp00_m2.py", paths)
        self.assertIn("governance/rsi_ccc_wp00/m2_test_rsi_ccc_wp00_m2.py", paths)
        self.assertIn("tests/test_rsi_ccc_wp00_m2_resource_laundering.py", paths)
        self.assertIn(".github/workflows/rsi-ccc-m2.yml", paths)
        self.assertIn("governance/rsi_ccc_wp00/m2_routing_registry.json", paths)
        self.assertNotIn(".ghos-routing/workflows.json", paths)

        for record in records:
            data = (ROOT / record["path"]).read_bytes()
            self.assertEqual(git_blob_sha(data), record["git_blob_sha"])


if __name__ == "__main__":
    unittest.main()
