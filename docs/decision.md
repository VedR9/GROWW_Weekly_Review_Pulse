# Decision log (tech & business)

This file records **substantive decisions** made while shaping this project—problem scope, documentation structure, architectural constraints, and governance of the weekly pulse work. New decisions should be added **at the top** (after this intro) so the latest entries are easy to find.

**Format** (reuse for future entries):

**ID:** `DEC-YYYYMMDD-xxx` · **Date:** · **Status:** Proposed | Accepted | Superseded | Deprecated  
**Context:** · **Decision:** · **Consequences:** · **Alternatives considered:**

---

---

### DEC-20260517-011 — End-to-end orchestration runner

**Date:** 2026-05-17  
**Status:** Accepted  
**Context:** Need a single repeatable script to run all phases as requested in Phase 4.  
**Decision:** Implement `phases/phase-04-e2e-and-operations/e2e_runner.py` to trigger synthetic data generation, phase 1 ingest, phase 2 LLM generation, and phase 3 MCP sync synchronously using `subprocess`.  
**Consequences:** Operators have a single 1-click execution path documented in `RUNBOOK.md`.  
**Alternatives considered:** Bash script (rejected to maintain platform independence and error handling).

---

### DEC-20260517-010 — Phase 3 MCP integration pattern (REST vs SSE)

**Date:** 2026-05-17  
**Status:** Accepted  
**Context:** The provided MCP Server (`saksham-mcp-server-dvvb.onrender.com`) exposes a FastAPI REST layer (`/append_to_doc`, `/create_email_draft`) rather than standard MCP SSE or Stdio protocol.  
**Decision:** Integrate Phase 3 directly using HTTP `POST` requests via `httpx` to those explicitly exposed endpoints, instead of using the `mcp` Python client SDK.  
**Consequences:** Coupling to this specific server implementation's REST signature; auth issues inside the MCP server are bubbled up but cannot be solved client-side.  
**Alternatives considered:** Forcing SSE connection (rejected: server returned 404).

---

## Decisions

### DEC-20260510-009 — CSV column mapping rules (review vs review title)

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** Short body alias `"review"` substring-matched `"review title"`, so the wrong column was used as the review body.  
**Decision:** Ignore headers in `_IGNORE_HEADERS` (e.g. `reviewer`). For substring matches on alias `review`, require `normalize_header(column) == "review"` so **Review Title** maps to title, **Review** maps to body.  
**Consequences:** App Store–style exports with separate Title / Review columns behave as expected.  
**Alternatives considered:** Removing `"review"` from body aliases (breaks single-column `"Review"` header).

---

### DEC-20260510-008 — Phase 1 ingest: Python package, CLI, rolling window anchor

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** Phase 1 needs reproducible ingestion, tests, and a stable handoff to Phase 2 without mandating a host language for the whole agent.  
**Decision:** Implement Phase 1 as a Python package **`review_ingest`** under `phases/phase-01-data-and-compliance/`, installable from repo root via `pyproject.toml`, with CLI entrypoint **`review-ingest`**. Rolling window: **inclusive** end date `--as-of` (default **UTC calendar today**), length `--weeks` in **8–12** (default **10**). Dedup key: SHA-256 of `review_date` + body (prefix). UTF-8 / UTF-8-SIG / CP1252 decode attempts for CSV.  
**Consequences:** Phase 2 can consume JSONL; later phases may wrap or reimplement orchestration in another runtime without changing the contract.  
**Alternatives considered:** Node-only ingest; notebooks only (rejected: weaker CI reproducibility).

---

### DEC-20260510-007 — Phase implementation layout: `phases/phase-0X-*` at repo root

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** Documentation already lives under `docs/`; code needs a clear per-phase home.  
**Decision:** Place runnable code and phase-specific READMEs under **`phases/phase-01-data-and-compliance/`**, **`phases/phase-02-pulse-generation/`**, etc., parallel to **`docs/phases/*/eval.md`**.  
**Consequences:** Docs remain eval/theory; `phases/` holds executable artifacts.  
**Alternatives considered:** Single `src/` without phase folders (rejected: harder to navigate per milestone).

---

