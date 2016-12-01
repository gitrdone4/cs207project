#!/usr/local/bin/python3

# Hacky solution to import array time series from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')
import arraytimeseries as ats

from crosscorr import kernal_dist
import unbalancedDB
import numpy as np
#below is your module. Use your ListTimeSeries or ArrayTimeSeries..
import arraytimeseries as ats
import random

# Global variables

HELP_MESSAGE = \
"""
Build DB

A python command line utility to generate vantage point DBs from light-curve files.

Usage: ./builddb  [optional flags]

Optional flags:
  -h, --help    Show this help message and exit.

"""
from settings import LIGHT_CURVES_DIR,DB_DIR,SAMPLE_DIR,TEMP_DIR,TS_LENGTH

def load_ts():
    global LIGHT_CURVES_DIR
    timeseries_dict = {}

    for file in os.listdir(LIGHT_CURVES_DIR):
        if file.startswith("ts-") and file.endswith(".txt"):
            #id_num = int(file[3:-4])
            filepath = LIGHT_CURVES_DIR + file
            data = np.loadtxt(filepath)
            times, values = data.T
            ts = ats.ArrayTimeSeries(times=times,values=values)
            timeseries_dict[file] = ts

    return timeseries_dict

def pick_vantage_points(timeseries_dict,n=20):
    return random.sample(timeseries_dict.keys(), n)

def calc_distances(vp_k,timeseries_dict):
    distances = []
    vp = timeseries_dict[vp_k]
    for k in timeseries_dict:
        if k != vp_k:
            distances.append((kernal_dist(vp, timeseries_dict[k]),k))
    return distances

def clear_vp_dbs():
    import shutil
    shutil.rmtree(DB_DIR)
    os.makedirs(DB_DIR, exist_ok=True)

def save_vp_dbs(vp,timeseries_dict):
    sorted_ds = (calc_distances(vp,timeseries_dict))
    db = unbalancedDB.connect(DB_DIR + vp[:-4] + ".dbdb")

    for key, val in sorted_ds:
        db.set(key, val)

    db.commit()
    db.close()

def create_vpdbs(n=20):
    print("Creating %d vantage point dbs" % n,end="")
    timeseries_dict = load_ts()
    vantage_points = pick_vantage_points(timeseries_dict,n)
    clear_vp_dbs()
    for vp in vantage_points:
        print('.', end="")
        save_vp_dbs(vp,timeseries_dict)
    print("Done.")

if __name__ == "__main__":
    # Default usage options
    need_help = False

    # First, identify which flags were included
    for arg in sys.argv[1:]:
        if arg.lower() in ['-h','--help', 'help']: need_help = True

    while(True):

        if need_help:
            print (HELP_MESSAGE)
            break
        else:
            break

