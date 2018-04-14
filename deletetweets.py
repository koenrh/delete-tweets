#!/usr/bin/env python

import argparse
import csv
import sys
import time
import twitter
from dateutil.parser import parse

__author__ = "Koen Rouwhorst"
__version__ = "0.1"

API_KEY = ""
API_SECRET = ""

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

def delete(api, date, r):
    with open("tweets.csv") as file:
        count = 0

        for row in csv.DictReader(file):
            tweet_id = int(row["tweet_id"])
            tweet_date = parse(row["timestamp"], ignoretz=True).date()

            if date != "" and tweet_date >= parse(date).date():
                continue

            if (r == "retweet" and row["retweeted_status_id"] == "" or
                    r == "reply" and row["in_reply_to_status_id"] == ""):
                continue

            try:
                print "Deleting tweet #{0} ({1})".format(tweet_id, tweet_date)

                api.DestroyStatus(tweet_id)
                count += 1
                time.sleep(1)

            except twitter.TwitterError, err:
                print "Exception: %s\n" % err.message

    print "Number of deleted tweets: %s\n" % count

def error(msg, ec=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(ec)

def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("-d", dest="date", required=True,
                        help="Delete tweets until this date")
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"],
                        help="Restrict to either replies or retweets")

    args = parser.parse_args()

    if API_KEY == "" or API_SECRET == "":
        error("No API key and/or secret set.")

    if ACCESS_TOKEN == "" or ACCESS_TOKEN_SECRET == "":
        error("No access token and/or secret set.")

    api = twitter.Api(consumer_key=API_KEY,
                      consumer_secret=API_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    delete(api, args.date, args.restrict)


if __name__ == "__main__":
    main()
