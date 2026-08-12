from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .model import Office


COUNCIL_OFFICES: tuple[Office, ...] = (
    Office.AXIOMATIST,
    Office.CARTOGRAPHER,
    Office.VERIFIER,
    Office.ADVERSARY,
    Office.FORMALIST,
    Office.STEWARD,
    Office.GRAMMARIAN,
    Office.COMPOSER,
    Office.AMANUENSIS,
    Office.REFEREE,
)

MINDER_OFFICES: tuple[Office, ...] = (
    Office.POSSIBILITY_MINDER,
    Office.REALITY_MINDER,
    Office.PURPOSE_MINDER,
    Office.CONTINUITY_MINDER,
    Office.CAPACITY_MINDER,
)

GRAND_ASSEMBLY_OFFICES: tuple[Office, ...] = MINDER_OFFICES + COUNCIL_OFFICES

ALLOWED_DECISIONS = frozenset(
    {
        "approve",
        "approve_with_conditions",
        "changes_requested",
        "reject",
        "abstain",
    }
)


@dataclass(frozen=True, slots=True)
class CouncilAssessment:
    matter_id: str
    matter_sha256: str
    review_count: int
    office_decisions: dict[str, str]
    review_sha256: dict[str, str]
    procedural_disposition: str
    ready_for_human_disposition: bool
    conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "matter_id": self.matter_id,
            "matter_sha256": self.matter_sha256,
            "review_count": self.review_count,
            "office_decisions": self.office_decisions,
            "review_sha256": self.review_sha256,
            "procedural_disposition": self.procedural_disposition,
            "ready_for_human_disposition": self.ready_for_human_disposition,
            "conditions": list(self.conditions),
            "authority_boundary": (
                "This compilation validates and summarizes Council records. "
                "It does not approve, merge, activate, ratify, or certify."
            ),
        }


