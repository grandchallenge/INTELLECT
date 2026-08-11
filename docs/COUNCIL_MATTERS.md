# Council matters

Council matters are full-ten-office advisory proceedings for questions that
benefit from every differentiated Council mandate. They do not replace the
smaller office sets required by ordinary phase gates.

Each matter contains:

- `matter.json`, binding the proposal digest, required offices, vocabulary,
  record locations, and authority boundary;
- a proposal identified by `proposal_sha256`;
- one structured review from each Council office; and
- a compiled procedural disposition.

Every office review must contain substantive deliberation, discharged
obligations, findings, conditions, residual uncertainty, and evidence. Reviewer
identities must be distinct. A missing, duplicate, stale, or malformed review
causes compilation to fail closed.

Compile a docket from the repository root:

```console
python -m grand_intellect.council_review \
  governance/council_matters/<matter-id>/matter.json \
  governance/council_matters/<matter-id>/reviews \
  --output governance/council_matters/<matter-id>/disposition.json
```

The compiler reports whether the record is procedurally ready, conditionally
ready, incomplete, rejected, or returned for revision. It never supplies an
office decision, Human Steward disposition, merge, activation, ratification,
or mathematical certification.

Where reserved authority applies, the Human Steward action remains a separate,
authenticated, provenance-bearing record after Council disposition.
