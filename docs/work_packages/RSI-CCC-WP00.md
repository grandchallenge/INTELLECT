# RSI-CCC-WP00 — Guarded Reflective Order-Enriched Cartesian Closure

## Status

M0 smallest-complete-model tranche in progress under `grandchallenge/INTELLECT#101`.

Research intake was authorized under `GI-COUNCIL-RSI-CCC-001` and integrated by PR #100 at merge commit `2badd8c3197ef4515591bba05ff782ff3cafc930`.

The current tranche supplies a content-bound formal target, a bounded executable checker, and adversarial fixtures. It does **not** yet supply the mechanically checked categorical preservation theorem required for WP00 promotion.

## Exact research claim

The target is a bounded self-replacement mechanism with four distinct components:

1. a Cartesian-closed semantic core;
2. typed reflection over explicit program representations;
3. semantic refinement plus a separate operational quality order;
4. guarded recursion beneath a fixed verification/admission kernel.

The strongest intended WP00 claim remains:

> Cartesian closure, typed reflection, certified refinement ordering, and guarded recursion can be combined into a coherent formal mechanism for recursively replacing a system with certified non-regressive variants beneath a fixed verification and admission kernel.

This statement remains a research target until the mechanized proof lane closes.

## M0 concrete model

The formal-object record selects the topos of trees, `Set^(omega^op)`, as the first concrete model candidate.

The required categorical surface is:

\[
\mathcal C(X\times A,B)\cong\mathcal C(X,B^A)
\]

with evaluation/currying compatibility, together with a later modality `Later` satisfying the staged interpretation

\[
(\mathrm{Later}\,X)_0=1,\qquad
(\mathrm{Later}\,X)_{n+1}=X_n.
\]

The guarded fixed-point target is:

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

`Prog(tau)` denotes closed, well-typed program representations for an admitted object language. Reflection is staged:

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

## Mechanization obligation

WP00 cannot pass its promotion gate until a proof artifact, bound into the same governed manifest, establishes the categorical and guarded preservation claims.

The mechanized statement must expose at least:

- CCC laws used by the construction;
- `Prog`/quotation/`run` typing and adequacy assumptions;
- `Later`/`next`/`gfix` laws;
- refinement preorder laws;
- monotonicity of composition;
- compatibility with currying and evaluation;
- checker-soundness and evaluation-context assumptions;
- admission preservation;
- guarded productivity.

Undecidable properties must enter through an explicit certificate language or a bounded decision procedure. No implicit oracle is admissible.

## Stop or narrow gate

Do not expand scope if the selected model cannot support the required interfaces without changing the claim, if reflection requires unrestricted quotation, if the refinement relation fails the claimed categorical compatibility, if preservation requires a mutable trust anchor or unstated oracle, or if the formal and executable artifacts cannot remain bound to one exact manifest.

## Claim boundary

M0 does not certify the proposed mathematics and does not authorize production self-modification, autonomous deployment, unbounded RSI claims, unrestricted self-reference, or replacement of the verification/admission trust kernel.
