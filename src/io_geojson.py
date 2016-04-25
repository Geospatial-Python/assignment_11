import json


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
    with open(input_file, 'r') as fp:
        gj = json.load(fp)
    return gj


def read_tweets(tweet_file):
    with open(tweet_file, 'r') as fp:
        to_return = json.load(fp)
    return to_return
