# Specification — E1-SOBOL MoE Flutter Reconnaissance

**Status:** pre-registered design proposal; no compute authority is created by this file.

## 1. Experimental object

Use a deliberately small, reproducible sparse MoE training harness whose router/expert state is observable at training-step resolution. Before E1 execution, pin exact code, model, tokenizer/data or synthetic-data generator, optimizer, device, precision, batch/sequence geometry, expert count, top-k routing, initialization, and base seed set.

The preferred E1 substrate is the smallest real sparse-MoE training configuration that exhibits non-trivial router competition without requiring material compute. If a reduced proxy is used, its conclusions are limited to mechanism discovery and must not be generalized to production-scale MoE systems without a later validation tranche.

## 2. Five control coordinates

Freeze numeric domains before execution. Proposed initial domains, subject to Charter review and baseline-specific normalization:

1. router learning-rate multiplier `m_lr ∈ [0.1, 10]` on a log scale relative to the baseline router LR;
2. routing temperature `tau ∈ [0.35, 2.0]`;
3. load-balancing gain `lambda_bal ∈ [0, 0.10]` or an equivalent normalized coefficient if the baseline uses a differently scaled balancing term;
4. capacity factor `c ∈ [1.0, 2.0]`;
5. optimizer-memory coordinate `mu ∈ [0, 0.95]`, mapped to the router optimizer's first-moment/momentum parameter while holding other optimizer settings fixed.

Any baseline-specific remapping must be declared before samples are generated and must preserve a monotone interpretation of each coordinate.

## 3. E1 design

Use a scrambled Sobol design rather than a Cartesian grid.

Proposed smallest useful tranche:

- 64 Sobol points across the five-dimensional normalized cube;
- 2 independent seeds per point for reconnaissance;
- one fixed baseline/control point repeated across at least 4 seeds to establish estimator/noise variance;
- bounded training horizon selected by a preflight sufficient to observe router equilibration and at least several candidate oscillation periods if present.

Do not increase point count merely to improve coverage. Escalate only if the first design leaves a decision-relevant ambiguity that cannot be resolved by targeted resampling or narrow continuation.

## 4. Observables

Capture at a fixed cadence and preserve raw traces for at least:

- training loss and validation/probe loss where applicable;
- router entropy;
- per-expert token/load fraction;
- coefficient of variation / Gini-style expert-load imbalance;
- expert activation/use counts;
- overflow/drop fraction and effective capacity utilization;
- router logits or a compact router-state projection;
- router gradient norm and update norm;
- expert gradient/update summary statistics;
- optimizer first-moment norm for router parameters;
- learning rate and temperature actually applied;
- step time and any skipped/overflowed-step signal.

If dimensionality is high, preserve the raw source statistics and derive low-dimensional state vectors reproducibly rather than recording only the final reduced representation.

## 5. Local-dynamics / complex-mode estimator

Freeze the estimator before E1 results are inspected.

Default proposal:

1. form a standardized local state vector from router entropy, imbalance, overflow/drop rate, router update norm, optimizer-memory norm, and the leading principal components of expert-load fractions;
2. fit a regularized local VAR(1) / linear state-transition model on overlapping windows after a declared burn-in;
3. compute eigenvalues of the fitted transition matrix;
4. track the dominant non-real conjugate pair, its modulus, angle/frequency, and implied log-damping or growth rate;
5. bootstrap or block-resample windows to estimate uncertainty;
6. repeat under at least three reasonable window lengths to test measurement-window dependence;
7. compare fitted-mode predictions against held-out one-step state evolution so spurious eigenpairs from ill-conditioned fits are rejected.

A point is not classified by spectral evidence alone; the fitted pair must correspond to recurrent structure in the measured traces.

## 6. Predeclared regime labels

Use operational labels, not theorem claims:

