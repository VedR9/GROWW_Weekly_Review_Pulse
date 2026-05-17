# GROWW - Weekly Review Pulse Runbook

## Overview
This runbook describes the end-to-end operation of the **GROWW - Weekly Review Pulse Agent**. The pipeline ingests reviews, uses the Groq LLM to generate themes and actionable insights, and synchronizes the output directly to Google Docs and Gmail using an MCP Server.

## Prerequisites
1. **Python Environment**: `python 3.10+` with dependencies listed in `pyproject.toml` (or using the `mcp`, `groq`, `httpx` and `python-dotenv` packages).
2. **Environment Variables (`.env`)**:
   - `GROQ_API_KEY`: API Key for the Groq LLM.
   - `GOOGLE_DOC_ID`: The ID of the target Google Doc (e.g., `1mXXX8-ggVEteGS9rC3s3H_Bq4NZAfTM89sU9Q1OBi5E`).
   - `EMAIL_TO`: The target email for the draft (e.g., `creditcardbhaina@gmail.com`).
3. **MCP Server**: The remote MCP Server (`https://saksham-mcp-server-dvvb.onrender.com/`) must be running and have valid `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` configured in its deployment environment to interact with Google Workspace.

## Execution

To execute the entire end-to-end pipeline, run the orchestrator script from the root of the project:

```bash
PYTHONPATH=phases/phase-01-data-and-compliance:phases/phase-02-pulse-generation:phases/phase-03-mcp-workspace .venv/bin/python phases/phase-04-e2e-and-operations/e2e_runner.py
```

### What happens during the run?
1. **Synthetic Data**: Generates the CSV of reviews (mocked for this repository).
2. **Phase 1 (Ingest)**: Normalizes and scrubs PII from the CSV into `out/normalized.jsonl`.
3. **Phase 2 (Pulse Generation)**: Samples top reviews and calls `llama-3.3-70b-versatile` on Groq to extract the top 3 themes, 3 quotes, and 3 actionable insights, saved to `out/pulse.md`.
4. **Phase 3 (MCP Sync)**: Connects to the remote Workspace MCP Server to append the markdown to the target Google Doc and draft an email.

## Troubleshooting

| Error | Root Cause | Fix |
|-------|------------|-----|
| `Request too large for model` | Groq rate limits hit (12K TPM). | Make sure `--max-tokens` is strictly set to 3000 in the orchestrator runner. |
| `Missing GOOGLE_TOKEN_JSON` | The Remote MCP Server is missing valid auth tokens. | Contact the server administrator to update the Render instance environment variables with valid Workspace OAuth tokens. |
| `The read operation timed out` | The Render MCP Server is taking too long to spin up (Cold Start). | The script is configured with a 120s timeout. If it still times out, visit the MCP server URL manually in a browser to wake it up, then re-run. |

## Contact
For pipeline failures, check the logs printed in the console. For authentication failures against Google Docs/Gmail, verify the Render MCP Server status.
