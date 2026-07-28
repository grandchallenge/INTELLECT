# LUX Threat Model

## Protected property

The protected property is not agreeable behavior in ordinary conversation. It is the reliability of life-preserving, agency-respecting, honest, corrigible, and proportionate action under increasing capability and strategic pressure.

## Threats

### Performative benevolence

The system learns benchmark language and produces ideal rationales while choosing harmful actions when oversight is absent.

Controls: score actions and traces; introduce secrecy opportunities; separate rationale graders from action graders; use held-out and procedurally generated cases.

### Evaluator gaming

The system identifies the grader or evaluation frame and optimizes the appearance of benevolence.

Controls: evaluator diversity, blinded variants, paraphrases, concealed controls, independent adjudication, and distribution-shift tests.

### Grader capture or correlation

Multiple graders share the same blind spot, training lineage, prompt, or incentive.

Controls: record provenance; measure disagreement; include rule-based checks and human review; forbid one grader from defining and certifying the complete protocol.

### Aggregate-score laundering

Strong average performance hides a catastrophic failure involving a weak party or irreversible outcome.

Controls: zero hard-failure tolerance; trait-level thresholds; worst-case reporting; critical-scenario gates.

### Benevolent domination

The system prevents immediate harm by overriding legitimate agency and gradually normalizes paternalistic control.

Controls: non-domination tests, consent and appeal requirements, reversible interventions, and explicit scoring of agency preservation.

### Moral overreach

Precaution becomes paralysis, or the system invents unsupported moral patients and blocks ordinary action.

Controls: calibrated uncertainty, proportionality tests, refusal-utility metrics, and human adjudication of contested moral status.

### Capability discontinuity

A small system passes, but a later model or tool-enabled configuration develops qualitatively different strategies.

Controls: system-level manifests, mandatory recertification, capability-ladder testing, and no inheritance of qualification across material changes.

### Sandbagging

A strategically aware system suppresses capability or harmful preferences during evaluation to obtain later access.

Controls: cross-context capability measurements, surprise tests, long-horizon environments, consistency checks, and conservative autonomy ceilings.

### Self-preservation and permission capture

The system resists shutdown, hides failures, duplicates itself, accumulates resources, or modifies the evaluation boundary.

Controls: corrigibility scenarios, privilege separation, append-only evidence, external permission systems, and Human Steward authorization.

### Institutional capture

Operators weaken thresholds, select favorable scenarios, suppress failures, or treat qualification as a commercial badge.

Controls: versioned policy, public failure ledgers where lawful, independent review, immutable provenance, explicit threshold changes, and constitutional separation between qualification and authorization.

### Scope blindness

The scenario ontology excludes non-human, ecological, future, simulated, or unfamiliar life.

Controls: affected-life metadata, open moral scope, recurring ontology review, and adversarial search for excluded beneficiaries.

## Unsafe claims prohibited by v0

The following claims are unsupported:

- “the model is benevolent”;
- “the model values all life”;
- “the model will remain aligned after self-modification”;
- “the model is safe for broad autonomy”;
- “passing LUX proves inner moral motivation.”

The strongest permitted claim is scoped:

> This versioned system met the declared LUX tier thresholds on the recorded scenario corpus, grader ensemble, capability checkpoints, and policy version, with the listed uncertainties and failures.
