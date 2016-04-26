'''
Created on Feb 23, 2016

@author: Max Ruiz
'''

import math

from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank


def compute_critical(p):
    """
    Given a list, p, of distances (constants), determine the upper and lower
    bound (or max and min value) of the set. The values in p are assumed floats.

    Parameter(s): list p

    Return(s): float lower, float upper
    """
    lower = min(p)
    upper = max(p)
    return lower, upper

def check_significant(lower, upper, observed):
    """
    Check if given observed point is outside or within a given lower and upper
    bound.

    Parameter(s): float lower, float upper, float observed.

    Return(s): boolean
    """
    return observed < lower or observed > upper

def find_largest_city(gj):
    """
    Iterate through a geojson feature collection and
    find the largest city.  Assume that the key
    to access the maximum population is 'pop_max'.

    Parameters
    ----------
    gj : dict
         A GeoJSON file read in as a Python dictionary

    Returns
    -------
    city : str
           The largest city

    population : int
                 The population of the largest city
    """

    max_population = 0
    for feat in gj['features']:
        test_max_pop = feat['properties']['pop_max']
        if test_max_pop > max_population:
            max_population = test_max_pop
            city = feat['properties']['name']

    return city, max_population

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
    sumx = 0.0
    sumy = 0.0
    for coord in points:
        sumx += coord[0]
        sumy += coord[1]
    x = sumx / len(points)
    y = sumy / len(points)

    return x, y


def average_nearest_neighbor_distance_tuples(points):
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
    min_dist_sum = 0
    for coord_n in points:
        first = True
        for  coord_m in points:
            if coord_n == coord_m:
                continue
            else:
                d = euclidean_distance(coord_n, coord_m)
                if first:
                    min_dist = d
                    first = False
                else:
                    if d < min_dist:
                        min_dist = d
        min_dist_sum += min_dist

    mean_d = min_dist_sum / len(points)

    return mean_d

def average_nearest_neighbor_distance(points, mark = None):
    if mark != None:
        pointsWithMark = list()
        for x in range(len(points)):
            if points[x].getMark() == mark:
                pointsWithMark.append(points[x].getPoint())
            else:
                continue
        return average_nearest_neighbor_distance_tuples(pointsWithMark)
    else:
        allPoints = list(points[x].getPoint() for x in range(len(points)))
        return average_nearest_neighbor_distance_tuples(allPoints)

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
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0
    for coord in points:
        if coord[0] < xmin:
            xmin = coord[0]
        elif coord[0] > xmax:
            xmax = coord[0]

        if coord[1] < ymin:
            ymin = coord[1]
        elif coord[1] > ymax:
            ymax = coord[1]

    xcorner = xmax - xmin
    ycorner = ymax - ymin
    mbr = [0,0,xcorner,ycorner]

    return mbr


def mbr_area(mbr):
    """
    Compute the area of a minimum bounding rectangle
    """
    length = mbr[3] - mbr[1]
    width = mbr[2] - mbr[0]
    area = length * width

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

    expected = 0.5 * math.sqrt(area / n)
    return expected

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
