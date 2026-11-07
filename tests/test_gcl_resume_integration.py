"""RWP-002 integration: checkpoint -> executor receipt -> provider readback and claims.

All providers in this file are deterministic fixtures. Live GitHub evidence must be
fetched by GithubCLIReadback; no mock output authorizes production actions.
"""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from threading import Lock, Thread
import unittest

from scripts.gcl_resume import (
    ContractError, KEY_VERSION, decide, record_for_job, validate_continuation,
)
from scripts.gcl_rwp_integrity import (
    acquire_github_claim, execute_nonproduction_fixture,
    fixture_record, verify_github_job,
)

SHA = "a" * 40
RUN_ID = 424242
REPO = "grandchallenge/INTELLECT"
JOB = {"record_type": "GCL_BOUNDED_JOB/1", "work_id": "RWP-002-CANARY",
       "step_id": "integration-check", "repository": REPO,
       "effect_class": "READ_ONLY", "action": "PYTHON_UNITTEST",
       "test_file": "test_gcl_resume_integration.py"}


class FakeGithub:
    def __init__(self, job=JOB, sha=SHA):
        self.record = record_for_job(job, sha)
        self.key = validate_continuation(self.record)
        self.refs = {}
        self.lock = Lock()
        self.create_calls = 0
        self.fixture_calls = 0
        self.lost_ack = False
        self.lost_fixture_ack = False
        self.move_main_on_claim = False
        self.fail_artifact = False
        self.remote = {
            "run": {"id": RUN_ID, "event": "workflow_dispatch",
                    "head_sha": sha, "head_branch": "main",
                    "name": "Agent continuity policy", "status": "completed",
                    "conclusion": "success", "run_attempt": 1},
            "jobs": {"total_count": 2, "jobs": [
                {"name": "Validate continuity contract", "status": "completed", "conclusion": "success"},
                {"name": "Execute exact-source bounded task", "status": "completed", "conclusion": "success"}]},
            "artifacts": {"total_count": 1, "artifacts": [
                {"id": 712, "name": f"gcl-rwp-{RUN_ID}-1", "expired": False,
                 "workflow_run": {"id": RUN_ID}, "digest": "sha256:" + "b" * 64}]},
            "main": {"commit": {"sha": sha}},
        }
        self.receipt = {
            "record_type": "GCL_BOUNDED_EXECUTION_RECEIPT/1",
            "work_id": job["work_id"], "step_id": job["step_id"],
            "operation_key": self.key, "operation_key_version": KEY_VERSION,
            "target_digest": self.record["target_digest"],
            "repository": REPO, "source_sha": sha,
            "run_id": str(RUN_ID), "run_attempt": "1", "result": "PASSED",
            "output_sha256": "c" * 64,
            "evidence_kind": "GITHUB_ACTIONS_TEST_EXECUTION",
            "mathematical_certification": False, "external_mutation": False,
            "created_utc": "2026-11-07T10:00:00Z"}

    def api_json(self, path):
        if path.endswith("/branches/main"):
            return copy.deepcopy(self.remote["main"])
        if path.endswith("/actions/runs/" + str(RUN_ID)):
            return copy.deepcopy(self.remote["run"])
        if path.endswith("/jobs?per_page=100"):
            return copy.deepcopy(self.remote["jobs"])
        if path.endswith("/artifacts?per_page=100"):
            return copy.deepcopy(self.remote["artifacts"])
        if "/git/ref/heads/gcl-rwp-claims/" in path or "/git/ref/heads/gcl-rwp-fixtures/" in path:
            key = path.split("/")[-1]
            prefix = "refs/heads/gcl-rwp-claims/" if "/gcl-rwp-claims/" in path else "refs/heads/gcl-rwp-fixtures/"
            ref = prefix + key
            if ref not in self.refs:
                raise ContractError("NOT_FOUND")
            return {"ref": ref, "object": {"sha": self.refs[ref]}}
        raise ContractError("UNEXPECTED_API_PATH: " + path)

    def artifact_json(self, repository, run_id, name):
        if self.fail_artifact:
            raise ContractError("ARTIFACT_UNAVAILABLE")
        return (json.dumps(self.receipt, sort_keys=True) + "\n").encode()

    def create_fixture(self, repository, ref, sha):
        with self.lock:
            self.fixture_calls += 1
            if ref in self.refs:
                raise ContractError("FIXTURE_EXISTS")
            self.refs[ref] = sha
            if self.lost_fixture_ack:
                raise ContractError("RESPONSE_LOST_AFTER_FIXTURE")
            return {"ref": ref, "object": {"sha": sha}}

    def create_claim(self, repository, ref, sha):
        with self.lock:
            self.create_calls += 1
            if ref in self.refs:
                raise ContractError("CLAIM_EXISTS")
            self.refs[ref] = sha
            if self.move_main_on_claim:
                self.remote["main"]["commit"]["sha"] = "f" * 40
            if self.lost_ack:
                raise ContractError("RESPONSE_LOST_AFTER_EFFECT")
            return {"ref": ref, "object": {"sha": sha}}


