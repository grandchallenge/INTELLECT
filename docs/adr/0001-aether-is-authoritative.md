# ADR-0001: AETHER is the authoritative semantic substrate

- Status: Accepted
- Date: 2026-07-18
- Constitutional: Yes

## Context

INTELLECT requires durable coordination facts, temporal replay, provenance, policy-aware visibility, recursive derivation, and explanation. Implementing these semantics again in Python would create competing truth systems and violate AETHER's language boundary.

## Decision

AETHER is the authoritative production substrate. INTELLECT is a constitutional application over AETHER's stable HTTP boundary.

The Python runtime may validate commands, project authoritative history, evaluate application policy gates, dispatch office agents, and render reports. It may not claim authoritative append order, replay, policy, provenance, or recursive truth independently of AETHER.

## Consequences

Benefits include one semantic center, replayable institutional history, preserved provenance and explanation, and a clear Python application boundary.

Costs include a production dependency on AETHER, temporary dual representation of some gate logic, cross-repository schema versioning, and required live conformance infrastructure.

## Rejected alternatives

A Python event database was rejected as a shadow kernel. Direct Rust embedding was deferred because the HTTP boundary provides cleaner deployment separation. A generic queue was rejected because delivery order does not provide semantic replay, recursive derivation, policy, provenance, or explanation.
