from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from review_ingest.models import SourceStore
from review_ingest.pipeline import ingest_files, write_jsonl


def _parse_as_of(raw: str | None) -> date:
    if raw is None:
        return datetime.now(timezone.utc).date()
    return date.fromisoformat(raw.strip())


def _parse_store(arg: str) -> SourceStore:
    a = arg.lower().strip()
    if a in ("auto", "unknown"):
        return "unknown"
    if a in ("app_store", "app-store", "ios", "apple"):
        return "app_store"
    if a in ("play_store", "play-store", "android", "google"):
        return "play_store"
    raise SystemExit(f"Invalid --store: {arg!r}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Normalize public App Store / Play Store review CSV exports (Phase 1)."
    )
    p.add_argument(
        "--input",
        "-i",
        action="append",
        required=True,
        help="Path to a CSV export. Repeat for multiple files.",
    )
    p.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output JSONL path (one NormalizedReview per line).",
    )
    p.add_argument(
        "--weeks",
        type=int,
        default=10,
        help="Rolling window length in weeks. Default 10.",
    )
    p.add_argument(
        "--as-of",
        type=str,
        default=None,
        help="Inclusive end date YYYY-MM-DD (UTC calendar date). Default: UTC today.",
    )
    p.add_argument(
        "--store",
        type=str,
        default="auto",
        help="Source label: app_store | play_store | auto (infer from filename).",
    )
    p.add_argument(
        "--summary-json",
        type=str,
        default=None,
        help="Optional path to write IngestSummary as JSON (for CI).",
    )
    args = p.parse_args(argv)

    as_of = _parse_as_of(args.as_of)
    store = _parse_store(args.store)
    paths = [Path(x) for x in (args.input or [])]
    reviews, summary = ingest_files(paths, as_of=as_of, weeks=args.weeks, source_store=store)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_path, reviews)

    if args.summary_json:
        sp = Path(args.summary_json)
        sp.parent.mkdir(parents=True, exist_ok=True)
        sp.write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")

    print(json.dumps(summary.to_dict(), indent=2), file=sys.stderr)
    print(
        f"Wrote {len(reviews)} reviews to {out_path}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
