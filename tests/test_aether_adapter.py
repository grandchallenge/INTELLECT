from __future__ import annotations

import unittest

from grand_intellect.aether import AetherHttpFabric, AetherTransportError
from grand_intellect.model import IntellectEvent


class FakeTransport:
    def __init__(self, capabilities: list[str] | None = None) -> None:
        self.capabilities = capabilities or [
            "resource_limits_v1",
            "pagination_v1",
        ]
        self.calls: list[tuple[str, str, dict | None, dict[str, str]]] = []

    def __call__(
        self,
        method: str,
        url: str,
        payload: dict | None,
        headers: dict[str, str],
    ) -> dict:
        self.calls.append((method, url, payload, headers))
        if url.endswith("/v1/status"):
            return {"capabilities": self.capabilities}
        if url.endswith("/v1/append"):
            return {"committed_cut": 8, "replayed": False}
        if "/v1/history/page" in url:
            return {
                "page": {
                    "offset": 0,
                    "limit": 500,
                    "total": 0,
                    "next_offset": None,
                },
                "datoms": [],
            }
        raise AssertionError(f"unexpected URL: {url}")


class PagedHistoryTransport(FakeTransport):
    def __init__(self) -> None:
        super().__init__()
        first = IntellectEvent(
            event_id="event-first",
            event_type="work_package.chartered",
            work_package_id="WP-HISTORY",
            actor="human_steward",
            payload={
                "title": "First",
                "purpose": "p",
                "scope": "s",
                "acceptance_criteria": ["a"],
            },
            occurred_at="2099-01-01T00:00:00+00:00",
        )
        second = IntellectEvent(
            event_id="event-second",
            event_type="alternative.registered",
            work_package_id="WP-HISTORY",
            actor="possibility_minder",
            payload={
                "alternative_id": "A",
                "summary": "Second",
                "mechanism": "m",
                "assumptions": ["x"],
                "discriminating_test": "t",
            },
            occurred_at="2000-01-01T00:00:00+00:00",
        )
        temporary = AetherHttpFabric(
            "http://aether.test",
            bearer_token="secret",
            namespace="test",
            schema_ref={"name": "intellect", "version": 0},
            transport=self,
        )
        self.pages = [temporary._event_datoms(first), temporary._event_datoms(second)]

    def __call__(
        self,
        method: str,
        url: str,
        payload: dict | None,
        headers: dict[str, str],
    ) -> dict:
        self.calls.append((method, url, payload, headers))
        if url.endswith("/v1/status"):
            return {"capabilities": self.capabilities}
        if "offset=0" in url:
            return {
                "page": {
                    "offset": 0,
                    "limit": 500,
                    "total": 16,
                    "next_offset": 8,
                },
                "datoms": self.pages[0],
            }
        if "offset=8" in url:
            return {
                "page": {
                    "offset": 8,
                    "limit": 500,
                    "total": 16,
                    "next_offset": None,
                },
                "datoms": self.pages[1],
            }
        raise AssertionError(f"unexpected URL: {url}")


class AetherAdapterTests(unittest.TestCase):
    def test_preflight_and_append_shape(self) -> None:
        transport = FakeTransport()
        fabric = AetherHttpFabric(
            "http://aether.test",
            bearer_token="secret",
            namespace="intellect-test",
            schema_ref={"name": "intellect", "version": 0},
            transport=transport,
        )
        event = IntellectEvent(
            event_type="work_package.chartered",
            work_package_id="WP-1",
            actor="human_steward",
            payload={"title": "Test"},
            idempotency_key="charter:WP-1",
        )
        receipt = fabric.append([event])
        self.assertEqual(receipt.cut, 8)
        self.assertEqual(len(transport.calls), 2)
        _, _, payload, headers = transport.calls[1]
        assert payload is not None
        self.assertEqual(headers["X-Aether-Namespace"], "intellect-test")
        self.assertEqual(payload["idempotency_key"], "charter:WP-1")
        self.assertEqual(len(payload["datoms"]), 8)
        self.assertTrue(all(datom["op"] == "Assert" for datom in payload["datoms"]))
        self.assertTrue(
            all("String" in datom["value"] for datom in payload["datoms"])
        )
        self.assertTrue(
            all(
                datom["provenance"]["schema_version"] == "intellect-v0"
                for datom in payload["datoms"]
            )
        )

    def test_missing_capability_fails_closed(self) -> None:
        transport = FakeTransport(capabilities=["pagination_v1"])
        fabric = AetherHttpFabric(
            "http://aether.test",
            bearer_token="secret",
            namespace="intellect-test",
            schema_ref={"name": "intellect", "version": 0},
            transport=transport,
        )
        with self.assertRaises(AetherTransportError):
            fabric.preflight()

    def test_history_uses_page_info_and_preserves_journal_order(self) -> None:
        transport = PagedHistoryTransport()
        fabric = AetherHttpFabric(
            "http://aether.test",
            bearer_token="secret",
            namespace="intellect-test",
            schema_ref={"name": "intellect", "version": 0},
            transport=transport,
        )
        events = fabric.history("WP-HISTORY")
        self.assertEqual(
            [event.event_id for event in events], ["event-first", "event-second"]
        )
        self.assertEqual(events[0].payload["title"], "First")


if __name__ == "__main__":
    unittest.main()
