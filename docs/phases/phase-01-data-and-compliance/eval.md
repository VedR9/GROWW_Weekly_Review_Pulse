# Phase 1 — Evaluation: Data and compliance

**Phase:** [phase-01-data-and-compliance](./) · **Plan:** [phase-by-implementationplan](../../phase-by-implementationplan.md)

---

## Scope under test

- Public review sources only (no authenticated scraping).
- Time window **8–12 weeks** of reviews.
- Fields present: rating, title, text, date (or documented equivalent mapping).
- PII and identifier minimization before any pulse generation.

---

## Testing

| # | Test | How |
|---|------|-----|
| T1 | Source policy | Confirm ingest path uses only public exports or documented allowable files; document any store-specific export steps. |
| T2 | Window | Run ingest with known fixture dates; assert records outside the chosen week range are excluded or parameterized correctly. |
| T3 | Schema | Validated normalized output matches agreed shape (types, required fields). |
| T4 | PII handling | Spot-check or automated scan that raw reviewer handles/names are not passed through as plain identifiers to Phase 2 inputs (adjust if your pipeline strips at Phase 2 instead—then document the split). |

---

## Exit criteria (must all be true to leave Phase 1)

- [x] **EC1:** Ingest runs reproducibly on at least one real export sample (or realistic fixture) for your product. — *Met by fixtures under `phases/phase-01-data-and-compliance/fixtures/` + `pytest`.*
- [x] **EC2:** Written note states explicitly that **no login-based scraping** is used. — *See `phases/phase-01-data-and-compliance/SOURCE_INVENTORY.md`.*
- [x] **EC3:** Normalized data contract is stable enough for Phase 2 to depend on it. — *See `phases/phase-01-data-and-compliance/DATA_CONTRACT.md` + `schema_version`.*
- [x] **EC4:** PII/identifier rules are documented and reflected in tests or checklist. — *`DATA_CONTRACT.md`, `review_ingest/pii.py`, and `tests/test_pii.py` / `test_ingest_phase1.py`.*

---

## Sign-off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Implementer | | | |
| Reviewer (optional) | | | |
