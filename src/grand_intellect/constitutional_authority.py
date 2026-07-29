from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping


class ConstitutionalAuthorityError(ValueError):
    """Raised when an authority schedule would create an unlawful authority."""


_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
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


def validate_authority_schedule(schedule: Mapping[str, Any]) -> None:
    """Fail closed if a constitutional authority schedule crosses a boundary."""

    if schedule.get("schema_version") != "1.0.0":
        raise ConstitutionalAuthorityError("unsupported authority schedule version")
    if schedule.get("status") not in {"proposed", "active", "superseded"}:
        raise ConstitutionalAuthorityError("invalid authority schedule status")

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

    activation = _mapping(schedule, "activation")
    if schedule["status"] == "active":
        if operating_standard.get("status") != "accepted":
            raise ConstitutionalAuthorityError(
                "an active schedule requires an accepted operating standard"
            )
        for key in (
            "human_steward_approval",
            "independent_adversary_review",
            "independent_referee_review",
        ):
            record = _mapping(activation, key)
            if record.get("status") != "approved" or not record.get("record_ref"):
                raise ConstitutionalAuthorityError(
                    f"active schedule requires {key}"
                )
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


def load_and_validate(path: Path) -> dict[str, Any]:
    schedule = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(schedule, dict):
        raise ConstitutionalAuthorityError("authority schedule must be an object")
    validate_authority_schedule(schedule)
    return schedule


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
