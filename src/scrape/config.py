# config.py
"""
Configuration file for Google Play Store Scraper
Contains app IDs, bank names, scraping settings, and file paths.
"""

# Google Play package IDs for each bank app
# TODO: Replace PACKAGE_ID_XXX with actual package IDs from Google Play
APP_IDS = {
    "CBE": "com.combanketh.mobilebanking",       # Example: "com.cbe.mobilebanking"
    "BOA": "com.boa.boaMobileBanking",       # Example: "com.bankofabyssinia.mobile"
    "Dashen": "com.dashen.dashensuperapp"  # Example: "com.dashenbank.app"
}

# Human-readable bank names
BANK_NAMES = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA": "Bank of Abyssinia",
    "Dashen": "Dashen Bank"
}

# Scraping configuration
SCRAPING_CONFIG = {
    "reviews_per_bank": 400,  # minimum 400 reviews per bank
    "lang": "en",             # language of the reviews
    "country": "us",          # store country
    "max_retries": 3          # retry times if scraping fails
}

# Paths to store raw and processed data
DATA_PATHS = {
    "raw": "data/raw",                     # folder for raw CSVs
    "raw_reviews": "data/raw/play_reviews_raw.csv",  # CSV file for all scraped reviews
    "processed_reviews": "data/processed/play_reviews_processed.csv"
}
