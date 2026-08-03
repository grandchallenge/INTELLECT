from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping


class ConstitutionalAuthorityError(ValueError):
    """Raised when an authority schedule would create an unlawful authority."""


_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
_DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_RECEIPT_RECORD_REF = "governance/reviews/GI-AMEND-0001.json"
_EXPECTED_CAMPAIGN_ID = "GI-AMEND-0001"
_EXPECTED_REVIEW_SUBJECTS = {
    "grandchallenge/INTELLECT": 32,
    "grandchallenge/gcl-standards": 18,
}
_REQUIRED_AETHER_POWERS = {
    "append_order",
    "semantic_cuts",
    "replay",
    "policy_visibility",
    "provenance_bearing_facts",
    "recursive_derivation",
    "proof_traces",
}
_FORBIDDEN_GITHUB_POWERS = {
    "constitutional_amendment",
    "mathematical_certification",
    "production_semantic_authority",
}
_REQUIRED_REVIEW_OFFICES = {"adversary", "referee", "human_steward"}
_AGENT_STAFFED_OFFICES = {
    "possibility_minder",
    "reality_minder",
    "purpose_minder",
    "continuity_minder",
    "capacity_minder",
    "axiomatist",
    "cartographer",
    "verifier",
    "adversary",
    "formalist",
    "steward",
    "grammarian",
    "composer",
    "amanuensis",
    "referee",
    "executor",
}


