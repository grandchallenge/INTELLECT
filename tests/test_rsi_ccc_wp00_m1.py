from __future__ import annotations

from hashlib import sha1, sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "governance" / "rsi_ccc_wp00" / "manifest.json"
FROZEN_FORMAL_OBJECT_SHA256 = "1fca7a5e5bba2f4b59ccf9288a6a01129652091f86071c7be70022ea076d0edc"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return sha1(header + data).hexdigest()


class RsiCccWp00M1BindingTests(unittest.TestCase):
    def test_m1_remains_bound_to_frozen_m0_object(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        formal = manifest["formal_object"]
        formal_data = (ROOT / formal["path"]).read_bytes()

        self.assertEqual(formal["sha256"], FROZEN_FORMAL_OBJECT_SHA256)
        self.assertEqual(sha256(formal_data).hexdigest(), FROZEN_FORMAL_OBJECT_SHA256)
        self.assertEqual(git_blob_sha(formal_data), formal["git_blob_sha"])
        self.assertEqual(
            manifest["mechanization"]["must_bind_to_formal_object_sha256"],
            FROZEN_FORMAL_OBJECT_SHA256,
        )

    def test_m1_proof_artifacts_are_content_bound_and_non_promotable(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        mechanization = manifest["mechanization"]

        self.assertEqual(mechanization["status"], "in_progress")
        self.assertFalse(manifest["promotion_ready"])
        self.assertEqual(mechanization["issue"], 104)
        self.assertEqual(mechanization["lean_toolchain"], "leanprover/lean4:v4.34.0")

        records = mechanization["proof_artifacts"]
        self.assertGreaterEqual(len(records), 5)
        for record in records:
            data = (ROOT / record["path"]).read_bytes()
            self.assertEqual(git_blob_sha(data), record["git_blob_sha"])


if __name__ == "__main__":
    unittest.main()
