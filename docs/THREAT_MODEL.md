# Threat Model

## Protected properties

The Grand Intellect protects work-package history, separation of powers, evidence and decision provenance, AETHER-enforced confidentiality, recovery paths, human authority over irreversible acts, and consistency between declared and executable governance.

## Threat actors

Threats may originate from malicious principals, compromised or overconfident agents, mistaken human stewards, buggy adapters, prompt injection in artifacts, stale execution attempts, and governance drift.

## Primary threats and controls

### Self-certification

One agent proposes, measures, judges, and approves its own work.

Controls: office separation, unique agent identity across offices, exact required reviews, and no automatic advancement from Council dispatch.

### Review laundering

An invocation is recorded as approval without discharging obligations.

Controls: exact obligation identifiers, latest-review semantics, findings, evidence references, and fail-closed gates.

### Criterion drift

Acceptance criteria change after results are visible.

Controls: event-sourced specifications, reversal conditions, versioned changes, and future AETHER cut comparison.

### Evidence fabrication

A contact record references nonexistent or manipulated evidence.

Controls: reproducible commands, Verifier and Adversary review, provenance, and future digest-bearing AETHER sidecars.

### Semantic split brain

INTELLECT and AETHER disagree about history or readiness.

Controls: AETHER as production authority, capability preflight, bounded history retrieval, explicit schema versions, and planned gate-conformance tests.

### Unauthorized visibility escalation

A client requests broader access than its token permits.

Controls: AETHER effective-policy ceilings; INTELLECT never treats client policy assertions as authority.

### Destructive disposal

An agent deletes records needed for recovery or accountability.

Controls: explicit deletion authorization, non-destructive dispositions by default, Human Steward authority, and recovery paths.

### Prompt injection through artifacts

An artifact attempts to alter powers or evade review.

Controls: artifacts are evidence rather than authority; mandates and permissions are supplied out of band and bounded by office and phase.

### Stale execution

An Executor acts under an expired claim or superseded specification.

Controls: planned AETHER lease epochs, expected-cut semantics, explicit realization IDs, and transition history.

## Current limitations

The foundation does not yet provide cryptographic artifact verification, live lease fencing, sandboxed model execution, secret management, distributed consensus, model-output security filtering, or policy-complete live AETHER tests. It must not be deployed as a safety-critical autonomous system in its current form.