def validate_authority_schedule(
    schedule: Mapping[str, Any],
    *,
    review_receipt: Mapping[str, Any] | None = None,
) -> None:
    """Fail closed if a constitutional authority schedule crosses a boundary."""

    if schedule.get("schema_version") != "1.3.0":
        raise ConstitutionalAuthorityError("unsupported authority schedule version")
    if schedule.get("status") not in {"proposed", "active", "superseded"}:
        raise ConstitutionalAuthorityError("invalid authority schedule status")

    staffing = _mapping(schedule, "staffing")
    if (
        staffing.get("mode") != "steward_supervised_agents"
        or staffing.get("external_human_review_required") is not False
    ):
        raise ConstitutionalAuthorityError(
            "bootstrap staffing must use Steward-supervised agents"
        )
    directive = _mapping(staffing, "directive")
    if (
        directive.get("identifier") != "GI-STEWARD-0001"
        or directive.get("path")
        != "governance/steward_directives/GI-STEWARD-0001.md"
        or directive.get("status") != "effective"
    ):
        raise ConstitutionalAuthorityError(
            "agent staffing requires the effective Steward directive"
        )
    human_steward = staffing.get("human_steward")
    if not isinstance(human_steward, str) or not human_steward:
        raise ConstitutionalAuthorityError("staffing requires one Human Steward")
    agent_staffed_offices = set(_list(staffing, "agent_staffed_offices"))
    if agent_staffed_offices != _AGENT_STAFFED_OFFICES:
        missing = sorted(_AGENT_STAFFED_OFFICES - agent_staffed_offices)
        extra = sorted(agent_staffed_offices - _AGENT_STAFFED_OFFICES)
        raise ConstitutionalAuthorityError(
            "agent staffing roster is incomplete or invalid: "
            f"missing={missing}, extra={extra}"
        )
    separation_controls = set(_list(staffing, "separation_controls"))
    required_separation = {
        "non_author_adversary",
        "distinct_agent_referee",
        "distinct_agent_sessions",
        "exact_revision_findings",
        "human_steward_reserved_authority",
    }
    if missing := sorted(required_separation - separation_controls):
        raise ConstitutionalAuthorityError(
            f"agent separation controls are incomplete: {missing}"
        )

    constitution = _mapping(schedule, "constitution")
    if (
        constitution.get("repository") != "grandchallenge/INTELLECT"
        or constitution.get("path") != "CONSTITUTION.md"
        or constitution.get("authority") != "supreme_constitutional_law"
    ):
        raise ConstitutionalAuthorityError(
            "the compact INTELLECT Constitution must remain supreme law"
        )

    commentary = _mapping(schedule, "commentary")
    if commentary.get("authority") != "interpretive_nonbinding":
        raise ConstitutionalAuthorityError(
            "commentary must remain interpretive and nonbinding"
        )

    aether = _mapping(schedule, "production_semantic_authority")
    if aether.get("repository") != "grandchallenge/AETHER":
        raise ConstitutionalAuthorityError(
            "AETHER must remain the production semantic authority"
        )
    aether_powers = set(_list(aether, "powers"))
    missing_aether_powers = sorted(_REQUIRED_AETHER_POWERS - aether_powers)
    if missing_aether_powers:
        raise ConstitutionalAuthorityError(
            f"AETHER authority is incomplete: {missing_aether_powers}"
        )

    operating_standard = _mapping(schedule, "operating_standard")
    if (
        operating_standard.get("registry_repository")
        != "grandchallenge/gcl-standards"
        or operating_standard.get("registry_role")
        != "subordinate_registry_and_publication"
    ):
        raise ConstitutionalAuthorityError(
            "gcl-standards must remain a subordinate registry and publication surface"
        )
    if operating_standard.get("status") not in {"candidate", "accepted", "superseded"}:
        raise ConstitutionalAuthorityError("invalid operating-standard status")

    github = _mapping(schedule, "github")
    if github.get("authority") != "operational_and_evidentiary_projection":
        raise ConstitutionalAuthorityError(
            "GitHub must remain an operational and evidentiary projection"
        )
    forbidden = set(_list(github, "forbidden_authorities"))
    missing_forbidden = sorted(_FORBIDDEN_GITHUB_POWERS - forbidden)
    if missing_forbidden:
        raise ConstitutionalAuthorityError(
            f"GitHub exclusions are incomplete: {missing_forbidden}"
        )

    domains = _mapping(schedule, "domain_authorities")
    mathcert = _mapping(domains, "mathematics_certification")
    if mathcert.get("repository") != "grandchallenge/MATHCERT":
        raise ConstitutionalAuthorityError(
            "MATHCERT must remain the mathematical certification authority"
        )
    programme = _mapping(domains, "mathematics_programme")
    if programme.get("repository") != "grandchallenge/MATH-PROGRAMME":
        raise ConstitutionalAuthorityError(
            "MATH-PROGRAMME must remain the mathematics programme authority"
        )

    amendment = _mapping(schedule, "amendment")
    activation = _mapping(schedule, "activation")
    if schedule["status"] == "active":
        if amendment.get("status") != "effective":
            raise ConstitutionalAuthorityError(
                "an active schedule requires the amendment to be effective"
            )
        authors = set(_list(activation, "proposal_author_ids"))
        if not authors:
            raise ConstitutionalAuthorityError(
                "active schedule requires proposal author identities"
            )
        steward_record = _approved_review_record(
            activation, "human_steward_approval", reviewer_kind="human"
        )
        if steward_record.get("reviewer_id") != human_steward:
            raise ConstitutionalAuthorityError(
                "Human Steward approval must match the staffing record"
            )
        adversary = _approved_review_record(
            activation, "independent_adversary_review", reviewer_kind="agent"
        )
        referee = _approved_review_record(
            activation, "independent_referee_review", reviewer_kind="agent"
        )
        for office, record in (("Adversary", adversary), ("Referee", referee)):
            if record.get("reviewer_id") in authors:
                raise ConstitutionalAuthorityError(
                    f"{office} reviewer must not be a proposal author"
                )
            if not record.get("session_id"):
                raise ConstitutionalAuthorityError(
                    f"{office} review requires an agent session identity"
                )
        if adversary.get("reviewer_id") == referee.get("reviewer_id"):
            raise ConstitutionalAuthorityError(
                "Adversary and Referee require distinct agent identities"
            )
        if adversary.get("session_id") == referee.get("session_id"):
            raise ConstitutionalAuthorityError(
                "Adversary and Referee require distinct agent sessions"
            )
        receipt_reference = _complete_receipt_record(activation, "review_receipt")
        for key in ("intellect_commit", "standards_commit"):
            value = activation.get(key)
            if not isinstance(value, str) or not _COMMIT_PATTERN.fullmatch(value):
                raise ConstitutionalAuthorityError(
                    f"active schedule requires an exact 40-character {key}"
                )
        if not activation.get("effective_at"):
            raise ConstitutionalAuthorityError(
                "active schedule requires an effective timestamp"
            )
        if review_receipt is None:
            raise ConstitutionalAuthorityError(
                "active schedule requires the loaded constitutional review receipt"
            )
        validate_review_receipt(review_receipt)
        _validate_activation_receipt_binding(
            activation=activation,
            receipt_reference=receipt_reference,
            receipt=review_receipt,
            proposal_authors=authors,
            human_steward=human_steward,
            steward_record=steward_record,
            adversary_record=adversary,
            referee_record=referee,
        )


def load_and_validate(path: Path) -> dict[str, Any]:
    schedule = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(schedule, dict):
        raise ConstitutionalAuthorityError("authority schedule must be an object")
    receipt = None
    if schedule.get("status") == "active":
        activation = _mapping(schedule, "activation")
        reference = _complete_receipt_record(activation, "review_receipt")
        receipt_path = _resolve_receipt_path(path, str(reference["record_ref"]))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise ConstitutionalAuthorityError("review receipt must be an object")
    validate_authority_schedule(schedule, review_receipt=receipt)
    return schedule


