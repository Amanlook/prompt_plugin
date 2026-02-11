"""Prompt history manager — save, search, and reuse past prompts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from prompt_plugin.models import HistoryEntry, TaskCategory, Tone

_DEFAULT_HISTORY_FILE = Path.home() / ".prompt_plugin" / "history.json"


class HistoryManager:
    """Persistent prompt history backed by a local JSON file."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or _DEFAULT_HISTORY_FILE
        self._entries: list[HistoryEntry] = []
        self._load()

    # ── Persistence ────────────────────────────────────────────────────────

    def _load(self) -> None:
        if self._path.exists():
            try:
                raw = json.loads(self._path.read_text())
                self._entries = [HistoryEntry(**e) for e in raw]
            except (json.JSONDecodeError, ValueError):
                self._entries = []

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [e.model_dump(mode="json") for e in self._entries]
        self._path.write_text(json.dumps(data, indent=2, default=str))

    # ── Public API ─────────────────────────────────────────────────────────

    def add(
        self,
        original: str,
        enhanced: str,
        category: TaskCategory,
        tone: Tone,
    ) -> HistoryEntry:
        """Add a new entry and persist."""
        next_id = max((e.id for e in self._entries), default=0) + 1
        entry = HistoryEntry(
            id=next_id,
            original=original,
            enhanced=enhanced,
            category=category,
            tone=tone,
            timestamp=datetime.now(tz=__import__('datetime').timezone.utc),
        )
        self._entries.append(entry)
        self._save()
        return entry

    def list(
        self,
        category: TaskCategory | None = None,
        limit: int = 20,
        starred_only: bool = False,
    ) -> list[HistoryEntry]:
        """Return recent history, optionally filtered."""
        items = list(reversed(self._entries))
        if category:
            items = [e for e in items if e.category == category]
        if starred_only:
            items = [e for e in items if e.starred]
        return items[:limit]

    def search(self, query: str, limit: int = 10) -> list[HistoryEntry]:
        """Simple substring search across original and enhanced prompts."""
        q = query.lower()
        results = [
            e for e in reversed(self._entries)
            if q in e.original.lower() or q in e.enhanced.lower()
        ]
        return results[:limit]

    def star(self, entry_id: int) -> HistoryEntry | None:
        """Toggle the starred status of a history entry."""
        for e in self._entries:
            if e.id == entry_id:
                e.starred = not e.starred
                self._save()
                return e
        return None

    def delete(self, entry_id: int) -> bool:
        """Delete a history entry by ID."""
        before = len(self._entries)
        self._entries = [e for e in self._entries if e.id != entry_id]
        if len(self._entries) < before:
            self._save()
            return True
        return False

    def clear(self) -> int:
        """Clear all history. Returns count of deleted entries."""
        count = len(self._entries)
        self._entries = []
        self._save()
        return count

    @property
    def count(self) -> int:
        return len(self._entries)
