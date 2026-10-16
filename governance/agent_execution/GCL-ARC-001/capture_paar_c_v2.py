#!/usr/bin/env python3
"""Bounded, exact-head, read-only PAAR-C role execution capture."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HEAD = "b380e583ca2c997c07a4b7f15cbf97728006a79e"
MATERIAL = "b6b353decee67953b74c984a1c8856c3ea56debbae0599f759564f13bbe214b4"
SUBJECT = {"repository":"grandchallenge/MATH-PROGRAMME",
           "head_sha":HEAD,"material_sha256":MATERIAL}
ROLES = (
 ("VERIFIER", ("python3","-m","unittest","-q","tests.test_paar_role_evidence_v2")),
 ("ADVERSARY", ("python3","-m","unittest","-q","tests.test_agent_routine_review")),
 ("REFEREE", ("python3","governance/assurance/GCL-PAAR-001/replay_baseline.py","--offline")),
)

def git(*args, cwd):
    return subprocess.check_output(("git",)+args,cwd=cwd,text=True).strip()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--candidate-dir",type=Path,required=True)
    parser.add_argument("--intellect-dir",type=Path,required=True)
    args=parser.parse_args()
    candidate=args.candidate_dir.resolve()
    intellect=args.intellect_dir.resolve()
    if git("rev-parse","HEAD",cwd=candidate)!=HEAD:
        raise SystemExit("FAIL: candidate head drift")
    if git("branch","--show-current",cwd=intellect)!="governance/arc001-v2-paar-c-real-capture":
        raise SystemExit("FAIL: source branch drift")
    passes=[]
    query=subprocess.run(
        ("gh","api","repos/grandchallenge/MATH-PROGRAMME/pulls/2710/files?per_page=100"),
        text=True,capture_output=True,check=True,timeout=25)
    changed=json.loads(query.stdout)
    if len(changed)!=5:
        raise SystemExit("FAIL: candidate manifest count drift")
    manifest=[]
    for f in changed:
        manifest.append({"path":f["filename"],"status":f["status"],
            "blob_sha":f["sha"],"previous_filename":f.get("previous_filename") or ""})
    canonical=json.dumps(sorted(manifest,key=lambda x:x["path"]),
                         sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    if hashlib.sha256(canonical).hexdigest()!=MATERIAL:
        raise SystemExit("FAIL: candidate material drift")
    for index,(role,argv) in enumerate(ROLES):
        process=subprocess.run(argv,cwd=candidate,text=True,
                               capture_output=True,timeout=75,check=False)
        if process.returncode:
            raise SystemExit(f"FAIL: {role} command {process.returncode}: "
                             +process.stderr[-500:])
        stream="stderr" if process.stderr.strip() else "stdout"
        raw=getattr(process,stream)
        if not raw.strip() or len(raw.encode())>131072:
            raise SystemExit("FAIL: missing or oversized output")
        digest=hashlib.sha256(raw.encode()).hexdigest()
        observed=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ident=f"GCL-PAAR-C-2710-{role}-20261016"
        command=" ".join(argv)
        rel=(f"governance/agent_execution/executions/"
             f"MATH-PROGRAMME-{HEAD}/{role.lower()}-0.json")
        payload={"record_type":"GCL_PROTECTED_ROLE_EXECUTION_OUTPUT_V1",
            "subject":SUBJECT,"role":role,"logical_pass_id":ident,
            "reviewer_system_id":"GPT-6","transport_login":"fyremael",
            "mode":"non_authoring_read_only","command":command,
            "exit_code":process.returncode,"finding":"PASS",
            "observed_utc":observed,
            "environment":{"python":platform.python_version(),"os":platform.platform(),
                "toolchain":"CPython unittest / source commit "+HEAD},
            "output":{"stdout":process.stdout,"stderr":process.stderr,
                      "selected_stream":stream}}
        path=intellect/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
        blob=git("hash-object",str(path),cwd=intellect)
        entry={"role":role,"logical_pass_id":ident,
            "reviewer_system_id":"GPT-6","transport_login":"fyremael",
            "subject_head_sha":HEAD,"mode":"non_authoring_read_only",
            "write_set":[],"read_set":["MATH-PROGRAMME source "+HEAD,argv[-1]],
            "checks":[{"command":command,"exit_code":0,"receipt_sha256":digest,
                "execution_evidence":{"path":rel,"blob_sha":blob}}],
            "finding":"ACCEPT_BOUNDED","unresolved":[]}
        if role=="ADVERSARY":
            entry["negative_controls"]=[
                "tests.test_agent_routine_review hostile role-source checks"]
        passes.append(entry)
        print(f"{role}: EXIT=0 selected={stream} sha256={digest} git_blob={blob}")
    dossier={"schema_version":"2.0.0",
        "record_type":"GCL_AGENT_REVIEW_DOSSIER_V2",
        "subject":SUBJECT,"work_class":"MATERIAL_CONTROL",
        "transport_login":"fyremael",
        "review_scope":"SECURITY_AND_GOVERNANCE_REVIEW",
        "reviewer_system_disclosure":"GPT-6 sequential same-transport logical passes",
        "native_nonauthor_review_claimed":False,
        "claimed_effects":{"mathematical_certification":False,
                           "reserved_authorization":False,
                           "credential_escalation":False},
        "passes":passes}
    path=intellect/f"governance/agent_execution/reviews/MATH-PROGRAMME-{HEAD}.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(dossier,indent=2,sort_keys=True)+"\n")
    print("DOSSIER",path.relative_to(intellect),
          "GIT_BLOB",git("hash-object",str(path),cwd=intellect))
    print("SUBJECT",json.dumps(SUBJECT,sort_keys=True))
    print("STATUS prepared only; native independent approval NOT performed")

if __name__=="__main__":
    main()
