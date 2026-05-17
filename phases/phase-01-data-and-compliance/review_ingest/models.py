from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Literal

SourceStore = Literal["app_store", "play_store", "unknown"]


@dataclass(frozen=True)
class NormalizedReview:
    """Canonical record for Phase 2+. No reviewer names or handles."""

    rating: float
    title: str
    body: str
    review_date: date
    source_store: SourceStore


@dataclass
class IngestSummary:
    """Row-level stats for operators and tests."""

    rows_read: int = 0
    rows_after_window: int = 0
    rows_output: int = 0
    duplicates_dropped: int = 0
    empty_body_skipped: int = 0
    invalid_row_skipped: int = 0
    pii_redactions: int = 0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "rows_read": self.rows_read,
            "rows_after_window": self.rows_after_window,
            "rows_output": self.rows_output,
            "duplicates_dropped": self.duplicates_dropped,
            "empty_body_skipped": self.empty_body_skipped,
            "invalid_row_skipped": self.invalid_row_skipped,
            "pii_redactions": self.pii_redactions,
            "warnings": list(self.warnings),
        }
