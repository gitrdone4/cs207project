from timeseries import TimeSeries
import numpy as np


class ArrayTimeSeries(TimeSeries):
    """
    A subclass that stores two arrays internally, an ordered set
    of numerical data and its time points contiguously as two of `np.array`.

    Parameters
    ----------
        values : sequence-like
            Actual data points for ArrayTimeSeries.
            Any user-provided sequence-like object. Mandatory.
        times : sequence-like
            Time values for ArrayTimeSeries. Mandatory

    Notes
    -----

    INVARIANTS:

    WARNINGS:

    """
    def __init__(self, times, values):
        TimeSeries.__init__(self, times, values)
        self._times = np.array(times)
        self._values = np.array(values)

    def __iter__(self):
        for val in zip(self._times, self._values):
            yield val

    def __itertimes__(self):
        super().__itertimes__()

    def __iteritems__(self):
        super().__iteritems__()

    def __len__(self):
        super().__len__()

    def __getitem__(self, index):
        try:
            return self._times[index], self._values[index]
        except IndexError:
            raise("Index out of bounds!")

    def __setitem__(self, index, item):
        try:
            self._times[index] = item[0]
            self._values[index] = item[1]
        except IndexError:
            raise("Index out of bounds!")