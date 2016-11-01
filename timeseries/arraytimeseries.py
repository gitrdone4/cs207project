from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
import numpy as np
import numbers

class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
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
        # J: breaking DRY and adding sequenceness checks here, since
        # we don't inherit from TimeSeries anymore and
        # since the upper levels of the inheritance hierarchy
        # are (mostly) abstract things...
        self.__class__.is_sequence(times)
        self.__class__.is_sequence(values)
        self._times = np.array(list(times))
        self._values = np.array(list(values))

        if len(self._times) != len(self._values):
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self._times) != len(set(self._times)):
            raise ValueError("Time data should contain no repeats")

    def __len__(self):
        # Note: len of np.appry returns and error for arrays of size 1.
        #super().__len__()
        return len(np.atleast_1d(self._values))


    #### ABSTRACT FNS BELOW; REMOVE THIS LATER ######

    def __eq__(self, rhs):
        # Note: np.array_equal compares both elements and dimensions.
        try:
            if isinstance(rhs, list):
                raise "Cannot compare list to ArrayTimeSeries!"
            self.__class__._check_time_domains_helper(self, rhs)
            return (np.array_equal(self._values,rhs._values) and np.array_equal(self._times,rhs._times))

        except TypeError:
            raise NotImplemented


    def __add__ (self,rhs):
        # N: Note – currently, we’re adding the value arrays if everything is the same length.
        # N: But it would be possible to have to time series that were the same length but which
        # N: covered different times. Should we address this as well?

        try:
            if isinstance(rhs, list):
                raise "Cannot add a list to a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__(values=(self._values + rhs), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                return self.__class__(values=self._values + rhs._values, times=self._times)
        except TypeError:
            raise NotImplemented

    def __sub__(self, rhs):
        try:
            if isinstance(rhs, list):
                raise "Cannot sub a list from a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__(values=(self._values - rhs), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                return self.__class__(values=self._values - rhs._values, times=self._times)
        except TypeError:
            raise NotImplemented

    def __mul__(self, rhs):
        try:
            if isinstance(rhs, list):
                raise "Cannot mul a list with a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__(values=(self._values * rhs), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return self.__class__(values=self._values * rhs._values, times=self._times)
        except TypeError:
            raise NotImplemented

    def __neg__(self):
        return self.__class__(values=((-1)*self._values), times=self._times)

    def __pos__(self):
        return self.__class__(values=self._values, times=self._times)

    def mean(self, chunk = None):
        return np.mean(self._values)

    def std(self, chunk = None):
        return np.std(self._values, ddof=1)
