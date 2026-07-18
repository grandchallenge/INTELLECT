from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Protocol

from .model import IntellectEvent


@dataclass(frozen=True, slots=True)
class AppendReceipt:
    cut: int
    event_ids: tuple[str, ...]
    replayed: bool = False


class CoordinationFabric(Protocol):
    """Minimal semantic-fabric boundary consumed by the constitutional runtime."""

    authoritative: bool

    def append(self, events: list[IntellectEvent]) -> AppendReceipt: ...

    def history(self, work_package_id: str) -> list[IntellectEvent]: ...


class InMemoryFabric:
    """Deterministic test double. Never an authoritative production substrate."""

    authoritative = False

    def __init__(self) -> None:
        self._events: list[IntellectEvent] = []
        self._idempotency: dict[str, AppendReceipt] = {}
        self._lock = RLock()

    def append(self, events: list[IntellectEvent]) -> AppendReceipt:
        if not events:
            raise ValueError("at least one event is required")
        keys = {event.idempotency_key for event in events if event.idempotency_key}
        if len(keys) > 1:
            raise ValueError("one append batch may use at most one idempotency key")
        key = next(iter(keys), None)
        with self._lock:
            if key is not None and key in self._idempotency:
                previous = self._idempotency[key]
                return AppendReceipt(previous.cut, previous.event_ids, replayed=True)
            existing = {event.event_id for event in self._events}
            duplicates = [event.event_id for event in events if event.event_id in existing]
            if duplicates:
                raise ValueError(f"duplicate event ids: {duplicates}")
            self._events.extend(events)
            receipt = AppendReceipt(
                cut=len(self._events),
                event_ids=tuple(event.event_id for event in events),
            )
            if key is not None:
                self._idempotency[key] = receipt
            return receipt

    def history(self, work_package_id: str) -> list[IntellectEvent]:
        with self._lock:
            return [
                event
                for event in self._events
                if event.work_package_id == work_package_id
            ]
