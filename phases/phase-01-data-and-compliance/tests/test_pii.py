from review_ingest.pii import redact_pii


def test_redacts_email_and_handle():
    raw = "Reach me at user.name+tag@example.com or @myhandle for details"
    out, n = redact_pii(raw)
    assert "example.com" not in out
    assert "[redacted-email]" in out
    assert "[redacted-handle]" in out
    assert n >= 2