- `STABLE_NONOSCILLATORY`: no recurrent oscillation; dominant fitted modes are real or non-real modes are clearly damped/noise-like.
- `DAMPED_OSCILLATION`: recurrent complex mode with negative growth/damping, consistent frequency across adjacent windows, and amplitude decaying toward baseline.
- `PERSISTENT_OSCILLATION`: recurrent complex mode with near-zero fitted growth within uncertainty, stable frequency, and non-decaying bounded amplitude over the declared observation window.
- `DIVERGENT_OSCILLATORY_INSTABILITY`: recurrent complex mode with positive fitted growth and increasing oscillatory amplitude prior to numerical/training failure.
- `ORDINARY_COLLAPSE`: severe expert-load concentration or routing degeneracy without evidence of a coherent complex-mode crossing.
- `UNRESOLVED_TRANSIENT`: oscillatory-looking behavior that fails recurrence, window-stability, or null-model discrimination.

Exact numeric tolerances for growth-rate sign, frequency stability, recurrence length, and collapse imbalance must be fixed from baseline-estimator noise calibration before the Sobol result labels are generated.

## 7. Null-model tests

Every nominated candidate neighborhood must be tested against:

1. optimizer ringing — set router momentum/first-moment memory to zero or a much lower value while preserving other coordinates;
2. capacity clipping periodicity — repeat with a higher capacity factor / no-drop configuration where supported;
3. router stochasticity — change routing noise / deterministic routing controls where supported and compare spectral persistence;
4. data/batch periodicity — permute or de-periodize data order and inspect whether frequency tracks the data cadence;
5. measurement-window artifact — vary fit windows and state-vector reduction without changing raw traces;
6. ordinary collapse — compare against imbalance trajectories and expert-use extinction without coherent complex-mode recurrence;
7. non-normal transient amplification — estimate transient growth of the fitted local operator (e.g. singular-value growth / numerical-abscissa proxy) and distinguish one-shot amplification from a sustained near-unit complex pair.

## 8. Candidate-surface score

A Sobol point may contribute to a nominated surface only when:

- the same qualitative mode recurs in both reconnaissance seeds or in a targeted confirmatory restart;
- dominant complex-pair frequency is locally coherent;
- estimated growth/damping approaches or changes sign under a coherent nearby parameter move;
- a neighboring stable/non-oscillatory regime exists;
- ordinary collapse is not the sole explanation;
- the result survives declared window sensitivity checks.

Nomination should be based on a fixed score assembled from recurrence, spectral-margin proximity, local parameter coherence, and null-test penalties. Do not hand-pick a visually attractive trajectory.

## 9. E2/E3 continuation trigger

E2 is admitted only if E1 yields at least one reproducible candidate neighborhood. E3 continuation uses a narrowly bracketed one-dimensional or low-dimensional path through the nearest candidate surface, with at least 3 seeds and a frozen measurement protocol.

Measure onset location, frequency, damping/growth, return behavior and any hysteresis observable inside the bounded training regime.

## 10. Resource escalation

Remain on the smallest available single-GPU envelope for E1 design calibration and initial reconnaissance.

Escalation to A100/H100-scale or materially larger model/data regimes is justified only if:

- E1 identifies a candidate surface that survives null controls;
- the next decision requires scale validation rather than more local discrimination;
- the proposed larger run has a fixed manifest, bounded seed/point count, estimated GPU-hours and a stop rule;
- applicable GCT/GCL resource authorization is recorded before execution.

## 11. Artifact contract

For every run preserve:

- immutable experiment manifest;
- exact code/environment/model/data identities;
- Sobol coordinate and transformed parameter values;
- seed;
- raw observable traces;
- reduced state construction metadata;
- estimator configuration and fitted operator/eigenvalues per window;
- regime label and reason codes;
- null-test relations;
- runtime/resource accounting;
- failure/abort reason where applicable.

The E1 summary must include all negative samples and may not discard failed or inconvenient trajectories post hoc.
