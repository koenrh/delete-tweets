# Delete tweets

[![Build Status](https://travis-ci.com/koenrh/delete-tweets.svg?branch=master)](https://travis-ci.com/koenrh/delete-tweets)

This is a simple script that helps you delete tweets (or just replies or retweets)
from your timeline. There are quite a few third-party services that allow you
to delete tweets, but these very likely will not allow you to delete tweets beyond
the infamous [3,200 tweet limit](https://web.archive.org/web/20131019125213/https://dev.twitter.com/discussions/276).

## Prerequisites

Unfortunately, as of late 2018, you are required to have a Twitter Developer account
in order to create a Twitter app.

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
export TWITTER_CONSUMER_KEY="[your consumer key]"
export TWITTER_CONSUMER_SECRET="[your consumer secret]"
export TWITTER_ACCESS_TOKEN="[your access token]"
export TWITTER_ACCESS_TOKEN_SECRET="[your access token secret]"
```

### Get your tweet archive

1. Open the [Your Twitter data page](https://twitter.com/settings/your_twitter_data).
1. Scroll to the 'Download your Twitter data' section at the bottom of the page.
1. Click 'Request data', and wait for the email to arrive.
1. Follow the link in the email to download your Tweet data.
1. Unpack the archive, and move `tweet.js` to the same directory as this script.

## Getting started

### Local

First, install the required dependencies.

```bash
pip install -r requirements.txt
```

Then, for example, delete any tweet from _before_ January 1, 2018:

```bash
python deletetweets.py -d 2018-01-01 tweet.js
```

Or only delete all retweets:

```bash
python deletetweets.py -r retweet tweet.js
```

### Docker

Alternatively, you could run this script in a [Docker](https://docs.docker.com/install/)
container.

First, you need to build the Docker image.

```bash
docker build -t koenrh/delete-tweets .
```

Then, run the script using the following command.

:warning: Before you continue, you should be aware that most shells record user
input (and thus secrets) into a history file. In Bash you could prevent this by
prepending your command with a _single space_ (requires `$HISTCONTROL` to be set
to `ignorespace` or `ignoreboth`).

```bash
docker run --env TWITTER_CONSUMER_KEY="$TWITTER_CONSUMER_KEY=" \
  --env TWITTER_CONSUMER_SECRET="$TWITTER_CONSUMER_SECRET=" \
  --env TWITTER_ACCESS_TOKEN="$TWITTER_ACCESS_TOKEN=" \
  --env TWITTER_ACCESS_TOKEN_SECRET="$TWITTER_ACCESS_TOKEN_SECRET=" \
  --volume "$PWD:/app" --rm -it koenrh/delete-tweets -d 2018-01-01 /app/tweet.js
```

You could make this command more easily accessible by putting it an executable,
and make sure that it is available in your `$PATH`.
