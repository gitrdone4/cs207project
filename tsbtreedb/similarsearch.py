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
Similar Search

A python command line utility to search for similar light curves.

Usage: ./similarsearch input.txt  [optional flags]

Optional flags:
  -h, --help    Show this help message and exit.

"""
LIGHT_CURVES_DIR = "light_curves/"
DB_DIR = "temp/"


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

def load_ts(ts_name):
     global LIGHT_CURVES_DIR

     if ts_name.startswith("ts-"):
        filepath = LIGHT_CURVES_DIR + ts_name
        try:
            data = np.loadtxt(filepath)
        except(IOError):
            print("Unable to load %s" % file)
        else:
            times, values = data.T
            ts = ats.ArrayTimeSeries(times=times,values=values)
            return ts

def load_input(filepath):
    try:
        data = np.loadtxt(filepath)
    except(IOError):
        print("Unable to load %s" % file)
    else:
        times, values = data.T
        ts = ats.ArrayTimeSeries(times=times,values=values)
        return ts


def load_vp_lcs():
    global DB_DIR
    vps_dict= {}
    for file in os.listdir(DB_DIR):
        if file.startswith("ts-") and file.endswith(".dbdb"):
            lc_id = file[:-5] +  '.txt'
            vps_dict[lc_id] = load_ts(lc_id)
    return vps_dict


def print_children(key,db):
    try:
        print (key, 'left: ', db.get_left(key))
    except:
        print ('None')
    try:
        print (key, 'right: ', db.get_right(key))
    except:
        print ('None')
    print ('\n')

def build_vp_dbs(vp,timeseries_dict):
    sorted_ds = (calc_distances(vp,timeseries_dict))
    db = unbalancedDB.connect(DB_DIR + vp[:-4] + ".dbdb")

    for key, val in sorted_ds:
        db.set(key, val)

    db.commit()
    db.close()


if __name__ == "__main__":
    # Default usage options
    need_help = False
    have_input = False
    while(True):
        if len(sys.argv) <= 1:
            print("Error: No aurguments provided")
            print("Usage: ./similarsearch input.txt  [optional flags]")
            break

        # First, identify which flags were included
        for arg in sys.argv[1:]:
            if arg.lower() in ['-h','--help', 'help']: need_help = True
            if '.txt' in arg.lower():
                have_input = True
                input_path = arg

        if need_help:
            print (HELP_MESSAGE)
            break
        elif(have_input):
            vps_dict = load_vp_lcs()
            print("Loaded %d vp files" % len(vps_dict))
            input_ts = load_input(input_path)
            vp_distances = []
            for k in vps_dict:
                if k != input_path:
                    vp_distances.append((kernal_dist(input_ts, vps_dict[k]),k))

            vp_distances = sorted(vp_distances)
            closest_vp = vp_distances[0][1]
            print(closest_vp)
            break
        else:
            break

