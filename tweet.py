import utils
from point import Point

class Tweet(object):
	def __init__(self, tweet_dic):
		self.tweet = tweet_dic['text']
		self.lat = tweet_dic['place']['bounding_box']['coordinates'][0][1]
		self.lng = tweet_dic['place']['bounding_box']['coordinates'][0][0]
		self.user = tweet_dic['user']['screen_name']
		self.source = tweet_dic['source']
		self.followers = tweet_dic['user']['followers_count']
		self.point = Point(self.lat, self.lng)

