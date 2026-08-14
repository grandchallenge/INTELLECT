"""Fail-closed validation for TC-BOOTSTRAP-CLOSE-001."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_SOURCE_HEAD = "8c3da17b2c401944e43b6e9bb0fae3bc95b05624"
EXPECTED_SOURCE_TREE = "9d1f2d2b821a3398e8895b75f8badebc2fb6a059"
EXPECTED_INVENTORY_SHA256 = "ad2803363071e7402cdaa48b3d39062a0efcaac2e53eac69ab76a93001484d6d"
EXPECTED_RECORD_SHA256 = "ec871730221523a55e09c81b7e81d785284e4b181ec84ac65480962c9f8dee27"
EXPECTED_LADDER = [
    ("TROVE-CURATA-XREF-WP00", 24, "b6158a995a97ae58abfe139925de4ec6c9cd0a0b", "e080192f3c4cb1881cf781572dd1246b22792163"),
    ("TC-FIXTURE-001", 28, "e8d12e6f314ddabcf3a36f9ec49216b669d07024", "59b34a195aa7d4fdd381d428dab3e4f18e2016e7"),
    ("TC-FIXTURE-002", 30, "04fdb6bb3232be2d94cb197e19aa0deb333b0c97", "b6a1511a7f1d7ca01108f57cede2982377ebd270"),
    ("TC-FIXTURE-003", 44, "af5a568a2f49db949ff5c355f33ab29231cabac4", "0096eb21ca62c5ef7f6e458f358edcb1cd963a20"),
    ("TC-FIXTURE-003-REVIEW-REMEDY-001", 46, "09ebdf7e1f01abc1dd75450725b4e8b0d93f3a65", "5c5f6a1cbb6327c559884a79abc119cf706153af"),
    ("TC-FIXTURE-004", 49, "6dc65962ec77e17ae5bdd2c75ccd5da63aefcef7", "6e2385a841dfd55bbab480d79a47611cc6557103"),
    ("TC-FIXTURE-004-REVIEW-REMEDY-001", 51, "dbb68b54aaf6df2eced710e6dd3936aa3bb2f7fc", "70a0a74502e0480d387d740027e48751286e4bfe"),
    ("TC-FIXTURE-005", 60, "2318a962f3b0f79b47f3b0b03efa2743298b6776", "e5d0c3415250581350d01a27fea6bd60c8162c56"),
]

ROOT_FIELDS = {
    "schema_version",
    "closure_id",
    "status",
    "source",
    "destination",
    "bootstrap_ladder",
    "bootstrap_roots",
    "artifact_inventory",
    "artifact_inventory_sha256",
    "schema_paths",
    "workflow_paths",
    "review_remedies",
    "migration_contract",
    "authority_boundary",
    "claim_boundary",
    "closure_record_sha256",
}


class TroveCurataBootstrapClosureError(ValueError):
    """Raised when the bootstrap closure or migration boundary drifts."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TroveCurataBootstrapClosureError(message)


