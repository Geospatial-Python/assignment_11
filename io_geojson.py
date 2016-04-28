import json
import random

def read_tweet_json(input_file):
    """
    Read a tweet json file

    Parameters
    ----------
    input_file : str
                 The PATH to the data to be read

    Returns
    -------
    gj : dict
         An in memory version of the geojson
    """
    with open(input_file, 'r') as fp:
        tweets = json.loads(fp.read())
        return tweets


def ingest_twitter_data(twitter_data):
    """
    Ingest a tweet data and return the dict of needed data.

    Parameters
    ----------
    twitter_data : str
                 The tweet data  to be ingest

    Returns
    -------
    need_data : dict

    """

    if twitter_data['geo']==None:

        x_list=[value[1] for value in (twitter_data["place"]["bounding_box"]["coordinates"][0])]

        y_list=[value[0] for value in (twitter_data["place"]["bounding_box"]["coordinates"][0])]
        x=random.uniform(min(x_list),max(x_list))
        y=random.uniform(min(y_list),max(y_list))
    else:
        x=twitter_data['geo']['coordinates'][0]
        y=twitter_data['geo']['coordinates'][1]

    need_data={"point":(x,y),"text":twitter_data["text"],"id_str":twitter_data["id_str"],"lang":twitter_data["lang"],"source":twitter_data["source"],"created_time":twitter_data["created_at"]}
    return need_data

def read_geojson(input_file):
    """
    Read a geojson file

    Parameters
    ----------
    input_file : str
                 The PATH to the data to be read

    Returns
    -------
    gj : dict
         An in memory version of the geojson
    """
    # Please use the python json module (imported above)
    # to solve this one.
    gj = None
    fp = open(input_file, 'r')
    gj = json.loads(fp.read())
    fp.close()
    return gj

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
    for feature in gj["features"]:
        if feature["properties"]["pop_max"]>max_population:
            max_population=feature["properties"]["pop_max"]
            city=feature["properties"]["nameascii"]

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

    To find the average of pop_max and pop_min.

    """

    sum_pop_max=0
    sum_pop_min=0
    num=0
    for feature in gj["features"]:
        sum_pop_max+=feature["properties"]["pop_max"]
        sum_pop_min+=feature["properties"]["pop_min"]
        num+=1

    return float(sum_pop_max/num),float(sum_pop_min/num)
