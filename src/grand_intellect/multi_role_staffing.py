from __future__ import annotations

from collections.abc import Mapping, Sequence


class MultiRoleReviewError(ValueError):
    """Raised when a multi-role review set violates functional separation."""


def validate_review_set(reviews: Sequence[Mapping[str, object]]) -> None:
    pass_ids: set[str] = set()
    analyses: set[tuple[str, ...]] = set()
    required = {
        "schema_version", "work_class", "effects", "reviewer_system_id",
        "logical_pass_id", "role", "mode", "subject", "criteria", "finding",
        "evidence", "unresolved_obligations", "reserved_authority_ref",
        "authority_claims",
    }
    reserved_effects = {
        "human_authority", "math_certification", "destructive_disposal",
        "safety_critical", "credential_expansion", "public_commitment",
        "irreversible_resource", "production_semantic", "corpus_admission",
    }
    substantive_effects = {"public_contract", "authority_boundary", "material_result"}
    for review in reviews:
        if set(review) != required:
            raise MultiRoleReviewError("review fields do not match the closed contract")
        pass_id = review.get("logical_pass_id")
        if not isinstance(pass_id, str) or not pass_id or pass_id in pass_ids:
            raise MultiRoleReviewError("logical audit pass identifiers must be unique")
        pass_ids.add(pass_id)
        role = review.get("role")
        mode = review.get("mode")
        if role in {"Adversary", "Referee"} and mode != "non_authoring_read_only":
            raise MultiRoleReviewError(f"{role} must use non_authoring_read_only mode")
        work_class = review.get("work_class")
        effects = set(review.get("effects", []))
        if effects & reserved_effects and work_class != "reserved":
            raise MultiRoleReviewError("reserved effect cannot be classification-downgraded")
        if effects & substantive_effects and work_class == "routine_bounded":
            raise MultiRoleReviewError("substantive effect cannot be routine-classified")
        reserved_ref = review.get("reserved_authority_ref")
        if work_class == "reserved" and not reserved_ref:
            raise MultiRoleReviewError("reserved work requires exact human authority")
        if work_class != "reserved" and reserved_ref is not None:
            raise MultiRoleReviewError("non-reserved work cannot claim reserved authority")
        if review.get("finding") == "approved" and review.get("unresolved_obligations"):
            raise MultiRoleReviewError("approved review retains unresolved obligations")
        claims = review.get("authority_claims")
        if not isinstance(claims, Mapping) or any(claims.values()):
            raise MultiRoleReviewError("review evidence cannot manufacture authority or certification")
        analysis = tuple(
            sorted(str(item) for item in review.get("criteria", []))
            + sorted(str(item) for item in review.get("evidence", []))
            + [str(review.get("finding"))]
        )
        if analysis in analyses:
            raise MultiRoleReviewError("duplicated analysis does not create a distinct audit pass")
        analyses.add(analysis)

    subjects = {
        (
            str(review.get("subject", {}).get("commit")),
            str(review.get("subject", {}).get("tree")),
            str(review.get("subject", {}).get("base_commit")),
            str(review.get("subject", {}).get("dependency_closure_sha256")),
            str(review.get("subject", {}).get("material_evidence_sha256")),
        )
        for review in reviews
        if isinstance(review.get("subject"), Mapping)
    }
    if len(subjects) > 1:
        raise MultiRoleReviewError("material subject or evidence drift invalidates review set")
