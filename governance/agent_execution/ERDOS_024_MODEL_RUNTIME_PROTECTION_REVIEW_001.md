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

## Bounded non-reserved INTELLECT control review (role-scoped logical passes)

1. **Authorization:** Is Copilot CLI model use with `GITHUB_TOKEN` and the organization’s Copilot policy actually permitted and billed appropriately, with model/version/CLI arguments tested against the exact effective runner? A GitHub checkout/CI success does not establish model entitlement. If not, record `MODEL_RUNTIME_UNAVAILABLE`.
2. **Permission isolation:** Are model tools truly restricted read-only? Are action environment scopes, immutable dependencies, third-party artifact inputs, stdout/stderr, and untrusted worker text robust against token disclosure/prompt injection and unexpected command/network access? Distinguish "model has no issue-write permission" from an actual airtight sandbox claim.
3. **Provenance:** Check author identity, exact run/attempt ID, signed/pinned source hashes, separate publisher credentials, token expiry, candidate rejection and replay idempotence, and absence of untrusted-model-sourced authority fields.
4. **Trigger economics:** A protected-main push is a trigger, not a one-time lifetime budget. Ensure an explicit per-campaign already-attempted receipt/lock or one-shot protected authorization so subsequent pushes cannot repeatedly bill/model-run after malformed or failed attempts; inspect the soft-credit-limit semantics and bounded total bill. Hostile cases include concurrent workflow runs, force-push events, cancelled jobs, retry, and partial artifact publication.
5. **Governance separation:** Verify queue-only maintenance is not subjected to blanket specialist signoff. Under effective GI-STEWARD-0003, one agent system may staff non-reserved author, verifier, adversary and referee roles using recorded logical passes sharing a GitHub identity. An authoring-system Adversary/Referee pass must be declared `non_authoring_read_only`; role evidence is not identical to GitHub PR review permission or mathematical certification. Any expressly reserved protection, credential expansion or permission change follows its specific authority gate.
6. **Canary admission:** For a non-reserved preparatory evidence runner, record applicable role-scoped INTELLECT logical-pass findings and admit a separate Programme activation PR through its actual protected rules. A special nonauthor GitHub review receipt is needed only if the specific admission route or platform protection requires it. Demand live Project #2 readback and one bounded Erdős #41 evidence-only run or explicit blocker. Preserve immutable Forge → Solve → Cert authority boundaries.


## Staffing clarification — logical independence is the default

Effective `grandchallenge/INTELLECT/governance/steward_directives/GI-STEWARD-0003.md` and the active constitutional authority schedule explicitly permit a **single Codex system, model instance, session, or GitHub identity** to staff multiple non-reserved GCL roles. A separate `logical_pass_id` is evidence of an independent **role question**, not a claim about physical isolation. For a system assessing its own proposed work, adversarial/referee audit is `non_authoring_read_only`, bound to the exact reviewed bytes; mutation ends the pass. Reviews report reproducible defects and uncertainty, not ceremonial consensus.

**Separation levels:**
- `OPERATIONAL_PREPARATORY`: source reconnaissance, exploratory formalization, bounded Solve work, computational tests, review candidates, and internal evidence comments. Shared GitHub authentication and role-scoped logical passes are allowed. GitHub issue-comment posting is not mathematical result publication.
- `PROTECTED_NON_RESERVED_CHANGE`: implementation and operational/security assessment, with explicit role-scoped passes and the actual native protected PR checks. A distinct identity is not needed *just because* the agent acted in different logical offices. Any domain-specific admission contract that expressly mandates a nonauthor GitHub review must still be satisfied if that contract is selected.
- `PROMOTED_CLAIM`: MATHFORGE authoritative source-semantic acceptance where its admitted contract requires domain review, MATHCERT formal certification, and external publication **as an established mathematical result**. Enforce each explicit substantive independence/evidence rule; no system certifies solely from its own construction/verification.
- `RESERVED_AUTHORITY`: credential escalation, security control weakening, constitutional authority and other expressly reserved changes cannot be self-authorized through role labels; apply their particular gates.

**Execution host is not identity authority:** The existing GSD/QTR Colab runner can run role-scoped mathematical audits and return SHA-256-locked evidence using the already authorized GitHub operator. Colab compute isolation does not confer a formally independent mathematical certifier or a distinct authenticated PR approver. Its OAuth, source-lock, billing and model adapter must be assessed within the same bounded operational review, not assumed.

The independent GitHub-App proposal in the original review intake is therefore **not a prerequisite for ordinary Erdős #41 preparatory review execution**. It may be a separate implementation choice only for admission paths where a genuine nonauthor approval is explicitly required. No protection bypass is implied by this correction.

## Exit criteria and negative controls

**This packet is NOT a positive security review.** No approval, protected receipt or authority may be inferred from the issue, packet, CI pass or a model's unsupported assertion. For the non-reserved execution-only subject, positive control assessment can use GI-STEWARD-0003 logical passes (role, system ID, logical-pass ID, exact subject, mode, evidence, finding and open obligations), followed by actual protected Programme admission. Do not demand separate GitHub credentials merely to demonstrate logical-role independence. If an existing material-protection specialist receipt is *specifically invoked*, its current adapter requires exact source fingerprint and a genuine authenticated nonauthor GitHub PR APPROVED review; do not forge that receipt or relax that narrower contract. A reserved credential/permission change and any formal mathematical certification or established-result publication retain their express stricter gates. Missing exact evidence, live entitlement, spending controls, isolation or scope => retain the hold and report the blocker.

The permitted sequence is **hold AI → separately admit routine Project repair → INTELLECT role-scoped control review under GI-STEWARD-0003 → separate protected activation (native required checks unchanged) → one real canary → evidence-only Forge handoff**. Source-specific or reserved authority changes still use their explicit independent specialist gates. No new routine Human Steward-in-the-middle ceremony or artificial GitHub identity multiplication is introduced.
