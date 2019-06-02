import argparse
import time
import tweepy

from datetime import datetime
from elasticsearch import Elasticsearch

import keys


es = Elasticsearch()


parser = argparse.ArgumentParser(description='Elasticsearch eats tweets for breakfast!')
parser.add_argument('--handle', help='Twitter handle', required=True)

args = parser.parse_args()


def _ts():
    return datetime.now().strftime('%Y%m%d %H:%M:%S UTC')


auth = tweepy.OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

page = 0
fetch_intervals = 90
reset_pause = 60*60*1

if fetch_intervals < 90:
    fetch_intervals = 90

if reset_pause < 90:
    reset_pause = 90

while True:
    tweets = api.user_timeline(args.handle, page=page)

    for tweet in tweets:
        json = tweet._json

        id = json.pop('id', -1)
        json['created_at'] = datetime.strptime(json['created_at'], '%a %b %d %H:%M:%S +0000 %Y').isoformat()
        json['user']['created_at'] = datetime.strptime(json['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y').isoformat()
        del json['user']['id']

        res = es.index(index=f"tweets-{args.handle.lower()}", doc_type="tweet", id=id, body=json)
        res = res['result']
        print(f"{_ts()} id={id} {res}")

        if res == 'created':
            page += 1
            time.sleep(fetch_intervals)
        elif res == 'updated':
            print(f"{_ts()} reset")
            page = 0
            time.sleep(reset_pause)
