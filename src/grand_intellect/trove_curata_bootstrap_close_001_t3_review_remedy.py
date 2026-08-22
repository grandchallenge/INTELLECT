"""Fail-closed validation for the TC-BOOTSTRAP-CLOSE-001 T3 review remedy."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


EXPECTED_CHECKS = [
    {"name": "Analyze (actions)", "job_id": 94628521372, "conclusion": "success"},
    {"name": "Analyze (python)", "job_id": 94628521430, "conclusion": "success"},
    {"name": "CodeQL", "job_id": 94628623529, "conclusion": "success"},
    {"name": "policy / policy", "job_id": 94628523542, "conclusion": "success"},
    {"name": "security / action-policy", "job_id": 94628523449, "conclusion": "success"},
    {"name": "test (3.11.14)", "job_id": 94628524365, "conclusion": "success"},
    {"name": "test (3.12.13)", "job_id": 94628524463, "conclusion": "success"},
    {"name": "validate", "job_id": 94628522589, "conclusion": "success"},
]


class TroveCurataBootstrapCloseT3ReviewRemedyError(ValueError):
    """Raised when the historical defect or prospective remedy drifts."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TroveCurataBootstrapCloseT3ReviewRemedyError(message)


def exact_json_equal(actual: Any, expected: Any) -> bool:
    """Compare parsed JSON values using JSON Schema's value semantics."""
    if isinstance(actual, bool) or isinstance(expected, bool):
        return type(actual) is bool and type(expected) is bool and actual is expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return actual == expected
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, dict):
        return set(actual) == set(expected) and all(
            exact_json_equal(actual[key], expected[key]) for key in actual
        )
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(
            exact_json_equal(actual_item, expected_item)
            for actual_item, expected_item in zip(actual, expected, strict=True)
        )
    return actual == expected


def validate_trove_curata_bootstrap_close_t3_review_remedy(
    record: dict[str, Any],
) -> dict[str, Any]:
    require(
        set(record)
        == {
            "schema_version",
            "remedy_id",
            "status",
            "historical_subject",
            "declared_t3_gate",
            "observed_evidence",
            "defect",
            "remedy_contract",
            "authority_boundary",
            "claim_boundary",
        },
        "remedy field set drift",
    )
    require(record["schema_version"] == "0.1.0", "schema version drift")
    require(
        record["remedy_id"] == "TC-BOOTSTRAP-CLOSE-001-T3-REVIEW-REMEDY-001",
        "remedy identity drift",
    )
    require(
        record["status"]
        == "pending_exact_head_t3_review_steward_disposition_and_protected_merge",
        "remedy status drift",
    )

    require(
        exact_json_equal(
            record["historical_subject"],
            {
            "repository": "grandchallenge/INTELLECT",
            "issue_number": 68,
            "pull_request_number": 69,
            "author_account": "fyremael",
            "protected_predecessor": "8c3da17b2c401944e43b6e9bb0fae3bc95b05624",
            "final_merged_head": "d587996f71a38aeb8ce4a0c667da1a8350b7f153",
            "final_tree": "27539df4924775abf5a841b7591aaaa38223d672",
            "protected_merge_commit": "041f7d9b1c85e157a651bcf3edf07c7499185b00",
            "merged_at": "2026-08-14T00:37:36Z",
            "historical_t3_gate_satisfied": False,
            },
        ),
        "historical subject drift",
    )
    require(
        exact_json_equal(
            record["declared_t3_gate"],
            {
            "exact_head_checks_required": True,
            "non_author_agent_adversary_required": True,
            "distinct_session_non_author_agent_referee_required": True,
            "exact_head_human_steward_disposition_required": True,
            "protected_merge_required": True,
            },
        ),
        "declared T3 gate drift",
    )

    evidence = record["observed_evidence"]
    require(
        set(evidence)
        == {
            "exact_head_github_approval",
            "bound_non_author_adversary_finding",
            "bound_distinct_session_referee_finding",
            "bound_exact_head_human_steward_disposition",
            "required_check_runs",
            "workflow_success_is_t3_substitute",
            "mechanical_merge_is_t3_substitute",
        },
        "observed evidence field set drift",
    )
    require(
        exact_json_equal(
            evidence["exact_head_github_approval"],
            {
            "review_id": 4932733903,
            "reviewer": "jimsteeg",
            "commit_id": "d587996f71a38aeb8ce4a0c667da1a8350b7f153",
            "submitted_at": "2026-08-14T00:35:49Z",
            "state": "APPROVED",
            "is_t3_substitute": False,
            },
        ),
        "historical GitHub review drift",
    )
    for key in {
        "bound_non_author_adversary_finding",
        "bound_distinct_session_referee_finding",
        "bound_exact_head_human_steward_disposition",
    }:
        require(evidence[key] is None, "missing historical evidence relabelled")
    require(exact_json_equal(evidence["required_check_runs"], EXPECTED_CHECKS), "check evidence drift")
    require(evidence["workflow_success_is_t3_substitute"] is False, "workflow substituted for T3")
    require(evidence["mechanical_merge_is_t3_substitute"] is False, "merge substituted for T3")

    require(
        exact_json_equal(
            record["defect"],
            {
            "kind": "missing_bound_t3_role_and_steward_records",
            "historical_timeline_rewritten": False,
            "historical_review_relabelled": False,
            "historical_disposition_relabelled": False,
            "source_content_identity_disputed": False,
            "source_protected_merge_identity_disputed": False,
            },
        ),
        "defect characterization drift",
    )

    require(
        exact_json_equal(
            record["remedy_contract"],
            {
            "prospective_remediation_only": True,
            "historical_state_rewritten": False,
            "corrective_non_author_agent_adversary_required": True,
            "corrective_distinct_session_non_author_agent_referee_required": True,
            "corrective_exact_head_human_steward_disposition_required": True,
            "ordinary_human_steward": "fyremael",
            "recovery_owner": "jimsteeg",
            "mandatory_routine_human_reviewers": [],
            "github_approval_is_steward_authorization": False,
            "mechanical_merge_is_steward_authorization": False,
            "agent_may_merge_own_work": False,
            "protected_merge_required": True,
            "protected_main_readback_required": True,
            "destination_acceptance_blocked_until_remedy_protected_merge": True,
            },
        ),
        "remedy contract drift",
    )

    require(
        exact_json_equal(
            record["authority_boundary"],
            {
            "project_owner": "grandchallenge",
            "project_scope": "gcl_contained",
            "implementation_changed": False,
            "bootstrap_artifacts_changed": False,
            "destination_activated": False,
            "fixture_006_authorized": False,
            "aether_role": "future_projection_nonblocking",
            },
        ),
        "authority boundary drift",
    )
    require(
        exact_json_equal(
            record["claim_boundary"],
            {
            "corpus_admitted": False,
            "deletion_authorized": False,
            "privacy_compliance_proved": False,
            "legality_or_rights_proved": False,
            "dataset_quality_certified": False,
            "fitness_for_training_proved": False,
            "production_release_qualified": False,
            "public_release_authorized": False,
            "mathematics_certified": False,
            "commercial_claim_authorized": False,
            },
        ),
        "claim boundary drift or inflation",
    )
    return record


def load_and_validate_trove_curata_bootstrap_close_t3_review_remedy(
    path: str | Path,
) -> dict[str, Any]:
    record = json.loads(Path(path).read_text(encoding="utf-8"))
    require(isinstance(record, dict), "remedy root must be an object")
    return validate_trove_curata_bootstrap_close_t3_review_remedy(record)
