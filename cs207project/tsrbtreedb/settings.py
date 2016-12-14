#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
"""
A central place to store global variables that are assumed to consistent throughout
the simsearch and socket0server modal.

"""

LIGHT_CURVES_DIR = "light_curves/"
DB_DIR = "vp_dbs/"
SAMPLE_DIR = "sample_data/"
TEMP_DIR = "temp/"
TS_LENGTH = 100 #Number of data points for generated time series
PORT = 20042 #Port used by socket server
SOCKET_SERVER_IP ='localhost'


def tsid_to_fn(tsid):
	return 'ts_datafile_' + str(tsid)

def tsfn_to_id(tsfn):
    return int(tsfn.replace('ts_datafile_',''))
