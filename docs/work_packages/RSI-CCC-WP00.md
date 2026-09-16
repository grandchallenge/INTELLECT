# RSI-CCC-WP00 — Guarded Reflective Cartesian Closure with Certified Refinement

## Status

M0 smallest-complete-model tranche in progress under `grandchallenge/INTELLECT#101`.

Research intake was authorized under `GI-COUNCIL-RSI-CCC-001` and integrated by PR #100 at merge commit `2badd8c3197ef4515591bba05ff782ff3cafc930`.

The current tranche supplies a content-bound formal target, a bounded executable checker, and adversarial fixtures. It does **not** yet supply the mechanically checked preservation theorem required for WP00 promotion.

The governed identity remains `RSI-CCC-WP00`. The M0 descriptive title is narrowed from “Order-Enriched Cartesian Closure” because the selected ambient model is not presently claimed to carry a nontrivial order on every hom-set.

## Exact research claim

The target is a bounded self-replacement mechanism with four distinct components:

1. a Cartesian-closed guarded semantic core;
2. typed reflection over explicit program representations;
3. an external certified semantic-refinement preorder over an explicitly admitted program or morphism relation domain, plus a separate operational quality order;
4. guarded recursion beneath a fixed verification/admission kernel.

The strongest intended WP00 claim is:

> Cartesian closure, typed reflection, certified refinement ordering, and guarded recursion can be combined into a coherent formal mechanism for recursively replacing a system with certified non-regressive variants beneath a fixed verification and admission kernel.

This statement remains a research target until the mechanized proof lane closes.

## M0 enrichment resolution

M0 takes the smaller defensible path.

The ambient categorical model remains the topos of trees, `Set^(omega^op)`. WP00 does **not** infer an order-enriched category merely because admitted programs carry a refinement relation. Instead, refinement is a separately defined preorder over an explicit relation domain of typed admitted programs or represented morphisms.

The theorem lane must prove the declared compatibility laws only on that relation domain:

- reflexivity and transitivity;
- monotonicity of composition when all represented morphisms are in scope;
- order preservation by currying for declared related representations;
- order preservation by evaluation for declared related function and argument representations.

A later move to `Pos`/CPO-valued guarded presheaves would be a stronger model change and requires a new exact formal object and review. It is not assumed by M0.

## M0 concrete model

The formal-object record selects `Set^(omega^op)` as the first concrete model candidate.

The required Cartesian-closed surface is

\[
\mathcal C(X\times A,B)\cong\mathcal C(X,B^A),
\]

with explicit product, Kripke exponential, evaluation, and currying constructions in the mechanization.

The later modality target is

\[
(\mathrm{Later}\,X)_0=1,\qquad
(\mathrm{Later}\,X)_{n+1}=X_n,
\]

with natural transformation

\[
\mathrm{next}_X:X\to\mathrm{Later}\,X.
\]

The guarded fixed-point target is

\[
f:\mathrm{Later}\,A\to A
\quad\Longmapsto\quad
\mathrm{gfix}(f):A
\]

with characteristic law

\[
\mathrm{gfix}(f)=f(\mathrm{next}(\mathrm{gfix}(f))).
\]

These are theorem targets, not claims established by the Python reference model.

## Reflection boundary

`Prog(tau)` denotes closed, intrinsically well-typed program representations for an admitted object language. Reflection is staged:

\[
\mathrm{run}_\tau:\mathrm{Prog}(\tau)\to\mathrm{Later}\,\llbracket\tau\rrbracket.
\]

The adequacy target is

\[
\mathrm{run}_\tau(\mathrm{quote}(t))
=
\mathrm{next}_\tau(\llbracket t\rrbracket).
\]

WP00 does not assume an unrestricted semantic quotation operator `A -> Prog(A)` and does not admit unrestricted self-application.

## Improvement order

Semantic equivalence, specification refinement, and operational quality are separate relations.

For the bounded executable instance, a candidate refines the admitted solver only when it preserves every previously answered task and weakly extends the competence domain. Capability improvement requires strict competence-domain inclusion.

A semantics-preserving optimization requires an identical answer vector and strictly lower declared cost under the same fixed evaluation context.

A candidate cannot supply its own metric or context.

This executable preorder is evidence about the admission protocol. It is not evidence that every hom-set of `Set^(omega^op)` is ordered.

## Fixed trust kernel

The following remain outside the replacement gate:

- checker semantics;
- evaluator/interpreter semantics used by the checker;
- admission policy;
- artifact/content identity rules;
- evaluation-context and metric binding;
- checker resource limits.

Any attempted substitution is rejected.

This fixed-kernel boundary is part of the theorem assumptions and cannot be hidden by the phrase “self-verification.”

## Bounded executable evidence

`src/grand_intellect/rsi_ccc_wp00.py` implements a finite parity domain over integers `0..15`.

The positive trace has two accepted steps:

1. `baseline` answers only inputs `0..3`;
2. `capability-extension` answers the full finite domain correctly;
3. `optimized-equivalent` preserves the full answer vector and reduces declared cost from `40` to `10`.

Admission binds every proposal to:

- the exact admitted base digest;
- the exact candidate digest;
- `parity16-fixed-context-v1`;
- `rsi-ccc-fixed-kernel-v1`;
- fixed resource bounds.

Rejected proposals leave the admitted state unchanged.

## Adversarial fixtures

The test suite exercises fail-closed rejection for:

- malformed proposal shape;
- stale base identity;
- candidate digest mismatch;
- metric/evaluation-context substitution;
- trust-kernel substitution;
- resource-bound violation;
- unsafe output;
- loss of previously admitted competence;
- absence of strict improvement;
- candidate-defined improvement mode.

These tests establish behavior of the bounded executable checker only.

## M1 theorem order

The mechanization tranche must proceed in layers:

\[
\text{CCC laws}
\to
\text{guardedness}
\to
\text{reflection adequacy}
\to
\text{refinement compatibility}
\to
\text{admission preservation}.
\]

The admission theorem must retain checker soundness, evaluation-context integrity, certificate validity, and resource assumptions as explicit hypotheses.

The M1 milestone is:

\[
\boxed{\text{one proved guarded self-replacement step}}
\]

One typed program representation proposes another; the checker accepts or rejects it; an accepted transition preserves the declared invariant. Repeated application may be considered only after the one-step theorem is closed.

## Mechanization obligation

WP00 cannot pass its promotion gate until a Lean 4 proof artifact, bound into the same governed manifest, establishes at least:

- the stage-indexed objects and restriction maps;
- products and the Kripke exponential;
- evaluation and currying laws;
- `Later`, `next`, and guarded fixed-point laws;
- the intrinsically typed object language;
- quotation/interpreter adequacy;
- external refinement-preorder laws on the declared relation domain;
- scoped compatibility with composition, currying, and evaluation;
- checker-soundness and evaluation-context assumptions;
- one-step admission preservation;
- guarded productivity for the later trace theorem.

Undecidable properties must enter through an explicit certificate language or a bounded decision procedure. No implicit oracle is admissible.

## Stop or narrow gate

Do not expand scope if the ambient guarded CCC cannot support the typed semantics, if reflection requires unrestricted quotation, if the external refinement relation cannot satisfy its scoped compatibility laws, if preservation requires a mutable trust anchor or unstated oracle, or if the formal and executable artifacts cannot remain bound to one exact manifest.

## Claim boundary

M0 does not claim ambient order enrichment of `Set^(omega^op)`. It does not certify the proposed mathematics and does not authorize production self-modification, autonomous deployment, unbounded RSI claims, unrestricted self-reference, or replacement of the verification/admission trust kernel.
