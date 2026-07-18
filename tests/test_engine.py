from __future__ import annotations

import unittest

from grand_intellect.engine import GateBlocked, GrandIntellect
from grand_intellect.fabric import InMemoryFabric
from grand_intellect.model import Decision, Disposition, Office, Phase, ReviewStatus


class GrandIntellectLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fabric = InMemoryFabric()
        self.system = GrandIntellect(self.fabric)
        self.wp = "WP-001"

    def approve_required(self) -> None:
        state = self.system.state(self.wp)
        for office in self.system.constitution.required_offices(state.phase):
            self.system.submit_review(
                self.wp,
                office=office,
                status=ReviewStatus.APPROVED,
                obligations=tuple(
                    sorted(
                        self.system.constitution.required_obligations(
                            state.phase, office
                        )
                    )
                ),
                evidence_refs=(
                    f"evidence://{state.phase.value}/{office.value}",
                ),
            )

    def advance(self) -> None:
        self.approve_required()
        report = self.system.gate_report(self.wp)
        self.assertTrue(report.ready, report.missing)
        self.system.advance(self.wp)

    def test_complete_epistemic_cycle(self) -> None:
        self.system.charter(
            self.wp,
            title="Constitutional vertical slice",
            purpose=(
                "Prove governed phase transitions over an append-only event fabric."
            ),
            scope="One work package from charter through disposal.",
            acceptance_criteria=(
                "All gates close",
                "Every transition is replayable",
            ),
            constraints=("No unreviewed phase transition",),
        )
        self.advance()
        self.assertEqual(self.system.state(self.wp).phase, Phase.GENERATION)

        self.system.register_alternative(
            self.wp,
            alternative_id="ALT-1",
            summary="Application-side gate evaluator",
            mechanism="Project events and evaluate an executable constitution.",
            assumptions=("AETHER provides ordered replay",),
            discriminating_test=(
                "Replay identical history twice and compare gate reports."
            ),
        )
        self.system.register_alternative(
            self.wp,
            alternative_id="ALT-2",
            summary="Pure semantic-kernel rules",
            mechanism="Encode every gate solely in AETHER Datalog.",
            assumptions=(
                "The current DSL expresses all cardinality constraints",
            ),
            discriminating_test=(
                "Compile the complete gate programme without host checks."
            ),
        )
        self.advance()

        self.system.record_specification(
            self.wp,
            claims=(
                "Transitions are denied until every obligation is satisfied",
            ),
            evaluation_contract={"tests": ["unit", "replay"], "required": True},
            reversal_conditions=(
                "A host check diverges from AETHER-derived truth",
            ),
            interfaces=("CoordinationFabric.append", "CoordinationFabric.history"),
        )
        self.advance()

        self.system.record_realization(
            self.wp,
            realization_id="R-1",
            artifact_refs=("src/grand_intellect",),
            verification_commands=(
                "python -m unittest discover -s tests -v",
            ),
        )
        self.advance()

        self.system.record_contact(
            self.wp,
            contact_id="CONTACT-1",
            claim="Blocked gates reject incomplete work packages.",
            method="Negative and end-to-end unit tests.",
            outcome="Incomplete transitions fail; the full cycle succeeds.",
            uncertainty="Live AETHER integration remains environment-dependent.",
            could_disconfirm=True,
            evidence_refs=("tests/test_engine.py",),
        )
        self.advance()

        self.system.record_judgment(
            self.wp,
            decision=Decision.ACCEPT,
            rationale=(
                "The vertical slice closes the constitutional lifecycle "
                "deterministically."
            ),
            selected_alternative_ids=("ALT-1",),
            tradeoffs=(
                "Application gates remain a policy cache, not semantic authority",
            ),
            reversal_conditions=(
                "AETHER replay produces a different event order",
            ),
        )
        self.advance()

        self.system.record_memory(
            self.wp,
            knowledge=(
                "The executable constitution can govern a complete work package "
                "lifecycle."
            ),
            reasons=(
                "Every phase transition was admitted by explicit checks and reviews",
            ),
            scope=(
                "Single-process application layer over a coordination-fabric protocol."
            ),
            limitations=("No live AETHER server was used by this unit test",),
            retrieval_tags=("constitution", "work-package", "aether"),
        )
        self.advance()

        self.system.record_disposal(
            self.wp,
            object_id="ALT-2",
            disposition=Disposition.ARCHIVED,
            reason=(
                "Deferred until the AETHER DSL supports the full gate programme "
                "ergonomically."
            ),
            recovery_path="ledger://WP-001/alternative/ALT-2",
        )
        self.system.record_frontier(
            self.wp,
            questions=(
                "Can every application gate be compiled into provenance-bearing "
                "AETHER rules?",
            ),
        )
        self.advance()
        self.assertEqual(self.system.state(self.wp).phase, Phase.COMPLETE)

    def test_gate_reports_missing_obligations(self) -> None:
        self.system.charter(
            self.wp,
            title="Incomplete charter",
            purpose="Exercise denial.",
            scope="Charter only.",
            acceptance_criteria=("Denied",),
        )
        report = self.system.gate_report(self.wp)
        self.assertFalse(report.ready)
        self.assertIn("approved review: referee", report.missing)
        with self.assertRaises(GateBlocked):
            self.system.advance(self.wp)

    def test_idempotent_charter_append(self) -> None:
        receipt = self.system.charter(
            self.wp,
            title="Idempotent charter",
            purpose="Prove append replay.",
            scope="One event.",
            acceptance_criteria=("One event exists",),
            idempotency_key="charter:WP-001",
        )
        replay = self.fabric.append([self.fabric.history(self.wp)[0]])
        self.assertTrue(replay.replayed)
        self.assertEqual(receipt.cut, replay.cut)
        self.assertEqual(len(self.fabric.history(self.wp)), 1)

    def test_reopen_complete_work_package(self) -> None:
        self.test_complete_epistemic_cycle()
        self.system.reopen(
            self.wp, reason="New evidence invalidated an assumption"
        )
        self.assertEqual(self.system.state(self.wp).phase, Phase.GENERATION)

    def test_arbitrary_obligation_does_not_satisfy_office_contract(self) -> None:
        self.system.charter(
            self.wp,
            title="Exact obligations",
            purpose="Reject ceremonial review.",
            scope="Charter gate.",
            acceptance_criteria=("Exact obligation required",),
        )
        self.system.submit_review(
            self.wp,
            office=Office.REFEREE,
            status=ReviewStatus.APPROVED,
            obligations=("looked at it",),
        )
        report = self.system.gate_report(self.wp)
        self.assertIn(
            "obligation: referee/referee.acceptance_testable", report.missing
        )

    def test_later_changes_requested_revokes_prior_approval(self) -> None:
        self.system.charter(
            self.wp,
            title="Review revocation",
            purpose="Ensure latest review controls.",
            scope="Charter gate.",
            acceptance_criteria=("Revocation blocks",),
        )
        phase = self.system.state(self.wp).phase
        obligations = tuple(
            sorted(
                self.system.constitution.required_obligations(
                    phase, Office.REFEREE
                )
            )
        )
        self.system.submit_review(
            self.wp,
            office=Office.REFEREE,
            status=ReviewStatus.APPROVED,
            obligations=obligations,
        )
        self.system.submit_review(
            self.wp,
            office=Office.REFEREE,
            status=ReviewStatus.CHANGES_REQUESTED,
            obligations=obligations,
            findings=("Acceptance criterion is ambiguous",),
        )
        self.assertIn(
            "approved review: referee", self.system.gate_report(self.wp).missing
        )

    def test_authoritative_mode_rejects_test_fabric(self) -> None:
        with self.assertRaisesRegex(ValueError, "authoritative deployment"):
            GrandIntellect(InMemoryFabric(), require_authoritative_fabric=True)

    def test_deletion_requires_explicit_authorization(self) -> None:
        self.system.charter(
            self.wp,
            title="Deletion authority",
            purpose="Prove irreversible disposal fails closed.",
            scope="One disposal command.",
            acceptance_criteria=("Unauthorised deletion is rejected",),
        )
        self.advance()
        for index in range(2):
            self.system.register_alternative(
                self.wp,
                alternative_id=f"ALT-{index}",
                summary=f"Alternative {index}",
                mechanism="Distinct mechanism",
                assumptions=("Declared assumption",),
                discriminating_test=f"Test {index}",
            )
        self.advance()
        self.system.record_specification(
            self.wp,
            claims=("Claim",),
            evaluation_contract={"test": "fails on defect"},
            reversal_conditions=("Contradictory evidence",),
        )
        self.advance()
        self.system.record_realization(
            self.wp,
            realization_id="R-1",
            artifact_refs=("artifact://r1",),
            verification_commands=("verify-r1",),
        )
        self.advance()
        self.system.record_contact(
            self.wp,
            contact_id="C-1",
            claim="Claim",
            method="Discriminating test",
            outcome="Observed",
            uncertainty="Residual uncertainty",
            could_disconfirm=True,
        )
        self.advance()
        self.system.record_judgment(
            self.wp,
            decision=Decision.ACCEPT,
            rationale="Evidence met the declared burden.",
            selected_alternative_ids=("ALT-0",),
            tradeoffs=("Known trade-off",),
            reversal_conditions=("Contradictory evidence",),
        )
        self.advance()
        self.system.record_memory(
            self.wp,
            knowledge="Retain the reasons.",
            reasons=("Reason",),
            scope="This work package",
            limitations=("Known limitation",),
            retrieval_tags=("deletion",),
        )
        self.advance()
        with self.assertRaisesRegex(ValueError, "explicit authorization"):
            self.system.record_disposal(
                self.wp,
                object_id="artifact://r1",
                disposition=Disposition.DELETED,
                reason="No longer retained",
            )


if __name__ == "__main__":
    unittest.main()
