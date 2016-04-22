from . import utils
import random


class Point(object):
    def __init__(self, x, y, **mark):
        self.x = x
        self.y = y
        self.mark = mark

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(self, other)

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def is_coincident(self, other_point):
        return utils.check_coincident((self.x, self.y), (other_point.x, other_point.y))

    def shift_point(self, delta_x, delta_y):
        result = utils.shift_point((self.x, self.y), delta_x, delta_y)
        self.x = utils.getx(result)
        self.y = utils.gety(result)

    def get_array(self):
        return [self.x, self.y]

    def euclidean_distance(self, other_point):
        return utils.euclidean_distance([self.x, self.y], [other_point.x, other_point.y])
