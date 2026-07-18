# Instructions for implementation agents

## Source of authority

Read, in order:

1. `CONSTITUTION.md`;
2. `SPEC.md`;
3. `docs/ARCHITECTURE.md`;
4. the relevant ADRs;
5. executable tests.

Prose governs intent; tests govern the current executable contract. A conflict between them is a defect to surface, not an invitation to choose silently.

## Non-negotiable boundaries

- Do not make the in-memory fabric authoritative.
- Do not reimplement AETHER resolver or rule semantics in Python.
- Do not auto-approve reviews.
- Do not auto-advance gates after Council dispatch.
- Do not weaken gate minima without a constitutional ADR.
- Do not delete institutional records without explicit authorization.
- Do not store credentials in events or fixtures.
- Do not treat model hidden reasoning as institutional evidence.

## Definition of done

A change is complete when:

- behavior is covered by tests;
- source and examples compile;
- documentation reflects the implementation boundary;
- new institutional events are replayable;
- new reviews state obligations;
- AETHER wire changes are versioned;
- constitutional changes include threat analysis and Human Steward approval.
