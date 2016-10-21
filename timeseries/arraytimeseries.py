from timeseries import TimeSeries
import numpy as np


class ArrayTimeSeries(TimeSeries):
    """
    A subclass that stores a single, ordered set
    of numerical data contiguously as a `np.array`.

    Parameters
    ----------

    Notes
    -----

    INVARIANTS:

    WARNINGS:

    """

    def __init__(self, values):
        self.is_sequence(values)
        self.data = np.array(values)
