from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .constitution import Constitution, GateReport
from .engine import GrandIntellect
from .fabric import AppendReceipt, CoordinationFabric
from .model import Decision, Office, Phase, WorkPackageState

_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_DIGEST_LENGTHS = {
    "git_blob_sha1": 40,
    "git_tree_sha1": 40,
    "sha256": 64,
}
_COMPLETE_HANDOFF_STATES = {
    "ready",
    "submitted",
    "certified",
    "qualified",
    "rejected",
    "proof_debt",
}
_PROMOTING_HANDOFF_STATES = {"certified", "qualified"}


@dataclass(frozen=True, slots=True, init=False)
class GitHubArtifactRef:
    """An immutable GitHub artifact identity.

    A commit identifies the repository snapshot. ``digest_algorithm`` and
    ``digest`` identify the artifact at ``artifact_path``. Commit identifiers
    are not accepted as substitutes for artifact digests.

    The ``sha256`` keyword remains as a compatibility alias for the 0.2.0 API.
    """

    repository: str
    commit_sha: str
    artifact_path: str
    digest_algorithm: str
    digest: str
    issue: str | None
    pull_request: str | None

    def __init__(
        self,
        *,
        repository: str,
        commit_sha: str,
        artifact_path: str,
        digest_algorithm: str = "sha256",
        digest: str | None = None,
        sha256: str | None = None,
        issue: str | None = None,
        pull_request: str | None = None,
    ) -> None:
        if digest is not None and sha256 is not None:
            raise ValueError("supply digest or sha256, not both")
        if sha256 is not None:
            digest_algorithm = "sha256"
            digest = sha256
        normalized_digest = _required(digest, "digest")
        _validate_digest(digest_algorithm, normalized_digest)
        object.__setattr__(self, "repository", _repository(repository))
        object.__setattr__(self, "commit_sha", _commit(commit_sha))
        object.__setattr__(self, "artifact_path", _required(artifact_path, "artifact_path"))
        object.__setattr__(self, "digest_algorithm", digest_algorithm)
        object.__setattr__(self, "digest", normalized_digest)
        object.__setattr__(self, "issue", issue)
        object.__setattr__(self, "pull_request", pull_request)

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository": self.repository,
            "commit_sha": self.commit_sha,
            "artifact_path": self.artifact_path,
            "digest_algorithm": self.digest_algorithm,
            "digest": self.digest,
            "issue": self.issue,
            "pull_request": self.pull_request,
        }


@dataclass(frozen=True, slots=True)
class MathSolveProvider:
    """Construct governed Solve routes and reviewed exemptions."""

    repository: str = "grandchallenge/MATHSOLVE"
    certification_repository: str = "grandchallenge/MATHCERT"

    def governed_route(
        self,
        *,
        programme_ref: str,
        provider_work_package_id: str,
        provider_issue: str,
        provider_commit: str | None = None,
        forge_inputs: Iterable[GitHubArtifactRef] = (),
        artifact_manifest: Iterable[GitHubArtifactRef] = (),
        claim_ledger: GitHubArtifactRef | None = None,
        proof_obligation_dag: GitHubArtifactRef | None = None,
        failed_route_ledger: GitHubArtifactRef | None = None,
        resource_ledger: GitHubArtifactRef | None = None,
    ) -> dict[str, Any]:
        _repository(self.repository)
        if provider_commit is not None:
            _commit(provider_commit)
        return {
            "status": "governed",
            "authority": "github",
            "future_projection": "aether",
            "programme_ref": _required(programme_ref, "programme_ref"),
            "provider_repository": self.repository,
            "provider_work_package_id": _required(
                provider_work_package_id, "provider_work_package_id"
            ),
            "provider_issue": _required(provider_issue, "provider_issue"),
            "provider_commit": provider_commit,
            "forge_inputs": [item.to_dict() for item in forge_inputs],
            "artifact_manifest": [item.to_dict() for item in artifact_manifest],
            "claim_ledger": claim_ledger.to_dict() if claim_ledger else None,
            "proof_obligation_dag": (
                proof_obligation_dag.to_dict() if proof_obligation_dag else None
            ),
            "failed_route_ledger": (
                failed_route_ledger.to_dict() if failed_route_ledger else None
            ),
            "resource_ledger": resource_ledger.to_dict() if resource_ledger else None,
            "certification_repository": self.certification_repository,
        }

    def exemption(
        self,
        *,
        waiver_id: str,
        reason: str,
        scope: str,
        risks: Iterable[str],
        approving_offices: Iterable[Office],
        human_steward_authorization: str,
        review_condition: str,
    ) -> dict[str, Any]:
        offices = sorted({office.value for office in approving_offices})
        required = {Office.REFEREE.value, Office.STEWARD.value}
        if not required.issubset(offices):
            raise ValueError("an exemption requires Referee and Steward approval")
        return {
            "status": "exempted",
            "authority": "github",
            "future_projection": "aether",
            "waiver_id": _required(waiver_id, "waiver_id"),
            "reason": _required(reason, "reason"),
            "scope": _required(scope, "scope"),
            "risks": _nonempty(risks, "risks"),
            "approving_offices": offices,
            "human_steward_authorization": _required(
                human_steward_authorization, "human_steward_authorization"
            ),
            "review_condition": _required(review_condition, "review_condition"),
            "cert_handoff_required": True,
            "certification_repository": self.certification_repository,
        }


