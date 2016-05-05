import json

#In the io_geojson module write a function that ingests the twitter data and returns a dictionary. Note that you could write this from scratch or,
#if a suitable library exists (maybe a built-in), utilize someone else's library.

def read_twitter_data(input_file):
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
    with open(input_file,'r') as file:
        gj = json.load(file)
    return gj

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
    with open(input_file,'r') as file:
        gj = json.load(file)
    return gj
