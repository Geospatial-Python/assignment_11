import random
import utils
from nltk.sentiment.util import demo_liu_hu_lexicon as classifier

class Tweet(object):

	def __init__(self, tweet):

		self.tweet_id = tweet['id']
		self.date = tweet['created_at']
		self.text = tweet['text']
		self.username = tweet['user']['name']
		self.user_description = tweet['user']['description']
		self.followers_count = tweet['user']['followers_count']
		self.bounds = tweet['place']['bounding_box']['coordinates'][0]
		self.sentiment = self.classify(self.text)

	def find_lat(self, n):
		return self.bounds[n][1]

	def find_lng(self, n):
		return self.bounds[n][0]

	def bounds(self):
		lat = random.uniform(self.find_lat(0), self.find_lat(1))
		lng = random.uniform(self.find_lng(0), self.find_lng(1))
		return lat, lng

	def classify(self, text):
		return classifier(text)