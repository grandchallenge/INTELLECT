from __future__ import annotations

import unittest

from grand_intellect.rsi_ccc_wp00 import (
    CONTEXT_ID,
    KERNEL_ID,
    check_proposal,
)
from grand_intellect.rsi_ccc_wp00_m2 import accepted_candidates


class RsiCccWp00M2ResourceLaunderingTests(unittest.TestCase):
    def test_hidden_resource_laundering_fails_closed(self) -> None:
        """A candidate may not move cost outside the fixed proposal schema."""
        _, _, _, _, current, optimized = accepted_candidates()
        proposal: dict[str, object] = {
            "base_digest": current.digest,
            "candidate": optimized.payload(),
            "candidate_digest": optimized.digest,
            "context_id": CONTEXT_ID,
            "kernel_id": KERNEL_ID,
            "mode": "semantics_preserving_optimization",
            "external_resource_cost": 1_000_000,
        }

        decision = check_proposal(current, proposal)
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.code, "malformed")
        self.assertIn("exact bounded schema", decision.detail)


if __name__ == "__main__":
    unittest.main()
