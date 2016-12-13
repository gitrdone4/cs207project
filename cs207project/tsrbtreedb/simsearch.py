#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import random
import heapq

from cs207project.tsrbtreedb.crosscorr import standardize, kernel_dist
from cs207project.tsrbtreedb.makelcs import make_lcs_wfm
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
from cs207project.rbtree.redblackDB import connect
from cs207project.storagemanager.filestoragemanager import FileStorageManager
import cs207project.timeseries.arraytimeseries as ats

# Global variables

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, SAMPLE_DIR, TS_LENGTH, tsfn_to_id


def load_nparray(filepath):
    """Helper to load space delimited nparray from disk"""
    try:
        nparray = np.loadtxt(filepath)
    except(IOError):
        raise IOError("Unable to load np array %s" % filepath)
    else:
        return nparray


def load_ts(ts_id,fsm):
    """Helper to load previously generated ts file from disk vis fsm"""
    ts = fsm.get(ts_id)
    if ts is not None:
        return ts
    else:
        raise ValueError("time series '%s' does not appear to be in the database" % ts_id)

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


def add_ts_to_vpdbs(ts,ts_fn,db_dir,lc_dir):
    """
    Based on names of vantage point db files, adds single new time seires to vp indexes
    """
    vp_dict= {}
    fsm = FileStorageManager(lc_dir)

    s_ts = standardize(ts)

    for file in os.listdir(db_dir):
        if file.startswith("ts_datafile_") and file.endswith(".dbdb"):
            vp_ts = load_ts(file[:-5],fsm)
            dist_to_vp = kernel_dist(standardize(vp_ts),s_ts)
            # print("Adding " + ts_fn + " to " + (db_dir + file))
            db = connect(db_dir + file)
            db.set(dist_to_vp,ts_fn)
            db.commit()
            db.close()

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


def find_lc_candidates(vp_t,ts,db_dir,lc_dir):
    fsm = FileStorageManager(lc_dir)

    vp_fn, dist_to_vp = vp_t
    db_path = db_dir + vp_fn + ".dbdb"
    db = connect(db_dir + vp_fn + ".dbdb")

    # Identify light curves in selected vantage db that are up to 2x the distance
    # that the time series is from the vantage point
    lc_candidates = db.chop(2 * dist_to_vp)
    db.close()

    return (lc_candidates,fsm)

def search_vpdb(vp_t,ts,db_dir,lc_dir):
    """
    Searches for most similar light curve based on pre-computed distances in vpdb

    Args:
        vp_t: tuple containing vantage point filename and distance of time series to vantage point
        ts: time series to search on.
    Returns:
        Tuple: Distance to closest light curve, filename of closest light curve, ats object for closest light curve

    """
    vp_fn, dist_to_vp = vp_t
    lc_candidates,fsm = find_lc_candidates(vp_t,ts,db_dir,lc_dir)
    s_ts = standardize(ts)

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

def ts_already_exists(ts,db_dir,lc_dir):
    """
    Searches database to see if time series already exists

    Returns tsid if it finds a matching time series, -1 otherwise

    """
    s_ts = standardize(ts)

    vp_t = find_closest_vp(load_vp_lcs(db_dir,lc_dir),ts)
    vp_fn, dist_to_vp = vp_t
    lc_candidates,fsm = find_lc_candidates(vp_t,ts,db_dir,lc_dir)
    lc_candidates.append((0,vp_fn))
    existing_ts_id = -1

    for d_to_vp,ts_fn in lc_candidates:
        candidate_ts = load_ts(ts_fn,fsm)
        dist_to_ts = kernel_dist(standardize(candidate_ts),s_ts)

        if dist_to_ts < .00001:
            existing_ts_id = tsfn_to_id(ts_fn)
            break

    return existing_ts_id

def search_vpdb_for_n(vp_t,ts,db_dir,lc_dir,n):
    """
    Searches for n most similar light curve based on pre-computed distances in vpdb

    Args:
        vp_t: tuple containing vantage point filename and distance of time series to vantage point
        ts: time series to search on.
    Returns:
        Dict: A dict of n closet time series ids, with distances as the keys and ts ids as the values

    """

    s_ts = standardize(ts)
    vp_fn, dist_to_vp = vp_t
    lc_candidates,fsm = find_lc_candidates(vp_t,ts,db_dir,lc_dir)
    lc_candidates.append((0,vp_fn))

    dist_list = []

    existing_ts_id = -1

    for d_to_vp,ts_fn in lc_candidates:
        candidate_ts = load_ts(ts_fn,fsm)
        dist_to_ts = kernel_dist(standardize(candidate_ts),s_ts)

        if dist_to_ts < .00001:
            existing_ts_id = tsfn_to_id(ts_fn)
        else:
            dist_list.append((dist_to_ts,tsfn_to_id(ts_fn)))

    return (dict(heapq.nsmallest(n, dist_list)),existing_ts_id)

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


def rebuild_lcs_dbs(lc_dir,db_dir,n_vps= 20, n_lcs = 1000):
    """Calls functions to regenerate light curves and rebuild vp indexes"""
    print("\nRebuilding simulated light curves and vantage point index files....\n(This may take up to 30 seconds)")
    make_lcs_wfm(n_lcs, lc_dir)
    create_vpdbs(n_vps,lc_dir,db_dir)
    print("Indexes rebuilt.\n")


