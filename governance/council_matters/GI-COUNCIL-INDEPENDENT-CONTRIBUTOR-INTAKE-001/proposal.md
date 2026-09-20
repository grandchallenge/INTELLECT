# GI-COUNCIL-INDEPENDENT-CONTRIBUTOR-INTAKE-001: independent contribution intake and concurrency integrity

**Status:** Before the Council for full-quorum review

**Decision class:** research-contribution intake, concurrency control, provenance, and epistemic-integrity policy

**Authority boundary:** Council recommendation only. Current constitutional, Human Steward, MATH-PROGRAMME, MATHSOLVE, MATHCERT, MATH-CORE, protected-branch, certification, publication, and external-claim authority remains unchanged.

## 1. Question presented

Should GCL adopt a common intake contract for independent, zero-context, or externally operated research contributors so that their value as epistemically separate contributors is preserved while their results become durable, replayable, concurrency-safe evidence?

The proposed rule is:

> An independent contributor produces evidence. Intake preserves that evidence. GCL adjudication determines whether anything enters protected knowledge.

The contributor is not an implicit GCL Executor, Referee, certifier, integrator, or canonical-state writer merely because GCL dispatched the question.

## 2. Trigger and observed defect

A recent zero-context NS-CI handoff correctly supplied a sealed mathematical problem, explicit time-boxed assignments, rejection tests, and a structured return format. It did not initially require a durable contribution artifact.

That gap exposed a broader design defect.

A chat-only return can be lost, truncated, summarized, or silently reinterpreted. Conversely, requiring every independent contributor to learn GCL governance and mutate a canonical repository would collapse the epistemic separation that motivated independent contribution in the first place, create a permissions dependency, and couple mathematical evidence production to internal execution machinery.

Existing executor contracts already identify adjacent requirements:

- MATHSOLVE continuity requires narrow durable tranches, checkpointing before branch expansion, live exact-head rebinding, post-mutation readback, and stale conversational-state rejection.
- RH parallel-route execution requires bounded subproblem allocation, prohibits accidental duplicate work except intentional independent adversarial replay, protects reusable results before downstream consumption, rejects stale-branch CI as integration evidence, and requires exact protected identities.
- MATH-CORE architecture requires exact-checkpoint concurrency control, stale-response rejection, deterministic admission/rejection receipts, explicit supersession and downstream invalidation semantics, bounded resource budgets, and no producer self-authorization.
- MATH-PROGRAMME architectural integrity warns against duplicate governance planes and silent authority transfer between coordination, evidence, assurance, certification, and canonical recording.

The independent-contributor interface should inherit those integrity lessons without forcing external contributors to become internal execution agents.

## 3. Design objective

Create a transport-independent contribution protocol that:

1. accepts useful work from humans, external models, theorem systems, contractors, collaborators, or agents with no GCL repository permissions;
2. preserves the exact returned contribution before synthesis or adjudication;
3. makes the source handoff, assignment, declared context, dependencies, assumptions, and claim boundary explicit;
4. supports intentional parallel independent work without accidental overwrite or duplicate canonical mutation;
5. rejects stale rebinding, hidden context substitution, silent result merging, and authority inflation;
6. separates raw contribution, intake receipt, adjudication, and protected incorporation;
7. remains compatible with GCL-AGENT-CONTINUITY-001 without making that internal execution policy a prerequisite for an external contributor;
8. does not create a second Claim Ledger, certification system, or mathematical authority plane.

## 4. Proposed independent-contribution model

### 4.1 Sealed dispatch

Every independent contribution begins from one exact dispatch object or handoff pointer.

The dispatch must identify:

- programme/campaign or research context;
- source repository, path, and exact commit SHA where applicable;
- source handoff digest when practical;
- bounded assignment identifier;
- declared concurrency mode;
- wall-clock or other resource limit if one is imposed;
- allowed evidence surface;
- required output schema;
- prohibited claims or authority transitions.

A snapshot SHA is an issuance identity, not permission to mutate a stale base.

For a true zero-context assignment, the handoff itself must contain all mathematical hydration necessary for the requested work. The contributor should not be required to browse GCL history merely to discover assumptions that should have been part of the sealed problem.

### 4.2 Contributor role

The contributor has proposal/evidence authority only.

Unless separately authorized under an existing internal execution contract, the contributor must not:

