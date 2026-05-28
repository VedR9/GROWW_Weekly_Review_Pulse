import logging
import subprocess
import sys
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def run_step(name: str, cmd: list):
    logging.info(f"=== Starting {name} ===")
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        logging.info(result.stdout)
        logging.info(f"=== Finished {name} ===")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error in {name}:")
        logging.error(e.stderr)
        sys.exit(1)

def main():
    load_dotenv()
    
    # 1. Ensure env vars are set
    if not os.getenv("GROQ_API_KEY"):
        logging.error("Missing GROQ_API_KEY in .env")
        sys.exit(1)
        
    doc_id = os.getenv("GOOGLE_DOC_ID")
    email_to = os.getenv("EMAIL_TO")
    
    if not doc_id or not email_to:
        logging.error("Missing GOOGLE_DOC_ID or EMAIL_TO in .env")
        sys.exit(1)

    # Note: Phase 1 (Ingest) usually assumes CSV input. We generate synthetic first.
    run_step("Synthetic Data Generation", [
        sys.executable, "generate_synthetic_reviews.py"
    ])

    # 1. Phase 1: Ingest
    run_step("Phase 1: Review Ingestion & Normalization", [
        sys.executable, "-m", "review_ingest.cli",
        "--input", "phases/phase-01-data-and-compliance/fixtures/sample_play_store.csv",
        "--input", "phases/phase-01-data-and-compliance/fixtures/sample_app_store.csv",
        "--output", "out/normalized.jsonl",
        "--weeks", "52"
    ])

    # 2. Phase 2: Pulse Generation
    run_step("Phase 2: Pulse Generation via Groq", [
        sys.executable, "-m", "pulse_generator.cli",
        "--input", "out/normalized.jsonl",
        "--output", "out/pulse.md",
        "--max-tokens", "3000"
    ])

    # 3. Phase 3: MCP Sync (Google Docs + Gmail)
    run_step("Phase 3: MCP Workspace Integration", [
        sys.executable, "-m", "mcp_client.cli",
        "--pulse-file", "out/pulse.md",
        "--doc-id", doc_id,
        "--email-to", email_to
    ])
    
    logging.info("🎉 E2E Pipeline Completed Successfully!")

if __name__ == "__main__":
    # Ensure correct PYTHONPATH
    os.environ["PYTHONPATH"] = "phases/phase-01-data-and-compliance:phases/phase-02-pulse-generation:phases/phase-03-mcp-workspace:" + os.environ.get("PYTHONPATH", "")
    main()
