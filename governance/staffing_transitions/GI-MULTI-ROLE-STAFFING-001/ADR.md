# ADR: Organization-wide multi-role agent staffing

- Identifier: `GI-MULTI-ROLE-STAFFING-001`
- Status: candidate
- Effective policy version: `1.0.0` after protected schedule selection
- Decision authority: Human Steward under Constitution Articles X and XI

## Problem

The current schedule correctly minimizes human participation but treats agent
independence as multiplication of invocations and sessions. That creates
repeated routing and approval handling without proving that different audit
criteria were applied. Repository rules consequently conflict about whether
automation may integrate already-authorized work.

## Decision

Adopt constitutional amendment `GI-AMEND-0002` and implement it through
`GI-STEWARD-0003`. Separate functions through exact-subject, role-scoped,
read-only logical passes. Permit one system to staff multiple non-reserved roles
and autonomously complete routine and non-reserved substantive work through
protected controls. Retain one human decision only for reserved authority and
retain explicitly declared specialist outcome-independence rules.

## Alternatives

- Keep separate invocations for every review role: rejected because identity
  multiplication is costly and does not itself establish evidentiary diversity.
- Remove role separation entirely: rejected because adversarial, verification,
  formal, and judgment lenses remain necessary.
- Allow automation to exercise reserved human powers: rejected as contrary to
  Article X and the non-impersonation boundary.

## Compatibility and reversal

Existing evidence remains historically valid. Existing schemas may continue to
record invocation identifiers, but new records distinguish system identity from
logical pass identity. Revert only through a later exact directive if audit
quality degrades, an external binding rule requires organizational independence,
or the protected control plane cannot preserve exact-subject pass records.
