import json
from datetime import date
from pathlib import Path

from review_ingest.pipeline import ingest_files

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def test_ingest_app_store_fixture_window_and_schema():
    as_of = date(2026, 5, 10)
    path = FIXTURES / "sample_app_store.csv"
    reviews, summary = ingest_files([path], as_of=as_of, weeks=10, source_store="app_store")
    # Jan row excluded; Apr rows inside window
    assert summary.rows_read == 3
    assert summary.invalid_row_skipped == 0
    assert len(reviews) == 2
    bodies = sorted(r.body for r in reviews)
    assert any("redacted" in b.lower() for b in bodies)
    for r in reviews:
        assert r.source_store == "app_store"
        d = {
            "schema_version": 1,
            "rating": r.rating,
            "title": r.title,
            "body": r.body,
            "review_date": r.review_date.isoformat(),
            "source_store": r.source_store,
        }
        json.dumps(d)
    assert "Reviewer" not in json.dumps([{"title": r.title, "body": r.body} for r in reviews])


def test_dedup_play_store():
    as_of = date(2026, 5, 10)
    path = FIXTURES / "sample_play_store.csv"
    reviews, summary = ingest_files([path], as_of=as_of, weeks=10, source_store="play_store")
    assert summary.duplicates_dropped >= 1
    assert len(reviews) == 1
