from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
import numpy as np

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
        self.is_sequence(times)
        self.is_sequence(values)
        self._times = np.array(list(times))
        self._values = np.array(list(values))

        if len(self._times) != len(self._values):
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self._times) != len(set(self._times)):
            raise ValueError("Time data should contain no repeats")

    def __iter__(self):
        for val in zip(self._times, self._values):
            yield val


    # J: since our ABC is an interface, need to
    # reimplement these here... IMO we should
    # consider changing these so that our ABC
    # implements the most essential functionality
    # instead of just being an interface. this is not java :)

    # J: should this not iterate over tuples?
    def __iter__(self):
        for val in self._values:
            yield val

    def itertimes(self):
        for tim in self._times:
            yield tim

    def itervalues(self):
        # R: Identical to __iter__
        for val in self._values:
            yield val

    def iteritems(self):
        for i in range(len(self._values)):
            yield self._times[i], self._values[i]

    def __len__(self):
        # Note: len of np.appry returns and error for arrays of size 1.
        #super().__len__()
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


    # J: adding this here to make test pass
    # imo we should consider implementing this in
    # SizedContainerTimeSeriesInterface...
    def interpolate(self,ts_to_interpolate):
        """
        Returns new TimeSeries instance with piecewise-linear-interpolated values
        for submitted time-times.If called times are outside of the domain of the existing
        Time Series, the minimum or maximum values are returned.

        Parameters
        ----------
        self: TimeSeries instance
        ts_to_interpolate: list or other sequence of times to be interpolated

        """
        def binary_search(times, t):
            """ Returns surrounding time indexes for value that is to be interpolated"""
            min = 0
            max = len(times) - 1
            while True:
                if max < min:
                    return (max,min)
                m = (min + max) // 2
                if times[m] < t:
                    min = m + 1
                elif times[m] > t:
                    max = m - 1
                else: #Should never hit this case in current implementation
                    return (min,max)

        def interpolate_val(times,values,t):
            """Returns interpolated value for given time"""

            if t in times:          #time already exits in ts -- return it
                return values[times.index(t)]

            elif t >= times[-1]:    #time is above the domain of the existing values -- return max time value
                return values[-1]

            elif t <= times[0]:     #time is below the domain of the existing values -- return min time value
                return values[0]

            else:                   #time is between two existing points -- interpolate it
                low,high = binary_search(times, t)
                slope = (float(values[high]) - values[low])/(times[high] - times[low])
                c = values[low]
                interpolated_val = (t-times[low])*slope + c
                return interpolated_val

        interpolated_ts = [interpolate_val(self._times,self._values,t) for t in ts_to_interpolate]
        return self.__class__(values=interpolated_ts,times=ts_to_interpolate)

    # J: these methods need to be implemented
    def __abs__(self):
        pass
    def __add__ (self):
        pass
    def __bool__(self):
        pass
    def __contains__(self):
        pass
    def __mul__(self):
        pass
    def __ne__(self):
        pass
    def __neg__(self):
        pass
    def __pos__(self):
        pass
    def __radd__(self):
        pass
    def __repr__(self):
        pass
    def __rmul__(self):
        pass
    def __rsub__(self):
        pass
    def __str__(self):
        pass
    def __sub__(self):
        pass