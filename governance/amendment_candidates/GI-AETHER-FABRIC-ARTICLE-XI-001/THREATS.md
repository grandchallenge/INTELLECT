# Adversary threat analysis (candidate analysis, not an acceptance review)

| Attack | Required boundary | Disconfirming test / expected result |
| --- | --- | --- |
| Selective delivery and starvation influence judgment | Missing is unknown; envelope policy attributable and bounded | Hold semantic inputs fixed, selectively delay principals; no false evidence or authority is inferred; unfairness is observable |
| Priority/retry/locality policy laundering | Mechanical optimizer cannot invent utility or widen eligibility | Mutate priorities, endpoint eligibility and retries outside envelope; reject before semantic start |
| Authority-token interpretation | Resource identity never implies semantic actor, office or GHOS controller | Replay a resource lease/token as authority; no admission, execution or promotion |
| Delivery receipt presented as completion | Distinct event algebra and correlation | Deliver bytes without semantic acceptance; no accepted cut/receipt/trace fabricated |
| Timeout followed by hidden commit | AETHER retains start and cancellation lifecycle | Pre-start timeout never later commits; after start, timeout cannot silently recast semantic completion |
| Successful replication promotes stale follower | Epoch/prefix/fencing remain semantic | Fully copy bytes to stale/divergent replica; append remains rejected |
| Telemetry directly changes policy | Evidence requires ordinary submission/admission | Forge queue/latency reports; no policy or allocation mutation without governed decision |
| Protocol downgrade or identity collision | Exact compatible versions; distinct typed identities | Unknown version, mismatched identity stratum or revoked envelope fails closed |
| Sidecar availability becomes truth | Semantic identity/provenance/visibility stable under location changes | Cache/move/rank bytes; admitted results and policy unchanged |
| Audit backpressure erases accountability | Required audit evidence has declared failure semantics | Fill/drop sink; no unrecorded accountable success |

Residual risk: denial and biased observation remain possible without an authority violation. A successful schema check cannot prove fairness or containment. E2 must test these attacks against an executable realization; this document records required evidence, not passing results. A compromised mechanical service needs a tested local fallback preserving semantic state.
