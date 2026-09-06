"""Integrity checks for an unratified Article XI preparation packet.

This module cannot approve or activate an amendment.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def validate_preparation(directory: Path, constitution: Path) -> dict:
    packet = json.loads((directory / "packet.json").read_text(encoding="utf-8"))
    if packet["status"] != "PREPARATION_ONLY" or packet["ready_for_human_disposition"] is not False:
        raise ValueError("preparation cannot assert decision readiness or activation")
    if packet["current_effective_version"] != "1.2.0" or packet["proposed_effective_version"] != "1.3.0":
        raise ValueError("unexpected version boundary")
    expected = {f"AF-A{i:02}" for i in range(1, 19)}
    if set(packet["unresolved_e0_seams"]) != expected or len(packet["unresolved_e0_seams"]) != 18:
        raise ValueError("unresolved E0 seam removed or duplicated")
    if packet["e1_status"] != "candidate_not_admitted" or packet["e2_status"] != "not_supplied":
        raise ValueError("unverified downstream evidence claimed")
    current = hashlib.sha256(constitution.read_text(encoding="utf-8").encode()).hexdigest()
    if current != packet["constitution_sha256"]:
        raise ValueError("constitutional base drift")
    required = {"README.md", "ARTICLE-IX.proposed.md", "CONSTITUTION.proposed.diff", "ADR.md",
                "THREATS.md", "MIGRATION.md", "GATES.md", "human-steward-disposition.json"}
    if set(packet["files"]) != required:
        raise ValueError("incomplete payload or unexpected path")
    for name, digest in packet["files"].items():
        # Hash normalized LF text so the candidate is inspectable on Windows too.
        data = (directory / name).read_text(encoding="utf-8").encode()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"payload drift: {name}")
    human = json.loads((directory / "human-steward-disposition.json").read_text(encoding="utf-8"))
    if human != {"status": "not_requested", "reviewer": None, "exact_packet_sha256": None,
                 "record_ref": None, "decision": None}:
        raise ValueError("preparation must preserve unset human disposition")
    return {"packet_valid": True, "ready_for_human_disposition": False,
            "effective_change_authorized": False}
