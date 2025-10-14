import tweepy
import os

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LAUNCH_DATE = datetime(2024, 10, 14)
JUPITER_ARRIVAL = datetime(2030, 4, 11)

API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

def calculate_mission_metrics():
    now = datetime.utcnow()
    total_days = (JUPITER_ARRIVAL - LAUNCH_DATE).days
    days_since = max(0, (now - LAUNCH_DATE).days)
    progress_pct = min(100, (days_since / total_days) * 100)
    return progress_pct

def create_progress_bar(percentage, length=20):
    filled = int(length * percentage / 100)
    empty = length - filled
    return "▓" * filled + "▒" * empty

def create_tweet():
    progress = calculate_mission_metrics()
    bar = create_progress_bar(progress)
    tweet = f"{bar} {progress:.2f}%".rstrip('0').rstrip('.')
    return tweet

def post_tweet(tweet_text):
    try:
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET_KEY,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        response = client.create_tweet(text=tweet_text)
        print(f"Tweet posted successfully: {response.data['id']}")
    except Exception as e:
        print(f"Error posting tweet: {e}")

def main():
    tweet = create_tweet()

if __name__ == "__main__":
    main()
