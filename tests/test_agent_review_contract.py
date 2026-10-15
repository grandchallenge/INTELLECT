"""Contract tests: multi-role / one account; exact-head and false independence."""
from __future__ import annotations

import copy
import unittest

from grand_intellect.agent_review_contract import (
    AgentReviewContractError, validate_later_anchor, validate_review_dossier,
)

H = "a" * 40
D = "b" * 64


def example():
    passes = []
    for role in ("VERIFIER", "ADVERSARY", "REFEREE"):
        passes.append({
            "role": role,
            "logical_pass_id": "PASS-" + role,
            "reviewer_system_id": "same-agent-system",
            "transport_login": "single-institutional-account",
            "subject_head_sha": H,
            "mode": "non_authoring_read_only",
            "write_set": [],
            "read_set": ["src:sha:" + H],
            "checks": [{"command": "python -m unittest",
                        "exit_code": 0,
                        "receipt_sha256": D}],
            "negative_controls": ["deny-untrusted-mutating-input"] if
                                 role == "ADVERSARY" else [],
            "finding": "ACCEPT_BOUNDED",
            "unresolved": []
        })
    return {
        "record_type": "GCL_AGENT_REVIEW_DOSSIER_V1",
        "subject": {"repository": "grandchallenge/MATH-PROGRAMME",
                    "head_sha": H, "material_sha256": D},
        "work_class": "MATERIAL_CONTROL",
        "transport_login": "single-institutional-account",
        "passes": passes,
        "claimed_effects": {"mathematical_certification": False,
                            "reserved_authorization": False,
                            "credential_escalation": False},
    }


class AgentReviewContractTests(unittest.TestCase):
    def check_fail(self, mutation, match=None):
        data = example()
        mutation(data)
        with self.assertRaises(AgentReviewContractError) as e:
            validate_review_dossier(data)
        if match:
            self.assertIn(match, str(e.exception))

    def test_one_github_login_three_roles_is_valid(self):
        result = validate_review_dossier(example())
        self.assertTrue(result["eligible_for_separate_protected_review"])
        self.assertEqual(result["transport_logins_needed"], 1)
        self.assertEqual(result["reviewer_system_ids"], ["same-agent-system"])
        self.assertFalse(result["github_approval_created"])
        self.assertFalse(result["protected_review_performed"])

    def test_duplicate_logical_pass_is_invalid(self):
        self.check_fail(lambda d: d["passes"][1].update(logical_pass_id="PASS-VERIFIER"),
                        "duplicate")

    def test_wrong_review_role_order_invalid(self):
        self.check_fail(lambda d: d["passes"].reverse(), "ordered roles")

    def test_changed_exact_candidate_head_invalid(self):
        self.check_fail(lambda d: d["passes"][1].update(subject_head_sha="c"*40),
                        "source-bound")

    def test_review_mode_mutating_invalid(self):
        self.check_fail(lambda d: d["passes"][1].update(mode="authoring"),
                        "non-authoring")

    def test_write_set_nonempty_invalid(self):
        self.check_fail(lambda d: d["passes"][0]["write_set"].append("candidate"),
                        "attempted mutation")

    def test_neg_control_required(self):
        self.check_fail(lambda d: d["passes"][1].update(negative_controls=[]),
                        "adverse")

    def test_authentic_transport_identity_consistent(self):
        self.check_fail(lambda d: d["passes"][2].update(transport_login="fake-reviewer"),
                        "attributable")

    def test_check_digest_missing_invalid(self):
        self.check_fail(lambda d: d["passes"][0]["checks"][0].update(receipt_sha256="NA"),
                        "receipt")

    def test_failed_check_keeps_blocker(self):
        d = example()
        d["passes"][0]["checks"][0]["exit_code"] = 2
        result = validate_review_dossier(d)
        self.assertFalse(result["eligible_for_separate_protected_review"])
        self.assertIn("VERIFIER: failed check", result["blocking_objections"])

    def test_adverse_findings_not_overridden(self):
        d = example()
        d["passes"][1]["finding"] = "REVISE"
        d["passes"][1]["unresolved"] = ["malformed reviewer token"]
        self.assertFalse(validate_review_dossier(d)["eligible_for_separate_protected_review"])

    def test_review_cannot_certify_math(self):
        self.check_fail(lambda d: d["claimed_effects"].update(
            mathematical_certification=True), "overclaimed")

    def test_independent_method_required_for_science(self):
        self.check_fail(lambda d: d.update(work_class="MATHEMATICAL_CLAIM"),
                        "independent method")

    def test_distinct_method_with_receipt_not_equal_auto_certification(self):
        d = example()
        d["work_class"] = "MATHEMATICAL_CLAIM"
        d["independent_method_evidence"] = [{"method": "FORMAL_KERNEL",
                                             "receipt_sha256": D}]
        r = validate_review_dossier(d)
        self.assertTrue(r["eligible_for_separate_protected_review"])
        self.assertFalse(r["scientific_certification_created"])

    def test_self_referential_pr_head_forbidden(self):
        self.check_fail(lambda d: d.update(source_pr_head_sha="c"*40),
                        "cyclic")

    def test_review_anchor_belongs_to_later_receipt(self):
        d = example()
        later = {
            "record_type": "GCL_PROTECTED_ROLE_REVIEW_RECEIPT_V1",
            "subject": copy.deepcopy(d["subject"]),
            "source_protected_merge_verified": True,
            "source_review_anchor": {
                "source_pr_number": 123,
                "source_pr_head_sha": "c"*40,
                "approved_review_id": 456,
                "review_dossier_blob_sha": "d"*40
            }
        }
        validate_later_anchor(d, later)
        bad = copy.deepcopy(later)
        bad["subject"]["head_sha"] = "f"*40
        with self.assertRaises(AgentReviewContractError):
            validate_later_anchor(d, bad)

    def test_later_receipt_requires_protected_merge_and_real_review_id(self):
        d = example()
        r = {"record_type": "GCL_PROTECTED_ROLE_REVIEW_RECEIPT_V1",
             "subject": d["subject"], "source_protected_merge_verified": False,
             "source_review_anchor": {"source_pr_number": 10,
                                      "source_pr_head_sha": "c"*40,
                                      "approved_review_id": 0,
                                      "review_dossier_blob_sha": "d"*40}}
        with self.assertRaises(AgentReviewContractError):
            validate_later_anchor(d, r)
        r["source_review_anchor"]["approved_review_id"] = 1
        with self.assertRaisesRegex(AgentReviewContractError, "unprotected"):
            validate_later_anchor(d, r)


if __name__ == "__main__":
    unittest.main()
