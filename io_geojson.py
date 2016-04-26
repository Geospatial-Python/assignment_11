'''
Created on Apr 19, 2016

@author: Max Ruiz
'''
import json

def read_geojson(input_file):
    # Please use the python json module (imported above)
    # to solve this one.
    with open(input_file,'r') as f:
        gj = json.load(f)
    return gj

def processTweets(tweets):
    with open(tweets, 'r') as f:
        jfile = json.load(f)
    return jfile
