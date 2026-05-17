from __future__ import annotations

import re

_EMAIL = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    re.UNICODE,
)
# Public social-style @handles (single token); conservative to reduce false positives.
_HANDLE = re.compile(r"(?<!\w)@([a-zA-Z0-9_]{2,30})\b")

_REPLACEMENT_EMAIL = "[redacted-email]"
_REPLACEMENT_HANDLE = "[redacted-handle]"


def redact_pii(text: str) -> tuple[str, int]:
    """
    Remove obvious emails and @handles from review title/body.
    Returns (redacted_text, number of substitutions).
    """
    if not text:
        return text, 0
    count = 0
    s, n = _EMAIL.subn(_REPLACEMENT_EMAIL, text)
    count += n
    s, n = _HANDLE.subn(_REPLACEMENT_HANDLE, s)
    count += n
    return s, count
