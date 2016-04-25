from . import utils
import random
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank


class Tweet(object):
    all = 'All'
    positive = 'Positive'
    negative = 'Negative'
    neutral = 'Neutral'

    def __init__(self, tweet_dict):
        """

        Parameters
        ----------
        tweet_dict A dictionary containing all the tweet information, as formated by the Twitter API.

        Returns
        -------

        """
        self.tweet = tweet_dict['text']
        # Lat/lon is formatted in tweets as : longitude, latitude
        self.bounds = tweet_dict['place']['bounding_box']['coordinates'][0]
        self.date = tweet_dict['created_at']
        self.username = tweet_dict['user']['name']
        self.user_description = tweet_dict['user']['description']
        self.tweet_id = tweet_dict['id']
        self.user_followers_count = tweet_dict['user']['followers_count']
        self.lat = None
        self.lon = None

    def get_lat_n(self, n):
        """
        Get the nth latitude in the bounding polygon.
        Parameters
        ----------
        n

        Returns
        -------

        """
        return self.bounds[n][1]

    def get_lon_n(self, n):
        """
        Get the nth longitude in the bounding polygon.
        Parameters
        ----------
        n

        Returns
        -------

        """
        return self.bounds[n][0]

    def gen_point_in_bounds(self):
        """
        Generates a random point inside the bounding polygon.
        Returns
        -------

        """
        # The latitudes are the same for points 0 and 2, as well as 1 and 3.
        self.lat = random.uniform(self.get_lat_n(0), self.get_lat_n(1))
        # The longitudes are the same for points 0 and 1, as well as 2 and 3.
        self.lon = random.uniform(self.get_lon_n(0), self.get_lon_n(2))
        return self.lat, self.lon

    def classifier(self):

        tokenizer = treebank.TreebankWordTokenizer()
        pos_words = 0
        neg_words = 0
        tokenized_sent = [word.lower() for word in tokenizer.tokenize(self.tweet)]

        x = list(range(len(tokenized_sent))) # x axis for the plot
        y = []

        for word in tokenized_sent:
            if word in opinion_lexicon.positive():
                pos_words += 1
                y.append(1) # positive
            elif word in opinion_lexicon.negative():
                neg_words += 1
                y.append(-1) # negative
            else:
                y.append(0) # neutral

        if pos_words > neg_words:
            return 'Positive'
        elif pos_words < neg_words:
            return 'Negative'
        elif pos_words == neg_words:
            return 'Neutral'
