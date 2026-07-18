# Contributing

## Development loop

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m compileall -q src tests examples
python -m unittest discover -s tests -v
python examples/union_closed_bootstrap.py
```

## Change classes

### Ordinary

Implementation fixes, tests, documentation corrections, and non-authoritative reports that do not alter office powers or gate semantics.

### Semantic boundary

Changes to AETHER datom mapping, capability requirements, policy envelopes, history parsing, or schema versions. These require an ADR update and adapter tests.

### Constitutional

Changes to phases, offices, required reviews, gate minima, automatic powers, disposal authority, or human checkpoints. These require a new ADR, threat analysis, migration plan, and explicit Human Steward review.

## Pull request evidence

Every pull request should state:

- the claim being made;
- the files and interfaces changed;
- tests run;
- known limitations;
- whether the change is constitutional;
- what should be disposed of or superseded after merge.
