# Problem Statement

## Context & approach

This milestone builds on the **same product you selected in Milestone 1**. The goal is an automated **weekly pulse** from recent **App Store** and **Play Store** reviews, delivered through **Google Workspace using MCP (Model Context Protocol)**, not by calling Google APIs directly from your code.

**Why MCP:** The agent (or app) should integrate with **Google Docs** and **Gmail** via configured **MCP servers** that expose document and mail capabilities as tools. That keeps Workspace auth and behavior in the MCP layer and satisfies the requirement to avoid embedding raw Google API clients for Docs/Gmail in the solution.

---

## What you deliver

1. Turn recent store reviews into a **one-page weekly pulse** with:
   - **Top themes**
   - **Real user quotes**
   - **Three action ideas**
2. **Record that pulse in Google Docs** (create/update the document) using the **Google Docs MCP server**.
3. **Send yourself a draft email** containing the weekly note using the **Gmail MCP server** (draft or send, per your setup—still MCP-driven, not direct Gmail API usage in application code).

---

👥 **Who this helps**

- **Product / Growth** — see what to fix next
- **Support** — know what users are saying and acknowledge it
- **Leadership** — a quick weekly health pulse

---

🛠️ **What you must build**

- Import reviews from the **last 8–12 weeks** (rating, title, text, date) from **public review exports only** — **no** scraping behind logins.
- Group reviews into **5 themes max** (e.g., onboarding, KYC, payments, statements, withdrawals).
- Produce a **weekly one-page note**:
  - Top **3** themes
  - **3** user quotes
  - **3** action ideas
- **Persist and present** the note in **Google Docs** via **Docs MCP** (the “one-pager” lives there).
- **Draft the notification email** in **Gmail** via **Gmail MCP**, addressed to yourself or an alias.
- **Do not include PII** in any artifact.

---

🔧 **Technical implementation (MCP for Workspace)**

All **Google Docs** and **Gmail** operations required for this milestone must go through **MCP servers**, not through direct Google REST API calls from your app logic.

| Area | Required integration |
|------|----------------------|
| Weekly pulse document | **Google Docs MCP server** — create/update the one-page pulse |
| Draft email with the note | **Gmail MCP server** — compose/draft (and send if your flow requires it) |

You must **configure and authenticate** those MCP servers appropriately (OAuth / service account / whatever your chosen servers document). Your implementation should **invoke MCP tools/capabilities** for Docs and Gmail rather than duplicating the same flows with the official Google APIs in code.

---

⚠️ **Key constraints**

- **Public review exports only** — no authenticated-store scraping.
- **Max 5 themes** for grouping.
- Pulse text **scannable, ≤250 words** where the brief specifies length for the note body.
- **No usernames, emails, or IDs** in any deliverable artifact.
- **Google Workspace (Docs + Gmail) must use MCP servers; do not substitute direct Google APIs for those integrations.**
