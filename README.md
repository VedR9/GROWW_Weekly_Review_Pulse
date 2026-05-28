# GROWW Weekly Review Pulse & Dashboard 🚀

An automated end-to-end pipeline and sleek Product Analytics Dashboard to ingest app reviews, generate actionable AI insights, and surface them for Product Managers.

## Overview

The **GROWW Weekly Review Pulse** addresses the challenge of manually parsing hundreds of app reviews every week. It autonomously aggregates feedback into clear themes and actionable insights, drafts an email, appends notes to a Google Doc, and **powers a real-time web dashboard**—all completely automatically.

## 📊 Product Analytics Dashboard
A premium, backend-less React dashboard designed specifically for Product Managers. It provides a real-time, week-over-week view of the product's health.
- **Critical Crash Alerts**: Automatically detects spikes in "crash" or "bug" mentions and flashes a system health warning banner, comparing the crash rate week-over-week.
- **Feature Request Radar**: AI analyzes thousands of reviews to extract the Top 3 most requested features, complete with a percentage estimate of how many users are asking for it (rendered as progress bars).
- **AI Action Ideas**: The LLM suggests strategic product roadmap items based on the week's top complaints, presented as a clear checklist.
- **Platform Sentiment Splits**: Breaks down the average app rating into 🍏 iOS App Store and 🤖 Android Play Store specific metrics.

## ⚙️ Architecture & Data Flow

This project utilizes a modern **Serverless / GitOps** architecture to run entirely for free without needing a database:

1. **Python Data Pipeline (`phases/`)**: Every Sunday, GitHub Actions runs the Python pipeline. It scrubs PII from CSVs, calls the Groq LLM API (`llama-3.3-70b`) to extract insights, and calculates mathematical sentiment scores.
2. **MCP Integrations**: A remote Model Context Protocol (MCP) server pushes the raw markdown pulse directly to Google Docs and Gmail.
3. **GitOps Persistence**: The pipeline appends the week's metrics to `ui/public/history.json` and automatically commits/pushes the file back to the `master` branch.
4. **Vercel Frontend (`ui/`)**: Vercel detects the new commit and instantly deploys the updated static React dashboard, acting as a database-free frontend.

## Local Setup & Execution

### Prerequisites
- Python 3.10+ & Node.js 18+
- An active `GROQ_API_KEY`
- A valid `GOOGLE_DOC_ID` and target `EMAIL_TO`

### Running the Data Pipeline
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run the full extraction pipeline
python phases/phase-04-e2e-and-operations/e2e_runner.py
```

### Running the Dashboard Locally
```bash
cd ui
npm install
npm run dev
```

## Cloud Automation

This project includes a fully configured GitHub Actions workflow (`.github/workflows/weekly_pulse.yml`).
When deployed to GitHub, the pipeline runs securely every **Sunday at 10:00 AM IST**. 

---
*Built for fast, actionable, and secure product review analysis.*
