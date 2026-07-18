from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable
from urllib import error, request

from .fabric import AppendReceipt
from .model import IntellectEvent


class AetherTransportError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class AetherAttributeMap:
    event_type: int = 1
    work_package_id: int = 2
    actor: int = 3
    payload_json: int = 4
    occurred_at: int = 5
    event_id: int = 6
    correlation_id: int = 7
    causation_id: int = 8


class AetherHttpFabric:
    """Authoritative INTELLECT event fabric over AETHER's stable HTTP boundary.

    Each INTELLECT event is represented as one AETHER entity with scalar
    attributes. AETHER remains authoritative for append order, cuts, replay,
    policy visibility, and provenance. The mapping is deliberately explicit and
    versioned; it is not a shadow rule engine.
    """

    authoritative = True
    REQUIRED_CAPABILITIES = frozenset({"resource_limits_v1", "pagination_v1"})

    def __init__(
        self,
        base_url: str,
        *,
        bearer_token: str,
        namespace: str,
        schema_ref: dict[str, Any],
        attributes: AetherAttributeMap | None = None,
        timeout_seconds: float = 10.0,
        replica: int = 1,
        transport: Callable[
            [str, str, dict[str, Any] | None, dict[str, str]], dict[str, Any]
        ]
        | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.bearer_token = bearer_token
        self.namespace = namespace
        self.schema_ref = dict(schema_ref)
        self.attributes = attributes or AetherAttributeMap()
        self.timeout_seconds = timeout_seconds
        self.replica = replica
        self._transport = transport or self._http_transport
        self._preflight_done = False

    def preflight(self) -> None:
        status = self._request("GET", "/v1/status")
        capabilities = {str(x) for x in status.get("capabilities", [])}
        missing = sorted(self.REQUIRED_CAPABILITIES - capabilities)
        if missing:
            raise AetherTransportError(
                "AETHER server lacks required capabilities: " + ", ".join(missing)
            )
        self._preflight_done = True

    def append(self, events: list[IntellectEvent]) -> AppendReceipt:
        if not events:
            raise ValueError("at least one event is required")
        if not self._preflight_done:
            self.preflight()
        idempotency_keys = {
            event.idempotency_key for event in events if event.idempotency_key
        }
        if len(idempotency_keys) > 1:
            raise ValueError("one append batch may use at most one idempotency key")
        idempotency_key = next(iter(idempotency_keys), None)
        datoms: list[dict[str, Any]] = []
        for event in events:
            datoms.extend(self._event_datoms(event))
        response = self._request(
            "POST",
            "/v1/append",
            {
                "schema_ref": self.schema_ref,
                "expected_cut": None,
                "idempotency_key": idempotency_key,
                "datoms": datoms,
            },
        )
        cut = _extract_cut(response)
        event_ids = tuple(event.event_id for event in events)
        return AppendReceipt(
            cut=cut,
            event_ids=event_ids,
            replayed=bool(response.get("replayed", False)),
        )

    def history(self, work_package_id: str) -> list[IntellectEvent]:
        if not self._preflight_done:
            self.preflight()
        events: dict[int, dict[int, Any]] = {}
        entity_order: list[int] = []
        offset = 0
        limit = 500
        while True:
            page = self._request(
                "GET", f"/v1/history/page?offset={offset}&limit={limit}"
            )
            rows = page.get("items", page.get("datoms", page.get("history", [])))
            if not isinstance(rows, list):
                raise AetherTransportError("unexpected AETHER history response")
            for row in rows:
                if not isinstance(row, dict):
                    continue
                entity = int(row["entity"])
                attribute = int(row["attribute"])
                operation = row.get("op")
                if operation not in (None, "Assert"):
                    raise AetherTransportError(
                        "reserved INTELLECT event attribute used non-Assert "
                        f"operation: {operation}"
                    )
                if entity not in events:
                    events[entity] = {}
                    entity_order.append(entity)
                events[entity][attribute] = _decode_value(row.get("value"))
            page_info = page.get("page")
            if isinstance(page_info, dict):
                next_offset = page_info.get("next_offset")
                if next_offset is None:
                    break
                offset = int(next_offset)
                continue
            if not page.get("has_more", False):
                break
            offset += len(rows)

        result: list[IntellectEvent] = []
        attrs = self.attributes
        for entity in entity_order:
            values = events[entity]
            if str(values.get(attrs.work_package_id, "")) != work_package_id:
                continue
            required = {
                attrs.event_type,
                attrs.work_package_id,
                attrs.actor,
                attrs.payload_json,
                attrs.occurred_at,
                attrs.event_id,
            }
            if not required.issubset(values):
                continue
            payload_value = values[attrs.payload_json]
            payload = (
                json.loads(payload_value)
                if isinstance(payload_value, str)
                else payload_value
            )
            result.append(
                IntellectEvent(
                    event_id=str(values[attrs.event_id]),
                    event_type=str(values[attrs.event_type]),
                    work_package_id=str(values[attrs.work_package_id]),
                    actor=str(values[attrs.actor]),
                    payload=dict(payload),
                    occurred_at=str(values[attrs.occurred_at]),
                    correlation_id=_optional(values.get(attrs.correlation_id)),
                    causation_id=_optional(values.get(attrs.causation_id)),
                )
            )
        return result

    def _event_datoms(self, event: IntellectEvent) -> list[dict[str, Any]]:
        attrs = self.attributes
        entity = _stable_u64(event.event_id)
        values = (
            (attrs.event_type, event.event_type),
            (attrs.work_package_id, event.work_package_id),
            (attrs.actor, event.actor),
            (
                attrs.payload_json,
                json.dumps(event.payload, sort_keys=True, separators=(",", ":")),
            ),
            (attrs.occurred_at, event.occurred_at),
            (attrs.event_id, event.event_id),
            (attrs.correlation_id, event.correlation_id or ""),
            (attrs.causation_id, event.causation_id or ""),
        )
        provenance = {
            "author_principal": event.actor,
            "agent_id": event.actor,
            "tool_id": "grand-intellect",
            "session_id": event.correlation_id or event.work_package_id,
            "source_ref": {
                "uri": f"intellect:event:{event.event_id}",
                "digest": None,
            },
            "parent_datom_ids": [],
            "confidence": 1.0,
            "trust_domain": "grandchallenge/intellect",
            "schema_version": "intellect-v0",
        }
        return [
            {
                "entity": entity,
                "attribute": attribute,
                "value": {"String": value},
                "op": "Assert",
                "element": _stable_u64(f"{event.event_id}:{attribute}"),
                "replica": self.replica,
                "causal_context": {"frontier": []},
                "provenance": provenance,
                "policy": {
                    "capability": "intellect.read",
                    "visibility": "intellect",
                },
            }
            for attribute, value in values
        ]

    def _request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "X-Aether-Namespace": self.namespace,
            "Content-Type": "application/json",
        }
        return self._transport(method, self.base_url + path, payload, headers)

    def _http_transport(
        self,
        method: str,
        url: str,
        payload: dict[str, Any] | None,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=body, method=method, headers=headers)
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                decoded = json.loads(response.read().decode("utf-8"))
                if not isinstance(decoded, dict):
                    raise AetherTransportError(
                        "AETHER response must be a JSON object"
                    )
                return decoded
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise AetherTransportError(
                f"AETHER request failed with HTTP {exc.code}: {detail}"
            ) from exc
        except error.URLError as exc:
            raise AetherTransportError(
                f"AETHER request failed: {exc.reason}"
            ) from exc


def _stable_u64(value: str) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return (int.from_bytes(digest[:8], "big") % ((1 << 63) - 1)) + 1


def _extract_cut(response: dict[str, Any]) -> int:
    candidates = [
        response.get("cut"),
        response.get("committed_cut"),
        (response.get("receipt") or {}).get("cut")
        if isinstance(response.get("receipt"), dict)
        else None,
    ]
    for candidate in candidates:
        if isinstance(candidate, int):
            return candidate
        if isinstance(candidate, dict):
            for key in ("index", "offset", "value"):
                if isinstance(candidate.get(key), int):
                    return int(candidate[key])
    raise AetherTransportError("append response did not contain a recognized cut")


def _optional(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value)


def _decode_value(value: Any) -> Any:
    if isinstance(value, dict) and len(value) == 1:
        tag, payload = next(iter(value.items()))
        if tag in {"String", "U64", "I64", "Bool", "F64", "Float", "Entity"}:
            return payload
    return value
