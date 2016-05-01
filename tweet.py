import utils
import random
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

class Tweet(object):
    def __init__(self, tweet_dict):
        self.tweet = tweet_dict['text']
        self.bounds = tweet_dict['place']['bounding_box']['coordinates'][0]
        self.date = tweet_dict['created_at']
        self.username = tweet_dict['user']['name']
        self.user_description = tweet_dict['user']['description']
        self.tweet_id = tweet_dict['id']
        self.user_followers_count = tweet_dict['user']['followers_count']
        self.sentiment = self.classifier(self.tweet)
        #print("Current Sentiment:" + self.sentiment)
        
    def get_lat_n(self, n):
        return self.bounds[n][1]
    
    def get_lon_n(self, n):
        return self.bounds[n][0]
    
    def gen_point_in_bounds(self):
        lat = random.uniform(self.get_lat_n(0), self.get_lat_n(1))
        lon = random.uniform(self.get_lon_n(0), self.get_lon_n(2))
        return lat, lon
    
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
    