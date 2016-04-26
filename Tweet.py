'''
Created on Apr 19, 2016

@author: Max Ruiz
'''

import utils
import random

from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank



class Tweet(object):
    def __init__(self, tweet_json_obj):

        self.twText = tweet_json_obj["text"]
        self.twBoundingBox = tweet_json_obj["place"]["bounding_box"]["coordinates"][0]
        self.twID = tweet_json_obj["id"]
        self.twRetweetCount = tweet_json_obj["retweet_count"]
        self.twRepliedTo = tweet_json_obj["in_reply_to_screen_name"]
        self.twScreenName = tweet_json_obj["user"]["screen_name"]
        self.twDate = tweet_json_obj["created_at"]

        self.sentiment = self.classifier(self.twText)
        self.mark = self.sentiment


    def getLatitude(self, corner):
        return self.twBoundingBox[corner][1]

    def getLongitude(self, corner):
        return self.twBoundingBox[corner][0]

    def getRandPointInBoundingBox(self):
        latitude = random.uniform(self.getLatitude(0), self.getLatitude(1))
        longitude = random.uniform(self.getLongitude(0), self.getLongitude(2))
        return latitude, longitude

    def getMark(self):
        return self.mark

    def getPoint(self):
        x, y = self.getRandPointInBoundingBox()
        return (x,y)


    def classifier(self,sentence):

        tokenizer = treebank.TreebankWordTokenizer()
        pos_words = 0
        neg_words = 0
        tokenized_sent = [word.lower() for word in tokenizer.tokenize(sentence)]

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


