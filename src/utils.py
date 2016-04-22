import math
import random

from . import point


def create_random(n):
    """
    Generates n random points. Coordinates are between 0 and 1.00 inclusive.
    """
    rng = random.Random()
    marks = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    to_return = []
    for i in range(n):
        to_return.append(point.Point(
            round(rng.uniform(0, 1), 2),
            round(rng.uniform(0, 1), 2),
            color=rng.choice(marks)))
    return to_return


def check_significant(lower, upper, distance):
    return (distance < lower) or (distance > upper)


def mean_center(points):
    """
    Given a set of points, compute the mean center

    Parameters
    ----------
    points : list
         A list of points in the form (x,y)

    Returns
    -------
    x : float
        Mean x coordinate

    y : float
        Mean y coordinate
    """
    x = 0
    y = 0
    n = 0
    for point in points:
        x += point[0]
        y += point[1]
        n += 1

    x /= n
    y /= n

    return x, y


def minimum_bounding_rectangle(points):
    """
    Given a set of points, compute the minimum bounding rectangle.

    Parameters
    ----------
    points : list
             A list of points in the form (x,y)

    Returns
    -------
     : list
       Corners of the MBR in the form [xmin, ymin, xmax, ymax]
    """

    mbr = [None,None,None,None]
    for point in points:
        # First iteration, everything is None. The point will
        # form the initial boundaries for the rectangle.
        if mbr[0] is None:
            mbr[0] = point[0]
            mbr[1] = point[1]
            mbr[2] = point[0]
            mbr[3] = point[1]
        else:
            # Verify that each edge is far enough. If not, extend the rectangle.
            if point[0] < mbr[0]:
                mbr[0] = point[0]
            if point[1] < mbr[1]:
                mbr[1] = point[1]
            if point[0] > mbr[2]:
                mbr[2] = point[0]
            if point[1] > mbr[3]:
                mbr[3] = point[1]

    return mbr


def mbr_area(mbr):
    """
    Compute the area of a minimum bounding rectangle
    """
    area = (mbr[3] - mbr[1]) * (mbr[2] - mbr[0])

    return area


def expected_distance(area, n):
    """
    Compute the expected mean distance given
    some study area.

    This makes lots of assumptions and is not
    necessarily how you would want to compute
    this.  This is just an example of the full
    analysis pipe, e.g. compute the mean distance
    and the expected mean distance.

    Parameters
    ----------
    area : float
           The area of the study area

    n : int
        The number of points
    """

    expected = 0.5 * ((area / n) ** 0.5)
    return expected


"""
Below are the functions that you created last week.
Your syntax might have been different (which is awesome),
but the functionality is identical.  No need to touch
these unless you are interested in another way of solving
the assignment
"""


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