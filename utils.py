import math
import random
#from analytics import *
#from .point import Point

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

def create_random(n):
    """
    A simple method to return n random points.

    Parameters
    ----------
    n : integer
            number of points desired

    Returns
    -------
    points : n tuples of points
    """
    points = []
    limit = range(n)
    for i in limit:
        points.append((random.uniform(0,1), random.uniform(0,1)))

    return points

def permutations(p=99, n=100):
    """
    A simple method to return n random permutations of opints.

    Parameters
    ----------
    n : integer
            number of points desired

    Returns
    -------
    points : n tuples of points
    """
    permutes = []
    limit = range(p)
    for i in limit:
        permutes.append(average_nearest_neighbor_distance(create_random(n)))

    return permutes


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
#   Take a list of instances of your point class.
def average_nearest_neighbor_distance(points, mark=None):
    """
    Given a set of points, compute the average nearest neighbor.

    Parameters
    ----------
    points : list
             A list of points in the form (x,y)

    Returns
    -------
    mean_d : float
             Average nearest neighbor distance

    References
    ----------
    Clark and Evan (1954 Distance to Nearest Neighbor as a
     Measure of Spatial Relationships in Populations. Ecology. 35(4)
     p. 445-453.
    """

    #create empty list of distances
    shortestDistList = []
    temp = []

#   Accept a mark keyword argument where you can compute an average nearest neighbor distance for points with a shared mark. If mark is not provided, compute the average nearest neighbor using all points.
    if mark is not None:
        for point in points:
            if point.mark is mark:
                temp.append(point)

    else:
        temp = points

    for i in temp:
        shortest = 9999999999
        for j in temp:
            if i!=j:
                current = euclidean_distance(i,j)
                if(current<shortest):
                    shortest = current
        shortestDistList.append(shortest)

    n = 0
    mean_d = 0
    for i in shortestDistList:
        mean_d = mean_d+i
        n = n+1

    return mean_d/(n)

def create_random_marked_points(n, marks=[]):
    pointList = list()
    # for i in range(n):
    random.seed()
    for x in range(n):
        # get random x and y
        x = random.randint(0,100)
        # randomly select a mark
        y = random.randint(0,100)
        # create a point
        if len(marks) == 0:
        # Add it to a list
            pointList.append(Point(x, y))
        else:
            pointList.append(Point(x, y, random.choice(marks)))

