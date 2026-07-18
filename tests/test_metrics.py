from __future__ import annotations

import unittest

from grand_intellect.engine import GrandIntellect
from grand_intellect.fabric import InMemoryFabric
from grand_intellect.metrics import calculate_metrics
from grand_intellect.model import Office, ReviewStatus


class MetricsTests(unittest.TestCase):
    def test_metrics_reflect_exact_current_review_coverage(self) -> None:
        system = GrandIntellect(InMemoryFabric())
        system.charter(
            "WP-METRICS",
            title="Metrics",
            purpose="Measure governance state.",
            scope="Charter phase.",
            acceptance_criteria=("Coverage is exact",),
        )
        phase = system.state("WP-METRICS").phase
        office = Office.AXIOMATIST
        system.submit_review(
            "WP-METRICS",
            office=office,
            status=ReviewStatus.APPROVED,
            obligations=tuple(
                sorted(system.constitution.required_obligations(phase, office))
            ),
        )
        metrics = calculate_metrics(system.state("WP-METRICS"), system.constitution)
        self.assertEqual(metrics.current_required_office_count, 4)
        self.assertEqual(metrics.current_satisfied_office_count, 1)
        self.assertEqual(metrics.current_review_coverage, 0.25)
        self.assertFalse(metrics.gate_ready)

    def test_transition_count_excludes_governed_reopenings(self) -> None:
        system = GrandIntellect(InMemoryFabric())
        wp = "WP-METRIC-TRANSITIONS"
        system.charter(
            wp,
            title="Transition metrics",
            purpose="Count ordinary transitions separately from reopenings.",
            scope="One lifecycle.",
            acceptance_criteria=("Counts are exact",),
        )

        state = system.state(wp)
        for office in system.constitution.required_offices(state.phase):
            system.submit_review(
                wp,
                office=office,
                status=ReviewStatus.APPROVED,
                obligations=tuple(
                    sorted(
                        system.constitution.required_obligations(
                            state.phase, office
                        )
                    )
                ),
            )
        system.advance(wp)

        metrics = calculate_metrics(system.state(wp), system.constitution)
        self.assertEqual(metrics.transition_count, 1)
        self.assertEqual(metrics.reopening_count, 0)


if __name__ == "__main__":
    unittest.main()