def canonical_sha256(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_matter(value: Mapping[str, Any]) -> None:
    required = {
        "schema_version",
        "matter_id",
        "title",
        "status",
        "decision_class",
        "proposal_path",
        "proposal_sha256",
        "authority",
        "required_offices",
        "allowed_decisions",
        "review_directory",
        "disposition_path",
    }
    missing = sorted(required - value.keys())
    if missing:
        raise ValueError(f"matter missing required fields: {', '.join(missing)}")
    if value["schema_version"] != "1.0":
        raise ValueError("unsupported matter schema_version")
    proposal_sha256 = value["proposal_sha256"]
    if not isinstance(proposal_sha256, str) or len(proposal_sha256) != 64:
        raise ValueError("matter proposal_sha256 must be a SHA-256 digest")
    required_offices = tuple(str(item) for item in value["required_offices"])
    expected = tuple(office.value for office in COUNCIL_OFFICES)
    if required_offices != expected:
        raise ValueError("matter must require each Council office exactly once")
    if set(value["allowed_decisions"]) != ALLOWED_DECISIONS:
        raise ValueError("matter decision vocabulary differs from Council contract")
    authority = value["authority"]
    if not isinstance(authority, Mapping):
        raise ValueError("matter authority must be an object")
    if authority.get("reserved_disposition") != "human_steward":
        raise ValueError("Human Steward disposition must remain reserved")
    if authority.get("automation_may_activate") is not False:
        raise ValueError("Council automation may not activate the matter")
    if authority.get("automation_may_certify_mathematics") is not False:
        raise ValueError("Council automation may not certify mathematics")


def validate_review(
    review: Mapping[str, Any], *, matter_id: str, matter_sha256: str
) -> None:
    required = {
        "schema_version",
        "matter_id",
        "matter_sha256",
        "office",
        "reviewer_id",
        "decision",
        "deliberation",
        "discharged_obligations",
        "findings",
        "conditions",
        "residual_uncertainty",
        "evidence_refs",
    }
    missing = sorted(required - review.keys())
    if missing:
        raise ValueError(f"review missing required fields: {', '.join(missing)}")
    if review["schema_version"] != "1.0":
        raise ValueError("unsupported review schema_version")
    if review["matter_id"] != matter_id:
        raise ValueError("review is bound to another matter")
    if review["matter_sha256"] != matter_sha256:
        raise ValueError("review is stale for the current matter")
    try:
        office = Office(str(review["office"]))
    except ValueError as exc:
        raise ValueError("review office is unknown") from exc
    if office not in COUNCIL_OFFICES:
        raise ValueError("review office is not a Council office")
    if review["decision"] not in ALLOWED_DECISIONS:
        raise ValueError("review decision is invalid")
    for field in ("reviewer_id", "deliberation"):
        if not isinstance(review[field], str) or not review[field].strip():
            raise ValueError(f"review {field} must be non-empty")
    for field in (
        "discharged_obligations",
        "findings",
        "conditions",
        "residual_uncertainty",
        "evidence_refs",
    ):
        if not isinstance(review[field], list) or any(
            not isinstance(item, str) or not item.strip() for item in review[field]
        ):
            raise ValueError(f"review {field} must be a string array")
    if not review["discharged_obligations"]:
        raise ValueError("review must discharge at least one office obligation")
    if review["decision"] == "approve_with_conditions" and not review["conditions"]:
        raise ValueError("conditional approval must state conditions")


def assess_council(
    matter: Mapping[str, Any], reviews: Sequence[Mapping[str, Any]]
) -> CouncilAssessment:
    validate_matter(matter)
    matter_sha256 = canonical_sha256(matter)
    by_office: dict[str, Mapping[str, Any]] = {}
    reviewers: set[str] = set()
    for review in reviews:
        validate_review(
            review,
            matter_id=str(matter["matter_id"]),
            matter_sha256=matter_sha256,
        )
        office = str(review["office"])
        reviewer_id = str(review["reviewer_id"])
        if office in by_office:
            raise ValueError(f"duplicate Council review for {office}")
        if reviewer_id in reviewers:
            raise ValueError("one reviewer identity may not occupy two Council offices")
        by_office[office] = review
        reviewers.add(reviewer_id)
    missing = [
        office.value for office in COUNCIL_OFFICES if office.value not in by_office
    ]
    if missing:
        raise ValueError(f"missing Council reviews: {', '.join(missing)}")

    decisions = {office: str(review["decision"]) for office, review in by_office.items()}
    review_sha256 = {
        office: canonical_sha256(review) for office, review in by_office.items()
    }
    values = set(decisions.values())
    if "reject" in values:
        procedural = "returned_rejected"
    elif "changes_requested" in values:
        procedural = "returned_for_revision"
    elif "abstain" in values:
        procedural = "incomplete"
    elif "approve_with_conditions" in values:
        procedural = "ready_with_conditions"
    else:
        procedural = "ready"
    # The Referee controls closure under Article II. Preserve every office's
    # decision and digest above, but use the Referee's reconciled conditions in
    # the compiled disposition instead of silently unioning conflicting advice.
    conditions = tuple(str(item) for item in by_office[Office.REFEREE.value]["conditions"])
    return CouncilAssessment(
        matter_id=str(matter["matter_id"]),
        matter_sha256=matter_sha256,
        review_count=len(by_office),
        office_decisions=decisions,
        review_sha256=review_sha256,
        procedural_disposition=procedural,
        ready_for_human_disposition=procedural in {"ready", "ready_with_conditions"},
        conditions=conditions,
    )


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def compile_docket(matter_path: Path, review_dir: Path) -> CouncilAssessment:
    matter = _read_object(matter_path)
    proposal_path = matter_path.parents[3] / str(matter.get("proposal_path", ""))
    if not proposal_path.is_file():
        raise ValueError("matter proposal_path does not resolve to a file")
    proposal_sha256 = hashlib.sha256(proposal_path.read_bytes()).hexdigest()
    if proposal_sha256 != matter.get("proposal_sha256"):
        raise ValueError("matter proposal digest does not match proposal content")
    reviews = [_read_object(path) for path in sorted(review_dir.glob("*.json"))]
    return assess_council(matter, reviews)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and compile a complete INTELLECT Council docket"
    )
    parser.add_argument("matter", type=Path)
    parser.add_argument("reviews", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        assessment = compile_docket(args.matter, args.reviews)
        encoded = json.dumps(assessment.to_dict(), indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(encoded, encoding="utf-8")
        else:
            print(encoded, end="")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