- mutate canonical campaign state;
- edit canonical handoffs or claim ledgers;
- merge protected branches;
- mark a theorem certified or admitted;
- issue Human Steward, Council, Referee, or MATHCERT dispositions;
- rewrite earlier contributions;
- silently consume another contributor's result when the dispatch class requires blind independence.

The contributor's argument is its authority.

### 4.3 Independent Contribution Record

Each return should be one complete, portable Independent Contribution Record (ICR), suitable for byte-preserving durable intake.

Minimum semantic fields:

- contribution_id — contributor- or dispatcher-generated unique identifier;
- source_dispatch — exact handoff pointer and, where available, content digest;
- assignment_id;
- concurrency_mode;
- contributor_declared_identity;
- context_declaration;
- external_sources_or_tools;
- timebox_or_resource_declaration;
- disposition;
- strongest_exact_statement;
- derivation_or_evidence;
- assumptions_used;
- verification_or_falsification_hooks;
- claim_boundary;
- next_residual;
- attachment manifest, if any.

The precise serialization may be Markdown plus machine-readable metadata or a versioned JSON schema. The semantic contract is more important than forcing one transport.

### 4.4 Context declaration

A zero-context contributor should state, in substance:

> Context used: supplied handoff only, plus standard mathematical facts. External sources: none. Prior campaign knowledge used: none.

If that statement is false, the contributor must disclose the additional context or sources used.

This declaration is evidence about epistemic conditions. It is not cryptographic proof of independence.

The intake system must not infer independence merely because contributor IDs, model sessions, filenames, or reviewer strings differ.

### 4.5 Verification hooks

A contribution must expose at least one route by which another mathematician or system can challenge it.

Examples include:

- a specific identity to differentiate;
- an explicit counterexample family and limiting regime;
- constants in a quantitative lemma;
- a finite fixture;
- a proof-assistant target;
- a source theorem and exact hypotheses;
- a computational script and input manifest;
- a clearly named assumption whose removal should break the conclusion.

This requirement is intended to make outside contributions inspectable rather than rhetorically persuasive.

## 5. Durable return and transport independence

Durability is mandatory. Repository access is not.

Three intake modes are proposed.

### Mode A — authorized contribution-inbox write

If the contributor has an explicitly authorized proposal-only write surface, it may persist the exact ICR into a designated contribution inbox.

The inbox is append-only from the contributor's perspective and is not canonical mathematical state.

### Mode B — no repository write capability

If the contributor cannot write to GCL repositories, it returns the complete ICR verbatim through the available transport.

The receiving GCL intake process must persist that payload without semantic editing before synthesis, summarization, or adjudication.

### Mode C — file or external artifact return

A human or external system may return a standalone file or artifact bundle.

Intake records the original bytes, content digest, transport metadata where available, and attachment digests.

No mode is mathematically privileged merely because it used GitHub directly.

## 6. Intake receipt and immutable raw evidence

The receiving system creates a separate Intake Receipt.

The raw ICR and its attachments must remain immutable evidence after intake. Corrections are new contributions or explicitly linked superseding records, not silent edits.

The Intake Receipt should record at minimum:

- receipt ID;
- raw contribution content digest;
- attachment digests;
- source dispatch identity;
- assignment ID;
- concurrency mode;
- contributor-declared identity and context class;
- receipt time;
- syntax/schema validation result;
- duplicate/conflict classification;
- live-state freshness classification;
- quarantine/security classification for executable attachments;
- adjudication status;
- later incorporation pointers, if any.

The receipt must distinguish metadata observed by GCL from claims merely declared by the contributor.

## 7. Concurrency modes

The protocol must distinguish at least three modes.

### 7.1 cooperative_claimed

Use when agents are collaborating on a shared frontier.

A dispatcher or tracker claims a bounded subproblem before work begins. Accidental duplicate active work should be rejected or rerouted.

This is consistent with the RH executor rule.

### 7.2 independent_blind

Use when epistemic separation is itself the purpose.

Multiple contributors may receive the same sealed assignment. Earlier contributions must not be disclosed to later contributors until the declared blind cohort closes, except where safety or authority requires interruption.

Duplicate mathematical work is intentional in this mode.

The dispatcher records distinct dispatch IDs. Intake preserves every raw return separately.

### 7.3 adversarial_replay

