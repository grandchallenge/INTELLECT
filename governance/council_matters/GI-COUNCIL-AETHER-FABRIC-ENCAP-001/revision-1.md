# GI-COUNCIL-AETHER-FABRIC-ENCAP-001 — Revision 1

## Purpose of this revision

This revision responds to the first full-Council review of exact subject
`59d71383f051a49ed88f0b375a19f9f332e10a13`.

It supplements, rather than rewrites, `proposal.md`. Where this revision is more
specific, it controls the resubmitted architecture recommendation. It does not
amend the Constitution or activate any implementation.

## R1. Canonical terminology

For this matter:

- **AETHER semantic authority** means authority over admitted semantic state
  within AETHER's governed domain: append order, cuts, replay, schema admission,
  policy visibility, provenance-bearing facts, recursive derivation, proof
  traces, and semantic acceptance/rejection.
- **Semantic authority does not mean constitutional authority, universal
  epistemic truth, or permission to alter institutional policy.**
- **FABRIC** means the proposed independently encapsulated mechanical
  coordination/data plane.
- **Mechanical coordination** means delivery, rendezvous, locality, placement,
  buffering, fan-out/fan-in, stream movement, retry mechanics, operational
  liveness, and replication/movement mechanics under an already authorized
  envelope.
- **Institutional allocation** means a governed choice of who/what class ought to
  undertake work. It belongs to POL/AETHER or a governed allocator whose
  decision is recorded/admitted through AETHER.
- **Physical realization** means mapping an already authorized allocation into a
  concrete endpoint/path/resource realization. It may belong to FABRIC.
- **Admission** means AETHER's governed act of accepting an input into semantic
  state. Arrival or delivery is not admission.
- **Operational lease** means temporary mechanical ownership of a resource or
  delivery slot.
- **Semantic authority lease** means a governed AETHER fact/contract that may
  authorize an actor to act within a semantic work domain.
- **Endpoint identity** means process/service/resource identity used by FABRIC.
- **Semantic actor identity** means identity represented in AETHER facts.
- **Institutional office identity** means an INTELLECT/POL role carrying bounded
  authority.
- **Controller identity** means an executor admitted under GHOS control policy.

Historical uses of “AETHER fabric” or “semantic coordination fabric” remain
valid descriptions of the pre-separation architecture. They must not be
retroactively interpreted as references to the future FABRIC component. New
documents after any effective separation should avoid unqualified use of
“fabric” when the distinction matters.

“Semantically subordinate” means **non-authoritative with respect to semantic
admission and institutional meaning**. It does not mean that AETHER is an
operational command-and-control parent of FABRIC.

## R2. Influence without authority

Round 1 correctly identified that a mechanical system can exercise de facto
institutional influence without declaring semantic authority.

FABRIC may affect latency, availability, locality, and cost. Those effects can
change which work completes or which evidence arrives. Therefore the separation
must govern influence channels, not only truth declarations.

### R2.1 Authorized optimization envelope

FABRIC may optimize only inside an **authorized mechanical envelope** supplied
by an upstream governed decision or static deployment policy.

An optimization envelope may constrain:

- eligible endpoint/resource classes;
- cost/latency bounds;
- locality preferences;
- retry budget;
- redundancy factor;
- priority class;
- deadline/TTL;
- privacy/trust-zone constraints.

FABRIC may optimize the realization within those bounds.

FABRIC must not independently choose:

- the institutional purpose of work;
- which claim deserves investigation;
- which evidence class may be suppressed;
- which guild/office has authority;
- whether a semantic claim is accepted;
- whether a blocked action becomes permitted;
- whether a constitutional or policy constraint may be relaxed.

### R2.2 Prohibited policy laundering

The following are semantic/control violations even if implemented through
mechanical mechanisms:

- intentional starvation of an authorized work class for non-mechanical reasons;
- selective delivery or suppression intended to alter institutional judgment;
- retry asymmetry that encodes an undeclared policy preference;
- priority inversion that bypasses an institutional allocation;
- endpoint filtering that changes authorized actor eligibility;
- locality policy that violates declared trust/visibility boundaries;
- fabricated or strategically biased resource advertisements;
- treating missing transport as negative evidence.

