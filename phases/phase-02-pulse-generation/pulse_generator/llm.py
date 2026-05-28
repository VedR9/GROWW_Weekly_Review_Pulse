import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

load_dotenv()

# Fallback to an empty string to allow testing initialization
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

def generate_pulse(reviews_text: str) -> str:
    """
    Calls the Groq LLM to generate the weekly pulse summary.
    """
    if not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY is not set. Generating a mock pulse artifact for testing.")
        return _mock_pulse()

    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
You are an expert product analyst. I am providing you with a list of recent app store reviews.
Your task is to generate a "Weekly Pulse" one-page summary based exactly on these reviews.

Constraints:
1. Max 5 themes considered, but only surface the TOP 3 themes in the note.
2. Provide exactly 3 real user quotes (anonymize them by removing names, emails, handles).
3. Provide exactly 3 actionable ideas based on the themes.
4. Provide exactly 3 Top Feature Requests based on what users are asking for. You MUST include an estimated percentage of users asking for this feature based on the review sample (e.g., "1. Dark Mode (15%)").
5. The pulse body MUST be concise.
6. Format the output in Markdown.

Reviews:
{reviews_text}

Output Format:
# GROWW - Weekly Review Pulse

## Top Themes
1. [Theme 1]: [Brief description]
2. [Theme 2]: [Brief description]
3. [Theme 3]: [Brief description]

## Top Feature Requests
1. [Feature 1] ([X]%)
2. [Feature 2] ([X]%)
3. [Feature 3] ([X]%)

## User Quotes
- "[Quote 1]"
- "[Quote 2]"
- "[Quote 3]"

## Action Ideas
- [Action 1]
- [Action 2]
- [Action 3]
"""

    logger.info("Calling Groq LLM (llama-3.3-70b-versatile)...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3, # Low temperature for more analytical/factual output
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to generate pulse with Groq: {e}")
        raise

def _mock_pulse() -> str:
    return """# GROWW - Weekly Review Pulse

## Top Themes
1. **Login Issues**: Users are experiencing issues logging in after the recent update.
2. **Slow Customer Support**: Multiple reports of support tickets taking days to resolve.
3. **Downloading Statements**: Users find it difficult to locate and download PDF statements.

## Top Feature Requests
1. Dark Mode for the dashboard (18%)
2. Fingerprint authentication on Android (12%)
3. Export transaction history to Excel (8%)

## User Quotes
- "Having login issues since the latest update. please fix."
- "Customer support is slow to respond to my queries."
- "Statements are hard to download. Needs improvement."

## Action Ideas
- Product: Add a highly visible "Download Statement" button on the main dashboard.
- Engineering: Investigate the authentication flow regressions introduced in the last build.
- Support: Implement an auto-responder SLA to acknowledge tickets faster.
"""
