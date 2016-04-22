from . import utils
import random


class Tweet(object):
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
        lat = random.uniform(self.get_lat_n(0), self.get_lat_n(1))
        # The longitudes are the same for points 0 and 1, as well as 2 and 3.
        lon = random.uniform(self.get_lon_n(0), self.get_lon_n(2))
        return lat, lon
