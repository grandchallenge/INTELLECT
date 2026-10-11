# GCL-ERDOS-024-MODEL-RUNTIME-INTELLECT-REVIEW-001
**Status:** REVIEW_PACKET / UNADJUDICATED  
**Authority:** INTELLECT, non-reserved protection/security review only  
**Issue:** https://github.com/grandchallenge/INTELLECT/issues/118  
**GCL lane:** protected implementation review of model execution, not mathematical source/proof certification

## Exact protected incident

- Grand Challenge MATH-PROGRAMME [PR #2540](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2540), candidate head `2489bf978dc8ab6efe3f911bb751fdd3d195e9bb`, protected merge commit `a403417178e49ec6c4446650e1ff9e5105387c31`, 2026-10-11.
- Original material-profile delegated review on that candidate failed with `candidate specialist class unresolved or mixed`, GitHub [Actions job 114369054619](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38105176728/job/114369054619). Green engineering CI and subsequent merge DO NOT transmute that negative verdict into a protection-specialist approval.
- Production queue [Actions run 38105865064](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/38105865064) failed: `Project Todo option conflicts with protected binding`. The AI reviewer and separate evidence publisher were **skipped**, so there is no observed model execution, independent specialist review, or posted mathematical evidence.
- Source target: Erdős #41 critic issue https://github.com/grandchallenge/MATH-PROGRAMME/issues/2536, original bound source return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1310#issuecomment-6104193801.
- Protective hold: Programme [PR #2541](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2541), setting both AI model and publisher `if` gates false pending this review. Routine Project queue-only repair is separate [PR #2542](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2542), which must not activate the AI reviewer.

## Original runtime mechanism (subject of review)

The currently merged code introduces `ci/erdos_forge_copilot_pilot.py` and two jobs in the existing `erdos-catalogue-queue-projection.yml`:

- `forge-pilot-review`: source packet built from 24-item protected roster and exact Formal Conjectures Git blob, original RESULT/1 comment hash, and a fixed deterministic counterexample to a FINSET/multiset predicate equivalence. Invokes Copilot CLI 1.0.66 with `gpt-5.4`, 420-second timeout, advertised 30-credit soft limit, no built-in MCP, read-only tools, no shell/write/URL, job permissions `contents: read`, `issues: read`, `copilot-requests: write`.
- `forge-pilot-evidence`: separate job with no Copilot grant; downloads run artifact, checks exact source-comment digest and response JSON schema, and can write only an `GCL-FORGE-CRITIQUE-CANDIDATE/1` comment with *no authority effects*.
- No protected Solve dispatch, protected source status promotion, Lean proof certification, MATHCERT result, reserved INTELLECT authority, or generic independent specialist accreditation may result from this proposal.

## Questions to be discharged by an actual nonauthor INTELLECT specialist

1. **Authorization:** Is Copilot CLI model use with `GITHUB_TOKEN` and the organization’s Copilot policy actually permitted and billed appropriately, with model/version/CLI arguments tested against the exact effective runner? A GitHub checkout/CI success does not establish model entitlement. If not, record `MODEL_RUNTIME_UNAVAILABLE`.
2. **Permission isolation:** Are model tools truly restricted read-only? Are action environment scopes, immutable dependencies, third-party artifact inputs, stdout/stderr, and untrusted worker text robust against token disclosure/prompt injection and unexpected command/network access? Distinguish "model has no issue-write permission" from an actual airtight sandbox claim.
3. **Provenance:** Check author identity, exact run/attempt ID, signed/pinned source hashes, separate publisher credentials, token expiry, candidate rejection and replay idempotence, and absence of untrusted-model-sourced authority fields.
4. **Trigger economics:** A protected-main push is a trigger, not a one-time lifetime budget. Ensure an explicit per-campaign already-attempted receipt/lock or one-shot protected authorization so subsequent pushes cannot repeatedly bill/model-run after malformed or failed attempts; inspect the soft-credit-limit semantics and bounded total bill. Hostile cases include concurrent workflow runs, force-push events, cancelled jobs, retry, and partial artifact publication.
5. **Governance separation:** Verify queue-only maintenance is not subjected to blanket specialist signoff; the proposed AI runner is an INTELLECT security/control-plane authorization and Forge-side evidence generator only. Review can't self-certify itself through the same PR/author runtime.
6. **Canary admission:** After a protected INTELLECT nonauthor security evidence receipt, admit a separate Programme PR reactivating only the named AI pilot jobs. Demand a successful live Project #2 readback and then a real isolated Erdős #41 run with evidence or explicit external blocker. Preserve immutable Forge → Solve → Cert authority boundaries.

## Exit criteria and negative controls

**This packet is NOT a positive security review.** No approval, protected receipt, or security authority may be inferred from the issue, the packet, a CI pass, the model's own opinion, or its original author's review. A positive disposition requires a separately protected INTELLECT source review record, a genuinely nonauthor qualified reviewer on the exact head, and the existing Programme specialist receipt adapter's actual fingerprint/provenance checks. Missing sources, mixed security scope, reviewer conflict, unknown effects, or provider access failure => retain hold and report the exact blocker.

The permitted sequence is **hold AI → separately admit routine Project repair → INTELLECT nonauthor review of AI runner → separate protected activation → one real canary → evidence-only Forge handoff**. No new routine Human Steward-in-the-middle ceremony is introduced.
