#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import random

from crosscorr import standardize, kernal_dist
import unbalancedDB

# This is a hacky solution to import the array time series class from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')
import arraytimeseries as ats

# Global variables

HELP_MESSAGE = \
"""
Light Curve Similarity Search

A python command line utility to searching for similar light curves.
Usage: ./simsearch input.txt  [optional flags]

Optional flags:
  -h, --help    Show this help message and exit.
  -p, --plot    Plot submitted light curve with most similar curve in database
  -r, --rebuild   Recreate light curve database (Run automatically on first use)
  -d, --demo  Run search on demo light curve data

"""
USAGE = "Usage: ./simsearch input_ts.txt [optional flags]"
LIGHT_CURVES_DIR = "light_curves/"
DB_DIR = "vp_dbs/"
SAMPLE_DIR = "sample_data/"
TEMP_DIR = "temp/"
TS_LENGTH = 100 #Number of data points for generated time series

def load_nparray(filepath):
    """Helper to load space delimited nparray from disk"""
    try:
        nparray = np.loadtxt(filepath)
    except(IOError):
        raise IOError("Unable to load np array %s" % filepath)
    else:
        return nparray

def load_ts(ts_fname):
    """Helper to load previously generated ts file from disk"""
    if ts_fname.startswith("ts-"):
        filepath = LIGHT_CURVES_DIR + ts_fname
        data = load_nparray(filepath)
        times, values = data.T
        return ats.ArrayTimeSeries(times=times,values=values)
    else:
        raise ValueError("'%s' does not appear to be a time series file" % ts_fname)

def load_external_ts(filepath):
    """
    Loads space delimited time series text file from disk to be searched on.

    Args:
        filepath: path to time series file
    Returns:
        A 100 point interpolated ArrayTimeSeries object for times between 0 and 1.
    Notes:
        - Only considers the first two columns of the text file (other columns are discarded)
        - Only evaluates time values between 0 and 1
        - First column is presumed to be times and second column is presumed to be light curve values.
    """
    data = load_nparray(filepath)
    data = data[:,:2] # truncate to first 2 cols

    # Remove rows with duplicate time values (if they exist) and resorts to ensure ts in ascending order
    _, indices = np.unique(data[:, 0], return_index=True)
    data = data[indices, :]

    times, values = data.T
    full_ts = ats.ArrayTimeSeries(times=times,values=values)
    interpolated_ats = full_ts.interpolate(np.arange(0.0, 1.0, (1.0 /TS_LENGTH)))
    return interpolated_ats

def load_vp_lcs():
    """
    Based on names of vantage point db files loads and returns time series curves
    of identified vantage points from disk
    """
    vp_dict= {}
    for file in os.listdir(DB_DIR):
        if file.startswith("ts-") and file.endswith(".dbdb"):
            lc_id = file[:-5] + '.txt'
            vp_dict[lc_id] = load_ts(lc_id)
    #print("Loaded %d vp files" % len(vps_dict))
    return vp_dict

def find_closest_vp(vps_dict, ts):
    """
    Calculates distances from ts to all vantage points.
    Returns tuple with filename of closest vantage point and distance to that vantage point.
    """
    s_ts = standardize(ts)
    vp_distances = sorted([(kernal_dist(s_ts, standardize(vps_dict[vp])),vp) for vp in vps_dict])
    dist_to_vp, vp_fn = vp_distances[0]
    return (vp_fn,dist_to_vp)

def search_vpdb(vp_t,ts):
    """
    Searches for most similar light curve based on pre-computed distances in vpdb

    Args:
        vp_t: tuple containing vantage point filename and distance of time series to vantage point
        ts: time series to search on.
    Returns:
        Tuple: Distance to closest light curve, filename of closest light curve, ats object for closest light curve

    """

    vp_fn, dist_to_vp = vp_t
    db_path = DB_DIR + vp_fn[:-4] + ".dbdb"
    db = unbalancedDB.connect(DB_DIR + vp_fn[:-4] + ".dbdb")
    s_ts = standardize(ts)

    # Identify light curves in selected vantage db that are up to 2x the distance
    # that the time series is from the vantage point
    lc_candidates = db.chop(2 * dist_to_vp)
    db.close()

    # Vantage point is ts to beat as we search through candidate light curves
    min_dist = dist_to_vp
    closest_ts_fn = vp_fn
    closest_ts = load_ts(vp_fn)

    for d_to_vp,ts_fn in lc_candidates:
        candidate_ts = load_ts(ts_fn)
        dist_to_ts = kernal_dist(standardize(candidate_ts),s_ts)
        if (dist_to_ts < min_dist):
            min_dist = dist_to_ts
            closest_ts_fn = ts_fn
            closest_ts = candidate_ts

    return(min_dist,closest_ts_fn,closest_ts)

def plot_two_ts(ts1,ts1_name,ts2,ts2_name,stand=True):
    """Plots two time series with matplotlib"""
    import matplotlib.pyplot as plt
    if (stand):
        ts1 = standardize(ts1)
        ts2 = standardize(ts2)
    plt.plot(ts1, label=ts1_name)
    plt.plot(ts2, label=ts2_name)
    plt.legend()
    plt.show()

def rebuild():
    pass

def run_demo(plot=False):
    demo_ts_fn = random.choice(os.listdir(SAMPLE_DIR))

    sim_search(SAMPLE_DIR + demo_ts_fn,plot)

def sim_search(input_fpath,plot=False):
    print("Loading %s" % input_fpath)
    input_ts = load_external_ts(input_fpath)
    closest_vp = find_closest_vp(load_vp_lcs(), input_ts)

    min_dist,closest_ts_fn,closest_ts = search_vpdb(closest_vp,input_ts)

    print("Closest light curve to %s: %s" % (input_fpath, closest_ts_fn))
    print("Distance from %s to %s: %.5f" % (input_fpath, closest_ts_fn, min_dist))
    if plot:
        plot_two_ts(input_ts,input_fpath,closest_ts,closest_ts_fn)

if __name__ == "__main__":
    """
    Main program loop. Determines which flags were submitted, confirms that lc files and db files
    exist (Recreates them if they don't) before kicking off similarity search.
    """

    need_help = False
    input_fpath = False
    plot = False
    rebuild = False
    demo = False

    while(True):
        if len(sys.argv) <= 1:
            print("No arguments provided")
            print(USAGE)
            break

        # First, identify which flags were included
        for arg in sys.argv[1:]:
            if arg.lower() in ['-h','--help', 'help']: need_help = True

            elif '.txt' in arg.lower() or '.dat_folded' in arg.lower():
                input_fpath = arg

            elif arg.lower() in ['-r','--rebuild']: rebuild = True
            elif arg.lower() in ['-d','--demo']: demo = True
            elif arg.lower() in ['-p','--plot']: plot = True

        # Execute selected options
        if need_help:
            print (HELP_MESSAGE)
            break
        elif rebuild:
            rebuild()

        if demo:
            run_demo(plot)
            break

        elif(input_fpath is not False):
            sim_search(input_fpath,plot)
            break
        else:
            print("Error: no compatible time series or light curve file provided")
            print(USAGE)
            break

