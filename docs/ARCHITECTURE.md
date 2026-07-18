# Architecture

## 1. System boundary

INTELLECT is the constitutional application layer of the Grand Intellect. AETHER is the authoritative semantic coordination substrate. Repositories, theorem provers, experiment runners, data systems, and deployment platforms are execution surfaces.

> INTELLECT decides what institutional obligations exist; AETHER establishes what coordination facts are authoritatively present and why.

## 2. Components

- `model.py` defines offices, phases, reviews, dispositions, decisions, immutable events, projected work-package state, and deterministic replay.
- `fabric.py` defines append and ordered-history boundaries. `InMemoryFabric` is non-authoritative.
- `constitution.py` defines explanatory phase gates combining substance and office obligations.
- `engine.py` defines lawful commands and phase restrictions. Commands emit events and never mutate projected state directly.
- `agents.py` defines office-bounded reviewers, one-agent-per-office registration, and Council dispatch without automatic advancement.
- `aether.py` implements the production HTTP boundary without reimplementing AETHER resolver or rule semantics.
- `cli.py` and `workspace.py` provide local inspection and authoring projections, not semantic authority.

## 3. Command path

```text
command
  │ validate phase and payload
  ▼
IntellectEvent
  │ append
  ▼
CoordinationFabric
  │ authoritative cut / replay
  ▼
ordered history
  │ project
  ▼
WorkPackageState
  │ evaluate
  ▼
GateReport
```

No command mutates `WorkPackageState`. State is reconstructed from history.

## 4. Agent review path

```text
Constitution.required_offices(phase)
  │
  ▼
AgentRegistry
  │ one bounded office per agent
  ▼
AgentContext
  │ mandate + obligations + projected state
  ▼
AgentReviewDecision
  │
  ▼
review.submitted event
  │
  ▼
GateReport
```

Agent decisions count only when translated into explicit institutional records.

## 5. AETHER event representation

Each event becomes one AETHER entity. Eight scalar attributes store event type, work-package ID, actor, canonical JSON payload, occurrence time, event ID, correlation ID, and causation ID.

The adapter uses stable hashes for entity and element IDs. Retries are deterministic at the mapping layer; AETHER idempotency keys remain authoritative duplicate control.

## 6. Progressive semantic compilation

The initial constitution runs in Python because several gates use cardinality and structured-document checks that should not be approximated.

The long-term process is:

1. express a gate predicate in AETHER;
2. retain the application gate as a conformance oracle;
3. run both over identical history;
4. require agreement;
5. expose AETHER proof traces;
6. retire duplicated application checks only after equivalence is established.

## 7. Consistency and security

The foundation assumes ordered history per AETHER namespace and schema reference. Distributed work must use explicit partition cuts rather than a fictitious global clock.

Credentials remain process configuration. Visibility is assigned at append and narrowed by effective policy; client assertions never widen authority.

## 8. Extension classes

Safe extensions include office-agent implementations, provider adapters behind `OfficeAgent`, artifact sidecar clients, reports, CLI projections, and conformance tests.

Constitutional changes include office creation or removal, changed gate minima, phase-order changes, automatic advancement, deletion authority, semantic-substrate changes, and expanded autonomous permissions.
