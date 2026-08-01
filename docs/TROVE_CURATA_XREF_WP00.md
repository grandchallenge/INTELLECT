# TROVE-CURATA-XREF-WP00

## Status

Approved GCL-side crossover work package. This record does not bind, modify, or govern `teraflop-ai/llm-data`.

## Purpose

TROVE-CURATA is an open pre-training data curation programme built around two distinct responsibilities:

- **TROVE** is the governed data estate: source objects, shards, corpus versions, and mixture-ready releases.
- **CURATA** is the curation control plane: extraction, normalization, policy processing, classification, deduplication, scoring, lineage, and admission decisions.

The work package reconciles this programme with existing GCL mechanisms so that data engineering does not create a parallel governance, provenance, or certification vocabulary.

## Authority boundary

1. `teraflop-ai/llm-data` is the collaborator-owned implementation repository.
2. GCL has no authority over that repository's branches, merges, releases, or claims unless its maintainers explicitly adopt a GCL contract.
3. INTELLECT governs GCL-side work packages and review obligations only.
4. GitHub remains the present operational record. AETHER is a future semantic projection and must not be required for initial execution.
5. Daft, Trafilatura, Presidio, OCR systems, embedding models, vector-search systems, and classifiers are replaceable providers. None has policy authority.
6. Successful execution is not equivalent to data quality, privacy, legality, safety, factuality, fitness for training, or downstream benefit.

## Crossover architecture

| Existing capability | Reuse in TROVE-CURATA | Decision |
|---|---|---|
| INTELLECT event-sourced work packages and office review | Govern material GCL-side curation changes and release decisions | Generalize |
| AETHER provenance and replay model | Future projection of source, transformation, review, and release events | Defer |
| GCL-GHOS repository controls | Baseline branch protection, immutable actions, CI, and review controls | Reuse directly |
| MATHFORGE source locks and provider manifests | Source/corpus provider manifests and deterministic acquisition records | Generalize |
| MATH-PROGRAMME artifact authority and claim ledgers | Corpus release manifests, admission state, and curation-claim boundaries | Generalize |
| MATHCERT intake/replay/qualification separation | CURATA-CERT qualification states and independent replay | Adapt locally |
| CSS adversarial fixtures | Parser, PII, dedup, contamination, and label-drift fixtures | Reuse directly |
| ALIGN matched comparisons | Ablations for curation interventions and mixture decisions | Reuse directly |
| MODULUS intervention telemetry | Threshold response curves and distribution-shift accounting | Adapt locally |
| MATHSOLVE mathematical routing | No direct data-curation analogue | Reject |

## Four-record contract

### TROVE Source Record

Identifies acquired material without asserting training eligibility.

Required concepts:

- stable source identifier;
- source family and URI;
- acquisition time or snapshot identity;
- raw byte or object digest;
- acquisition method and provider identity;
- rights and policy observations, explicitly non-dispositive;
- raw-content reference;
- source-level warnings.

### CURATA Transformation Receipt

Records one deterministic or model-assisted transformation.

Required concepts:

- input identity;
- stage contract and implementation identity;
- configuration and environment identity;
- model/tokenizer/prompt identities where applicable;
- output identity;
- metrics, warnings, and failure state;
- statement of whether the stage may alter content;
- independent replay method where available.

### CURATA Passport

Aggregates ordered lineage and eligibility decisions for a document or shard.

Required concepts:

- source record identity;
- ordered transformation receipt identities;
- PII and policy decisions;
- dedup memberships and retention role;
- quality and attribute scores with calibration references;
- admitted and prohibited uses;
- residual risks and unresolved review items.

At scale, passports should be shard-level by default, with document-level exception records. A verbose record per document is not required where it would make the estate operationally unmanageable.

### TROVE Release Manifest

Defines a content-addressed corpus release.

Required concepts:

- release identity and version;
- shard identities and aggregate digests;
- source-family and token accounting;
- mixture weights and sampling policy;
- provider manifests;
- qualification records;
- known limitations;
- admitted and prohibited uses;
- supersession and disposal relations.

## Identity model

Every material qualification must distinguish:

1. source or corpus identity;
2. curation-tooling identity;
3. qualification-tooling identity;
4. execution identity.

Model-assisted stages must additionally bind model weights, tokenizer, prompt or classifier contract, decoding/scoring parameters, and runtime versions. A fixed corpus processed by changed tooling is a distinct qualified object.

## Review tiers

### T0 — editorial or nonsemantic

Examples: prose correction, link repair, comments, formatting.

Required: ordinary review and applicable CI.

### T1 — deterministic transformation

Examples: parser change, normalization rule, metadata extraction.

Required: fixtures, deterministic replay, output-diff report, and non-author review.

### T2 — judgment or retention policy

Examples: PII detector, content filter, classifier, dedup threshold, representative-selection policy.

Required: adversarial fixtures, calibration or error analysis, subgroup accounting, reversal plan, and independent Referee review.

### T3 — corpus admission or high-impact policy

Examples: release admission, source-family exclusion, licensing interpretation, destructive deletion, major mixture decision.

Required: complete provider and qualification records, claim ledger, independent Adversary and Referee review, and Human Steward disposition for GCL-controlled releases.

## First fixture

**TC-FIXTURE-001 — HTML extraction baseline**

Pipeline:

```text
raw HTML
→ Trafilatura extraction
→ language identification
→ deterministic normalization
→ TROVE Source Record
→ CURATA Transformation Receipts
→ CURATA Passport
→ fixture report
```

Fixture classes:

- ordinary long-form article;
- navigation and boilerplate-heavy page;
- MathML/LaTeX/MathJax page;
- code-heavy page;
- multilingual page;
- malformed markup and encoding;
- explicit PII examples;
- duplicate and near-duplicate pair;
- content requiring a keep/remove decision.

Minimum acceptance criteria:

- schema-valid records;
- byte- and configuration-bound stage identities;
- no synthetic content insertion;
- preserved source-to-output traceability;
- explicit measurement of boilerplate residue;
- explicit math and code preservation report;
- explicit failures rather than silent admission;
- reproducible output under the pinned environment.

## Scientific evaluation boundary

CURATA-CERT answers whether a transformation behaved according to its declared contract. ALIGN evaluates whether the intervention improved downstream behavior.

Material interventions require matched comparisons where feasible, including rare-stratum retention and not merely aggregate validation loss. Candidate comparisons include:

- no fuzzy dedup versus MinHash/LSH threshold variants;
- source-local versus global deduplication;
- semantic cluster representative caps;
- quality-filter retention thresholds;
- generic versus STEM-preserving extraction;
- stripped versus markup-preserving wiki representations;
- PII redaction versus document removal.

## Handoff conditions

A collaborator implementation may claim conformance to this package only when it:

- explicitly opts in;
- publishes compatible record identities or a documented mapping;
- binds provider and execution versions;
- exposes fixture results and known failures;
- does not imply GCL certification from CI success;
- preserves collaborator authority over its repository and releases.

## Non-claims

This work package does not establish that any corpus is safe, private, legal, unbiased, factual, non-synthetic, contamination-free, high quality, optimal, or suitable for model training. It does not establish downstream performance improvement, novelty, priority, or commercial value.
