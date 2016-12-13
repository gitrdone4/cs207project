#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
genvpdbs.py contains the functions generate vantage point DBs from light-curve files.

"""

import sys
import os
import random
import numpy as np
from concurrent.futures import ProcessPoolExecutor

from cs207project.rbtree.redblackDB import connect
from cs207project.tsrbtreedb.crosscorr import kernel_dist, standardize
from cs207project.tsrbtreedb.makelcs import clear_dir
from cs207project.storagemanager.filestoragemanager import FileStorageManager
from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH
import cs207project.timeseries.arraytimeseries as ats

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

def save_vp_dbs(vp_tuple):
    """ Creates unbalanced binary tree databases and saves them to disk"""

    vp,timeseries_dict, DB_DIR = vp_tuple
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
    Create Vantage point databases in parallel

    Executes functions above:
        (1) Creates timeseries_dict from time series files on disk
        (2) Picks 20 vantage points at random
        (3) Using a process poll for parallelization, calculates kernel distance between vantage points and generated time series
        (4) Saves kernel distance indexes to disk as red-black tree databases
    """
    print("Creating %d vantage point dbs" % n,end="")
    timeseries_dict = load_ts_fsm(lc_dir)
    vantage_points = pick_vantage_points(timeseries_dict,n)
    clear_dir(db_dir)

    # This is in elegant, but needed to use the map function below where
    # we can effectually only pass one augment to the worker process
    vp_tuples = [(vp,timeseries_dict,db_dir) for vp in vantage_points]

    # build vantage point dbs in parallel (up to the number of processes on your machine)
    with ProcessPoolExecutor() as pool:
        results = pool.map(save_vp_dbs,vp_tuples)

    print("....................Done.")
