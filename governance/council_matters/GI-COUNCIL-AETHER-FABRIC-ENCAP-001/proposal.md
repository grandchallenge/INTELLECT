# GI-COUNCIL-AETHER-FABRIC-ENCAP-001 — Proposal

## Title

Separate AETHER and FABRIC into independently encapsulated systems while preserving asymmetric semantics and GCL authority boundaries.

## Status

Before Council. Advisory proposal only. This document does not amend the Constitution, activate FABRIC, alter AETHER production semantic authority, change GHOS controller admission, or authorize deployment.

## Purpose

Determine whether GCL should deliberately separate the semantic authority now embodied by AETHER from the lower-level mechanical coordination and data-plane responsibilities historically associated with the word “fabric.”

The proposed separation is intended to make both systems stronger:

- AETHER may evolve toward a rigorous semantic substrate for POLITY without being forced to absorb transport, placement, topology, or throughput concerns.
- FABRIC may evolve toward a reusable distributed coordination/data plane without acquiring authority to decide what facts mean, what is institutionally accepted, or what action is authorized.
- GHOS remains an independently governed execution/control plane.
- INTELLECT remains the constitutional/governance authority.
- AETHER-POL remains the institutional semantic layer above AETHER.

## Live constitutional context

Article IX currently states that AETHER is the authoritative coordination substrate for production deployments and assigns AETHER append order, semantic cuts, replay, policy visibility, provenance-bearing facts, recursive derivation, and proof traces.

Article X reserves changes to the AETHER authority boundary to the Human Steward.

Article XI requires an ADR, Adversary threat analysis, compatibility/migration plan, updated executable gates/tests, Human Steward approval, and an explicit effective version for a constitutional amendment.

Therefore this Council matter is advisory. A Council disposition may recommend approval, approval with conditions, revision, or rejection, but cannot itself ratify any Article IX change.

## Proposed architecture

```text
                    GCL / INTELLECT
               mandate · governance · policy
                         │
                         ▼
                    AETHER-POL
              institutional semantics
         charter · office · guild · claim
            evidence · decision · residue
                         │
                         ▼
                       AETHER
                 semantic truth plane
       facts · rules · cuts · proof · provenance
        authority · admission · explanation
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
           FABRIC                   GHOS
    coordination/data plane   execution/control plane
    transport · rendezvous    controllers · wake
    placement · delivery      credentials · mutation
    streams · backpressure    protected execution
    replication mechanics
              │                     │
              └──────────┬──────────┘
                         ▼
              agents · models · tools
              stores · GPUs · services
```

This is a plane separation, not a semantic fork.

## Proposed doctrine

### AETHER

AETHER owns semantic authority within its admitted domain:

- append order;
- semantic cuts and replay;
- semantic identity;
- schema admission;
- policy visibility;
- provenance-bearing facts;
- recursive derivation;
- proof traces;
- authority-bearing semantic leases/contracts where defined;
- semantic acceptance/rejection of imported results;
- institutional truth consumed by POL.

AETHER correctness must not depend on FABRIC availability.

AETHER must remain fully usable in a local/single-node mode without FABRIC.

### FABRIC

FABRIC owns mechanically distributed coordination:

- endpoint discovery;
- rendezvous;
- payload delivery;
- fan-out and fan-in;
- topology and locality;
- placement hints;
- transport;
- streams;
- backpressure;
- retry mechanics;
- operational liveness;
- resource advertisement;
- replication and movement mechanics.

FABRIC may carry semantic envelopes but does not interpret them as institutional truth.

FABRIC mechanics must not require AETHER semantics. FABRIC should remain useful for distributed training, simulation, evaluation, inference, artifact movement, experimental sweeps, and other GCL/GCT workloads that do not require AETHER.

### GHOS

GHOS remains the governed execution/control plane.

Neither AETHER nor FABRIC is admitted as a substitute persistent controller merely because it participates in coordination.