class MathematicalConstitution(Constitution):
    """Reviewed executable form of GI-MATH-INV-01."""

    def evaluate(self, state: WorkPackageState) -> GateReport:
        report = super().evaluate(state)
        if not state.mathematical:
            return report

        satisfied = list(report.satisfied)
        missing = list(report.missing)

        if state.phase == Phase.SPECIFICATION:
            if _has_admissible_route(state):
                satisfied.append("mathematics has a governed MATHSOLVE route or waiver")
            else:
                missing.append("mathematics requires a governed MATHSOLVE route or waiver")

        if state.phase == Phase.REALIZATION:
            if state.mathsolve_route is not None:
                route_missing = _completed_route_missing(state.mathsolve_route)
                if route_missing:
                    missing.extend(route_missing)
                else:
                    satisfied.append(
                        "MATHSOLVE realization lineage has commit and artifact identities"
                    )
            elif state.mathsolve_exemption is not None:
                if _admissible_exemption(state.mathsolve_exemption):
                    satisfied.append("MATHSOLVE exemption remains valid through realization")
                else:
                    missing.append("MATHSOLVE exemption is incomplete or invalid")
            else:
                missing.append("mathematical realization has no MATHSOLVE route or waiver")

        if state.phase == Phase.JUDGMENT:
            declared_claims = {
                str(claim).strip()
                for claim in (state.specification or {}).get("claims", [])
                if str(claim).strip()
            }
            registered_claims = {
                str(claim["claim_id"])
                for claim in state.mathematical_claims
                if str(claim.get("claim_id", "")).strip()
            }
            unregistered = sorted(declared_claims - registered_claims)
            undeclared = sorted(registered_claims - declared_claims)
            if unregistered:
                missing.append(
                    "mathematical claim records missing for specification claims: "
                    + ", ".join(unregistered)
                )
            if undeclared:
                missing.append(
                    "registered mathematical claims absent from specification: "
                    + ", ".join(undeclared)
                )

            for claim_id in sorted(declared_claims | registered_claims):
                handoff = state.mathcert_handoff_for(claim_id)
                if handoff is None:
                    missing.append(f"MATHCERT handoff missing for claim: {claim_id}")
                    continue
                status = str(handoff.get("status", ""))
                if status in _COMPLETE_HANDOFF_STATES and not _valid_handoff_artifact(handoff):
                    missing.append(
                        f"MATHCERT handoff for {claim_id} lacks commit-and-artifact identity"
                    )

            decision = str((state.judgment or {}).get("decision", ""))
            if decision in {Decision.ACCEPT.value, Decision.COMBINE.value}:
                nonpromotable = []
                for claim_id in sorted(declared_claims | registered_claims):
                    handoff = state.mathcert_handoff_for(claim_id)
                    status = str((handoff or {}).get("status", ""))
                    if status not in _PROMOTING_HANDOFF_STATES:
                        nonpromotable.append(f"{claim_id}:{status or 'missing'}")
                if nonpromotable:
                    missing.append(
                        "accepted mathematical claims require certified or qualified "
                        "MATHCERT dispositions: " + ", ".join(nonpromotable)
                    )

            if declared_claims and not any(
                item.startswith("MATHCERT handoff")
                or item.startswith("accepted mathematical claims")
                for item in missing
            ):
                satisfied.append("mathematical claims have disposition-compatible Cert handoffs")

        return GateReport(
            phase=report.phase,
            target_phase=report.target_phase,
            ready=not missing,
            satisfied=tuple(satisfied),
            missing=tuple(missing),
        )


