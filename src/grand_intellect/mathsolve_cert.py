from __future__ import annotations

from .engine import GrandIntellect
from .fabric import CoordinationFabric
from .mathsolve_cert_reviewed import (
    ADJUDICATED_HANDOFF_STATES,
    ALL_HANDOFF_STATES,
    INTAKE_HANDOFF_STATES,
    MATHCERT_PROVIDER_COMMIT,
    MATHCERT_ROUTE_REGISTRY_DIGEST,
    MATHCERT_ROUTE_REGISTRY_PATH,
    PROGRAMME_POLICY_COMMIT,
    PROGRAMME_POLICY_DIGEST,
    PROGRAMME_POLICY_PATH,
    PROMOTING_HANDOFF_STATES,
    GitHubArtifactRef,
    MathematicalConstitution as _ReviewedMathematicalConstitution,
    MathematicalGrandIntellect as _ReviewedMathematicalGrandIntellect,
    MathSolveProvider,
    _claim_ids,
)
from .model import Phase, WorkPackageState


class MathematicalConstitution(_ReviewedMathematicalConstitution):
    """Final reviewed constitution with fail-closed Integration lineage."""

    def evaluate(self, state: WorkPackageState):
        report = super().evaluate(state)
        if not state.mathematical or state.phase not in {Phase.JUDGMENT, Phase.INTEGRATION}:
            return report

        missing = list(report.missing)
        for claim_id in sorted(_claim_ids(state)):
            if state.mathcert_handoff_for(claim_id) is None:
                message = f"MATHCERT handoff missing for claim: {claim_id}"
                if message not in missing:
                    missing.append(message)
        return type(report)(
            phase=report.phase,
            target_phase=report.target_phase,
            ready=not missing,
            satisfied=report.satisfied,
            missing=tuple(missing),
        )


class MathematicalGrandIntellect(_ReviewedMathematicalGrandIntellect):
    """Runtime using the final reviewed mathematical constitution."""

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
    "PROMOTING_HANDOFF_STATES",
    "GitHubArtifactRef",
    "MathematicalConstitution",
    "MathematicalGrandIntellect",
    "MathSolveProvider",
]
