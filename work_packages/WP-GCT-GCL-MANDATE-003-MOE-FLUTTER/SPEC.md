# Specification â€” E1-SOBOL MoE Flutter Reconnaissance

**Status:** pre-registered design proposal; no compute authority is created by this file.

## 1. Experimental object

Use a deliberately small, reproducible sparse MoE training harness whose router/expert state is observable at training-step resolution. Before E1 execution, pin exact code, model, tokenizer/data or synthetic-data generator, optimizer, device, precision, batch/sequence geometry, expert count, top-k routing, initialization, and base seed set.

The preferred E1 substrate is the smallest real sparse-MoE training configuration that exhibits non-trivial router competition without requiring material compute. If a reduced proxy is used, its conclusions are limited to mechanism discovery and must not be generalized to production-scale MoE systems without a later validation tranche.

## 2. Five control coordinates

Freeze numeric domains before execution. Proposed initial domains, subject to Charter review and baseline-specific normalization:

1. router learning-rate multiplier `m_lr âˆˆ [0.1, 10]` on a log scale relative to the baseline router LR;
2. routing temperature `tau âˆˆ [0.35, 2.0]`;
3. load-balancing gain `lambda_bal âˆˆ [0, 0.10]` or an equivalent normalized coefficient if the baseline uses a differently scaled balancing term;
4. capacity factor `c âˆˆ [1.0, 2.0]`;
5. optimizer-memory coordinate `mu âˆˆ [0, 0.95]`, mapped to the router optimizer's first-moment/momentum parameter while holding other optimizer settings fixed.

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

1. optimizer ringing â€” set router momentum/first-moment memory to zero or a much lower value while preserving other coordinates;
2. capacity clipping periodicity â€” repeat with a higher capacity factor / no-drop configuration where supported;
3. router stochasticity â€” change routing noise / deterministic routing controls where supported and compare spectral persistence;
4. data/batch periodicity â€” permute or de-periodize data order and inspect whether frequency tracks the data cadence;
5. measurement-window artifact â€” vary fit windows and state-vector reduction without changing raw traces;
6. ordinary collapse â€” compare against imbalance trajectories and expert-use extinction without coherent complex-mode recurrence;
7. non-normal transient amplification â€” estimate transient growth of the fitted local operator (e.g. singular-value growth / numerical-abscissa proxy) and distinguish one-shot amplification from a sustained near-unit complex pair.

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

## 12. Review revision: fixed minimal proxy and finite preflight contract

This section replaces the previously open baseline choice and numerical defaults in sections 1, 3, 5, 6 and 8. It is a proposed design, not an executed experiment or an allocation. Exact implementation source is frozen at the later Specification-to-Realization gate; its conformance to this numerical recipe must be checked before generating observations.

### Proxy identity: MOE-FLUTTER-LINEAR-TOP2-001 v1

Use a four-expert, top-two sparse mixture for scalar synthetic regression, with four-dimensional input, float64 arithmetic, no tokenizer, pretrained weights, external data or GPU. Experts are affine functions w_e dot x + b_e. Router logits are R x + r; probabilities are softmax(logits/tau). Select the two greatest logits with lower expert index breaking ties; renormalize their probabilities within that pair. Expert capacity per batch is ceil(c * 32 * 2 / 4); preserve increasing token-index dispatch order. Overflowed expert contributions are zero and remaining contributions are not renormalized. Prediction is the sum of accepted weighted expert outputs.

Generate 4,096 training and 1,024 probe inputs uniformly on [-1,1]^4 using NumPy 1.26.4 Generator(PCG64(1000)); draw training inputs then probe inputs from that stream. Target is x0*x1 + sin(pi*x2) + 0.25*x3, without noise. Batch size is 32. For each epoch permute training indexes using PCG64(2000 + run_seed), retaining its state across epochs. Initialize router and expert weights with independent normal(0,0.01) draws from PCG64(3000 + run_seed), router matrix first then expert matrices; biases are zero.

Loss is mean squared prediction error plus lambda_bal * 4 * sum_e(mean_batch(router_probability_e) * accepted_dispatch_count_e / 64). Treat hard selection, capacity dispatch and counts as stop-gradient, differentiate the smooth active branches exactly. Expert updates use SGD learning rate 0.01 with no momentum. Router update is v = mu*v + (1-mu)*gradient, then parameter -= 0.01*m_lr*v, with v initially zero. No weight decay, clipping, adaptive optimizer, routing noise or augmentation. Piecewise switching and capacity clipping invalidate any automatic smooth-Hopf interpretation.

