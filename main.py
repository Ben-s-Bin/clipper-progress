import tweepy
import requests

from datetime import datetime, timezone
from dotenv import dotenv_values
from math import sqrt

env = dotenv_values(".env")

API_KEY = env.get("API_KEY")
API_SECRET_KEY = env.get("API_SECRET_KEY")
ACCESS_TOKEN = env.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = env.get("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = env.get("BEARER_TOKEN")

CLIPPER_ID = "2024-182A"
JUPITER_ID = "599"
CENTER = "500@10"
STEP_SIZE = "1d"
LAUNCH_DATE = "2024-10-14"

def fetch_horizons_data(body_id, epoch):
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    params = {
        "format": "json",
        "COMMAND": body_id,
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": CENTER,
        "START_TIME": epoch,
        "STOP_TIME": epoch,
        "STEP_SIZE": STEP_SIZE,
        "VEC_TABLE": 2
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    result = resp.json().get("result", "")
    lines = result.splitlines()
    try:
        start_idx = lines.index("$$SOE")
        data_line = lines[start_idx + 1].split()
        x, y, z = map(float, data_line[2:5])
        return x, y, z
    except Exception as e:
        print(f"Error parsing HORIZONS data: {e}")
        return None

def calculate_progress():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    clipper_vec = fetch_horizons_data(CLIPPER_ID, now)
    jupiter_vec = fetch_horizons_data(JUPITER_ID, now)
    launch_vec = fetch_horizons_data(CLIPPER_ID, LAUNCH_DATE)

    if not all([clipper_vec, jupiter_vec, launch_vec]):
        return 0.0
    
    dx = clipper_vec[0] - jupiter_vec[0]
    dy = clipper_vec[1] - jupiter_vec[1]
    dz = clipper_vec[2] - jupiter_vec[2]
    current_distance = sqrt(dx**2 + dy**2 + dz**2)

    dx0 = launch_vec[0] - jupiter_vec[0]
    dy0 = launch_vec[1] - jupiter_vec[1]
    dz0 = launch_vec[2] - jupiter_vec[2]
    total_distance = sqrt(dx0**2 + dy0**2 + dz0**2)

    progress_pct = max(0.0, min(100.0, 100 * (total_distance - current_distance) / total_distance))
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
