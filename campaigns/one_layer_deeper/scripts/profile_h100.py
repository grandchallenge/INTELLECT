from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any


def _nvidia_query(fields: str) -> list[str]:
    result = subprocess.run(["nvidia-smi", f"--query-gpu={fields}", "--format=csv,noheader,nounits"], check=True, capture_output=True, text=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _peak_memory_mib() -> float:
    values = _nvidia_query("memory.used")
    if len(values) != 1:
        raise RuntimeError("exactly one visible GPU is required")
    return float(values[0].split(",")[0])


def _parse_result(stdout: str) -> dict[str, Any]:
    lines = [line for line in stdout.splitlines() if line.startswith("RESULT_JSON=")]
    if not lines:
        raise RuntimeError("evaluator did not emit RESULT_JSON")
    return json.loads(lines[-1].split("=", 1)[1])


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile a pinned One Layer Deeper H100 run")
    parser.add_argument("--evaluator-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--submission", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--poll-ms", type=int, default=100)
    parser.add_argument("--upstream-commit", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--tier", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    evaluator_root = Path(args.evaluator_root).resolve()
    command = [sys.executable, "-m", "benchmark.runner", "--manifest", str(Path(args.manifest).resolve()), "--submission-file", str(Path(args.submission).resolve()), "--include-structured-metrics"]
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    process = subprocess.Popen(command, cwd=evaluator_root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    peak_mib = 0.0
    samples = 0
    while process.poll() is None:
        peak_mib = max(peak_mib, _peak_memory_mib())
        samples += 1
        time.sleep(max(0.01, args.poll_ms / 1000.0))
    stdout, stderr = process.communicate()
    elapsed = time.monotonic() - started
    peak_mib = max(peak_mib, _peak_memory_mib())
    if process.returncode:
        raise RuntimeError(f"evaluator failed with status {process.returncode}\n{stdout}\n{stderr}")
    result = _parse_result(stdout)
    seed_rows = result.get("seeds", [])
    completed_steps = sum(int(row.get("completed_training_steps", 0)) for row in seed_rows)
    training_seconds = sum(float(row.get("training_seconds", 0.0)) for row in seed_rows)
    batch_size = max((int(row.get("training_batch_size", 0)) for row in seed_rows), default=0)
    examples_per_second = completed_steps * batch_size / training_seconds if training_seconds > 0 else 0.0
    payload = {
        "schema_version": 1,
        "created_at": started_wall,
        "official_upstream_commit": args.upstream_commit,
        "profile": args.profile,
        "tier": args.tier,
        "dataset": args.dataset,
        "seed": args.seed,
        "command": command,
        "environment": {"python": sys.version, "platform": platform.platform(), "gpu": _nvidia_query("name,uuid,memory.total,driver_version")},
        "profiler": {"wall_seconds": elapsed, "poll_ms": args.poll_ms, "samples": samples, "peak_memory_mib": peak_mib, "peak_memory_gib": peak_mib / 1024.0, "completed_training_steps": completed_steps, "training_seconds": training_seconds, "examples_per_second": examples_per_second},
        "result": result,
        "stdout": stdout,
        "stderr": stderr,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
