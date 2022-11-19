# delete-tweets

![](https://github.com/koenrh/delete-tweets/workflows/build/badge.svg)
[![PyPI version](https://badge.fury.io/py/delete-tweets.svg)](https://badge.fury.io/py/delete-tweets)

This is a simple script that helps you delete tweets (or just replies or retweets)
from your timeline. There are quite a few third-party services that allow you
to delete tweets, but these very likely will not allow you to delete tweets beyond
the infamous [3,200 tweet limit](https://web.archive.org/web/20131019125213/https://dev.twitter.com/discussions/276).

This is a fork of the original that adds the printing of the tweets contents, likes, and RTs. This helps with identifying content on a dry-run, or as it is being deleted.

## Prerequisites

You are required to have a Twitter Developer account in order to create a Twitter app.

### Apply for a Twitter Developer account

1. [Create a Twitter Developer account](https://developer.twitter.com/en/apply):
    1. **User profile**: Use your current Twitter @username.
    1. **Account details**: Select *I am requesting access for my own personal use*,
      set your 'Account name' to your @username, and select your 'Primary country
      of operation.
    1. **Use case details**: select 'Other', and explain in at least 300 words that
      you want to create an app to semi-automatically clean up your own tweets.
    1. **Terms of service**: Read and accept the terms.
    1. **Email verification**: Confirm your email address.
1. Now wait for your Twitter Developer account to be reviewed and approved.

### Create a Twitter app

1. [Create a new Twitter app](https://developer.twitter.com/en/apps/create) (not
  available as long as your Twitter Developer account is pending review).
1. Set 'Access permissions' of your app to *Read and write*.

### Configure your environment

1. Open your Twitter Developer's [apps](https://developer.twitter.com/en/apps).
1. Click the 'Details' button next to your newly created app.
1. Click the 'Keys and tokens' tab, and find your keys, secret keys and access tokens.
1. Now you need to make these keys and tokens available to your shell environment.
  Assuming you are using [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)):

:warning: Before you continue, you should be aware that most shells record user
input (and thus secrets) into a history file. In Bash you could prevent this by
prepending your command with a _single space_ (requires `$HISTCONTROL` to be set
to `ignorespace` or `ignoreboth`).

```bash
export TWITTER_CONSUMER_KEY="your_consumer_key"
export TWITTER_CONSUMER_SECRET="your_consumer_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

### Get your tweet archive

1. Open the [Your Twitter data page](https://twitter.com/settings/your_twitter_data)
1. Scroll to the 'Download your Twitter data' section at the bottom of the page
1. Re-enter your password
1. Click 'Request data', and wait for the email to arrive
1. Follow the link in the email to download your Tweet data
1. Unpack the archive

## Getting started

### Installation

Clone the repo then install it by:

```
python3 setup.py install
```



### Usage

Delete any tweet from _before_ January 1, 2018:

```
delete-tweets --until 2018-01-01 tweet.js
```

Or only delete all retweets:

```
delete-tweets --filter retweets tweet.js
```

How I run it to delete old tweets with no engagement. This removes tweets that have no likes, no RTs, and are not replies to anyone else. Run with --dry-run first.

```delete-tweets --spare-min-likes 1 --spare-min-retweets 1 -r reply tweets.js```

### Spare tweets

You can optionally spare tweets by passing their `id_str`, setting a minimum
amount of likes or retweets:

```
delete-tweets --until 2018-01-01 tweet.js --spare-ids 21235434 23498723 23498723
```

Spare tweets that have at least 10 likes, or 5 retweets:

```
delete-tweets --until 2018-01-01 tweet.js --spare-min-likes 10 --spare-min-retweets 5
```