### R2.3 Mechanical-policy authority

Whoever configures a FABRIC optimization policy must have authority to set
mechanical execution policy for that deployment. That authority is not created
by FABRIC.

A deployment must bind:

`mechanical_policy_id -> authorizing principal/office -> scope -> version -> expiry`

AETHER may record that binding for provenance and audit. FABRIC may consume an
opaque or mechanically checkable policy envelope but must not widen it.

### R2.4 Compromise and containment

A compromised/unavailable FABRIC must be modeled as an operational fault, not an
epistemic conclusion.

AETHER must be able to distinguish:

- `not delivered / unknown`;
- `delivered but not admitted`;
- `admitted`;
- `rejected`.

The architecture must provide a containment mode in which FABRIC can be
disabled while AETHER retains local semantic correctness and recoverable work
state.

## R3. Normative event separation

The interface law must treat these as distinct typed events:

1. `AllocationDesired`
2. `MechanicalEnvelopeAuthorized`
3. `RouteRealized`
4. `PayloadDispatched`
5. `PayloadDelivered`
6. `DeliveryReceiptObserved`
7. `SemanticSubmissionProposed`
8. `SemanticAdmissionAccepted | SemanticAdmissionRejected`
9. `InstitutionalDecisionRecorded`

No event may be inferred solely from the existence of a later event unless a
normative contract explicitly defines the derivation.

In particular:

`PayloadDelivered` does not imply `SemanticAdmissionAccepted`.

`RouteRealized` does not imply `AllocationDesired` was authorized.

`DeliveryReceiptObserved` does not imply the payload is correct.

## R4. Identity strata

The implementation must preserve at least four non-collapsible identity strata:

| Stratum | Example | Authority implication |
| --- | --- | --- |
| endpoint/resource | process, worker, GPU, service | none by itself |
| semantic actor | AETHER agent/entity identity | semantic provenance only unless separately authorized |
| institutional office | Steward, Verifier, Guild office | bounded authority under POL/INTELLECT |
| execution controller | GHOS-admitted controller | execution authority only within admitted route |

Bridges among strata must be explicit facts/contracts and must not be inferred
from equal names, addresses, credentials, or co-location.

## R5. Semantic equivalence and E2 conformance

For E2, **semantic equivalence** means that, for the same admitted semantic
inputs and effective policy context, direct/local AETHER and
AETHER-over-reference-FABRIC produce equivalent canonical semantic outputs:

- semantic cuts;
- resolved facts;
- derived tuples;
- policy visibility;
- provenance source identities;
- proof traces;
- accepted/rejected semantic admissions.

Permitted differences are restricted to separately typed operational metadata,
such as transport timing, endpoint address, queue depth, or route realization.

The E2 conformance harness must:

1. run identical semantic workloads in direct/local mode;
2. run them through the reference FABRIC adapter;
3. canonicalize permitted operational metadata away;
4. compare all semantic outputs;
5. fail closed on any unexplained divergence.

Hostile cases must include duplication, reordering, stale endpoint delivery,
message loss, delayed delivery, retry, FABRIC restart, protocol mismatch,
invalid envelope, forged resource advertisement, and replay amplification.

## R6. Distributed truth and authority partitions

The separation must not move semantic fencing into FABRIC.

AETHER retains:

- authority-partition identity;
- semantic cut identity;
- leader/authority epoch semantics where admitted;
- stale-epoch semantic rejection;
- imported-fact provenance;
- semantic conflict/fencing decisions.

FABRIC may provide:

- byte/message replication;
- stream transport;
- follower data movement;
- topology/locality;
- retry/backpressure;
- physical health/liveness observations.

A FABRIC replica is not an AETHER authority replica merely because it contains
the same bytes.

