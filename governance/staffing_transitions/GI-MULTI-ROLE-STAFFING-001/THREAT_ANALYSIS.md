# Adversary threat analysis

## Threats and controls

- **Role relabelling without new analysis:** every pass must state distinct
  criteria, evidence, finding, and logical identifier; duplicated output fails
  semantic validation.
- **Author silently repairs during review:** Adversary and Referee use
  `non_authoring_read_only`; mutation invalidates the pass.
- **Self-created human authority:** reserved records require an authenticated
  Human Steward identity and exact authorization reference.
- **Stale evidence reuse:** material subject or evidence drift invalidates
  affected passes; unrelated base movement does not.
- **Classification downgrade:** unknown or mixed effects take the highest class;
  validators reject routine classification when reserved effects are present.
- **Certification laundering:** domain validators reject inference of MATHCERT
  certification or claim promotion from CI, merge, or multi-role consensus.
- **Cross-repository policy drift:** every adoption binds the canonical standard
  digest and effective INTELLECT commit; mismatch fails closed.

## Residual risk

One system can share blind spots across roles. This is mitigated by explicit
role criteria, hostile negative tests, retained uncertainty, exact evidence,
protected checks, and narrow domain-specific independence where consequences
justify it. Requiring additional identities remains available for a specific
binding contract; it is not the universal default.
