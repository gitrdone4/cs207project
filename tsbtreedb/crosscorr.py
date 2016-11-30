import numpy.fft as nfft
import numpy as np
#below is your module. Use your ListTimeSeries or ArrayTimeSeries..

# Hacky solution to import array time series from sister directory by inserting it into system path
# should fix once time series library is turned into a proper python model

import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.insert(0,d + '/timeseries')
import arraytimeseries as ats

from scipy.stats import norm
import random

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

def standardize(ts, m, s):
    "standardize timeseries ts by mean m and std deviation s"
    stand_vals = (ts.values() - m)/s
    return ats.ArrayTimeSeries(times=ts.times(), values=stand_vals)


def ccor(ts1, ts2):
    """
    given two standardized time series, compute their cross-correlation using FFT

    Args:
       ts1: first time series object
       ts2: second time series object
    Returns:
       Float - cross correlation value.

    Raises:
       ValueError: if length of ts1 and ts2 are not equal

    """

    # assert that len of ts1 = ts2
    if len(ts1) != len(ts2):
        raise ValueError("ts1 must be the same length as ts2 to calculate cross correlation")

    # fast fourier transform for ts1
    X = nfft.fft(ts1.values())

    # Complex conjugate of the fft transform of ts2
    Yhat = np.conjugate(nfft.fft(ts2.values()))

    # Normalizing scaler is required so that each shift is counted exactly once
    s = 1 / (1. * len(ts1))

    # The cross-correlation is the convolution of the fft transformed ts1 (X)
    # and the conjugate of ts2 (Yhat) scaled by s
    return  nfft.ifft(X * Yhat).real * s


# this is just for checking the max correlation with the
# kernelized cross-correlation
def max_corr_at_phase(ts1, ts2):
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr

#The equation for the kernelized cross correlation is given at
#http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
#normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
#of a time series with itself is 1. We'll set the default multiplier to 1.

def kernel_corr(ts1, ts2, mult=1):
    """
    compute a kernelized correlation between two time series objects to be used as distance measure

    Args:
        ts1: first time series object. (Must be standardized.)
        ts2: second time series object. (Must be standardized.)
        m: multiplier factor. Defaults to 1. (Must be non-negative.)

    Returns:
        Float - kernelized correlation value
    """

    # calculate kernel
    # K(e^(m*ccor(ts1,ts2)))
    kernel = np.sum(np.exp(mult * ccor(ts1, ts2)))

    # Calculate kernel normalization constant:
    # sqrt(K(x,x)K(y,y))
    k_norm = np.sqrt(np.sum(np.exp(mult * ccor(ts1, ts1))) *
                     np.sum(np.exp(mult * ccor(ts2, ts2))))

    # return normalized kernel if k_norm is non-zero
    if k_norm != 0:
        return kernel/k_norm
    else:
        return 0

def kernal_dist(ts1, ts2, mult=1):
    """
    Calculates a cross-correlation based distance between two time series objects.

    Args:
        ts1: 1st time series object.
        ts2: 2nd time series object.
        m: multiplier factor. Defaults to 1. (Must be non-negative.)

    Returns:
        Float: distance value
    """

    # Standardize the time series
    ts1_stndrdzed = standardize(ts1,ts1.mean(), ts1.std())
    ts2_stndrdzed = standardize(ts2,ts2.mean(), ts2.std())

    # Calculate the kernel correlation value for ts1 and ts2
    kernel_corr_val = kernel_corr(ts1_stndrdzed,ts2_stndrdzed, mult)

    # Theorem 1-P4 in Pavlos paper states that the dist^2 = C(ts1,ts1)+C(ts2,ts2)-2C(ts1,ts2)
    # (Where C = kernel correlation )
    # However, we are using normalized kernels here, so the dist^2 will be 2(1-C(ts1,ts2))
    return np.sqrt(2*(1-kernel_corr_val))

def s_stats(n,ts):
    return "%s mean: %.4f, %s std: %.4f" % (n,ts.mean(),n,ts.std())

def make_n_ts(n):
    return [tsmaker(0.5, 0.1, random.uniform(0,10)) for i in range(n)]

#this is for a quick and dirty test of these functions
if __name__ == "__main__":

    t1 = tsmaker(0.5, 0.1, random.uniform(0,10))
    t2 = tsmaker(0.5, 0.1, random.uniform(0,10))
    #t2 = random_ts(10)
    print(s_stats("ts1",t1))
    print(s_stats("ts2",t2))

    print(kernal_dist(t1,t2))
    import matplotlib.pyplot as plt
    plt.plot(t1, label='ts1')
    plt.plot(t2, label='ts2')
    plt.legend()
    plt.show()
    standts1 = standardize(t1, t1.mean(), t1.std())
    standts2 = standardize(t2, t2.mean(), t2.std())
    print("Standardized: ")
    print(s_stats("standts1",standts1))
    print(s_stats("standts2",standts2))
    #print(standts1.mean(), standts1.std(), standts2.mean(), standts2.std())

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print("idx, mcorr:", idx, mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=10)
    print("sumcorr: ", sumcorr)
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3,label='ts3 - Random')
    plt.plot(t4,label='ts4 - Random')
    plt.legend()
    plt.show()
    standts3 = standardize(t3, t3.mean(), t3.std())
    standts4 = standardize(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print("idx, mcorr:", idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=10)
    print("sumcorr: ", sumcorr)

    print("**** ts with it self *** ")
    idx, mcorr = max_corr_at_phase(standts3, standts3)
    print("idx, mcorr:", idx, mcorr)
    sumcorr = kernel_corr(standts3, standts3, mult=10)
    print("sumcorr: ", sumcorr)

   # print(make_n_ts(100))


