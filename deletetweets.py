#!/usr/bin/env python

import argparse
import io
import os
import sys
import time

import twitter
from backports import csv
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.1.1"


class TweetDestroyer(object):
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api

    def destroy(self, tweet_id):
        try:
            print("delete tweet %s" % tweet_id)
            time.sleep(0.5)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)


class TweetReader(object):
    def __init__(self, reader, date=None, restrict=None):
        self.reader = reader
        if date is not None:
            self.date = parse(date, ignoretz=True).date()
        self.restrict = restrict

    def __iter__(self):
        return self

    def next(self):
        row = next(self.reader)

        if row.get("timestamp", "") != "":
            tweet_date = parse(row["timestamp"], ignoretz=True).date()
            if self.date != "" and \
                    self.date is not None and \
                    tweet_date >= self.date:
                row = next(self.reader)

        if self.restrict == "retweet" and \
                row.get("retweeted_status_id", "") == "" or \
                self.restrict == "reply" and \
                row.get("retweeted_status_id", "") == "":
            row = next(self.reader)

        return row


def delete(date, r):
    with io.open("tweets.csv", encoding='utf-8') as tweets_file:
        count = 0

        api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                          consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                          access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
                          access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
        destroyer = TweetDestroyer(api)

        for row in TweetReader(csv.DictReader(tweets_file), date, r):
            destroyer.destroy(row["tweet_id"])

        print("Number of deleted tweets: %s\n" % count)


def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")

    args = parser.parse_args()

    if not ("TWITTER_CONSUMER_KEY" in os.environ and
            "TWITTER_CONSUMER_SECRET" in os.environ and
            "TWITTER_ACCESS_TOKEN" in os.environ and
            "TWITTER_ACCESS_TOKEN_SECRET" in os.environ):
        sys.stderr.write("Twitter API credentials not set.")
        exit(1)

    delete(args.date, args.restrict)


if __name__ == "__main__":
    main()
