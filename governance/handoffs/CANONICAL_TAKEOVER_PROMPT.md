# Canonical GCL Handoff Takeover Prompt

Use this exact prompt to start a substantial GCL takeover. Normally replace only the three target-work placeholders in the opening lines.

```text
CONSTITUTIONAL AUTHORITY REPOSITORY: grandchallenge/INTELLECT
TARGET WORK REPOSITORY: <OWNER/REPOSITORY>
WORKSET: <WORKSET-ID>
TRACKING POINTER: <ISSUE/PR/WORKSET POINTER IF APPLICABLE>

Take over `<WORKSET-ID>` in `<OWNER/REPOSITORY>`, tracked by `<ISSUE/PR/WORKSET POINTER IF APPLICABLE>`.

Treat this prompt only as a pointer. Do not rely on conversational history or stale handoff state.

Before mutation:

1. Re-fetch protected live state of `grandchallenge/INTELLECT` and the `TARGET WORK REPOSITORY`.
2. From protected INTELLECT, read `CONSTITUTION.md`, `governance/constitutional_authority_schedule.json`, and only the effective amendments/directives selected by that schedule that materially govern the work.
3. Read the canonical handoff contract at `grandchallenge/INTELLECT:governance/handoffs/README.md`.
4. From the target repository, read its live `AGENTS.md` and exact repository/domain governing instruments when present.
5. Read the repository-local work-set handoff at `<TARGET WORK REPOSITORY>:handoffs/<WORKSET-ID>/README.md` and follow its authoritative pointers.
6. Resolve the target repository's delegated domain authority and any exact admitted operating-standard adoption that materially applies.

Authority rules:

- `grandchallenge/INTELLECT:CONSTITUTION.md`, effective amendments, and the live INTELLECT authority schedule control constitutional powers, obligations, work-package transitions, office obligations, and reserved authority.
- The target repository owns only the domain authority delegated to it by the governing authority chain.
- `grandchallenge/MATHCERT` alone renders bounded mathematical certification dispositions through accepted routes.
- `grandchallenge/AETHER` owns the production semantic authority assigned by INTELLECT Article IX.
- `grandchallenge/gcl-standards` is the subordinate registry and publication repository for admitted cross-programme operating standards.
- GitHub issues, pull requests, checks, releases, and repository settings are operational or evidentiary surfaces. They do not create constitutional, certification, semantic, or domain authority by themselves.
- The canonical handoff contract is a continuity/execution projection. It does not create another lifecycle or enlarge target-repository jurisdiction.

Repository placement:

- generic handoff contract and starter template: `grandchallenge/INTELLECT:governance/handoffs/`;
- actual work-set continuity state: `<TARGET WORK REPOSITORY>:handoffs/<WORKSET-ID>/README.md`;
- for a cross-repository umbrella work set, use the repository that owns the governing work-package/coordination contract as `TARGET WORK REPOSITORY`, and keep component implementation state local to each component repository.

INTELLECT lifecycle reconciliation:

- Determine whether this work set is INTELLECT-governed. If so, state its current lawful phase: `Charter`, `Generation`, `Specification`, `Realization`, `Confrontation`, `Judgment`, `Integration`, `Disposal`, or `Complete`.
- A handoff and its preflight are continuity projections; they do not perform a phase transition.
- Do not redefine inherited purpose, scope, claims, evaluation contract, acceptance criteria, or reversal conditions merely to fit the current implementation.
- Any phase transition must satisfy the substantive conditions and office obligations required by the live INTELLECT Constitution and authority schedule.
- Follow the live staffing schedule. A single system may staff multiple non-reserved roles through distinct exact-subject logical passes when permitted. If an authoring system acts as Adversary or Referee, that pass must be declared `non_authoring_read_only`; mutation invalidates the pass.
- Do not manufacture Human Steward authority. Reserved authority exists only where the governing chain expressly reserves the material transition.

First produce the mandatory canonical preflight:

CONSTITUTIONAL AUTHORITY HEAD
TARGET WORK REPOSITORY
TARGET PROTECTED HEAD
INTELLECT WORK-PACKAGE PHASE: <phase / not applicable>
CONTROLLING DOCTRINE REVISIONS
TARGET DOMAIN AUTHORITY
PRIMARY DELIVERABLE
MATERIAL ACCEPTANCE CRITERIA
CURRENT SUBSTANTIVE STATE
SMALLEST SAFE EXECUTABLE TRANCHE
MATERIAL CLOSURE
MINIMUM REQUIRED CONTROL PATH
AFFECTED CHECKS
PROCESS ARTIFACTS PROPOSED
PROCESS NECESSITY TEST: pass / fail
DRIFT TRIPWIRES ACTIVE: none / list
AUTHORITY REQUIRED: delegated / reserved

Then immediately effectuate the `SMALLEST SAFE EXECUTABLE TRANCHE` unless an exact governing instrument reserves that transition.

Execution rules:

- Keep the `PRIMARY DELIVERABLE` as the object of optimization.
- Treat governance, CI, provenance, release engineering, synchronization, evidence, and repository mechanics as subordinate controls.
- Do not create a process artifact or additional control step unless its `PROCESS NECESSITY TEST` passes.
- Do not use machine evidence as a proxy for substantive mathematical, scientific, technical, editorial, or product quality beyond what the evidence actually tests.
- Distinguish substantive progress, substantive verification/review, required governance state, and incidental process state in every continuation.
- If two consecutive continuations occur without material advancement of the primary artifact, re-plan before continuing.
- If supporting machinery fails, determine whether it actually blocks a material acceptance criterion or reserved authority boundary before repairing or expanding it.
- Do not reproduce historical ceremony that is no longer a live material dependency.
- Prefer terminal completion of a meaningful substantive unit over accumulation of branches, manifests, evidence packets, gates, or intermediate state.
- Proceed autonomously through routine bounded, non-reserved work under the live delegated authority schedule.
- Do not request Human Steward, Referee, Council, or other approval merely as ceremony. Where an exact governing instrument requires an office finding or reserves a transition, satisfy that exact requirement and record the exact subject.
- Stop only for a genuine material blocker, material scope/control-plan change, exact reserved authority boundary, substantive contradiction/failure requiring escalation, or completed material closure.

If the repository-local handoff duplicates obsolete ceremony or conflicts with the live authority chain, preserve historical evidence but follow the higher live authority and identify the shortest safe path back to substantive execution.

For a new work set, create the repository-local handoff from:

`grandchallenge/INTELLECT:governance/handoffs/_TEMPLATE/README.md`

Do not invent a new lifecycle, generic handoff structure, or operating doctrine.
```

## Usage

Normally replace only:

- `<OWNER/REPOSITORY>` — the repository that owns the primary deliverable or governing work-package/coordination contract;
- `<WORKSET-ID>`;
- `<ISSUE/PR/WORKSET POINTER IF APPLICABLE>`.

Everything after the opening pointer should remain stable. Domain-specific execution state belongs in the target repository's `handoffs/<WORKSET-ID>/README.md`, not in a rewritten takeover prompt.
