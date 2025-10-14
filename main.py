import tweepy

from dotenv import dotenv_values
from datetime import datetime, timezone

env = dotenv_values(".env")

API_KEY = env.get("API_KEY")
API_SECRET_KEY = env.get("API_SECRET_KEY")
ACCESS_TOKEN = env.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = env.get("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = env.get("BEARER_TOKEN")

LAUNCH_DATE = datetime(2024, 10, 14, tzinfo=timezone.utc)
JUPITER_ARRIVAL = datetime(2030, 4, 11, tzinfo=timezone.utc)

def calculate_progress():
    now = datetime.now(timezone.utc)
    total_days = (JUPITER_ARRIVAL - LAUNCH_DATE).days
    elapsed_days = max(0, (now - LAUNCH_DATE).days)
    progress_pct = min(100, (elapsed_days / total_days) * 100)
    return progress_pct

def create_progress_bar(percentage, length=20):
    filled = int(length * percentage / 100)
    empty = length - filled
    return "▓" * filled + "▒" * empty

def create_tweet():
    progress = calculate_progress()
    bar = create_progress_bar(progress)
    return f"{bar} {progress:.2f}%".rstrip("0").rstrip(".")

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
    post_tweet(tweet)

if __name__ == "__main__":
    main()
