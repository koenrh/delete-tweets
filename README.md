# Delete tweets

Delete tweets (or just replies or retweets) from your timeline, including tweets
beyond the [3,200 tweet limit](https://web.archive.org/web/20131019125213/https://dev.twitter.com/discussions/276).

## Prerequisites

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

```bash
export TWITTER_CONSUMER_KEY="[your consumer key]"
export TWITTER_CONSUMER_SECRET="[your consumer secret]"
export TWITTER_ACCESS_TOKEN="[your access token]"
export TWITTER_ACCESS_TOKEN_SECRET="[your access token secret]"
```

### Get your tweet archive

1. Open your [Twitter account page](https://twitter.com/settings/account).
1. Scroll to the bottom of the page, click 'Request your archive' (not 'Your Twitter
  data' in the left sidebar!), and wait for the email to arrive.
1. Follow the link in the email to download your Tweet archive.
1. Unpack the archive, and move `tweets.csv` to the same directory as this script.

## Usage

### Local

First, install the required dependencies.

```
pip install -r requirements.txt
```

Then, for example, delete any tweet from before *January 1, 2014*:

```bash
python deletetweets.py -d 2014-01-01 tweets.csv
```

Or delete all retweets:

```bash
python deletetweets.py -r retweet tweets.csv
```

### Docker

Alternatively, if you have Docker [installed](https://docs.docker.com/install/),
you could run the script using the following command.

```bash
docker run --env TWITTER_CONSUMER_KEY="[your consumer key]" \
  --env TWITTER_CONSUMER_SECRET="[your consumer secret]" \
  --env TWITTER_ACCESS_TOKEN="[your access token]" \
  --env TWITTER_ACCESS_TOKEN_SECRET="[your access token secret]"
  --rm -it koenrh/delete-tweets \
  -v $E:PWD":/app" -d 2014-01-01 /app/tweets.csv
```

You could make this command more easily accessible by putting it an executable,
and make sure that it is available in your `$PATH`.
