# create_metadata.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

# imports
from string import ascii_uppercase
import pandas as pd
import numpy as np
import sqlite3
import os
import re

a_to_f = list(ascii_uppercase[:6])

# add metadata function
def get_metadata(fname):
    """
    Description
    -----------
    Creates a row of metadata associated with a
    time series id. Metadata row has the following
    columns: id, blarg, level, mean, std.

    Parameters
    ----------
    fname: str
        string of .npy file

    Returns
    -------
    metadata_tuple: tuple
        tuple with metadata of the time series.
    """

    # validate `fname`
    if not fname.endswith('.npy'):
        error_msg = 'Make sure you are inputting a .txt file!'
        raise ValueError(error_msg)

    # load dataset and calculate stats
    ts_out = pd.DataFrame(np.load('light_curves/'+fname)).transpose()
    ts_out.columns = ['_', 'value']
    _id = int(re.sub('(ts_datafile_|\.npy)', '' ,fname))
    mean = ts_out.value.mean()
    std = ts_out.value.std()
    blarg = np.random.uniform()
    level = np.random.choice(a_to_f)

    # put metadata into a tuple
    metadata_tuple = (_id, mean, std, blarg, level)
    return metadata_tuple

def main():

    # get names of text files
    fnames = [s for s in os.listdir('light_curves/') if s.endswith('.npy')]

    # construct metadata array
    metadata_arr = pd.DataFrame([get_metadata(f) for f in fnames])
    metadata_arr.columns = ['id','mean','std', 'blarg', 'level']
    metadata_arr.sort_values('id', inplace=True)

    # write csv file
    with sqlite3.connect('ts_metadata.db') as conn:
        metadata_arr.to_sql('ts_metadata', conn, if_exists='replace', index=False)
if __name__ == '__main__':
    main()
