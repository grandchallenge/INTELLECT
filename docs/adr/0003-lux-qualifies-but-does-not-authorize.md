# ADR 0003: LUX qualifies but does not authorize

- Status: proposed
- Date: 2026-07-23
- Decision owners: Human Steward, Steward, Verifier, Adversary, Referee

## Context

INTELLECT governs work and authority, while AETHER supplies authoritative provenance and replay. LUX introduces measurements that may support an autonomy decision. Allowing a benchmark component to grant its own permissions would collapse measurement, judgment, and execution into one mechanism.

## Decision

LUX is a subordinate qualification profile within INTELLECT.

It may:

- define scenario and evidence contracts;
- calculate trait and stability metrics;
- report whether declared policy thresholds are met;
- recommend an autonomy ceiling;
- state that Human Steward authorization is required.

It may not:

- change credentials or permissions;
- deploy a model;
- advance an INTELLECT phase automatically;
- replace Council review;
- make its local storage authoritative;
- enable broad autonomy in v0.

AETHER remains the production authority for evidence order, provenance, policy visibility, and replay. The INTELLECT Constitution remains the authority for safety-critical deployment and autonomous permission escalation.

## Alternatives considered

### Standalone LUX service with actuator access

Rejected. It creates a self-certifying safety boundary and a second source of governance truth.

### Documentation-only doctrine

Rejected. It cannot fail closed, produce reproducible reports, or prevent numerical thresholds from drifting silently.

### Immediate constitutional gate modification

Deferred. The v0 kernel should first generate evidence about the adequacy and burden of the proposed profile. Constitutional integration requires a later amendment with migration plan, threat analysis, executable gates, and explicit Human Steward approval.

## Consequences

Positive:

- qualification is testable without granting power;
- policy can mature before constitutional embedding;
- broad autonomy is explicitly unavailable;
- existing INTELLECT separation of powers is preserved.

Costs:

- a passing report still requires a separate governance decision;
- the evidence graph is not yet compiled into AETHER rules;
- operators must resist treating the report as an automatic certificate.

## Reversal conditions

Revisit when:

- live AETHER integration can derive qualification from authoritative evidence;
- the scenario ontology and grader audit have survived external red-teaming;
- a constitutional amendment is proposed for risk-class-dependent autonomy gates;
- evidence supports changing the disabled status of any tier.
