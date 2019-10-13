#!/usr/bin/env python

import argparse
import io
import os
import sys
import time
import json

import twitter
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "1.0.0"


class TweetDestroyer(object):
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api

    def destroy(self, tweet_id):
        try:
            print("delete tweet %s" % tweet_id)
            self.twitter_api.DestroyStatus(tweet_id)
            # NOTE: A poor man's solution to honor Twitter's rate limits.
            time.sleep(0.5)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)


class TweetReader(object):
    def __init__(self, reader, keyword=None, date=None, restrict=None, spare=[], min_likes=0, min_retweets=0):
        self.reader = reader
        if date is not None:
            self.date = parse(date, ignoretz=True).date()
        self.restrict = restrict
        self.spare = spare
        self.min_likes = min_likes
        self.min_retweets = min_retweets
	self.keyword = keyword


    def read(self):
        for row in self.reader:
            if row.get("created_at", "") != "":
                tweet_date = parse(row["created_at"], ignoretz=True).date()
                if self.date != "" and \
                        self.date is not None and \
                        tweet_date >= self.date:
                    continue

            if (self.restrict == "retweet" and
                    not row.get("full_text").startswith("RT @")) or \
                    (self.restrict == "reply" and
                     row.get("in_reply_to_user_id_str") == ""):
                continue

            if row.get("id_str") in self.spare:
                continue

            if (self.min_likes > 0 and int(row.get("favorite_count")) >= self.min_likes) or \
                    (self.min_retweets > 0 and int(row.get("retweet_count")) >= self.min_retweets):
                continue

            if self.keyword is not None:
	        tweet_text = row.get("full_text").encode("utf-8")
	        if (self.keyword in tweet_text.split()):
		   continue	

            yield row


def delete(tweetjs_path, k, date, r, s, min_l, min_r):
    with io.open(tweetjs_path, mode="r", encoding="utf-8") as tweetjs_file:
        count = 0

        api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                          consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                          access_token_key=os.environ["TWITTER_ACCESS_TOKEN"],
                          access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])
        destroyer = TweetDestroyer(api)

        tweets = json.loads(tweetjs_file.read()[25:])
        for row in TweetReader(tweets, k, date, r, s, min_l, min_r).read():
             destroyer.destroy(row["id_str"])
             count += 1

        print("Number of deleted tweets: %s\n" % count)

def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")
    parser.add_argument("file", help="Path to the tweet.js file",
                        type=str)
    parser.add_argument("--spare-ids", dest="spare_ids", help="A list of tweet ids to spare",
                        type=str, nargs="+", default=[])
    parser.add_argument("--spare-min-likes", dest="min_likes",
                        help="Spare tweets with more than the provided likes", type=int)
    parser.add_argument("--spare-min-retweets", dest="min_retweets",
                        help="Spare tweets with more than the provided retweets", type=int)
    parser.add_argument("--keyword", dest="keyword",
                        help="Keyword in tweets to delete")

    args = parser.parse_args()

    if not ("TWITTER_CONSUMER_KEY" in os.environ and
            "TWITTER_CONSUMER_SECRET" in os.environ and
            "TWITTER_ACCESS_TOKEN" in os.environ and
            "TWITTER_ACCESS_TOKEN_SECRET" in os.environ):
        sys.stderr.write("Twitter API credentials not set.")
        exit(1)

    delete(args.file, args.keyword, args.date, args.restrict, args.spare_ids, args.min_likes, args.min_retweets)


if __name__ == "__main__":
    main()
