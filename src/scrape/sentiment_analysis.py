"""
Sentiment and Thematic Analysis Script
Task 2: Sentiment and Thematic Analysis

This script performs sentiment analysis and thematic keyword extraction
on processed Google Play Store reviews.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from config import DATA_PATHS

# --- Sentiment Analysis ---
def compute_sentiment(text):
    """
    Compute sentiment label and polarity score using TextBlob
    Returns: (label, polarity)
    """
    if not text or pd.isna(text):
        return "neutral", 0.0
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return label, polarity

# --- Keyword Extraction ---
def extract_keywords_per_bank(df, top_n=5):
    """
    Extract top keywords per bank using TF-IDF.
    Adds a 'keywords' column with top keywords per bank.
    """
    df['keywords'] = None
    vectorizer = TfidfVectorizer(stop_words='english', max_features=50, ngram_range=(1,2))

    for bank in df['bank_name'].unique():
        bank_df = df[df['bank_name'] == bank]
        tfidf_matrix = vectorizer.fit_transform(bank_df['review_text'])
        feature_names = vectorizer.get_feature_names_out()
        
        # Top N keywords across all reviews for this bank
        sums = tfidf_matrix.sum(axis=0)
        keywords_scores = [(word, sums[0, idx]) for idx, word in enumerate(feature_names)]
        keywords_scores = sorted(keywords_scores, key=lambda x: x[1], reverse=True)
        top_keywords = [kw for kw, score in keywords_scores[:top_n]]
        
        df.loc[df['bank_name'] == bank, 'keywords'] = ', '.join(top_keywords)

    return df

# --- Theme Assignment ---
def assign_themes(df):
    """
    Assign themes based on keywords and simple rules.
    Themes per bank:
    - 'Account Access Issues'
    - 'Transaction Performance'
    - 'User Interface & Experience'
    - 'Customer Support'
    - 'Feature Requests'
    """
    theme_map = {
        'account': 'Account Access Issues',
        'login': 'Account Access Issues',
        'password': 'Account Access Issues',
        'transfer': 'Transaction Performance',
        'payment': 'Transaction Performance',
        'slow': 'Transaction Performance',
        'crash': 'User Interface & Experience',
        'ui': 'User Interface & Experience',
        'interface': 'User Interface & Experience',
        'support': 'Customer Support',
        'help': 'Customer Support',
        'feature': 'Feature Requests',
        'request': 'Feature Requests'
    }

    def map_keywords_to_themes(keywords_str):
        if pd.isna(keywords_str) or keywords_str == '':
            return ''
        keywords = keywords_str.lower().split(', ')
        themes = set()
        for kw in keywords:
            for k, t in theme_map.items():
                if k in kw:
                    themes.add(t)
        return ', '.join(sorted(themes))

    df['identified_theme'] = df['keywords'].apply(map_keywords_to_themes)
    return df

# --- Main Execution ---
def main():
    print("="*60)
    print("STARTING SENTIMENT AND THEMATIC ANALYSIS")
    print("="*60)

    # Load processed reviews
    try:
        df = pd.read_csv(DATA_PATHS['processed_reviews'])
        print(f"Loaded {len(df)} reviews from {DATA_PATHS['processed_reviews']}")
    except FileNotFoundError:
        print(f"ERROR: File not found: {DATA_PATHS['processed_reviews']}")
        return
    except Exception as e:
        print(f"ERROR loading CSV: {str(e)}")
        return

    # Compute sentiment
    print("\n[1/3] Computing sentiment...")
    sentiment_results = df['review_text'].apply(compute_sentiment)
    df['sentiment_label'] = sentiment_results.apply(lambda x: x[0])
    df['sentiment_score'] = sentiment_results.apply(lambda x: x[1])
    print("Sentiment analysis completed.")

    # Extract keywords
    print("\n[2/3] Extracting keywords per bank...")
    df = extract_keywords_per_bank(df, top_n=5)
    print("Keyword extraction completed.")

    # Assign themes
    print("\n[3/3] Assigning identified themes...")
    df = assign_themes(df)
    print("Thematic assignment completed.")

    # Save results
    os.makedirs(os.path.dirname(DATA_PATHS['sentiment_analysis']), exist_ok=True)
    df.to_csv(DATA_PATHS['sentiment_analysis'], index=False)
    print(f"\nFinal CSV saved: {DATA_PATHS['sentiment_analysis']}")
    print(f"Total reviews analyzed: {len(df)}")
    print("="*60)

if __name__ == "__main__":
    main()
