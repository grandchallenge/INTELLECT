# GI-COUNCIL-POSTMERGE-001: post-merge governance remediation

**Status:** Before the Council for review

**Decision class:** operating-policy and automation design

**Proponent:** Human Steward direction recorded in the Council docket

**Authority boundary:** Council recommendation; Human Steward disposition remains reserved

## Question presented

Should GCL replace its serial, human-serviced post-merge governance chain with
an event-driven Clerk that executes only the deterministic administrative
projections enumerated in one exact Human Steward authorization packet?

## Problem statement

The current governed-change path separates the subject merge, agent findings,
Human Steward authorization, receipt admission, activation, standards
admission, programme adoption, documentary reconciliation, and final-head
remedies into multiple serial pull requests. The separation preserves authority
but makes one already-rendered human decision depend on repeated repository
operation. Exact-head churn can also invalidate completed review when generated
administrative evidence changes a head without changing the governed payload.

## Proposed disposition

Adopt a three-stage remediation:

1. **Operational simplification now.** Replace hourly polling with event-driven
   dispatch plus a daily recovery sweep; add terminal campaign states; prepare
   downstream pull requests automatically; expose one current operator action;
   and reconcile documentation with the effective two-agent, one-Human-Steward
   model.
2. **Pre-authorized administrative projections.** After a narrow authority
   amendment, permit the Clerk to merge a generated projection only when an
   exact Human Steward packet enumerates the transition, target repository, and
   allowed paths; the governed payload is unchanged; exact-head checks pass;
   no hold or changes-requested review exists; and an execution receipt is
   emitted. The Clerk may not approve, ratify, certify mathematics, expand
   scope, decide a disputed finding, or change substantive policy.
3. **Governed-payload identity.** Bind review to a canonical digest of
   substantive allowlisted files and the campaign contract. Record checks and
   generated projections separately so administrative evidence does not
   invalidate an otherwise unchanged substantive review.

## Alternatives before the Council

- **A — Approve as proposed.** Implement all three stages with a shadow-mode
  pilot before projection merging is enabled.
- **B — Approve with changes.** Retain the event-driven and governed-payload
  changes but require a human merge for every projection.
- **C — Defer.** Run measurement and shadow mode without changing authority.
- **D — Reject.** Preserve the current exact-head and manually merged chain.

## Mandatory controls

- One authenticated Human Steward authorization per governed decision.
- A packet-declared transition graph with no undeclared target or path.
- Fail-closed exact identity, required-check, hold, and replay validation.
- Separate agent identities for offices whose independence is required.
- Append-only decision, execution, and readback evidence.
- No inference of constitutional activation, production truth, or mathematical
  certification from CI, a merge, a release, or a Council recommendation.
- Automatic rollback means disabling future execution and proposing a
  compensating change; it does not erase admitted history.

## Requested Council record

Each of the ten Council offices must independently record:

- its office-specific analysis;
- discharged obligations;
- material findings and residual uncertainty;
- evidence references;
- a decision of `approve`, `approve_with_conditions`, `changes_requested`,
  `reject`, or `abstain`; and
- proposed conditions or amendments.

The Referee must issue a final Council disposition only after all ten records
exist. The disposition is advisory unless and until the Human Steward performs
the separately authenticated reserved action required by effective authority.
