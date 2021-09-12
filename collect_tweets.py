import argparse
import time
import tweepy
import json
from datetime import datetime
import os

from tweepy.error import RateLimitError

import keys
import config


parser = argparse.ArgumentParser(description="Collects tweets for the farm!")
parser.add_argument("--handle", help="Twitter handle", required=True)

args = parser.parse_args()


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d %H:%M:%S UTC")


print("+ Starting the harvest...")

auth = tweepy.AppAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
print("+ Authenticated with Twitter!")

if not os.path.isdir(config.FARM_PATH):
    os.mkdir(config.FARM_PATH)
    print("+ Created the farm!")

handle_path = os.path.join(config.FARM_PATH, args.handle)
if not os.path.isdir(handle_path):
    os.mkdir(handle_path)
    print(f"+ Created space for handle={args.handle}")
records_path = os.path.join(handle_path, "records.csv")
page_path = os.path.join(handle_path, ".page")

if os.path.isfile(page_path):
    with open(page_path, "r") as f:
        page = int(f.read())
else:
    page = 0
    with open(page_path, "w") as f:
        f.write(str(page))


fetch_intervals = 60 * 1.5
reset_pause = 60 * 60 * 1
rate_limit_pause = 60 * 60 * 1

while True:
    try:
        tweets = api.user_timeline(args.handle, page=page)
    except RateLimitError as e:
        print(f"- Rate limit exceeded, pausing for {rate_limit_pause}s")
        time.sleep(rate_limit_pause)
        continue

    for tweet in tweets:
        id = tweet._json["id"]

        json_dump = os.path.join(handle_path, f"{id}.json")
        if os.path.isfile(json_dump):
            res = "updated"
        else:
            res = "created"

        try:
            with open(json_dump, "w", encoding="utf-8") as f:
                json.dump(tweet._json, f, ensure_ascii=False, indent=4)
        except:
            res = "error"
            print(f"- {generate_timestamp()},{res},{id}")
            continue

        print(f"+ {generate_timestamp()},{res},{id}")
        with open(records_path, "a") as f:
            f.write(f"{generate_timestamp()},{res},{id}\n")

        if res == "created":
            page += 1
            with open(page_path, "w") as f:
                f.write(str(page))
            time.sleep(fetch_intervals)
        elif res == "updated":
            print(f"+ {generate_timestamp()},reset")
            page = 0
            with open(page_path, "w") as f:
                f.write(str(page))
            time.sleep(reset_pause)
