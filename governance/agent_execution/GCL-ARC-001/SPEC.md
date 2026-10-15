# GCL-ARC-001 implementation specification

## Intended effect

Implement the existing GI-STEWARD-0003 one-system/multiple-role policy in
operational GCL trust receipts, and remove implied per-agent GitHub accounts
and routine Human Steward technical review. This initial INTELLECT PR is
candidate-only and does NOT change operational security authorization.

## Structural commitments

- Single real GitHub account for institutional transport, with actual login
  recorded in all passes. Existing bounded service Apps remain mechanical
  protected-write and admission identities.
- Agent role separation by exact-head read-only logical passes. Candidate
  writes, Verifier checks, Adversary attacks, Referee adjudicates; same
  system may staff several roles. Mutation invalidates read-only evidence.
- Distinguish logical pass independence from scientific methodological
  independence. A required scientific or mathematical independent method
  must be separately executed, traceable and verifiable.
- Trusted gates use byte-locked source, semantic checks, protected CI,
  reproducers, hostile tests, receipt digests and postwrite readback.
- Reserved actions remain reserved; no Human Steward routine review.
- Domain review dossier and later GitHub source review receipt are separate
  transactions. Never store unknown source PR commit SHA inside its own
  reviewed source blob.

## Minimum payload

GCL_AGENT_REVIEW_DOSSIER_V1 contains a subject repository, immutable head,
material digest, real transport login and ordered VERIFIER/ADVERSARY/REFEREE
passes with unique logical IDs, system IDs, modes, read/write sets, checks,
negative controls, dispositions and unresolved findings. Independent
method evidence is required for MATHEMATICAL_CLAIM.

GCL_PROTECTED_ROLE_REVIEW_RECEIPT_V1 is a later, separately protected
attestation referencing the already completed source PR head, real GitHub
review ID and dossier blob. It does not itself purport to prove mathematical
or scientific claims. Relying service must resolve authenticated GitHub
event provenance before using it.

## Pilot and downstream contracts

Initial target: MATH-PROGRAMME PR #2624 at commit
e577477b656c6865698d5dbc18962e2810f53a26, changed-material SHA256
e8254dbd487e59529d64e67b7832066cb4ff3a5437421e7b073b3effdd4822f0.
Blocked prior to migration by source-review provenance cycle and unwarranted
assumption that specialist roles need different GitHub people.

Pilot success: after separate protected migration, authorized controller
moves exactly 14 issue-bound critical reviews to Project Status RETURNED,
sets 14 Issue Fields GCL State RETURNED, removes all available labels and
preserves 5 source-correction REVISE labels on issues #2520, #2521, #2522,
#2523, #2536. All issues remain open. No scientific certification.

## Smallest executable tasks

A. Admit the candidate standard and 17 negative/positive verifier tests.
B. Build two-phase domain review producer and protected receipt writer;
   independently validate actual GitHub source review provenance.
C. Migrate MATH-PROGRAMME specialist receipt adapter with explicit
   protection-level admission. Fix the circular-Git-SHA requirement first.
D. Rerun exact-head PR #2624 through the genuine agent specialist lane,
   then merge via existing protected workflow.
E. Run Council Clerk and audit all 14 readbacks; record the correction ledger.

Do not silently skip A-C, manufacture a reviewer, change branch protection
outside a governed migration, or make the Founder an operational approver.
