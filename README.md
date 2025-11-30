# Bank Reviews Analysis

## Task 1: Data Collection & Preprocessing

### Overview
The goal of Task 1 is to collect and preprocess user reviews from the Google Play Store for three Ethiopian banks. The target was to scrape **at least 400 reviews per bank** (minimum 1200 reviews total) and prepare clean data for further analysis.

---

### Step-by-Step Methodology

#### 1. Setup & Environment
1. Created a virtual environment to isolate dependencies:
    ```bash
    python -m venv venv
    ```
2. Activated the environment:
    ```bash
    # Windows
    venv\Scripts\activate

    # Linux/Mac
    source venv/bin/activate
    ```
3. Installed required packages:
    ```bash
    pip install -r requirements.txt
    ```

#### 2. Scraper Implementation
1. Created `scraper.py` under `src/scrape/`.
2. Configured app IDs, bank names, and scraping parameters in `config.py`.
3. Scraper used `google_play_scraper` library to:
    - Fetch reviews, ratings, thumbs up, and review dates.
    - Handle retries for network/API failures.
    - Collect reviews **sorted by newest first**.
4. Saved raw scraped data to:
    ```
    data/raw/app_info.csv
    data/raw/raw_reviews.csv
    ```
5. Sample of command to run scraper:
    ```bash
    python src/scrape/scraper.py
    ```

#### 3. Preprocessing
1. Created `preprocessing.py` under `src/scrape/`.
2. Preprocessing pipeline included:
    - Handling missing values in critical fields (`review_text`, `rating`, `bank_name`).
    - Filling missing optional fields (`user_name` → "Anonymous", `thumbs_up` → 0, `reply_content` → empty string).
    - Normalizing dates to `YYYY-MM-DD`.
    - Cleaning review text (removing extra whitespace, dropping empty reviews).
    - Validating ratings to ensure all are 1–5.
    - Adding new features:
        - `review_year` and `review_month` extracted from `review_date`.
        - `text_length` representing the number of characters in the review text.
3. Final processed data saved to:
    ```
    data/processed/PlayReviewsProcessed.csv
    ```
4. Sample command to run preprocessing:
    ```bash
    python src/scrape/preprocessing.py
    ```

#### 4. GitHub & Version Control
1. Created `task-1` branch for all Task 1 work:
    ```bash
    git checkout -b task-1
    ```
2. Staged and committed essential files:
    ```bash
    git add src/scrape/scraper.py
    git add src/scrape/preprocessing.py
    git add src/scrape/config.py
    git commit -m "Task 1: Add scraper, preprocessing, and config files"
    ```
3. Pushed Task 1 branch to GitHub:
    ```bash
    git push -u origin task-1
    ```
4. Updated README with methodology (this file).

---

### Summary of Outputs
- **Raw Data**: `data/raw/raw_reviews.csv`  
- **Processed Data**: `data/processed/PlayReviewsProcessed.csv`  
- **Code Files**: `scraper.py`, `preprocessing.py`, `config.py`  

---

> ✅ Task 1 Complete: Minimum essentials achieved.
