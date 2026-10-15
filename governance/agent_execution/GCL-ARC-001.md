# GCL-ARC-001 — Agentic Role Separation and Evidence Admission

**Version:** 0.1.0 candidate. **Status:** PROPOSED_NOT_EFFECTIVE.
**Authority:** Subordinate implementation of already effective GI-STEWARD-0003,
Article XI, GCL-AGENT-STAFFING-001 and GCL-AGENT-CONTINUITY-001.
It does not amend the constitution or grant new rights.

## 1. Founding principle

One institutional GitHub account may transport evidence for many agent roles.
A GitHub login authenticates an action. It is NOT a research credential,
specialist office, independent source of reasoning, or expert verdict.

Agents perform research, implementation, verification, adversarial review,
refereeing and bounded execution. Founder-Operator retains accountability for
legal, financial, strategic, public and other expressly reserved decisions.
GCL technical truth comes from exact-head evidence, independent methods,
reproducible checks, durable error records and protected readback, not the
Founder personally approving technical changes.

GI-STEWARD-0003 already permits one agent system to staff several non-reserved
roles through distinct logical passes. No separate login, human, model instance,
or session is inherently required for each specialist role.

## 2. Three kinds of identity, deliberately separated

- **Transport principal:** actual authenticated GitHub writer, possibly the
  same for all agent roles. Never invent different GitHub users or reviews.
- **Specialist logical pass:** separately identified system, role, pass ID,
  immutable subject H, input evidence, methods, checks, falsifiers,
  limitations, disposition and permitted side effects. Same system and
  GitHub login are allowed; a role label alone is not independent evidence.
- **Protected execution principal:** existing narrowly scoped Council Clerk
  and Release Trust service Apps. They mechanically verify gates and perform
  authorized writes. They are NOT substitute experts or MATHCERT.

No shared passwords, additional agent passwords, fake actor identities,
or personal GitHub accounts for specialist staffing.

## 3. Agent review transaction

Candidate writes an ordinary branch and freezes exact HEAD H and its material
manifest, scope, work class, security effects and claim limits.

Verifier performs a non-authoring, read-only logical pass at H; records
reproducible test inputs, commands, results, evidence hashes and gaps.

Adversary performs a different non-authoring, read-only pass at the same H;
tests negative cases, privilege boundaries, forged receipts, races and partial
replay. Records real falsifiers and outstanding objections.

Referee checks both passes and source ground truth; records ACCEPT_BOUNDED,
REVISE or BLOCKED, with evidence and explicit unresolved obligations.
A source modification invalidates any affected earlier read-only finding.

Protected admission controller checks the policy selected on trusted main,
head/digest bindings, role/mode separation, independent evidence requirements,
tests, native GitHub rules and reserved boundaries BEFORE writing. Existing
service Apps can provide mechanical non-author PR acknowledgement if an
admitted contract permits it. No automatic expert opinion or math certification
is inferred from an App's GitHub username.

After protected admission, Controller reads back live state. Amanuensis
preserves a durable receipt, including unresolved REVISE cases.

## 4. Work classes

| Class | Agent obligation | Human involvement |
| --- | --- | --- |
| ROUTINE_BOUNDED | Bounded build, read-only audit, affected CI, protected readback | None by default |
| MATERIAL_CONTROL | Read-only Verifier, Adversary and Referee passes, threat-model tests and protected security gates | Only expressly reserved decisions |
| MATHEMATICAL_CLAIM | A genuinely distinct verification METHOD, e.g. Lean kernel or independently reproduced calculation, followed by applicable MATHCERT gate | Only if reserved |
| RESERVED | Agents prepare exact evidence and decision packet | Reserved authority actually decides |

One model saying yes twice is not an independent mathematical verification
method. Epistemic independence is earned by evidence and reproducibility, not
account multiplication. No GCL role pass can self-certify a research claim.
Credential escalation, irreversible commitment, safety-critical deployment,
destructive work or public claim promotion retains its existing domain gate.

## 5. Machine-checkable review evidence

The proposed GCL_AGENT_ROLE_PASS_V1 receipt records:
- Exact subject repository, candidate H and canonical material SHA256;
- Actual transport login, reviewer_system_id, logical_pass_id, role and mode;
- Read-set and write-set (the latter empty for verifier/adversary/referee);
- Checks executed and negative controls with inspectable result digests;
- Claims checked, unresolved objections and bounded disposition;
- No-math-certification/no-source-promotion effects unless independently
  authorized by the proper domain.

Distinct logical passes are required and must disclose use of the same
system and shared login. A real fresh-context review can help, but no prompt
phrase is proof of methodological independence. Fail closed on missing
counterexamples, cloned evidence or source H mutation.

## 6. Acyclic protected review evidence

**Never demand an artifact embed the Git SHA of the commit containing itself.**
The current MATH-PROGRAMME specialist receipt adapter requires
review_anchor.source_pr_head_sha in the original review artifact while also
requiring that same file blob be introduced at that reviewed PR head. That
creates a circular normal-Git dependency, confirmed from the protected code.

Replace through separately governed migration:

1. Freeze candidate H.
2. Write domain review dossier D referencing H and known source proofs only.
3. Submit D for an actual domain PR review at subsequently known head R.
   Validate substantive read-only logical passes and exact approved checks.
4. After genuine domain PR approval and protected merge M, separately issue a
   protected source receipt A, which can now bind R, GitHub review_id, D blob
   and M without self-reference.
5. Relying controller verifies protected D and A, candidate H/digest, real
   review provenance, source integrity and domain limits before any admission.

Directed acyclic dependency: H -> D -> reviewed R / merge M -> receipt A ->
consumer. The service App is an authenticated mechanical admission actor,
not a second specialist login. Its approval is valid only where existing
branch and review rules explicitly permit it.

## 7. Bootstrap and non-bypass migration

Admit this subordinate standard through INTELLECT's existing protected checks.
Introduce a two-phase review-evidence producer and hostile validator tests for
stale heads, changed blobs, forged GitHub actor, duplicate logical passes,
write attempts in review mode, invalid source authority, missing negative
tests, incomplete replay, and cyclical source-review references.

Migrate the MATH-PROGRAMME consumer to recognize role-scoped evidence,
methodological validation and trusted non-author *mechanical* attestation,
rather than requiring a distinct GitHub account for every technical role.
This is a source-control/security-sensitive contract change and needs its own
protected admission. An agent may NOT silently weaken the existing gate.
If old controls cannot admit their own repair, use a separately authorized
documented protected migration or recovery transaction with exact evidence.

After admission, replay originally blocked PRs. For Erdős PR #2624, complete
the control review, merge through protected checks, have Council Clerk update
the 14 review items, and independently read back all queue states. Preserve
five REVISE source-correction cases as open, not falsely math-certified.

## 8. Mandatory failure conditions

Reject fabricated GitHub actor/review ID, unverified proof, duplicate passes,
mutable reviewer source, mismatched material H, missing required independent
verification *method*, adversarial findings suppressed by authors, unsupported
privilege changes, protection bypass, self-referential SHA, unapproved reserved
act, or claims based only on agreement between LLM passes.

Preserve protected trust, actual scientific rigor, and the Founder's narrow
reserved authority without making the Founder a routine reviewer.
