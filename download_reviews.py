import csv
import datetime
from google_play_scraper import reviews, Sort
from app_store_scraper import AppStore
import logging

logging.basicConfig(level=logging.INFO)

def download_play_store_reviews(app_id="com.whatsapp", weeks=12, out_path="phases/phase-01-data-and-compliance/fixtures/sample_play_store.csv"):
    logging.info(f"Downloading Play Store reviews for {app_id}...")
    cutoff_date = datetime.datetime.now() - datetime.timedelta(weeks=weeks)
    
    result, continuation_token = reviews(
        app_id,
        lang='en', # defaults to 'en'
        country='us', # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.NEWEST
        count=200 # retrieve enough to hopefully cover the 12 weeks
    )
    
    # Write to CSV
    with open(out_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Star Rating", "Review Title", "Review Text", "Review Last Update Date"])
        count = 0
        for r in result:
            if r['at'] >= cutoff_date:
                writer.writerow([
                    r['score'],
                    "Play Store Review", # Play Store doesn't have review titles in the same way, we can mock or leave blank
                    r['content'].replace('\n', ' '),
                    r['at'].strftime("%Y-%m-%d")
                ])
                count += 1
    logging.info(f"Saved {count} Play Store reviews to {out_path}")

def download_app_store_reviews(app_name="whatsapp", app_id=310633997, weeks=12, out_path="phases/phase-01-data-and-compliance/fixtures/sample_app_store.csv"):
    logging.info(f"Downloading App Store reviews for {app_name}...")
    app = AppStore(country="us", app_name=app_name, app_id=app_id)
    app.review(how_many=200)
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(weeks=weeks)
    
    # Write to CSV
    with open(out_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Rating", "Review Title", "Review", "Date", "Reviewer"])
        count = 0
        for r in app.reviews:
            date_obj = r['date']
            if date_obj >= cutoff_date:
                writer.writerow([
                    r['rating'],
                    r.get('title', '').replace('\n', ' '),
                    r['review'].replace('\n', ' '),
                    date_obj.strftime("%Y-%m-%d"),
                    r.get('userName', 'Unknown')
                ])
                count += 1
    logging.info(f"Saved {count} App Store reviews to {out_path}")

if __name__ == "__main__":
    download_play_store_reviews()
    download_app_store_reviews()
