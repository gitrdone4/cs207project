#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
Light Curve Similarity Search

A python command line utility to searching for similar light curves.
Usage: ./simsearchutil.py input.txt  [optional flags]

Optional flags:
  -h, --help        Show this help message and exit.
  -p, --plot        Plot submitted light curve with most similar curve in database
  -r, --rebuild     Recreates light curve files vantage point indexes (Run automatically on first use)
  -d, --demo        Loads a random time series from sample data folder and runs similarity search

"""

import sys
import os
import random

from cs207project.tsrbtreedb.crosscorr import standardize, kernel_dist
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
import cs207project.timeseries.arraytimeseries as ats
from cs207project.tsrbtreedb.simsearch import need_to_rebuild, rebuild_lcs_dbs, \
					load_external_ts, find_closest_vp, load_vp_lcs,search_vpdb

# Global variables

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, SAMPLE_DIR

HELP_MESSAGE = \
"""
Light Curve Similarity Search

A python command line utility to searching for similar light curves.
Usage: ./simsearchutil.py input.txt  [optional flags]

Optional flags:
  -h, --help        Show this help message and exit.
  -p, --plot        Plot submitted light curve with most similar curve in database
  -r, --rebuild     Recreates light curve files vantage point indexes (Run automatically on first use)
  -d, --demo        Loads a random time series from sample data folder and runs similarity search

"""
USAGE = "Usage: ./simsearchutil.py input_ts.txt [optional flags]"


def plot_two_ts(ts1, ts1_name, ts2, ts2_name, stand=True):
    """Plots two time series with matplotlib"""
    import matplotlib.pyplot as plt
    if stand:
        ts1 = standardize(ts1)
        ts2 = standardize(ts2)
    plt.plot(ts1, label=ts1_name)
    plt.plot(ts2, label=ts2_name)
    plt.legend()
    plt.show()

def run_demo(db_dir, lc_dir, plot=False):
    """Loads a random time series from sample data folder and runs similarity search"""
    demo_ts_fn = random.choice(os.listdir(SAMPLE_DIR))
    sim_search(SAMPLE_DIR + demo_ts_fn,db_dir,lc_dir,plot)

def sim_search(input_fpath, db_dir, lc_dir, plot=False):
    """Executes similarity search on submitted time series files"""
    print("Loading %s..." % input_fpath, end="")
    input_ts = load_external_ts(input_fpath)
    print("Done.")
    closest_vp = find_closest_vp(load_vp_lcs(db_dir, lc_dir), input_ts)
    #print(closest_vp)
    min_dist, closest_ts_fn, closest_ts = search_vpdb(closest_vp, input_ts, db_dir, lc_dir)
    print("\n============================ Results ============================")
    print("%s is the closest light curve to %s" % (closest_ts_fn, input_fpath))
    print("Distance from %s to %s: %.5f" % (input_fpath, closest_ts_fn, min_dist))
    if plot:
        plot_two_ts(input_ts, input_fpath, closest_ts, closest_ts_fn)

if __name__ == "__main__":
    """
    Main program loop. Determines which flags were submitted, confirms that lc files and db files
    exist (Recreates them if they don't) before kicking off similarity search.
    """

    # Default conditions
    rebuild = need_to_rebuild(LIGHT_CURVES_DIR, DB_DIR)
    need_help = False
    input_fpath = False
    plot = False
    demo = False

    while True:
        if len(sys.argv) <= 1:
            print("No arguments provided")
            print(USAGE)
            break

        # First, identify which flags were included
        for arg in sys.argv[1:]:
            if arg.lower() in ['-h','--help', 'help']: need_help = True

            elif '.txt' in arg.lower() or '.dat_folded' in arg.lower():
                input_fpath = arg

            elif arg.lower() in ['-r', '--rebuild']: rebuild = True
            elif arg.lower() in ['-d', '--demo']: demo = True
            elif arg.lower() in ['-p', '--plot']: plot = True

        # Execute selected options
        if need_help:
            print(HELP_MESSAGE)
            break
        elif rebuild:
            rebuild_lcs_dbs(LIGHT_CURVES_DIR, DB_DIR)

        if demo:
            run_demo(DB_DIR, LIGHT_CURVES_DIR, plot)
            break

        elif(input_fpath is not False):
            sim_search(input_fpath, DB_DIR, LIGHT_CURVES_DIR, plot)
            break
        else:
            print("Error: no compatible time series or light curve file provided")
            print(USAGE)
            break
