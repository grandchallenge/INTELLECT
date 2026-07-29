from __future__ import annotations

from typing import Any, Iterable, Mapping

from .constitution import GateReport
from .engine import GrandIntellect
from .fabric import AppendReceipt, CoordinationFabric
from .mathsolve_reviewed import (
    GitHubArtifactRef,
    MathematicalConstitution as _ReviewedMathematicalConstitution,
    MathematicalGrandIntellect as _ReviewedMathematicalGrandIntellect,
    MathSolveProvider as _ReviewedMathSolveProvider,
    _commit,
    _nonempty,
    _required,
    _valid_artifact_ref,
    _validate_digest,
)
from .model import Decision, Office, Phase, WorkPackageState

PROGRAMME_POLICY_COMMIT = "8182b8a5dc7b157d1a6b2a0f43d66c0598a2b072"
PROGRAMME_POLICY_PATH = "governance/mathsolve_routing_audit.json"
PROGRAMME_POLICY_DIGEST = "39e907cce79137168e5b2a240674d7f4e6f56cdd"
MATHCERT_PROVIDER_COMMIT = "3854dd1b4f6e162a7e74c3da1993f022ee691e5e"
MATHCERT_ROUTE_REGISTRY_PATH = "governance/certification_routes.json"
MATHCERT_ROUTE_REGISTRY_DIGEST = "065f0531e4d763b389b207d4922d5a85b4335ee3"

INTAKE_HANDOFF_STATES = {"pending", "ready", "submitted"}
ADJUDICATED_HANDOFF_STATES = {"certified", "qualified", "rejected", "proof_debt"}
PROMOTING_HANDOFF_STATES = {"certified", "qualified"}
ALL_HANDOFF_STATES = INTAKE_HANDOFF_STATES | ADJUDICATED_HANDOFF_STATES


class MathSolveProvider(_ReviewedMathSolveProvider):
    """Reviewed provider with exact Programme and Cert contract pins."""

    def _programme_policy(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATH-PROGRAMME",
            commit_sha=PROGRAMME_POLICY_COMMIT,
            artifact_path=PROGRAMME_POLICY_PATH,
            digest_algorithm="git_blob_sha1",
            digest=PROGRAMME_POLICY_DIGEST,
            issue="https://github.com/grandchallenge/MATH-PROGRAMME/issues/123",
            pull_request="https://github.com/grandchallenge/MATH-PROGRAMME/pull/124",
        ).to_dict()

    def _certification_contract(self) -> dict[str, Any]:
        return GitHubArtifactRef(
            repository="grandchallenge/MATHCERT",
            commit_sha=MATHCERT_PROVIDER_COMMIT,
            artifact_path=MATHCERT_ROUTE_REGISTRY_PATH,
            digest_algorithm="git_blob_sha1",
            digest=MATHCERT_ROUTE_REGISTRY_DIGEST,
            issue="https://github.com/grandchallenge/MATHCERT/issues/31",
            pull_request="https://github.com/grandchallenge/MATHCERT/pull/32",
        ).to_dict()

    def governed_route(self, **fields: Any) -> dict[str, Any]:
        route = super().governed_route(**fields)
        route["programme_policy"] = self._programme_policy()
        route["certification_contract"] = self._certification_contract()
        return route

    def exemption(self, **fields: Any) -> dict[str, Any]:
        exemption = super().exemption(**fields)
        exemption["programme_policy"] = self._programme_policy()
        exemption["certification_contract"] = self._certification_contract()
        return exemption