class MathematicalGrandIntellect(GrandIntellect):
    """Grand Intellect runtime with reviewed Solve and Cert routing."""

    def __init__(
        self,
        fabric: CoordinationFabric,
        *,
        provider: MathSolveProvider | None = None,
        require_authoritative_fabric: bool = False,
    ) -> None:
        self.mathsolve_provider = provider or MathSolveProvider()
        super().__init__(
            fabric,
            constitution=MathematicalConstitution(),
            require_authoritative_fabric=require_authoritative_fabric,
        )

    def charter_mathematical(
        self,
        work_package_id: str,
        *,
        campaign_id: str,
        programme_ref: str,
        title: str,
        purpose: str,
        scope: str,
        acceptance_criteria: Iterable[str],
        constraints: Iterable[str] = (),
        stakeholders: Iterable[str] = (),
        actor: str = Office.HUMAN_STEWARD.value,
    ) -> tuple[AppendReceipt, AppendReceipt]:
        charter_receipt = self.charter(
            work_package_id,
            title=title,
            purpose=purpose,
            scope=scope,
            acceptance_criteria=acceptance_criteria,
            constraints=constraints,
            stakeholders=stakeholders,
            actor=actor,
        )
        declaration_receipt = self._append(
            "mathematics.declared",
            work_package_id,
            actor,
            {
                "campaign_id": _required(campaign_id, "campaign_id"),
                "programme_ref": _required(programme_ref, "programme_ref"),
                "routing_invariant": "GI-MATH-INV-01",
                "present_authority": "github",
                "future_projection": "aether",
            },
        )
        return charter_receipt, declaration_receipt

    def register_mathsolve_route(
        self, work_package_id: str, **route_fields: Any
    ) -> AppendReceipt:
        self._require_not_complete(work_package_id)
        return self._append(
            "mathsolve.route.recorded",
            work_package_id,
            Office.STEWARD.value,
            self.mathsolve_provider.governed_route(**route_fields),
        )

    def register_mathsolve_exemption(
        self, work_package_id: str, **exemption_fields: Any
    ) -> AppendReceipt:
        self._require_not_complete(work_package_id)
        return self._append(
            "mathsolve.exemption.recorded",
            work_package_id,
            Office.HUMAN_STEWARD.value,
            self.mathsolve_provider.exemption(**exemption_fields),
        )

    def register_mathematical_claim(
        self,
        work_package_id: str,
        *,
        claim_id: str,
        statement: str,
        claim_type: str,
        support_type: str,
        source_refs: Iterable[str],
        actor: str = Office.FORMALIST.value,
    ) -> AppendReceipt:
        state = self.state(work_package_id)
        if not state.mathematical:
            raise ValueError("mathematical claims require a mathematical charter")
        if state.phase in {Phase.CHARTER, Phase.GENERATION, Phase.COMPLETE}:
            raise ValueError("claim registration requires specification through disposal")
        return self._append(
            "mathematical.claim.registered",
            work_package_id,
            actor,
            {
                "claim_id": _required(claim_id, "claim_id"),
                "statement": _required(statement, "statement"),
                "claim_type": _required(claim_type, "claim_type"),
                "support_type": _required(support_type, "support_type"),
                "source_refs": _nonempty(source_refs, "source_refs"),
            },
        )

    def record_mathcert_handoff(
        self,
        work_package_id: str,
        *,
        handoff_id: str,
        issue: str,
        target_claim_ids: Iterable[str],
        status: str,
        commit_sha: str | None = None,
        artifact_path: str | None = None,
        digest_algorithm: str | None = None,
        digest: str | None = None,
        sha256: str | None = None,
        actor: str = Office.AMANUENSIS.value,
    ) -> AppendReceipt:
        state = self.state(work_package_id)
        claim_ids = _nonempty(target_claim_ids, "target_claim_ids")
        known = {str(claim["claim_id"]) for claim in state.mathematical_claims}
        unknown = sorted(set(claim_ids) - known)
        if unknown:
            raise ValueError(
                "MATHCERT handoff references unknown claims: " + ", ".join(unknown)
            )
        allowed = {"pending"} | _COMPLETE_HANDOFF_STATES
        if status not in allowed:
            raise ValueError(f"invalid MATHCERT status: {status}")

        if digest is not None and sha256 is not None:
            raise ValueError("supply digest or sha256, not both")
        if sha256 is not None:
            digest_algorithm = "sha256"
            digest = sha256
        supplied = [commit_sha, artifact_path, digest_algorithm, digest]
        if any(value is not None for value in supplied) and not all(
            value is not None for value in supplied
        ):
            raise ValueError(
                "commit_sha, artifact_path, digest_algorithm, and digest must be supplied together"
            )
        if status in _COMPLETE_HANDOFF_STATES and not all(
            value is not None for value in supplied
        ):
            raise ValueError(
                f"MATHCERT status {status} requires commit-and-artifact identity"
            )
        if commit_sha is not None:
            _commit(commit_sha)
            _required(artifact_path, "artifact_path")
            _validate_digest(str(digest_algorithm), str(digest))

        return self._append(
            "mathcert.handoff.recorded",
            work_package_id,
            actor,
            {
                "handoff_id": _required(handoff_id, "handoff_id"),
                "repository": self.mathsolve_provider.certification_repository,
                "issue": _required(issue, "issue"),
                "target_claim_ids": claim_ids,
                "status": status,
                "commit_sha": commit_sha,
                "artifact_path": artifact_path,
                "digest_algorithm": digest_algorithm,
                "digest": digest,
                "authority": "github",
                "future_projection": "aether",
            },
        )

    def _require_not_complete(self, work_package_id: str) -> None:
        if self.state(work_package_id).phase == Phase.COMPLETE:
            raise ValueError("completed work must be reopened before its route changes")


