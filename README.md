# GROWW Weekly Review Pulse 🚀

Automated end-to-end pipeline to ingest app reviews, generate actionable insights using LLMs, and push a summary directly to Google Workspace via the Model Context Protocol (MCP).

## Overview

The **GROWW Weekly Review Pulse Agent** addresses the challenge of manually parsing hundreds of app reviews every week. By leveraging the fast inference of Groq and a customized MCP Server, it autonomously aggregates feedback into clear themes and actionable insights, then drafts an email and appends the notes to a Google Doc. 

## Key Features
- **Review Normalization**: Ingests, scrubs PII, and normalizes app reviews into an optimized `jsonl` format.
- **LLM-Powered Insights**: Calls `llama-3.3-70b-versatile` on Groq to extract top themes, key quotes, and actionable product suggestions.
- **MCP Workspace Integration**: Avoids hardcoded Google SDKs in the application. Instead, it natively utilizes a remote MCP Server to abstract Google Docs and Gmail integration.
- **Fully Automated via GitHub Actions**: Runs autonomously in the cloud every Sunday at 10 AM IST.

## Architecture & Implementation Phases

The project was constructed in four strict phases to ensure modularity and reliability:

1. **[Phase 1: Data & Compliance](phases/phase-01-data-and-compliance)** 
   Handles ingestion of raw CSV reviews. It applies a rolling window and strips personally identifiable information (PII) before saving normalized JSONL data.
2. **[Phase 2: Pulse Generation](phases/phase-02-pulse-generation)** 
   Samples the cleaned reviews, structuring a robust prompt that is sent to the Groq API. Outputs the final pulse as Markdown.
3. **[Phase 3: MCP Workspace](phases/phase-03-mcp-workspace)** 
   Interfaces directly with an external FastAPI-based MCP server to push the generated Markdown to a Google Doc and draft an email—fully decoupling Google OAuth from this codebase.
4. **[Phase 4: E2E Orchestration](phases/phase-04-e2e-and-operations)** 
   Wraps all previous phases into a single, synchronous execution path, ready for cron or CI/CD scheduling.

*For deeper technical details and decisions, check the [`docs/`](docs/) directory and the [`RUNBOOK.md`](RUNBOOK.md).*

## Setup & Local Execution

### Prerequisites
- Python 3.10+
- An active `GROQ_API_KEY`
- A valid `GOOGLE_DOC_ID` and target `EMAIL_TO`
- A deployed MCP server providing `/append_to_doc` and `/send_email`

### Installation
Clone the repository and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Create a `.env` file at the root level and configure your variables:
```env
GROQ_API_KEY=your_key_here
GOOGLE_DOC_ID=your_doc_id_here
EMAIL_TO=your_email@example.com
MCP_SERVER_URL=https://your-mcp-server.onrender.com
```

### Running the Pipeline
Execute the orchestrator to run the entire pipeline:
```bash
python phases/phase-04-e2e-and-operations/e2e_runner.py
```

## Cloud Automation

This project includes a fully configured GitHub Actions workflow (`.github/workflows/weekly_pulse.yml`).
When deployed to GitHub, the pipeline runs securely every **Sunday at 10:00 AM IST**. 
To enable this, simply add the variables from your `.env` file as **Repository Secrets** in your GitHub Settings.

---
*Built for fast, actionable, and secure product review analysis.*
