# CLIENT

import sys
from serialization import serialize, Deserializer
from socket import socket, AF_INET, SOCK_STREAM
import json 
import collections 

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

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR, DB_DIR, SAMPLE_DIR, TS_LENGTH

# verbatim from simsearch.py
##############################################
def load_nparray(filepath):
    """Helper to load space delimited nparray from disk"""
    try:
        nparray = np.loadtxt(filepath)
    except(IOError):
        raise IOError("Unable to load np array %s" % filepath)
    else:
        return nparray

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
    # interpolated_ats = full_ts.interpolate(np.arange(0.0, 1.0, (1.0 /TS_LENGTH)))
    return full_ts
##############################################

# new code begins
##############################################
# conditional execution based on if the user passes an id or filepath
# if user gives an int assume they have given us an id they expect to find in the database
# if user gives us a string assume that it is a filepath
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20001))

user_input = sys.argv[1]
# 1 prep message for json conversion
if str.isdigit(user_input): 
	json_prep = {"type":"with_id","id":user_input}
elif isinstance(user_input, str):
	full_ts = load_external_ts(user_input)
	json_prep = {"type":"with_ts","ts":list(zip(full_ts.times(),full_ts.values()))}
else:
	raise ValueError("'%s' is not an appropriate input. Please give id of time series in database or filepath of new timeseries" % sys.argv[1])

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
if ds.ready():
	proximity_dict = ds.deserialize()

proximity_od = collections.OrderedDict(sorted(proximity_dict.items()))
print(proximity_od)
