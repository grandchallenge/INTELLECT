"""Grand Intellect constitutional runtime."""

from .agents import AgentCouncil, AgentRegistry, OfficeAgent
from .constitution import Constitution, GateReport
from .engine import GrandIntellect
from .fabric import InMemoryFabric
from .metrics import WorkPackageMetrics, calculate_metrics
from .model import Office, Phase, ReviewStatus
from .workspace import WorkPackageWorkspace

__all__ = [
    "AgentCouncil",
    "AgentRegistry",
    "OfficeAgent",
    "Constitution",
    "GateReport",
    "GrandIntellect",
    "InMemoryFabric",
    "Office",
    "WorkPackageMetrics",
    "calculate_metrics",
    "Phase",
    "ReviewStatus",
    "WorkPackageWorkspace",
]

__version__ = "0.1.0"
