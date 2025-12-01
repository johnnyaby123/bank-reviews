# 📊 Bank Reviews Analysis Project

This project scrapes, preprocesses, analyzes, and categorizes user reviews from Google Play Store for selected Ethiopian bank mobile apps.

---

# 🚀 Task 1: Data Collection & Preprocessing

## Overview
Task 1 focuses on collecting at least 400 reviews per bank (minimum 1200 reviews total) and creating a clean processed dataset for analysis.

---

## 1. Environment Setup

Create a virtual environment:
```bash
python -m venv venv
Activate the environment:

bash
Copy code
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
Install project requirements:

bash
Copy code
pip install -r requirements.txt
2. Scraper Development
Scraper files:

bash
Copy code
src/scrape/scraper.py
src/scrape/config.py
What the scraper does:
Uses google_play_scraper to collect:

Review text

Rating

User name

Thumbs up count

Review date

Handles retries

Scrapes 3 different banks

Saves raw outputs to:

bash
Copy code
data/raw/app_info.csv
data/raw/play_reviews_raw.csv
Run scraper:
bash
Copy code
python src/scrape/scraper.py
3. Preprocessing Pipeline
Preprocessing script:

bash
Copy code
src/scrape/preprocessing.py
Preprocessing steps
Loads:

bash
Copy code
data/raw/play_reviews_raw.csv
Cleans and formats data:

Removes missing/empty text

Normalizes dates to YYYY-MM-DD

Ensures rating is 1–5

Fills missing optional values

Adds new engineered features:

review_year

review_month

text_length

Output file:
bash
Copy code
data/processed/play_reviews_processed.csv
Run preprocessing:
bash
Copy code
python src/scrape/preprocessing.py
4. Git Workflow for Task 1
Create branch:

bash
Copy code
git checkout -b task-1
Stage required files:

bash
Copy code
git add src/scrape/scraper.py
git add src/scrape/preprocessing.py
git add src/scrape/config.py
git add data/processed/play_reviews_processed.csv
Commit:

bash
Copy code
git commit -m "Task 1: Add scraper, preprocessing, and config files"
Push branch:

bash
Copy code
git push -u origin task-1
Create Pull Request → merge to main.

🔍 Task 2: Sentiment & Thematic Analysis
Overview
Task 2 adds sentiment scoring, keyword extraction, and theme assignment to reveal user satisfaction drivers and pain points.

1. Sentiment Analysis Script
Script location:

bash
Copy code
src/scrape/sentiment_analysis.py
Config updated:

arduino
Copy code
src/scrape/config.py
Input file:
bash
Copy code
data/processed/play_reviews_processed.csv
Output file:
bash
Copy code
data/analysis/play_reviews_sentiment.csv
What the script does
Computes sentiment polarity using TextBlob.

Generates sentiment labels (positive / neutral / negative).

Extracts TF-IDF keywords per bank.

Assigns themes based on keyword rules.

Saves results into final sentiment CSV.

Run sentiment analysis:
bash
Copy code
python src/scrape/sentiment_analysis.py
2. Keyword Extraction
Method:

Runs TF-IDF vectorizer grouped by bank

Extracts top N significant keywords

Writes them to keywords column in the output CSV

3. Theme Assignment
Themes are based on keyword pattern logic:

Theme	Example Keywords
Account Access Issues	login, password, otp, account
Transaction Performance	transfer, fail, slow, payment
UI/UX Experience	ui, design, interface
Customer Support	support, help, response
Feature Requests	add, feature, improve

Column added:

nginx
Copy code
identified_theme
4. Git Workflow for Task 2
Create branch:

bash
Copy code
git checkout -b task-2
Stage Task 2 files:

bash
Copy code
git add src/scrape/sentiment_analysis.py
git add src/scrape/config.py
git add data/analysis/play_reviews_sentiment.csv
Commit:

bash
Copy code
git commit -m "Task 2: Sentiment analysis, keyword extraction, theme assignment"
Push:

bash
Copy code
git push -u origin task-2
Create Pull Request → Merge to main.

📁 Final Project Structure
arduino
Copy code
bank-reviews/
├─ src/
│  └─ scrape/
│     ├─ scraper.py
│     ├─ preprocessing.py
│     ├─ sentiment_analysis.py
│     └─ config.py
├─ data/
│  ├─ raw/
│  │  ├─ app_info.csv
│  │  └─ play_reviews_raw.csv
│  ├─ processed/
│  │  └─ play_reviews_processed.csv
│  └─ analysis/
│     └─ play_reviews_sentiment.csv
├─ requirements.txt
├─ venv/
└─ README.md
✅ Task Completion Summary
✔ Task 1 Completed
Scraped raw reviews

Preprocessed dataset

Generated clean CSV

✔ Task 2 Completed
Sentiment analysis pipeline

Keyword extraction

Thematic mapping

Final analysis CSV created

Branch pushed & ready for PR