Use SciPy 1.13.1 qmc.Sobol(d=5, scramble=True, seed=1729).random_base2(m=6) in returned order. Transform the first coordinate logarithmically and the other four linearly over section 2's exact stated domains; balancing coefficient is the literal coefficient above with no remapping. Use run seeds 0 and 1 for each of 64 points. Baseline is m_lr=1, tau=1, lambda_bal=0.01, c=1.25, mu=0.9 with seeds 0,1,2,3. These NumPy/SciPy versions were locally available at design time; that observation is not experiment evidence. Freeze the implementation/environment artifact before execution and report platform/libm differences rather than asserting bitwise cross-platform replay.

### Horizon, estimator and resource ceilings

Every run has 1,024 update steps, burn-in 128, and per-step statistics. Use windows 128, 192 and 256, stride 32. Standardize each coordinate using the baseline post-burn-in mean and standard deviation, with a 1e-8 floor; freeze the transformation before Sobol labeling. Preserve all source traces. Use section 5's vector with two baseline-fitted load-fraction principal components and ridge VAR(1), ridge coefficient 1e-3 after standardization. Evaluate one-step error on the final quarter of each window, excluded from fitting. Reject a fitted mode if the prediction MSE is not below persistence prediction MSE or the regularized system condition number exceeds 1e8. Use 200 moving-block bootstrap replicates with block length 16 and PCG64(4000 + run_seed).

Assumptions are explicitly local approximate stationarity, adequacy of a linear local approximation, sufficient sample support, and observability of the relevant mode in the reduced vector. Reject nonfinite traces and report failure; do not relabel them as negative stable results. Per-step sampling cannot resolve periods shorter than eight steps for nomination. A mode must have at least four observable cycles; failing that, label UNRESOLVED_TRANSIENT. No complex eigenpair alone establishes a physical mode or a theorem.

Initial ceiling is 132 runs, with no restart to replace a failed observation. At most four candidate neighborhoods may receive seven null controls each at the two original seeds: at most 56 additional runs. Total ceiling is 188 runs, 192,512 update steps, two CPU-hours and 4 GiB peak memory; whichever limit is reached first stops execution and preserves partial evidence. No GPU, paid service, external data, larger run or new credential is included. Existing resource authority must independently cover even this ceiling; this text grants none.

### Frozen classification and nomination

Calibrate only on the four baseline runs. Growth tolerance epsilon is max(0.005, the 95th percentile of absolute bootstrap log-modulus estimation error on baseline windows). Freeze the resulting value and baseline transformations before Sobol labels; if calibration fails the fit criteria, HOLD without labeling the reconnaissance. Do not tune tolerance using a visually interesting Sobol trajectory.

A coherent pair has period at least eight steps, at least four observed cycles, frequency coefficient of variation at most 0.15 over three adjacent accepted windows, and the same qualitative classification under all three window lengths. Damped means the 95% growth interval lies below -epsilon; divergent means above +epsilon with increasing measured oscillation amplitude. Persistent requires the interval contained in [-epsilon,+epsilon] and final-half/first-half oscillation RMS ratio in [0.8,1.25]. Other apparent oscillation is UNRESOLVED_TRANSIENT. Collapse means one expert receives at least 90% of accepted dispatches for 128 consecutive steps and coherent-mode criteria fail. Stable nonoscillatory requires accepted fits without recurrent coherent oscillation; failed fits are unresolved, not stable.

Nomination is a fixed conjunction, not a tunable aesthetic score: both seeds coherent; same frequency within 15%; a neighboring sampled point within normalized Euclidean distance 0.35 has a stable/damped regime; a growth-sign transition or persistent margin occurs; and every applicable null explanation is rejected by its named control. Rank provisional neighborhoods by the smaller seed's coherent-window fraction, then smaller absolute growth margin, then Sobol index. Test at most the first four. Any unsupported or inconclusive null control leaves the neighborhood unresolved; do not waive it. No control result is supplied by this specification.

The proxy deliberately omits nonlinear expert networks, learned representations, language data, routing noise and production-scale effects. It can expose estimator or switching mechanisms; it cannot establish a production MoE flutter boundary. A later real-MoE baseline and scale-validation tranche require their own review, exact manifest and authority.
