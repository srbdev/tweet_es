# Welcome to the Twitter Farm!

This is a Python script meant to run in the background to collect tweets from a given handle. It requires a Twitter developer account for the consumer and access tokens and secrets. Check out the following [link](https://developer.twitter.com/en) for more information.

## Getting Started

Before getting started, you'll need to create the following two files:

```python
# keys.py

CONSUMER_KEY="abcdef"
CONSUMER_SECRET="qwerty"

ACCESS_TOKEN="asdf"
ACCESS_TOKEN_SECRET="foobar"
```

```python
# config.py

FARM_PATH="/a/b/c"
```

`FARM_PATH` is where the raw data will be stored when collecting the tweets.

### Next Step

```bash
pip install -r requirements.txt
```

## Harvest Tweets

```bash
usage: collect_tweets.py [-h] --handle HANDLE

Collects tweets for the farm!

optional arguments:
  -h, --help       show this help message and exit
  --handle HANDLE  Twitter handle
```

```bash
python collect_tweets.py --handle POTUS
```

_Note: the handle doesn't need the `@` character in front of it._
