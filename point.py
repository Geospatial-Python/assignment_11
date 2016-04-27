#Point class
import sys
import os

sys.path.insert(0, os.path.abspath('..'))

import utils


class Point(object):

	def __init__(self, x, y, mark=None):
		self.x = x
		self.y = y
		self.mark = mark

	#Magic methods
	def __str__(self):
		return ("{0}, {1}").format(self.x, self.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __ne__(self, other):
		return self.x != other.x or self.y != other.y

	#Class methods
	def check_coincident(self, test):
		return utils.check_coincident((self.x, self.y), test)

	def shift_point(self, x_shift, y_shift):
		point = (self.x, self.y)
		self.x, self.y = utils.shift_point(point, x_shift, y_shift)
