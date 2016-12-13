# CLIENT

import sys
import json
import collections
import time
import os
import numpy as np
import random
from serialization import serialize, Deserializer
from socket import socket, AF_INET, SOCK_STREAM

from cs207project.tsrbtreedb.crosscorr import standardize, kernel_dist
from cs207project.tsrbtreedb.makelcs import make_lcs_wfm
from cs207project.tsrbtreedb.genvpdbs import create_vpdbs
from cs207project.rbtree.redblackDB import connect
from cs207project.storagemanager.filestoragemanager import FileStorageManager
import cs207project.timeseries.arraytimeseries as ats
import cs207project.tsrbtreedb.simsearch as simsearch

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, SAMPLE_DIR, TS_LENGTH

def open_socket(json_prep,ip = 'localhost',port = 20001):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((ip,port))

    # 2. to json
    msg_json = json.dumps(json_prep)

    # 3. to byte
    msg_byte = serialize(msg_json)

    # 4. client sends message
    s.send(msg_byte)

    # 5. client receives message
    msg = s.recv(8192)

    # 6. client converts received message from byte to json to dict
    ds = Deserializer()
    ds.append(msg)

    timeout = 0
    while not ds.ready() and timeout < 10:
        timeout += 1
        time.sleep(1)

    proximity_dict = ds.deserialize()
    return proximity_dict

def get_ts_with_id(tsid):
    """
    Returns ats object from database for given time series id (e.g., '503')

    Raise value error if time series id does not exist in database
    """

    json_prep = {"type":"get_by_id","tsid":tsid}
    s = open_socket(json_prep)

    if 'error_type' in s:
        raise ValueError(s['error'])
    else:
        times = np.array(s["ts"])[:,0]
        values = np.array(s["ts"])[:,1]
        full_ats = ats.ArrayTimeSeries(times=times,values=values)

    return full_ats

def save_ts_to_db(ats):
    """
    Saves submitted ats object to database.

    Returns assigned time series id.

    Note: get_n_nearest_ts_for_ts (below) will *also* save the time
    Submitted time series to the database if it's new.

    """

    json_prep = {"type":"save_ts_to_db","ts":list(zip(ats.times(),ats.values()))}
    s = open_socket(json_prep)

    if 'error_type' in s:
        raise ValueError(s['error'])
    else:
        return s['tsid']


def get_n_nearest_ts_for_tsid(tsid, n=5):
    """
    Returns ordered dict of n nearest time series for preexisting id

    Args
        tsid: int id of preexisting time series (e.g., 456)
        n: number of time series ids to be returned

    Returns:
        Ordered dict of nearest n time series, with distance values as keys and time series ids as values
    Raises:
        Value error if time series id does not exist

    """
    json_prep = {"type":"with_id","id":tsid,'n':n}
    s = open_socket(json_prep)

    if 'error_type' in s:
        raise ValueError(s['error'])
    else:
        proximity_od = collections.OrderedDict(sorted(s.items()))
        return proximity_od

def get_n_nearest_ts_for_ts(ats, n=5):
    """
    Returns dict of n nearest time series to inputed ats object; also saves ts to database

    Args:
        ts: array time series object of new ts to be evaluated
        n: number of time series ids to be returned

    Returns:
        2 augment dict:
            'n_closest_dict' is a sorted sub dictionary containing the n closest time series
            'tsid': is the assigned id of the new time series (if it's new) or the existing id if it was already there

        For example:
            {'n_closest_dict':{('0.21303259554936094', 372), ('0.2132077724142843', 231)},'tsid':1002}

    Raises:
        Value error if submitted time series is in incorrect format

    """
    json_prep = {"type":"with_ts","ts":list(zip(ats.times(),ats.values())),'n':n}
    s = open_socket(json_prep)

    if 'error_type' in s:
        raise ValueError(s['error'])
    else:
        s['n_closest_dict'] = collections.OrderedDict(sorted(s['n_closest_dict'].items()))
        return s



if __name__ == "__main__":

# conditional execution based on if the user passes an id or filepath
# if user gives an int assume they have given us an id they expect to find in the database
# if user gives us a string assume that it is a filepath

    user_input = sys.argv[1]
    # 1 prep message for json conversion
    if str.isdigit(user_input):
        #print(get_n_nearest_ts_for_tsid(user_input, n=2))
        print(get_ts_with_id(user_input))
    elif isinstance(user_input, str):
        full_ts = simsearch.load_external_ts(user_input)
        #print(get_n_nearest_ts_for_ts(full_ts, n=2))
        print(save_ts_to_db(full_ts))
    else:
        raise ValueError("'%s' is not an appropriate input. Please give id of time series in database or filepath of new timeseries" % sys.argv[1])



