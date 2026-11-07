# GCL-RWP-001 — Resumable Work Protocol

Status: bounded pilot ACCEPTED under INTELLECT #135 (protected commit 1ed8c9bd96ca36e4fbff3066b23fa8f12b47712f, read-only Actions run 42363627013). The independent post-closure review identified broader recovery gaps tracked in INTELLECT #137; see [GCL-RWP-002](GCL-RWP-002.md) for the hardened successor contract. This additive operational profile is subordinate to GCL-AGENT-CONTINUITY-001, the Constitution, the MATH-PROGRAMME cross-project recovery contract, all applicable protected GitHub controls, and hosted-platform policy.

## Purpose and authority

An agent turn or MCP reply is not an execution state store. GitHub Issues, commits, protected refs, PRs, Actions runs/jobs and artifacts are the durable work authority. CONTROL MCP and its private receipts are supporting evidence, not a competing scheduler or task database. A new agent must reconstruct work from these records, without relying on prior private reasoning.

Before consequential work, persist a continuation checkpoint in an existing issue, PR or governed source record with work ID, step ID, repository, exact protected source SHA, effect target digest, effect class, operation key, current state, attempt count, lease epoch, existing receipts, unresolved outcomes, next obligation and protected-admission status.

The current operation key is SHA-256 over canonical JSON with key_version=GCL_OPERATION_KEY/2, work ID, step ID, repository, exact source SHA, effect class and target digest. Historical GCL-RWP-001 smoke receipts used an earlier key formula and are preserved as historical evidence, never retroactively relabelled. Changing source or target changes the logical operation identity, but never resolves the unknown outcome of the old operation. Distinguish operation identity, individual attempts, remote provider run IDs, local execution, remote effect verification, acknowledgment and scientific certification.

## Durable recovery states

INTENT_RECORDED: planned but not yet remotely submitted; source and ownership must be current.

DISPATCHED: submission may have occurred. A dropped response does not prove absence.

OUTCOME_UNKNOWN: reconcile the existing effect before considering another submission.

POLICY_HELD: the exact denied action remains held. Do not automatically replay, disguise or reroute; unrelated authorized siblings remain eligible.

EFFECT_VERIFIED: an effect-specific receipt has been checked against remote authoritative state, with the same operation key.

COMPLETE: a historical checkpoint assertion only until an external authenticated verifier rechecks the exact remote effect. Neither an in-record Boolean nor a receipt pointer establishes true completion. The pure decision engine emits VERIFY_REMOTE for EFFECT_VERIFIED or COMPLETE.

The executable scripts/gcl_resume.py is an advisory recovery decision function plus a protected-source test executor; the separate GCL-RWP-002 adapter performs independently authenticated GitHub readback and tightly scoped nonproduction Git ref claims. The pure decision engine is not an effectful mutation driver. Recovery actions are DISPATCH_ELIGIBLE, RETRY_BOUNDED_READ, RECONCILE_REMOTE, HOLD_EXACT_OPERATION, HOLD_AUTHORITY, FENCE_AND_RECONCILE, REVALIDATE_SOURCE, ADVANCE_VERIFIED, ALREADY_COMPLETE, and DEFER_FOR_REVIEW.

A read-only technical failure may be retried within a bounded budget. An explicit safety rejection is operation-held pending legitimate remediation; no alternate routing or unattended repeat. On an accepted write or unknown post-send result, verify remote state first; REMOTE_NOT_FOUND alone does not prove absence. Expired leases fence stale workers but do not prove external jobs stopped. A moved protected head requires impact assessment, not blind cancellation of unrelated evidence.

## Independent GitHub execution pilot

The opt-in agent-continuity-policy.yml (bounded-execution job) workflow executes one narrow, non-effectful task type: a protected-repository Python unittest file. Its input is a source-controlled job capsule under governance/agent_execution/jobs. The capsule requires a fixed action PYTHON_UNITTEST and effect class READ_ONLY. The runner checks out exact GitHub run SHA, validates job structure and source identity, then uses subprocess argument vectors rather than arbitrary shell commands.

A GitHub Actions run/job and an uploaded JSON receipt contain the source SHA, work and step IDs, operation key, GitHub run ID/attempt, result and output digest. These survive loss of the ChatGPT conversation and MCP tunnel. The existing workflow's bounded-execution job has read-only GitHub permission and serialized concurrency for the same capsule. Dispatch that job on protected main with a nonempty job_path input; default/manual validation without a job_path performs no bounded worker run. It performs no GitHub write or external mutation, and makes no mathematical claim.

The READ_ONLY job label describes the intended GitHub operation, NOT an operating-system sandbox: a committed Python test can access its runner filesystem/network subject to GitHub-hosted runner policy. Source review, least-privilege token, exact-head checkout and a narrow test-file allowlist are the relevant protections. Artifact retention is 30 days; issue closure retains run IDs, fingerprints and evidence metadata, not the expired ZIP's bytes. Sibling eligibility always requires an independent dependency/authority check. The pilot is not a general autonomous research agent or a host-control worker. A separate protected executor and effect-specific readback are required before adopting external mutations. Do not create a second SQLite ledger, new watchdog daemon, duplicated recurring ChatGPT task or false 'exactly once' guarantee.

## Recovery on a new agent/session

1. Bind current protected policy, source, work issue, prior GitHub runs and artifact receipts.
2. Reconcile all uncertain remote effects by original operation key before any repeat.
3. Reassess changed protected source and any stale lease; fence old workers.
4. Select the next independently eligible bounded task, excluding held operations and unmet gates.
5. Persist intent before effect; execute only through the appropriate authorized runner.
6. Read back run/job/artifact and external effect separately. Record verified checkpoint and next obligation. Protected merge and mathematical certification remain separate controls.

## Mandatory adversarial checks

| Fault | Required result |
| --- | --- |
| Response lost after remote write | Reconcile; no duplicate remote mutation |
| Explicit denial | Hold exact action; independent siblings may proceed |
| Transient read failure | Bounded retries; no retry storm |
| Changed source SHA | Revalidate source; retain old uncertain effect |
| Stale or expired lease | Fence then reconcile external state |
| Fake acknowledgment | Cannot satisfy a verified effect receipt |
| Repeated invocation with changed target | Different operation key; no silent conflation |
| Context loss or tunnel failure | Resume from GitHub issue, run/job and artifact without relying on conversation |
| Workflow task injection | Reject arbitrary commands, path traversal and unsupported effects |

## Acceptance and closure

Source admission requires passing INTELLECT CI and protected merge/readback. Runtime pilot acceptance further requires an actual GitHub workflow_dispatch run, exact source/run/job readback and the uploaded receipt artifact. A source-merged workflow is not proof that it ever executed.

Downstream cross-programme adoptions, genuine research-agent continuation and privileged CHAD runner execution are independent obligations until they have their own protected evidence. INTELLECT #135 is closed with satisfied bounded-pilot acceptance. INTELLECT #137 governs the distinct hardened recovery programme; do not close it based on GCL-RWP-001's historical smoke run. No CI success may be represented as mathematical certification, external effect verification or deployed host control.
