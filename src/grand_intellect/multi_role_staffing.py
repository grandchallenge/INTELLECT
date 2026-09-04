from __future__ import annotations

from collections.abc import Mapping, Sequence


class MultiRoleReviewError(ValueError):
    """Raised when a multi-role review set violates functional separation."""


def validate_review_set(reviews: Sequence[Mapping[str, object]]) -> None:
    pass_ids: set[str] = set()
    for review in reviews:
        pass_id = review.get("logical_pass_id")
        if not isinstance(pass_id, str) or not pass_id or pass_id in pass_ids:
            raise MultiRoleReviewError("logical audit pass identifiers must be unique")
        pass_ids.add(pass_id)
        role = review.get("role")
        mode = review.get("mode")
        if role in {"Adversary", "Referee"} and mode != "non_authoring_read_only":
            raise MultiRoleReviewError(f"{role} must use non_authoring_read_only mode")
        work_class = review.get("work_class")
        reserved_ref = review.get("reserved_authority_ref")
        if work_class == "reserved" and not reserved_ref:
            raise MultiRoleReviewError("reserved work requires exact human authority")
        if work_class != "reserved" and reserved_ref is not None:
            raise MultiRoleReviewError("non-reserved work cannot claim reserved authority")
        if review.get("finding") == "approved" and review.get("unresolved_obligations"):
            raise MultiRoleReviewError("approved review retains unresolved obligations")

    subjects = {
        (
            str(review.get("subject", {}).get("commit")),
            str(review.get("subject", {}).get("tree")),
            str(review.get("subject", {}).get("material_evidence_sha256")),
        )
        for review in reviews
        if isinstance(review.get("subject"), Mapping)
    }
    if len(subjects) > 1:
        raise MultiRoleReviewError("material subject or evidence drift invalidates review set")
