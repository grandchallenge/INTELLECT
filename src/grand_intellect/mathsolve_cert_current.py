from __future__ import annotations

from typing import Any, Mapping

from .constitution import GateReport
from .engine import GrandIntellect
from .fabric import CoordinationFabric
from .mathsolve_cert_reviewed import (
    ADJUDICATED_HANDOFF_STATES,
    ALL_HANDOFF_STATES,
    INTAKE_HANDOFF_STATES,
    PROMOTING_HANDOFF_STATES,
    GitHubArtifactRef,
    MathematicalConstitution as _HistoricalMathematicalConstitution,
    MathematicalGrandIntellect as _HistoricalMathematicalGrandIntellect,
    MathSolveProvider as _HistoricalMathSolveProvider,
    _valid_artifact_ref,
)
from .model import Phase, WorkPackageState

PROGRAMME_POLICY_COMMIT = "6c0b3e55eeca9be1ef5a538b0fb659f3bf1045a2"
PROGRAMME_POLICY_PATH = "governance/mathsolve_routing_audit.json"
PROGRAMME_POLICY_DIGEST = "4a27ec8aaaa60f919ba51028807b83dc522bfcff"
PROGRAMME_UMBRELLA_STATE_PATH = "governance/umbrella_current_state_conformance.json"
PROGRAMME_UMBRELLA_STATE_DIGEST = "a2a1c3d590f535972c87f57d9b86155a246a61ba"
MATHCERT_PROVIDER_COMMIT = "0258e4f0bca0d90fac05b62aeef108f16dccffdd"
MATHCERT_ROUTE_REGISTRY_PATH = "governance/certification_routes.json"
MATHCERT_ROUTE_REGISTRY_DIGEST = "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1"

_OBSOLETE_CONTRACT_DIAGNOSTICS = {
    "mathematical route programme_policy identity drift",
    "mathematical route certification_contract identity drift",
    "mathematical route requires content-addressed programme_policy",
    "mathematical route requires content-addressed certification_contract",
}


class MathSolveProvider(_HistoricalMathSolveProvider):
    """Provider bound to the current Programme and Cert umbrella contracts."""

    def _programme_policy(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATH-PROGRAMME",
            commit_sha=PROGRAMME_POLICY_COMMIT,
            artifact_path=PROGRAMME_POLICY_PATH,
            digest_algorithm="git_blob_sha1",
            digest=PROGRAMME_POLICY_DIGEST,
            issue="https://github.com/grandchallenge/MATH-PROGRAMME/issues/159",
            pull_request="https://github.com/grandchallenge/MATH-PROGRAMME/pull/160",
        ).to_dict()

    def _umbrella_current_state(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATH-PROGRAMME",
            commit_sha=PROGRAMME_POLICY_COMMIT,
            artifact_path=PROGRAMME_UMBRELLA_STATE_PATH,
            digest_algorithm="git_blob_sha1",
            digest=PROGRAMME_UMBRELLA_STATE_DIGEST,
            issue="https://github.com/grandchallenge/MATH-PROGRAMME/issues/159",
            pull_request="https://github.com/grandchallenge/MATH-PROGRAMME/pull/160",
        ).to_dict()

    def _certification_contract(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATHCERT",
            commit_sha=MATHCERT_PROVIDER_COMMIT,
            artifact_path=MATHCERT_ROUTE_REGISTRY_PATH,
            digest_algorithm="git_blob_sha1",
            digest=MATHCERT_ROUTE_REGISTRY_DIGEST,
            issue="https://github.com/grandchallenge/MATHCERT/issues/36",
            pull_request="https://github.com/grandchallenge/MATHCERT/pull/40",
        ).to_dict()

    def governed_route(self, **fields: Any) -> dict[str, Any]:
        route = super().governed_route(**fields)
        route["programme_policy"] = self._programme_policy()
        route["programme_umbrella_state"] = self._umbrella_current_state()
        route["certification_contract"] = self._certification_contract()
        return route

    def exemption(self, **fields: Any) -> dict[str, Any]:
        exemption = super().exemption(**fields)
        exemption["programme_policy"] = self._programme_policy()
        exemption["programme_umbrella_state"] = self._umbrella_current_state()
        exemption["certification_contract"] = self._certification_contract()
        return exemption


