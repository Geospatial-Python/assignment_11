import json  # I would like you to use the JSON module for reading geojson (for now)


def read_tweets(inputFile):
    with open(inputFile, 'r') as fp:
        tweets = json.load(fp)
    return tweets

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
    
    with open(input_file, 'r') as f:
        gj = json.load(f)
    return gj