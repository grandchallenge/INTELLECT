# GI-STEWARD-0003: Streamlined multi-role agent staffing

**Status authority:** `governance/constitutional_authority_schedule.json`
**Issued:** 2026-09-04
**Issuer:** Human Steward (`fyremael`)
**Ordinary Human Steward:** `fyremael`
**Recovery owner:** `jimsteeg`
**Supersedes:** `GI-STEWARD-0002`, only when selected by the protected authority schedule
**Scope:** Grand Intellect and Grand Challenge Labs governance staffing
**Policy version:** `1.0.0`
**Duration:** Until superseded by a later exact Human Steward directive

## Direction

One Codex system may staff any combination of non-reserved Minder, Council,
specialist, review, and Executor roles. Functional separation is established by
role-scoped logical audit passes, not by multiplying people, agents, model
instances, conversations, processes, accounts, or GitHub approvals.

Each governed pass records its role, `reviewer_system_id`, `logical_pass_id`,
mode, exact subject, criteria, evidence, finding, and unresolved obligations.
The `logical_pass_id` distinguishes audit phases; it does not claim a separate
runtime invocation. Roles answering different questions use different logical
pass identifiers even when `reviewer_system_id` is identical.

An Adversary or Referee pass performed by a system that authored the candidate
must use `non_authoring_read_only` mode. The pass may identify defects but may
not repair the candidate. A material candidate or evidence change ends the pass
and invalidates every affected finding. Unrelated protected-head movement does
not invalidate a finding.

## Proportional work classes

- `routine_bounded`: reversible work within existing contracts and authority,
  with no promoted claim or reserved decision. The system may classify,
  implement, test, audit, merge through protected checks, and verify readback
  without a fresh human action or blanket approval count.
- `substantive`: a public-contract, evidence-gate, authority-boundary, or
  material-result change. The system performs applicable functional passes and
  records an ADR when required. Human action is required only if the decision
  is also reserved.
- `reserved`: a decision expressly assigned to the Human Steward or another
  human authority. Automation prepares one consolidated exact-subject decision
  and may faithfully transcribe and mechanically execute it after authorization.

Unknown or mixed work is classified at the highest applicable class. A role may
be not applicable only with an explicit reason. No class converts green CI,
mergeability, or automated consensus into authorization or certification.

## Reserved authority and narrow independence

The Human Steward retains the powers in Article X. Automation must not invent,
impersonate, or infer human judgment. The existing recovery safeguards and
recognized human roster remain unchanged.

Specialist independence remains mandatory where an admitted domain contract
expressly requires it. In particular, no system may render a MATHCERT
certification for a claim for which it supplied the sole construction or sole
verification evidence. Corpus admission, destructive disposal,
production-semantic activation, autonomous permission escalation,
credential expansion, safety-critical deployment, public commitments, and
irreversible resource commitments retain their declared authority gates.

These outcome restrictions do not reinstate blanket identity multiplication or
routine approval chains.

## Activation and migration

This directive is effective only when selected by the protected constitutional
authority schedule. The transition candidate must be reviewed under the
previously effective `GI-STEWARD-0002`: one non-author Adversary agent and a
different non-author Referee agent from a distinct session, followed by one
authenticated exact-packet authorization by `fyremael`.

That single authorization may cover the deterministic schedule cutover,
admission of `GCL-AGENT-STAFFING-001` version `1.0.0`, organization defaults,
and commit-addressed downstream adoption when the exact transition packet lists
those operations. No later ceremonial human click is required.

Completed decisions retain their recorded rules. In-flight decisions either
finish under an already authorized exact packet or restart under this directive.
Historical findings are not relabelled. Rollback requires a later exact Human
Steward directive and protected schedule selection.

## Authority boundary

This directive changes staffing and execution procedure, not office powers. It
does not amend the Constitution; grant mathematical, scientific, production,
safety, deployment, commercial, credential, destructive, novelty, or priority
authority; weaken protected branches or immutable releases; or make GitHub a
constitutional or production-semantic authority.
