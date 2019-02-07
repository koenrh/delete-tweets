#!/usr/bin/env python

import argparse
import io
import json
import os
import os.path
import sys
import time

import twitter
from dateutil.parser import parse

if sys.version_info.major < 3:
    from backports import csv
else:
    import csv

__author__ = "Koen Rouwhorst"
__version__ = "0.1.1"


class TweetDestroyer(object):
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api

    def destroy(self, tweet_id):
        try:
            print("delete tweet %s" % tweet_id)
            self.twitter_api.DestroyStatus(tweet_id)
            time.sleep(0.5)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)


class TweetReader(object):
    def __init__(self, reader, date=None, restrict=None):
        self.reader = reader
        if date is not None:
            self.date = parse(date, ignoretz=True).date()
        self.restrict = restrict

    def read(self):
        for row in self.reader:
            if row.get("timestamp", "") != "":
                tweet_date = parse(row["timestamp"], ignoretz=True).date()
                if self.date != "" and \
                        self.date is not None and \
                        tweet_date >= self.date:
                    continue

            if (self.restrict == "retweet" and
                    row.get("retweeted_status_id") == "") or \
                    (self.restrict == "reply" and
                     row.get("in_reply_to_status_id") == ""):
                continue

            yield row


def delete(csv_file, date, r, api_keys):
    with io.open(csv_file, encoding='utf-8') as tweets_file:
        count = 0

        api = twitter.Api(consumer_key=api_keys["consumer_key"],
                          consumer_secret=api_keys["consumer_secret"],
                          access_token_key=api_keys["access_token"],
                          access_token_secret=api_keys["access_token_secret"])
        destroyer = TweetDestroyer(api)

        for row in TweetReader(csv.DictReader(tweets_file), date, r).read():
            destroyer.destroy(row["tweet_id"])
            count += 1

        print("Number of deleted tweets: %s\n" % count)


def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")
    parser.add_argument("-k", dest="api_keys",
                        help="API keys in a JSON file")
    parser.add_argument("file", help="display a square of a given number",
                        type=str)

    args = parser.parse_args()

    api_keys = {}
    if args.api_keys and os.path.isfile(args.api_keys):
        with open(args.api_keys, "rb") as f:
            api_keys = json.load(f)
    else:
        api_keys["consumer_key"] = os.environ.get("TWITTER_CONSUMER_KEY")
        api_keys["consumer_secret"] = os.environ.get("TWITTER_CONSUMER_SECRET")
        api_keys["access_token"] = os.environ.get("TWITTER_ACCESS_TOKEN")
        api_keys["access_token_secret"] = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
    if not (api_keys["consumer_key"] and api_keys["consumer_secret"] and
            api_keys["access_token"] and api_keys["access_token_secret"]):
        sys.stderr.write("Twitter API credentials not set.\n")
        exit(1)

    delete(args.file, args.date, args.restrict, api_keys)


if __name__ == "__main__":
    main()
