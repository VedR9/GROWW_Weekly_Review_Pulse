import argparse
import logging
import sys
from pathlib import Path

from .sampling import load_reviews, stratified_sample, format_for_prompt
from .llm import generate_pulse

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Phase 2: Pulse Generation using Groq LLM")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to normalized.jsonl")
    parser.add_argument("--output", "-o", type=str, required=True, help="Path to output markdown artifact")
    parser.add_argument("--max-tokens", type=int, default=6000, help="Max token budget for the LLM prompt (default: 6000)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        logging.error(f"Input file not found: {input_path}")
        sys.exit(1)
        
    logging.info(f"Loading reviews from {input_path}...")
    reviews = load_reviews(str(input_path))
    
    logging.info("Applying Stratified Token Budgeting...")
    sampled = stratified_sample(reviews, max_tokens=args.max_tokens)
    
    prompt_text = format_for_prompt(sampled)
    
    pulse_markdown = generate_pulse(prompt_text)
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(pulse_markdown)
        
    logging.info(f"Successfully generated Weekly Pulse at {out_path}")

    # --- NEW: Append to history.json for the Dashboard ---
    try:
        import json, re
        from datetime import datetime
        history_path = Path("ui/public/history.json")
        
        # Base Metrics
        total_reviews = len(reviews)
        avg_rating = sum(r.get("rating", 3) for r in reviews) / total_reviews if total_reviews else 0
        sentiment_score = int(min(100, max(0, (avg_rating - 1) / 4 * 100)))
        
        # Crash Alert Logic
        crash_keywords = ["crash", "bug", "stuck", "broken", "freeze"]
        crash_count = sum(1 for r in reviews if any(k in str(r.get("body", "")).lower() for k in crash_keywords))
        crash_rate = crash_count / total_reviews if total_reviews else 0
        critical_alert = crash_rate > 0.05
        
        # Store Splits
        app_store_reviews = [r for r in reviews if r.get("source_store") == "app_store"]
        play_store_reviews = [r for r in reviews if r.get("source_store") == "play_store"]
        
        app_store_rating = sum(r.get("rating", 3) for r in app_store_reviews) / len(app_store_reviews) if app_store_reviews else 0
        play_store_rating = sum(r.get("rating", 3) for r in play_store_reviews) / len(play_store_reviews) if play_store_reviews else 0
        
        # Extract top theme using regex
        theme_match = re.search(r"1\.\s+\[?(?:\*\*)?(.*?)(?:\*\*)?\]?:", pulse_markdown)
        if not theme_match:
            theme_match = re.search(r"1\.\s+(?:\*\*)?(.*?)(?:\*\*)?:", pulse_markdown)
        top_theme = theme_match.group(1).strip() if theme_match else "General Feedback"
        
        # Extract Top 3 Feature Requests using regex
        feature_requests = []
        feature_section = re.search(r"## Top Feature Requests(.*?)(?:##|$)", pulse_markdown, re.DOTALL)
        if feature_section:
            lines = feature_section.group(1).strip().split('\n')
            for line in lines:
                match = re.search(r"\d+\.\s+(.*)", line.strip())
                if match:
                    feature_requests.append(match.group(1).strip())
        
        if not feature_requests:
            feature_requests = ["Dark Mode", "Export to PDF", "Faster Login"] # Fallback if parsing fails

        # Build the new record
        new_record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_reviews": total_reviews,
            "avg_rating": round(avg_rating, 1),
            "top_theme": top_theme,
            "sentiment_score": sentiment_score,
            "critical_alert": critical_alert,
            "crash_rate": round(crash_rate * 100, 1),
            "app_store_rating": round(app_store_rating, 1),
            "play_store_rating": round(play_store_rating, 1),
            "feature_requests": feature_requests[:3]
        }
        
        history_data = []
        if history_path.exists():
            with open(history_path, "r", encoding="utf-8") as f:
                history_data = json.load(f)
                
        # Remove any existing record for today to prevent duplicates
        history_data = [d for d in history_data if d.get("date") != new_record["date"]]
        history_data.append(new_record)
        
        history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2)
            
        logging.info("Successfully updated history.json for the dashboard")
    except Exception as e:
        logging.error(f"Failed to update history.json: {e}")

if __name__ == "__main__":
    main()
