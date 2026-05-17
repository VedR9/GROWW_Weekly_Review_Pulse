from __future__ import annotations

from datetime import date, timedelta


def date_window_end(as_of: date, *, weeks: int) -> date:
    """Rolling window: inclusive `as_of`, backwards `weeks` full weeks (7 * weeks days)."""
    return as_of - timedelta(days=7 * weeks)


def in_window(d: date, *, as_of: date, weeks: int) -> bool:
    start = date_window_end(as_of, weeks=weeks)
    return start <= d <= as_of
