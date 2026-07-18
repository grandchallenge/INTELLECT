# AETHER Boundary

AETHER is the authoritative semantic substrate for INTELLECT deployments. It owns append order, cuts, replay, effective policy, provenance, and derived tuples. INTELLECT owns constitutional policy, agent-office obligations, work-package artifacts, and application commands.

The boundary is intentionally asymmetric:

- INTELLECT appends versioned event envelopes as AETHER datoms.
- AETHER returns authoritative receipts and replayable history.
- INTELLECT projects that history into a work-package view and evaluates the executable constitution.
- The in-memory fabric exists only for deterministic tests and local pedagogy.

## Deployment contract

The adapter requires AETHER's documented Python-boundary preflight capabilities, `resource_limits_v1` and `pagination_v1`. It sends `X-Aether-Namespace`, bearer authentication, schema references, idempotency keys, provenance, and a policy envelope on every append.

Attribute IDs `1-8` are reserved by `intellect_v0.aether`. A production deployment must register the schema and pass the returned schema reference to `AetherHttpFabric`.

## Semantic closure roadmap

The first release deliberately keeps cardinality-heavy gate checks in the executable constitution. Subsequent work should compile progressively more of the gate model into AETHER rules, while retaining one conformance suite that proves application reports and AETHER-derived reports agree.
