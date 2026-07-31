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

PROGRAMME_POLICY_COMMIT = "d56edc23152f3ccde4c7db272b7af37f6cf698b9"
PROGRAMME_POLICY_PATH = "governance/mathsolve_routing_audit.json"
PROGRAMME_POLICY_DIGEST = "4a27ec8aaaa60f919ba51028807b83dc522bfcff"
PROGRAMME_RUNTIME_CONTRACT_PATH = "governance/umbrella_runtime_contract_v4.json"
PROGRAMME_RUNTIME_CONTRACT_DIGEST = "02cdfabb04f5d273fcb7531c515a73baab2bc52d"
PROGRAMME_CANDIDATE_ADMISSION_PATH = "governance/campaign_admission_registry.json"
PROGRAMME_CANDIDATE_ADMISSION_DIGEST = "a6bffaa197aa3921e3eb9d4f8a02b5dc2bbded24"
# Backward-compatible names for callers that imported the previous constants.
PROGRAMME_UMBRELLA_STATE_PATH = PROGRAMME_RUNTIME_CONTRACT_PATH
PROGRAMME_UMBRELLA_STATE_DIGEST = PROGRAMME_RUNTIME_CONTRACT_DIGEST
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
    """Provider bound to current Programme active, candidate, and Cert contracts."""

    def _programme_policy(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATH-PROGRAMME",
            commit_sha=PROGRAMME_POLICY_COMMIT,
            artifact_path=PROGRAMME_POLICY_PATH,
            digest_algorithm="git_blob_sha1",
            digest=PROGRAMME_POLICY_DIGEST,
            issue="https://github.com/grandchallenge/MATH-PROGRAMME/issues/175",
            pull_request="https://github.com/grandchallenge/MATH-PROGRAMME/pull/176",
        ).to_dict()

    def _programme_runtime_contract(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATH-PROGRAMME",
            commit_sha=PROGRAMME_POLICY_COMMIT,
            artifact_path=PROGRAMME_RUNTIME_CONTRACT_PATH,
            digest_algorithm="git_blob_sha1",
            digest=PROGRAMME_RUNTIME_CONTRACT_DIGEST,
            issue="https://github.com/grandchallenge/MATH-PROGRAMME/issues/175",
            pull_request="https://github.com/grandchallenge/MATH-PROGRAMME/pull/176",
        ).to_dict()

    def _programme_candidate_admission(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATH-PROGRAMME",
            commit_sha=PROGRAMME_POLICY_COMMIT,
            artifact_path=PROGRAMME_CANDIDATE_ADMISSION_PATH,
            digest_algorithm="git_blob_sha1",
            digest=PROGRAMME_CANDIDATE_ADMISSION_DIGEST,
            issue="https://github.com/grandchallenge/MATH-PROGRAMME/issues/175",
            pull_request="https://github.com/grandchallenge/MATH-PROGRAMME/pull/176",
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
        route["programme_runtime_contract"] = self._programme_runtime_contract()
        route["programme_candidate_admission"] = self._programme_candidate_admission()
        route.pop("programme_umbrella_state", None)
        route["certification_contract"] = self._certification_contract()
        return route

    def exemption(self, **fields: Any) -> dict[str, Any]:
        exemption = super().exemption(**fields)
        exemption["programme_policy"] = self._programme_policy()
        exemption["programme_runtime_contract"] = self._programme_runtime_contract()
        exemption["programme_candidate_admission"] = self._programme_candidate_admission()
        exemption.pop("programme_umbrella_state", None)
        exemption["certification_contract"] = self._certification_contract()
        return exemption


class MathematicalConstitution(_HistoricalMathematicalConstitution):
    """Constitution enforcing current active, candidate, runtime, and Cert identities."""

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
                        "Programme routing, reviewed candidate admission, runtime, and MATHCERT registry identities are current"
                    )

        return GateReport(
            phase=report.phase,
            target_phase=report.target_phase,
            ready=not missing,
            satisfied=tuple(dict.fromkeys(satisfied)),
            missing=tuple(dict.fromkeys(missing)),
        )


class MathematicalGrandIntellect(_HistoricalMathematicalGrandIntellect):
    """Runtime using current Programme and Cert provider identities."""

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
            "programme_runtime_contract",
            "grandchallenge/MATH-PROGRAMME",
            PROGRAMME_POLICY_COMMIT,
            PROGRAMME_RUNTIME_CONTRACT_PATH,
            PROGRAMME_RUNTIME_CONTRACT_DIGEST,
        ),
        (
            "programme_candidate_admission",
            "grandchallenge/MATH-PROGRAMME",
            PROGRAMME_POLICY_COMMIT,
            PROGRAMME_CANDIDATE_ADMISSION_PATH,
            PROGRAMME_CANDIDATE_ADMISSION_DIGEST,
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
    if "programme_umbrella_state" in record:
        errors.append("mathematical route contains superseded programme_umbrella_state")
    return errors


__all__ = [
    "ADJUDICATED_HANDOFF_STATES",
    "ALL_HANDOFF_STATES",
    "INTAKE_HANDOFF_STATES",
    "MATHCERT_PROVIDER_COMMIT",
    "MATHCERT_ROUTE_REGISTRY_DIGEST",
    "MATHCERT_ROUTE_REGISTRY_PATH",
    "PROGRAMME_CANDIDATE_ADMISSION_DIGEST",
    "PROGRAMME_CANDIDATE_ADMISSION_PATH",
    "PROGRAMME_POLICY_COMMIT",
    "PROGRAMME_POLICY_DIGEST",
    "PROGRAMME_POLICY_PATH",
    "PROGRAMME_RUNTIME_CONTRACT_DIGEST",
    "PROGRAMME_RUNTIME_CONTRACT_PATH",
    "PROGRAMME_UMBRELLA_STATE_DIGEST",
    "PROGRAMME_UMBRELLA_STATE_PATH",
    "PROMOTING_HANDOFF_STATES",
    "GitHubArtifactRef",
    "MathematicalConstitution",
    "MathematicalGrandIntellect",
    "MathSolveProvider",
    "current_provider_contract_errors",
]
