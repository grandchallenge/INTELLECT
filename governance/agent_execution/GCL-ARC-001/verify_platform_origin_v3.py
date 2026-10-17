#!/usr/bin/env python3
"""Fail-closed offline V3 pilot source-dossier/witness binding verification.

Not a remote runner identity verifier. The MATH-PROGRAMME production
paar_execution_origin.verify_witness() must separately confirm GitHub API.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROLE_ORDER=('VERIFIER','ADVERSARY','REFEREE')
RECORD='GCL_AGENT_PLATFORM_ORIGIN_DOSSIER_V3'
RUN=38988609732

class OriginSourceError(ValueError):
    pass

def demand(value,reason):
    if not value: raise OriginSourceError(reason)

def verify(dossier,witness,witness_bytes,witness_git_blob):
    demand(isinstance(dossier,dict) and dossier.get('record_type')==RECORD
           and dossier.get('schema_version')=='3.0.0','V3 source contract drift')
    source=dossier.get('subject') or {}
    demand(source==witness.get('source') and source.get('repository')=='grandchallenge/MATH-PROGRAMME'
           and source.get('head_sha')=='b380e583ca2c997c07a4b7f15cbf97728006a79e'
           and source.get('material_sha256')=='b6b353decee67953b74c984a1c8856c3ea56debbae0599f759564f13bbe214b4',
           'source material identity drift')
    execution=dossier.get('platform_execution') or {}
    entry=execution.get('protected_witness') or {}
    demand(entry.get('git_blob_sha')==witness_git_blob
           and entry.get('sha256')==hashlib.sha256(witness_bytes).hexdigest()
           and entry.get('path')=='governance/agent_execution/GCL-ARC-001/witness-38988609732.json',
           'witness bytes/immutable identity drift')
    demand(witness.get('record_type')=='GCL_PAAR_C_PLATFORM_EXECUTION_WITNESS/1'
           and witness.get('run_id')==RUN and witness.get('run_attempt')==1
           and witness.get('workflow_sha')=='80f3b83d94795dba2acceef05f66b386ac6f735d'
           and witness.get('runner_environment')=='github-hosted'
           and witness.get('run_event')=='workflow_dispatch',
           'platform run subject/identity drift')
    demand(execution.get('run_id')==RUN
           and execution.get('run_attempt')==1
           and execution.get('workflow_head_sha')==witness['workflow_sha']
           and execution.get('origin_artifact_id')==12084032389
           and execution.get('origin_artifact_name')=='paar-c-origin-38988609732-1',
           'platform origin pointer drift')
    roles=witness.get('executions')
    demand(isinstance(roles,list) and len(roles)==3
           and tuple(r.get('role') for r in roles)==ROLE_ORDER,
           'distinct ordered role evidence missing')
    for role in roles:
        stream=role.get('selected_stream')
        demand(stream in ('stdout','stderr') and isinstance(role.get(stream),str)
               and role.get('exit_code')==0
               and hashlib.sha256(role[stream].encode()).hexdigest()==role.get('selected_sha256'),
               'protected platform output mismatch')
    demand(execution.get('role_output_sha256')=={r['role']:r['selected_sha256'] for r in roles},
           'source dossier role output hash drift')
    require_limits={'later_independent_platform_execution_verified':True,
                    'historical_2026_10_15_chad_execution_authenticated':False,
                    'independent_specialist_persons_certified':False,
                    'cryptographic_hardware_attestation':False,
                    'mathematical_certification':False,
                    'gcl_wide_assurance_certified':False}
    demand(dossier.get('claims')==require_limits
           and (witness.get('limits') or {}).get('original_chad_execution_attested') is False,
           'unsupported assurance claim promotion')
    return {'status':'V3_SOURCE_BYTES_BOUND_PENDING_NATIVE_REVIEW',
            'run_id':RUN,'roles':list(ROLE_ORDER),
            'historical_chad_execution_attested':False,'remote_platform_verified_here':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repository',type=Path,default=Path('.'))
    opts=p.parse_args();repo=opts.repository.resolve()
    path=repo/'governance/agent_execution/GCL-ARC-001/witness-38988609732.json'
    dossier=json.loads((repo/'governance/agent_execution/reviews_v3/MATH-PROGRAMME-b380e583ca2c997c07a4b7f15cbf97728006a79e.json').read_text())
    raw=path.read_bytes();record=json.loads(raw)
    blob=subprocess.check_output(('git','hash-object',str(path)),cwd=repo,text=True).strip()
    print(json.dumps(verify(dossier,record,raw,blob),sort_keys=True))

if __name__=='__main__':main()
