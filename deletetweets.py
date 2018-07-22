#!/usr/bin/env python

import argparse
import json
import sys
import time
import os
import twitter
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.2"

def delete(api, date, r):
    with open('tweet.js') as file:
        js, jsonData = file.read().split(' = ')
        data = json.loads(jsonData)
        count = 0

        for line in data:
            tweet_id = int(line["id_str"])
            tweet_date = parse(line["created_at"], ignoretz=True).date()

            if date != "" and tweet_date >= parse(date).date():
                continue

            if (r == "retweet" and line["retweeted_status_id_str"] == "" or
                    r == "reply" and line["in_reply_to_status_id_str"] == ""):
                continue

            try:
                print("Deleting tweet ", tweet_id, tweet_date)

                api.DestroyStatus(tweet_id)
                count += 1
                time.sleep(0.5)

            except twitter.error.TwitterError as err:
                print(err.message)
                for i in err.message:
                    print(i)

    print("Number of deleted tweets: %s\n" % count)

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

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
        error("No consumer key/secret and/or access token/secret set.")

    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                      consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                      access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
                      access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    delete(api, args.date, args.restrict)


if __name__ == "__main__":
    main()
