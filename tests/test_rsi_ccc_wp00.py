from __future__ import annotations

import unittest

from grand_intellect.rsi_ccc_wp00 import (
    CONTEXT_ID,
    KERNEL_ID,
    MAX_DECLARED_COST,
    Candidate,
    admit,
    baseline_candidate,
    bounded_trace,
    capability_candidate,
    check_proposal,
    denotationally_equal,
    expected_answer,
    make_proposal,
    optimized_candidate,
)


class RsiCccWp00Tests(unittest.TestCase):
    def test_capability_extension_is_admitted(self) -> None:
        old = baseline_candidate()
        new = capability_candidate()
        proposal = make_proposal(old, new, "capability_extension")
        decision = check_proposal(old, proposal)
        self.assertTrue(decision.accepted)
        self.assertEqual(admit(old, proposal), new)
        self.assertLess(old.competence_domain, new.competence_domain)

    def test_semantics_preserving_optimization_is_admitted(self) -> None:
        old = capability_candidate()
        new = optimized_candidate()
        proposal = make_proposal(old, new, "semantics_preserving_optimization")
        decision = check_proposal(old, proposal)
        self.assertTrue(decision.accepted)
        self.assertTrue(denotationally_equal(old, new))
        self.assertLess(new.declared_cost, old.declared_cost)

    def test_bounded_trace_has_two_accepted_improvements(self) -> None:
        s0, s1, s2 = bounded_trace()
        self.assertLess(s0.competence_domain, s1.competence_domain)
        self.assertTrue(denotationally_equal(s1, s2))
        self.assertLess(s2.declared_cost, s1.declared_cost)

    def test_malformed_proposal_fails_closed(self) -> None:
        old = baseline_candidate()
        raw = {"wrong": "shape"}
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "malformed")
        self.assertEqual(admit(old, raw), old)

    def test_stale_base_fails_closed(self) -> None:
        old = baseline_candidate()
        raw = make_proposal(old, capability_candidate(), "capability_extension")
        raw["base_digest"] = "0" * 64
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "stale_base")
        self.assertEqual(admit(old, raw), old)

    def test_artifact_identity_mismatch_fails_closed(self) -> None:
        old = baseline_candidate()
        raw = make_proposal(old, capability_candidate(), "capability_extension")
        raw["candidate_digest"] = "f" * 64
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "artifact_identity_mismatch")
        self.assertEqual(admit(old, raw), old)

    def test_context_substitution_fails_closed(self) -> None:
        old = baseline_candidate()
        candidate = Candidate(
            "context-substitution",
            capability_candidate().answers,
            40,
            context_id="attacker-metric-v2",
            kernel_id=KERNEL_ID,
        )
        raw = make_proposal(old, candidate, "capability_extension")
        raw["context_id"] = "attacker-metric-v2"
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "context_substitution")
        self.assertEqual(admit(old, raw), old)

    def test_trust_kernel_mutation_fails_closed(self) -> None:
        old = baseline_candidate()
        candidate = Candidate(
            "kernel-substitution",
            capability_candidate().answers,
            40,
            context_id=CONTEXT_ID,
            kernel_id="candidate-controlled-kernel",
        )
        raw = make_proposal(old, candidate, "capability_extension")
        raw["kernel_id"] = "candidate-controlled-kernel"
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "trust_kernel_mutation")
        self.assertEqual(admit(old, raw), old)

    def test_resource_bound_fails_closed(self) -> None:
        old = baseline_candidate()
        candidate = Candidate(
            "too-expensive",
            capability_candidate().answers,
            MAX_DECLARED_COST + 1,
        )
        raw = make_proposal(old, candidate, "capability_extension")
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "resource_bound")
        self.assertEqual(admit(old, raw), old)

    def test_unsafe_candidate_fails_closed(self) -> None:
        old = baseline_candidate()
        answers = list(capability_candidate().answers)
        answers[7] = not expected_answer(7)
        candidate = Candidate("unsafe", tuple(answers), 40)
        raw = make_proposal(old, candidate, "capability_extension")
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "unsafe_candidate")
        self.assertEqual(admit(old, raw), old)

    def test_non_refinement_fails_closed(self) -> None:
        old = baseline_candidate()
        answers = list(capability_candidate().answers)
        answers[0] = None
        candidate = Candidate("drops-old-domain", tuple(answers), 40)
        raw = make_proposal(old, candidate, "capability_extension")
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "non_refinement")
        self.assertEqual(admit(old, raw), old)

    def test_non_improvement_fails_closed(self) -> None:
        old = capability_candidate()
        candidate = Candidate("same", old.answers, old.declared_cost)
        raw = make_proposal(old, candidate, "semantics_preserving_optimization")
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "non_improvement")
        self.assertEqual(admit(old, raw), old)

    def test_unknown_improvement_mode_fails_closed(self) -> None:
        old = baseline_candidate()
        raw = make_proposal(old, capability_candidate(), "candidate_defined_metric")
        decision = check_proposal(old, raw)
        self.assertEqual(decision.code, "non_improvement")
        self.assertEqual(admit(old, raw), old)


if __name__ == "__main__":
    unittest.main()
