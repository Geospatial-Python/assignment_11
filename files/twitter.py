from . import utils
import random
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank


class Tweet(object):

    positive = 'Positive'
    negative = 'Negative'
    neutral = 'Neutral'


    def __init__(self, tweet_dict):

        self.tweet = tweet_dict['text']
        self.bounds = tweet_dict['place']['bounding_box']['coordinates'][0][0]
        self.follower_count = tweet_dict['user']['followers_count']
        self.screen_name = tweet_dict['user']['screen_name']
        self.friends = tweet_dict['user']['friends_count']
        self.lat = None
        self.long = None

        self.sentiment = self.classifier(self.tweet)


    def get_lat(self, n):

        return self.bounds[n][1]

    def get_long(self, n):

        return self.bounds[n][0]

    def generate_bounds(self):

        self.lat = random.uniform(self.get_lat(0), self.get_lat(1))
        self.long = random.uniform(self.get_long(0), self.get_long(1))


    def classifier(sentence):

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