class MathematicalConstitution(_ReviewedMathematicalConstitution):
    """Constitution with distinct packet, intake, and adjudication gates."""

    def evaluate(self, state: WorkPackageState) -> GateReport:
        report = super().evaluate(state)
        if not state.mathematical:
            return report

        satisfied = [
            item
            for item in report.satisfied
            if item != "mathematical claims have disposition-compatible Cert handoffs"
        ]
        missing = [
            item
            for item in report.missing
            if not (
                item.startswith("MATHCERT handoff for ")
                and item.endswith(" lacks commit-and-artifact identity")
            )
        ]

        if state.phase in {Phase.SPECIFICATION, Phase.REALIZATION}:
            record = state.mathsolve_route or state.mathsolve_exemption
            if record is not None:
                contract_errors = _provider_contract_errors(record)
                if contract_errors:
                    missing.extend(contract_errors)
                else:
                    satisfied.append(
                        "Programme policy and MATHCERT route-registry identities are pinned"
                    )

        if state.phase in {Phase.JUDGMENT, Phase.INTEGRATION}:
            claim_ids = _claim_ids(state)
            cert_missing: list[str] = []
            for claim_id in sorted(claim_ids):
                handoff = state.mathcert_handoff_for(claim_id)
                if handoff is None:
                    continue
                status = str(handoff.get("status", ""))
                if status not in ALL_HANDOFF_STATES:
                    cert_missing.append(
                        f"MATHCERT handoff for {claim_id} has invalid status: {status or 'missing'}"
                    )
                    continue
                if status != "pending" and not _valid_packet_artifact(handoff):
                    cert_missing.append(
                        f"MATHCERT handoff packet for {claim_id} lacks MATHSOLVE artifact identity"
                    )
                if status in {"submitted"} | ADJUDICATED_HANDOFF_STATES and not str(
                    handoff.get("intake_acknowledgement", "")
                ).strip():
                    cert_missing.append(
                        f"MATHCERT intake acknowledgement missing for claim: {claim_id}"
                    )
                if status not in ADJUDICATED_HANDOFF_STATES:
                    cert_missing.append(
                        f"MATHCERT adjudicated disposition missing for claim: {claim_id}"
                    )
                elif not _valid_cert_output(handoff):
                    cert_missing.append(
                        f"MATHCERT disposition for {claim_id} lacks output artifact identity"
                    )
            missing.extend(cert_missing)
            if claim_ids and not cert_missing and not any(
                item.startswith("MATHCERT handoff missing for claim:") for item in missing
            ):
                satisfied.append(
                    "mathematical claims have content-addressed MATHCERT adjudications"
                )

            decision = str((state.judgment or {}).get("decision", ""))
            if decision in {Decision.ACCEPT.value, Decision.COMBINE.value}:
                for claim_id in sorted(claim_ids):
                    handoff = state.mathcert_handoff_for(claim_id)
                    status = str((handoff or {}).get("status", ""))
                    if status not in PROMOTING_HANDOFF_STATES:
                        marker = (
                            "accepted mathematical claims require certified or qualified "
                            "MATHCERT dispositions"
                        )
                        if not any(marker in item for item in missing):
                            missing.append(
                                marker + f": {claim_id}:{status or 'missing'}"
                            )

        return GateReport(
            phase=report.phase,
            target_phase=report.target_phase,
            ready=not missing,
            satisfied=tuple(dict.fromkeys(satisfied)),
            missing=tuple(dict.fromkeys(missing)),
        )


