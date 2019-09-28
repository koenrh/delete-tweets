import unittest

from deletetweets import TweetReader


class FakeTwitterApi(object):
    def __init__(self):
        self.tweets = []

    def DestroyStatus(self, tweet_id):
        self.tweets.append(tweet_id)
        print("Destroyed tweet %s" % tweet_id)


class FakeReader(object):
    def __init__(self, test_dict):
        self.index = 0
        self.test_dict = test_dict

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.test_dict):
            raise StopIteration

        value = self.test_dict[self.index]
        self.index = self.index + 1
        return value

    def next(self):
        return self.__next__()


class TestDeleteTweets(unittest.TestCase):
    def test_tweet_reader_retweet(self):
        tweets = [{"id_str": "42", "full_text": "RT @github \\o/"},
                  {"id_str": "43", "full_text": ""},
                  {"id_str": "49", "full_text": ""},
                  {"id_str": "44", "full_text": "RT @google OK, Google"}]

        expected = [{"id_str": "42"}, {"id_str": "44"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              restrict="retweet").read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))

    def test_tweet_reader_reply(self):
        tweets = [{"id_str": "12", "in_reply_to_user_id_str": ""},
                  {"id_str": "14", "in_reply_to_user_id_str": "200"},
                  {"id_str": "16", "in_reply_to_user_id_str": ""},
                  {"id_str": "18", "in_reply_to_user_id_str": "203"}]

        expected = [{"id_str": "14"}, {"id_str": "18"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              restrict="reply").read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))

    def test_tweet_reader_date(self):
        tweets = [{"id_str": "21", "created_at": "Wed March 06 20:22:06 +0000 2013"},
                  {"id_str": "22", "created_at": "Thu March 05 20:22:06 +0000 2014"}]

        expected = [{"id_str": "21"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              date="2014-02-01").read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))

    def test_tweet_reader_spare(self):
        tweets = [{"id_str": "21"},
                  {"id_str": "22"},
                  {"id_str": "23"}]

        expected = [{"id_str": "21"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              spare=["22", "23"]).read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))

    def test_tweet_reader_likes(self):
        tweets = [{"id_str": "21", "favorite_count": 0},
                  {"id_str": "22", "favorite_count": 1},
                  {"id_str": "23", "favorite_count": 2}]

        expected = [{"id_str": "21"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              min_likes=1).read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))

    def test_tweet_reader_retweets(self):
        tweets = [{"id_str": "21", "retweet_count": 0},
                  {"id_str": "22", "retweet_count": 1},
                  {"id_str": "23", "retweet_count": 2}]

        expected = [{"id_str": "21"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              min_retweets=1).read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))

    def test_tweet_reader_min_none_arg(self):
        tweets = [{"id_str": "21", "retweet_count": 0}]
        expected = [{"id_str": "21"}]
        actual = []

        for idx, val in enumerate(TweetReader(FakeReader(tweets),
                                              min_likes=None, min_retweets=None).read()):
            self.assertEqual(expected[idx]["id_str"], val["id_str"])
            actual.append(val)

        self.assertEqual(len(expected), len(actual))


if __name__ == "__main__":
    unittest.main()