def _canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_trove_curata_bootstrap_closure(record: dict[str, Any]) -> dict[str, Any]:
    """Validate the exact bootstrap snapshot and inactive migration contract."""

    _require(set(record) == ROOT_FIELDS, "closure field set drift")
    _require(record["schema_version"] == "0.1.0", "schema version drift")
    _require(record["closure_id"] == "TC-BOOTSTRAP-CLOSE-001", "closure identity drift")
    _require(
        record["status"] == "prepared_pending_source_merge_and_destination_acceptance",
        "closure status drift",
    )

    source = record["source"]
    _require(
        source
        == {
            "repository": "grandchallenge/INTELLECT",
            "issue_number": 68,
            "protected_head_at_preparation": EXPECTED_SOURCE_HEAD,
            "protected_tree_at_preparation": EXPECTED_SOURCE_TREE,
            "bootstrap_role_after_activation": "immutable_history_replay_and_constitutional_context",
        },
        "source identity drift",
    )

    destination = record["destination"]
    _require(
        destination
        == {
            "repository": "grandchallenge/TROVE-CURATA",
            "repository_observed_existing_at_preparation": False,
            "acceptance_record_id": "TC-REPO-ACCEPT-001",
            "canonical_from": "TC-FIXTURE-006",
            "activation_state": "not_active",
        },
        "destination boundary drift",
    )

    ladder = record["bootstrap_ladder"]
    _require(isinstance(ladder, list) and len(ladder) == 8, "bootstrap ladder length drift")
    observed_ladder = [
        (
            entry.get("record_id"),
            entry.get("pull_request"),
            entry.get("exact_head"),
            entry.get("protected_merge"),
        )
        for entry in ladder
    ]
    _require(observed_ladder == EXPECTED_LADDER, "bootstrap ladder identity drift")
    _require(
        [entry["role"] for entry in ladder]
        == [
            "foundation",
            "extraction_observation",
            "pii_observation",
            "governed_transformation",
            "prospective_review_remedy",
            "duplicate_observation",
            "prospective_review_remedy",
            "quality_signal_observation",
        ],
        "bootstrap ladder role drift",
    )

    roots = record["bootstrap_roots"]
    _require(
        set(roots) == {"fixtures/trove_curata", "schemas", "workflows"}
        and all(re.fullmatch(r"[0-9a-f]{40}", value) for value in roots.values()),
        "bootstrap root identity drift",
    )

    inventory = record["artifact_inventory"]
    _require(isinstance(inventory, list) and len(inventory) >= 50, "artifact inventory incomplete")
    paths = [entry.get("path") for entry in inventory]
    _require(paths == sorted(paths) and len(paths) == len(set(paths)), "artifact path ordering drift")
    for entry in inventory:
        _require(
            set(entry) == {"path", "mode", "blob_sha", "size"}
            and isinstance(entry["path"], str)
            and entry["mode"] in {"100644", "100755"}
            and bool(re.fullmatch(r"[0-9a-f]{40}", entry["blob_sha"]))
            and isinstance(entry["size"], int)
            and entry["size"] >= 0,
            "artifact identity drift",
        )
    inventory_digest = _canonical_digest(inventory)
    _require(
        inventory_digest == record["artifact_inventory_sha256"] == EXPECTED_INVENTORY_SHA256,
        "artifact inventory digest drift",
    )
    _require(
        record["schema_paths"]
        == [path for path in paths if path.startswith("schemas/")],
        "schema identity projection drift",
    )
    _require(
        record["workflow_paths"]
        == [path for path in paths if path.startswith(".github/workflows/")],
        "workflow identity projection drift",
    )

    remedies = record["review_remedies"]
    _require(set(remedies) == {"fixture_003", "fixture_004"}, "review remedy set drift")
    for remedy in remedies.values():
        _require(
            remedy["historical_defect_preserved"] is True
            and remedy["historical_state_rewritten"] is False
            and remedy["prospective_remedy_record"].endswith("REVIEW-REMEDY-001"),
            "review remedy history drift",
        )

    migration = record["migration_contract"]
    required_true = {
        "source_protected_merge_required",
        "destination_protected_acceptance_required",
        "two_sided_readback_required",
        "destination_import_must_match_source_blobs",
        "intellect_historical_replay_remains_permitted",
        "intellect_prospective_historical_correction_remains_permitted",
    }
    required_false = {
        "destination_may_invent_bootstrap_authority",
        "destination_may_activate_before_readback",
        "fixture_006_may_begin_before_activation",
        "fixture_006_may_be_implemented_in_intellect_after_activation",
    }
    _require(migration["review_tier"] == "T3", "migration tier drift")
    _require(all(migration[key] is True for key in required_true), "migration safeguard disabled")
    _require(all(migration[key] is False for key in required_false), "migration authority escalation")
    _require(
        migration["destination_replay_fixtures"]
        == [f"TC-FIXTURE-00{index}" for index in range(1, 6)],
        "destination replay ladder drift",
    )

    authority = record["authority_boundary"]
    _require(
        authority["project_owner"] == "grandchallenge"
        and authority["gcl_contained"] is True
        and authority["github_operational_record"] is True
        and authority["aether_role"] == "future_projection_nonblocking",
        "authority identity drift",
    )
    for key in {
        "providers_have_policy_authority",
        "providers_have_admission_authority",
        "passports_have_admission_authority",
        "metrics_have_admission_authority",
        "bootstrap_closure_activates_destination",
        "bootstrap_closure_admits_corpus",
    }:
        _require(authority[key] is False, "authority escalation")

    claims = record["claim_boundary"]
    _require(isinstance(claims, dict) and len(claims) == 17, "claim boundary field set drift")
    _require(all(value is False for value in claims.values()), "claim inflation")

    supplied_record_digest = record["closure_record_sha256"]
    digest_subject = dict(record)
    del digest_subject["closure_record_sha256"]
    _require(
        _canonical_digest(digest_subject)
        == supplied_record_digest
        == EXPECTED_RECORD_SHA256,
        "closure record digest drift",
    )
    return record


def load_and_validate_trove_curata_bootstrap_closure(path: str | Path) -> dict[str, Any]:
    record = json.loads(Path(path).read_text(encoding="utf-8"))
    _require(isinstance(record, dict), "closure record must be an object")
    return validate_trove_curata_bootstrap_closure(record)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        raise SystemExit("usage: python -m grand_intellect.trove_curata_bootstrap_closure RECORD")
    record = load_and_validate_trove_curata_bootstrap_closure(args[0])
    print(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
