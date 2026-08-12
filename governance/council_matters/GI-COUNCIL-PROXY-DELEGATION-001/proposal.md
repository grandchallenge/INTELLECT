# GI-COUNCIL-PROXY-DELEGATION-001: machine proxy delegation

**Status:** Before the full Council

**Decision class:** constitutional staffing and operating-policy referral

**Passage rule:** full quorum and unanimous consent

**Authority boundary:** Council recommendation only; existing law remains effective until the required Human Steward and Article XI actions occur

## Questions presented

1. May a named independent-human operator create a bounded delegation under
   which a registered machine proxy performs approved tasks on that operator's
   behalf without impersonating the operator or manufacturing a human act?
2. May routine approvals outside the control plane cease to require
   independent-human operator review when declared agent-office review,
   deterministic policy checks, and attributed proxy execution provide the
   required separation and evidence?

## Motion A: bounded machine proxy delegates

The Council recommends creation of a `machine_proxy_delegate` role with these
properties:

- every delegation names the human principal, proxy identity, exact task
  classes, repositories, paths, operations, limits, expiry, revocation route,
  and evidence obligations;
- every proxy act is recorded as a machine act performed under a delegation;
  it is never represented as the human principal's login, signature, review,
  presence, or contemporaneous judgment;
- a proxy may execute only a task already approved by effective policy or by a
  separately valid authorization whose scope includes that task;
- the proxy cannot delegate further, widen its scope, approve its own work,
  resolve a disputed finding, or convert operational success into authority;
- credentials are short-lived and restricted to the exact repository, branch,
  operation, and duration required; and
- the human principal or authorized control-plane office may revoke the
  delegation prospectively in one authenticated action without erasing prior
  evidence.

## Motion B: routine non-control-plane approvals

The Council recommends a governed classification under which a routine
execution-plane task may be approved by the required non-author agent offices
and executed by an attributed machine proxy without independent-human operator
review when all of the following are true:

- the task class and acceptance policy were previously approved through the
  applicable human-authority process;
- the task is deterministic, reversible or compensable, bounded in cost and
  blast radius, and contains no unresolved judgment or material exception;
- exact inputs, policy version, checks, office decisions, proxy identity,
  output, integration result, and readback are recorded;
- the actor that authored or generated the change is not its sole reviewer;
- any ambiguity, policy drift, hold, changes request, failed check, unknown
  state, or classification dispute routes to a human operator; and
- sampling, incident triggers, and periodic review can return a task class to
  human review.

Routine status must never be inferred merely from file path, PR label, actor,
repository, prior success, or low apparent effort.

## Control-plane exclusion

Proxy substitution for required human review is prohibited for:

- constitutions, amendments, authority schedules, office powers, staffing
  authority, or autonomous permission escalation;
- credentials, secrets, identity, organization membership, repository
  administration, branch protections, rulesets, CODEOWNERS, required-check
  policy, protected workflows, or proxy-delegation policy itself;
- destructive or irreversible acts, safety-critical deployment, public
  commitments, major resource commitments, or exception/waiver grants;
- activation, ratification, claim promotion, release promotion, or any act
  whose protected integration supplies institutional effect;
- AETHER production semantic authority, operational truth, append order,
  replay authority, or provenance-bearing facts; and
- MATHCERT mathematical certification or any mathematical claim disposition.

An unknown, mixed, or disputed classification is control-plane by default.

## Motion disposition

Each Council office must choose exactly one disposition:

- `table_for_human_steward_disposition`: endorse both motions as a policy
  direction and send them to the required constitutional and Human Steward
  process;
- `convene_governance_rework_committee`: refer both motions to a temporary
  committee to produce the missing constitutional, policy, schema, threat,
  migration, test, and pilot package;
- `reject`; or
- `abstain`.

No motion passes, and no committee is convened, unless all ten Council offices
participate and choose the same affirmative disposition. A split decision,
rejection, abstention, missing office, duplicate reviewer identity, or stale
record yields `no_unanimous_disposition` and preserves the current rules.

## Committee mandate if unanimously selected

The temporary Governance Proxy Delegation Committee shall include at least the
Axiomatist, Verifier, Adversary, Formalist, Steward, Grammarian, Amanuensis, and
Referee offices. It must produce:

1. an Article XI-compatible amendment and operating-policy package;
2. normative task, control-plane, delegation, proxy-act, revocation, hold,
   exception, incident, and readback schemas;
3. a closed initial task-class allowlist and explicit denied-capability list;
4. authentication, credential, independence, replay, race, custody, retention,
   recovery, and audit controls;
5. migration and grandfathering rules;
6. adversarial tests and a shadow-mode pilot with predeclared thresholds; and
7. an exact packet for renewed full-Council review and separate Human Steward
   disposition.

The committee may draft and test but may not approve, merge, activate,
ratify, certify, or exercise Human Steward authority.
