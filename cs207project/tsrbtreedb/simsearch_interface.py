#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import cs207project.tsrbtreedb.simsearch as simsearch
import numpy as np
from cs207project.storagemanager.filestoragemanager import FileStorageManager
from cs207project.tsrbtreedb.makelcs import clear_dir
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
from cs207project.timeseries.arraytimeseries import ArrayTimeSeries
from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH, SAMPLE_DIR,tsid_to_fn,tsfn_to_id

def rebuild_if_needed(lc_dir,db_dir,n_vps=20,n_lcs=1000):
    """
    Helper that checks if needed time series files & vantage point databases already exists
    recreates them if they don't.
    """
    if (simsearch.need_to_rebuild(lc_dir,db_dir)):
        simsearch.rebuild_lcs_dbs(lc_dir,db_dir, n_vps=n_vps, n_lcs=n_lcs)

def sanitize_ats(ats):
    interpolated_ats = ats.interpolate(np.arange(0.0, 1.0, (1.0 /TS_LENGTH)))
    return interpolated_ats

def add_ts_wfm(ts,fsm):
    """
    Save new time series to disk, and updates vantage point databases

    Returns newly created ts id, or existing id if previously saved.

    """
    interpolated_ats = sanitize_ats(ts)

    # check if ts already exists in db
    tsid = simsearch.ts_already_exists(interpolated_ats,DB_DIR,LIGHT_CURVES_DIR)

    if tsid == -1: #Save new ts to disk
        tsid = fsm.get_unique_id()
        fsm.store(tsid,interpolated_ats)

        # then update vantage point indexes
        simsearch.add_ts_to_vpdbs(interpolated_ats,tsid,DB_DIR,LIGHT_CURVES_DIR)
        tsid = tsfn_to_id(tsid)

    return tsid

def add_ts(ts):
    """Wrapper for function above for cases where file storage manager object has not already been generated"""
    fsm = FileStorageManager(LIGHT_CURVES_DIR)
    return add_ts_wfm(ts,fsm)

def get_by_id(id):
    """
    Args:
        id: int id of existing ts in database (e.g (547))

    Returns:
        Returns the array time series object associated with id

    Raises:
        ValueError: If id does not exist in the database

    """
    fsm = FileStorageManager(LIGHT_CURVES_DIR)
    try:
        ats = simsearch.load_ts(tsid_to_fn(id),fsm)
        return ats
    except ValueError:
        raise #Can not find ts by that id

def simsearch_by_id(id,n=5):
    """
    Args:
        id: int id of existing ts in database (e.g (547))
        n: number of time series to return. (Defaults to 5)

    Returns:
        Returns a dictionary of the n closest time series ids keyed by distances
        {.456:"ts_425", .3021:"ts_537"}

    Raises:
        ValueError: If id does not exist in the database

    """

    # Confirm indexes and time series files already exist
    rebuild_if_needed(LIGHT_CURVES_DIR,DB_DIR)

    fsm = FileStorageManager(LIGHT_CURVES_DIR)
    try:
        input_ts = simsearch.load_ts(tsid_to_fn(id),fsm)
    except IOError:
        raise ValueError("No time series with that id")
    else:
        closest_vp = simsearch.find_closest_vp(simsearch.load_vp_lcs(DB_DIR,LIGHT_CURVES_DIR), input_ts)
        return simsearch.search_vpdb_for_n(closest_vp,input_ts,DB_DIR,LIGHT_CURVES_DIR,n)[0]

def simsearch_by_ts(ts,n=5):
    """
    Args:
        ts: a (JSON???) encapsulation of an external time series;
            (Although it would be easier if you sent an array time series object)
        n: number of time series to return. (Defaults to 5)

    Returns:
        Returns a three argument tuple:
         - First element is a dictionary of the n closest time series ids keyed by
        distances.
         - Second augment is the newly assigned id of the new time series (if it's new) or
         the id of the existing ts if it's not new.
         - Third element is a bool to report whether the ts is new or not.

        Example: ({.456:"ts_425",.3021:"ts_537"},1201,True)

    Notes:

        Third augment is a boolean value that's True if the the submitted ts is "new /non-existent"
        time series, false if it already exists. We test for already exists by
        checking if there's a time series in the database with a distance of 0 (or
        very close to zero)

    """

    # Confirm indexes and time series files already exist
    rebuild_if_needed(LIGHT_CURVES_DIR,DB_DIR)

    is_new = False
    fsm = FileStorageManager(LIGHT_CURVES_DIR)
    interpolated_ats = sanitize_ats(ts)
    closest_vp = simsearch.find_closest_vp(simsearch.load_vp_lcs(DB_DIR,LIGHT_CURVES_DIR),interpolated_ats)
    n_closest_dict, tsid = simsearch.search_vpdb_for_n(closest_vp,interpolated_ats,DB_DIR,LIGHT_CURVES_DIR,n)

    if tsid == -1:
        is_new = True
        tsid = add_ts_wfm(interpolated_ats,fsm)

    return (n_closest_dict,tsid,is_new)

def rebuild_vp_indexs(n=20):
    """
    Rebuilds vantage point "databases" based on time series that have been
    saved to disk. May take some time(up to 30 seconds in my experience)

    """
    simsearch.create_vpdbs(n,LIGHT_CURVES_DIR,DB_DIR)

if __name__ == '__main__':
    print(simsearch_by_id(2000,n=5))