Use when an existing result is intentionally challenged.

The prior claim may be disclosed, but the contributor must be told which evidence it may rely on and what it is expected to falsify or independently reproduce.

A replay is not independent merely because it was performed in another session.

## 8. Concurrency integrity requirements

### 8.1 No overwrite

Two returns for the same assignment may never overwrite one another.

Each receives its own immutable raw record and receipt.

### 8.2 No premature synthesis

When parallel independence matters, no synthesis document may replace the raw contributions before all declared cohort returns are durably preserved or the cohort is explicitly closed with missing-return evidence.

### 8.3 Deterministic duplicate classification

Intake should distinguish:

- byte-identical duplicate return;
- semantically repeated but independently produced contribution;
- superseding correction by the same contributor;
- conflicting contribution;
- malformed or incomplete return;
- intentionally repeated adversarial replay.

Byte identity does not prove common provenance, and semantic similarity does not prove copying.

### 8.4 Exact source binding

A contribution is evidence about the exact sealed handoff it received.

If the live campaign advances, the contribution remains valid historical evidence relative to that handoff but must not be silently rebound to the new state.

Intake should record at least:

- current_for_dispatch;
- stale_relative_to_live_state;
- dependency_changed;
- cannot_determine.

A stale contribution may still contain a timeless lemma or counterexample. Freshness classification controls incorporation, not whether the evidence is preserved.

### 8.5 Protected dependency consumption

A contribution must not become a dependency of another protected route merely because it exists in the inbox.

Before protected consumption, GCL adjudication must identify the exact contribution digest, verify the relevant mathematics or evidence to the required level, and record the resulting accepted dependency through the existing protected route.

This preserves the executor rule that reusable dependencies are protected before downstream consumption.

### 8.6 Supersession and invalidation

Corrections or new campaign state must not destroy prior evidence.

Receipts should support explicit relations such as:

- supersedes;
- contradicts;
- duplicates;
- derived_from;
- invalidated_for_live_incorporation_by;
- incorporated_as.

These relations are provenance edges, not automatic claim-status transitions.

## 9. Integrity and security controls

### 9.1 Returned contributions are untrusted payloads

A returned mathematical packet may contain prose, code, commands, URLs, or embedded instructions.

Intake treats it as data.

No returned code or instruction is executed automatically merely because the contribution arrived from an invited agent.

Executable attachments require separate sandboxed evaluation under existing execution controls.

### 9.2 Identity claims

A declared contributor identity is not authentication.

Where actual identity, contractual attribution, publication credit, legal provenance, or access authority matters, the relevant authenticated system must provide that evidence separately.

### 9.3 External sources and provenance

A contribution must identify external sources materially used.

Intake must not silently convert reconstruction, paraphrase, numerical evidence, or third-party claims into independent verification.

### 9.4 Sensitive information

Contribution channels must reject or quarantine credentials, secrets, private keys, personal data not required by the task, or other material inappropriate for durable research records.

### 9.5 Attachments

Every retained attachment should be content-addressed.

Large or executable artifacts may be stored outside the narrative record, but the ICR and receipt must bind their exact identity.

## 10. Adjudication boundary

The raw contribution record answers:

> What did the contributor return under the sealed assignment?

The adjudication record answers:

> What does GCL conclude after checking it?

These must not be the same artifact.

Adjudication may classify a contribution as, for example:

- received_unadjudicated;
- reproduced;
- conditionally_useful;
- contradicted;
- subsumed;
- candidate_for_protected_admission;
- rejected_for_incorporation.

These statuses describe GCL's treatment of the contribution. They do not rewrite the contributor's own disposition.

Only existing MATHSOLVE/MATHCERT/governance routes may create protected theorem, certificate, or canonical-claim effects.

## 11. Relationship to GCL-AGENT-CONTINUITY-001

GCL-AGENT-CONTINUITY-001 remains the internal execution policy for GCL agents performing authorized multi-step operations.

This proposal adds a boundary adapter for independent contributors.

It does not require an external contributor to adopt GCL repository mutation, recovery, or branch procedures merely to contribute evidence.

The receiving GCL intake process is itself subject to internal continuity requirements:

- persist useful returned work before expensive synthesis;
- bind exact source and contribution identities;
- recover from connector or context failure from durable intake state;
- reject stale conversational reconstruction when it conflicts with the preserved contribution;
- report the exact durable receipt and next obligation.