class MathematicalGrandIntellect(_ReviewedMathematicalGrandIntellect):
    """Runtime with content-addressed packet and Cert output semantics."""

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

    def record_mathcert_handoff(
        self,
        work_package_id: str,
        *,
        handoff_id: str,
        issue: str,
        target_claim_ids: Iterable[str],
        status: str,
        packet_repository: str | None = None,
        packet_commit_sha: str | None = None,
        packet_artifact_path: str | None = None,
        packet_digest_algorithm: str | None = None,
        packet_digest: str | None = None,
        intake_acknowledgement: str | None = None,
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
        if status not in ALL_HANDOFF_STATES:
            raise ValueError(f"invalid MATHCERT status: {status}")

        packet_fields = [
            packet_repository,
            packet_commit_sha,
            packet_artifact_path,
            packet_digest_algorithm,
            packet_digest,
        ]
        _all_or_none(packet_fields, "packet artifact identity")
        if status != "pending" and not all(value is not None for value in packet_fields):
            raise ValueError(f"MATHCERT status {status} requires packet artifact identity")
        if packet_repository is not None:
            if packet_repository != "grandchallenge/MATHSOLVE":
                raise ValueError("MATHCERT packet repository must be grandchallenge/MATHSOLVE")
            _commit(str(packet_commit_sha))
            _required(packet_artifact_path, "packet_artifact_path")
            _validate_digest(str(packet_digest_algorithm), str(packet_digest))

        if digest is not None and sha256 is not None:
            raise ValueError("supply digest or sha256, not both")
        if sha256 is not None:
            digest_algorithm = "sha256"
            digest = sha256
        output_fields = [commit_sha, artifact_path, digest_algorithm, digest]
        _all_or_none(output_fields, "Cert output artifact identity")
        if status in ADJUDICATED_HANDOFF_STATES:
            if not all(value is not None for value in output_fields):
                raise ValueError(
                    f"MATHCERT status {status} requires Cert output artifact identity"
                )
        elif any(value is not None for value in output_fields):
            raise ValueError("intake states may not carry a Cert adjudication output")
        if commit_sha is not None:
            _commit(commit_sha)
            _required(artifact_path, "artifact_path")
            _validate_digest(str(digest_algorithm), str(digest))

        acknowledgement = str(intake_acknowledgement or "").strip()
        if status in {"submitted"} | ADJUDICATED_HANDOFF_STATES:
            if not acknowledgement:
                raise ValueError(
                    f"MATHCERT status {status} requires an intake acknowledgement"
                )
        elif acknowledgement:
            raise ValueError("pending and ready states may not claim intake acknowledgement")

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
                "packet_repository": packet_repository,
                "packet_commit_sha": packet_commit_sha,
                "packet_artifact_path": packet_artifact_path,
                "packet_digest_algorithm": packet_digest_algorithm,
                "packet_digest": packet_digest,
                "intake_acknowledgement": acknowledgement or None,
                "commit_sha": commit_sha,
                "artifact_path": artifact_path,
                "digest_algorithm": digest_algorithm,
                "digest": digest,
                "authority": "github",
                "future_projection": "aether",
            },
        )


def _all_or_none(values: list[Any], label: str) -> None:
    if any(value is not None for value in values) and not all(
        value is not None for value in values
    ):
        raise ValueError(f"{label} fields must be supplied together")


def _claim_ids(state: WorkPackageState) -> set[str]:
    declared = {
        str(claim).strip()
        for claim in (state.specification or {}).get("claims", [])
        if str(claim).strip()
    }
    registered = {
        str(claim.get("claim_id", "")).strip()
        for claim in state.mathematical_claims
        if str(claim.get("claim_id", "")).strip()
    }
    return declared | registered


def _provider_contract_errors(record: Mapping[str, Any]) -> list[str]:
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


def _valid_packet_artifact(handoff: Mapping[str, Any]) -> bool:
    return _valid_artifact_ref(
        {
            "repository": handoff.get("packet_repository"),
            "commit_sha": handoff.get("packet_commit_sha"),
            "artifact_path": handoff.get("packet_artifact_path"),
            "digest_algorithm": handoff.get("packet_digest_algorithm"),
            "digest": handoff.get("packet_digest"),
        }
    ) and handoff.get("packet_repository") == "grandchallenge/MATHSOLVE"


def _valid_cert_output(handoff: Mapping[str, Any]) -> bool:
    return _valid_artifact_ref(
        {
            "repository": handoff.get("repository"),
            "commit_sha": handoff.get("commit_sha"),
            "artifact_path": handoff.get("artifact_path"),
            "digest_algorithm": handoff.get("digest_algorithm"),
            "digest": handoff.get("digest"),
        }
    ) and handoff.get("repository") == "grandchallenge/MATHCERT"
