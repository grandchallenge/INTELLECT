from __future__ import annotations

import unittest
from dataclasses import dataclass

from grand_intellect.agents import (
    AgentContext,
    AgentCouncil,
    AgentRegistry,
    AgentReviewDecision,
)
from grand_intellect.engine import GrandIntellect
from grand_intellect.fabric import InMemoryFabric
from grand_intellect.model import Office, ReviewStatus


@dataclass
class ApprovingAgent:
    office: Office

    @property
    def agent_id(self) -> str:
        return f"agent:{self.office.value}"

    def review(self, context: AgentContext) -> AgentReviewDecision:
        return AgentReviewDecision(
            status=ReviewStatus.APPROVED,
            obligations=context.required_obligations,
            evidence_refs=(f"state://{context.work_package.work_package_id}",),
        )


class AgentCouncilTests(unittest.TestCase):
    def test_council_dispatches_distinct_required_offices(self) -> None:
        system = GrandIntellect(InMemoryFabric())
        system.charter(
            "WP-AGENTS",
            title="Agent dispatch",
            purpose="Prove office-bounded reviews.",
            scope="Charter gate.",
            acceptance_criteria=("Required offices review",),
        )
        registry = AgentRegistry()
        for office in system.constitution.required_offices(
            system.state("WP-AGENTS").phase
        ):
            registry.register(ApprovingAgent(office))
        decisions = AgentCouncil(system, registry).conduct_gate_review("WP-AGENTS")
        self.assertEqual(len(decisions), 4)
        self.assertTrue(system.gate_report("WP-AGENTS").ready)

    def test_one_agent_id_cannot_hold_two_offices(self) -> None:
        @dataclass
        class SharedIdentityAgent:
            office: Office
            agent_id: str = "agent:shared"

            def review(self, context: AgentContext) -> AgentReviewDecision:
                return AgentReviewDecision(
                    status=ReviewStatus.APPROVED,
                    obligations=context.required_obligations,
                )

        registry = AgentRegistry()
        registry.register(SharedIdentityAgent(Office.AXIOMATIST))
        with self.assertRaises(ValueError):
            registry.register(SharedIdentityAgent(Office.REFEREE))


if __name__ == "__main__":
    unittest.main()
