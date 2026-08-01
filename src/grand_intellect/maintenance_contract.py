from __future__ import annotations

from typing import Any, Mapping

ADOPTION_ID = "GI-ADMIN-MAINT-001"
PROGRAMME_CONTROL_ID = "MP-ADMIN-MAINT-001"
PROGRAMME_DECISION_ID = "MP-ADMIN-DECISION-001"
PROGRAMME_MIRROR_POLICY_ID = "MP-ADMIN-MIRROR-001"
PROGRAMME_REPOSITORY = "grandchallenge/MATH-PROGRAMME"
PROGRAMME_PULL_REQUEST = 184
INTELLECT_ISSUE = 21
ACCELERATION_FACTOR = 0.1

EXPECTED_DURATIONS = {
    "pilot_duration": "P9D",
    "structural_sweep": "PT16H48M",
    "administrative_review": "P3D",
    "deep_conformance_review": "P9D",
    "constitutional_review": "P36DT12H",
    "tracker_refresh": "PT7H12M",
    "ordinary_local_waiver_limit": "P3D",
    "emergency_override_limit": "PT7H12M",
    "emergency_steward_review": "PT2H24M",
    "emergency_retrospective": "PT16H48M",
    "unresolved_p1_limit": "PT16H48M",
}

REQUIRED_PROTECTED_ARTIFACTS = {
    "governance/administrative_maintenance_control.json",
    "governance/administrative_maintenance_council_decision.json",
    "governance/issue_mirror_enforcement_policy.json",
}

PHASE_A = "PHASE_A_COMMITTED_PENDING_PROTECTED_PIN"
PHASE_B = "PHASE_B_PROTECTED_ADOPTION_COMPLETE"


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 40 and all(ch in "0123456789abcdef" for ch in value)


def maintenance_adoption_errors(
    record: Mapping[str, Any],
    *,
    require_effective_protected_adoption: bool = False,
) -> list[str]:
    """Return fail-closed diagnostics for a Programme maintenance adoption record."""

    errors: list[str] = []
    if record.get("adoption_id") != ADOPTION_ID:
        errors.append("maintenance adoption identity drift")
    if record.get("programme_control_id") != PROGRAMME_CONTROL_ID:
        errors.append("maintenance control identity drift")
    if record.get("programme_decision_id") != PROGRAMME_DECISION_ID:
        errors.append("maintenance decision identity drift")
    if record.get("programme_mirror_policy_id") != PROGRAMME_MIRROR_POLICY_ID:
        errors.append("maintenance mirror policy identity drift")

    candidate = record.get("programme_candidate")
    if not isinstance(candidate, Mapping):
        errors.append("maintenance adoption requires Programme candidate context")
    else:
        if candidate.get("repository") != PROGRAMME_REPOSITORY:
            errors.append("maintenance Programme repository drift")
        if candidate.get("pull_request") != PROGRAMME_PULL_REQUEST:
            errors.append("maintenance Programme pull request drift")
        if candidate.get("candidate_can_create_authority") is not False:
            errors.append("candidate Programme reference cannot create authority")

    artifacts = record.get("required_protected_artifacts")
    if not isinstance(artifacts, list) or set(artifacts) != REQUIRED_PROTECTED_ARTIFACTS:
        errors.append("maintenance protected artifact set drift")

    semantics = record.get("accepted_semantics")
    if not isinstance(semantics, Mapping):
        errors.append("maintenance adoption requires accepted semantics")
    else:
        for field in (
            "protected_records_are_state_authority",
            "issues_are_navigation_only",
            "repository_head_is_distinct_from_material_artifact_identity",
            "unchanged_consumed_blobs_do_not_require_repin",
            "event_triggered_material_synchronization_is_immediate",
        ):
            if semantics.get(field) is not True:
                errors.append(f"maintenance semantic invariant failed: {field}")
        if semantics.get("acceleration_factor") != ACCELERATION_FACTOR:
            errors.append("maintenance acceleration factor drift")
        for field, expected in EXPECTED_DURATIONS.items():
            if semantics.get(field) != expected:
                errors.append(f"maintenance duration drift: {field}")

    fail_closed = record.get("fail_closed_requirements")
    if not isinstance(fail_closed, Mapping) or any(value is not True for value in fail_closed.values()):
        errors.append("maintenance fail-closed requirements incomplete")

    provider = record.get("provider_identity_disposition")
    if not isinstance(provider, Mapping) or provider.get("existing_mathematical_provider_identities_changed") is not False:
        errors.append("maintenance adoption must not repin unchanged mathematical providers")

    phase = record.get("phase")
    phase_b = record.get("phase_b_requirements")
    if not isinstance(phase_b, Mapping):
        errors.append("maintenance adoption requires Phase B identity fields")
        phase_b = {}

    if phase == PHASE_A:
        if record.get("effective") is not False:
            errors.append("Phase A maintenance adoption cannot be effective")
        if record.get("authority_status") != "CANDIDATE_COMMITMENT_NOT_PROTECTED_AUTHORITY":
            errors.append("Phase A maintenance adoption cannot claim protected authority")
        for field in (
            "exact_programme_merge_commit",
            "maintenance_control_blob",
            "decision_record_blob",
            "mirror_policy_blob",
        ):
            if phase_b.get(field) is not None:
                errors.append(f"Phase A maintenance adoption must not fabricate {field}")
    elif phase == PHASE_B:
        if record.get("effective") is not True:
            errors.append("Phase B maintenance adoption must be effective")
        if record.get("authority_status") != "PROTECTED_CONTENT_ADDRESSED_AUTHORITY":
            errors.append("Phase B maintenance adoption requires protected content-addressed authority")
        for field in (
            "exact_programme_merge_commit",
            "maintenance_control_blob",
            "decision_record_blob",
            "mirror_policy_blob",
        ):
            if not _is_sha(phase_b.get(field)):
                errors.append(f"Phase B maintenance adoption requires exact {field}")
    else:
        errors.append("maintenance adoption phase is invalid")

    if require_effective_protected_adoption and phase != PHASE_B:
        errors.append("protected Programme maintenance adoption is not complete")

    claims = record.get("claim_boundaries")
    if not isinstance(claims, Mapping) or any(value is not False for value in claims.values()):
        errors.append("maintenance adoption cannot promote mathematical or external claims")

    return errors


__all__ = [
    "ACCELERATION_FACTOR",
    "ADOPTION_ID",
    "EXPECTED_DURATIONS",
    "INTELLECT_ISSUE",
    "PHASE_A",
    "PHASE_B",
    "PROGRAMME_CONTROL_ID",
    "PROGRAMME_DECISION_ID",
    "PROGRAMME_MIRROR_POLICY_ID",
    "PROGRAMME_PULL_REQUEST",
    "PROGRAMME_REPOSITORY",
    "REQUIRED_PROTECTED_ARTIFACTS",
    "maintenance_adoption_errors",
]
