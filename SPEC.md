# Grand Intellect Foundation Specification

## 1. Objective

Build an executable constitutional control plane for collective agent work over AETHER. The foundation must turn work-package governance into explicit commands, immutable events, replayable state, admission gates, office-bounded reviews, and machine-readable artifacts.

## 2. Defensible claim

Version `0.1.0` may claim:

> INTELLECT can govern one work package through a complete epistemic lifecycle using deterministic event projection and explicit constitutional gates, while exposing an authoritative production boundary to AETHER.

It may not claim autonomous scientific discovery, fully semantic gate compilation, distributed scheduling, or production readiness.

## 3. Design principles

1. **Constitution before orchestration.** Agent activity is subordinate to explicit powers and obligations.
2. **Events before mutable records.** Institutional state must be reconstructible.
3. **Evidence before closure.** No transition from Confrontation without a disconfirmable test.
4. **Reasons before summaries.** Memory records retain scope, limitations, and decision lineage.
5. **Disposal before completion.** Completion requires an explicit active-set decision and residual frontier.
6. **AETHER before shadow semantics.** Production coordination truth remains in AETHER.
7. **Fail closed.** Missing reviews or artifacts block advancement.
8. **Proportional governance.** Future risk classes may deepen gates, but shall not silently weaken constitutional minima.

## 4. Functional requirements

### FR-1 Event envelope

Every institutional mutation shall produce an `IntellectEvent` with a globally unique event ID, event type, work-package ID, actor, payload, UTC timestamp, correlation ID, optional causation ID, and optional idempotency key.

### FR-2 Replay

The work-package state shall be reconstructible solely from ordered events. Projection must be deterministic for the same event sequence.

### FR-3 Constitutional gates

The runtime shall expose a gate report containing current phase, target phase, readiness, satisfied conditions, and missing conditions. Advancement shall fail when any condition is missing.

### FR-4 Office review

A review shall contain office, phase, status, discharged obligations, findings, evidence references, and actor identity through the event envelope. An empty obligation set shall not satisfy a gate.

### FR-5 Agent dispatch

The runtime shall support registration of one agent per office and dispatch required gate reviews through office-specific contexts. The Council dispatcher shall record reviews but shall not advance a phase automatically.

### FR-6 Disposal safety

A deletion disposition shall require explicit authorization. Non-destructive dispositions shall retain a recovery path where applicable.

### FR-7 Reopening

A completed work package may reopen only through an explicit event containing a reason. The first reopened phase shall be Generation.

### FR-8 AETHER adapter

The production fabric adapter shall preflight documented capabilities; send bearer authentication and namespace headers; use a registered schema reference; append tagged AETHER datoms; attach provenance and policy envelopes; preserve idempotency keys; parse authoritative cuts; and retrieve history through bounded pagination.

### FR-9 Test-only fabric

The in-memory fabric shall declare itself non-authoritative. Production construction may require an authoritative fabric and reject the test double.

### FR-10 Schemas and templates

Machine-readable schemas shall exist for events, work-package charters, and agent reviews. Human-readable templates shall align with those schemas.

## 5. Non-functional requirements

- Projection and gate evaluation must be deterministic for an ordered event history.
- Every transition must identify the conditions that admitted it.
- Gate reports must explain missing and satisfied obligations.
- The foundation shall run on Python 3.11+ without third-party runtime dependencies.
- The fabric and agent boundaries must be injectable; unit tests require no network access.
- Documentation must distinguish implemented behavior, test doubles, integration contracts, and future work.
- Credentials shall never be stored in events, artifacts, examples, or logs.

## 6. Data model

The event projector maintains charter fields, current phase, alternatives, specification, realizations, contact records, reviews, judgment, memory records, disposal records, residual frontier, transition history, and event IDs.

The model intentionally avoids embedding model-provider prompts or hidden reasoning. Agent outputs become institutional only through explicit, reviewable records.

## 7. AETHER mapping

One INTELLECT event maps to one AETHER entity. Eight scalar attributes store event type, work-package ID, actor, canonical JSON payload, occurrence time, event ID, correlation ID, and causation ID.

Attribute IDs are versioned by `aether/intellect_v0.aether` and the adapter's `AetherAttributeMap`.

## 8. Verification matrix

| Requirement | Evidence |
| --- | --- |
| FR-1, FR-2 | `tests/test_engine.py`, `tests/test_cli.py` |
| FR-3 | blocked-gate and complete-cycle tests |
| FR-4 | Council and lifecycle tests |
| FR-5 | `tests/test_agents.py` |
| FR-6 | deletion authorization test |
| FR-7 | reopening test |
| FR-8 | `tests/test_aether_adapter.py` |
| FR-9 | authoritative constructor guard test |
| FR-10 | `schemas/` and workspace materialization |

## 9. Acceptance criteria

The foundation is acceptable when all unit tests pass on Python 3.11 and 3.12; source, tests, and examples compile; the Union-Closed exemplar reaches Generation through explicit office reviews; incomplete work cannot advance; a complete cycle can reach Complete and reopen; AETHER wire contracts are tested; and documentation states the release boundary honestly.

## 10. Deferred work

- live AETHER conformance tests;
- schema registration automation;
- AETHER-derived gate predicates and proof traces;
- persistent artifact sidecar integration;
- lease-backed Executor claims;
- model-provider adapters;
- risk-class-dependent gate profiles;
- distributed Council sessions;
- operator interface and dashboards;
- repository automation for work-package materialization.