Protected execution correctness must remain independent of AETHER/FABRIC availability unless a future separately governed controller-admission action says otherwise.

### POL

AETHER-POL remains the institutional semantic layer.

POL describes who may do what, under what charter, with what evidence, and how work/claims/decisions become institutionally meaningful.

POL semantics are interpreted through AETHER, not FABRIC.

### INTELLECT

INTELLECT remains constitutional/governance authority.

INTELLECT determines office obligations, mandates, work-package gates, constitutional policy, and authority schedules. Neither AETHER nor FABRIC may silently acquire those powers.

## Core laws

The following laws are proposed as non-negotiable invariants:

1. **FABRIC may carry a fact; it cannot make it true.**
2. **FABRIC may deliver an instruction; delivery does not confer authority.**
3. **FABRIC may carry a result; AETHER determines how that result enters institutional knowledge.**
4. **AETHER correctness must not depend on FABRIC availability.**
5. **FABRIC mechanics must not depend on AETHER semantics.**
6. **Operational liveness is not semantic authority.**
7. **Resource capability is not institutional permission.**
8. **Physical replication is not semantic consensus.**
9. **Transport success is not semantic admission.**
10. **Neither AETHER nor FABRIC may displace GHOS controller governance or INTELLECT constitutional authority by implementation convenience.**

## Boundary examples

### Work allocation

AETHER/POL may establish:

```text
work_open(W17)
requires_capability(W17, spectral_analysis)
route_authorized(W17, spectral_guild)
```

A learning allocator may select a desired agent/guild class.

FABRIC then realizes the mechanical placement and delivery to a concrete endpoint.

The receiving worker has no additional semantic authority merely because FABRIC delivered the work.

### Result return

A worker produces an artifact, result, and evidence.

FABRIC transports them.

AETHER may admit:

```text
asserts(agent_41, claim_93)
supported_by(claim_93, evidence_19)
```

Further verification/decision semantics remain above FABRIC.

### Memory

AETHER/AETHER-MEM knows the semantic identity, provenance, visibility, validity, and relations of a memory object.

FABRIC may locate and move the physical bytes, vector shards, or artifacts.

The payload is not made authoritative by availability or retrieval rank.

## Similar-looking concepts that must remain distinct

| FABRIC concept | AETHER concept | Required distinction |
| --- | --- | --- |
| operational lease | semantic authority lease | resource/liveness ownership is not action authority |
| endpoint identity | semantic actor identity | process address is not institutional identity |
| heartbeat | authority validity | liveness is not permission |
| replica | semantic copy/import | replicated bytes are not accepted truth |
| route | route decision record | physical path is not institutional allocation rationale |
| retry | causal replay | transport repetition is not semantic history |
| resource advertisement | capability assertion | hardware/service availability is not accepted capability |
| delivery receipt | admission record | arrival is not truth |

## Dependency law

The intended dependency graph is asymmetric but non-circular:

```text
POL -> AETHER
AETHER -> optional FABRIC adapter
FABRIC -> no AETHER semantic dependency
GHOS -> independent controller governance
```

Allowed:

- AETHER may use FABRIC as an optional transport/placement implementation behind a narrow interface.
- AETHER may publish semantic envelopes that FABRIC transports.
- FABRIC may expose operational telemetry that AETHER records as claims/facts subject to normal admission.

Forbidden:

- FABRIC deciding semantic validity.
- AETHER relying on FABRIC for local truth/replay correctness.
- FABRIC consulting AETHER to perform its core delivery semantics.
- GHOS treating either component as an admitted controller without separate governance.
- POL deriving authority from FABRIC liveness or resource state alone.

## Alternatives for Council consideration

### Alternative A — Keep AETHER and FABRIC unified

AETHER remains both semantic coordination kernel and distributed fabric.

Advantages:
- fewer repositories and interfaces;
- less protocol/versioning burden;
- direct optimization across semantics and transport.

