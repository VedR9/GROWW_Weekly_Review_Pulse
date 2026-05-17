from __future__ import annotations

import csv
import hashlib
import io
import json
from collections.abc import Iterable
from datetime import date
from pathlib import Path
from typing import TextIO

from review_ingest.mapping import build_row_dict, extract_fields
from review_ingest.models import IngestSummary, NormalizedReview, SourceStore
from review_ingest.pii import redact_pii
from review_ingest.window import in_window

_ENCODING_TRIES = ("utf-8-sig", "utf-8", "cp1252")


def _read_csv_rows(path: Path) -> tuple[list[str], list[list[str]]]:
    raw = path.read_bytes()
    last_err: Exception | None = None
    for enc in _ENCODING_TRIES:
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError as e:
            last_err = e
            text = None
    else:
        raise RuntimeError(f"Could not decode file as {', '.join(_ENCODING_TRIES)}") from last_err

    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def _fingerprint(rec: NormalizedReview) -> str:
    payload = f"{rec.review_date.isoformat()}\n{rec.body.strip()[:4000]}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ingest_files(
    paths: Iterable[Path | str],
    *,
    as_of: date,
    weeks: int,
    source_store: SourceStore = "unknown",
) -> tuple[list[NormalizedReview], IngestSummary]:
    """
    Load CSV review exports, normalize, filter to [as_of - 7*weeks, as_of], dedupe.
    Reviewer columns are never emitted. Title/body pass PII redaction.
    """
    summary = IngestSummary()
    out: list[NormalizedReview] = []
    seen: set[str] = set()

    for p in paths:
        path = Path(p)
        if not path.is_file():
            summary.warnings.append(f"Missing file skipped: {path}")
            continue
        headers, data_rows = _read_csv_rows(path)
        if not headers:
            summary.warnings.append(f"Empty CSV: {path}")
            continue
        store = source_store if source_store != "unknown" else _detect_store_from_path(path)
        for row_cells in data_rows:
            summary.rows_read += 1
            raw = build_row_dict(headers, row_cells)
            fields = extract_fields(raw)
            rating = fields["rating"]
            title_raw = fields["title"] or ""
            body_raw = fields["body"] or ""
            rd = fields["review_date"]
            if rating is None or rd is None:
                summary.invalid_row_skipped += 1
                continue
            if not body_raw.strip():
                summary.empty_body_skipped += 1
                continue
            if not in_window(rd, as_of=as_of, weeks=weeks):
                continue
            if len(body_raw.split()) < 6:
                continue
            import emoji
            if emoji.emoji_count(body_raw) > 0:
                continue
            try:
                import langdetect
                if langdetect.detect(body_raw) != 'en':
                    continue
            except:
                # If langdetect fails (e.g. not enough text to detect), skip it or assume it's not valid English
                continue
            summary.rows_after_window += 1
            title, ct = redact_pii(title_raw)
            summary.pii_redactions += ct
            body, cb = redact_pii(body_raw)
            summary.pii_redactions += cb
            rec = NormalizedReview(
                rating=float(rating),
                title=title,
                body=body,
                review_date=rd,
                source_store=store,
            )
            fp = _fingerprint(rec)
            if fp in seen:
                summary.duplicates_dropped += 1
                continue
            seen.add(fp)
            out.append(rec)

    summary.rows_output = len(out)
    out.sort(key=lambda r: r.review_date, reverse=True)
    return out, summary


def _detect_store_from_path(path: Path) -> SourceStore:
    name = path.name.lower()
    if "app_store" in name or "app-store" in name or "ios" in name:
        return "app_store"
    if "play" in name or "android" in name:
        return "play_store"
    return "unknown"


def normalized_to_jsonl(reviews: list[NormalizedReview], sink: TextIO) -> None:
    for r in reviews:
        d = {
            "schema_version": 1,
            "rating": r.rating,
            "title": r.title,
            "body": r.body,
            "review_date": r.review_date.isoformat(),
            "source_store": r.source_store,
        }
        sink.write(json.dumps(d, ensure_ascii=False))
        sink.write("\n")


def write_jsonl(path: Path, reviews: list[NormalizedReview]) -> None:
    with path.open("w", encoding="utf-8") as f:
        normalized_to_jsonl(reviews, f)
