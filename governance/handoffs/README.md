# Canonical GCL handoff contract

This directory is the durable GCL-wide contract for continuity and takeover of governed work. It is an INTELLECT governance projection subordinate to the Constitution; it does not amend the Constitution, create office powers, create a second lifecycle, or enlarge any repository's domain authority.

## Authority chain

Before mutation, resolve authority in this order:

1. `grandchallenge/INTELLECT:CONSTITUTION.md`;
2. effective amendments and `grandchallenge/INTELLECT:governance/constitutional_authority_schedule.json`;
3. admitted cross-programme standards where materially applicable;
4. the target repository's delegated domain authority, `AGENTS.md`, and exact adopted controls;
5. this handoff contract and the repository-local work-set handoff;
6. GitHub operational/evidentiary state.

A lower layer may not enlarge its own authority. `MATHCERT` alone renders bounded mathematical certification dispositions through accepted routes. AETHER retains the production semantic authority assigned by INTELLECT Article IX. GitHub issues, pull requests, checks, releases, and repository settings are operational or evidentiary surfaces; they do not create constitutional, certification, semantic, or domain authority by themselves.

## Repository placement rule

The generic handoff machinery lives here in `grandchallenge/INTELLECT`:

- `governance/handoffs/README.md` — this contract;
- `governance/handoffs/CANONICAL_TAKEOVER_PROMPT.md` — copy/paste takeover entry point;
- `governance/handoffs/_TEMPLATE/README.md` — starter for a new repository-local handoff.

The actual work-set handoff lives with the work it describes:

`<TARGET WORK REPOSITORY>:handoffs/<WORKSET-ID>/README.md`

The target repository is the repository that owns the primary deliverable or the governing work-package/coordination contract. For a cross-repository umbrella work set, the coordinating repository named by the governed work package may own the umbrella handoff while component implementation state remains local to each component repository.

Do not centralize ordinary work-set state in INTELLECT merely because INTELLECT owns the constitutional handoff contract. Do not place a GCL-wide handoff contract in a domain repository merely because that repository happens to host one work set.

## INTELLECT lifecycle reconciliation

A handoff is a continuity projection, not a phase transition.

If the work set is INTELLECT-governed, identify its current lawful phase:

`Charter -> Generation -> Specification -> Realization -> Confrontation -> Judgment -> Integration -> Disposal -> Complete`

The handoff may support any phase, but it cannot advance a phase, declare completion, replace an office finding, or silently redefine inherited purpose, scope, claims, evaluation contract, acceptance criteria, or reversal conditions.

Review separation remains governed by the live constitutional schedule. A system may staff multiple non-reserved roles through distinct exact-subject logical passes where permitted. If an authoring system acts as Adversary or Referee, that pass must be declared non-authoring and read-only; mutation invalidates that pass.

## Mandatory first executable preflight

Before mutation, the execution lead must state:

```text
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
```

If `PROCESS NECESSITY TEST` is `fail`, do not create the proposed process artifact or step.

If `AUTHORITY REQUIRED` is `reserved`, cite the exact governing instrument and material transition. Importance, polish, or generic template language is not evidence of reserved authority.

## Substance-first execution

The primary deliverable remains the object of optimization. Supporting governance, CI, provenance, release, synchronization, evidence, and repository mechanics are subordinate controls.

Every material activity must do at least one of the following:

1. improve the primary deliverable against an acceptance criterion;
2. directly verify an acceptance criterion;
3. perform the smallest control action required to preserve correctness, provenance, authority, security, or reversibility;
4. remove a demonstrated blocker to one of the above.

Otherwise defer or abandon it.

A green build, merge, manifest, release packet, ledger entry, or evidence bundle is not substantive completion unless the work set itself makes that object the primary deliverable.

Every continuation must distinguish:

- substantive progress on the primary artifact;
- substantive verification or review;
- required governance state;
- incidental process state.

Two consecutive continuations without material primary-artifact advancement require re-planning before the same execution path continues.

A failed supporting mechanism does not automatically authorize a larger mechanism. First determine whether the failure blocks a material acceptance criterion or exact authority boundary. If it does not, route around, defer, or remove it. If it does, repair the narrowest blocking defect.

### Drift tripwires

- `PROCESS_DOMINANCE` — process becomes the dominant work while the primary artifact is materially unchanged;
- `REPEATED_CONTINUATION` — two consecutive continuations without material advancement;
- `EVIDENCE_SUBSTITUTION` — machine/process evidence is treated as proof of quality it does not test;
- `REMEDIATION_RECURSION` — supporting repair creates another supporting repair dependency;
- `OBJECTIVE_DRIFT` — current activity cannot be traced to a material criterion or exact boundary;
- `ARTIFACT_INFLATION` — supporting artifacts accumulate faster than substantive outputs.

When a tripwire fires, re-plan toward the shortest path back to substantive progress or terminal material closure.

## Standard repository-local handoff structure

Each new substantial `<TARGET WORK REPOSITORY>:handoffs/<WORKSET-ID>/README.md` should remain thin and domain-specific. Use this order unless a material domain requirement requires a narrow departure:

1. `# <WORKSET-ID> — Handoff`
2. `## Target repository and authority`
3. `## Purpose`
4. `## Primary deliverable`
5. `## Material acceptance criteria`
6. `## Current substantive state`
7. `## Authoritative pointers`
8. `## Smallest safe next tranche`
9. `## Material dependencies and boundaries`
10. `## Reserved authority / stop conditions`
11. `## Notes intentionally omitted`

Structural rules:

- keep the file thin and repository/work-set specific;
- do not duplicate the Constitution, this contract, or generic operating doctrine;
- do not reproduce historical ceremony unless it remains a live material dependency;
- do not embed large status logs, replay transcripts, release packets, or procedural archives;
- link to authoritative domain artifacts instead of restating them redundantly;
- preserve history as evidence, but inherit only live controls and material dependencies.

Use `grandchallenge/INTELLECT:governance/handoffs/_TEMPLATE/README.md` as the starter form.

## Terminal-state bias

Prefer completing one meaningful substantive unit to a defensible terminal state over opening many partial surfaces. Once the primary artifact and required acceptance criteria are satisfied, close the minimum required governance path promptly. Do not continue producing process evidence after the governing boundary is already satisfied.

The default question is:

> What is the least process necessary to protect the substantive result?
