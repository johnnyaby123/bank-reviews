# Bank Reviews Analysis

## Task 1: Data Collection & Preprocessing

### Overview
This project collects and preprocesses user reviews from the Google Play Store for three Ethiopian banks.

### Methodology

1. **Data Collection**
   - Scraped at least 400 reviews per bank (minimum 1200 total reviews).
   - Used `google_play_scraper` to fetch reviews including rating, review text, user info, and app metadata.
   - Implemented retry mechanism and polite delays to ensure reliable scraping.

2. **Data Preprocessing**
   - Handled missing values in critical fields (`review_text`, `rating`, `bank_name`).
   - Normalized date formats to `YYYY-MM-DD`.
   - Cleaned review text (removed extra spaces, handled empty reviews).
   - Validated ratings to ensure values are between 1–5.
   - Prepared final dataset and saved as `PlayReviewsProcessed.csv`.

### Output
- Raw review data saved in `data/raw_reviews.csv`.
- Processed and cleaned data saved as `PlayReviewsProcessed.csv`.
