from __future__ import annotations
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from grand_intellect.amendment_preparation import validate_preparation

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "governance/amendment_candidates/GI-AETHER-FABRIC-ARTICLE-XI-001"

class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "packet"
        shutil.copytree(PACKET, self.path)

    def rewrite(self, **changes):
        path = self.path / "packet.json"
        data = json.loads(path.read_text())
        data.update(changes)
        path.write_text(json.dumps(data))

    def check(self):
        return validate_preparation(self.path, ROOT / "CONSTITUTION.md")

    def test_candidate_valid_but_never_authorizes_effective_change(self):
        result = self.check()
        self.assertTrue(result["packet_valid"])
        self.assertFalse(result["ready_for_human_disposition"])
        self.assertFalse(result["effective_change_authorized"])

    def test_false_readiness_and_activation_rejected(self):
        for change in ({"status": "EFFECTIVE"}, {"ready_for_human_disposition": True}):
            with self.subTest(change=change):
                self.rewrite(status="PREPARATION_ONLY", ready_for_human_disposition=False)
                self.rewrite(**change)
                with self.assertRaises(ValueError): self.check()

    def test_removed_ambiguity_rejected(self):
        self.rewrite(unresolved_e0_seams=[f"AF-A{i:02}" for i in range(1,18)])
        with self.assertRaises(ValueError): self.check()

    def test_payload_drift_rejected(self):
        with (self.path / "ARTICLE-IX.proposed.md").open("a") as f: f.write("Extra authority")
        with self.assertRaises(ValueError): self.check()

    def test_forged_human_receipt_rejected_even_with_updated_digest(self):
        path = self.path / "human-steward-disposition.json"
        path.write_text(json.dumps({"status":"approved","reviewer":"agent"}))
        data = json.loads((self.path / "packet.json").read_text())
        data["files"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.rewrite(files=data["files"])
        with self.assertRaises(ValueError): self.check()

    def test_false_evidence_rejected(self):
        self.rewrite(e2_status="passed")
        with self.assertRaises(ValueError): self.check()

    def test_base_drift_rejected(self):
        self.rewrite(constitution_sha256="0"*64)
        with self.assertRaises(ValueError): self.check()
