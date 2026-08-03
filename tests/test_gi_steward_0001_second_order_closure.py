from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ATTESTATION = (
    ROOT
    / "governance"
    / "attestations"
    / "GI-STEWARD-0001-HUMAN-STEWARD-ROSTER-002.md"
)


class StewardRosterSecondOrderClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = ATTESTATION.read_text(encoding="utf-8")

    def test_exact_record_chain_is_bound(self) -> None:
        required = (
            "fac641298b7762d4e9a4e5faa98468af5b756463",
            "f479737bb1440505b21a00693c10fb96b244501a",
            "f314072d38bbbad44bce15f1a305e7699a3f146a",
            "e63218db0748ab6c8d4baf6a8286a5db4ab89fc2",
            "d5f70999b3dd037b06adf08d3186375613fbfd30",
            "5163711280",
            "4841857703",
            "5163767209",
        )
        for identity in required:
            with self.subTest(identity=identity):
                self.assertIn(identity, self.text)

    def test_distinct_agent_referee_is_named(self) -> None:
        self.assertIn(
            "openai-gpt-5.6-thinking-stewardship-referee", self.text
        )
        self.assertIn(
            "gpt-5.6-thinking-stewardship-referee-20260803T075700Z",
            self.text,
        )
        self.assertIn("substantive independent documentary review", self.text)

    def test_failed_conditions_are_not_concealed(self) -> None:
        self.assertIn("disposition was stale", self.text)
        self.assertIn("approval was also non-qualifying", self.text)
        self.assertIn("does not rewrite history", self.text)

    def test_operating_model_and_campaign_boundary_are_preserved(self) -> None:
        self.assertIn("`fyremael` and `jimsteeg`", self.text)
        self.assertIn("one acting Human Steward", self.text)
        self.assertIn(
            "cc007ca6fe0437d5906d84beada789852ab048e398bfb15924e3516e4c0c9d79",
            self.text,
        )
        self.assertIn(
            "governance/reviews/GI-AMEND-0001-cc007ca6fe04.json",
            self.text,
        )
        self.assertIn("does not activate", self.text)


if __name__ == "__main__":
    unittest.main()
