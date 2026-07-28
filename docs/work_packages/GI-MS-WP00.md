# GI-MS-WP00 — MATHSOLVE Provider Contract

## Status

Executable foundation implemented for GitHub-first authority. AETHER projection is specified but not yet authoritative.

## Binding invariant

> Every Grand Intellect mathematical struggle, including MATH-PROGRAMME, is governed through MATHSOLVE or explicitly exempted. Full lineage is preserved in GitHub now and projected into AETHER later. Every resulting claim is handed to MATHCERT.

## Provider boundary

`MathSolveProvider` constructs two records:

- `governed`: identifies the Programme parent, MATHSOLVE work package and issue, Forge inputs, exact Solve commit, artifact digests, claim ledger, proof-obligation DAG, and certification repository;
- `exempted`: identifies the waiver, bounded scope, risks, Referee and Steward approval, Human Steward authority, and review condition.

Silence is neither a route nor a waiver.

## Executable admission gates

The mathematical constitution adds three fail-closed checks:

1. **Specification → Realization:** a mathematical work package requires an admissible MATHSOLVE route or exemption.
2. **Realization → Confrontation:** a governed route requires an exact 40-character provider commit, a nonempty digest-bearing artifact manifest, a claim ledger, and a proof-obligation DAG. A waiver must remain complete.
3. **Judgment → Integration:** every registered mathematical claim requires a MATHCERT handoff record. The handoff status remains explicit: `pending`, `certified`, `qualified`, `rejected`, or `proof_debt`.

The latest route event supersedes the previous route projection without deleting its history.

## GitHub-first lineage events

- `mathematics.declared`
- `mathsolve.route.recorded`
- `mathsolve.exemption.recorded`
- `mathematical.claim.registered`
- `mathcert.handoff.recorded`

GitHub issue, commit, path, and SHA-256 identities are the present stable references. Branch names alone are not accepted as completed realization lineage.

## Future AETHER projection

`aether/intellect_math_v0.aether` defines the first route and handoff predicates. It is a projection contract, not a claim that the schema is deployed. The migration sequence remains:

1. GitHub authoritative;
2. AETHER shadow projection;
3. dual-record conformance;
4. AETHER semantic authority for institutional state while GitHub remains authoritative for repository artifacts.

## Verification

`tests/test_mathsolve_provider.py` proves:

- ungoverned mathematics fails closed;
- an issue-only route can enter Realization but cannot enter Confrontation;
- realization lineage requires commit and digest identities;
- every registered claim requires a MATHCERT handoff;
- exemptions require Referee, Steward, and Human Steward authority.

## Known limitations

- The provider constructs and validates records; it does not fetch GitHub state itself.
- The first AETHER projection does not yet derive full constitutional gate readiness.
- Certification status is preserved but MATHCERT remains the authority for what each status means.
- Programme-wide inventory and MATHSOLVE manifest enforcement are delivered in the linked MP-MS-WP00 and MS-GOV-WP00 work packages.
