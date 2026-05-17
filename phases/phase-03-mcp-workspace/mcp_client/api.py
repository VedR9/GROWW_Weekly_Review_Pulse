import logging
import httpx
from typing import Dict, Any

logger = logging.getLogger(__name__)

BASE_URL = "https://saksham-mcp-server-dvvb.onrender.com"

def append_to_google_doc(doc_id: str, content: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/append_to_doc"
    payload = {
        "doc_id": doc_id,
        "content": content
    }
    
    logger.info(f"Calling MCP Server to append to doc: {doc_id}")
    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

def send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/send_email"
    payload = {
        "to": to,
        "subject": subject,
        "body": body
    }
    
    logger.info(f"Calling MCP Server to send email to: {to}")
    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
