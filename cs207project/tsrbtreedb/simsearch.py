#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
simsearch.py contains the main functions for creating, adding, and searching the light curve databases.

"""

import os
import heapq
from concurrent.futures import ProcessPoolExecutor
import numpy as np

from cs207project.tsrbtreedb.crosscorr import standardize, kernel_dist
from cs207project.tsrbtreedb.makelcs import make_lcs_wfm
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
from cs207project.rbtree.redblackDB import connect
from cs207project.storagemanager.filestoragemanager import FileStorageManager
import cs207project.timeseries.arraytimeseries as ats

# Global variables

from cs207project.tsrbtreedb.settings import TS_LENGTH, tsfn_to_id, tsid_to_fn

# Helper functions

def load_nparray(filepath):
    """Helper to load space delimited nparray from disk"""
    try:
        nparray = np.loadtxt(filepath)
    except(IOError):
        raise IOError("Unable to load np array %s" % filepath)
    else:
        return nparray

def load_ts(ts_id, fsm):
    """Helper to load previously generated ts file from disk with fsm"""
    ts = fsm.get(ts_id)
    if ts is not None:
        return ts
    else:
        raise ValueError("time series '%s' does not appear to be in the database" % ts_id)

def load_ts_wo_fm(ts_id,lc_dir):
    """Wraps load_ts above for functions that don't already have a file manager object"""
    fsm = FileStorageManager(lc_dir)
    return load_ts(ts_id,fsm)

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

def ts_already_exists(ts, db_dir, lc_dir):
    """
    Helper that search ts database to see if time series already exists

    Returns tsid (e.g., 456) if it finds a matching time series, -1 otherwise
    """
    vp_t = find_closest_vp(load_vp_lcs(db_dir,lc_dir),ts)
    _ ,existing_ts_id = search_vpdb_for_n(vp_t, ts, db_dir, lc_dir, 5)

    return existing_ts_id

def need_to_rebuild(lc_dir, db_dir):
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

def rebuild_lcs_dbs(lc_dir, db_dir, n_vps=20, n_lcs=1000):
    """Calls functions to regenerate light curves and rebuild vp indexes"""
    print("\nRebuilding simulated light curves and vantage point index files....\n(This may take up to 30 seconds)")
    make_lcs_wfm(n_lcs, lc_dir)
    create_vpdbs(n_vps,lc_dir,db_dir)
    print("Indexes rebuilt.\n")

# Main functions for similarity search

def search_vpdb_for_n(vp_t, ts, db_dir, lc_dir, n):
    """
    Searches for n most similar light curve based on pre-computed distances in vpdb

    Args:
        vp_t: tuple containing vantage point filename and distance of time series to vantage point
        ts: time series to search on.
    Returns:
        Dict: A dict of n closet time series ids, with distances as the keys and ts ids as the values

    Note:
        Uses processes pool to calculate distances in parallel, and heap queue data to minimize time
        for sorting final distance list to n smallest distances.
    """

    # 1. Setup data to be processed in parallel
    vp_fn, dist_to_vp = vp_t
    lc_candidates,fsm = find_lc_candidates(vp_t,db_dir,lc_dir)
    lc_candidates.append((dist_to_vp,vp_fn))
    existing_ts_id = -1
    s_ts = standardize(ts)

    lc_candidate_data = [(ts_fn,fsm,s_ts) for d_to_vp,ts_fn in lc_candidates]

    # 2. Calculate distances in parallel
    with ProcessPoolExecutor() as pool:
        dist_list = pool.map(calc_distance, lc_candidate_data)

    # 3. Sort distances for n+1 smallest
    n_smallest = heapq.nsmallest(n+1, dist_list)

    # 4. Look through sublist of closest time series to see if any of have a distance of zero.
    # If so, mark it as an existing time series.
    # Otherwise, trim the list by 1.
    for dist_to_ts,tsid in n_smallest:
        if dist_to_ts < .00001:
            existing_ts_id = tsid

    if (existing_ts_id == -1):
        n_smallest = n_smallest[:-1]
    else:
        n_smallest = [(d,id) for d,id in n_smallest if (id != existing_ts_id)]

    # 5. Return n_smallest dict, and exiting id (or -1 if not in db)
    return (dict(n_smallest),existing_ts_id)

