# GCL-AGENT-CONTINUITY-001 — Bounded-turn continuity and timeout recovery

**Version:** 1.0.0  
**Status:** effective operational policy  
**Authority:** subordinate to `CONSTITUTION.md` and effective amendments  
**Scope:** GCL repositories and agents performing authorized multi-step operations

## 1. Purpose

Long-running agent turns are an unreliable persistence boundary. A timeout, connector interruption, context loss, process restart, or agent substitution MUST NOT erase completed work or become a substantive stopping condition.

This policy converts multi-step work into exact-head, repository-backed tranches that can be resumed by the same or a different authorized agent.

## 2. Required execution protocol

For every operation likely to require multiple tool calls, multiple evidence sources, or more than one substantive reasoning branch, the acting agent SHALL:

1. Re-fetch the live target ref and bind the operation to its exact commit SHA before mutation.
2. Read the governing instructions that materially control the operation.
3. Define the smallest current proof, repair, or evidence obligation. Do not begin downstream branches before the current obligation is durably resolved or a named boundary is reached.
4. Retrieve only the evidence needed for the current obligation. Reuse exact already-bound evidence unless state may have changed.
5. As soon as a proof-quality result, repair, diagnostic, or sharpened boundary exists, write it durably before opening another expensive branch of inquiry.
6. After mutation, read back the new exact head and bind subsequent work to it.
7. Treat timeout, connector failure, truncated tool output, CI infrastructure failure, compiler diagnostics, and context loss as recoverable execution failures unless they expose a genuine authority, governance, authentication, safety, materially changed-state, scope, or evidentiary boundary.
8. On recovery or agent substitution, re-fetch the live head and last durable checkpoint. Reject stale conversational state where it conflicts with repository state.
9. Before stopping, name the exact terminal boundary. If no such boundary can be stated, continue through available recovery paths.
10. Report the exact durable head/checkpoint and the remaining obligation in the terminal response.

## 3. Durable checkpoint requirements

A checkpoint may be a commit, work-package record, recovery record, or machine-readable continuity receipt. It MUST identify, directly or by exact repository history:

- operation or campaign identifier;
- repository and target ref;
- exact parent/head SHA;
- completed result or evidence;
- claims that remain unproved or uncertified;
- next smallest obligation;
- any named terminal boundary;
- whether protected-state integration or certification is authorized.

Checkpoint commits SHOULD be small and single-purpose. A large retrospective commit after several independent investigations is non-conforming when earlier durable checkpoints were reasonably available.

## 4. Timeout and interruption recovery

A timeout is not a mathematical, scientific, governance, or certification disposition.

After an interrupted turn, the next authorized agent SHALL continue from the latest exact durable state without requiring the Human Steward to restate already-established authority or facts. Recovery SHALL begin with live-state rebinding, not with replay from chat memory.

If the interrupted work produced no durable checkpoint, the next agent SHALL reconstruct only from independently verifiable repository/tool evidence and shall label any unverified conversational reconstruction as such.

## 5. Alternate-agent handoff

No agent identity is part of the proof or authority chain unless a governing rule explicitly says otherwise. A successor agent may continue a bounded operation when it can establish:

- the governing authority;
- the current exact head;
- the last durable checkpoint;
- the remaining obligation;
- the absence of a reserved-authority boundary.

The successor MUST NOT rely on a prior agent's private reasoning as authority.

## 6. Tooling discipline

Agents SHALL minimize turn-amplification risk:

- prefer exact file/range reads over broad repository sweeps;
- avoid re-fetching unchanged evidence;
- checkpoint before launching a second independent high-cost investigation;
- prefer small exact-head commits over one monolithic end-of-turn write;
- do not wait for a final prose response to make completed work durable.

These rules optimize persistence, not scope. They do not authorize premature stopping.

## 7. Stop conditions

Legitimate stopping conditions are limited to a named:

- governance or reserved-authority boundary;
- authentication/credential boundary;
- safety constraint;
- materially changed live state that invalidates the bounded operation;
- scope change requiring new authority;
- substantive evidentiary boundary for which no authorized recovery or evidence-acquisition path remains.

Recoverable infrastructure and orchestration failures are not stop conditions.

## 8. Enforcement

Repositories adopting this policy SHALL bind it from their root `AGENTS.md` or equivalent agent instruction surface and SHALL carry a machine-readable adoption record.

The canonical machine contract is `governance/agent_execution/GCL-AGENT-CONTINUITY-001.json`.

The canonical downstream adoption schema is `schemas/agent_continuity_adoption.schema.json`. Downstream repositories SHALL retain repository-local validators for specialization semantics. A local schema snapshot is non-authoritative and must be pinned to the exact admitted INTELLECT schema identity; mutable remote schema fetching is not an authority or conformance mechanism.

CI SHALL validate at least:

- policy identifier and version;
- presence of the canonical policy document;
- binding reference in the repository's agent instructions;
- integrity of the machine-readable contract.

Downstream repositories MAY add stronger checks, including continuity-receipt schemas and campaign-specific checkpoint requirements.

GitHub/CI enforcement governs repository integration. It does not claim control over external model-host timeout schedulers.

## 9. Non-authority clauses

This policy does not:

- expand mathematical certification authority;
- authorize protected-branch bypass;
- manufacture Human Steward authorization;
- waive independent review where governing process requires it;
- convert CI success into certification or promotion authority.