class VerifiedJobTests(unittest.TestCase):
    def setUp(self):
        self.provider = FakeGithub()
        self.record = self.provider.record

    def verify(self):
        return verify_github_job(self.record, RUN_ID, self.provider)

    def test_exact_success_across_all_surfaces(self):
        decision = decide(self.record, {"signal": "NONE", "current_sha": SHA, "lease_epoch": 0})
        self.assertEqual(decision["operation_key"], self.provider.key)
        self.assertEqual(decision["action"], "DISPATCH_ELIGIBLE")
        self.assertTrue(decision["effect_authorized"])
        proof = self.verify()
        self.assertEqual(proof["operation_key"], decision["operation_key"])
        self.assertEqual(proof["artifact_id"], 712)
        self.assertEqual(proof["result"], "VERIFIED_READ_ONLY_EXECUTION")
        self.assertFalse(proof["external_mutation_verified"])
        self.assertEqual(proof["receipt_sha256"], hashlib.sha256(self.provider.artifact_json(REPO, RUN_ID, "")).hexdigest())

    def test_forged_receipt_and_wrong_target_fail(self):
        for field, bad in (("operation_key", "0" * 64),
                           ("target_digest", "0" * 64),
                           ("source_sha", "d" * 40),
                           ("result", "FAILED"), ("run_attempt", "9"),
                           ("external_mutation", True)):
            with self.subTest(field=field):
                provider = FakeGithub()
                provider.receipt[field] = bad
                with self.assertRaises(ContractError):
                    verify_github_job(self.record, RUN_ID, provider)

    def test_expired_artifact_fails_closed(self):
        self.provider.remote["artifacts"]["artifacts"][0]["expired"] = True
        with self.assertRaisesRegex(ContractError, "EXPIRED"):
            self.verify()

    def test_missing_artifact_bytes_fail_closed(self):
        self.provider.fail_artifact = True
        with self.assertRaises(ContractError):
            self.verify()

    def test_wrong_run_source_or_job_result_fail(self):
        changes = (("run", "head_sha", "d" * 40),
                   ("run", "conclusion", "failure"),
                   ("run", "head_branch", "unprotected"),
                   ("jobs", None, None))
        for bucket, key, val in changes:
            with self.subTest(bucket=bucket, key=key):
                provider = FakeGithub()
                if bucket == "jobs":
                    provider.remote[bucket]["jobs"][1]["conclusion"] = "failure"
                else:
                    provider.remote[bucket][key] = val
                with self.assertRaises(ContractError):
                    verify_github_job(self.record, RUN_ID, provider)

    def test_job_count_and_duplicate_artifact_fail(self):
        provider = FakeGithub()
        provider.remote["jobs"]["total_count"] = 101
        with self.assertRaisesRegex(ContractError, "INCOMPLETE"):
            verify_github_job(self.record, RUN_ID, provider)
        provider = FakeGithub()
        provider.remote["artifacts"]["artifacts"].append(copy.deepcopy(provider.remote["artifacts"]["artifacts"][0]))
        provider.remote["artifacts"]["total_count"] = 2
        with self.assertRaisesRegex(ContractError, "NOT_UNIQUE"):
            verify_github_job(self.record, RUN_ID, provider)

    def test_terminal_record_never_self_certifies(self):
        claim = {"operation_key": self.provider.key,
                 "remote_identity": f"github://actions/{RUN_ID}",
                 "artifact_sha256": "b" * 64}
        record = {**self.record, "state": "COMPLETE", "receipt": claim}
        decision = decide(record, {"signal": "REMOTE_EFFECT_VERIFIED", "current_sha": SHA, "lease_epoch": 0})
        self.assertEqual(decision["action"], "VERIFY_REMOTE")
        self.assertFalse(decision["effect_authorized"])
        self.assertEqual(verify_github_job(record, RUN_ID, self.provider)["result"],
                         "VERIFIED_READ_ONLY_EXECUTION")

    def test_stored_pointer_conflict_fails(self):
        proof = {"operation_key": self.provider.key,
                 "remote_identity": f"github://actions/{RUN_ID}",
                 "artifact_sha256": "0" * 64}
        value = {**self.record, "state": "COMPLETE", "receipt": proof}
        with self.assertRaisesRegex(ContractError, "STORED_POINTER_CONFLICTS"):
            verify_github_job(value, RUN_ID, self.provider)
        value["receipt"] = {**proof, "artifact_sha256": "b" * 64,
                            "remote_identity": "github://actions/999"}
        with self.assertRaisesRegex(ContractError, "STORED_POINTER_CONFLICTS"):
            verify_github_job(value, RUN_ID, self.provider)

    def test_successor_with_no_conversation_state(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "checkpoint.json"
            p.write_text(json.dumps({"record": self.record, "run_id": RUN_ID}))
            # New process/session can reconstruct from durable bytes + provider state.
            recovered = json.loads(p.read_text())
            self.assertEqual(verify_github_job(recovered["record"], recovered["run_id"],
                                                FakeGithub())["operation_key"], self.provider.key)


class AtomicClaimTests(unittest.TestCase):
    def setUp(self):
        self.provider = FakeGithub()
        self.record = {**self.provider.record, "effect_class": "EXTERNAL_MUTATION",
                       "work_id": "RWP-002-MUTATION-FIXTURE"}
        self.record["target_digest"] = "d" * 64

    def test_one_winner_two_competing_workers(self):
        results = []
        guard = Lock()
        def attempt():
            value = acquire_github_claim(self.record, self.provider)
            with guard:
                results.append(value["claim_state"])
        workers = [Thread(target=attempt) for _ in range(2)]
        for t in workers: t.start()
        for t in workers: t.join()
        self.assertEqual(results.count("CLAIM_CREATED_THIS_ATTEMPT"), 1)
        self.assertEqual(results.count("EXISTING_CLAIM_OUTCOME_UNCERTAIN"), 1)
        self.assertEqual(len(self.provider.refs), 1)

    def test_lost_ack_not_replayed(self):
        self.provider.lost_ack = True
        first = acquire_github_claim(self.record, self.provider)
        self.assertEqual(first["claim_state"], "EXISTING_CLAIM_OUTCOME_UNCERTAIN")
        self.assertFalse(first["effect_dispatch_authorized"])
        second = acquire_github_claim(self.record, self.provider)
        self.assertEqual(second["claim_state"], "EXISTING_CLAIM_OUTCOME_UNCERTAIN")
        self.assertEqual(len(self.provider.refs), 1)

    def test_moved_source_fail_closed(self):
        self.provider.remote["main"]["commit"]["sha"] = "f" * 40
        with self.assertRaisesRegex(ContractError, "PROTECTED_MAIN_MOVED"):
            acquire_github_claim(self.record, self.provider)
        self.assertEqual(self.provider.create_calls, 0)

    def test_claim_is_not_permission_to_mutate(self):
        claim = acquire_github_claim(self.record, self.provider)
        self.assertEqual(claim["claim_state"], "CLAIM_CREATED_THIS_ATTEMPT")
        self.assertFalse(claim["effect_dispatch_authorized"])
        decision = decide(self.record, {"signal": "NONE", "current_sha": SHA, "lease_epoch": 0})
        self.assertEqual(decision["action"], "CLAIM_REQUIRED")
        self.assertFalse(decision["effect_authorized"])

    def test_changed_target_changes_claim_identity(self):
        a = acquire_github_claim(self.record, self.provider)
        changed = {**self.record, "target_digest": "e" * 64}
        b = acquire_github_claim(changed, self.provider)
        self.assertNotEqual(a["operation_key"], b["operation_key"])
        self.assertEqual(len(self.provider.refs), 2)

    def test_stale_lease_prevents_pure_dispatch(self):
        decision = decide(self.record, {"signal": "NONE", "current_sha": SHA, "lease_epoch": 5})
        self.assertEqual(decision["action"], "FENCE_AND_RECONCILE")
        self.assertFalse(decision["effect_authorized"])


class NonproductionEffectFixtureTests(unittest.TestCase):
    def setUp(self):
        self.provider = FakeGithub()
        self.record = fixture_record(SHA)

    def test_one_effect_across_replay_and_successor(self):
        first = execute_nonproduction_fixture(self.record, self.provider)
        self.assertEqual(first["result"], "VERIFIED_NONPRODUCTION_REF_EFFECT")
        self.assertTrue(first["external_mutation_verified"])
        self.assertFalse(first["general_mutation_executor_authorized"])
        second = execute_nonproduction_fixture(json.loads(json.dumps(self.record)), self.provider)
        self.assertEqual(second["result"], "VERIFIED_NONPRODUCTION_REF_EFFECT")
        self.assertEqual(second["claim_state"], "EXISTING_CLAIM_OUTCOME_UNCERTAIN")
        self.assertEqual(self.provider.fixture_calls, 1)

    def test_lost_effect_ack_recovered_by_readback(self):
        self.provider.lost_fixture_ack = True
        first = execute_nonproduction_fixture(self.record, self.provider)
        self.assertEqual(first["result"], "VERIFIED_NONPRODUCTION_REF_EFFECT")
        second = execute_nonproduction_fixture(self.record, self.provider)
        self.assertEqual(second["result"], "VERIFIED_NONPRODUCTION_REF_EFFECT")
        self.assertEqual(self.provider.fixture_calls, 1)

    def test_claim_ack_lost_does_not_create_effect(self):
        self.provider.lost_ack = True
        first = execute_nonproduction_fixture(self.record, self.provider)
        self.assertEqual(first["result"], "OUTCOME_UNKNOWN_HOLD")
        self.assertEqual(self.provider.fixture_calls, 0)
        second = execute_nonproduction_fixture(self.record, self.provider)
        self.assertEqual(second["result"], "OUTCOME_UNKNOWN_HOLD")
        self.assertEqual(self.provider.fixture_calls, 0)

    def test_main_moves_after_claim_effect_is_not_sent(self):
        self.provider.move_main_on_claim = True
        outcome = execute_nonproduction_fixture(self.record, self.provider)
        self.assertEqual(outcome["result"], "OUTCOME_UNKNOWN_HOLD")
        self.assertEqual(self.provider.fixture_calls, 0)

    def test_wrong_target_denied(self):
        with self.assertRaisesRegex(ContractError, "NOT_FIXED_NONPRODUCTION_FIXTURE"):
            execute_nonproduction_fixture({**self.record, "target_digest": "0"*64}, self.provider)
        self.assertEqual(self.provider.create_calls, 0)

    def test_two_workers_one_effect(self):
        results = []
        guard = Lock()
        def attempt():
            out = execute_nonproduction_fixture(self.record, self.provider)
            with guard:
                results.append(out["result"])
        threads = [Thread(target=attempt) for _ in range(2)]
        for t in threads: t.start()
        for t in threads: t.join()
        self.assertEqual(results, ["VERIFIED_NONPRODUCTION_REF_EFFECT"]*2)
        self.assertEqual(self.provider.fixture_calls, 1)


if __name__ == "__main__":
    unittest.main()