def _has_admissible_route(state: WorkPackageState) -> bool:
    if state.mathsolve_route is not None:
        route = state.mathsolve_route
        return (
            route.get("status") == "governed"
            and route.get("authority") == "github"
            and route.get("provider_repository") == "grandchallenge/MATHSOLVE"
            and bool(str(route.get("provider_work_package_id", "")).strip())
            and bool(str(route.get("provider_issue", "")).strip())
            and bool(str(route.get("programme_ref", "")).strip())
        )
    if state.mathsolve_exemption is not None:
        return _admissible_exemption(state.mathsolve_exemption)
    return False


def _admissible_exemption(exemption: Mapping[str, Any]) -> bool:
    offices = set(exemption.get("approving_offices", []))
    return (
        exemption.get("status") == "exempted"
        and exemption.get("authority") == "github"
        and {Office.REFEREE.value, Office.STEWARD.value}.issubset(offices)
        and bool(str(exemption.get("waiver_id", "")).strip())
        and bool(str(exemption.get("reason", "")).strip())
        and bool(str(exemption.get("scope", "")).strip())
        and bool(exemption.get("risks"))
        and bool(str(exemption.get("human_steward_authorization", "")).strip())
        and bool(str(exemption.get("review_condition", "")).strip())
        and exemption.get("cert_handoff_required") is True
    )


def _completed_route_missing(route: Mapping[str, Any]) -> list[str]:
    missing: list[str] = []
    commit = route.get("provider_commit")
    if not isinstance(commit, str) or not _COMMIT_SHA.fullmatch(commit):
        missing.append("MATHSOLVE route requires an exact provider commit")
    manifest = route.get("artifact_manifest")
    if not isinstance(manifest, list) or not manifest:
        missing.append("MATHSOLVE route requires a nonempty artifact manifest")
    else:
        for index, item in enumerate(manifest):
            if not isinstance(item, Mapping) or not _valid_artifact_ref(item):
                missing.append(
                    f"MATHSOLVE artifact_manifest[{index}] lacks stable artifact identity"
                )
    for field, label in (
        ("claim_ledger", "claim ledger"),
        ("proof_obligation_dag", "proof-obligation DAG"),
    ):
        value = route.get(field)
        if not isinstance(value, Mapping) or not _valid_artifact_ref(value):
            missing.append(f"MATHSOLVE route requires a digest-bearing {label}")
    return missing


def _valid_artifact_ref(value: Mapping[str, Any]) -> bool:
    try:
        _repository(str(value.get("repository", "")))
        _commit(str(value.get("commit_sha", "")))
        _required(value.get("artifact_path"), "artifact_path")
        _validate_digest(
            str(value.get("digest_algorithm", "")), str(value.get("digest", ""))
        )
    except ValueError:
        return False
    return True


def _valid_handoff_artifact(handoff: Mapping[str, Any]) -> bool:
    return _valid_artifact_ref(
        {
            "repository": handoff.get("repository"),
            "commit_sha": handoff.get("commit_sha"),
            "artifact_path": handoff.get("artifact_path"),
            "digest_algorithm": handoff.get("digest_algorithm"),
            "digest": handoff.get("digest"),
        }
    )


def _validate_digest(algorithm: str, digest: str) -> None:
    if algorithm not in _DIGEST_LENGTHS:
        raise ValueError(
            "digest_algorithm must be git_blob_sha1, git_tree_sha1, or sha256"
        )
    pattern = _HEX40 if _DIGEST_LENGTHS[algorithm] == 40 else _HEX64
    if not pattern.fullmatch(digest):
        raise ValueError(f"{algorithm} digest has invalid form")


def _required(value: Any, name: str) -> str:
    normalized = "" if value is None else str(value).strip()
    if not normalized:
        raise ValueError(f"{name} is required")
    return normalized


def _nonempty(values: Iterable[Any], name: str) -> list[str]:
    result = [str(value).strip() for value in values if str(value).strip()]
    if not result:
        raise ValueError(f"{name} must contain at least one value")
    return result


def _repository(value: str) -> str:
    normalized = _required(value, "repository")
    if not _REPOSITORY.fullmatch(normalized):
        raise ValueError("repository must use owner/name form")
    return normalized


def _commit(value: str) -> str:
    normalized = _required(value, "commit_sha")
    if not _COMMIT_SHA.fullmatch(normalized):
        raise ValueError("commit_sha must be a lowercase 40-character SHA")
    return normalized
