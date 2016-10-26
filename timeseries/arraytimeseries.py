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
        #super().__len__() Note: len of np.appry returns and error for arrays of size 1.
        return len(np.atleast_1d(self._values))

    def __getitem__(self, index):
        try:
            return self._times[index], self._values[index]
        except IndexError:
            raise IndexError("Index out of bounds!")

    def __setitem__(self, index, item):
        try:
            self._times[index] = item[0]
            self._values[index] = item[1]
        except IndexError:
            raise IndexError("Index out of bounds!")

    def _check_time_domains_helper(lhs , rhs):
        if not np.array_equal(lhs._times,rhs._times):
            raise ValueError(str(lhs)+' and '+str(rhs)+' must have identical time domains')

    def __eq__(self, rhs):
        # Note: np.array_equal compares both elements and dimensions.
        self.__class__._check_time_domains_helper(self, rhs)
        try:
            return (np.array_equal(self._values,rhs._values) and np.array_equal(self._times,rhs._times))

        except TypeError:
            raise NotImplemented