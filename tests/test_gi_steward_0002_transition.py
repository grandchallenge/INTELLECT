from __future__ import annotations

import json
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DIRECTIVE = (
    ROOT / "governance" / "steward_directives" / "GI-STEWARD-0002.md"
)
SCHEMA = ROOT / "schemas" / "constitutional_authority_schedule.schema.json"
SCHEDULE = ROOT / "governance" / "constitutional_authority_schedule.json"


class MinimumSteadyStateHumanGovernanceTests(unittest.TestCase):
    def test_directive_preserves_one_human_exact_packet_boundary(self) -> None:
        text = DIRECTIVE.read_text(encoding="utf-8")
        for required in (
            "**Ordinary Human Steward:** `fyremael`",
            "**Recovery owner:** `jimsteeg`",
            "one substantive, authenticated,\nrole-bound authorization",
            "not a mandatory reviewer or second signer",
            "one non-author agent Adversary finding",
            "one different non-author agent Referee finding from a distinct session",
            "Automation may\nassemble, validate, route, and replay the packet. It may not manufacture the\nSteward authorization",
            "standing, exact authorization granted by `fyremael`",
            "single-use continuity\n  authorizer",
            "replacement must be an authenticated human other than\n  `jimsteeg`",
            "Restoration may not change roles or permissions",
            "routes to\n  the Steward-replacement protocol instead of assuming unavailable credentials",
            "authorizes no recovery or destructive operation unless every\nexact trigger, evidence, packet, and role restriction above is satisfied",
            "Satisfying any condition in isolation grants no authority",
            "Custody, review, a green check, or merge of this\nfile does not activate it.",
            "Rollback requires a later exact Human Steward directive",
        ):
            self.assertIn(required, text)

    def test_schedule_schema_names_only_the_exact_directive_sequence(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(
            schema["properties"]["schema_version"]["enum"],
            ["1.4.0", "1.5.0"],
        )
        staffing = schema["properties"]["staffing"]["properties"]
        self.assertEqual(
            staffing["directive"]["properties"]["identifier"]["enum"],
            ["GI-STEWARD-0001", "GI-STEWARD-0002"],
        )
        self.assertEqual(staffing["ordinary_human_steward"]["const"], "fyremael")
        self.assertEqual(staffing["recovery_owner"]["const"], "jimsteeg")
        self.assertEqual(
            staffing["human_actions_per_governed_decision_target"]["const"], 1
        )
        self.assertEqual(
            staffing["supersession"]["properties"]["predecessor"]["const"],
            "GI-STEWARD-0001",
        )
        self.assertEqual(
            staffing["supersession"]["properties"]["organization_2fa"]["const"][
                "evidence_sha256"
            ],
            "dcf18dabdafe717045188cfed7d3a0ccbc59c44707296045d69d5736c9b55611",
        )
        self.assertFalse(
            staffing["recovery_protocols"]["const"]["steward_replacement"][
                "recovery_owner_self_promotion_allowed"
            ]
        )
        replacement = staffing["recovery_protocols"]["const"][
            "steward_replacement"
        ]
        self.assertEqual(
            replacement["authorization_source"],
            "standing_exact_directive_authorization_by_fyremael",
        )
        self.assertFalse(replacement["incumbent_authorization_required_at_trigger"])
        self.assertTrue(
            replacement["replacement_candidate_must_differ_from_recovery_owner"]
        )
        account = staffing["recovery_protocols"]["const"]["account_recovery"]
        self.assertTrue(account["bounded_access_restoration_precedes_authorization"])
        self.assertFalse(
            account["role_or_permission_change_allowed_during_restoration"]
        )
        self.assertEqual(account["unrecoverable_route"], "steward_replacement")

    def test_recovery_protocols_fail_closed_against_circular_or_unilateral_routes(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        recovery_schema = schema["properties"]["staffing"]["properties"][
            "recovery_protocols"
        ]
        expected = recovery_schema["const"]
        jsonschema.validate(expected, recovery_schema)

        for mutate in (
            lambda value: value["steward_replacement"].__setitem__(
                "incumbent_authorization_required_at_trigger", True
            ),
            lambda value: value["steward_replacement"].__setitem__(
                "recovery_owner_self_promotion_allowed", True
            ),
            lambda value: value["steward_replacement"].__setitem__(
                "replacement_candidate_must_differ_from_recovery_owner", False
            ),
            lambda value: value["account_recovery"].__setitem__(
                "role_or_permission_change_allowed_during_restoration", True
            ),
            lambda value: value["account_recovery"].__setitem__(
                "unrecoverable_route", "recovery_owner_discretion"
            ),
            lambda value: value["organization_deletion"]["initiators"].append(
                "jimsteeg"
            ),
        ):
            candidate = json.loads(json.dumps(expected))
            mutate(candidate)
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(candidate, recovery_schema)

    def test_schedule_versions_are_mutually_exclusive(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        current = json.loads(SCHEDULE.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(
            current,
            schema,
            cls=jsonschema.Draft202012Validator,
            format_checker=jsonschema.FormatChecker(),
        )

        mixed = json.loads(json.dumps(current))
        mixed["schema_version"] = "1.5.0"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mixed, schema)

        smuggled = json.loads(json.dumps(current))
        smuggled["staffing"]["recovery_owner"] = "jimsteeg"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(smuggled, schema)


if __name__ == "__main__":
    unittest.main()
