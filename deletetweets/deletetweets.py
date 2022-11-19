import io
import os
import sys
import json

import twitter
from datetime import datetime
from dateutil import parser


class TweetDestroyer(object):
    def __init__(self, twitter_api, dry_run=False):
        self.twitter_api = twitter_api
        self.dry_run = dry_run

    def destroy(self, tweet_id):
        try:
            if not self.dry_run:
                self.twitter_api.DestroyStatus(tweet_id)
        except twitter.TwitterError as err:
            e = err.args[0]
            if ('code' in e[0].keys()) and (e[0]['code'] in [34, 144]):
                print('[*] Tweet does not exist')
            else:
                print("Unknown Exception: %s\n" % err.message)


class TweetReader(object):
    def __init__(self, reader, since_date=None, until_date=None, filters=[], spare=[], min_likes=0, min_retweets=0):
        self.reader = reader
        self.since_date = datetime.min if since_date is None else parser.parse(since_date, ignoretz=True)
        self.until_date = datetime.now() if until_date is None else parser.parse(until_date, ignoretz=True)
        self.filters = filters
        self.spare = spare
        self.min_likes = 0 if min_likes is None else min_likes
        self.min_retweets = 0 if min_retweets is None else min_retweets

    def read(self):
        for row in self.reader:
            if row["tweet"].get("created_at", "") != "":
                tweet_date = parser.parse(row["tweet"]["created_at"], ignoretz=True)
                if tweet_date >= self.until_date or tweet_date <= self.since_date:
                    continue

            if ("retweets" in self.filters and
                    not row["tweet"].get("full_text").startswith("RT @")) or \
                    ("replies" in self.filters and
                     row["tweet"].get("in_reply_to_user_id_str") == ""):
                continue

            if row["tweet"].get("id_str") in self.spare:
                continue

            if (self.min_likes > 0 and int(row["tweet"].get("favorite_count")) >= self.min_likes) or \
                    (self.min_retweets > 0 and int(row["tweet"].get("retweet_count")) >= self.min_retweets):
                continue

            yield row


def delete(tweetjs_path, since_date, until_date, filters, s, min_l, min_r, dry_run=False):
    with io.open(tweetjs_path, mode="r", encoding="utf-8") as tweetjs_file:
        count = 0

        api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                          consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                          access_token_key=os.environ["TWITTER_ACCESS_TOKEN"],
                          access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
                          sleep_on_rate_limit=True)
        destroyer = TweetDestroyer(api, dry_run)

        tweets = json.loads(tweetjs_file.read()[25:])
        for row in TweetReader(tweets, since_date, until_date, filters, s, min_l, min_r).read():
            print('Delete [{} - (L:{} RT:{})] - {}'.format(row["tweet"]["id_str"], row["tweet"]["favorite_count"], row["tweet"]["retweet_count"], row["tweet"]["full_text"]))
            destroyer.destroy(row["tweet"]["id_str"])
                
            count += 1

        print("Number of deleted tweets: %s\n" % count)

    sys.exit()
