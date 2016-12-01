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
Make Light Curves

A python command line utility for generating simulated light curve time series data files

Usage: ./makelcs 100 [optional flags]

Optional flags:
  -d, --delete  Delete existing light curves and exit.
  -h, --help    Show this help message and exit.

"""
from simsearch import LIGHT_CURVES_DIR,DB_DIR,SAMPLE_DIR,TEMP_DIR,TS_LENGTH


def tsmaker(mean, scale, jitter, length = 100):
    """
    Creates array time series object based on the normal distribution PDF.

    Args:
        mean: center of distribution
        scale: variance/spread of distribution.
        jitter: how much uniform-random variation is added on top of the distribution
        length: Length of the time series. (Defaults to 100 values)
    Returns:
        An array time series object.

    """
    times = np.arange(0.0, 1.0, (1.0 / length))
    values = norm.pdf(times, mean, scale) + jitter*np.random.randn(100)
    return ats.ArrayTimeSeries(times=times, values=values)

def random_ts(jitter,length = 100):
    """
    Creates uniform random array time series object.

    Args:
        jitter: how much variation to data points should have. (A value of zero is basically a straight line.)
        length: Length of the time series. Defaults to 100 values.
    Returns:
        An array time series object.

    """
    times = np.arange(0.0, 1.0, (1.0 / length))
    values = jitter*np.random.random(100)
    return ats.ArrayTimeSeries(times=times, values=values)

def make_n_ts(n):
    mean = .5
    scale = np.random.exponential(2)
    jitter = np.random.exponential()
    norm_ts = [tsmaker(mean, scale, jitter) for i in range(n//2)]
    rand_ts = [random_ts(np.random.uniform(0,10)) for i in range(n//2)]
    return norm_ts + rand_ts

def write_ts(ts,i):
    global LIGHT_CURVES_DIR

    os.makedirs(LIGHT_CURVES_DIR, exist_ok=True)
    filename = "ts-{}.txt".format(i)
    path = LIGHT_CURVES_DIR + filename
    datafile_id = open(path, 'wb')
    data = np.array([ts.times(), ts.values()])
    data = data.T

    np.savetxt(datafile_id, data, fmt=['%.3f','%8f'])
    datafile_id.close()

def erase_lc_dir():
    """Erase files in light curve directory"""
    global LIGHT_CURVES_DIR
    import shutil
    shutil.rmtree(LIGHT_CURVES_DIR)
    os.makedirs(LIGHT_CURVES_DIR, exist_ok=True)

if __name__ == "__main__":
    # Default usage options
    need_help = False
    delete = False
    num_lcs = 10

    # First, identify which flags were included
    for arg in sys.argv[1:]:
        if arg.lower() in ['-h','--help', 'help']: need_help = True
        elif arg.lower() in ['-d','--delete']: delete = True
        elif int(sys.argv[1]) > 0 and int(sys.argv[1]) < 100000:
            num_lcs = int(sys.argv[1])

    while(True):

        if need_help:
            print (HELP_MESSAGE)
            break

        if delete:
            cmd = input('\nErase existing files in "%s" directory? (Y/n):\n' % LIGHT_CURVES_DIR)
            if cmd.lower() == 'y' or cmd.lower() == 'yes' or cmd == '':
                erase_lc_dir()
                print("\nErased existing files. Exiting.")
                break

        cmd = input('\nErase existing files in "%s" directory and generate %d new simulated light-curves?(Y/n):\n' %(LIGHT_CURVES_DIR, num_lcs ))
        if cmd.lower() == 'y' or cmd.lower() == 'yes' or cmd == '':
            light_curves = make_n_ts(num_lcs)
            erase_lc_dir()
            for i, ts in enumerate(light_curves):
                write_ts(ts,i)
            print("\nWrote %d light-curves files. Exiting." % num_lcs)
            break
        else:
            print("\nExiting.")
            break

