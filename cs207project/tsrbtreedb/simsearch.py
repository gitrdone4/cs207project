#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# CS207 Group Project Part 7
# Created by Team 2 (Jonne Seleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah) for Team 4

import sys
import os
import numpy as np
import random

from cs207project.tsrbtreedb.crosscorr import standardize, kernel_dist
from cs207project.tsrbtreedb.makelcs import make_lcs_wfm
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
from cs207project.rbtree.redblackDB import connect
from cs207project.storagemanager.filestoragemanager import FileStorageManager
import cs207project.timeseries.arraytimeseries as ats

# Global variables

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, SAMPLE_DIR, TS_LENGTH

HELP_MESSAGE = \
"""
Light Curve Similarity Search

A python command line utility to searching for similar light curves.
Usage: ./simsearch input.txt  [optional flags]

Optional flags:
  -h, --help        Show this help message and exit.
  -p, --plot        Plot submitted light curve with most similar curve in database
  -r, --rebuild     Recreates light curve files vantage point indexes (Run automatically on first use)
  -d, --demo        Loads a random time series from sample data folder and runs similarity search

"""
USAGE = "Usage: ./simsearch input_ts.txt [optional flags]"

def load_nparray(filepath):
    """Helper to load space delimited nparray from disk"""
    try:
        nparray = np.loadtxt(filepath)
    except(IOError):
        raise IOError("Unable to load np array %s" % filepath)
    else:
        return nparray


def load_ts(ts_id,fsm):
    """Helper to load previously generated ts file from disk"""
    if ts_id.startswith("ts_datafile"):
        return fsm.get(ts_id)
    else:
        raise ValueError("'%s' does not appear to be a time series file" % ts_id)

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

def load_vp_lcs(db_dir,lc_dir):
    """
    Based on names of vantage point db files loads and returns time series curves
    of identified vantage points from disk
    """
    vp_dict= {}
    fsm = FileStorageManager(lc_dir)

    for file in os.listdir(db_dir):
        if file.startswith("ts_datafile_") and file.endswith(".dbdb"):
            lc_id = file[:-5]
            vp_dict[lc_id] = load_ts(lc_id,fsm)
    #print("Loaded %d vp files" % len(vps_dict))
    return vp_dict

def find_closest_vp(vps_dict, ts):
    """
    Calculates distances from ts to all vantage points.
    Returns tuple with filename of closest vantage point and distance to that vantage point.
    """
    s_ts = standardize(ts)
    vp_distances = sorted([(kernel_dist(s_ts, standardize(vps_dict[vp])),vp) for vp in vps_dict])
    dist_to_vp, vp_fn = vp_distances[0]
    return (vp_fn,dist_to_vp)

def search_vpdb(vp_t,ts,db_dir,lc_dir):
    """
    Searches for most similar light curve based on pre-computed distances in vpdb

    Args:
        vp_t: tuple containing vantage point filename and distance of time series to vantage point
        ts: time series to search on.
    Returns:
        Tuple: Distance to closest light curve, filename of closest light curve, ats object for closest light curve

    """

    fsm = FileStorageManager(lc_dir)

    vp_fn, dist_to_vp = vp_t
    db_path = db_dir + vp_fn + ".dbdb"
    db = connect(db_dir + vp_fn + ".dbdb")
    s_ts = standardize(ts)

    # Identify light curves in selected vantage db that are up to 2x the distance
    # that the time series is from the vantage point
    lc_candidates = db.chop(2 * dist_to_vp)
    db.close()

    # Vantage point is ts to beat as we search through candidate light curves
    min_dist = dist_to_vp
    closest_ts_fn = vp_fn
    closest_ts = load_ts(vp_fn,fsm)

    for d_to_vp,ts_fn in lc_candidates:
        candidate_ts = load_ts(ts_fn,fsm)
        dist_to_ts = kernel_dist(standardize(candidate_ts),s_ts)
        if (dist_to_ts < min_dist):
            min_dist = dist_to_ts
            closest_ts_fn = ts_fn
            closest_ts = candidate_ts

    return(min_dist,closest_ts_fn,closest_ts)

def need_to_rebuild(lc_dir,db_dir):
    """Helper to determine whether required lc files and database files already exist or need to be generated"""

    # If either of the folders do not exists, we need to rebuild
    if not (os.path.isdir(lc_dir)):
        return True
    if not (os.path.isdir(db_dir)):
        return True

    # Count correctly named lc files in lc dir
    lc_files = 0
    for file in os.listdir(lc_dir):
        if file.startswith("ts_datafile") and file.endswith(".npy"):
            lc_files +=1

    if lc_files < 10:
        return True

    vpdb_files = 0
    for file in os.listdir(db_dir):
        if file.startswith("ts_datafile") and file.endswith(".dbdb"):
            vpdb_files += 1

    if vpdb_files < 5:
        return True

    # If everything above evals to false, then we (probably) don't need to rebuild
    return False

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

def rebuild_lcs_dbs(lc_dir,db_dir,n_vps= 20, n_lcs = 1000):
    """Calls functions to regenerate light curves and rebuild vp indexes"""
    print("\nRebuilding simulated light curves and vantage point index files....\n(This may take up to 30 seconds)")
    make_lcs_wfm(n_lcs, lc_dir)
    create_vpdbs(n_vps,lc_dir,db_dir)
    print("Indexes rebuilt.\n")

def run_demo(db_dir,lc_dir,plot=False):
    """Loads a random time series from sample data folder and runs similarity search"""
    demo_ts_fn = random.choice(os.listdir(SAMPLE_DIR))
    sim_search(SAMPLE_DIR + demo_ts_fn,db_dir,lc_dir,plot)

def sim_search(input_fpath,db_dir,lc_dir,plot=False):
    """Executes similarity search on submitted time series files"""
    print("Loading %s..." % input_fpath,end="")
    input_ts = load_external_ts(input_fpath)
    print("Done.")
    closest_vp = find_closest_vp(load_vp_lcs(db_dir,lc_dir), input_ts)
    #print(closest_vp)
    min_dist,closest_ts_fn,closest_ts = search_vpdb(closest_vp,input_ts,db_dir,lc_dir)
    print("\n============================ Results ============================")
    print("%s is the closest light curve to %s" % (closest_ts_fn, input_fpath))
    print("Distance from %s to %s: %.5f" % (input_fpath, closest_ts_fn, min_dist))
    if plot:
        plot_two_ts(input_ts,input_fpath,closest_ts,closest_ts_fn)

if __name__ == "__main__":
    """
    Main program loop. Determines which flags were submitted, confirms that lc files and db files
    exist (Recreates them if they don't) before kicking off similarity search.
    """

    # Default conditions
    rebuild = need_to_rebuild(LIGHT_CURVES_DIR,DB_DIR)
    need_help = False
    input_fpath = False
    plot = False
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
            rebuild_lcs_dbs(LIGHT_CURVES_DIR,DB_DIR)

        if demo:
            run_demo(DB_DIR,LIGHT_CURVES_DIR,plot)
            break

        elif(input_fpath is not False):
            sim_search(input_fpath,DB_DIR,LIGHT_CURVES_DIR,plot)
            break
        else:
            print("Error: no compatible time series or light curve file provided")
            print(USAGE)
            break

