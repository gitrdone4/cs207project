#!/usr/local/bin/python3

# Hacky solution to import array time series from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')
import arraytimeseries as ats


import crosscorr
import numpy as np
#below is your module. Use your ListTimeSeries or ArrayTimeSeries..
import arraytimeseries as ats
from scipy.stats import norm
import random

# Global variables

HELP_MESSAGE = \
"""
Build DB

A python command line utility for ____ time series data files

Usage: ./builddb  [optional flags]

Optional flags:
  -h, --help    Show this help message and exit.

"""
LIGHT_CURVES_DIR = "light_curves/"


def load_ts():
    global LIGHT_CURVES_DIR
    timeseries_dict = {}

    for file in os.listdir(LIGHT_CURVES_DIR):
        if file.startswith("ts-") and file.endswith(".txt"):
            i = number = int(file[3:-4])
            fn = LIGHT_CURVES_DIR + file
            data = np.loadtxt(fn)
            times, values = data.T
            ts = ats.ArrayTimeSeries(times=times,values=values)
            timeseries_dict[i] = ts

    return timeseries_dict


if __name__ == "__main__":
    # Default usage options
    need_help = False

    # First, identify which flags were included
    for arg in sys.argv[1:]:
        if arg.lower() in ['-h','--help', 'help']: need_help = True


    while(True):

        if need_help:
            print (HELP_MESSAGE)
            break
        else:
            timeseries_list = load_ts()
            print(timeseries_list)
            break

