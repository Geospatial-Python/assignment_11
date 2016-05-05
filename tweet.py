from point import Point
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

import random


class Tweet(object):
    def __init__(self, tweet_dictionary):

        # in addition to the text, consider the date, the username, and the number of f

        self.text = tweet_dictionary['text']
        self.date = tweet_dictionary['created_at']
        self.username = tweet_dictionary['user']['name']
        self.bounds = tweet_dictionary['place']['bounding_box']['coordinates'][0]
        self.user_followers = tweet_dictionary['user']['followers_count']

    def gen_rand_pt(self, mark=None):

        # create a random point known from the approximately known bounding location
        lat = random.uniform(self.bounds[0][1], self.bounds[1][1])
        lon = random.uniform(self.bounds[0][0], self.bounds[2][0])

        # apply composition here

        return Point(lat, lon,self.classifier())

    def classifier(self):

        tokenizer = treebank.TreebankWordTokenizer()
        pos_words = 0
        neg_words = 0
        tokenized_sent = [word.lower() for word in tokenizer.tokenize(self.text)]

        x = list(range(len(tokenized_sent)))
        y = []

        for word in tokenized_sent:
            if word in opinion_lexicon.positive():
                pos_words += 1
                y.append(1)
            elif word in opinion_lexicon.negative():
                neg_words += 1
                y.append(-1)
            else:
                y.append(0)

        if pos_words > neg_words:
            return 'Positive'
        elif pos_words < neg_words:
            return 'Negative'
        elif pos_words == neg_words:
            return 'Neutral'
