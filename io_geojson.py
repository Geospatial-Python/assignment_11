import json
# from urllib.request import urlopen

def read_tweets(input_file):
  with open(input_file, 'r') as f:
    tweets = json.load(f)
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
  gj = None

  with open(input_file, 'r') as f:
    gj = json.load(f)

  return gj
