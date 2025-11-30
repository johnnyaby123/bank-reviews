# src/scrape/scraper.py
"""
Task-1: Scrape Google Play Store reviews for three Ethiopian banks
Saves CSV to data/raw/play_reviews_raw.csv
"""

import os
import csv
import time
from google_play_scraper import reviews_all
from datetime import datetime

os.makedirs("data/raw", exist_ok=True)

# --- REPLACE these with actual Play Store package ids ---
APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp"
}
# ----------------------------------------------------------

OUT_FILE = "data/raw/play_reviews_raw.csv"
FIELDS = ["review_id", "review", "rating", "date", "bank", "source"]

def save_rows(rows, filename):
    write_header = not os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        for r in rows:
            writer.writerow(r)

def fetch_reviews(pkg_id, bank_name):
    print(f"Fetching reviews for {bank_name} ({pkg_id}) ...")
    raw = reviews_all(
        pkg_id,
        sleep_milliseconds=0,  # pause between requests
        lang='en',
        country='us'
    )
    rows = []
    for r in raw:
        rid = r.get("reviewId") or ""
        content = r.get("content") or ""
        score = r.get("score") or None
        date_obj = r.get("at")
        date = date_obj.strftime("%Y-%m-%d") if date_obj else ""
        rows.append({
            "review_id": rid,
            "review": content,
            "rating": score,
            "date": date,
            "bank": bank_name,
            "source": "Google Play"
        })
    return rows

def main():
    for bank, pkg in APPS.items():
        if "PACKAGE_ID" in pkg:
            print(f"ERROR: Replace PACKAGE_ID for {bank} with actual Play Store package id")
            return

    # clear CSV if exists
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    for bank, pkg in APPS.items():
        rows = fetch_reviews(pkg, bank)
        print(f"Fetched {len(rows)} reviews for {bank}")
        save_rows(rows, OUT_FILE)
        time.sleep(2)

    print(f"All done. CSV saved to {OUT_FILE}")

if __name__ == "__main__":
    main()