If future evidence shows a primitive truly belongs below AETHER and above raw
FABRIC, the correct response is a separately reviewed shared contract/layer, not
silent semantic migration.

## R7. AETHER-MEM and sidecars

For governed memory:

AETHER owns semantic identity, provenance, validity, visibility, relations,
admission, and retrieval-policy meaning.

FABRIC may coordinate physical storage locality, shard movement, artifact
transport, cache placement, or vector-shard movement.

A retrieval rank, cache hit, or physical availability event is not itself an
AETHER semantic judgment.

Existing sidecars remain subordinate to semantic control.

## R8. Migration and lineage obligations

No current AETHER responsibility moves solely because it “looks distributed.”

Every proposed move requires a migration ledger entry containing:

- responsibility name;
- current repository/path/module;
- current semantic/control dependencies;
- proposed owner;
- classification (`SEMANTIC`, `INSTITUTIONAL`, `EXECUTION`, `FABRIC`,
  `AMBIGUOUS`);
- rationale;
- conformance evidence;
- compatibility plan;
- rollback path;
- effective version.

Historical records and the stale 2026 AETHER-POL PR remain part of lineage and
must not be rewritten as though the separation had always existed.

Any deprecated AETHER API must have a compatibility window and explicit
replacement contract.

## R9. E0–E4 stop/go criteria

### E0 -> E1

Proceed only when:

- all material current responsibilities have an owner classification;
- every `AMBIGUOUS` item has an explicit unresolved record;
- no proposed FABRIC responsibility includes semantic admission or
  constitutional authority.

### E1 -> E2

Proceed only when:

- interface schemas are versioned;
- event types in R3 are explicit;
- identity strata are explicit;
- failure/non-guarantee semantics are specified;
- incompatible versions fail closed.

### E2 -> E3

Proceed only when:

- semantic-equivalence conformance is green;
- hostile duplication/reordering/loss/replay cases are green;
- FABRIC can be disabled without semantic corruption;
- no hidden direct policy channel is observed.

### E3 -> E4

Independent FABRIC encapsulation/repository is justified only when:

- extracted responsibilities remain mechanically coherent;
- AETHER local mode remains green;
- maintenance/incident ownership is assigned;
- compatibility burden is measured and accepted;
- at least one useful non-AETHER workload runs on the same FABRIC contract;
- evidence shows the separation reduces coupling/failure blast radius or enables
  material reuse sufficient to justify permanent interface cost.

Failure of these gates returns the programme to the prior stage; it does not
force extraction.

## R10. Cross-plane trace model

A complete operation should be reconstructible without collapsing event types.

A cross-plane correlation record may bind:

`mandate/work -> allocation -> mechanical policy -> route -> controller execution -> delivery -> semantic submission -> admission -> decision`

The trace may share correlation identifiers, but each plane owns its own event
semantics.

Operational telemetry becomes AETHER evidence only through normal semantic
submission/admission with provenance.

## R11. Council-requested architecture wording

The revised recommended architecture statement is:

> AETHER is the authoritative semantic substrate within its admitted domain.
> FABRIC is an independently encapsulated mechanical coordination/data plane.
> FABRIC may realize authorized movement, placement, rendezvous, streaming,
> replication, and operational optimization, but cannot create semantic
> admission, institutional permission, or constitutional authority.
> POL supplies institutional semantics over AETHER. GHOS remains independently
> responsible for governed persistent execution. INTELLECT remains
> constitutional authority.

This wording replaces any implication that AETHER is universal truth or that
FABRIC is operationally commanded by AETHER.

## R12. Requested reconsideration

The proposer asks the full Council to reconsider the architecture on the
combined subject:

- original proposal; and
- this Revision 1.

An `approve` or `approve_with_conditions` disposition remains architectural and
advisory only.

If the Council recommends the architecture, a later Article XI packet must
separately supply the constitutional ADR, Adversary threat analysis,
compatibility/migration plan, executable gates/tests, Human Steward approval,
and explicit effective version before Article IX or the AETHER authority
boundary changes.
