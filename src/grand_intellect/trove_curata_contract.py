"""Fail-closed validation for the TROVE-CURATA crossover contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


EXPECTED_RECORD_CONTRACTS = {
    "trove_source_record",
    "curata_transformation_receipt",
    "curata_passport",
    "trove_release_manifest",
}

EXPECTED_REVIEW_TIERS = {
    "T0": "editorial_or_nonsemantic",
    "T1": "deterministic_transformation",
    "T2": "judgment_or_retention_policy",
    "T3": "corpus_admission_or_high_impact_policy",
}

FALSE_CLAIMS = {
    "dataset_quality_proved",
    "privacy_proved",
    "legality_proved",
    "safety_proved",
    "fitness_for_training_proved",
    "downstream_improvement_proved",
    "commercial_claim_authorized",
}

ALLOWED_DECISIONS = {
    "reuse_directly",
    "generalize",
    "adapt_locally",
    "defer",
    "reject",
}

ALLOWED_AUTHORITY_EFFECTS = {
    "none",
    "gcl_side_only",
    "future_projection_only",
}


class TroveCurataContractError(ValueError):
    """Raised when a TROVE-CURATA work-package contract is unsafe or incomplete."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TroveCurataContractError(message)


def validate_trove_curata_contract(record: dict[str, Any]) -> dict[str, Any]:
    """Validate semantic invariants not safely delegated to JSON Schema alone."""

    _require(record.get("schema_version") == "0.1.0", "unsupported schema version")
    _require(
        record.get("work_package_id") == "TROVE-CURATA-XREF-WP00",
        "unexpected work-package identity",
    )
    _require(
        record.get("status") in {"approved", "implemented", "reviewed", "admitted", "superseded"},
        "invalid lifecycle status",
    )

    authority = record.get("authority")
    _require(isinstance(authority, dict), "authority must be an object")
    _require(
        authority.get("gcl_repository") == "grandchallenge/INTELLECT",
        "GCL-side authority must remain in INTELLECT",
    )
    _require(
        authority.get("collaborator_repository") == "teraflop-ai/llm-data",
        "collaborator repository identity drift",
    )
    _require(
        authority.get("collaborator_repository_authority") == "collaborator_owned",
        "GCL may not claim collaborator-repository authority",
    )
    _require(
        authority.get("current_operational_authority") == "github",
        "GitHub must remain the present operational record",
    )
    _require(
        authority.get("aether_role") == "future_projection_nonblocking",
        "AETHER must not become a runtime prerequisite",
    )

    contracts = record.get("record_contracts")
    _require(isinstance(contracts, list), "record_contracts must be a list")
    _require(len(contracts) == len(set(contracts)), "duplicate record contract")
    _require(set(contracts) == EXPECTED_RECORD_CONTRACTS, "record contract set drift")

    _require(record.get("review_tiers") == EXPECTED_REVIEW_TIERS, "review tier semantics drift")

    provider_decisions = record.get("provider_decisions")
    _require(isinstance(provider_decisions, list) and provider_decisions, "provider decisions required")
    capabilities: set[str] = set()
    for decision in provider_decisions:
        _require(isinstance(decision, dict), "provider decision must be an object")
        capability = decision.get("capability")
        _require(isinstance(capability, str) and capability.strip() == capability and capability, "invalid capability")
        _require(capability not in capabilities, "duplicate provider capability")
        capabilities.add(capability)
        _require(decision.get("decision") in ALLOWED_DECISIONS, "invalid provider decision")
        _require(
            decision.get("authority_effect") in ALLOWED_AUTHORITY_EFFECTS,
            "invalid authority effect",
        )
        if capability == "aether_provenance_projection":
            _require(decision.get("decision") == "defer", "AETHER must remain deferred")
            _require(
                decision.get("authority_effect") == "future_projection_only",
                "AETHER may have future-projection effect only",
            )
        if capability == "mathsolve_mathematical_routing":
            _require(decision.get("decision") == "reject", "MATHSOLVE routing has no data-curation role")
            _require(decision.get("authority_effect") == "none", "rejected capability cannot confer authority")

    fixture = record.get("fixture")
    _require(isinstance(fixture, dict), "fixture must be an object")
    _require(fixture.get("fixture_id") == "TC-FIXTURE-001", "fixture identity drift")
    _require(fixture.get("source_family") == "html", "first fixture must remain HTML")
    _require(fixture.get("execution_provider") == "daft", "execution provider drift")
    _require(fixture.get("extractor") == "trafilatura", "extractor drift")
    _require(fixture.get("synthetic_content_allowed") is False, "synthetic content must remain prohibited")

    claim_boundary = record.get("claim_boundary")
    _require(isinstance(claim_boundary, dict), "claim boundary must be an object")
    _require(set(claim_boundary) == FALSE_CLAIMS, "claim boundary field set drift")
    for claim in FALSE_CLAIMS:
        _require(claim_boundary.get(claim) is False, f"claim inflation: {claim}")

    return record


def load_and_validate_trove_curata_contract(path: str | Path) -> dict[str, Any]:
    """Load a JSON contract from disk and validate its fail-closed invariants."""

    contract_path = Path(path)
    try:
        record = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TroveCurataContractError(f"unable to load contract: {exc}") from exc
    _require(isinstance(record, dict), "contract root must be an object")
    return validate_trove_curata_contract(record)
