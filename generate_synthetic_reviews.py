import csv
import datetime
import random
import os

def generate_synthetic_reviews(weeks=52):
    play_store_path = "phases/phase-01-data-and-compliance/fixtures/sample_play_store.csv"
    app_store_path = "phases/phase-01-data-and-compliance/fixtures/sample_app_store.csv"
    
    now = datetime.datetime.now()
    reviews_data = [
        {"rating": 5, "title": "Great App", "text": "Works perfectly. I use it every day."},
        {"rating": 4, "title": "Good", "text": "Good but has some minor bugs."},
        {"rating": 3, "title": "Okay", "text": "It is okay but could be faster. Can someone at [email] contact me?"},
        {"rating": 2, "title": "Issues", "text": "Having login issues since the latest update. @support please fix."},
        {"rating": 1, "title": "Terrible", "text": "Crashes on startup. Unusable."},
        {"rating": 5, "title": "Awesome", "text": "The new UI is fantastic and payments are quick."},
        {"rating": 4, "title": "Solid", "text": "Solid app for KYC but takes too long to approve."},
        {"rating": 3, "title": "Average", "text": "Customer support is slow to respond to my queries."},
        {"rating": 2, "title": "Disappointed", "text": "Statements are hard to download. Needs improvement."},
        {"rating": 5, "title": "Love it", "text": "Seamless onboarding process. Very impressed."},
    ]
    
    # Generate Play Store CSV
    with open(play_store_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Star Rating", "Review Title", "Review Text", "Review Last Update Date"])
        for i in range(500):
            days_ago = random.randint(0, weeks * 7)
            date = (now - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")
            template = random.choice(reviews_data)
            writer.writerow([template["rating"], template["title"], template["text"], date])
            
    # Generate App Store CSV
    with open(app_store_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Rating", "Review Title", "Review", "Date", "Reviewer"])
        for i in range(500):
            days_ago = random.randint(0, weeks * 7)
            date = (now - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")
            template = random.choice(reviews_data)
            writer.writerow([template["rating"], template["title"], template["text"], date, f"User{random.randint(100, 999)}"])
            
    print(f"Generated 500 mock Play Store reviews to {play_store_path}")
    print(f"Generated 500 mock App Store reviews to {app_store_path}")

if __name__ == "__main__":
    generate_synthetic_reviews()