## 12. Relationship to MATH-CORE and duplicate-plane avoidance

The contribution inbox is an evidence intake surface, not a new Claim Blackboard or Claim Ledger.

If or when MATH-CORE has an admitted representation for external proposals, the intake receipt should map to that representation rather than create a competing reasoning-state ontology.

Until then, repository-local contribution records may exist as bounded evidence artifacts, but they must not claim canonical reasoning-state authority.

## 13. Executor-derived requirements incorporated

The proposal incorporates the following operating feedback already present in executor contracts and campaign practice.

### Concurrency

- claim bounded cooperative work before branch execution;
- do not duplicate active cooperative work unless independent replay is intentional;
- preserve blind cohorts without cross-contamination;
- use exact dispatch IDs so simultaneous returns cannot collide;
- make same-assignment multiple returns append-only;
- reconcile live-state movement before incorporation rather than discarding or silently rebinding contributions.

### Integrity

- exact-head or exact-handoff binding;
- stale evidence rejection for current integration;
- durable checkpoint before downstream dependency consumption;
- fresh review after mutation;
- protected readback after integration;
- content-addressed evidence and deterministic receipts;
- explicit supersession/invalidation;
- no producer self-authorization;
- preserve the distinction between proposal evidence, assurance, certification, and canonical state.

### Operational resilience

- timeout or transport failure is not a mathematical disposition;
- a returned contribution should be made durable before launching another expensive synthesis branch;
- failed or partial returns remain evidence with an explicit incomplete status rather than disappearing;
- intake must support contributors with no GitHub credentials;
- recovery must not require the contributor to reconstruct prior work from chat memory if a durable return exists.

## 14. Additional defects and requirements identified

### 14.1 Independence contamination

If one contributor sees another contribution before finishing an independent_blind assignment, the resulting work may still be useful but must not retain the same independence classification.

### 14.2 Sybil independence

Ten sessions of the same model or one operator are not automatically ten independent sources. The system must record available provenance and avoid numerical independence counts unsupported by authenticated evidence.

### 14.3 Incentive distortion

A return schema that rewards only PROVED results biases contributors toward optimistic arguments. REFUTED, REDUCED, and BLOCKED must remain first-class outcomes when accompanied by exact evidence.

### 14.4 Time-box integrity

A short wall-clock assignment is a search-budget constraint, not a proof-quality discount. Contributors must stop at the time bound and return the strongest exact result achieved, including a precise blocker where appropriate.

### 14.5 Assimilation risk

Requiring zero-context contributors to read internal governance, issue history, or prior proposed solutions can destroy the very independence being purchased. Governance should be enforced by the dispatcher and intake boundary, not transferred wholesale into the contributor prompt.

### 14.6 Authorship and rights

Mathematical usefulness does not establish publication authorship, ownership, licensing rights, confidentiality status, or priority. Those questions remain separate and require their own provenance and legal/policy treatment where material.

### 14.7 Prompt/instruction injection

Contributor artifacts may contain text that resembles operational instructions. Intake and adjudication systems must treat those instructions as quoted payload unless a separate authorized control path adopts them.

## 15. Proposed pilot

If adopted, run a bounded pilot before generalization.

Recommended first pilot:

- campaign: NS-CI;
- source: the protected C2-MIX-DIRECTION-COMPRESSION-LEDGER-CHARGE zero-context handoff;
- cohort: at least two deliberately independent blind contributions on Assignment A and/or B, plus one cooperative or adversarial contribution for comparison;
- contributor mutation authority: none required;
- intake: append-only raw ICRs plus separate receipts;
- adjudication: separate GCL-aligned synthesis after blind cohort closure;
- protected incorporation: absent unless a subsequent ordinary MATHSOLVE route verifies and admits a result.

Pilot acceptance criteria:

1. 100% of returned packets preserved byte-for-byte or as exact uploaded artifacts before synthesis;
2. 100% of receipts bind exact source dispatch and content digest;
3. zero contribution overwrites;
4. zero contributor-originated canonical mutations;
5. deterministic duplicate/conflict/stale classifications;
6. no blind-cohort cross-disclosure before closure;
7. external-source/context declarations preserved;
8. executable attachments not auto-executed;
9. adjudication artifacts separate from raw contributions;
10. no certification, canonical-claim, Human Steward, Council, or publication authority inferred from intake;
11. successful recovery from at least one simulated truncated/duplicate/stale return fixture;
12. executor feedback collected on coordination overhead, ambiguity, result usefulness, and concurrency failure modes.

