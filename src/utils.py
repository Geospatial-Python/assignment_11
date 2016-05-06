def n_random_Points(n,marks=[]):

    PointList = [point.Point(random.uniform(0,1),random.uniform(0,1),random.choice(marks)) for x in range(n)]

    return PointList


def manhattan_distance(a, b):
    """
    Compute the Manhattan distance between two points
    Parameters
    ----------
    a : tuple
        A point in the form (x,y)
    b : tuple
        A point in the form (x,y)
    Returns
    -------
    distance : float
               The Manhattan distance between the two points
    """
    distance =  abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance


def euclidean_distance(a, b):
    """
    Compute the Euclidean distance between two points
    Parameters
    ----------
    a : tuple
        A point in the form (x,y)
    b : tuple
        A point in the form (x,y)
    Returns
    -------
    distance : float
               The Euclidean distance between the two points
    """
    distance = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return distance


def shift_point(points, x_shift, y_shift):
    """
    Shift a point by some amount in the x and y directions
    Parameters
    ----------
    point : tuple
            in the form (x,y)
    x_shift : int or float
              distance to shift in the x direction
    y_shift : int or float
              distance to shift in the y direction
    Returns
    -------
    new_x : int or float
            shited x coordinate
    new_y : int or float
            shifted y coordinate
    Note that the new_x new_y elements are returned as a tuple
    Example
    -------
    >>> points = (0,0)
    >>> shift_point(points, 1, 2)
    (1,2)
    """
    x = getx(points)
    y = gety(points)

    x += x_shift
    y += y_shift

    return x, y


def check_coincident(a, b):
    """
    Check whether two points are coincident
    Parameters
    ----------
    a : tuple
        A point in the form (x,y)
    b : tuple
        A point in the form (x,y)
    Returns
    -------
    equal : bool
            Whether the points are equal
    """
    return a == b


def check_in(points, point_list):
    """
    Check whether point is in the point list
    Parameters
    ----------
    point : tuple
            In the form (x,y)
    point_list : list
                 in the form [point, point_1, point_2, ..., point_n]
    """
    return points in point_list


def getx(points):
    """
    A simple method to return the x coordinate of
     an tuple in the form(x,y).  We will look at
     sequences in a coming lesson.
    Parameters
    ----------
    point : tuple
            in the form (x,y)
    Returns
    -------
     : int or float
       x coordinate
    """
    return points[0]


def gety(points):
    """
    A simple method to return the x coordinate of
     an tuple in the form(x,y).  We will look at
     sequences in a coming lesson.
    Parameters
    ----------
    point : tuple
            in the form (x,y)
    Returns
    -------
     : int or float
       y coordinate
    """
    return points[1]

from . import point
import math
import random