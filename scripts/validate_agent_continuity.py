#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "governance/agent_execution/GCL-AGENT-CONTINUITY-001.md"
MANIFEST = ROOT / "governance/agent_execution/GCL-AGENT-CONTINUITY-001.json"
AGENTS = ROOT / "AGENTS.md"

errors = []
for p in (POLICY, MANIFEST, AGENTS):
    if not p.exists():
        errors.append(f"missing required file: {p.relative_to(ROOT)}")

if MANIFEST.exists():
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON manifest: {exc}")
        data = {}
    if data.get("policy_id") != "GCL-AGENT-CONTINUITY-001":
        errors.append("unexpected policy_id")
    if data.get("version") != "1.0.0":
        errors.append("unexpected policy version")
    req = data.get("requirements", {})
    for key in (
        "exact_head_preflight",
        "checkpoint_before_branch_expansion",
        "post_mutation_readback",
        "timeout_is_not_substantive_boundary",
        "alternate_agent_live_rebind",
        "named_terminal_boundary",
    ):
        if req.get(key) is not True:
            errors.append(f"required continuity control not enabled: {key}")

if AGENTS.exists():
    text = AGENTS.read_text(encoding="utf-8")
    if "GCL-AGENT-CONTINUITY-001" not in text:
        errors.append("AGENTS.md does not bind GCL-AGENT-CONTINUITY-001")

if errors:
    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    raise SystemExit(1)

print("GCL-AGENT-CONTINUITY-001 integrity: PASS")
