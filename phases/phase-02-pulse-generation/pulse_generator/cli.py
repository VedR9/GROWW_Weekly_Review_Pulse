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

if __name__ == "__main__":
    main()
