# GI-MC-WP00 — MATHCERT lifecycle alignment

## Identity

- INTELLECT issue: `grandchallenge/INTELLECT#6`
- Parent Programme audit: `grandchallenge/MATH-PROGRAMME#123`
- MATHCERT provider merge: `3854dd1b4f6e162a7e74c3da1993f022ee691e5e`
- MATHCERT route-registry Git blob: `065f0531e4d763b389b207d4922d5a85b4335ee3`
- MATHSOLVE provider merge: `cdb34f47829942bd89a3f7f754b412527eaafb92`
- MATH-PROGRAMME policy merge: `8182b8a5dc7b157d1a6b2a0f43d66c0598a2b072`
- MATH-PROGRAMME routing-registry Git blob: `39e907cce79137168e5b2a240674d7f4e6f56cdd`

## Constitutional correction

The runtime now separates four facts.

1. A handoff record exists.
2. A content-addressed MATHSOLVE packet is ready.
3. MATHCERT has acknowledged intake.
4. MATHCERT has issued a content-addressed disposition.

The state classes are:

- `pending`: no complete packet is required;
- `ready`: a MATHSOLVE packet exists, but MATHCERT has not acknowledged intake;
- `submitted`: MATHCERT has acknowledged the packet, but has not adjudicated it;
- `certified`, `qualified`, `rejected`, `proof_debt`: MATHCERT has issued an adjudication.

Only `certified` and `qualified` can support an `accept` or `combine` judgment. `rejected` and `proof_debt` close lineage but block positive promotion.

## Artifact requirements

A ready or later state requires the exact MATHSOLVE packet repository, commit, path, digest algorithm, and digest.

A submitted or adjudicated state requires an explicit MATHCERT intake acknowledgement.

An adjudicated state also requires the exact MATHCERT output repository, commit, path, digest algorithm, and digest.

The runtime forbids a ready or submitted state from carrying a Cert adjudication output. It also forbids an adjudicated state without a packet, intake acknowledgement, or Cert output.

## Provider authority

Every governed route and reviewed exemption carries the exact Programme policy artifact and MATHCERT route-registry artifact. A waiver cannot remove the Cert handoff obligation.

GitHub remains present authority. The AETHER file is a future semantic projection. It does not claim that an AETHER namespace is deployed or authoritative.

## Adversarial coverage

The tests reject:

- ready without a packet identity;
- submitted without intake acknowledgement;
- adjudication without a MATHCERT output identity;
- pending, ready, or submitted at Judgment or Integration;
- rejected or proof-debt evidence used for positive promotion;
- a missing handoff at Integration;
- drift in the pinned Programme or MATHCERT contract identity.

## Claim boundary

This package corrects constitutional routing and lifecycle semantics. It certifies no mathematical claim. A packet, intake acknowledgement, repository merge, or green governance workflow is not mathematical certification.
