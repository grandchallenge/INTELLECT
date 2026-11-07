"""Adversarial GCL-RWP-001 continuation and bounded-worker tests."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.gcl_resume import ContractError, decide, read_job, validate_continuation, validate_job

SHA = "a" * 40
BASE = {
    "record_type": "GCL_CONTINUATION/1",
    "work_id": "RWP-001-PILOT",
    "step_id": "acceptance-tests",
    "repository": "grandchallenge/INTELLECT",
    "source_sha": SHA,
    "effect_class": "EXTERNAL_MUTATION",
    "target_digest": "b" * 64,
    "state": "INTENT_RECORDED",
    "attempts": 0,
    "lease_epoch": 7,
    "receipt": None,
}
OBS = {"signal": "NONE", "current_sha": SHA, "lease_epoch": 7}
JOB = {
    "record_type": "GCL_BOUNDED_JOB/1",
    "work_id": "RWP-001-SMOKE",
    "step_id": "unit-tests",
    "repository": "grandchallenge/INTELLECT",
    "effect_class": "READ_ONLY",
    "action": "PYTHON_UNITTEST",
    "test_file": "test_gcl_resume.py",
}

def record(**changes):
    return dict(BASE, **changes)

def obs(**changes):
    return dict(OBS, **changes)

class ContinuationTests(unittest.TestCase):
    def test_intent_can_dispatch(self):
        result = decide(record(), obs())
        self.assertEqual(result["action"], "DISPATCH_ELIGIBLE")
        self.assertTrue(result["effect_authorized"])

    def test_mutation_lost_response_never_replayed(self):
        for state in ("DISPATCHED", "OUTCOME_UNKNOWN"):
            for signal in ("TRANSIENT", "RESPONSE_LOST", "REMOTE_NOT_FOUND"):
                with self.subTest(state=state, signal=signal):
                    result = decide(record(state=state), obs(signal=signal))
                    self.assertEqual(result["action"], "RECONCILE_REMOTE")
                    self.assertFalse(result["effect_authorized"])

    def test_denial_scoped_and_siblings_eligible(self):
        result = decide(record(), obs(signal="EXPLICIT_DENIAL"))
        self.assertEqual(result["action"], "HOLD_EXACT_OPERATION")
        self.assertFalse(result["effect_authorized"])
        self.assertTrue(result["independent_siblings_eligible"])
        self.assertEqual(decide(record(state="POLICY_HELD"), obs())["action"], "HOLD_EXACT_OPERATION")

    def test_read_only_retries_bounded(self):
        for n in range(3):
            result = decide(record(effect_class="READ_ONLY", state="DISPATCHED", attempts=n), obs(signal="TRANSIENT"))
            self.assertEqual(result["action"], "RETRY_BOUNDED_READ")
        result = decide(record(effect_class="READ_ONLY", state="DISPATCHED", attempts=3), obs())
        self.assertEqual(result["action"], "DEFER_FOR_REVIEW")

    def test_lease_fence(self):
        result = decide(record(state="DISPATCHED"), obs(lease_epoch=8))
        self.assertEqual(result["action"], "FENCE_AND_RECONCILE")
        self.assertFalse(result["effect_authorized"])

    def test_source_movement(self):
        result = decide(record(), obs(current_sha="c" * 40))
        self.assertEqual(result["action"], "REVALIDATE_SOURCE")

    def test_authority_boundary(self):
        self.assertEqual(decide(record(), obs(signal="AUTHORITY_DENIAL"))["action"], "HOLD_AUTHORITY")

    def test_matching_remote_readback(self):
        key = validate_continuation(record())
        receipt = {"operation_key": key, "remote_identity": "github://run/123",
                   "verified_by_readback": True}
        self.assertEqual(decide(record(state="EFFECT_VERIFIED", receipt=receipt), obs())["action"], "ADVANCE_VERIFIED")
        self.assertEqual(decide(record(state="COMPLETE", receipt=receipt), obs())["action"], "ALREADY_COMPLETE")
        with self.assertRaises(ContractError):
            validate_continuation(record(state="COMPLETE", receipt={**receipt, "operation_key": "0" * 64}))

    def test_ack_is_not_effect(self):
        key = validate_continuation(record())
        receipt = {"operation_key": key, "remote_identity": "mcp-reply",
                   "verified_by_readback": False}
        with self.assertRaises(ContractError):
            validate_continuation(record(state="COMPLETE", receipt=receipt))

    def test_identity_stable_but_target_bound(self):
        self.assertEqual(validate_continuation(record()), validate_continuation(copy.deepcopy(record())))
        self.assertNotEqual(validate_continuation(record()), validate_continuation(record(target_digest="c" * 64)))
        self.assertNotEqual(validate_continuation(record()), validate_continuation(record(source_sha="d" * 40)))

    def test_invalid_state_and_metadata(self):
        invalid = [record(attempts=True), record(lease_epoch=-1), record(source_sha="main"),
                   record(target_digest="bad"), record(state="COMPLETE"),
                   {**record(), "extra": 1}]
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises(ContractError):
                    validate_continuation(value)

class BoundedJobTests(unittest.TestCase):
    def test_valid_job(self):
        self.assertEqual(validate_job(JOB)["action"], "PYTHON_UNITTEST")

    def test_unsupported_effect_and_injection(self):
        bad = [{"action": "SHELL"}, {"effect_class": "EXTERNAL_MUTATION"},
               {"test_file": "../../etc/passwd"},
               {"test_file": "test_good.py; echo unsafe"},
               {"test_file": "setup.py"}]
        for change in bad:
            with self.subTest(change=change):
                with self.assertRaises(ContractError):
                    validate_job(dict(JOB, **change))

    def test_restrict_capsule_path_and_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            path = root / "governance/agent_execution/jobs/RWP-001-SMOKE.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(JOB), encoding="utf-8")
            self.assertEqual(read_job(root, "governance/agent_execution/jobs/RWP-001-SMOKE.json")["work_id"], JOB["work_id"])
            for bad in ("../job.json", "/etc/passwd", "governance/agent_execution/../../x.json"):
                with self.subTest(bad=bad), self.assertRaises(ContractError):
                    read_job(root, bad)
            path.unlink()
            path.symlink_to(root / "other.json")
            with self.assertRaises(ContractError):
                read_job(root, "governance/agent_execution/jobs/RWP-001-SMOKE.json")

if __name__ == "__main__":
    unittest.main()
