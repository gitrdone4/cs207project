#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
Socket Server Client

This module contains the functions for formating socket requests  and sending them to the socket server.

Main functions
    get_ts_with_id              Retrieve existing time series by id
    save_ts_to_db               Save new time series to database
    get_n_nearest_ts_for_ts     Find nearest n time series for submitted time series
    get_n_nearest_ts_for_tsid   Find nearest n time series for  existing id
    open_socket                 Performs socket server magic

"""

import sys
import json
import collections
import time
import numpy as np

from cs207project.socketclient.serialization import serialize, Deserializer
from socket import socket, AF_INET, SOCK_STREAM

import cs207project.timeseries.arraytimeseries as ats
from cs207project.tsrbtreedb.simsearch import load_external_ts
from cs207project.tsrbtreedb.settings import PORT,SOCKET_SERVER_IP

def open_socket(json_prep,ip=SOCKET_SERVER_IP,port =PORT,timeout=15):
    """
    Open Socket -- where the socket server magic happens!

    Args:
        json_prep: Specially formated dict
        ip: Ip address of socket server
        port: Port of socket server
        timeout: time in seconds client should wait before timing out

    Returns:
        Specially formated reponse_dict from socket server

    """
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

    # What until ds is ready, or timeout
    waittime = 0
    while not ds.ready() and waittime  < timeout:
        waittime += 1
        time.sleep(1)

    reponse_dict = ds.deserialize()
    return reponse_dict


def get_ts_with_id(tsid):
    """
    Returns ats object from database for given time series id (e.g., '503')

    Raise value error if time series id does not exist in database
    """

    json_prep = {"type":"get_by_id","ts":tsid}
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

    Args:
        ats: array time series object ()
    Returns:
        tsid: the assigned time series id.
    Raises:
        ValueError if there's a problem saving the time series.

    If time series has already been saved, will return existing id.

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

    Args:
        tsid: int id of preexisting time series (e.g., 456)
        n: number of time series ids to be returned

    Returns:
        Ordered dict of nearest n time series, with distance values as keys and time series ids as values
    Raises:
        Value error if time series id does not exist in database

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
    """
    conditional execution based on if the user passes an id or filepath
    if user gives an int assume they have given us an id they expect to find in the database
    if user gives us a string assume that it is a filepath
    """

    user_input = sys.argv[1]
    # 1 prep message for json conversion
    if str.isdigit(user_input):
        #print(get_n_nearest_ts_for_tsid(user_input, n=2))
        print(get_ts_with_id(user_input))
    elif isinstance(user_input, str):
        full_ts = load_external_ts(user_input)
        #print(get_n_nearest_ts_for_ts(full_ts, n=2))
        print(save_ts_to_db(full_ts))
    else:
        raise ValueError("'%s' is not an appropriate input. Please give id of time series in database or filepath of new timeseries" % sys.argv[1])



