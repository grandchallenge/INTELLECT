"""GCL-RWP-002: authenticated GitHub readback and atomic nonproduction claim gate.

External effects are not dispatched by this module.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from scripts.gcl_resume import (
    ContractError, HEX, KEY_VERSION, SHA, require, validate_continuation,
)

VERIFICATION = "GCL_RUN_VERIFICATION/1"
CLAIM = "GCL_GITHUB_REF_CLAIM/1"


class GithubCLIReadback:
    """Authenticated GitHub CLI transport, without exposing credentials."""

    def _call(self, args: list[str], *, timeout: int = 50) -> str:
        p = subprocess.run(["gh", *args], capture_output=True, text=True,
                           timeout=timeout, check=False)
        if p.returncode:
            raise ContractError("GITHUB_AUTHENTICATED_READBACK_FAILED")
        return p.stdout

    def api_json(self, path: str) -> dict:
        require(path.startswith("repos/grandchallenge/"), "API_PATH_NOT_GCL")
        return json.loads(self._call(["api", "--method", "GET", path]))

    def artifact_json(self, repository: str, run_id: int, name: str) -> bytes:
        require(repository == "grandchallenge/INTELLECT", "ARTIFACT_REPOSITORY_INVALID")
        require(name.startswith("gcl-rwp-") and "/" not in name, "ARTIFACT_NAME_INVALID")
        with tempfile.TemporaryDirectory() as d:
            self._call(["run", "download", str(run_id), "--repo", repository,
                        "--name", name, "--dir", d], timeout=120)
            base = Path(d)
            files = list(base.iterdir())
            require(len(files) == 1 and files[0].name == "gcl-rwp-receipt.json",
                    "ARTIFACT_MEMBERS_INVALID")
            file = files[0]
            require(file.is_file() and not file.is_symlink(), "ARTIFACT_FILE_INVALID")
            require(file.stat().st_size <= 32768, "ARTIFACT_TOO_LARGE")
            return file.read_bytes()

    def create_fixture(self, repository: str, ref: str, sha: str) -> dict:
        require(repository == "grandchallenge/INTELLECT", "FIXTURE_REPOSITORY_INVALID")
        require(ref.startswith("refs/heads/gcl-rwp-fixtures/"), "FIXTURE_REF_INVALID")
        require(SHA.fullmatch(sha) is not None, "FIXTURE_SHA_INVALID")
        return json.loads(self._call(["api", "--method", "POST",
            f"repos/{repository}/git/refs", "-f", f"ref={ref}",
            "-f", f"sha={sha}"]))

    def create_claim(self, repository: str, ref: str, sha: str) -> dict:
        require(repository == "grandchallenge/INTELLECT", "CLAIM_REPOSITORY_INVALID")
        require(ref.startswith("refs/heads/gcl-rwp-claims/"), "CLAIM_REF_INVALID")
        require(SHA.fullmatch(sha) is not None, "CLAIM_SHA_INVALID")
        return json.loads(self._call(["api", "--method", "POST",
            f"repos/{repository}/git/refs", "-f", f"ref={ref}",
            "-f", f"sha={sha}"]))


def verify_github_job(record: dict, run_id: int, provider: GithubCLIReadback) -> dict:
    """Verify real provider state, not a claimed success bit in the checkpoint.

    A mock provider is permitted for testing, never for a live verification claim.
    This verifier proves a bounded test execution, NOT an external effect.
    """
    key = validate_continuation(record)
    require(record["effect_class"] == "READ_ONLY", "EXTERNAL_EFFECT_VERIFIER_REQUIRED")
    require(type(run_id) is int and run_id > 0, "RUN_ID_INVALID")
    repo, sha = record["repository"], record["source_sha"]
    require(repo == "grandchallenge/INTELLECT", "UNSUPPORTED_READBACK_REPOSITORY")
    root = f"repos/{repo}"
    run = provider.api_json(f"{root}/actions/runs/{run_id}")
    require(run["id"] == run_id and run["event"] == "workflow_dispatch"
            and run["head_sha"] == sha and run.get("head_branch") == "main"
            and run["name"] == "Agent continuity policy"
            and run["status"] == "completed" and run["conclusion"] == "success",
            "RUN_NOT_EXACT_VERIFIED_SUCCESS")
    attempt = run.get("run_attempt")
    require(type(attempt) is int and attempt > 0, "RUN_ATTEMPT_INVALID")
    jobs = provider.api_json(f"{root}/actions/runs/{run_id}/jobs?per_page=100")
    require(type(jobs.get("jobs")) is list and jobs.get("total_count") == len(jobs["jobs"]),
            "RUN_JOBS_INCOMPLETE")
    executions = [j for j in jobs["jobs"] if j.get("name") == "Execute exact-source bounded task"]
    require(len(executions) == 1 and executions[0]["status"] == "completed"
            and executions[0]["conclusion"] == "success", "EXECUTION_JOB_NOT_VERIFIED")
    artifact_name = f"gcl-rwp-{run_id}-{attempt}"
    artifacts = provider.api_json(f"{root}/actions/runs/{run_id}/artifacts?per_page=100")
    require(type(artifacts.get("artifacts")) is list and artifacts.get("total_count") == len(artifacts["artifacts"]),
            "RUN_ARTIFACTS_INCOMPLETE")
    matches = [a for a in artifacts["artifacts"] if a.get("name") == artifact_name]
    require(len(matches) == 1, "EXECUTION_ARTIFACT_NOT_UNIQUE")
    artifact = matches[0]
    require(not artifact.get("expired") and artifact.get("workflow_run", {}).get("id") == run_id,
            "EXECUTION_ARTIFACT_EXPIRED_OR_UNBOUND")
    zip_digest = artifact.get("digest", "")
    require(type(zip_digest) is str and zip_digest.startswith("sha256:")
            and HEX.fullmatch(zip_digest[7:]) is not None, "ARTIFACT_ZIP_DIGEST_INVALID")
    receipt_bytes = provider.artifact_json(repo, run_id, artifact_name)
    receipt = json.loads(receipt_bytes)
    require(type(receipt) is dict, "RECEIPT_OBJECT_REQUIRED")
    expected = {"record_type", "work_id", "step_id", "operation_key",
                "operation_key_version", "target_digest", "repository", "source_sha",
                "run_id", "run_attempt", "result", "output_sha256", "evidence_kind",
                "mathematical_certification", "external_mutation", "created_utc"}
    require(set(receipt) == expected, "RECEIPT_SCHEMA_MISMATCH")
    require(receipt["record_type"] == "GCL_BOUNDED_EXECUTION_RECEIPT/1"
            and receipt["work_id"] == record["work_id"] and receipt["step_id"] == record["step_id"]
            and receipt["operation_key"] == key and receipt["operation_key_version"] == KEY_VERSION
            and receipt["target_digest"] == record["target_digest"]
            and receipt["repository"] == repo and receipt["source_sha"] == sha
            and receipt["run_id"] == str(run_id) and receipt["run_attempt"] == str(attempt)
            and receipt["result"] == "PASSED" and receipt["evidence_kind"] == "GITHUB_ACTIONS_TEST_EXECUTION"
            and receipt["external_mutation"] is False
            and receipt["mathematical_certification"] is False,
            "RECEIPT_NOT_BOUND_TO_RUN_AND_OPERATION")
    require(type(receipt["output_sha256"]) is str
            and HEX.fullmatch(receipt["output_sha256"]) is not None, "OUTPUT_DIGEST_INVALID")
    return {"record_type": VERIFICATION, "operation_key": key,
            "source_sha": sha, "run_id": run_id, "run_attempt": attempt,
            "artifact_id": artifact["id"], "artifact_zip_sha256": zip_digest[7:],
            "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
            "result": "VERIFIED_READ_ONLY_EXECUTION",
            "external_mutation_verified": False,
            "next_action": "RECORD_DURABLE_EVIDENCE_AND_ADVANCE"}


def acquire_github_claim(record: dict, provider: GithubCLIReadback) -> dict:
    """GitHub unique ref creation arbitrates a one-shot nonproduction claim.

    A created claim is NOT permission to execute an external effect. On collision,
    timeout or lost acknowledgment the operation stays held for reconciliation.
    """
    key = validate_continuation(record)
    require(record["effect_class"] == "EXTERNAL_MUTATION", "CLAIM_ONLY_FOR_MUTATIONS")
    require(record["state"] == "INTENT_RECORDED", "CLAIM_REQUIRES_RECORDED_INTENT")
    repo, sha = record["repository"], record["source_sha"]
    require(repo == "grandchallenge/INTELLECT", "UNSUPPORTED_CLAIM_REPOSITORY")
    current = provider.api_json(f"repos/{repo}/branches/main")
    require(current["commit"]["sha"] == sha, "PROTECTED_MAIN_MOVED")
    ref = f"refs/heads/gcl-rwp-claims/{key}"
    created = False
    try:
        response = provider.create_claim(repo, ref, sha)
        created = response.get("ref") == ref and response.get("object", {}).get("sha") == sha
    except (ContractError, OSError, ValueError, subprocess.SubprocessError):
        pass
    try:
        seen = provider.api_json(f"repos/{repo}/git/ref/heads/gcl-rwp-claims/{key}")
        matches = seen.get("ref") == ref and seen.get("object", {}).get("sha") == sha
    except (ContractError, OSError, ValueError, KeyError, subprocess.SubprocessError):
        matches = False
    if created and matches:
        state = "CLAIM_CREATED_THIS_ATTEMPT"
    elif matches:
        state = "EXISTING_CLAIM_OUTCOME_UNCERTAIN"
    else:
        state = "CLAIM_NOT_VERIFIED"
    return {"record_type": CLAIM, "operation_key": key, "claim_ref": ref,
            "claim_state": state, "effect_dispatch_authorized": False,
            "next_action": "INDEPENDENT_EFFECT_AUTHORIZATION_AND_READBACK"
                           if state == "CLAIM_CREATED_THIS_ATTEMPT"
                           else "HOLD_AND_RECONCILE_NO_REPLAY"}


FIXTURE_TARGET = hashlib.sha256(
    b'{"effect":"CREATE_DEDICATED_TEST_REF","contract":"GCL_NONPRODUCTION_REF_EFFECT/1"}'
).hexdigest()


def fixture_record(source_sha: str) -> dict:
    """Separate, fixed, nonproduction GitHub ref mutation; not a general worker."""
    from scripts.gcl_resume import RECORD
    return {"record_type": RECORD, "work_id": "RWP-002-FIXTURE",
            "step_id": "test-unique-ref", "repository": "grandchallenge/INTELLECT",
            "source_sha": source_sha, "effect_class": "EXTERNAL_MUTATION",
            "target_digest": FIXTURE_TARGET, "state": "INTENT_RECORDED",
            "attempts": 0, "lease_epoch": 0, "receipt": None}


def execute_nonproduction_fixture(record: dict, provider: GithubCLIReadback) -> dict:
    """A tightly specified test Git ref; deliberately cannot write protected main.

    Creates at most one effect ref per operation key, conditional on winning the
    one-shot claim. A successor can verify it after an acknowledgment loss.
    """
    key = validate_continuation(record)
    require(record == fixture_record(record["source_sha"]), "NOT_FIXED_NONPRODUCTION_FIXTURE")
    effect_ref = f"refs/heads/gcl-rwp-fixtures/{key}"
    claim = acquire_github_claim(record, provider)
    if claim["claim_state"] == "CLAIM_CREATED_THIS_ATTEMPT":
        try:
            provider.create_fixture("grandchallenge/INTELLECT", effect_ref, record["source_sha"])
        except (ContractError, OSError, ValueError, subprocess.SubprocessError):
            pass
    try:
        effect = provider.api_json(f"repos/grandchallenge/INTELLECT/git/ref/heads/gcl-rwp-fixtures/{key}")
        verified = effect.get("ref") == effect_ref and effect.get("object", {}).get("sha") == record["source_sha"]
    except (ContractError, OSError, ValueError, KeyError, subprocess.SubprocessError):
        verified = False
    return {"record_type": "GCL_NONPRODUCTION_EFFECT_READBACK/1",
            "operation_key": key, "claim_state": claim["claim_state"],
            "effect_ref": effect_ref, "result": "VERIFIED_NONPRODUCTION_REF_EFFECT"
            if verified else "OUTCOME_UNKNOWN_HOLD",
            "external_mutation_verified": verified,
            "general_mutation_executor_authorized": False}