def calc_distance(lc_candidate_data):
    """Working function called by search_vpdb_for_n above"""
    ts_fn,fsm,s_ts = lc_candidate_data
    candidate_ts = load_ts(ts_fn,fsm)
    dist_to_ts = kernel_dist(standardize(candidate_ts),s_ts)
    return(dist_to_ts,tsfn_to_id(ts_fn))


def add_ts_to_vpdbs(ts, ts_fn, db_dir, lc_dir):
    """
    Based on names of vantage point db files, adds single new time series to vp indexes
    (Does not re-pick vantage points)

    Uses ProcessPoolExecutor to run in parallel.
    """

    fsm = FileStorageManager(lc_dir)
    s_ts = standardize(ts)

    # Setup data for process poll execution
    vp_fns  = [file for file in os.listdir(db_dir) if file.startswith("ts_datafile_") and file.endswith(".dbdb")]
    vp_tuples = [(vp_fn,fsm,s_ts,ts_fn,db_dir) for vp_fn in vp_fns]

    # Create processes
    with ProcessPoolExecutor() as pool:
        _ = pool.map(add_ts_to_vpdb,vp_tuples)

def add_ts_to_vpdb(data_tuple):
    """
    Worker function called by add_ts_to_vpdbs above.
    This process is repeated on each vantage point.
    """
    file,fsm,s_ts,ts_fn,db_dir = data_tuple
    vp_ts = load_ts(file[:-5],fsm)
    dist_to_vp = kernel_dist(standardize(vp_ts), s_ts)
    # print("Adding " + ts_fn + " to " + (db_dir + file))
    db = connect(db_dir + file)
    db.set(dist_to_vp,ts_fn)
    db.commit()
    db.close()


def load_vp_lcs(db_dir, lc_dir):
    """
    Based on names of vantage point db files loads and returns time series curves
    of identified vantage points from disk
    """
    vp_dict={}
    fsm = FileStorageManager(lc_dir)

    for file in os.listdir(db_dir):
        if file.startswith("ts_datafile_") and file.endswith(".dbdb"):
            lc_id = file[:-5]
            vp_dict[lc_id] = load_ts(lc_id, fsm)

    return vp_dict

def find_closest_vp(vps_dict, ts):
    """
    Calculates distances from time series to all vantage points.
    Returns tuple with filename of closest vantage point and distance to that vantage point.
    """
    s_ts = standardize(ts)
    vp_distances = sorted([(kernel_dist(s_ts, standardize(vps_dict[vp])),vp) for vp in vps_dict])
    dist_to_vp, vp_fn = vp_distances[0]
    return (vp_fn,dist_to_vp)

def find_lc_candidates(vp_t, db_dir, lc_dir):
    """
    Identifies light curves in selected vantage db that are up to 2x the distance
    that the time series is from the vantage point

    Returns tuple with list of light curve candidates and file storage manager object
    """

    fsm = FileStorageManager(lc_dir)

    vp_fn, dist_to_vp = vp_t

    db = connect(db_dir + vp_fn + ".dbdb")
    lc_candidates = db.chop(2 * dist_to_vp)
    db.close()

    return (lc_candidates,fsm)

def search_vpdb(vp_t, ts, db_dir, lc_dir):
    """
    Searches for most *single* most similar light curve based on pre-computed distances in vpdb

    Used by command line utility (not by Rest API)

    Args:
        vp_t: tuple containing vantage point filename and distance of time series to vantage point
        ts: time series to search on.
    Returns:
        Tuple: Distance to closest light curve, filename of closest light curve, ats object for closest light curve

    """
    n_smallest_d,_ = search_vpdb_for_n(vp_t, ts, db_dir, lc_dir, 1)
    min_dist,closest_tsid = [(k,n_smallest_d[k]) for k in n_smallest_d][0]

    closest_ts_fn = tsid_to_fn(closest_tsid)
    closest_ts = load_ts_wo_fm(closest_ts_fn,lc_dir)
    return(min_dist,closest_ts_fn + '.npy',closest_ts)

if __name__ == "__main__":
    """Activate command line util in simsearchutil if run directly"""
    from cs207project.tsrbtreedb.simsearchutil import cmd_line_util
    cmd_line_util()
