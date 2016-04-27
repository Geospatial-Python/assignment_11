import utils
from point import Point
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank

class Tweet(object):
	def __init__(self, tweet_dic):
		self.tweet = tweet_dic['text']
		self.lat = tweet_dic['place']['bounding_box']['coordinates'][0][1]
		self.lng = tweet_dic['place']['bounding_box']['coordinates'][0][0]
		self.user = tweet_dic['user']['screen_name']
		self.source = tweet_dic['source']
		self.followers = tweet_dic['user']['followers_count']
		self.point = Point(self.lat, self.lng)
		self.sentiment = self.classifier()

	def classifier(self):
		
		tokenizer = treebank.TreebankWordTokenizer()
		pos_words = 0
		neg_words = 0
		tokenized_sent = [word.lower() for word in tokenizer.tokenize(self.tweet)]

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

