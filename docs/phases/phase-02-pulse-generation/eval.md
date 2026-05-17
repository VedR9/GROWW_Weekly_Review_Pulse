# Phase 2 — Evaluation: Pulse generation

**Phase:** [phase-02-pulse-generation](./) · **Plan:** [phase-by-implementationplan](../../phase-by-implementationplan.md)

---

## Scope under test

- At most **5** theme buckets used internally; **top 3** themes in the output.
- **3** user quotes and **3** action ideas.
- Pulse body **≤250 words** and **scannable** (headings/bullets OK if your format allows).
- **No** usernames, emails, or IDs in generated text.

---

## Testing

| # | Test | How |
|---|------|-----|
| T1 | Theme cap | Input diverse reviews; verify clustering/grouping uses ≤5 themes and surfaced list shows 3 themes. |
| T2 | Counts | Assert exactly 3 quotes and 3 action ideas in structured output. |
| T3 | Word limit | Programmatic or manual count on pulse body; fails if >250 words per brief. |
| T4 | PII avoidance | Review sample outputs for emails, @handles, phone patterns; red-team with borderline inputs. |
| T5 | Consistency | Same fixture input → stable structure (JSON/markdown sections) for Phase 3 consumption. |

---

## Exit criteria

- [ ] **EC1:** Generated pulse matches required structure (themes, quotes, actions).
- [ ] **EC2:** Theme and word-count constraints verified by test or documented checklist.
- [ ] **EC3:** Sample outputs archived (sanitized) as golden references optional but recommended.
- [ ] **EC4:** Output format agreed for Phase 3 (plain text/markdown blocks for Doc + email).

---

## Sign-off

| Role | Name | Date | Notes |
|------|------|------|-------|
| Implementer | | | |
| Reviewer (optional) | | | |
