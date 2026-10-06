# GI-COUNCIL-RSI-CCC-001 — Guarded reflective Cartesian-closure RSI intake

**Status:** Before the full Council  
**Decision class:** research-programme intake  
**Requested disposition:** approve intake of `RSI-CCC-WP00` for formal investigation  
**Effect of approval:** research authorization only; no mathematical certification, production activation, or deployment authority

## 1. Matter

GCL proposes to investigate whether the semantic discipline of Cartesian closure can be extended with typed reflection, a certified improvement ordering, and guarded recursion to form a coherent substrate for bounded recursive self-improvement.

The starting invariant is the exponential adjunction

\[
\mathcal C(X\times A,B) \cong \mathcal C(X,B^A),
\]

with evaluation and currying related by the beta law

\[
\operatorname{ev}_{A,B}\circ(\Lambda f\times\operatorname{id}_A)=f.
\]

This supplies a semantics-preserving evaluation–abstraction invariant. By itself it does not provide self-inspection, capability ordering, or safe recursion. WP00 therefore proposes to add those three structures explicitly and test whether the combined object supports certified recursive replacement without claiming unrestricted self-reference.

## 2. Proposed formal object

The work package will study a structure of the form

\[
\mathfrak R=
(\mathcal C,\mathrm{Prog},\mathrm{run},\sqsubseteq,Q,\triangleright,\operatorname{gfix}),
\]

where:

- `C` is Cartesian closed;
- `Prog(A)` is a typed representation of programs producing values of type `A`;
- `run_A : Prog(A) -> Later A` is staged evaluation;
- `sqsubseteq` is a semantic refinement order;
- `Q` is a separately represented operational quality measure;
- `Later` is a guarded temporal modality;
- `gfix` is a guarded fixed-point operator.

The research question is not whether this notation alone constitutes recursive self-improvement. The question is whether one concrete model can satisfy the required laws simultaneously and support an executable, proof-carrying replacement loop with an explicit trust boundary.

## 3. Reflection obligation

WP00 must distinguish semantic values from inspectable code. It may not assume an unrestricted internal quotation operator from arbitrary semantic values to syntax.

The intended interface is staged:

\[
\mathrm{run}_A : \mathrm{Prog}(A) \to \triangleright A.
\]

For quoted well-typed terms, the adequacy target is

\[
\mathrm{run}_A(\ulcorner t\urcorner)
=
\operatorname{next}_A(\llbracket t\rrbracket).
\]

A running system may carry an explicit image containing solver code, proposer code, configuration, and proof metadata. The proposer may inspect that image and propose a replacement, including a replacement for the proposer itself. This is intensional self-rewriting over explicit data, not unrestricted semantic self-application.

## 4. Improvement-order obligation

Exact denotational equality is sufficient for optimization but not for capability growth. WP00 must therefore separate:

1. semantic equivalence;
2. specification-preserving refinement;
3. operational quality.

For a task relation `R`, a concrete capability order may use safe competence-domain extension:

\[
p\sqsubseteq_R q
\iff
\operatorname{Safe}_R(q)
\land
D_p\subseteq D_q.
\]

Operational quality is represented independently, for example by a vector containing coverage, accuracy, latency, memory, and risk. An accepted strict improvement must satisfy both semantic refinement and the declared quality order.

The formal development must state and check monotonicity of composition and compatibility of the refinement order with currying and evaluation.

## 5. Proof-carrying admission obligation

A proposal must carry evidence sufficient for a small trusted checker to validate the declared gate. The checker is not required to decide arbitrary program equivalence.

A candidate admission record should establish, as applicable:

- well-typedness;
- specification or contract preservation;
- semantic refinement;
- required quality improvement;
- exact binding to the candidate artifact and evaluation context.

Admission must fail closed. A rejected, stale, malformed, or insufficiently evidenced proposal leaves the admitted state unchanged.

## 6. Controlled-recursion obligation

