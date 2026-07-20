# Programme Specification: One Layer Deeper

## Research claim

A compact model with a learned, weight-tied transition operator can achieve greater exact task accuracy per H100 second than an untied shallow baseline, while retaining useful accuracy when computational depth or problem family is held out.

The programme does not assume the hidden Hard recurrence is repeated modular squaring. Public tasks are treated as probes of reusable composition, not as permission to encode a modular-arithmetic solver.

## Candidate systems

1. **Official-style baseline:** one Transformer block, token/position embeddings, tied output embedding, RMS normalization, AdamW.
2. **Tied recurrent Transformer:** one shared attention/MLP cell applied repeatedly with explicit training and evaluation unroll counts.
3. **Recurrent neural tape:** a shared local convolution and gated channel mixer over short digit/work positions.

## Stability interventions

Stability mechanisms enter only after recurrent baselines are measured:

1. sigmoid-gated residual scales;
2. per-loop RMS state normalization;
3. a low-weight penalty on variance of loop update energy.

A mechanism is retained only when it improves held-out-depth accuracy or permits deeper evaluation without unacceptable throughput loss.

## Optimizer conditions

- **AdamW:** common baseline, betas `(0.9, 0.95)`.
- **Hybrid Muon:** Newton–Schulz orthogonalized updates for internal matrix parameters and AdamW for embeddings, norms, gates, and boundary state.
- **Groupwise AdamW:** slower momentum decay for the recurrent core and faster boundary adaptation for encoder/readout parameters.

Optimizer comparisons hold architecture, depth profile, batch size, and time tier fixed.

## Experimental phases

### P1 — Reproduction

Reproduce baseline E1, M1, and M5. Record exact accuracy, completed steps, examples/s, peak GPU memory, evaluator commit, Python/Torch/CUDA/driver identity, and full result payload. Repeat baseline seeds before using variance estimates.

### P2 — Recurrence

Compare tied Transformer and neural tape first on E1, then M5. Match evaluator wall-clock allowance, not nominal parameter count or step count.

### P3 — Extrapolation

Train on a distribution of unroll counts and evaluate beyond common training depth. Produce accuracy-versus-unroll and state-norm-versus-unroll curves.

### P4 — Stability

Ablate each intervention individually before combining. Promote only when replicated runs show improved held-out-depth accuracy, a wider stable unroll interval, or reduced catastrophic state growth without material throughput loss.

### P5 — Optimizer co-design

Compare the three optimizer modes on the promoted architecture. Report optimizer-state size, updates/s, score, and variance. Reject Muon when Newton–Schulz cost erases its learning-speed advantage.

### P6 — Hard governance

The machine gate requires complete M1–M5 evidence, at least three seeds per dataset, minimum baseline gain, bounded throughput loss, bounded held-out-depth gap, memory headroom, finite dynamics, and the exact evaluator pin. Passing the machine gate does not submit. The Human Steward authorizes the hosted attempt.

## Reproducibility contract

Every run artifact records the immutable upstream commit, generated profile and source hash, command, manifest, seed, hardware/software identity, raw evaluator result and logs, resource measurements, and classification as `official-faithful` or `resource-adapted`.

Only official-faithful evidence may satisfy the Hard gate. Architectural novelty is not an acceptance criterion. The simplest candidate on the superior wall-clock frontier is preferred.
