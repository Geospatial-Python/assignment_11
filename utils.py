'''
Created on Feb 23, 2016

@author: Max Ruiz
'''
import math
import random
#import analytics
from analytics import average_nearest_neighbor_distance
from point import Point


def g_function(pointsArr, d):
    gPrime = 0
    for x in pointsArr:
        shrtDist = 100000
        for y in pointsArr:
            if x == y:
                continue
            else:
                temp = euclidean_distance(x,y)
                if temp < shrtDist:
                    shrtDist = temp
        if shrtDist <= d:
            gPrime += shrtDist

    return gPrime / len(pointsArr)

def create_random_marked_points(n, marks=[]):
    random.seed()
    randPoints = list()
    for x in range(n):
        _x = random.randint(0,100)
        _y = random.randint(0,100)
        if marks is None:
            randPoints.append(Point(_x, _y))
        else:
            if len(marks) == 0:
                randPoints.append(Point(_x, _y))
            else:
                rndmark = random.choice(marks)
                randPoints.append(Point(_x, _y, rndmark))
    return randPoints

def permutations(p=99, n=100, marks = None):
    """
    Calculate p number of average_nearest_neighbor_distances from n number
    of randomly generated points. Return list of size p with distance values.

    Parameter(s): integer p, integer n

    Return(s): list perm
    """
    perm = []
    for x in range(p):
        points = create_random_marked_points(n, marks)
        avg_nnd = average_nearest_neighbor_distance(points)
        perm.append(avg_nnd)

    return perm

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


def shift_point(point, x_shift, y_shift):
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
    >>> point = (0,0)
    >>> shift_point(point, 1, 2)
    (1,2)
    """
    x = getx(point)
    y = gety(point)

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


def check_in(point, point_list):
    """
    Check whether point is in the point list

    Parameters
    ----------
    point : tuple
            In the form (x,y)

    point_list : list
                 in the form [point, point_1, point_2, ..., point_n]
    """
    return point in point_list


def getx(point):
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
    return point[0]


def gety(point):
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
    return point[1]
