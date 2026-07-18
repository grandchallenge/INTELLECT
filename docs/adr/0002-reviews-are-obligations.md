# ADR-0002: Reviews are obligation records, not attendance

- Status: Accepted
- Date: 2026-07-18
- Constitutional: Yes

## Context

Multi-agent systems often count an invoked role as a completed review. This permits ceremonial governance: agents are named, but no specific intellectual burden is discharged.

## Decision

A review satisfies a gate only when it records the reviewing office, current phase, approval status, exact discharged obligations, findings when applicable, and evidence references through the event record.

The latest review by an office controls its current gate status. A later request for changes revokes an earlier approval. A Council dispatcher records reviews but cannot advance a phase.

## Consequences

The system distinguishes presence from work and objection from approval. It requires structured agent outputs and makes superficial consensus less convenient, which is intentional.
