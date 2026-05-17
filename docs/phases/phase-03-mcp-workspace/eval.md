# Phase 3 — Evaluation: MCP (Google Docs + Gmail)

**Phase:** [phase-03-mcp-workspace](./) · **Plan:** [phase-by-implementationplan](../../phase-by-implementationplan.md)

---

## Scope under test

- **Google Docs MCP:** create/update document containing the weekly pulse.
- **Gmail MCP:** create draft (and optional send if in scope) with pulse content.
- **No** direct Google Docs/Gmail REST client usage in application code for these operations—**MCP tools only**.

---

## Testing

| # | Test | How |
|---|------|-----|
| T1 | Docs MCP | From host, invoke Docs MCP tool(s); verify a Doc exists with expected title/sections/body. |
| T2 | Gmail MCP | Invoke Gmail MCP to create draft; open Gmail UI and confirm draft subject/body/recipient. |
| T3 | Boundary check | Code search or dependency audit: no `googleapis` / raw REST calls for Docs+Gmail in app paths that duplicate MCP (allow exceptions only if documented in [decision.md](../../decision.md)). |
| T4 | Auth recovery | Document how to refresh tokens or re-auth if MCP disconnects; smoke-test after token refresh if applicable. |
| T5 | Failure modes | Induce a controlled error (e.g. invalid doc ID); confirm error surfaces clearly and no partial secrets leak in logs. |

---

## Exit criteria

- [ ] **EC1:** At least one successful **Docs MCP** write of the pulse content end-to-end.
- [ ] **EC2:** At least one successful **Gmail MCP** draft (or send, if required) with aligned content.
- [ ] **EC3:** MCP configuration documented with **secrets redacted**.
- [ ] **EC4:** Explicit confirmation that Workspace operations for this milestone use **MCP**, not parallel API code paths.

---

## Sign-off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Implementer | | | |
| Reviewer (optional) | | | |