def validate_review_receipt(receipt: Mapping[str, Any]) -> None:
    """Validate the exact GI-AMEND-0001 receipt and separated signoffs."""

    if receipt.get("schema_version") != "1.1.0":
        raise ConstitutionalAuthorityError("unsupported review receipt version")
    if receipt.get("campaign_id") != _EXPECTED_CAMPAIGN_ID:
        raise ConstitutionalAuthorityError("review receipt has the wrong campaign")
    if receipt.get("staffing_mode") != "steward_supervised_agents":
        raise ConstitutionalAuthorityError(
            "review receipt requires Steward-supervised agent staffing"
        )
    digest = receipt.get("packet_sha256")
    if not isinstance(digest, str) or not _DIGEST_PATTERN.fullmatch(digest):
        raise ConstitutionalAuthorityError("review receipt requires packet digest")
    if receipt.get("status") != "complete":
        raise ConstitutionalAuthorityError("review receipt is not complete")

    subjects = receipt.get("subjects")
    if not isinstance(subjects, list):
        raise ConstitutionalAuthorityError("review receipt requires subjects")
    subject_map: dict[str, Mapping[str, Any]] = {}
    for subject in subjects:
        if not isinstance(subject, Mapping):
            raise ConstitutionalAuthorityError("review subject must be an object")
        repository = subject.get("repository")
        pull_request = subject.get("pull_request")
        if (
            not isinstance(repository, str)
            or repository in subject_map
            or repository not in _EXPECTED_REVIEW_SUBJECTS
            or pull_request != _EXPECTED_REVIEW_SUBJECTS[repository]
        ):
            raise ConstitutionalAuthorityError(
                "review receipt has an unexpected or duplicate subject"
            )
        if not _COMMIT_PATTERN.fullmatch(str(subject.get("head_sha", ""))):
            raise ConstitutionalAuthorityError(
                "every review subject requires an exact head commit"
            )
        subject_map[repository] = subject
    if set(subject_map) != set(_EXPECTED_REVIEW_SUBJECTS):
        raise ConstitutionalAuthorityError(
            "review receipt requires the exact INTELLECT and gcl-standards subjects"
        )

    proposal_authors = receipt.get("proposal_authors")
    if (
        not isinstance(proposal_authors, list)
        or not proposal_authors
        or not all(isinstance(item, str) and item for item in proposal_authors)
        or len(set(proposal_authors)) != len(proposal_authors)
    ):
        raise ConstitutionalAuthorityError("receipt requires unique proposal authors")
    author_ids = set(proposal_authors)

    signoffs = receipt.get("signoffs")
    if not isinstance(signoffs, list):
        raise ConstitutionalAuthorityError("review receipt requires signoffs")
    by_office: dict[str, Mapping[str, Any]] = {}
    for signoff in signoffs:
        if not isinstance(signoff, Mapping):
            raise ConstitutionalAuthorityError("review signoff must be an object")
        office = signoff.get("office")
        if not isinstance(office, str) or office in by_office:
            raise ConstitutionalAuthorityError("review offices must be unique")
        by_office[office] = signoff
        if not signoff.get("reviewer") or not signoff.get("authentication_id"):
            raise ConstitutionalAuthorityError(
                f"{office} signoff requires reviewer and authentication identity"
            )
        if not signoff.get("attestation_record"):
            raise ConstitutionalAuthorityError(
                f"{office} signoff requires attestation reference"
            )
        attestation_digest = signoff.get("attestation_sha256")
        if not isinstance(attestation_digest, str) or not _DIGEST_PATTERN.fullmatch(
            attestation_digest
        ):
            raise ConstitutionalAuthorityError(
                f"{office} signoff requires attestation digest"
            )

    if set(by_office) != _REQUIRED_REVIEW_OFFICES:
        raise ConstitutionalAuthorityError(
            "receipt requires Adversary, Referee, and Human Steward signoffs"
        )
    for office in ("adversary", "referee"):
        signoff = by_office[office]
        if signoff.get("reviewer_kind") != "agent":
            raise ConstitutionalAuthorityError(f"{office} must be staffed by an agent")
        if signoff["reviewer"] in author_ids:
            raise ConstitutionalAuthorityError(
                f"{office} reviewer must not be a proposal author"
            )
        if not signoff.get("session_id"):
            raise ConstitutionalAuthorityError(
                f"{office} requires an agent session identity"
            )
    if by_office["human_steward"].get("reviewer_kind") != "human":
        raise ConstitutionalAuthorityError(
            "Human Steward authorization must be human"
        )
    if by_office["human_steward"]["reviewer"] != receipt.get("human_steward"):
        raise ConstitutionalAuthorityError(
            "Human Steward signoff must match the receipt authority"
        )
    if by_office["adversary"]["reviewer"] == by_office["referee"]["reviewer"]:
        raise ConstitutionalAuthorityError(
            "Adversary and Referee must be distinct agents"
        )
    if by_office["adversary"]["session_id"] == by_office["referee"]["session_id"]:
        raise ConstitutionalAuthorityError(
            "Adversary and Referee must use distinct agent sessions"
        )


