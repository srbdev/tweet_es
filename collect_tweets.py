import argparse
import time
import tweepy
import json
from datetime import datetime

import keys


parser = argparse.ArgumentParser(description="collects tweets for the farm!")
parser.add_argument("--handle", help="Twitter handle", required=True)

args = parser.parse_args()


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d %H:%M:%S UTC")


auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

page = 0
fetch_intervals = 90
reset_pause = 60 * 60 * 1

if fetch_intervals < 90:
    fetch_intervals = 90

if reset_pause < 90:
    reset_pause = 90

while True:
    tweets = api.user_timeline(args.handle, page=page)

    for tweet in tweets:
        id = tweet._json["id"]

        with open(f"{id}.json", "w", encoding="utf-8") as file:
            json.dump(tweet._json, file, ensure_ascii=False, indent=4)

        res = "created"
        print(f"{generate_timestamp()} id={id} {res}")

        if res == "created":
            page += 1
            time.sleep(fetch_intervals)
        elif res == "updated":
            print(f"{generate_timestamp()} reset")
            page = 0
            time.sleep(reset_pause)
