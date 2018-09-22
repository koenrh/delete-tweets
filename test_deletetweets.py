import unittest

from datetime import date
from deletetweets import TweetReader


class FakeTwitterApi(object):
    def __init__(self):
        self.tweets = []

    def DestroyStatus(self, tweet_id):
        self.tweets.append(tweet_id)
        print "Destroyed tweet %s" % tweet_id


class FakeReader(object):
    def __init__(self, test_dict):
        self.index = 0
        self.test_dict = test_dict

    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.test_dict):
            raise StopIteration

        value = self.test_dict[self.index]
        self.index = self.index + 1
        return value


class TestDeleteTweets(unittest.TestCase):
    def test_tweet_reader_retweet(self):
        tweets = [{"tweet_id": "42", "retweeted_status_id": "200"},
                  {"tweet_id": "43", "retweeted_status_id": ""},
                  {"tweet_id": "44", "retweeted_status_id": "300"}]

        expected = [{"tweet_id": "42"}, {"tweet_id": "44"}]

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              restrict="retweet")):
            self.assertEqual(expected[idx]['tweet_id'], val['tweet_id'])

    def test_tweet_reader_reply(self):
        tweets = [{"tweet_id": "12", "in_reply_to_status_id": ""},
                  {"tweet_id": "13", "in_reply_to_status_id": "203"}]

        expected = [{"tweet_id": "13"}]

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              restrict="reply")):
            self.assertEqual(expected[idx]['tweet_id'], val['tweet_id'])

    def test_tweet_reader_date(self):
        tweets = [{"tweet_id": "21", "timestamp": "2013-03-06 20:22:06 +0000"},
                  {"tweet_id": "22", "timestamp": "2014-03-06 20:22:06 +0000"}]

        expected = [{"tweet_id": "21"}]

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              date='2014-02-01')):
            self.assertEqual(expected[idx]['tweet_id'], val['tweet_id'])


if __name__ == '__main__':
    unittest.main()
