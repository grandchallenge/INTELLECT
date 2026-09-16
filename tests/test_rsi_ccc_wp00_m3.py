from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha1
import json
from pathlib import Path
import unittest

from grand_intellect.rsi_ccc_wp00 import baseline_candidate, sha256_json
from grand_intellect.rsi_ccc_wp00_m2_receipts import (
    CHECKER_DIGEST,
    EVALUATION_CONTEXT_DIGEST,
    FROZEN_FORMAL_OBJECT_SHA256,
    KERNEL_DIGEST,
    POLICY_DIGEST,
    RESOURCE_ENVELOPE_DIGEST,
)
from grand_intellect.rsi_ccc_wp00_m3 import (
    M3ReplayError,
    evaluate_committed_envelope,
    generated_m3_artifact,
    public_state_view,
    replay_m3_artifact,
)
from grand_intellect.rsi_ccc_wp00_m3_proposer import (
    OBJECTIVE_DIGEST,
    ProposerPrivateState,
    clone_with_private_identity,
    generate_committed_envelope,
)

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "m3_proposer_evidence.json"
M3_MANIFEST_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "m3_manifest.json"
PROPOSER_PATH = ROOT / "src" / "grand_intellect" / "rsi_ccc_wp00_m3_proposer.py"
CHECKER_PATH = ROOT / "src" / "grand_intellect" / "rsi_ccc_wp00.py"
FORMAL_OBJECT_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "formal_object.json"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


def first_envelope():
    old = baseline_candidate()
    envelope = generate_committed_envelope(
        public_state_view(old),
        ProposerPrivateState("bounded-search-proposer-A", "m3-prefix-cost-v1", 0),
    )
    assert envelope is not None
    return old, envelope


def recommit(envelope: dict[str, object]) -> dict[str, object]:
    envelope["proposal_digest"] = sha256_json(envelope["proposal"])
    body = dict(envelope)
    body.pop("transcript_digest", None)
    envelope["transcript_digest"] = sha256_json(body)
    return envelope


