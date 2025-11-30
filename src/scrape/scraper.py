"""
Google Play Store Review Scraper
Task 1: Data Collection for Ethiopian banks
Folder: C:\Users\HP\OneDrive\Documents\bank-reviews\src\scrape
"""

import sys
import os
import time
from datetime import datetime
from tqdm import tqdm
import pandas as pd

# Ensure Python can find config.py in the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS

from google_play_scraper import app, Sort, reviews


class PlayStoreScraper:
    def __init__(self):
        # Load configuration from config.py
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.reviews_per_bank = SCRAPING_CONFIG['reviews_per_bank']
        self.lang = SCRAPING_CONFIG['lang']
        self.country = SCRAPING_CONFIG['country']
        self.max_retries = SCRAPING_CONFIG['max_retries']

    def get_app_info(self, app_id):
        try:
            result = app(app_id, lang=self.lang, country=self.country)
            return {
                'app_id': app_id,
                'title': result.get('title', 'N/A'),
                'score': result.get('score', 0),
                'ratings': result.get('ratings', 0),
                'reviews': result.get('reviews', 0),
                'installs': result.get('installs', 'N/A')
            }
        except Exception as e:
            print(f"Error getting app info for {app_id}: {e}")
            return None

    def scrape_reviews(self, app_id, count=400):
        print(f"\nScraping reviews for {app_id}...")
        for attempt in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=count,
                    filter_score_with=None
                )
                print(f"Scraped {len(result)} reviews")
                return result
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                if attempt < self.max_retries - 1:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("Failed to scrape reviews after max retries")
                    return []

    def process_reviews(self, reviews_data, bank_code):
        processed = []
        for review in reviews_data:
            processed.append({
                'review_id': review.get('reviewId', ''),
                'review_text': review.get('content', ''),
                'rating': review.get('score', 0),
                'review_date': review.get('at', datetime.now()),
                'user_name': review.get('userName', 'Anonymous'),
                'thumbs_up': review.get('thumbsUpCount', 0),
                'reply_content': review.get('replyContent', None),
                'bank_code': bank_code,
                'bank_name': self.bank_names[bank_code],
                'app_version': review.get('reviewCreatedVersion', 'N/A'),
                'source': 'Google Play'
            })
        return processed

    def scrape_all_banks(self):
        all_reviews = []
        app_info_list = []

        print("="*60)
        print("Starting Google Play Store Review Scraper")
        print("="*60)

        # Phase 1: App Info
        print("\n[1/2] Fetching app info...")
        for bank_code, app_id in self.app_ids.items():
            info = self.get_app_info(app_id)
            if info:
                info['bank_code'] = bank_code
                info['bank_name'] = self.bank_names[bank_code]
                app_info_list.append(info)

        if app_info_list:
            df_info = pd.DataFrame(app_info_list)
            os.makedirs(DATA_PATHS['raw'], exist_ok=True)
            df_info.to_csv(f"{DATA_PATHS['raw']}/app_info.csv", index=False)
            print(f"App info saved to {DATA_PATHS['raw']}/app_info.csv")

        # Phase 2: Scrape reviews
        print("\n[2/2] Scraping reviews...")
        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Banks"):
            reviews_data = self.scrape_reviews(app_id, self.reviews_per_bank)
            if reviews_data:
                processed = self.process_reviews(reviews_data, bank_code)
                all_reviews.extend(processed)
            time.sleep(2)

        if all_reviews:
            df_reviews = pd.DataFrame(all_reviews)
            os.makedirs(DATA_PATHS['raw'], exist_ok=True)
            df_reviews.to_csv(DATA_PATHS['raw_reviews'], index=False)
            print(f"\nScraping complete! CSV saved to: {DATA_PATHS['raw_reviews']}")
            return df_reviews
        else:
            print("\nNo reviews were collected.")
            return pd.DataFrame()

    def display_sample_reviews(self, df, n=3):
        print("\nSample Reviews:")
        for bank_code in self.bank_names.keys():
            bank_df = df[df['bank_code'] == bank_code]
            if not bank_df.empty:
                print(f"\n{self.bank_names[bank_code]}:")
                for i, row in bank_df.head(n).iterrows():
                    print(f"Rating: {'⭐'*row['rating']}")
                    print(f"Review: {row['review_text'][:200]}...")
                    print(f"Date: {row['review_date']}\n")


def main():
    scraper = PlayStoreScraper()
    df = scraper.scrape_all_banks()
    if not df.empty:
        scraper.display_sample_reviews(df)
    return df


if __name__ == "__main__":
    reviews_df = main()
