# Delete tweets

Delete tweets (or just replies or retweets) from your timeline, including tweets
beyond the [3,200 tweet limit](https://web.archive.org/web/20131019125213/https://dev.twitter.com/discussions/276).

## Prerequisites

### Configure access

1. Open Twitter's [Application Management](https://apps.twitter.com/), and create a new Twitter app.
2. Set the permissions of your app to *Read and Write*.
3. Set the required environment variables:

```bash
TWITTER_CONSUMER_KEY="[your consumer key]"
TWITTER_CONSUMER_SECRET="[your consumer secret]"
TWITTER_ACCESS_TOKEN="[your access token]"
TWITTER_ACCESS_TOKEN_SECRET="[your access token secret]"
```

### Get your Twitter archive

1. Open your [account page](https://twitter.com/settings/account).
2. Click 'Your Twitter archive', and a link to your archive will arrive per email.
3. Follow the link in the email to download the archive.
4. Unpack the archive, and move `tweets.csv` to the same directory as this script.

## Installation

Install the required dependencies.

```
pip install -r requirements.txt
```

## Usage

For example, delete any tweet from before *January 1, 2014*:

```bash
python deletetweets.py -d 2014-01-01
```

Or delete all retweets:

```bash
python deletetweets.py -r "retweet"
```
