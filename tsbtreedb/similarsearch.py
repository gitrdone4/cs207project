#!/usr/local/bin/python3

# Hacky solution to import array time series from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')
import arraytimeseries as ats

from crosscorr import kernel_dist
from crosscorr import standardize
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



def load_ts(ts_name):
     global LIGHT_CURVES_DIR

     if ts_name.startswith("ts-"):
        filepath = LIGHT_CURVES_DIR + ts_name
        try:
            data = np.loadtxt(filepath)
        except(IOError):
            print("Error: Unable to load %s" % ts_name)
        else:
            times, values = data.T
            ts = ats.ArrayTimeSeries(times=times,values=values)
            return ts

def load_input(filepath):
    try:
        data = np.loadtxt(filepath)
    except(IOError):
        print("Error: Unable to load %s" % filepath)
    else:

        #Only read first two cols of file
        data = data[:,:2]

        #Remove duplicate time values (if they exist) and resort
        _, indices = np.unique(data[:, 0], return_index=True)
        data = data[indices, :]

        times, values = data.T
        full_ts = ats.ArrayTimeSeries(times=times,values=values)
        interpolated_ts = full_ts.interpolate(np.arange(0.0, 1.0, (1.0 /100)))
        return interpolated_ts


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

def search_vpdb(vp_t,input_ts):
    dist_to_vp, vp_id = vp_t
    print(vp_id,dist_to_vp)
    print(vp_id)
    db_path = DB_DIR + vp_id[:-4] + ".dbdb"
    print(db_path)
    db = unbalancedDB.connect(DB_DIR + vp_id[:-4] + ".dbdb")
    x = db.chop(dist_to_vp)
    print(len(x))
    #x = sorted(x)
    min_dist = dist_to_vp
    min_dist_ts_id = vp_id
    min_ts = load_ts(vp_id)
    for i in x:
        ts2 = load_ts(i[1])
        distance = (kernel_dist(input_ts,ts2))
        if (distance < min_dist):
            min_dist = distance
            min_dist_ts_id = i[1]
            min_ts = ts2

    db.close()
    return(min_dist,min_dist_ts_id,min_ts)


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
            if '.txt' in arg.lower() or '.dat_folded' in arg.lower()  :
                have_input = True
                input_path = arg
            else:
                print("Error: no compatible input file provided.")
                print("Usage: ./similarsearch input.txt  [optional flags]")
                break

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
                    vp_distances.append((kernel_dist(input_ts, vps_dict[k]),k))

            vp_distances = sorted(vp_distances)
            closest_vp = vp_distances[0]
            print("Closest vp:", closest_vp)
            d, ts2_id, ts2 = search_vpdb(closest_vp,input_ts)

            import matplotlib.pyplot as plt
            standts1 = standardize(input_ts, input_ts.mean(), input_ts.std())
            standts2 = standardize(ts2, ts2.mean(), ts2.std())
            plt.plot(standts1, label=input_path)
            plt.plot(standts2, label=ts2_id)
            plt.legend()
            plt.show()
            break
        else:
            break

