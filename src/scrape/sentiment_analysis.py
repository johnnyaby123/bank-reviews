"""
Sentiment & Thematic Analysis
Task 2: Analyze bank reviews for sentiment and themes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from config import DATA_PATHS

class SentimentThematicAnalyzer:
    """Class to perform sentiment and thematic analysis on bank reviews"""

    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['processed_reviews']
        self.output_path = output_path or DATA_PATHS['sentiment_analysis']
        self.df = None
        self.themes_keywords = {
            "Account & Login Issues": ["login", "password", "account", "otp", "verification"],
            "Transaction & Performance": ["transfer", "payment", "slow", "failed", "transaction"],
            "UI/UX & Experience": ["ui", "interface", "experience", "navigation", "easy", "design"],
            "Customer Support": ["support", "customer service", "help", "response", "call"],
            "Feature Requests": ["feature", "option", "add", "request", "improve"]
        }

    def load_data(self):
        """Load processed reviews"""
        print("Loading processed reviews...")
        self.df = pd.read_csv(self.input_path)
        print(f"Loaded {len(self.df)} reviews.")

    def analyze_sentiment(self):
        """Compute sentiment using TextBlob"""
        print("\nPerforming sentiment analysis...")
        def get_sentiment(text):
            polarity = TextBlob(str(text)).sentiment.polarity
            if polarity > 0.1:
                return "Positive", polarity
            elif polarity < -0.1:
                return "Negative", polarity
            else:
                return "Neutral", polarity

        self.df[['sentiment_label', 'sentiment_score']] = self.df['review_text'].apply(lambda x: pd.Series(get_sentiment(x)))
        print("Sentiment analysis complete.")

    def assign_themes(self):
        """Assign themes based on keywords"""
        print("\nAssigning themes...")
        def find_theme(text):
            text_lower = str(text).lower()
            assigned = []
            for theme, keywords in self.themes_keywords.items():
                if any(keyword in text_lower for keyword in keywords):
                    assigned.append(theme)
            if not assigned:
                assigned.append("Other")
            return ", ".join(assigned)

        self.df['identified_theme'] = self.df['review_text'].apply(find_theme)
        print("Themes assigned.")

    def save_results(self):
        """Save final CSV"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.df.to_csv(self.output_path, index=False)
        print(f"\nResults saved to {self.output_path}")

    def run_pipeline(self):
        """Run the complete sentiment and thematic analysis pipeline"""
        self.load_data()
        self.analyze_sentiment()
        self.assign_themes()
        self.save_results()
        print("\n✓ Sentiment & thematic analysis complete!")

def main():
    analyzer = SentimentThematicAnalyzer()
    analyzer.run_pipeline()
    return analyzer.df

if __name__ == "__main__":
    df_result = main()
