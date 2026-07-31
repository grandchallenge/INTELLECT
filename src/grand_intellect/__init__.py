"""Grand Intellect constitutional runtime."""

from .agents import AgentCouncil, AgentRegistry, OfficeAgent
from .constitution import Constitution, GateReport
from .engine import GrandIntellect
from .fabric import InMemoryFabric
from .mathsolve import (
    ADJUDICATED_HANDOFF_STATES,
    ALL_HANDOFF_STATES,
    INTAKE_HANDOFF_STATES,
    MATHCERT_PROVIDER_COMMIT,
    MATHCERT_ROUTE_REGISTRY_DIGEST,
    MATHCERT_ROUTE_REGISTRY_PATH,
    PROGRAMME_POLICY_COMMIT,
    PROGRAMME_POLICY_DIGEST,
    PROGRAMME_POLICY_PATH,
    PROGRAMME_RUNTIME_CONTRACT_DIGEST,
    PROGRAMME_RUNTIME_CONTRACT_PATH,
    PROGRAMME_UMBRELLA_STATE_DIGEST,
    PROGRAMME_UMBRELLA_STATE_PATH,
    PROMOTING_HANDOFF_STATES,
    GitHubArtifactRef,
    MathematicalConstitution,
    MathematicalGrandIntellect,
    MathSolveProvider,
)
from .metrics import WorkPackageMetrics, calculate_metrics
from .model import Office, Phase, ReviewStatus
from .workspace import WorkPackageWorkspace

__all__ = [
    "ADJUDICATED_HANDOFF_STATES",
    "ALL_HANDOFF_STATES",
    "AgentCouncil",
    "AgentRegistry",
    "Constitution",
    "GateReport",
    "GitHubArtifactRef",
    "GrandIntellect",
    "INTAKE_HANDOFF_STATES",
    "InMemoryFabric",
    "MATHCERT_PROVIDER_COMMIT",
    "MATHCERT_ROUTE_REGISTRY_DIGEST",
    "MATHCERT_ROUTE_REGISTRY_PATH",
    "MathematicalConstitution",
    "MathematicalGrandIntellect",
    "MathSolveProvider",
    "Office",
    "OfficeAgent",
    "PROGRAMME_POLICY_COMMIT",
    "PROGRAMME_POLICY_DIGEST",
    "PROGRAMME_POLICY_PATH",
    "PROGRAMME_RUNTIME_CONTRACT_DIGEST",
    "PROGRAMME_RUNTIME_CONTRACT_PATH",
    "PROGRAMME_UMBRELLA_STATE_DIGEST",
    "PROGRAMME_UMBRELLA_STATE_PATH",
    "PROMOTING_HANDOFF_STATES",
    "Phase",
    "ReviewStatus",
    "WorkPackageMetrics",
    "WorkPackageWorkspace",
    "calculate_metrics",
]

__version__ = "0.2.2"
