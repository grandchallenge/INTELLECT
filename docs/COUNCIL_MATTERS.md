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

`GI-COUNCIL-OPERATING-BURDEN-002` is the narrow Stage 1 successor to the
returned `GI-COUNCIL-POSTMERGE-001` proposal. It recommends enforcement of the
effective no-mandatory-routine-reviewer staffing rule and impact-gated expensive
post-merge replay. It does not grant machine proxy, merge, activation,
ratification, certification, or promotion authority.

## Unanimous motions

Matters whose impact requires full quorum and unanimity use the Council motion
contract. Every office must submit one exact-motion-bound disposition under a
distinct reviewer identity. An affirmative result exists only when all ten
offices choose the same affirmative disposition. A split vote, rejection,
abstention, missing office, stale record, or duplicate reviewer fails closed
without changing current rules.

```console
python -m grand_intellect.council_motion \
  governance/council_matters/<matter-id>/motion.json \
  governance/council_matters/<matter-id>/reviews
```

A unanimous committee referral constitutes only the bounded drafting and
testing committee described by the exact motion. It creates no proxy authority
and does not amend, approve, merge, activate, ratify, or certify.

A committee schedule amendment uses a new exact motion and ten separately bound
office records. Unanimous Council tabling submits only that schedule for the
required Human Steward disposition; it does not amend the underlying policy or
start a time window until an exact ratification/opening record says so.

## Fifteen-office Grand assembly

The Constitution's five Minder offices and ten Council offices may form a
fifteen-office Grand assembly for cross-order terminal policy review. This is
broader than the formally named ten-office Council. Executor and Human Steward
remain operational offices outside its advisory quorum.

Grand assembly passage requires one exact-motion-bound record from every Minder
and Council office, fifteen distinct reviewer identities, fifteen distinct
session identities, and one unanimous affirmative disposition. Its compiler is
separate so historical ten-office Council contracts retain their exact meaning.

```console
python -m grand_intellect.grand_assembly_motion \
  governance/grand_assembly_matters/<matter-id>/motion.json \
  governance/grand_assembly_matters/<matter-id>/reviews
```

Grand assembly concurrence is not Human Steward authorization or effectiveness.