class MathematicalConstitution(_HistoricalMathematicalConstitution):
    """Constitution enforcing the current three-artifact umbrella contract."""

    def evaluate(self, state: WorkPackageState) -> GateReport:
        report = super().evaluate(state)
        if not state.mathematical:
            return report

        satisfied = [
            item
            for item in report.satisfied
            if item != "Programme policy and MATHCERT route-registry identities are pinned"
        ]
        missing = [
            item for item in report.missing if item not in _OBSOLETE_CONTRACT_DIAGNOSTICS
        ]

        if state.phase in {Phase.SPECIFICATION, Phase.REALIZATION}:
            record = state.mathsolve_route or state.mathsolve_exemption
            if record is not None:
                contract_errors = current_provider_contract_errors(record)
                missing.extend(contract_errors)
                if not contract_errors:
                    satisfied.append(
                        "Programme routing, umbrella state, and MATHCERT registry identities are current"
                    )

        return GateReport(
            phase=report.phase,
            target_phase=report.target_phase,
            ready=not missing,
            satisfied=tuple(dict.fromkeys(satisfied)),
            missing=tuple(dict.fromkeys(missing)),
        )


class MathematicalGrandIntellect(_HistoricalMathematicalGrandIntellect):
    """Runtime using current Programme, umbrella, and Cert provider identities."""

    def __init__(
        self,
        fabric: CoordinationFabric,
        *,
        provider: MathSolveProvider | None = None,
        require_authoritative_fabric: bool = False,
    ) -> None:
        self.mathsolve_provider = provider or MathSolveProvider()
        GrandIntellect.__init__(
            self,
            fabric,
            constitution=MathematicalConstitution(),
            require_authoritative_fabric=require_authoritative_fabric,
        )


def current_provider_contract_errors(record: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = (
        (
            "programme_policy",
            "grandchallenge/MATH-PROGRAMME",
            PROGRAMME_POLICY_COMMIT,
            PROGRAMME_POLICY_PATH,
            PROGRAMME_POLICY_DIGEST,
        ),
        (
            "programme_umbrella_state",
            "grandchallenge/MATH-PROGRAMME",
            PROGRAMME_POLICY_COMMIT,
            PROGRAMME_UMBRELLA_STATE_PATH,
            PROGRAMME_UMBRELLA_STATE_DIGEST,
        ),
        (
            "certification_contract",
            "grandchallenge/MATHCERT",
            MATHCERT_PROVIDER_COMMIT,
            MATHCERT_ROUTE_REGISTRY_PATH,
            MATHCERT_ROUTE_REGISTRY_DIGEST,
        ),
    )
    for field, repository, commit, path, digest in expected:
        value = record.get(field)
        if not isinstance(value, Mapping) or not _valid_artifact_ref(value):
            errors.append(f"mathematical route requires content-addressed {field}")
            continue
        if (
            value.get("repository") != repository
            or value.get("commit_sha") != commit
            or value.get("artifact_path") != path
            or value.get("digest_algorithm") != "git_blob_sha1"
            or value.get("digest") != digest
        ):
            errors.append(f"mathematical route {field} identity drift")
    return errors


__all__ = [
    "ADJUDICATED_HANDOFF_STATES",
    "ALL_HANDOFF_STATES",
    "INTAKE_HANDOFF_STATES",
    "MATHCERT_PROVIDER_COMMIT",
    "MATHCERT_ROUTE_REGISTRY_DIGEST",
    "MATHCERT_ROUTE_REGISTRY_PATH",
    "PROGRAMME_POLICY_COMMIT",
    "PROGRAMME_POLICY_DIGEST",
    "PROGRAMME_POLICY_PATH",
    "PROGRAMME_UMBRELLA_STATE_DIGEST",
    "PROGRAMME_UMBRELLA_STATE_PATH",
    "PROMOTING_HANDOFF_STATES",
    "GitHubArtifactRef",
    "MathematicalConstitution",
    "MathematicalGrandIntellect",
    "MathSolveProvider",
    "current_provider_contract_errors",
]
