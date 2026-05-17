# Review source inventory & policy

## Allowed sources (public / vendor-approved exports only)

This milestone accepts **only** data obtained through **legitimate, to-you** export paths, for example:

- **Apple App Store Connect:** ratings and reviews exports or downloads your team is entitled to as the app’s account holder (typically CSV from the developer console).
- **Google Play Console:** review exports or reports available to your developer account (typically CSV).

Operators must **not** use:

- Logged-in **scraping** of consumer-facing store pages where the brief forbids it  
- Third-party aggregators that violate Apple/Google terms  
- Any bypass of authentication that the problem statement rules out  

**This repository’s ingest path is “CSV file on disk you already obtained legitimately.”** It does not perform HTTP scraping or store login.

## Column mapping

Headers vary by platform and export version. The implementation flex-maps common column names (e.g. `Review`, `Review Text`, `Star Rating`, `Date`). See `review_ingest/mapping.py` for accepted aliases.

When Apple or Google change export column names, **version this mapping** in code and note the change in [decision.md](../../docs/decision.md).

## Time window

Rolling **8–12 weeks** of reviews (configurable `--weeks`). **Anchor date** for the window end is **`--as-of`** (UTC calendar date); default is **UTC today** if omitted (see decisions log).
