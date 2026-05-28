import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

from .api import append_to_google_doc, send_email

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

from dotenv import load_dotenv
import os

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Phase 3: Connect to Workspace MCP Server")
    parser.add_argument("--pulse-file", type=str, default="out/pulse.md", help="Path to pulse markdown file")
    parser.add_argument("--doc-id", type=str, default=os.getenv("GOOGLE_DOC_ID"), help="Google Doc ID")
    parser.add_argument("--email-to", type=str, default=os.getenv("EMAIL_TO"), help="Email address")
    
    args = parser.parse_args()
    
    if not args.doc_id or not args.email_to:
        logging.error("Missing --doc-id or --email-to (or GOOGLE_DOC_ID / EMAIL_TO in .env)")
        sys.exit(1)
    
    pulse_path = Path(args.pulse_file)
    if not pulse_path.exists():
        logging.error(f"Pulse file not found at {pulse_path}. Run Phase 2 first!")
        sys.exit(1)
        
    logging.info(f"Reading pulse from {pulse_path}...")
    with open(pulse_path, "r", encoding="utf-8") as f:
        pulse_content = f.read()
        
    # Append to Google Doc
    try:
        logging.info("Pushing pulse to Google Docs via MCP...")
        doc_resp = append_to_google_doc(args.doc_id, pulse_content)
        logging.info(f"Docs MCP Response: {doc_resp}")
        # If the MCP server returns an error JSON, we should also fail
        if isinstance(doc_resp, dict) and doc_resp.get('status') == 'error':
            logging.error(f"MCP Server returned an error: {doc_resp.get('message')} - {doc_resp.get('details')}")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to append to Google Doc: {e}")
        sys.exit(1)
        
    # Create Gmail Draft -> Send Email
    try:
        logging.info("Sending pulse email via MCP...")
        subject = f"GROWW - Weekly Review Pulse - {datetime.now().strftime('%Y-%m-%d')}"
        email_resp = send_email(to=args.email_to, subject=subject, body=pulse_content)
        logging.info(f"Gmail MCP Response: {email_resp}")
        if isinstance(email_resp, dict) and email_resp.get('status') == 'error':
            logging.error(f"MCP Server returned an error: {email_resp.get('message')} - {email_resp.get('details')}")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
