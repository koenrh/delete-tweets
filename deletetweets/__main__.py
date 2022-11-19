#!/usr/bin/env python

import argparse
import os
import sys

from deletetweets import deletetweets

__author__ = "Koen Rouwhorst"
__version__ = "1.0.6"


def main():
    parser = argparse.ArgumentParser(description="Delete old tweets.")
    parser.add_argument("--since", dest="since_date", help="Delete tweets since this date")
    parser.add_argument("--until", dest="until_date", help="Delete tweets until this date")
    parser.add_argument("--filter", action="append", dest="filters", choices=["replies", "retweets"],
                        help="Filter replies or retweets", default=[])
    parser.add_argument("file", help="Path to the tweet.js file",
                        type=str)
    parser.add_argument("--spare-ids", dest="spare_ids", help="A list of tweet ids to spare",
                        type=str, nargs="+", default=[])
    parser.add_argument("--spare-min-likes", dest="min_likes",
                        help="Spare tweets with more than the provided likes", type=int, default=0)
    parser.add_argument("--spare-min-retweets", dest="min_retweets",
                        help="Spare tweets with more than the provided retweets", type=int, default=0)
    parser.add_argument("--spare-replies", dest="spare_replies",
                        help="Spare tweets that are replies to others", type=int, default=0)
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", default=False)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    # legacy options
    parser.add_argument("-d", dest="until_date", help=argparse.SUPPRESS)
    parser.add_argument("-r", dest="restrict", choices=["reply", "retweet"], help=argparse.SUPPRESS)

    args = parser.parse_args()

    if not ("TWITTER_CONSUMER_KEY" in os.environ and
            "TWITTER_CONSUMER_SECRET" in os.environ and
            "TWITTER_ACCESS_TOKEN" in os.environ and
            "TWITTER_ACCESS_TOKEN_SECRET" in os.environ):
        sys.stderr.write("Twitter API credentials not set.\n")
        exit(1)

    filters = []

    if args.restrict == "reply":
        filters.append("replies")
    elif args.restrict == "retweet":
        filters.append("retweets")

    for f in args.filters:
        if f not in filters:
            filters.append(f)

    deletetweets.delete(args.file, args.since_date, args.until_date, filters, args.spare_ids,
                        args.min_likes, args.min_retweets, args.dry_run)


if __name__ == "__main__":
    main()
