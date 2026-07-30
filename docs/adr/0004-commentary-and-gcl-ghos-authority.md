# ADR-0004: Reconcile commentary and GCL-GHOS with constitutional authority

**Date:** 2026-07-29
**Status:** Proposed constitutional amendment
**Amendment:** `GI-AMEND-0001`
**Decision owner:** Human Steward
**Required reviews:** non-author agent Adversary and distinct agent Referee
under `GI-STEWARD-0001`

## Problem

The compact Constitution is precise enough to govern power. The expanded
architectural text contains valuable explanations, failure modes, and
operating guidance, but it occasionally speaks as if it were an alternative
constitution: it introduces Renewal as a phase, implies that the Council may
certify without a domain qualifier, and presents one artifact layout as a
universal minimum.

Separately, the candidate GitHub Constitutional Operating System described
`gcl-standards` as owning cross-programme standards and treated repository
artifacts as canonical without an explicit boundary against AETHER production
semantics. Those formulations can invert Article IX and create a second source
of constitutional authority.

## Decision

Retain `CONSTITUTION.md` unchanged as constitutional law. Refactor the expanded
text into `The Grand Intellect: Constitutional Commentary and Operating
Doctrine`, expressly subordinate to the Constitution.

Propose `GI-AMEND-0001` to:

- designate that commentary;
- establish the Human → Constitution → INTELLECT → standards → programme →
  repository projection hierarchy;
- preserve AETHER's production semantic authority;
- reserve bounded mathematical certification to MATHCERT;
- designate `gcl-standards` as a registry and publication repository rather
  than the source of constitutional power; and
- authorize commit-addressed GCL-GHOS adoption only after the amendment and
  standard complete separated agent review and Human Steward authorization.

## Alternatives considered

### Replace the compact Constitution with the expanded text

Rejected. The expanded text is rich but too interpretive to serve as a stable,
enforceable allocation of power. It also contains unresolved differences from
the executable lifecycle.

### Keep both texts as coequal constitutions

Rejected. Coequal texts create ambiguity precisely where separation of powers
requires deterministic precedence.

### Treat GCL-GHOS as the umbrella constitution

Rejected. A platform operating standard should describe how GitHub realizes
governance, not acquire the power to define constitutional offices or semantic
truth.

### Leave authority implicit

Rejected. Repository profiles and automation had already encoded the wrong
direction of authority. Prose alone would allow the inversion to recur.

## Adversary threat analysis

| Threat | Failure | Control |
| --- | --- | --- |
| Commentary capture | Interpretive prose silently adds powers or waives gates | Nonbinding designation, explicit precedence, negative test |
| Registry capture | Custody of standards becomes constitutional ownership | Subordinate registry role enforced in both repositories |
| Platform capture | Green checks, merged PRs, or releases manufacture authority | GitHub exclusions and exact authoritative references |
| Semantic split brain | Repository state competes with AETHER event order or replay | Article IX restated and validator requires all AETHER powers |
| Mathematical overclaim | Council closure or CI is represented as certification | MATHCERT reservation and forbidden-inference clauses |
| Self-ratification | Author, agent, bot, or merge event is treated as approval | Distinct non-author agent Adversary and Referee records plus Human Steward authorization at exact commits |
| Correlated agent review | One invocation is relabelled as multiple offices | Distinct recorded agent sessions, role briefs, findings, and exact-packet binding |
| Profile drift | Future schemas again classify INTELLECT as a provider | Constitutional profile plus cross-repository validation |
| Formality evasion | “Exploratory mode” is used to waive constitutional substance | Modes scale manifestation and review depth, not Article V gates |
| Documentary fork | Expanded compact or lifecycle becomes shadow law | Authoritative Compact and phase reconciliation clauses |

Residual risk includes correlated agent judgment and Human Steward
concentration. `GI-STEWARD-0001` accepts that temporary bootstrap risk while
requiring distinct agent identities, explicit findings, exact revisions, and
single-human accountability.

## Compatibility and migration

1. Preserve `CONSTITUTION.md` byte-for-byte; no current gate or work-package
   event changes.
2. Add the commentary, amendment instrument, machine-readable authority
   schedule, schema, validator, and adversarial tests in INTELLECT.
3. Change the candidate standards schema from `canonical_policy_source` to
   distinct `constitutional_source` and `operating_policy_source` fields.
4. Reclassify INTELLECT from `provider` to `constitutional` in the candidate
   repository profile. Existing live custom-property settings remain migration
   work and must not be changed before ratification.
5. Amend GCL-GHOS and its ADR to state the subordinate registry and AETHER
   boundaries.
6. After separated agent review and Human Steward authorization, pin exact
   commits in both authority records and the mathematics adoption record.
7. The Human Steward may then promulgate version 1.1.0. A later implementation
   PR may migrate live GitHub properties and settings against the accepted
   commits.

Existing work packages remain valid. “Renewal” maps to the existing governed
reopen-to-Generation command; no event migration is required.

## Executable gates and tests

The amendment adds:

- `governance/constitutional_authority_schedule.json`;
- `schemas/constitutional_authority_schedule.schema.json`;
- `grand_intellect.constitutional_authority.validate_authority_schedule`; and
- negative tests for commentary, registry, GitHub, and activation-boundary
  violations.

The shared Council Clerk additionally resolves all coordinated PR heads and
checks into one digest-addressed packet, validates distinct structured agent
Adversary and Referee findings, publishes the Human Steward attestation, and
emits a machine-readable receipt. The Human Steward inspects and signs;
automation performs transcription. Any new subject commit invalidates the old
packet.

The coordinated `gcl-standards` change validates both constitutional and
operating-policy sources and rejects active programme adoption without an
effective amendment and exact commit identities.

## Approval and effective version

Human Steward approval is **pending**. Non-author agent Adversary and distinct
agent Referee review are **pending** under `GI-STEWARD-0001`. Authoring this
proposal, passing CI, or merging it does not constitute approval.

If all activation conditions are satisfied and recorded, the effective
constitutional version will be **1.1.0**.
