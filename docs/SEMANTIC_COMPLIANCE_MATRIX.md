# Semantic Compliance Matrix

| Constitutional claim | Executable locus | Verification | Status |
| --- | --- | --- | --- |
| Generation precedes Specification | phase order and engine restrictions | complete lifecycle test | Closed locally |
| Consequential work requires alternatives | Generation gate | lifecycle and negative tests | Closed locally |
| Measurement must permit disconfirmation | Confrontation gate | lifecycle test | Closed locally |
| Judgment records trade-offs and reversal conditions | Judgment command and gate | lifecycle test | Closed locally |
| Memory preserves reasons, scope, and limitations | Integration gate | lifecycle and metrics | Closed locally |
| Completion requires disposal and residual frontier | Disposal gate | lifecycle test | Closed locally |
| Reviews are obligations, not attendance | exact obligation IDs | ceremonial-review test | Closed locally |
| Later objection revokes prior approval | latest-review semantics | revocation test | Closed locally |
| One identity cannot occupy multiple offices | `AgentRegistry` | identity-separation test | Closed locally |
| Council dispatch cannot advance a phase | API separation | Council tests | Closed locally |
| Deletion requires authority | engine guard | deletion test | Closed locally |
| Completed work can reopen without rewriting history | `phase.reopened` | reopening test | Closed locally |
| Test fabric is not production authority | `authoritative = False` and constructor guard | engine and workspace tests | Closed locally |
| AETHER is production semantic authority | adapter and ADR-0001 | mocked wire tests | Boundary implemented; live closure open |
| AETHER replay uses bounded pagination | `PageInfo.next_offset` handling | pagination test | Closed against contract |
| AETHER facts carry provenance and policy | datom mapping | append-shape test | Closed against contract |
| AETHER derives gate readiness with proof traces | future semantic programme | live conformance matrix | Open |
| Executor claims are lease-fenced | future AETHER coordination integration | live run matrix | Open |
| Artifact evidence is digest-verified | future sidecar integration | live run matrix | Open |
| Distributed truth uses explicit partition cuts | future partition integration | federated matrix | Open |
