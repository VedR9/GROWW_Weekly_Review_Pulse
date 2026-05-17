from datetime import date, timedelta

from review_ingest.window import date_window_end, in_window


def test_in_window_inclusive():
    as_of = date(2026, 5, 10)
    weeks = 10
    start = date_window_end(as_of, weeks=weeks)
    assert start == as_of - timedelta(days=70)
    assert in_window(start, as_of=as_of, weeks=weeks)
    assert in_window(as_of, as_of=as_of, weeks=weeks)
    assert not in_window(start - timedelta(days=1), as_of=as_of, weeks=weeks)
    assert not in_window(as_of + timedelta(days=1), as_of=as_of, weeks=weeks)
