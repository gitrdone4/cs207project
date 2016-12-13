#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
Make Light Curves

Code for generating simulated light curve time series data files.
Can be used independently or called by simsearch.

"""

import sys
import os
import random
import numpy as np
from scipy.stats import norm

import cs207project.timeseries.arraytimeseries as ats
from cs207project.storagemanager.filestoragemanager import FileStorageManager

# Global variables

from cs207project.tsrbtreedb.settings import LIGHT_CURVES_DIR

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
    values = norm.pdf(times, mean, scale) + jitter*np.random.randn(length)
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
    values = jitter*np.random.random(length)
    return ats.ArrayTimeSeries(times=times, values=values)

def make_n_ts(n):
    """
    Generates n random light curves to be stored to disk.

    Currently set to do half based on normal pdf (with some noise thrown in)
    and half uniformly randomly...but not working as well as I had hoped.
    Should probably tweak in the future.
    """
    mean = .5
    scale = np.random.exponential(2)
    jitter = np.random.exponential()
    norm_ts = [tsmaker(mean, scale, jitter) for i in range(n//2)]
    rand_ts = [random_ts(np.random.uniform(0,10)) for i in range(n//2)]
    return norm_ts + rand_ts


def clear_dir(dir,recreate=True):
    """Erase folder and recreate it"""
    import shutil
    if os.path.exists(dir):
        shutil.rmtree(dir)
    if(recreate):
        os.makedirs(dir, exist_ok=True)

def write_ts_wfm(ts,fsm):
    """ Write light curve to disk useing file storage manager"""
    unique_id = fsm.get_unique_id()
    fsm.store(unique_id, ts)

def make_lcs_wfm(num_lcs,lc_dir=''):
    """
    Executes functions above:
        (1) Makes FileStoage Manager object
        (1) Generates n light curves
        (3) Writes them to disk
    """
    clear_dir(lc_dir)
    fsm = FileStorageManager(lc_dir)
    light_curves = make_n_ts(num_lcs)
    print("Generating %d light-curve files" % num_lcs, end="")
    for i, ts in enumerate(light_curves):
        if i % 50 == 0:
            print('.', end="")
        write_ts_wfm(ts,fsm)
    print("Done.")
