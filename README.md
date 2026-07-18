# The Grand Intellect

**A constitutional architecture for collective intelligence, implemented over the AETHER semantic coordination fabric.**

The Grand Intellect turns a collection of agents into a governed cognitive institution. It separates the production of possibilities, contact with reality, purposive judgment, institutional memory, execution, review, and disposal so that no agent can manufacture and certify its own success.

> Intelligence is the disciplined production of alternatives, their confrontation with reality, their selection under purpose, their preservation across time, their realization as consequential artifacts, and the deliberate removal of what no longer deserves cognitive space.

## Current release boundary

This repository is an **executable foundation**, not a completed autonomous research institution.

Implemented now:

- an event-sourced work-package model;
- eight constitutional phase gates;
- five Minder offices, ten Council offices, Executor and Human Steward offices;
- explicit office mandates and phase-specific review obligations;
- replayable reviews, decisions, contact records, memory records, and disposal records;
- an agent registry and Council dispatcher that preserve office separation;
- a deterministic in-memory fabric for tests only;
- an authoritative HTTP adapter for AETHER's append, cut, history, policy, and provenance boundary;
- JSON schemas, work-package templates, a CLI, an example campaign, and CI.

Not yet implemented:

- a production AETHER deployment bundled with this repository;
- model-provider adapters or autonomous agent prompting;
- semantic compilation of every constitutional gate into AETHER rules;
- distributed execution, scheduling, leases, or artifact sidecars owned by INTELLECT;
- a user interface;
- unattended authority over irreversible actions.

The project fails closed when an obligation is absent. It does not infer that an agent reviewed a work package merely because the agent was invoked.

## Architecture in one page

```text
Human Steward
     │
     ▼
Grand Intellect application layer
  ├── Work-package commands
  ├── Executable constitution
  ├── Minder cycle
  ├── Council review dispatch
  ├── Artifact and decision contracts
  └── Gate reports
     │
     ▼
AETHER semantic coordination fabric
  ├── Append-only datoms
  ├── Authoritative cuts and replay
  ├── Policy-aware visibility
  ├── Provenance-bearing facts
  ├── Recursive semantic closure
  └── Explainable derived tuples
     │
     ▼
Executors, repositories, experiments, proofs, datasets, and deployments
```

INTELLECT is a constitutional application over AETHER, not a competing semantic kernel. The Python layer may project AETHER history and provide admission checks, but production truth remains anchored to AETHER.

## The three orders

### The Minders

The Minders govern the lifecycle of thought:

- **Possibility Minder:** produces materially distinct alternatives;
- **Reality Minder:** demands evidence capable of changing judgment;
- **Purpose Minder:** selects under explicit objectives and trade-offs;
- **Continuity Minder:** preserves reasons, scope, provenance, and lineage;
- **Capacity Minder:** retires what no longer earns active attention.

### The Council

The Council governs intellectual rigor through bounded offices:

- Axiomatist;
- Cartographer;
- Verifier;
- Adversary;
- Formalist;
- Steward;
- Grammarian;
- Composer;
- Amanuensis;
- Referee.

Each office discharges a distinct obligation. Review is evidence of work performed, not attendance.

### The Executors

Executors build proofs, programs, experiments, datasets, reports, and deployments under an explicit specification. They may realize an approved contract but may not silently redefine it.

## Work-package lifecycle

```text
Charter
  → Generation
  → Specification
  → Realization
  → Confrontation
  → Judgment
  → Integration
  → Disposal
  → Complete
                  ↘ governed reopening → Generation
```

Every transition requires both substantive artifacts and approved office reviews. For example, the Confrontation gate requires a contact record whose test could have disconfirmed the claim, an uncertainty statement, and approved Reality Minder, Verifier, and Adversary reviews.

See [`CONSTITUTION.md`](CONSTITUTION.md) and [`docs/WORK_PACKAGE_LIFECYCLE.md`](docs/WORK_PACKAGE_LIFECYCLE.md).

## Quick start

