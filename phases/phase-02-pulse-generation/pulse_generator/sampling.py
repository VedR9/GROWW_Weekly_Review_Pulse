import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# A simple heuristic: 1 word ~ 1.3 tokens
def estimate_tokens(text: str) -> int:
    return int(len(text.split()) * 1.3)

def load_reviews(jsonl_path: str) -> List[Dict[str, Any]]:
    reviews = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                reviews.append(json.loads(line))
    return reviews

def stratified_sample(reviews: List[Dict[str, Any]], max_tokens: int = 6000) -> List[Dict[str, Any]]:
    """
    Applies Stratified Token Budgeting.
    Prioritizes 1-star and 2-star reviews. Then fills remaining budget with 3-star, and finally 4/5-star.
    """
    # Group by rating
    critical = [r for r in reviews if r.get('rating') in (1.0, 2.0)]
    neutral = [r for r in reviews if r.get('rating') == 3.0]
    positive = [r for r in reviews if r.get('rating') in (4.0, 5.0)]
    
    # Sort each group by date (newest first)
    critical.sort(key=lambda r: r.get('review_date', ''), reverse=True)
    neutral.sort(key=lambda r: r.get('review_date', ''), reverse=True)
    positive.sort(key=lambda r: r.get('review_date', ''), reverse=True)
    
    sampled = []
    current_tokens = 0
    
    def add_reviews(source_list):
        nonlocal current_tokens
        for r in source_list:
            text = f"[Rating: {r.get('rating')}] {r.get('title', '')}: {r.get('body', '')}"
            tokens = estimate_tokens(text)
            if current_tokens + tokens > max_tokens:
                break
            sampled.append(r)
            current_tokens += tokens

    # Priority 1: Critical reviews
    add_reviews(critical)
    
    # Priority 2: Neutral reviews
    if current_tokens < max_tokens:
        add_reviews(neutral)
        
    # Priority 3: Positive reviews
    if current_tokens < max_tokens:
        add_reviews(positive)
        
    logger.info(f"Sampled {len(sampled)} reviews out of {len(reviews)} (Estimated tokens: {current_tokens})")
    return sampled

def format_for_prompt(sampled_reviews: List[Dict[str, Any]]) -> str:
    lines = []
    for r in sampled_reviews:
        lines.append(f"Rating: {r.get('rating')} | Date: {r.get('review_date')} | Title: {r.get('title')}\nBody: {r.get('body')}\n")
    return "\n".join(lines)