WP00 must exclude unguarded recursive self-application from the claimed mechanism.

The intended recursive interface is guarded:

\[
f : \triangleright A \to A,
\qquad
\operatorname{gfix}_A(f) : A,
\]

with the characteristic equation

\[
\operatorname{gfix}(f)
=
f(\operatorname{next}(\operatorname{gfix}(f))).
\]

A candidate concrete model is the topos of trees, `Set^(omega^op)`, with a later modality that shifts observations by one stage. The final work is not required to use this model if a better concrete model is supplied, but it must provide an actual model rather than rely only on syntax.

## 7. Recursive replacement loop

The target bounded loop is:

\[
\boxed{
\text{Generate}
\to
\text{Type-check}
\to
\text{Evaluate}
\to
\text{Compare}
\to
\text{Certify}
\to
\text{Authorize}
\to
\text{Replace}
}
\]

The recursive call must occur only after the current candidate has passed its admission gate.

A finite run may be defined by primitive recursion over an explicit budget. An indefinite observable trace, if included, must be productive through the guarded modality.

## 8. Required theorem target

Assuming the trusted checker is sound for the admitted certificate language, the mechanized core should prove a preservation result covering:

1. type preservation of every admitted state;
2. preservation of the declared safety/contract invariant;
3. monotone semantic refinement across accepted replacements;
4. strict quality progress where the policy declares strict improvement;
5. stasis after rejected proposals;
6. productivity of the guarded recursive trace.

The theorem must state its assumptions explicitly. In particular, checker soundness must not be smuggled into an unqualified claim of self-verification.

## 9. Required executable demonstration

WP00 must contain at least one bounded executable demonstration with a small enough domain to inspect completely.

The baseline demonstration should include both:

- a capability-extension transition in which the candidate safely solves a strict superset of the baseline competence domain; and
- a semantics-preserving optimization transition in which denotation is unchanged but the declared machine-cost measure improves.

The demonstration must also include negative fixtures showing rejection of malformed, stale, unsafe, non-refining, or non-improving proposals.

## 10. Required outputs

WP00 is complete only with all of the following:

- a concrete categorical model;
- typed reflective representation and staged evaluator;
- order-enriched refinement structure;
- guarded fixed-point construction;
- mechanically checked preservation theorem for the core claim;
- executable bounded demonstration;
- adversarial rejection fixtures;
- exact trust-boundary statement;
- reproducible commands and dependency lock;
- a short research report separating proved results, executable evidence, and conjecture.

## 11. Promotion gate

WP00 may advance only when the concrete model, mechanized theorem, executable demonstration, and trust-boundary statement refer to the same exact formal object and agree on the same claim boundary.

No result may be promoted from executable evidence to mathematical theorem without a separate proof artifact. No theorem about the bounded formal mechanism may be promoted to a claim about unbounded intelligence growth.

## 12. Claim boundary

Intake does not assert or authorize:

- universal program equivalence;
- unrestricted internal truth;
- infallible self-verification;
- guaranteed discovery of improvements;
- unbounded intelligence growth;
- unrestricted self-application;
- unguarded recursion;
- replacement of the complete trust base by itself;
- production self-modification;
- autonomous deployment or operational activation.

The strongest intended WP00 claim is narrower:

> Cartesian closure, typed reflection, certified refinement ordering, and guarded recursion can be combined into a coherent formal mechanism for recursively replacing a system with certified non-regressive variants beneath a fixed verification and admission kernel.

## 13. Council question

Should GCL admit `RSI-CCC-WP00 — Guarded Reflective Order-Enriched Cartesian Closure` as a bounded research work package under the outputs, promotion gate, and claim boundary above?

Allowed dispositions are:

- `approve`;
- `approve_with_conditions`;
- `changes_requested`;
- `reject`;
- `abstain`.

Council approval is advisory research-intake governance. It does not itself certify the mathematics, activate a self-modifying runtime, authorize production use, or alter reserved constitutional authority.
