from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

# Column header tokens (normalized: lower, non-alnum -> space) we accept for each role.
_RATING_ALIASES = frozenset(
    {"rating", "star rating", "review rating", "stars", "score", "star"}
)
_TITLE_ALIASES = frozenset({"title", "review title", "summary"})
_BODY_ALIASES = frozenset(
    {"review", "review text", "text", "body", "comment", "comments", "content"}
)
_DATE_ALIASES = frozenset(
    {
        "date",
        "review date",
        "submitted",
        "last update",
        "review last update date",
        "created",
        "created date",
        "review submit date",
    }
)
# Column headers we never use as rating/title/body/date (avoid "review" ⊆ "reviewer").
_IGNORE_HEADERS = frozenset(
    {
        "reviewer",
        "reviewer nickname",
        "user",
        "nickname",
        "author",
        "developer reply",
        "developer response",
    }
)


def normalize_header(h: str) -> str:
    s = h.strip().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def _pick_field(row: dict[str, str], aliases: frozenset[str]) -> str | None:
    for key, val in row.items():
        if val is None or not str(val).strip():
            continue
        nh = normalize_header(key)
        if nh in _IGNORE_HEADERS:
            continue
        if nh in aliases:
            return str(val).strip()
        for a in aliases:
            if len(a) >= 4 and a in nh:
                # Avoid mapping "Review Title" to body: nh is "review title", a is "review".
                if a == "review" and nh != "review":
                    continue
                return str(val).strip()
    return None


def parse_rating(raw: str | None) -> float | None:
    if raw is None or not str(raw).strip():
        return None
    s = str(raw).strip().replace(",", ".")
    try:
        return float(s)
    except ValueError:
        m = re.search(r"(\d+(?:\.\d+)?)", s)
        if m:
            return float(m.group(1))
        return None


_DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%d-%b-%Y",
    "%b %d, %Y",
    "%B %d, %Y",
)


def parse_review_date(raw: str | None) -> date | None:
    if raw is None or not str(raw).strip():
        return None
    s = str(raw).strip()
    if len(s) >= 10 and s[4] == "-" and s[7] == "-":
        try:
            return date.fromisoformat(s[:10])
        except ValueError:
            pass
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            dt = dt.astimezone(tz=None).replace(tzinfo=None)
        return dt.date()
    except ValueError:
        pass
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s[:40], fmt).date()
        except ValueError:
            continue
    return None


def build_row_dict(fieldnames: list[str], row: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for i, name in enumerate(fieldnames):
        out[name] = row[i] if i < len(row) else ""
    return out


def extract_fields(raw_row: dict[str, str]) -> dict[str, Any]:
    """Map a CSV row to rating, title, body, review_date; drop reviewer-only fields."""
    rating_raw = _pick_field(raw_row, _RATING_ALIASES)
    title = _pick_field(raw_row, _TITLE_ALIASES) or ""
    body = _pick_field(raw_row, _BODY_ALIASES) or ""
    date_raw = _pick_field(raw_row, _DATE_ALIASES)
    return {
        "rating": parse_rating(rating_raw),
        "title": title,
        "body": body,
        "review_date": parse_review_date(date_raw),
    }