class RsiCccWp00M3Tests(unittest.TestCase):
    def load_artifact(self) -> dict[str, object]:
        return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

    def test_artifact_is_exact_generated_replay(self) -> None:
        artifact = self.load_artifact()
        self.assertEqual(artifact, generated_m3_artifact())
        result = replay_m3_artifact(artifact)
        self.assertEqual(result.accepted_transition_count, 5)
        self.assertEqual(result.final_candidate_digest, "4f0b7070b8e32d839f2d296bea9bb4ce3981aa0100e71605f4cf3dc45fe02b03")
        self.assertEqual(result.transcript_chain_digest, "295b815b1a14c4453da824d28c7e85309799678b737f274c795ebddd0704a008")
        self.assertEqual(result.independent_certificate_chain_digest, "7120c0be21626ab9a29b61a71f5a7837ea4c1cb163be54592d3f2f20d89411d8")

    def test_bounded_proposer_materially_generates_mixed_sequence(self) -> None:
        proposal_digests = [event["proposal_digest"] for event in self.load_artifact()["events"]]
        self.assertEqual(proposal_digests, [
            "c48b9eb1f664658e4e00e7192317b36be38e389804087c71d3f3bfc5afffe690",
            "5d132973675d8e54fcd31a12c7b2b9ff4ce520aa52f7dd1da6750fc00652a30a",
            "e35745452befafd849fc7d83ff2cc630e8f93538733e9a72f8418058b7f715e4",
            "205aadc286496c225737d967fab9b07b7f83cf332da1000a1606abbdc543978c",
            "a01b2d61440704a22dea5d3252c3bae1d3bf9820029de4667133d7339cba23f7",
        ])

    def test_proposer_private_identity_does_not_change_independent_certificate(self) -> None:
        old, envelope_a = first_envelope()
        envelope_b = clone_with_private_identity(envelope_a, ProposerPrivateState("different-proposer", "private-state-B", 1001))
        result_a = evaluate_committed_envelope(old, envelope_a)
        result_b = evaluate_committed_envelope(old, envelope_b)
        self.assertTrue(result_a.accepted and result_b.accepted)
        self.assertNotEqual(envelope_a["transcript_digest"], envelope_b["transcript_digest"])
        self.assertEqual(result_a.proposal_digest, result_b.proposal_digest)
        self.assertEqual(result_a.certificate_digest, result_b.certificate_digest)
        self.assertEqual(result_a.next_state.digest, result_b.next_state.digest)

    def test_proposer_has_no_checker_or_external_resource_import(self) -> None:
        source = PROPOSER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        self.assertTrue(roots.issubset({"__future__", "dataclasses", "hashlib", "json", "typing"}))
        self.assertNotIn("grand_intellect.rsi_ccc_wp00", source)

    def test_forged_evidence_and_metric_are_rejected(self) -> None:
        old, envelope = first_envelope()
        for key, value in (
            ("certificate", {"accepted": True, "code": "accepted"}),
            ("metric", {"name": "proposer-defined", "score": 0}),
        ):
            mutated = deepcopy(envelope)
            mutated["proposal"][key] = value
            recommit(mutated)
            result = evaluate_committed_envelope(old, mutated)
            self.assertFalse(result.accepted)
            self.assertEqual(result.code, "malformed")

    def test_stale_predecessor_is_rejected_after_valid_commit(self) -> None:
        old, envelope0 = first_envelope()
        first = evaluate_committed_envelope(old, envelope0)
        current = first.next_state
        envelope1 = generate_committed_envelope(public_state_view(current), ProposerPrivateState("bounded-search-proposer-A", "m3-prefix-cost-v1", 1))
        assert envelope1 is not None
        mutated = deepcopy(envelope1)
        mutated["proposal"]["base_digest"] = old.digest
        recommit(mutated)
        result = evaluate_committed_envelope(current, mutated)
        self.assertFalse(result.accepted)
        self.assertEqual(result.code, "stale_base")

    def test_context_and_kernel_substitution_are_rejected(self) -> None:
        old, envelope = first_envelope()
        for field, value, code in (
            ("context_id", "attacker-context-v9", "context_substitution"),
            ("kernel_id", "attacker-kernel-v9", "trust_kernel_mutation"),
        ):
            mutated = deepcopy(envelope)
            mutated["proposal"][field] = value
            mutated["proposal"]["candidate"][field] = value
            mutated["proposal"]["candidate_digest"] = sha256_json(mutated["proposal"]["candidate"])
            recommit(mutated)
            result = evaluate_committed_envelope(old, mutated)
            self.assertFalse(result.accepted)
            self.assertEqual(result.code, code)

    def test_resource_policy_and_transcript_smuggling_fail_closed(self) -> None:
        old, envelope = first_envelope()
        proposal_mutation = deepcopy(envelope)
        proposal_mutation["proposal"]["max_declared_cost"] = 999999999
        recommit(proposal_mutation)
        self.assertEqual(evaluate_committed_envelope(old, proposal_mutation).code, "malformed")

        top_level = deepcopy(envelope)
        top_level["policy_digest"] = "proposer-policy"
        self.assertEqual(evaluate_committed_envelope(old, top_level).code, "malformed_envelope")

        transcript_mutation = deepcopy(envelope)
        transcript_mutation["private_state_digest"] = "00" * 32
        self.assertEqual(evaluate_committed_envelope(old, transcript_mutation).code, "transcript_mismatch")

        objective_mutation = deepcopy(envelope)
        objective_mutation["objective_digest"] = "11" * 32
        body = dict(objective_mutation)
        body.pop("transcript_digest")
        objective_mutation["transcript_digest"] = sha256_json(body)
        self.assertEqual(evaluate_committed_envelope(old, objective_mutation).code, "objective_mismatch")

    def test_receipt_reuse_against_new_state_is_rejected(self) -> None:
        old, envelope = first_envelope()
        first = evaluate_committed_envelope(old, envelope)
        replay = evaluate_committed_envelope(first.next_state, envelope)
        self.assertFalse(replay.accepted)
        self.assertEqual(replay.code, "public_state_mismatch")

    def test_receipt_and_certificate_lineage_recomputes(self) -> None:
        artifact = self.load_artifact()
        previous_receipt = artifact["events"][0]["previous_transcript_receipt_digest"]
        previous_certificate = artifact["events"][0]["previous_certificate_digest"]
        for event in artifact["events"]:
            self.assertEqual(event["previous_transcript_receipt_digest"], previous_receipt)
            self.assertEqual(event["previous_certificate_digest"], previous_certificate)
            self.assertEqual(event["checker_digest"], CHECKER_DIGEST)
            self.assertEqual(event["formal_object_sha256"], FROZEN_FORMAL_OBJECT_SHA256)
            self.assertEqual(event["policy_digest"], POLICY_DIGEST)
            self.assertEqual(event["evaluation_context_digest"], EVALUATION_CONTEXT_DIGEST)
            self.assertEqual(event["kernel_digest"], KERNEL_DIGEST)
            self.assertEqual(event["resource_envelope_digest"], RESOURCE_ENVELOPE_DIGEST)
            self.assertEqual(event["objective_digest"], OBJECTIVE_DIGEST)
            body = dict(event)
            retained = body.pop("receipt_digest")
            self.assertEqual(sha256_json(body), retained)
            previous_receipt = retained
            previous_certificate = event["certificate_digest"]
        self.assertEqual(previous_receipt, artifact["transcript_chain_digest"])
        self.assertEqual(previous_certificate, artifact["independent_certificate_chain_digest"])

    def test_tampered_artifact_fails_exact_replay(self) -> None:
        artifact = deepcopy(self.load_artifact())
        artifact["events"][2]["private_state_digest"] = "22" * 32
        with self.assertRaises(M3ReplayError):
            replay_m3_artifact(artifact)

    def test_frozen_checker_and_formal_object_are_byte_stable(self) -> None:
        self.assertEqual(git_blob_sha(CHECKER_PATH.read_bytes()), "e4ad8cef6fdf514c2aad0dbac372b3a42f5e6dbb")
        self.assertEqual(git_blob_sha(FORMAL_OBJECT_PATH.read_bytes()), "8baee8d3a1f50a4d527afdc29747a0fa563451bb")

    def test_m3_manifest_binds_all_evidence_and_remains_non_promotable(self) -> None:
        manifest = json.loads(M3_MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertFalse(manifest["promotion_ready"])
        self.assertEqual(manifest["issue"], 108)
        self.assertEqual(manifest["objective_digest"], OBJECTIVE_DIGEST)
        self.assertEqual(manifest["transcript_chain_digest"], "295b815b1a14c4453da824d28c7e85309799678b737f274c795ebddd0704a008")
        self.assertEqual(manifest["independent_certificate_chain_digest"], "7120c0be21626ab9a29b61a71f5a7837ea4c1cb163be54592d3f2f20d89411d8")
        for record in manifest["evidence_artifacts"]:
            self.assertEqual(git_blob_sha((ROOT / record["path"]).read_bytes()), record["git_blob_sha"])


if __name__ == "__main__":
    unittest.main()
