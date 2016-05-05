import utils
import math

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
    city = None
    max_population = 0

    features = gj['features']
    for i in features:
        if(i['properties']['pop_max']>max_population):
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

    #I chose the least creative route of finding the average population among all cities

    sum_population = 0
    n = 0

    features = gj['features']
    for i in features:
        sum_population = i['properties']['pop_max']+sum_population
        n = n+1

    return sum_population/n

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

    for i in points:
        x = x+i[0]
        y = y+i[1]
        n = n+1

    x = x/n
    y = y/n
    return x, y


# def average_nearest_neighbor_distance(points):
#     """
#     Given a set of points, compute the average nearest neighbor.

#     Parameters
#     ----------
#     points : list
#              A list of points in the form (x,y)

#     Returns
#     -------
#     mean_d : float
#              Average nearest neighbor distance

#     References
#     ----------
#     Clark and Evan (1954 Distance to Nearest Neighbor as a
#      Measure of Spatial Relationships in Populations. Ecology. 35(4)
#      p. 445-453.
#     """

#     #create empty list of distances
#     shortestDistList = []

#     for i in points:
#         shortest = 9999999999
#         for j in points:
#             if i!=j:
#                 current = euclidean_distance(i,j)
#                 if(current<shortest):
#                     shortest = current
#         shortestDistList.append(shortest)

#     n = 0
#     mean_d = 0
#     for i in shortestDistList:
#         mean_d = mean_d+i
#         n = n+1

#     return mean_d/(n)

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

    mbr = [0,0,0,0]

    x_max = -99999999999
    x_min = 999999999999
    y_max = -99999999999
    y_min = 999999999999

    for i in points:
        if i[0] > x_max:
            x_max = i[0]
        if i[0] < x_min:
            x_min = i[0]
        if i[1] > y_max:
            y_max = i[1]
        if i[1] < y_min:
            y_min = i[1]

        mbr = [x_min,y_min,x_max,y_max]

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

    expected = 0.5 * math.sqrt(area / n)
    return expected

def compute_critical(points):
    """
    Compute the "critical" points for the Monte Carlo
    simulation as the minimum and maximum of the points

    Parameters
    ----------
    points : float
           The area of the study area

    (min,max) : int
        The minimum and maximum list
    """

    return min(points), max(points)

def check_significant(input_min,input_max,X):
    """
    Compute the "critical" points for the Monte Carlo
    simulation as the minimum and maximum of the points

    Parameters
    ----------
    area : float
           The area of the study area

    n : int
        The number of points
    """

    flag = False;

    if X>input_max:
        flag = True
    elif X<input_min:
        flag = True

    return flag