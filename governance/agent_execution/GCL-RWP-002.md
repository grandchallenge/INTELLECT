# GCL-RWP-002 — Verifiable continuity and bounded concurrency

Status source: INTELLECT #137 is authoritative for protected admission, execution acceptance and final disposition. This source document does not assert its own terminal state. Parent bounded pilot #135 remains historically accepted; its original receipt and digest are not rewritten.

## Purpose

A conversation can disappear, a platform can deny one invocation, and a successful remote action can lose its response. The governing outcome must come from GitHub's durable source, work, run and effect records, not from agent memory or a self-asserted success flag.

This implementation remains a bounded pilot. It does not authorize arbitrary external mutations, protected-branch writes, general mathematical research agents, or safety-filter bypass.

## Exact operation identity

Canonical GCL_OPERATION_KEY/2 is the SHA-256 of sorted, compact JSON fields: key_version, work_id, step_id, repository, source_sha, effect_class, target_digest.

For a unit-test job, target_digest is the SHA-256 of canonical JSON with target_type=GCL_UNITTEST_TARGET/1, action=PYTHON_UNITTEST, and the allowlisted test_file. Intent, executor and verifier compute the SAME operation key. The original GCL-RWP-001 smoke used an earlier formula; retain historical evidence without inventing an identity conversion.

The only allowed test modules are test_gcl_resume.py and test_gcl_resume_integration.py. This is source-policy allowlisting, NOT an OS sandbox. Runner GitHub token permissions remain read-only and checkout is exact-source pinned.

## No Boolean as evidence

A stored COMPLETE or EFFECT_VERIFIED state is an untrusted assertion. The pure classifier returns VERIFY_REMOTE and effect_authorized=false rather than granting completion. A stored evidence pointer is insufficient.

A separate, authenticated successor process uses GithubCLIReadback with an existing approved GitHub CLI identity to query the original run, jobs and artifacts, download the original receipt, check source SHA, logical key, run identity/attempt, target fingerprint, job conclusions and receipt schema. It writes a GCL_RUN_VERIFICATION/1 witness. Invoke it from the exact protected checkout with python -m scripts.gcl_resume verify-run; it does not require a new workflow or change the protected GHOS registry. Missing, expired, incomplete or mismatched evidence fails closed. Test mocks cannot be represented as live authenticated proof.

GitHub Actions artifacts expire (current workflow retention: 30 days). Durable issues must retain exact source, run/job/artifact IDs, artifact ZIP digest, receipt digest, output digest, review and admission references, and limitations BEFORE expiry. A digest does not substitute for the original expired bytes.

## Atomic one-shot claim and fixed nonproduction effect

For external mutations, the classifier returns CLAIM_REQUIRED; it never directly authorizes effect dispatch. The claim gate first checks current protected main and attempts ONE GitHub unique-ref creation at refs/heads/gcl-rwp-claims/<operation-key>. Competing creations cannot both win the same ref. A lost response is resolved by readback and held without a second creation attempt.

A fixed test-only operation (RWP-002-FIXTURE/test-unique-ref) creates refs/heads/gcl-rwp-fixtures/<operation-key> only for the initial claim winner. A successor reads back that effect ref without repeating it. No generic external command, protected main write, issue mutation, credential expansion or deployment is enabled. The ref points to an exact protected SHA.

The claim is a one-shot atomic uniqueness gate, NOT a distributed lease with expiry/takeover, and not general production authority. A future production executor requires effect-specific authorized fencing and readback.

## Recovery discipline

Technical read failures permit bounded retries. An uncertain external mutation requires exact-key readback before replay. An explicit platform denial holds only that operation; do not repackage or reroute the denied invocation. Stale ownership/source requires fencing or revalidation. Even apparently terminal checkpoints are reverified against the authenticated source. Independent sibling work requires its own dependency and authority analysis: no default eligibility.

## Adversarial acceptance matrix

| Scenario | Required outcome |
| --- | --- |
| Intent vs runner keys | Identical GCL_OPERATION_KEY/2 |
| Forged receipt, changed source, wrong target or wrong attempt | Reject |
| Expired artifact, missing receipt or incomplete job set | Reject |
| Two workers contest one claim | Exactly one initial winner |
| Claim reply lost | Hold; no test-effect dispatch |
| Test-effect reply lost | Remote readback, no duplicate effect |
| Main moves or lease is stale | Fence; no automatic dispatch |
| Successor without chat history | Recover solely from durable record and provider readback |
| Live source-pinned GitHub execution | Verify run, jobs, receipt and artifact |
| Separate authenticated successor process | Verify current provider run, job and artifact state |
| Nonproduction ref effect | One claim, one effect, replay-safe readback |

These are pilot tests, not mathematical certification or proof of unrestricted GCL agent continuity.

## Protected completion obligations

1. Source CI, two Python versions, governance and workflow checks pass.
2. Obtain INTELLECT's independent GitHub approval and protected merge/readback.
3. Run the integration capsule on exact admitted main; read back genuine GitHub execution evidence.
4. Run the authenticated verifier as a separate process from the original execution using the exact admitted source SHA; retain the actual verification witness and CLI readback receipt on INTELLECT #137.
5. Run fixed nonproduction Git ref fixture on authenticated operator shell; read back the ref and repeat the read-only verification with same identity.
6. Record exact durable evidence and non-author review before closing #137.

General production-effect fencing, cross-programme expansion and autonomous research-agent execution are NOT conferred by this package.

## Routing custody

The pre-existing agent-continuity-policy.yml workflow and frozen GHOS routing registry remain byte-for-byte unchanged. A proposed workflow extension triggered a new SECRET_CREDENTIAL classification and was withdrawn, rather than rewriting frozen RSI evidence or misdeclaring credentials. Authenticated follow-up verification uses the separately approved CHAD operator surface and does not bypass GitHub branch rulesets.
