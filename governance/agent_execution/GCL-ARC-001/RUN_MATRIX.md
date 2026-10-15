# GCL-ARC-001 acceptance and hostile-replay matrix

| Test | Expected result | Authority |
| --- | --- | --- |
| One real GitHub account, three unique read-only role passes | Structurally valid | GCL role-pass validator |
| Same reviewer system for several declared logical passes | Permitted but NOT a distinct external expert | GI-STEWARD-0003 |
| Duplicate logical pass ID | Reject | Validator |
| Verifier/Adversary/Referee attempts a candidate write | Reject and invalidate finding | Validator |
| Candidate head differs from reviewed head | Reject | Trusted source lock |
| Adversary has no adverse fixture | Reject | Validator |
| An executable check fails | Record blocker; cannot accept | Verifier |
| A discovered revision is silently discarded by Referee | Reject | Evidence gate |
| Reviewer claims mathematical certification | Reject | MATHCERT only |
| Mathematical claim with no independent method receipt | Reject | Domain validator |
| Domain review embeds its own future PR commit SHA | Reject self-reference | Provenance DAG |
| Later receipt contains fake/unapproved GitHub review ID | Reject upon actual GitHub API readback | Trusted controller |
| Agent review says accepted but protected status check fails | Reject admission | GitHub rules |
| Exact subject changes after review | Re-run affected passes | Candidate immutability |
| Same agent transport login claims to be different GitHub user | Reject attribution | GitHub auth |
| Protected source reviewer App issues verified mechanical approval | Accept only if role receipts and native rules pass | Release Trust |
| Reserved action without express Human decision | Reject | Constitution |
| Project mutation outside Council Clerk | Reject | Control plane |
| Three passes agree but all use unverified same calculation | Reject scientific certification | Independent method gate |
| Erdős 14 queue state readback after actual admission | 14 RETURNED, 5 REVISE, no AVAILABLE | Council Clerk |

All source review checks must execute on exact known material, and real
external events must be independently fetched by the protected controller.
The initial Python tests validate record invariants, NOT the existence of
the GitHub events or truth of an asserted scientific finding.

Bootstrap failure modes: reviewer identity unavailable, protected-source
recipient cannot mint an authorized App token, adapter provenance circle,
or policy gate only repairable by a separately protected transaction.
Each must produce a named durable BLOCKED receipt, not founder handoff.
