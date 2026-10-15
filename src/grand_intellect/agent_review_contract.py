"""GCL-ARC-001: role-pass shape checker, never an authority or GitHub approver.

This module validates documentary invariants. A trusted protected controller
must independently replay the reported evidence and verify GitHub provenance.
"""
from __future__ import annotations

import re
from typing import Any

ROLES = ("VERIFIER", "ADVERSARY", "REFEREE")
CLASSES = ("ROUTINE_BOUNDED", "MATERIAL_CONTROL", "MATHEMATICAL_CLAIM", "RESERVED")
SHA1 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class AgentReviewContractError(ValueError):
    """Invalid, incomplete, contradictory, or overclaiming role packet."""


def require(test: bool, reason: str) -> None:
    if not test:
        raise AgentReviewContractError(reason)


def _sha(value: Any, regex: re.Pattern[str], field: str) -> None:
    require(isinstance(value, str) and bool(regex.fullmatch(value)), field)


def validate_review_dossier(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate shape and logical separation, NOT independent factual truth."""
    require(isinstance(packet, dict), "dossier must be an object")
    require(packet.get("record_type") == "GCL_AGENT_REVIEW_DOSSIER_V1", "record type")
    subject = packet.get("subject")
    require(isinstance(subject, dict), "missing subject")
    require(subject.get("repository") and isinstance(subject["repository"], str),
            "repository required")
    _sha(subject.get("head_sha"), SHA1, "unbound candidate commit")
    _sha(subject.get("material_sha256"), SHA256, "unbound candidate material")
    require(packet.get("work_class") in CLASSES, "work class")
    transport = packet.get("transport_login")
    require(isinstance(transport, str) and bool(transport.strip()), "transport missing")

    # No review dossier can know the head or the GitHub review ID of its own PR.
    # Actual source PR identifiers must first appear in the *later* receipt.
    for forbidden in ("source_pr_head_sha", "source_pr_review_id",
                      "review_anchor", "own_commit_sha"):
        require(forbidden not in packet, "cyclic source review reference")

    passes = packet.get("passes")
    require(isinstance(passes, list) and len(passes) == 3, "three passes required")
    require([p.get("role") if isinstance(p, dict) else None for p in passes]
            == list(ROLES), "ordered roles required")
    ids: set[str] = set()
    systems: set[str] = set()
    blockers: list[str] = []
    for part in passes:
        role = part["role"]
        name = part.get("logical_pass_id")
        require(isinstance(name, str) and bool(name.strip()) and name not in ids,
                "duplicate/missing logical pass identity")
        ids.add(name)
        system = part.get("reviewer_system_id")
        require(isinstance(system, str) and bool(system.strip()), "reviewer system ID")
        systems.add(system)
        require(part.get("transport_login") == transport,
                "transport identity not attributable")
        require(part.get("subject_head_sha") == subject["head_sha"],
                "pass not source-bound")
        require(part.get("mode") == "non_authoring_read_only",
                "non-authoring review mode required")
        require(part.get("write_set") == [], "review pass attempted mutation")
        require(isinstance(part.get("read_set"), list) and bool(part["read_set"]),
                "review has no evidence read set")
        require(part.get("finding") in ("ACCEPT_BOUNDED", "REVISE", "BLOCKED"),
                "missing bounded finding")
        require(isinstance(part.get("unresolved"), list),
                "missing unresolved findings field")
        checks = part.get("checks")
        require(isinstance(checks, list) and bool(checks), "no executable checks")
        for check in checks:
            require(isinstance(check, dict) and isinstance(check.get("command"), str)
                    and bool(check["command"].strip()), "check command not bound")
            require(type(check.get("exit_code")) is int, "exit code unbound")
            _sha(check.get("receipt_sha256"), SHA256, "check receipt absent")
            if check["exit_code"] != 0:
                blockers.append(f"{role}: failed check")
        if role == "ADVERSARY":
            neg = part.get("negative_controls")
            require(isinstance(neg, list) and bool(neg),
                    "no actual adverse test/control")
        if part["finding"] != "ACCEPT_BOUNDED" or part["unresolved"]:
            blockers.append(f"{role}: disposition or unresolved objection")

    if packet["work_class"] == "MATHEMATICAL_CLAIM":
        methods = packet.get("independent_method_evidence")
        require(isinstance(methods, list) and bool(methods),
                "scientific independent method not recorded")
        for m in methods:
            require(isinstance(m, dict) and m.get("method") in
                    ("FORMAL_KERNEL", "INDEPENDENT_COMPUTATION", "EXTERNAL_SOURCE_PROOF"),
                    "unsupported independent scientific method")
            _sha(m.get("receipt_sha256"), SHA256,
                 "scientific verification method receipt missing")
    effects = packet.get("claimed_effects")
    require(effects == {"mathematical_certification": False,
                        "reserved_authorization": False,
                        "credential_escalation": False},
            "agent review overclaimed authority")
    return {
        "schema": "GCL_AGENT_ROLE_PASS_VALIDATION_V1",
        "candidate_head": subject["head_sha"],
        "validated_roles": list(ROLES),
        "transport_logins_needed": 1,
        "reviewer_system_ids": sorted(systems),
        "blocking_objections": blockers,
        "eligible_for_separate_protected_review": not blockers,
        "protected_review_performed": False,
        "github_approval_created": False,
        "scientific_certification_created": False,
    }


def validate_later_anchor(dossier: dict[str, Any], receipt: dict[str, Any]) -> None:
    """Check the acyclic shape; live GitHub events need separate authentic replay."""
    validate_review_dossier(dossier)
    require(receipt.get("record_type") == "GCL_PROTECTED_ROLE_REVIEW_RECEIPT_V1",
            "later receipt record type")
    require(receipt.get("subject") == dossier["subject"],
            "later receipt candidate changed")
    anchor = receipt.get("source_review_anchor")
    require(isinstance(anchor, dict), "no separate source review anchor")
    _sha(anchor.get("source_pr_head_sha"), SHA1, "source PR head missing")
    require(type(anchor.get("source_pr_number")) is int
            and anchor["source_pr_number"] > 0, "source PR number missing")
    require(type(anchor.get("approved_review_id")) is int
            and anchor["approved_review_id"] > 0, "source review ID missing")
    _sha(anchor.get("review_dossier_blob_sha"), SHA1, "dossier blob missing")
    require(receipt.get("source_protected_merge_verified") is True,
            "unprotected source dossier")
    # This function cannot attest that the GitHub identifiers correspond to
    # true accepted events: the protected controller must fetch the REST data.
