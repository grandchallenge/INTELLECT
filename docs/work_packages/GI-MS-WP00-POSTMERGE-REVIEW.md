# GI-MS-REV00 — Post-merge Council review of GI-MS-WP00

## Review status

`CORRECTIVE_REVIEW_IMPLEMENTED_CI_PENDING`

Reviewed object: merged `grandchallenge/INTELLECT#4` at merge commit `c135aa658658c503db3d8bf5aa79f5c5c3d6fdb5`.

This is a post-merge constitutional review. It does not certify mathematics. It reviews the correctness of the machinery that governs mathematical routing and promotion.

## Council review

**Status:** reviewed with required corrections applied.

The Council accepts the placement of the Solve route at Specification, the completed lineage check at Realization, and the Cert disposition check at Judgment. The lifecycle remains proportionate and does not duplicate MATH-PROGRAMME, MATHSOLVE, or MATHCERT authority.

The original implementation nevertheless collapsed three distinct states:

1. a Cert handoff exists;
2. a Cert disposition is complete and content-addressed;
3. a Cert disposition positively supports promotion.

The reviewed implementation separates them. `rejected` and `proof_debt` close lineage but cannot support an `accept` or `combine` judgment. Only `certified` and `qualified` can support positive mathematical integration.

## Adversary review

**Status:** reviewed; five bypass classes tested.

Findings:

- A registered claim absent from the specification could previously enter the Cert route. The reviewed constitution now requires exact bidirectional correspondence between declared and registered claim IDs.
- A complete Cert status could previously be recorded without an artifact identity. All states other than `pending` now require repository, commit, path, digest algorithm, and digest.
- A rejected or proof-debt handoff could previously satisfy the Judgment gate. Positive judgment now requires `certified` or `qualified`.
- A waiver record could previously set `cert_handoff_required` false. The reviewed constructor and schema make this value invariantly true.
- SHA-256-only artifact references prevented exact use of Git blob and tree identities already used by the mathematics repositories. The reviewed contract admits `git_blob_sha1`, `git_tree_sha1`, and `sha256` while rejecting commit IDs as artifact digests.

## Formalist review

**Status:** reviewed.

The following distinctions are now explicit:

- repository snapshot identity: `commit_sha`;
- artifact identity: `digest_algorithm` plus `digest` at `artifact_path`;
- handoff existence: any recorded status;
- completed disposition: `ready`, `submitted`, `certified`, `qualified`, `rejected`, or `proof_debt`, with artifact identity;
- positive promotion support: `certified` or `qualified` only.

A specification claim and a registered mathematical claim must have the same stable claim ID. Claim renaming therefore requires a new event and renewed Cert correspondence rather than silent substitution.

## Amanuensis review

**Status:** reviewed.

Continuity actions:

- the public package API remains stable through `grand_intellect.mathsolve`;
- the reviewed implementation is isolated in `mathsolve_reviewed.py` for audit legibility;
- package version advances from `0.2.0` to `0.2.1`;
- the route schema, runtime semantics, AETHER projection, tests, and this review record use the same status distinctions;
- GitHub remains present authority; AETHER remains a shadow projection.

No previous event is deleted. New route or handoff events supersede projected current state while historical events remain replayable.

## Referee review

**Status:** conditional approval pending repository CI and linked Programme/Solve corrective review.

The constitutional design is admissible after the corrections in this branch. Final approval requires:

1. all INTELLECT tests to pass on the exact corrective head;
2. MATHSOLVE to require true artifact identities and positive Cert status for promotion;
3. MATH-PROGRAMME to distinguish completed handoff from positive claim promotion and to enforce waiver scope and authority;
4. exact cross-repository provider commits to be reconciled after corrective merges.

## Claim boundary

This review establishes governance semantics only. It does not certify any mathematical claim, infer correctness from repository placement, or represent AETHER as authoritative.
