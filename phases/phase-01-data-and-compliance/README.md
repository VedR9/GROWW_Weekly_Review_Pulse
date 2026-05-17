# Phase 1 — Data and compliance (implementation)

Runnable **public CSV export → normalized JSONL** pipeline. No store scraping and **no reviewer identifiers** in output.

## Operator quick start

1. Export reviews from **App Store Connect** / **Play Console** using **official** export or download flows (see [SOURCE_INVENTORY.md](./SOURCE_INVENTORY.md)).
2. Save one or more CSV files (UTF-8).
3. From the **repository root**, with the dev environment installed:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

4. Run ingest (example):

```bash
review-ingest \
  -i path/to/app_store_reviews.csv \
  -i path/to/play_reviews.csv \
  -o out/normalized.jsonl \
  --store auto \
  --weeks 10 \
  --as-of 2026-05-10
```

- **`--weeks`:** integer **8–12** (default **10**). Rolling window: `as_of − 7×weeks` through `as_of` (inclusive), **UTC calendar date** for `--as-of` (default: UTC “today” when omitted).
- **`--store`:** `app_store` | `play_store` | `auto` (infer `app_store` / `play_store` from filename hints; else `unknown`).
- **stderr** prints an `IngestSummary` JSON (counts, warnings).

Artifacts:

- **`--output`:** JSON Lines; one object per review, schema in [DATA_CONTRACT.md](./DATA_CONTRACT.md).
- **`--summary-json`:** optional path to write the same summary as JSON for CI.

## Fixtures and tests

```bash
PYTHONPATH=phases/phase-01-data-and-compliance .venv/bin/python -m pytest phases/phase-01-data-and-compliance/tests -v
```

Sanitized samples live under [`fixtures/`](./fixtures/).

## Related docs

- [DATA_CONTRACT.md](./DATA_CONTRACT.md) — normalized record schema for Phase 2.
- [SOURCE_INVENTORY.md](./SOURCE_INVENTORY.md) — allowed data sources policy.
- [Eval criteria](../../docs/phases/phase-01-data-and-compliance/eval.md)