Python 3.11 or later is required. The core has no runtime dependencies outside the standard library.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
python examples/union_closed_bootstrap.py
intellect init work/WP-001 WP-001 \
  --title "Test a claim" \
  --purpose "Confront a mechanism with discriminating evidence" \
  --scope "One candidate implementation and benchmark" \
  --criterion "The benchmark can reject the mechanism"
intellect gate work/WP-001/events.jsonl WP-001
intellect metrics work/WP-001/events.jsonl WP-001
```

The in-memory fabric is a test double. A production construction must require an authoritative AETHER fabric:

```python
from grand_intellect import GrandIntellect
from grand_intellect.aether import AetherHttpFabric

fabric = AetherHttpFabric(
    "https://aether.example",
    bearer_token="...",
    namespace="grand-intellect",
    schema_ref={"name": "intellect_v0", "version": 0},
)

system = GrandIntellect(fabric, require_authoritative_fabric=True)
```

## Minimal governed cycle

```python
from grand_intellect import GrandIntellect, InMemoryFabric, Office, ReviewStatus

system = GrandIntellect(InMemoryFabric())
system.charter(
    "WP-001",
    title="Test a claim",
    purpose="Determine whether the proposed mechanism survives controlled evidence.",
    scope="One implementation and one discriminating benchmark.",
    acceptance_criteria=("The benchmark can reject the mechanism",),
)

for office in system.constitution.required_offices(system.state("WP-001").phase):
    system.submit_review(
        "WP-001",
        office=office,
        status=ReviewStatus.APPROVED,
        obligations=tuple(sorted(system.constitution.required_obligations(system.state("WP-001").phase, office))),
        evidence_refs=("CHARTER.md",),
    )

system.advance("WP-001")
```

## AETHER integration

AETHER's current public boundary provides the exact facilities INTELLECT needs: append-only datoms, deterministic replay, policy-aware visibility, provenance, recursive derivation, and explanation. INTELLECT uses the stable HTTP boundary rather than importing or duplicating Rust kernel semantics.

The versioned event mapping is defined in [`aether/intellect_v0.aether`](aether/intellect_v0.aether). The adapter:

1. checks required server capabilities;
2. encodes each INTELLECT event as one AETHER entity;
3. appends tagged scalar datoms with provenance and policy envelopes;
4. receives an authoritative cut;
5. reconstructs work-package history through bounded pagination;
6. projects that history into the constitutional view.

See [`aether/README.md`](aether/README.md) and [`docs/adr/0001-aether-is-authoritative.md`](docs/adr/0001-aether-is-authoritative.md).

## Repository map

```text
src/grand_intellect/     executable constitutional runtime
schemas/                  machine-readable event and artifact contracts
aether/                   AETHER schema and boundary documentation
examples/                 governed campaign exemplars
tests/                    lifecycle, agent, CLI, and adapter tests
docs/                     architecture, pedagogy, threats, roadmap, templates
.github/workflows/        required validation
```

## Development contract

Before proposing a change:

```bash
python -m compileall -q src tests examples
python -m unittest discover -s tests -v
python examples/union_closed_bootstrap.py
intellect init work/WP-001 WP-001 \
  --title "Test a claim" \
  --purpose "Confront a mechanism with discriminating evidence" \
  --scope "One candidate implementation and benchmark" \
  --criterion "The benchmark can reject the mechanism"
intellect gate work/WP-001/events.jsonl WP-001
intellect metrics work/WP-001/events.jsonl WP-001
```

A change that modifies office powers, phase gates, deletion authority, or the AETHER truth boundary is constitutional. It requires an ADR, explicit threat analysis, and Human Steward review.

## Read next

1. [`CONSTITUTION.md`](CONSTITUTION.md)
2. [`SPEC.md`](SPEC.md)
3. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
4. [`docs/PEDAGOGY.md`](docs/PEDAGOGY.md)
5. [`docs/ROADMAP.md`](docs/ROADMAP.md)
6. [`docs/STATUS.md`](docs/STATUS.md)