### DEC-20260510-006 — Documentation set split (architecture / plan / phases / decisions)

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** The milestone needs a clear place for design narrative, phased delivery, per-phase quality gates, and durable rationale without mixing everything into the problem statement.  
**Decision:** Maintain **four** doc types: [`architecture.md`](./architecture.md) (system design and boundaries), [`phase-by-implementationplan.md`](./phase-by-implementationplan.md) (phased work, no code-level prescription), under `docs/phases/**/eval.md` (tests and exit criteria per phase), and **`decision.md`** (this file) for ADR-style entries.  
**Consequences:** Contributors know where to update what; phase gates stay reviewable in isolation.  
**Alternatives considered:** Single monolithic README; folding eval criteria into the implementation plan only (rejected: harder to use as a checklist at phase boundaries).

---

### DEC-20260510-005 — Phase structure: four phases with linear dependency

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** Implementation needs an order of operations that matches data → insight → Workspace integration → operational readiness.  
**Decision:** Use **four** phases—**(1)** data and compliance, **(2)** pulse generation, **(3)** Docs + Gmail MCP, **(4)** end-to-end and operations—with **strict** ordering (later phases assume earlier exit criteria).  
**Consequences:** No skipping MCP setup before pulse format is stable; reduces rework when Gmail/Docs parameters change.  
**Alternatives considered:** Merging Phase 1 and 2 (rejected: conflates legal/data policy with narrative quality); merging Phase 3 and 4 (rejected: MCP auth deserves its own gate).

---

### DEC-20260510-004 — Per-phase `eval.md` as the quality gate

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** “Done” for a phase must be objective enough to stop endless polish.  
**Decision:** Each phase folder includes an **`eval.md`** containing **scoped tests**, **exit criteria** (checkboxes), and optional **sign-off**—and advancement requires satisfying that file, not informal agreement.  
**Consequences:** Phase exits are auditable; teams can tailor tests inside each `eval.md` without bloating the main plan.  
**Alternatives considered:** Exit criteria only inside `phase-by-implementationplan.md` (rejected: evals would be duplicated or too shallow per phase).

---

### DEC-20260510-003 — Google Workspace: MCP-only surface for Docs and Gmail in the application

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** The product brief requires Google Docs and Gmail integration **via MCP servers**, not bespoke Google API usage in application orchestration code.  
**Decision:** Treat **Google Docs MCP** and **Gmail MCP** as the **only** integration path for creating/updating the pulse document and creating the email draft (send optional). Do **not** embed parallel **direct** Docs/Gmail API clients in the same orchestration layer for those actions.  
**Consequences:** OAuth and API complexity concentrate in MCP server implementations; the host invokes **tools**, not raw REST from app code for those operations. Third-party MCP implementations may use Google SDKs internally—that is expected.  
**Alternatives considered:** Hybrid (MCP for drafts, direct API for “quick fixes”)—rejected as it violates the milestone constraint and blurs accountability.

---

### DEC-20260510-002 — Problem framing: MCP-first context in the problem statement

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** An earlier draft mixed deliverables with implementation detail; stakeholders needed a single narrative that **Workspace integration is MCP-driven**.  
**Decision:** Rewrite [`problemStatement.md`](../problemStatement.md) so **context & approach** upfront explain **why MCP** (boundary for Workspace auth/tools), map deliverables to **Docs MCP** and **Gmail MCP**, and restate the **no direct Google APIs for Docs/Gmail** constraint in both technical and “key constraints” sections.  
**Consequences:** Grading and partner review align on MCP; less ambiguity vs “use APIs elsewhere.”  
**Alternatives considered:** Leaving MCP details only in an appendix (rejected: easy to miss).

---

### DEC-20260510-001 — Filename for the phased implementation plan

**Date:** 2026-05-10  
**Status:** Accepted  
**Context:** Multiple naming conventions were possible (`implementation-plan.md`, `phases.md`, etc.).  
**Decision:** Standardize on **`phase-by-implementationplan.md`** under `docs/` as the canonical phased plan filename.  
**Consequences:** Links from `architecture.md`, phase evals, and `decision.md` use this path; renames require updating cross-references.  
**Alternatives considered:** `implementation-plan.md`, `roadmap.md`.

---

## Template (for new decisions)

Copy below this line when adding a brand-new decision from scratch:

---

**ID:** DEC-YYYYMMDD-001  
**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Superseded | Deprecated  
**Context:** What problem or uncertainty triggered this?  
**Decision:** What did we choose?  
**Consequences:** Trade-offs, follow-up work, or what breaks if we ignore this.  
**Alternatives considered:** Brief list.
