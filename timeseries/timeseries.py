from sizedcontainertimeseriesinterface import SizedContainerTimeSeriesInterface
from lazy import LazyOperation
from lazy import lazy
import numpy as np
import numbers

class TimeSeries(SizedContainerTimeSeriesInterface):
    """
    A class that stores a single, ordered set of numerical data.

    Parameters
    ----------
    values : list
        This can be any object that can be treated like a sequence. Mandatory.
    times : list
        This can be any object that can be treated like a sequence. Optional.
        If it is not supplied, equally spaced integers are used instead.
    position: int
        The index position at which the requested item should be inserted

    Notes
    -----
    PRE: `values` is sorted in non-decreasing order
    POST:

    INVARIANTS:

    WARNINGS:
    - Does not maintain an accurate time series if `input_data` is unsorted.
    """

    def __init__(self, values, times=None):
        """
        The TimeSeries class constructor. It must be provided the initial data
        to fill the time series instance with.

        Parameters
        ----------
        values : sequence-like
            Actual data points for TimeSeries.
            Any user-provided sequence-like object. Mandatory.
        times : sequence-like
            Time values for TimeSeries. Optional.
            If None, equally spaced integers are used instead.

        Notes
        -----
        PRE: If times is not provided, `values` must be sorted
        POST:

        INVARIANTS:
        inital_data and times (if provided) must be sequences.

        WARNINGS:

        """

        # First confirm `inital_data` is a sequence.
        # J: all Python sequences implement __iter__(), which we can use here.

        self.__class__.is_sequence(values)
        self._values = list(values)

        if times:
            self.__class__.is_sequence(times)
            self._times = list(times)

        else:
            self._times = list(range(len(self._values)))

        if len(self._times) != len(self._values):
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self._times) != len(set(self._times)):
            raise ValueError("Time data should contain no repeats")

    def __len__(self):
        return len(self._values)


    #### ABSTRACT THE METHODS BELOW TO BASE CLASS; REMOVE THIS LATER ######

    # J: new implementation inherited from parent class.
    # leaving this here in case need to debug tests....

    # def __setitem__(self, index, value):
    #     try:
    #         self._values[index] = value
    #     except IndexError:
    #         raise IndexError("Index out of bounds!")

    # J: Also abstracted this to parent class...
    # def __contains__(self, needle):

    #     # J this also works for
    #     # R: leverages self._values is a list.
    #     # Will have to change when we relax this.
    #     return needle in self._values



    # J: should this not be (self - other)?

    def __neg__(self):
        return self.__class__((-x for x in self._values), self._times)

    def __pos__(self):
        return self.__class__((x for x in self._values), self._times)

    def __add__(self, rhs):
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot add a numpy array to a TimeSeries!"
            if isinstance(rhs, list):
                raise "Cannot add a list to a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                # R: may be worth testing time domains are preserved correctly
                return self.__class__(values=(a + rhs for a in self), times=self._times)
            else:
                self._check_length_helper(self, rhs)
                # R: test me. should fail when the time domains are non congruent
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return self.__class__(values=(a + b for a, b in pairs), times=self._times)
        except TypeError:
            raise NotImplemented # R: test me. should fail when we try to add a numpy array or list

    def __sub__(self, rhs):
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot sub a numpy array from a TimeSeries!"
            if isinstance(rhs, list):
                raise "Cannot sub a list from a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return self.__class__((a - rhs for a in self), self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return self.__class__((a - b for a, b in pairs), self._times)
        except TypeError:
            raise NotImplemented


    def __mul__(self, rhs):
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot mul a numpy array with a TimeSeries!"
            if isinstance(rhs, list):
                raise "Cannot mul a list with a TimeSeries!"
            if isinstance(rhs, numbers.Real):
                return TimeSeries((a * rhs for a in self), self._times)
            else:
                self._check_length_helper(self, rhs)
                self._check_time_domains_helper(self, rhs)
                pairs = zip(self._values, rhs)
                return TimeSeries((a * b for a, b in pairs), self._times)
        except TypeError:
            raise NotImplemented


    def __eq__(self, rhs):
        # R: leverages self._values is a list. Will have to change when we relax this.
        try:
            if isinstance(rhs, np.ndarray):
                raise "Cannot compare numpy array to TimeSeries!"
            self._check_length_helper(self, rhs)
            self._check_time_domains_helper(self, rhs)
            return self._values==rhs._values
        except TypeError:
            raise NotImplemented

    @lazy
    def identity(self):
        """
            An identity function with one argument that just returns the argument - self is the only argument

            Returns
            -------
            self : the instance to identify
        """
        return self

    @property
    def lazy(self):
        """
            A lazy property method that returns a new LazyOperation instance using the TimeSeries.identity() method

            Returns
            -------
            self.identity() : an instance of LazyOperation
        """
        return self.identity()