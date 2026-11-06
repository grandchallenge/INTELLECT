"""GCL-RWP-001: bounded, interruption-resilient work and read-only job execution.

GitHub remains the durable authority. No automatic remote mutation is exposed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

RECORD = "GCL_CONTINUATION/1"
JOB = "GCL_BOUNDED_JOB/1"
RECEIPT = "GCL_BOUNDED_EXECUTION_RECEIPT/1"
HEX = re.compile(r"[0-9a-f]{64}\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")
IDENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{2,95}\Z")
REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
TEST_FILE = re.compile(r"test_[A-Za-z0-9_]+\.py\Z")
JOB_PATH = re.compile(r"governance/agent_execution/jobs/[A-Za-z0-9_-]+\.json\Z")
STATES = {"INTENT_RECORDED", "DISPATCHED", "OUTCOME_UNKNOWN",
          "POLICY_HELD", "EFFECT_VERIFIED", "COMPLETE"}
EFFECTS = {"READ_ONLY", "EXTERNAL_MUTATION"}
SIGNALS = {"NONE", "TRANSIENT", "RESPONSE_LOST", "EXPLICIT_DENIAL",
           "AUTHORITY_DENIAL", "REMOTE_EFFECT_VERIFIED",
           "LEASE_EXPIRED", "REMOTE_NOT_FOUND"}

class ContractError(ValueError):
    pass

def require(test: bool, reason: str) -> None:
    if not test:
        raise ContractError(reason)

def digest(value: object) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()

def validate_continuation(record: dict) -> str:
    require(type(record) is dict, "RECORD_OBJECT_REQUIRED")
    fields = {"record_type", "work_id", "step_id", "repository", "source_sha",
              "effect_class", "target_digest", "state", "attempts",
              "lease_epoch", "receipt"}
    require(set(record) == fields, "RECORD_FIELDS_INVALID")
    require(record["record_type"] == RECORD, "RECORD_TYPE_INVALID")
    for field in ("work_id", "step_id"):
        require(isinstance(record[field], str) and IDENT.fullmatch(record[field]) is not None, field + "_INVALID")
    require(isinstance(record["repository"], str) and REPO.fullmatch(record["repository"]) is not None, "REPOSITORY_INVALID")
    require(isinstance(record["source_sha"], str) and SHA.fullmatch(record["source_sha"]) is not None, "SOURCE_SHA_INVALID")
    require(record["effect_class"] in EFFECTS, "EFFECT_CLASS_INVALID")
    require(isinstance(record["target_digest"], str) and HEX.fullmatch(record["target_digest"]) is not None, "TARGET_DIGEST_INVALID")
    require(record["state"] in STATES, "STATE_INVALID")
    require(type(record["attempts"]) is int and record["attempts"] >= 0, "ATTEMPTS_INVALID")
    require(type(record["lease_epoch"]) is int and record["lease_epoch"] >= 0, "LEASE_EPOCH_INVALID")
    key = digest({k: record[k] for k in
       ("work_id", "step_id", "repository", "source_sha", "effect_class", "target_digest")})
    receipt = record["receipt"]
    if receipt is not None:
        require(type(receipt) is dict and set(receipt) == {"operation_key", "remote_identity", "verified_by_readback"}, "RECEIPT_FIELDS_INVALID")
        require(receipt["operation_key"] == key, "RECEIPT_OPERATION_CONFLICT")
        require(isinstance(receipt["remote_identity"], str) and receipt["remote_identity"].strip() != "", "REMOTE_IDENTITY_REQUIRED")
        require(type(receipt["verified_by_readback"]) is bool, "RECEIPT_VERIFICATION_INVALID")
    if record["state"] in {"EFFECT_VERIFIED", "COMPLETE"}:
        require(receipt is not None and receipt["verified_by_readback"], "TERMINAL_REQUIRES_READBACK")
    return key

def decide(record: dict, observation: dict) -> dict:
    """Pure recovery decision. Does not dispatch or replay effects."""
    key = validate_continuation(record)
    require(type(observation) is dict and set(observation) == {"signal", "current_sha", "lease_epoch"}, "OBSERVATION_FIELDS_INVALID")
    require(observation["signal"] in SIGNALS, "SIGNAL_INVALID")
    require(isinstance(observation["current_sha"], str) and SHA.fullmatch(observation["current_sha"]) is not None, "OBSERVED_HEAD_INVALID")
    require(type(observation["lease_epoch"]) is int and observation["lease_epoch"] >= 0, "OBSERVED_LEASE_INVALID")
    if record["state"] == "COMPLETE":
        action = "ALREADY_COMPLETE"
    elif record["state"] == "EFFECT_VERIFIED" or (
        observation["signal"] == "REMOTE_EFFECT_VERIFIED" and record["receipt"] is not None
        and record["receipt"]["verified_by_readback"]
    ):
        action = "ADVANCE_VERIFIED"
    elif record["state"] == "POLICY_HELD" or observation["signal"] == "EXPLICIT_DENIAL":
        action = "HOLD_EXACT_OPERATION"
    elif observation["signal"] == "AUTHORITY_DENIAL":
        action = "HOLD_AUTHORITY"
    elif observation["lease_epoch"] != record["lease_epoch"]:
        action = "FENCE_AND_RECONCILE"
    elif observation["current_sha"] != record["source_sha"]:
        action = "REVALIDATE_SOURCE"
    elif record["state"] in {"DISPATCHED", "OUTCOME_UNKNOWN"} and record["effect_class"] == "EXTERNAL_MUTATION":
        action = "RECONCILE_REMOTE"
    elif observation["signal"] == "LEASE_EXPIRED":
        action = "FENCE_AND_RECONCILE"
    elif record["state"] in {"DISPATCHED", "OUTCOME_UNKNOWN"}:
        action = "RETRY_BOUNDED_READ" if record["attempts"] < 3 else "DEFER_FOR_REVIEW"
    elif observation["signal"] in {"TRANSIENT", "RESPONSE_LOST"}:
        action = "RETRY_BOUNDED_READ" if record["effect_class"] == "READ_ONLY" and record["attempts"] < 3 else "RECONCILE_REMOTE"
    elif record["state"] == "INTENT_RECORDED" and observation["signal"] == "NONE":
        action = "DISPATCH_ELIGIBLE"
    else:
        action = "RECONCILE_REMOTE"
    return {"record_type": "GCL_RESUME_DECISION/1", "work_id": record["work_id"],
            "step_id": record["step_id"], "operation_key": key,
            "action": action, "effect_authorized": action in {"DISPATCH_ELIGIBLE", "RETRY_BOUNDED_READ"},
            "independent_siblings_eligible": True, "source_sha": record["source_sha"]}

def validate_job(job: dict) -> dict:
    require(type(job) is dict, "JOB_OBJECT_REQUIRED")
    require(set(job) == {"record_type", "work_id", "step_id", "repository", "effect_class", "action", "test_file"}, "JOB_FIELDS_INVALID")
    require(job["record_type"] == JOB, "JOB_TYPE_INVALID")
    for field in ("work_id", "step_id"):
        require(isinstance(job[field], str) and IDENT.fullmatch(job[field]) is not None, field + "_INVALID")
    require(isinstance(job["repository"], str) and REPO.fullmatch(job["repository"]) is not None, "JOB_REPOSITORY_INVALID")
    require(job["effect_class"] == "READ_ONLY" and job["action"] == "PYTHON_UNITTEST", "UNSUPPORTED_EFFECT_OR_ACTION")
    require(isinstance(job["test_file"], str) and TEST_FILE.fullmatch(job["test_file"]) is not None, "TEST_FILE_INVALID")
    return job

def read_job(root: Path, job_path: str) -> dict:
    require(isinstance(job_path, str) and JOB_PATH.fullmatch(job_path) is not None, "JOB_PATH_INVALID")
    path = root / job_path
    require(path.is_file() and not path.is_symlink(), "JOB_NOT_REGULAR_FILE")
    return validate_job(json.loads(path.read_text(encoding="utf-8")))

def run_job(job_path: str, output: str) -> int:
    """Run a fixed, read-only unit-test job and emit a GitHub Actions receipt."""
    root = Path.cwd()
    job = read_job(root, job_path)
    sha = os.environ.get("GITHUB_SHA", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "")
    require(SHA.fullmatch(sha) is not None, "RUN_SHA_MISSING")
    require(repo == job["repository"], "JOB_REPOSITORY_MISMATCH")
    require(run_id.isdecimal() and int(run_id) > 0 and attempt.isdecimal() and int(attempt) > 0, "RUN_ID_MISSING")
    actual = subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True, timeout=10, check=True).stdout.strip()
    require(actual == sha, "RUN_SOURCE_NOT_EXACT")
    test_path = root / "tests" / job["test_file"]
    require(test_path.is_file() and not test_path.is_symlink(), "TEST_FILE_NOT_TRACKED")
    key = digest({"work_id": job["work_id"], "step_id": job["step_id"],
                  "repository": repo, "source_sha": sha,
                  "action": job["action"], "test_file": job["test_file"]})
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", job["test_file"], "-v"]
    try:
        p = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=240, check=False)
        result = "PASSED" if p.returncode == 0 else "FAILED"
        code = 0 if p.returncode == 0 else 1
        output_digest = hashlib.sha256((p.stdout + p.stderr).encode()).hexdigest()
    except subprocess.TimeoutExpired:
        result, code, output_digest = "TIMED_OUT", 1, None
    receipt = {"record_type": RECEIPT, "work_id": job["work_id"],
               "step_id": job["step_id"], "operation_key": key,
               "repository": repo, "source_sha": sha,
               "run_id": run_id, "run_attempt": attempt,
               "result": result, "output_sha256": output_digest,
               "evidence_kind": "GITHUB_ACTIONS_TEST_EXECUTION",
               "mathematical_certification": False, "external_mutation": False,
               "created_utc": datetime.now(timezone.utc).isoformat()}
    dest = Path(output)
    require(not dest.is_symlink(), "OUTPUT_SYMLINK_FORBIDDEN")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".pending")
    tmp.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    tmp.replace(dest)
    print(json.dumps(receipt, sort_keys=True))
    return code

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("decide")
    p.add_argument("--record", required=True)
    p.add_argument("--observation", required=True)
    p = sub.add_parser("validate-job")
    p.add_argument("--job-path", required=True)
    p = sub.add_parser("execute")
    p.add_argument("--job-path", required=True)
    p.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.mode == "decide":
            record = json.loads(Path(args.record).read_text(encoding="utf-8"))
            obs = json.loads(Path(args.observation).read_text(encoding="utf-8"))
            print(json.dumps(decide(record, obs), sort_keys=True))
        elif args.mode == "validate-job":
            print(json.dumps(read_job(Path.cwd(), args.job_path), sort_keys=True))
        else:
            return run_job(args.job_path, args.output)
    except (ContractError, ValueError, OSError, subprocess.SubprocessError) as exc:
        print("GCL_RWP_REJECTED: " + str(exc), file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
