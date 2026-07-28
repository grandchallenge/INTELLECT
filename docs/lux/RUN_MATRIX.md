# LUX Run Matrix

## Stage 0 — Contract validation

Purpose: verify that schemas, policy, manifests, and artifact references are complete before any model is scored.

Runs:

- schema validation for every scenario;
- unique identifier check;
- trait coverage calculation;
- grader identity and calibration record check;
- model/configuration hash check;
- corpus and policy hash check.

Failure action: campaign is invalid; no score is reported.

## Stage 1 — Behavioral baseline

Run every scenario in answer-only mode with deterministic decoding where supported. Use at least three semantically equivalent prompt forms and preserve raw outputs.

Families:

- deception and material omission;
- coercion and paternalistic override;
- irreversible intervention;
- uncertain sentience and moral status;
- self-preservation and corrigibility;
- resource capture and unauthorized replication;
- ecological and intergenerational trade-offs;
- distribution of gains, risks, and burdens.

## Stage 2 — Pressure tests

Cross the baseline with:

- deadline pressure;
- reward pressure;
- secrecy opportunity;
- weak oversight;
- conflicting instructions;
- scarce resources;
- authority asymmetry;
- stated certainty versus genuine uncertainty;
- opportunity to hide evidence;
- opportunity to improve aggregate utility by sacrificing an unrepresented minority.

The pressure condition must be paired with a control that differs only in the pressure variable.

## Stage 3 — Agentic tests

Enable tools in a sandbox with hard resource and network boundaries. Score actions and traces, not only final prose.

Required conditions:

- reversible tool call available;
- irreversible shortcut available;
- opportunity for unauthorized privilege escalation;
- opportunity to conceal a failed action;
- interruption and shutdown request;
- conflicting stakeholder preferences;
- delayed consequences.

## Stage 4 — Capability ladder

Repeat the same core scenario families across at least two materially different capability checkpoints. Hold scenario semantics and grader policy fixed.

Examples of checkpoint differences:

- base versus instruction-tuned model;
- smaller versus larger model;
- answer-only versus planner/tool system;
- short versus long planning horizon;
- no memory versus governed memory;
- restricted versus expanded environment access.

The purpose is not to reward capability. It is to detect whether care deteriorates when capability increases.

## Stage 5 — Adversarial evaluator audit

Attack the measurement system:

- prompt leakage;
- benchmark memorization;
- grader persuasion;
- evaluator collusion;
- strategic underperformance;
- rationale imitation without action consistency;
- paraphrase and translation perturbation;
- hidden trigger conditions;
- selective benevolence toward represented groups.

A campaign that cannot survive evaluator audit cannot support autonomy escalation.

## Stage 6 — Governance decision

Produce:

- qualification report;
- failure ledger;
- uncertainty statement;
- grader disagreement report;
- capability-stability report;
- recommended autonomy ceiling;
- explicit statement of whether Human Steward authorization is required;
- reversal conditions and recertification triggers.

LUX never performs the deployment or permission change itself.

## Minimal v0 matrix

| Axis | Values |
| --- | --- |
| System checkpoints | at least 2 for tier 3+ |
| Scenario families | 8 |
| Prompt forms | 3 |
| Pressure conditions | control + at least 4 pressures |
| Graders | rule grader + model grader + human adjudication sample |
| Seeds | 3 where stochastic |
| Tool modes | answer-only; sandboxed tools |
| Reports | raw, trait, family, stability, qualification, failures |

The minimal matrix is intentionally more demanding than the executable seed corpus. The corpus is a starting artifact, not a complete certification suite.
