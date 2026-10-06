from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AMENDMENT_PATH = ROOT / "AMENDMENTS" / "0001-commentary-and-gcl-ghos.md"
SCHEDULE_PATH = ROOT / "governance" / "constitutional_authority_schedule.json"
RECEIPT_PATH = (
    ROOT / "governance" / "reviews" / "GI-AMEND-0001-22dbfa0ea0e6.json"
)
FIELD_RE = re.compile(r"^\*\*(?P<key>[^*]+):\*\* (?P<value>.+)$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


class DocumentaryClosureError(ValueError):
    pass


def metadata_from(text: str) -> dict[str, str]:
    header, separator, _ = text.partition("\n## Recitals")
    if not separator:
        raise DocumentaryClosureError("amendment recitals separator is missing")
    fields: dict[str, str] = {}
    for line in header.splitlines():
        match = FIELD_RE.fullmatch(line)
        if match:
            fields[match.group("key")] = match.group("value")
    return fields


def validate_metadata(fields: dict[str, str]) -> None:
    expected = {
        "Status": "Effective",
        "Effective constitutional version": "1.1.0",
        "Activation record": "`governance/constitutional_authority_schedule.json`",
        "Activation merge": (
            "`grandchallenge/INTELLECT#42` at "
            "`8d47ed8930d33253ae476c64dfec7c748185a535`"
        ),
        "Effective at": "`2026-08-03T10:00:00Z`",
        "Review packet": (
            "`22dbfa0ea0e652161126dd4647477036b89e6c13ecbd9101cda60ce00e9f95c5`"
        ),
        "Review receipt": (
            "`governance/reviews/GI-AMEND-0001-22dbfa0ea0e6.json`"
        ),
        "Human Steward approval": (
            "`fyremael`; attestation comment `5164721769`; "
            "authenticated reaction `391939851`"
        ),
        "Agent Adversary review": (
            "`openai-gpt-5.6-thinking-final-head-adversary`; "
            "comment `5164348042`"
        ),
        "Agent Referee review": (
            "`openai-gpt-5.6-thinking-final-head-referee`; "
            "comment `5164535200`"
        ),
        "Related ADR": (
            "`docs/adr/0004-commentary-and-gcl-ghos-authority.md`; "
            "not yet accepted"
        ),
        "GCL-GHOS status at activation": "Candidate; not yet admitted",
    }
    for key, value in expected.items():
        if fields.get(key) != value:
            raise DocumentaryClosureError(f"incorrect documentary field: {key}")
    serialized = json.dumps(fields, sort_keys=True)
    for stale_or_inflated in (
        "Proposed; not in force",
        "Pending",
        "ADR-0001 accepted",
        "GCL-GHOS-00 admitted",
        "programme adoption active",
    ):
        if stale_or_inflated in serialized:
            raise DocumentaryClosureError(
                f"stale or inflated documentary claim: {stale_or_inflated}"
            )


class GIAmend0001DocumentaryClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = AMENDMENT_PATH.read_text(encoding="utf-8")
        self.fields = metadata_from(self.text)
        self.schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
        self.receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))

    def test_documentary_header_is_exact_and_current(self) -> None:
        validate_metadata(self.fields)
        merge_value = self.fields["Activation merge"].rsplit("`", 2)[1]
        packet_value = self.fields["Review packet"].strip("`")
        self.assertRegex(merge_value, COMMIT_RE)
        self.assertRegex(packet_value, DIGEST_RE)

    def test_header_binds_active_schedule_and_receipt(self) -> None:
        self.assertEqual(self.schedule["status"], "active")
        self.assertEqual(self.schedule["amendment"]["status"], "effective")
        self.assertEqual(self.schedule["constitution"]["effective_version"], "1.2.0")
        self.assertEqual(self.schedule["staffing_amendment"]["identifier"], "GI-AMEND-0002")
        self.assertEqual(
            self.schedule["operating_standard"]["status_at_activation"], "candidate"
        )
        self.assertEqual(
            self.schedule["activation"]["review_receipt"]["packet_sha256"],
            self.receipt["packet_sha256"],
        )
        self.assertEqual(
            self.schedule["activation"]["review_receipt"]["record_ref"],
            str(RECEIPT_PATH.relative_to(ROOT)).replace("\\", "/"),
        )
        self.assertEqual(
            self.fields["Review packet"].strip("`"),
            self.receipt["packet_sha256"],
        )
        self.assertEqual(
            self.fields["Effective at"].strip("`"),
            self.schedule["activation"]["effective_at"],
        )

    def test_documentary_effect_does_not_promote_subordinate_decisions(self) -> None:
        self.assertEqual(
            self.fields["Related ADR"],
            "`docs/adr/0004-commentary-and-gcl-ghos-authority.md`; not yet accepted",
        )
        self.assertEqual(
            self.fields["GCL-GHOS status at activation"],
            "Candidate; not yet admitted",
        )
        self.assertNotIn("MATH-PROGRAMME adoption", "\n".join(self.fields.values()))

    def test_mutation_rejects_premature_standard_admission(self) -> None:
        mutated = dict(self.fields)
        mutated["GCL-GHOS status at activation"] = "Accepted and admitted"
        with self.assertRaisesRegex(
            DocumentaryClosureError,
            "incorrect documentary field: GCL-GHOS status at activation",
        ):
            validate_metadata(mutated)

    def test_substantive_articles_remain_present(self) -> None:
        for article in range(1, 10):
            self.assertIn(f"## Article {article}:", self.text)
        self.assertIn("The activation record satisfied Article 8", self.text)
        self.assertIn(
            "Before activation was recorded, this amendment was a\nreviewable proposal",
            self.text,
        )
        self.assertNotIn(
            "Upon satisfaction of Article 8 and recorded Human Steward promulgation",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
