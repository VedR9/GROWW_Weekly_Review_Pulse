# Normalized review contract (Phase 1 → Phase 2)

## Transport

- **JSON Lines** (`.jsonl`): one UTF-8 JSON object per line.
- **`schema_version`:** `1` (bump when fields change).

## Record shape

Each line is a **`NormalizedReview`** with:

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `schema_version` | `integer` | yes | Currently `1`. |
| `rating` | `number` | yes | Typically 1–5; store-specific scales normalized to a float. |
| `title` | `string` | yes | May be empty string. **PII redaction** may have run (see below). |
| `body` | `string` | yes | Non-empty after ingest filters. **PII redaction** applied. |
| `review_date` | `string` | yes | ISO **date** `YYYY-MM-DD` (calendar date of the review). |
| `source_store` | `string` | yes | One of: `app_store`, `play_store`, `unknown`. |

### Explicitly omitted

The following **never** appear in this contract (Phase 2 must not receive them from Phase 1):

- Reviewer name, nickname, user id, email  
- Device id, country, or other fields unless you add a **new schema version** and update Phase 2.

### PII handling in Phase 1

- Title and body pass **redaction** for obvious **emails** and **`@handles`** in text (see `review_ingest/pii.py`).
- Reviewer columns in CSV are **ignored** for mapping into `title` / `body` / `rating` / `date`.

## Example line

```json
{"schema_version": 1, "rating": 4.0, "title": "Good overall", "body": "Notifications are flaky but app is solid.", "review_date": "2026-05-01", "source_store": "play_store"}
```
