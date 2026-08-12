# GI-COUNCIL-OPERATING-BURDEN-002: enforce minimum routine burden

**Status:** Before the Council for operating-policy review

**Decision class:** enforcement of effective staffing and workflow impact policy

**Authority boundary:** Council recommendation; current constitutional,
Human Steward, AETHER, and MATHCERT authority remains unchanged

## Question presented

Should GCL immediately correct routine review routing that treats recovery owner
`jimsteeg` as a required reviewer, and replace unconditional expensive
post-merge test fanout with impact-gated replay plus lightweight readback?

## Effective authority

`GI-STEWARD-0002` already makes `fyremael` the ordinary Human Steward,
`jimsteeg` the recovery owner, and the Human Steward's exact-packet action the
sole ordinary human action for a governed decision. The protected authority
schedule records no mandatory routine reviewers and a target of one human
action. This matter neither amends that directive nor creates a new delegation.

The live INTELLECT and MATH-PROGRAMME main rulesets require zero approving
reviews and name no required reviewer. A routine `jimsteeg` request is therefore
routing drift, not an authority gate. Historical records that accurately name
`jimsteeg` remain immutable evidence.

## Observed operating defect

Current high-velocity work nevertheless requests `jimsteeg` approval on routine
pull requests before the separate Human Steward action. GitHub search returned
at least 100 merged, `jimsteeg`-reviewed GCL pull requests from 2026-08-05
through 2026-08-12, 85 of them in MATH-PROGRAMME.

MATH-PROGRAMME also launches twelve standalone CMDG workflows on every push to
`main`, although the same workflows already use a governed dependency closure
for pull requests. Each lane permits up to twenty minutes. Merge `4f5adc7`
launched fifteen direct push workflows and a deterministic downstream cascade.
Its Programme policy run took 15 minutes 56 seconds because a known visual
rendering tool was classified as unknown, expanding the transition to all seven
policy shards and all three formal replay lanes.

INTELLECT's ordinary post-merge CI completed in under two minutes in the sampled
runs. The remediation therefore targets the evidenced MATH-PROGRAMME fanout and
cross-programme review-routing drift; it does not abolish relevant verification.

## Council disposition requested

Recommend the following Stage 1 correction under current authority:

1. **Zero routine recovery-owner actions.** A routine reviewer request,
   CODEOWNER entry, campaign record, or operator instruction that names
   `jimsteeg` as required is invalid unless it binds an exact recovery operation
   admitted by `GI-STEWARD-0002`. Optional review remains permitted only when
   separately named and must not become a merge prerequisite.
2. **One reserved human action at most.** Where Human Steward authority is
   required, route one exact packet to `fyremael`. Ordinary non-reserved work
   requires no synthetic Human Steward action. A platform approval, merge
   click, automated check, or Council record cannot manufacture that action.
3. **Impact-gated post-merge replay.** Expensive standalone suites run after a
   merge only when the exact merge transition intersects their versioned
   dependency closure. Relevant merges retain full replay. Unrelated merges do
   not instantiate those suites.
4. **Bounded exact-SHA readback.** Every protected merge retains immediate,
   asynchronous identity and required-state readback. Failed, unknown, stale,
   or reserved/control-plane results place a hold on downstream effect and
   route a compensating proposal; they do not erase the merge or create
   authority.
5. **Recovery without polling pressure.** Manual dispatch and scheduled drift
   detection remain available. High-frequency recovery polling and duplicate
   event consumers must be consolidated by the active governance-rework
   committee into event-driven dispatch plus one daily recovery sweep.
6. **Classifier precision.** Known governed paths must map to their declared
   shards. Unknown paths continue to fail closed; classification precision may
   not weaken required checks or formal proof closure.
7. **Regression evidence.** Validators must reject routine `jimsteeg`
   dependencies, push/PR path-closure divergence, relevant-merge suppression,
   authority expansion, and loss of manual or scheduled recovery.

## Acceptance criteria

- routine mandatory `jimsteeg` actions: `0`;
- Human Steward actions per governed decision: `<= 1`;
- unrelated merges launching standalone CMDG lanes: `0`;
- relevant merges launching the full declared CMDG family: `100%`;
- manual dispatch and scheduled recovery retained;
- no required check removed or renamed;
- no automatic approval, ratification, activation, certification, promotion, or
  Human Steward impersonation;
- median post-merge workflow fanout and elapsed time reduced by at least 70%
  for the sampled unrelated-merge class before broader rollout; and
- all failures, unknowns, and residual exceptions retained as evidence.

## Relationship to pending proxy work

This is the narrow Stage 1 successor to `GI-COUNCIL-POSTMERGE-001`, whose broad
merge-capable proposal was returned for revision. It does not approve the
pending proxy-delegation motions, replace required human judgment, or satisfy
the proxy committee's fifteen-office terminal gate. That committee retains the
separate task of designing any future machine proxy or automated integration
authority.

## Evidence considered

- `governance/steward_directives/GI-STEWARD-0002.md`;
- `governance/constitutional_authority_schedule.json`;
- `governance/council_matters/GI-COUNCIL-POSTMERGE-001/disposition.json`;
- `governance/committees/GI-PROXY-DELEGATION-COMMITTEE-001.md`;
- live INTELLECT ruleset `19964077` and MATH-PROGRAMME ruleset `17137629`;
- INTELLECT PR #57 and PR #60 review records;
- MATH-PROGRAMME protected merge `4f5adc7` and workflow run `31596587540`;
- MATH-PROGRAMME `governance/cmdg_workflow_impact_gating.json`; and
- MATH-PROGRAMME workflow and policy-impact validators.
