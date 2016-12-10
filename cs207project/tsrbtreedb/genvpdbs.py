#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import sys
import os
import random
import numpy as np

from cs207project.rbtree.redblackDB import connect
from cs207project.tsrbtreedb.crosscorr import kernel_dist, standardize
from cs207project.tsrbtreedb.makelcs import clear_dir
from cs207project.storagemanager.filestoragemanager import FileStorageManager
from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH
import cs207project.timeseries.arraytimeseries as ats

# Global variables

HELP_MESSAGE = \
"""
Generate Vantage Point Index DBs

A python command line utility to generate vantage point DBs from light-curve files.

Usage: ./genvpdbs  [optional flags]

Optional flags:
  -h, --help    Show this help message and exit.
"""

def load_ts_fsm(lc_dir):
    """Loads time series from fsm; returns dict keyed to filename"""
    timeseries_dict = {}
    fsm = FileStorageManager(lc_dir)

    for i in fsm.get_ids():
        timeseries_dict[i] = fsm.get(i)

    return timeseries_dict

def pick_vantage_points(timeseries_dict,n=20):
    """Selects n light curves at random to serve as vantage points"""
    return random.sample(timeseries_dict.keys(), n)

def calc_distances(vp_k,timeseries_dict):
    """Calculates kernel distance between vantage point and all loaded light curves"""
    distances = []
    vp = standardize(timeseries_dict[vp_k])
    for k in timeseries_dict:
        if k != vp_k:
            k_dist = kernel_dist(vp, standardize(timeseries_dict[k]))
            distances.append((k_dist,k))
    return distances

def save_vp_dbs(vp,timeseries_dict, DB_DIR):
    """ Creates unbalanced binary tree databases and saves them to disk"""
    sorted_ds = calc_distances(vp,timeseries_dict)

    # ts_datafile_51 -> vp_dbs/ts_datafile_51.dbdb
    db_filepath = DB_DIR + vp + ".dbdb"
    db = connect(db_filepath)

    for dist_to_vp,ts_fn in sorted_ds:
        db.set(dist_to_vp, ts_fn)

    db.commit()
    db.close()

def create_vpdbs(n,lc_dir,db_dir):
    """
    Executes functions above:
        (1) Creates timeseries_dict from time series files on disk
        (2) Picks 20 vantage points at random
        (3) Calculates kernel distance between vantage points and generated time series (This can take a while)
        (4) Saves kernel distance indexes to disk as binary tree databases
    """
    print("Creating %d vantage point dbs" % n,end="")
    timeseries_dict = load_ts_fsm(lc_dir)
    vantage_points = pick_vantage_points(timeseries_dict,n)
    clear_dir(db_dir)
    for vp in vantage_points:
        print('.', end="")
        save_vp_dbs(vp,timeseries_dict,db_dir)
    print("Done.")

# if __name__ == "__main__":
#     """Enables this file to be run independently of simsearch as it's own CLU."""
#     need_help = False

#     # First, identify which flags were included
#     for arg in sys.argv[1:]:
#         if arg.lower() in ['-h','--help', 'help']: need_help = True

#     while(True):
#         if need_help:
#             print (HELP_MESSAGE)
#             break
#         else:
#             print("Starting...(May take a little while)")
#             create_vpdbs(20,LIGHT_CURVES_DIR,DB_DIR)
#             break
