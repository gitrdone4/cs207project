from timeseries import TimeSeries
import numpy as np

class ArrayTimeSeries(TimeSeries):
    """
    A subclass that stores a single, ordered set of numerical data as a np.array

    Parameters
    ----------

    Notes
    -----

    INVARIANTS:

    WARNINGS:

    """

    def __init__(self, initial_data):
        self.is_sequence(initial_data)
        self.data = np.array(initial_data)
