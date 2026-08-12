from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .council_review import GRAND_ASSEMBLY_OFFICES, canonical_sha256
from .model import Office


AFFIRMATIVE_DISPOSITION = "adopt_fifteen_office_terminal_gate"
ALLOWED_DISPOSITIONS = frozenset({AFFIRMATIVE_DISPOSITION, "reject", "abstain"})


@dataclass(frozen=True, slots=True)
class GrandAssemblyAssessment:
    matter_id: str
    motion_sha256: str
    full_quorum: bool
    unanimous: bool
    office_dispositions: dict[str, str]
    review_sha256: dict[str, str]
    procedural_disposition: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "matter_id": self.matter_id,
            "motion_sha256": self.motion_sha256,
            "required_office_count": 15,
            "full_quorum": self.full_quorum,
            "unanimous": self.unanimous,
            "office_dispositions": self.office_dispositions,
            "review_sha256": self.review_sha256,
            "procedural_disposition": self.procedural_disposition,
            "current_rules_remain_effective": True,
            "authority_boundary": (
                "This compilation records fifteen-office Grand assembly procedure. "
                "It does not create Human Steward authorization, proxy authority, "
                "merge authority, activation, ratification, or certification."
            ),
        }


def validate_motion(value: Mapping[str, Any]) -> None:
    required = {
        "schema_version", "matter_id", "title", "status", "proposal_path",
        "proposal_sha256", "passage_rule", "required_offices",
        "affirmative_disposition", "allowed_dispositions", "authority",
        "review_directory", "disposition_path",
    }
    missing = sorted(required - value.keys())
    if missing:
        raise ValueError(f"Grand assembly motion missing fields: {', '.join(missing)}")
    if value["schema_version"] != "1.0":
        raise ValueError("unsupported Grand assembly motion schema_version")
    if value["passage_rule"] != "fifteen_office_full_quorum_unanimous_consent":
        raise ValueError("Grand assembly motion must require fifteen-office unanimity")
    expected = [office.value for office in GRAND_ASSEMBLY_OFFICES]
    if value["required_offices"] != expected:
        raise ValueError("Grand assembly motion must require all five Minders and ten Council offices")
    if value["affirmative_disposition"] != AFFIRMATIVE_DISPOSITION:
        raise ValueError("Grand assembly affirmative disposition differs from contract")
    if set(value["allowed_dispositions"]) != ALLOWED_DISPOSITIONS:
        raise ValueError("Grand assembly disposition vocabulary differs from contract")
    authority = value["authority"]
    required_authority = {
        "effect": "prospective_terminal_review_gate_only",
        "prior_ten_office_records_remain_valid": True,
        "current_rules_remain_effective": True,
        "human_steward_action_required": True,
        "automation_may_activate": False,
    }
    if not isinstance(authority, Mapping):
        raise ValueError("Grand assembly authority must be an object")
    for key, expected_value in required_authority.items():
        if authority.get(key) != expected_value:
            raise ValueError(f"Grand assembly authority boundary invalid: {key}")


def validate_review(review: Mapping[str, Any], *, matter_id: str, motion_sha256: str) -> None:
    required = {
        "schema_version", "matter_id", "motion_sha256", "office", "reviewer_id", "session_id",
        "disposition", "deliberation", "discharged_obligations", "findings",
        "amendments", "residual_uncertainty", "evidence_refs",
    }
    missing = sorted(required - review.keys())
    if missing:
        raise ValueError(f"Grand assembly review missing fields: {', '.join(missing)}")
    if review["schema_version"] != "1.0":
        raise ValueError("unsupported Grand assembly review schema_version")
    if review["matter_id"] != matter_id or review["motion_sha256"] != motion_sha256:
        raise ValueError("Grand assembly review is stale or bound to another matter")
    try:
        office = Office(str(review["office"]))
    except ValueError as exc:
        raise ValueError("Grand assembly review office is unknown") from exc
    if office not in GRAND_ASSEMBLY_OFFICES:
        raise ValueError("Grand assembly review office is not a required office")
    if review["disposition"] not in ALLOWED_DISPOSITIONS:
        raise ValueError("Grand assembly review disposition is invalid")
    for field in ("reviewer_id", "session_id", "deliberation"):
        if not isinstance(review[field], str) or not review[field].strip():
            raise ValueError(f"Grand assembly review {field} must be non-empty")
    for field in ("discharged_obligations", "findings", "amendments", "residual_uncertainty", "evidence_refs"):
        if not isinstance(review[field], list) or any(not isinstance(item, str) or not item.strip() for item in review[field]):
            raise ValueError(f"Grand assembly review {field} must be a string array")
    if not review["discharged_obligations"]:
        raise ValueError("Grand assembly review must discharge an office obligation")


def assess_motion(motion: Mapping[str, Any], reviews: Sequence[Mapping[str, Any]]) -> GrandAssemblyAssessment:
    validate_motion(motion)
    digest = canonical_sha256(motion)
    by_office: dict[str, Mapping[str, Any]] = {}
    reviewer_ids: set[str] = set()
    session_ids: set[str] = set()
    for review in reviews:
        validate_review(review, matter_id=str(motion["matter_id"]), motion_sha256=digest)
        office = str(review["office"])
        reviewer_id = str(review["reviewer_id"])
        session_id = str(review["session_id"])
        if office in by_office:
            raise ValueError(f"duplicate Grand assembly review for {office}")
        if reviewer_id in reviewer_ids:
            raise ValueError("one reviewer identity may not occupy two Grand assembly offices")
        if session_id in session_ids:
            raise ValueError("one session identity may not occupy two Grand assembly offices")
        by_office[office] = review
        reviewer_ids.add(reviewer_id)
        session_ids.add(session_id)
    missing = [office.value for office in GRAND_ASSEMBLY_OFFICES if office.value not in by_office]
    if missing:
        raise ValueError(f"missing Grand assembly reviews: {', '.join(missing)}")
    dispositions = {office: str(review["disposition"]) for office, review in by_office.items()}
    unique = set(dispositions.values())
    unanimous = len(unique) == 1
    procedural = AFFIRMATIVE_DISPOSITION if unanimous and next(iter(unique)) == AFFIRMATIVE_DISPOSITION else "no_unanimous_disposition"
    return GrandAssemblyAssessment(
        matter_id=str(motion["matter_id"]), motion_sha256=digest, full_quorum=True,
        unanimous=unanimous, office_dispositions=dispositions,
        review_sha256={office: canonical_sha256(review) for office, review in by_office.items()},
        procedural_disposition=procedural,
    )


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def compile_motion(motion_path: Path, review_dir: Path) -> GrandAssemblyAssessment:
    motion = _read_object(motion_path)
    proposal_path = motion_path.parents[3] / str(motion.get("proposal_path", ""))
    if not proposal_path.is_file():
        raise ValueError("Grand assembly proposal_path does not resolve to a file")
    if hashlib.sha256(proposal_path.read_bytes()).hexdigest() != motion.get("proposal_sha256"):
        raise ValueError("Grand assembly proposal digest does not match proposal content")
    return assess_motion(motion, [_read_object(path) for path in sorted(review_dir.glob("*.json"))])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile a fifteen-office unanimous Grand assembly motion")
    parser.add_argument("motion", type=Path)
    parser.add_argument("reviews", type=Path)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(compile_motion(args.motion, args.reviews).to_dict(), indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
