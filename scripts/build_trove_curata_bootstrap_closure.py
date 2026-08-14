#!/usr/bin/env python3
"""Build the immutable TC-BOOTSTRAP-CLOSE-001 source snapshot record."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "governance" / "trove_curata_bootstrap_closure.json"
SOURCE_HEAD = "8c3da17b2c401944e43b6e9bb0fae3bc95b05624"

LADDER = [
    {
        "record_id": "TROVE-CURATA-XREF-WP00",
        "role": "foundation",
        "pull_request": 24,
        "exact_head": "b6158a995a97ae58abfe139925de4ec6c9cd0a0b",
        "protected_merge": "e080192f3c4cb1881cf781572dd1246b22792163",
    },
    {
        "record_id": "TC-FIXTURE-001",
        "role": "extraction_observation",
        "pull_request": 28,
        "exact_head": "e8d12e6f314ddabcf3a36f9ec49216b669d07024",
        "protected_merge": "59b34a195aa7d4fdd381d428dab3e4f18e2016e7",
    },
    {
        "record_id": "TC-FIXTURE-002",
        "role": "pii_observation",
        "pull_request": 30,
        "exact_head": "04fdb6bb3232be2d94cb197e19aa0deb333b0c97",
        "protected_merge": "b6a1511a7f1d7ca01108f57cede2982377ebd270",
    },
    {
        "record_id": "TC-FIXTURE-003",
        "role": "governed_transformation",
        "pull_request": 44,
        "exact_head": "af5a568a2f49db949ff5c355f33ab29231cabac4",
        "protected_merge": "0096eb21ca62c5ef7f6e458f358edcb1cd963a20",
    },
    {
        "record_id": "TC-FIXTURE-003-REVIEW-REMEDY-001",
        "role": "prospective_review_remedy",
        "pull_request": 46,
        "exact_head": "09ebdf7e1f01abc1dd75450725b4e8b0d93f3a65",
        "protected_merge": "5c5f6a1cbb6327c559884a79abc119cf706153af",
    },
    {
        "record_id": "TC-FIXTURE-004",
        "role": "duplicate_observation",
        "pull_request": 49,
        "exact_head": "6dc65962ec77e17ae5bdd2c75ccd5da63aefcef7",
        "protected_merge": "6e2385a841dfd55bbab480d79a47611cc6557103",
    },
    {
        "record_id": "TC-FIXTURE-004-REVIEW-REMEDY-001",
        "role": "prospective_review_remedy",
        "pull_request": 51,
        "exact_head": "dbb68b54aaf6df2eced710e6dd3936aa3bb2f7fc",
        "protected_merge": "70a0a74502e0480d387d740027e48751286e4bfe",
    },
    {
        "record_id": "TC-FIXTURE-005",
        "role": "quality_signal_observation",
        "pull_request": 60,
        "exact_head": "2318a962f3b0f79b47f3b0b03efa2743298b6776",
        "protected_merge": "e5d0c3415250581350d01a27fea6bd60c8162c56",
    },
]


def run_git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def canonical_digest(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def is_bootstrap_artifact(path: str) -> bool:
    return bool(
        path.startswith("fixtures/trove_curata/")
        or re.fullmatch(r"requirements-trove-curata(?:-[a-z]+)?\.txt", path)
        or re.fullmatch(r"\.github/workflows/trove-curata-[a-z-]+\.yml", path)
        or re.fullmatch(r"docs/(?:TC_FIXTURE|TROVE_CURATA)[A-Z0-9_]*\.md", path)
        or path == "docs/assets/trove-curata-progress.png"
        or re.fullmatch(r"governance/trove_curata[a-z0-9_]*\.json", path)
        or re.fullmatch(r"schemas/trove_curata[a-z0-9_]*\.schema\.json", path)
        or re.fullmatch(r"src/grand_intellect/trove_curata[a-z0-9_]*\.py", path)
        or re.fullmatch(r"tests/test_trove_curata[a-z0-9_]*\.py", path)
    )


def artifact_inventory() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    listing = run_git("ls-tree", "-r", "-l", SOURCE_HEAD)
    for line in listing.splitlines():
        metadata, path = line.split("\t", 1)
        mode, object_type, blob_sha, size = metadata.split()
        if object_type == "blob" and is_bootstrap_artifact(path):
            rows.append(
                {
                    "path": path,
                    "mode": mode,
                    "blob_sha": blob_sha,
                    "size": int(size),
                }
            )
    rows.sort(key=lambda row: str(row["path"]))
    if not rows:
        raise RuntimeError("bootstrap artifact inventory is empty")
    return rows


def build_record() -> dict[str, object]:
    inventory = artifact_inventory()
    record: dict[str, object] = {
        "schema_version": "0.1.0",
        "closure_id": "TC-BOOTSTRAP-CLOSE-001",
        "status": "prepared_pending_source_merge_and_destination_acceptance",
        "source": {
            "repository": "grandchallenge/INTELLECT",
            "issue_number": 68,
            "protected_head_at_preparation": SOURCE_HEAD,
            "protected_tree_at_preparation": run_git("rev-parse", f"{SOURCE_HEAD}^{{tree}}"),
            "bootstrap_role_after_activation": "immutable_history_replay_and_constitutional_context",
        },
        "destination": {
            "repository": "grandchallenge/TROVE-CURATA",
            "repository_observed_existing_at_preparation": False,
            "acceptance_record_id": "TC-REPO-ACCEPT-001",
            "canonical_from": "TC-FIXTURE-006",
            "activation_state": "not_active",
        },
        "bootstrap_ladder": LADDER,
        "bootstrap_roots": {
            "fixtures/trove_curata": run_git(
                "rev-parse", f"{SOURCE_HEAD}:fixtures/trove_curata"
            ),
            "schemas": run_git("rev-parse", f"{SOURCE_HEAD}:schemas"),
            "workflows": run_git("rev-parse", f"{SOURCE_HEAD}:.github/workflows"),
        },
        "artifact_inventory": inventory,
        "artifact_inventory_sha256": canonical_digest(inventory),
        "schema_paths": [
            row["path"] for row in inventory if str(row["path"]).startswith("schemas/")
        ],
        "workflow_paths": [
            row["path"]
            for row in inventory
            if str(row["path"]).startswith(".github/workflows/")
        ],
        "review_remedies": {
            "fixture_003": {
                "historical_defect_preserved": True,
                "prospective_remedy_record": "TC-FIXTURE-003-REVIEW-REMEDY-001",
                "historical_state_rewritten": False,
            },
            "fixture_004": {
                "historical_defect_preserved": True,
                "prospective_remedy_record": "TC-FIXTURE-004-REVIEW-REMEDY-001",
                "historical_state_rewritten": False,
            },
        },
        "migration_contract": {
            "review_tier": "T3",
            "source_protected_merge_required": True,
            "destination_protected_acceptance_required": True,
            "two_sided_readback_required": True,
            "destination_import_must_match_source_blobs": True,
            "destination_replay_fixtures": [
                "TC-FIXTURE-001",
                "TC-FIXTURE-002",
                "TC-FIXTURE-003",
                "TC-FIXTURE-004",
                "TC-FIXTURE-005",
            ],
            "destination_may_invent_bootstrap_authority": False,
            "destination_may_activate_before_readback": False,
            "fixture_006_may_begin_before_activation": False,
            "fixture_006_may_be_implemented_in_intellect_after_activation": False,
            "intellect_historical_replay_remains_permitted": True,
            "intellect_prospective_historical_correction_remains_permitted": True,
        },
        "authority_boundary": {
            "project_owner": "grandchallenge",
            "gcl_contained": True,
            "github_operational_record": True,
            "aether_role": "future_projection_nonblocking",
            "providers_have_policy_authority": False,
            "providers_have_admission_authority": False,
            "passports_have_admission_authority": False,
            "metrics_have_admission_authority": False,
            "bootstrap_closure_activates_destination": False,
            "bootstrap_closure_admits_corpus": False,
        },
        "claim_boundary": {
            "production_corpus_admitted": False,
            "dataset_quality_certified": False,
            "privacy_certified": False,
            "legality_or_rights_certified": False,
            "training_fitness_qualified": False,
            "release_candidate_declared": False,
            "public_release_authorized": False,
            "records_ranked": False,
            "records_rejected": False,
            "records_deleted": False,
            "records_suppressed": False,
            "records_retained_by_authority": False,
            "canonical_record_selected": False,
            "reference_contamination_absence_proved": False,
            "downstream_improvement_proved": False,
            "novelty_or_priority_claimed": False,
            "commercial_claim_authorized": False,
        },
    }
    record["closure_record_sha256"] = canonical_digest(record)
    return record


def main() -> int:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(record["closure_record_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
