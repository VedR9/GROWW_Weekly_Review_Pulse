# Phase 4 — Evaluation: End-to-end and operations

**Phase:** [phase-04-e2e-and-operations](./) · **Plan:** [phase-by-implementationplan](../../phase-by-implementationplan.md)

---

## Scope under test

- Full flow: **ingest → pulse generation → Google Docs MCP → Gmail MCP**.
- Repeatability and clarity for a “weekly run.”
- Alignment with [architecture.md](../../architecture.md) and [problemStatement.md](../../../problemStatement.md).

---

## Testing

| # | Test | How |
|---|------|-----|
| T1 | E2E happy path | One command or documented agent session from fresh export folder to Doc + Gmail draft without manual content copying. |
| T2 | Idempotency / versioning | Second run updates Doc (or creates new doc per policy) without corrupting prior content; document behavior. |
| T3 | Constraint regression | Re-check no PII, ≤5 themes, ≤250 words, public data only on the E2E output. |
| T4 | Runbook | Another person can follow written steps to reproduce (within access to exports and MCP auth). |

---

## Exit criteria

- [ ] **EC1:** E2E run completed successfully at least once with evidence (screenshots or logs acceptable).
- [ ] **EC2:** [architecture.md](../../architecture.md) matches as-built behavior (update architecture if you changed boundaries).
- [ ] **EC3:** Open decisions or known limitations captured in [decision.md](../../decision.md) or a short “Known gaps” subsection there.
- [ ] **EC4:** Milestone deliverables from the problem statement are demonstrably met (pulse in Docs, email draft, constraints).

---

## Sign-off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Implementer | | | |
| Reviewer (optional) | | | |
