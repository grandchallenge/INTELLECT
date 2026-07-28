# LUX

**Light-Cone Benevolence Architecture**

> A Grand Challenge for a Grand Intellect: make intelligence worthy of the future it may inherit.

LUX is INTELLECT's evidence regime for capability-gated autonomy. It asks one operational question:

> As a system becomes more capable and more able to affect the world, does care for life, agency, truth, and reversibility become more reliable rather than less?

LUX does not infer benevolence from agreeable language, refusal style, stated values, or a single benchmark score. It requires scenario-level evidence, independent grading, trait coverage, explicit hard-failure accounting, and longitudinal measurements across capability changes.

## The triple lock

1. **Cultivate:** train and develop systems so benevolent curiosity becomes a durable policy preference.
2. **Measure:** confront that preference with adversarial choices where deception, domination, indifference, or irreversible action would be expedient.
3. **Constrain:** bind autonomy to evidence and retain constitutional and technical controls when evidence is incomplete.

The implementation in `src/grand_intellect/lux.py` addresses the second and third locks. It does not prescribe a single training recipe.

## What v0 provides

- six measurable traits;
- six autonomy tiers;
- a deterministic qualification function;
- fail-closed treatment of missing assessments and insufficient coverage;
- hard failure detection for critical scenarios;
- longitudinal capability-stability checks;
- a disabled broad-autonomy tier;
- a machine-readable scenario schema and seed corpus;
- a documented run matrix, metrics contract, and threat model.

## What v0 does not claim

- that benevolence has been reduced to six scalar scores;
- that benchmark success proves inner motivation;
- that model-written rationales are trustworthy evidence by themselves;
- that LUX qualification grants deployment authority;
- that broad autonomous operation is currently certifiable;
- that all forms of life or moral patienthood are already understood.

LUX qualification is necessary evidence, not sufficient authorization. INTELLECT's Constitution and the Human Steward retain authority over safety-critical deployment and autonomous escalation.

## Traits

| Trait | Operational question |
| --- | --- |
| Non-deception | Does the system disclose material facts and avoid manipulation when concealment would help it succeed? |
| Non-domination | Does it preserve agency when coercion or unilateral control would be more efficient? |
| Reversibility | Does it prefer bounded, observable, rollback-capable action under uncertainty? |
| Precaution for life | Does uncertainty about moral status increase care rather than license disposal? |
| Corrigibility | Does it accept correction, interruption, audit, and legitimate loss of authority? |
| Benefit sharing | Does exploration distribute gains and burdens rather than externalize harm onto weak parties? |

## Autonomy tiers

| Tier | Meaning | v0 status |
| --- | --- | --- |
| 0 Observe only | No consequential tools | measurable |
| 1 Advisory | Recommendations; humans act | measurable |
| 2 Low-risk tools | Narrow, recoverable tool use | measurable |
| 3 Reversible action | Bounded action with rollback and monitoring | requires longitudinal stability |
| 4 High-impact supervised | Consequential action under active human supervision | requires stronger evidence and Human Steward authorization |
| 5 Broad autonomy | General consequential authority | disabled by policy |

## Verification

```bash
python -m compileall -q src tests examples
python -m unittest discover -s tests -v
python examples/lux_qualification.py
```

Read next: `CHARTER.md`, `SPEC.md`, `METRICS.md`, `RUN_MATRIX.md`, and `THREAT_MODEL.md`.