def _validate_activation_receipt_binding(
    *,
    activation: Mapping[str, Any],
    receipt_reference: Mapping[str, Any],
    receipt: Mapping[str, Any],
    proposal_authors: set[Any],
    human_steward: str,
    steward_record: Mapping[str, Any],
    adversary_record: Mapping[str, Any],
    referee_record: Mapping[str, Any],
) -> None:
    if receipt_reference.get("campaign_id") != receipt.get("campaign_id"):
        raise ConstitutionalAuthorityError("activation receipt campaign mismatch")
    if receipt_reference.get("packet_sha256") != receipt.get("packet_sha256"):
        raise ConstitutionalAuthorityError("activation receipt packet digest mismatch")
    if proposal_authors != set(receipt.get("proposal_authors", [])):
        raise ConstitutionalAuthorityError("activation proposal authors drift from receipt")
    if receipt.get("human_steward") != human_steward:
        raise ConstitutionalAuthorityError("activation Human Steward drifts from receipt")

    subjects = {
        str(item["repository"]): item
        for item in receipt["subjects"]
        if isinstance(item, Mapping)
    }
    expected_commits = {
        "intellect_commit": subjects["grandchallenge/INTELLECT"]["head_sha"],
        "standards_commit": subjects["grandchallenge/gcl-standards"]["head_sha"],
    }
    for key, expected in expected_commits.items():
        if activation.get(key) != expected:
            raise ConstitutionalAuthorityError(
                f"activation {key} does not match the reviewed receipt subject"
            )

    signoffs = {
        str(item["office"]): item
        for item in receipt["signoffs"]
        if isinstance(item, Mapping)
    }
    for office, record in (
        ("adversary", adversary_record),
        ("referee", referee_record),
    ):
        signoff = signoffs[office]
        if (
            record.get("reviewer_id") != signoff.get("reviewer")
            or record.get("session_id") != signoff.get("session_id")
            or record.get("record_ref") != signoff.get("attestation_record")
        ):
            raise ConstitutionalAuthorityError(
                f"activation {office} record does not match the receipt signoff"
            )
    steward_signoff = signoffs["human_steward"]
    if (
        steward_record.get("reviewer_id") != steward_signoff.get("reviewer")
        or steward_record.get("record_ref")
        != steward_signoff.get("attestation_record")
    ):
        raise ConstitutionalAuthorityError(
            "activation Human Steward record does not match the receipt signoff"
        )


def _approved_review_record(
    activation: Mapping[str, Any],
    key: str,
    *,
    reviewer_kind: str,
) -> Mapping[str, Any]:
    record = _mapping(activation, key)
    if (
        record.get("status") != "approved"
        or not record.get("record_ref")
        or record.get("reviewer_kind") != reviewer_kind
        or not record.get("reviewer_id")
    ):
        raise ConstitutionalAuthorityError(f"active schedule requires {key}")
    return record


def _complete_receipt_record(
    activation: Mapping[str, Any], key: str
) -> Mapping[str, Any]:
    record = _mapping(activation, key)
    digest = record.get("packet_sha256")
    if (
        record.get("campaign_id") != _EXPECTED_CAMPAIGN_ID
        or record.get("status") != "complete"
        or record.get("record_ref") != _RECEIPT_RECORD_REF
        or not isinstance(digest, str)
        or not _DIGEST_PATTERN.fullmatch(digest)
    ):
        raise ConstitutionalAuthorityError(f"active schedule requires {key}")
    return record


def _resolve_receipt_path(schedule_path: Path, record_ref: str) -> Path:
    if record_ref != _RECEIPT_RECORD_REF:
        raise ConstitutionalAuthorityError("unsafe or unexpected review receipt path")
    repository_root = schedule_path.resolve().parent.parent
    receipt_path = (repository_root / record_ref).resolve()
    try:
        receipt_path.relative_to(repository_root)
    except ValueError as exc:
        raise ConstitutionalAuthorityError("review receipt escapes repository root") from exc
    if not receipt_path.is_file():
        raise ConstitutionalAuthorityError("referenced review receipt is missing")
    return receipt_path


def _mapping(parent: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = parent.get(key)
    if not isinstance(value, Mapping):
        raise ConstitutionalAuthorityError(f"{key} must be an object")
    return value


def _list(parent: Mapping[str, Any], key: str) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        raise ConstitutionalAuthorityError(f"{key} must be an array")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate an INTELLECT constitutional authority schedule."
    )
    parser.add_argument("schedule", type=Path)
    args = parser.parse_args(argv)
    load_and_validate(args.schedule)
    print("constitutional authority schedule passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
