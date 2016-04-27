#analytics
import math
import json
import sys 
import os

sys.path.insert(0, os.path.abspath('..'))

import utils
import point

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
    temp = gj['features']
    city = ""
    max_population = 0

    for i in temp:
        if (i['properties']['pop_max'] > max_population):
            max_population = i['properties']['pop_max']
            city = i['properties']['name']

    return city, max_population

def write_your_own(gj):
    """
    Here you will write your own code to find
    some attribute in the supplied geojson file.

    Take a look at the attributes available and pick
    something interesting that you might like to find
    or summarize.  This is totally up to you.

    Do not forget to write the accompanying test in
    tests.py!
    """
    #Finds how many megacities there are in the geoJSON
    temp = gj['features']
    megacities = 0

    for i in temp:
        if(i['properties']['megacity'] == 1):
            megacities += 1


    return megacities

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

    for point in points:
        x += point[0]
        y += point[1] 

    x = x / len(points)
    y = y / len(points)

    return x, y

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

    temp_points = []

    if mark is not None:
        for point in points:
            if point.mark is mark:
                temp_points.append(point)
    else:
        temp_points = points

    nearest = []

    for i, point in enumerate(temp_points):
        nearest.append(None)
        for j, point2 in enumerate(temp_points):
            if i is not j:
                dist = euclidean_distance((point.x, point.y), (point2.x, point2.y))
                if nearest[i] == None:
                    nearest[i] = dist
                elif nearest[i] > dist:
                    nearest[i] = dist

    mean_d = sum(nearest) / len(points)

    return mean_d

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

    first = True 
    mbr = [0,0,0,0]

    for point in points:
        if first:
            first = False
            mbr[0] = point[0]
            mbr[1] = point[1]
            mbr[2] = point[0]
            mbr[3] = point[1]

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
    area = (mbr[1] - mbr[3]) * (mbr[0] - mbr[2])
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

    expected = 0.5 * (area / n) ** 0.5
    return expected

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


def permutations(p=99, n=100, marks=None):
    perms = []

    if marks is None:
        for i in range(p):
            perms.append(average_nearest_neighbor_distance(utils.create_random_marked_points(n, marks=None)))

    else:
        for i in range(p):
            perms.append(average_nearest_neighbor_distance(utils.create_random_marked_points(n, marks)))

    return perms

def find_criticals(perms):
    lower = min(perms)
    upper = max(perms)
    return lower, upper

def check_significance(lower, upper, observed):
    if observed > upper:
        return True
    elif observed < lower:
        return True
    else:
        return False
