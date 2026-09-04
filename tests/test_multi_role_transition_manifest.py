from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance/staffing_transitions/GI-MULTI-ROLE-STAFFING-001/manifest.json"
SCHEMA = ROOT / "schemas/multi_role_transition_manifest.schema.json"


class MultiRoleTransitionManifestTests(unittest.TestCase):
    def test_manifest_is_closed_and_binds_exact_staged_artifacts(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        jsonschema.validate(manifest, schema)
        for artifact in manifest["artifacts"]:
            content = subprocess.run(
                ["git", "show", f":{artifact['path']}"], cwd=ROOT,
                check=True, capture_output=True,
            ).stdout
            self.assertEqual(hashlib.sha256(content).hexdigest(), artifact["sha256"])
            blob = subprocess.check_output(
                ["git", "rev-parse", f":{artifact['path']}"], cwd=ROOT, text=True,
            ).strip()
            self.assertEqual(blob, artifact["git_blob_sha1"])

    def test_activation_is_fail_closed_and_ordered(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        order = manifest["activation_order"]
        self.assertLess(order.index("obtain_one_exact_packet_human_steward_authorization"), order.index("merge_exact_pull_request_through_protected_controls"))
        self.assertIn("protected_merge_and_readback", manifest["unresolved_obligations"])


if __name__ == "__main__":
    unittest.main()
