import json
import folium
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
    
    with open(input_file, 'r') as f:
        gj=json.load(f)
    
    # Please use the python json module (imported above)
    # to solve this one.

    return gj