Risks:
- semantic core and performance substrate face conflicting evolutionary pressures;
- distributed mechanics may leak into truth semantics;
- wider blast radius;
- AETHER becomes harder to reason about, qualify, or reuse conservatively.

### Alternative B — Independent encapsulation with asymmetric semantics (recommended)

AETHER and FABRIC become separately encapsulated; FABRIC is mechanically independent and semantically subordinate.

Advantages:
- clear semantic authority;
- failure containment;
- independent performance evolution;
- FABRIC becomes reusable beyond AETHER;
- AETHER can remain conservative and explainable;
- POLITY architecture becomes substantially clearer.

Risks:
- new interface/protocol;
- version compatibility burden;
- potential duplicate notions such as lease/identity/routing;
- temptation to recreate semantic authority inside FABRIC for convenience.

### Alternative C — FABRIC as authoritative tuple-space; AETHER becomes rule/explanation layer

Rejected by the proposer.

This would move shared-state authority downward into FABRIC and turn AETHER into a derived semantic service.

It would conflict with the direction of AETHER's current semantic kernel and create ambiguity over authoritative truth.

### Alternative D — FABRIC as an internal AETHER module only

Mechanically separates code but not lifecycle, qualification, or encapsulation.

This may be useful as an intermediate refactor but does not achieve the desired fault, evolution, and reuse boundaries.

## Recommended staged programme

### E0 — Boundary doctrine

No code movement.

Inventory AETHER responsibilities and classify each as:

- `SEMANTIC`;
- `INSTITUTIONAL`;
- `EXECUTION`;
- `FABRIC`;
- `AMBIGUOUS`.

Deliver a closed boundary matrix and ADR.

### E1 — Interface law

Specify the smallest mechanical interface needed by AETHER:

- envelopes;
- endpoint discovery;
- rendezvous;
- delivery;
- correlation;
- operational failure reporting;
- optional locality/resource hints.

Do not include semantic acceptance, authority, claim judgment, or policy interpretation.

### E2 — Local reference FABRIC

Implement a deliberately boring in-process reference adapter.

Acceptance requirement:

> AETHER semantic outputs are byte-/meaning-equivalent with the adapter enabled or absent for covered workloads.

### E3 — Extract proven mechanics

Move only responsibilities already classified and proven mechanical behind the interface.

No semantic change is permitted as part of extraction.

### E4 — Independent FABRIC runtime/repository

Only after the interface survives real workloads, establish independent encapsulation/release discipline for FABRIC.

### E5 — Distributed POLITY proof

Run one bounded polity across multiple endpoints.

Induce FABRIC loss/recovery/replacement and prove:

- availability can degrade;
- work can be retried/replaced;
- AETHER semantic truth is not corrupted;
- no delivery event creates authority;
- provenance remains reconstructible.

### E6 — AETHER-Learn integration

Separate:

- desired institutional allocation (AETHER/POL/AETHER-Learn);
- physical realization (FABRIC).

Evaluate routing regret, locality, cost, latency, and failure recovery without conflating them.

## Constitutional treatment

The proposer recommends that Council distinguish two questions:

1. **Architecture approval:** Is the separation doctrine technically/institutionally sound enough to guide implementation?
2. **Constitutional activation:** Does Article IX require amendment before any implementation changes production authority or representation?

The proposer expects the answer to (2) to be yes if constitutional wording or effective AETHER authority changes.

A Council architecture approval must therefore not be represented as constitutional activation.

If Council approves the doctrine, the next constitutional packet should include the Article XI requirements and a proposed Article IX amendment that preserves AETHER semantic authority while naming FABRIC as non-authoritative mechanical infrastructure.

## Candidate Article IX direction

This is discussion text, not an amendment:

