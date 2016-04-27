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
    with open ('data/us_cities.geojson', 'r') as f:
        gj = json.load(f)
    
    return gj

def read_twitter(input_file):

    with open('F:/GitHub GIS 321/assignment_10/tweets.json', 'r') as fp:
        twitter_gj = json.load(fp)
    return twitter_gj
