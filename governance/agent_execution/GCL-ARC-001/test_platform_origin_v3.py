"""Bounded adversarial source-provenance checks; not remote platform attestations."""
import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('origin',HERE/'verify_platform_origin_v3.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class V3SourceTests(unittest.TestCase):
    def setUp(self):
        p=HERE/'witness-38988609732.json'
        self.raw=p.read_bytes()
        self.witness=json.loads(self.raw)
        self.dossier=json.loads((ROOT/'governance/agent_execution/reviews_v3/MATH-PROGRAMME-b380e583ca2c997c07a4b7f15cbf97728006a79e.json').read_text())
        self.blob='4f1114a841e1adc5039c518ab6a55eeec9e80509'
    def verify(self):return mod.verify(self.dossier,self.witness,self.raw,self.blob)
    def reject(self):
        with self.assertRaises(mod.OriginSourceError):self.verify()
    def test_bound_positive_does_not_upgrade_origin(self):
        x=self.verify()
        self.assertFalse(x['historical_chad_execution_attested'])
        self.assertFalse(x['remote_platform_verified_here'])
    def test_untrusted_blob_rejected(self):
        self.blob='0'*40;self.reject()
    def test_untrusted_digest_rejected(self):
        self.dossier['platform_execution']['protected_witness']['sha256']='0'*64;self.reject()
    def test_wrong_run_id_rejected(self):
        self.witness['run_id']+=1;self.reject()
    def test_wrong_workflow_head_rejected(self):
        self.witness['workflow_sha']='0'*40;self.reject()
    def test_wrong_subject_rejected(self):
        self.dossier['subject']['head_sha']='0'*40;self.reject()
    def test_wrong_artifact_rejected(self):
        self.dossier['platform_execution']['origin_artifact_id']=0;self.reject()
    def test_tampered_raw_output_rejected(self):
        self.witness['executions'][0]['stderr']+='tampered';self.reject()
    def test_duplicate_role_rejected(self):
        self.witness['executions'][1]['role']='VERIFIER';self.reject()
    def test_bad_dossier_digest_rejected(self):
        self.dossier['platform_execution']['role_output_sha256']['REFEREE']='0'*64;self.reject()
    def test_false_historical_claim_rejected(self):
        self.dossier['claims']['historical_2026_10_15_chad_execution_authenticated']=True;self.reject()
    def test_false_mathematical_claim_rejected(self):
        self.dossier['claims']['mathematical_certification']=True;self.reject()

if __name__=='__main__':unittest.main()