> AETHER is the authoritative semantic coordination substrate for production deployments.
>
> AETHER owns append order, semantic cuts, replay, policy visibility, provenance-bearing facts, recursive derivation, proof traces, and semantic admission within its admitted domain.
>
> FABRIC may provide independently encapsulated transport, rendezvous, placement, streaming, replication, and other mechanical distribution services. FABRIC has no constitutional or semantic authority by virtue of delivery, liveness, replication, locality, or availability.
>
> INTELLECT owns constitutional policy, office obligations, work-package commands, artifact contracts, application projections, and gate reports.
>
> GHOS execution-controller admission and protected execution remain separately governed.

Exact wording is intentionally left to Council deliberation and any later amendment packet.

## Risks requiring explicit Council treatment

1. **Semantic leakage:** convenience logic migrates into FABRIC and becomes de facto authority.
2. **Split-brain vocabulary:** lease, identity, route, replica, and heartbeat acquire conflicting meanings.
3. **Dependency inversion:** AETHER becomes operationally dependent on FABRIC and loses local correctness.
4. **Control-plane confusion:** FABRIC is mistaken for a GHOS controller.
5. **Authority laundering:** resource availability or transport delivery is treated as permission.
6. **Protocol ossification:** the interface freezes before sufficient workloads test it.
7. **Premature repository split:** code is moved before the boundary is proven.
8. **Performance tax:** semantic envelopes impose avoidable transport overhead.
9. **Observability ambiguity:** operational telemetry is mistaken for semantic evidence.
10. **Migration drift:** old AETHER paths continue to carry hidden fabric responsibilities indefinitely.

## Acceptance tests for a future implementation

The separation is not considered proven merely because two repositories exist.

Required properties:

```text
AETHER without FABRIC
=> semantically correct, locally constrained

FABRIC without AETHER
=> mechanically useful, semantically agnostic

AETHER + FABRIC
=> distributed semantic coordination

FABRIC failure
!= semantic corruption

FABRIC delivery
!= semantic admission

FABRIC liveness
!= institutional authority
```

Additional fail-capable tests should include:

- dropped messages;
- duplicated messages;
- stale endpoints;
- reordered delivery;
- FABRIC restart;
- AETHER restart;
- network partition;
- malicious/invalid envelope;
- resource advertisement spoof;
- cross-version protocol mismatch;
- attempt to infer authority from delivery/liveness;
- attempt to bypass GHOS controller admission.

## Proposed Council questions

Each office should answer from its constitutional function:

- Are the primitive boundaries coherent?
- Are any dependencies hidden or circular?
- Can the claimed separation be tested and falsified?
- What failure modes could collapse semantic authority?
- Which contracts must become normative?
- Is the staged programme proportionate and maintainable?
- Are terms such as fabric, authority, route, lease, identity, and admission unambiguous?
- Does the architecture compose with POL, GHOS, AETHER-Learn, AETHER-MEM, and distributed truth?
- What records must be preserved for future inheritance?
- Should the proposal be approved, approved with conditions, returned for revision, or rejected?

## Requested disposition

The proposer requests one of:

- `approve`;
- `approve_with_conditions`;
- `changes_requested`;
- `reject`;
- `abstain`.

An approval is an architectural recommendation only.

Any constitutional amendment, change to AETHER authority, production activation, or new controller admission remains separately governed.

## Reversal condition

Reconsider the separation if empirical implementation shows that:

- the interface materially compromises semantic correctness;
- independently encapsulated FABRIC cannot remain useful without semantic coupling;
- coordination overhead materially exceeds the fault/evolution benefits;
- the boundary requires systematic duplication of semantic state;
- or evidence shows a unified design is demonstrably simpler without weakening authority, replay, provenance, or failure containment.

## Residual frontier

Even if the separation is approved, the following remain open research/engineering questions:

- exact FABRIC transport model;
- endpoint/resource identity model;
- placement and backpressure semantics;
- AETHER/FABRIC version-negotiation protocol;
- topology-aware AETHER-Learn integration;
- relationship to AETHER-MEM physical storage/retrieval;
- multi-host authority partitions and distributed truth;
- whether FABRIC eventually becomes a GCT-wide infrastructure product;
- performance envelopes at polity scale.