## 16. Requested Council disposition

The Council is asked to determine whether GCL should:

1. adopt the conceptual separation of independent contributor, intake, adjudication, and protected incorporation;
2. require durable return while keeping repository write access optional;
3. require exact dispatch/source binding and a context declaration for zero-context work;
4. adopt explicit concurrency modes rather than one generic parallel-agent category;
5. require immutable raw contribution preservation and separate intake receipts;
6. fail closed on silent stale rebinding, overwrite, blind-cohort contamination, duplicate identity assumptions, or authority inflation;
7. run the bounded NS-CI pilot above before creating an organization-wide mandatory schema;
8. direct any later schema/tooling work to reuse MATH-CORE and agent-continuity concepts instead of creating a duplicate governance plane.

The preferred initial disposition is approve with conditions for bounded pilot, not immediate organization-wide activation.

## 17. Questions for differentiated Council review

The full Council should specifically address:

- Axiomatist: Are contributor, contribution, intake, adjudication, incorporation, and independence classes defined sharply enough?
- Cartographer: Does the protocol fit INTELLECT, MATH-CORE, MATHFORGE/MATHSOLVE/MATHCERT, GitHub, and external transports without creating a new authority plane?
- Verifier: Are the receipt, digest, stale-state, duplicate, cohort, and recovery properties mechanically testable?
- Adversary: Can a malicious, duplicated, contaminated, or stale contributor exploit the protocol to gain apparent authority or erase conflicting evidence?
- Formalist: What minimum machine schema/state machine is necessary for deterministic validation without over-formalizing mathematical prose?
- Steward: Does the pilot preserve current authority and avoid manufacturing Human Steward or Council actions?
- Grammarian: Are terms such as independent, blind, verified, accepted, incorporated, and durable semantically controlled?
- Composer: Does the lifecycle remain coherent under concurrency, correction, supersession, adjudication, and later MATH-CORE integration?
- Amanuensis: Is raw evidence preserved in a way that future agents can recover without relying on chat history?
- Referee: What exact pilot conditions reconcile the offices, and what evidence must return before broader institutionalization?

## 18. Evidence considered

- grandchallenge/INTELLECT@7e6b61ddf77e2d73309657d089a98cae84cc735f:docs/COUNCIL_MATTERS.md;
- grandchallenge/INTELLECT@7e6b61ddf77e2d73309657d089a98cae84cc735f:governance/agent_execution/GCL-AGENT-CONTINUITY-001.md;
- grandchallenge/MATH-PROGRAMME@f1a57fc81bfa0389b070e7c896fa76baa83720c1:records/MATH_CORE_01_GCL_MATHEMATICS_ARCHITECTURE_MEMORIAL.md;
- grandchallenge/MATH-PROGRAMME@f1a57fc81bfa0389b070e7c896fa76baa83720c1:handoffs/GCL-TCS-PILOT-INSTITUTIONALIZATION-001/MATH_CORE_INTEGRITY.md;
- grandchallenge/MATHSOLVE@04a2d15d49c78027d75d76c22c67be3f4a12c73b:AGENTS.md;
- grandchallenge/MATHSOLVE@04a2d15d49c78027d75d76c22c67be3f4a12c73b:handoffs/RH-001/routes/README.md;
- grandchallenge/MATHSOLVE@04a2d15d49c78027d75d76c22c67be3f4a12c73b:handoffs/NS-CI-001/C2_MIX_DIRECTION_COMPRESSION_LEDGER_CHARGE_ZERO_CONTEXT.md.

## 19. Claim boundary

This proposal does not:

- certify any mathematical contribution;
- prove that a contributor is independent;
- grant external agents write, merge, review, or protected-state authority;
- create a new Claim Ledger or MATH-CORE substitute;
- activate persistent coordination;
- alter MATHCERT authority;
- authorize external publication, novelty, priority, authorship, licensing, patent, product, deployment, or commercial claims;
- change constitutional or Human Steward authority by itself.

Until a later exact governed disposition says otherwise, current rules remain effective.
