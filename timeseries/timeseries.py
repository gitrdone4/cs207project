import numpy as np
import numbers

class TimeSeries:
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

    # J: maximum length of `values` after which
    # abbreviation will occur in __str__() and __repr__()
    MAX_LENGTH = 10

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

        # J: unit test this
        # N: done
        # J: all Python sequences implement __iter__(), which we can use here.

        self.is_sequence(values)
        self.data = list(values)

        if times:

            # R: haven't checked if times is iterable.
            #    make this a precondition?
            # J: can't we simply test for this as well?
            self.is_sequence(times)
            self.time = list(times)

        else:
            self.time = list(range(len(self.data)))

        if len(self.time) != len(self.data):

            # R: unit test me
            # N: Done.
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self.time) != len(set(self.time)):

            # R: unit test me. consider moving to precondition
            # N: Done.
            raise ValueError("Time data should contain no repeats")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        # OLD IMPLEMENTATION - get value based on time
        # if index not in self.time:
        #     raise ValueError("Choose t from time column")
        # return self.data[self.time.index(index)]
        # NEW IMPLEMENTATION - get value based on index
        try:
            return self.data[index]
        except IndexError:
            raise("Index out of bounds!")

    def __setitem__(self, index, value):
        # OLD IMPLEMENTATION - set value based on time
        # if index not in self.time:
        #     raise ValueError("Choose t from time column")
        # self.data[self.time.index(index)] = value
        # NEW IMPLEMENTATION - set value based on index
        try:
            self.data[index] = value
        except IndexError:
            raise("Index out of bounds!")

    def __iter__(self):
        for val in self.data:
            yield val

    def itertimes(self):
        for tim in self.time:
            yield tim

    def itervalues(self):
        # R: Identical to __iter__
        for val in self.data:
            yield val

    def iteritems(self):
        for i in range(len(self.data)):
            yield self.time[i], self.data[i]

    def __contains__(self, needle):
        # R: leverages self.data is a list. Will have to change when we relax this.
        return needle in self.data

    def values(self):
        # "values: returns a numpy array of values (should have done this)"
        # R: I just created this one but according to current instructions it should have already been implemented
        # Old instructions say it was implemented for ArrayTimeSeries not the more general TimeSeries class, so I'm confused 
        # I think this should be readonly but already taken care of by making it a numpy array
        # motivates making self.data -> self._data
        return np.array(self.data)

    def times(self):
        # R: another read only seeming thing
        # motivates making self.time -> self._time
        return np.array(self.time)

    def items(self):
        return list(zip(self.time, self.data))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}(Length: {}, {})'.format(class_name,
                                           len(self.data),
                                           str(self))

    def __str__(self):
        """
        Description
        -----------
        Instance method for pretty-printing the TimeSeries contents.

        Parameters
        ----------
        self: TimeSeries instance

        Returns
        -------
        pretty_printed: string
            an end-user-friendly printout of the time series.
            If `len(self.data) > MAX_LENGTH`, printout abbreviated
            using an ellipsis: `['a','b','c', ..., 'x','y','z']`.

        Notes
        -----
        PRE:
        POST:

        INVARIANTS:

        WARNINGS:

        """
        if len(self.data) > self.MAX_LENGTH:
            needed = self.data[:3]+self.data[-3:]
            pretty_printed = "[{} {} {}, ..., {} {} {}]".format(*needed)
 
        else:
            pretty_printed = "{} {}".format(list(self.data), list(self.time))

        return pretty_printed

    @staticmethod
    def _check_length_helper(lhs , rhs):
        if not len(lhs)==len(rhs):
            raise ValueError(str(lhs)+' and '+str(rhs)+' must have the same length')

    @staticmethod
    # makes check lengths redundant. However I keep them separate in case we want to add functionality to add objects without a defined time dimension later.
    def _check_time_domains_helper(lhs , rhs):
        if not lhs.time==rhs.time:
            raise ValueError(str(lhs)+' and '+str(rhs)+' must have identical time domains')

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self.data))
    
    def __bool__(self): 
        return bool(abs(self.data))

    def __neg__(self):
        return TimeSeries((-x for x in self.data), self.time) 
    
    def __pos__(self):
        return TimeSeries((-x for x in self.data), self.time)

    def __add__(self, rhs):
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries((a + rhs for a in self), self.time) # R: may be worth testing time domains are preserved correctly
            else: 
                TimeSeries._check_length_helper(self, rhs) 
                TimeSeries._check_time_domains_helper(self, rhs) # R: test me. should fail when the time domains are non congruent
                pairs = zip(self.data, rhs)
                return TimeSeries((a + b for a, b in pairs), self.time)
        except TypeError:
            raise NotImplemented # R: test me. should fail when we try to add a numpy array or list
    
    def __radd__(self, other): # other + self delegates to self.__add__
        return self + other

    def __sub__(self, rhs):
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries((a - rhs for a in self), self.time) 
            else: 
                TimeSeries._check_length_helper(self, rhs) 
                TimeSeries._check_time_domains_helper(self, rhs) 
                pairs = zip(self.data, rhs)
                return TimeSeries((a - b for a, b in pairs), self.time)
        except TypeError:
            raise NotImplemented 
    
    def __rsub__(self, other): 
        return -(self - other)

    def __mul__(self, rhs): # does this define exponentiation as well?
        try:
            if isinstance(rhs, numbers.Real):
                return TimeSeries((a * rhs for a in self), self.time)
            else: 
                TimeSeries._check_length_helper(self, rhs) 
                TimeSeries._check_time_domains_helper(self, rhs)
                pairs = zip(self.data, rhs)
                return TimeSeries((a * b for a, b in pairs), self.time)
        except TypeError:
            raise NotImplemented
    
    def __rmul__(self, other):
        return self * other

    def is_sequence(self, seq):
        """
        Description
        -----------
        Checks if `seq` is a sequence by verifying if it implements __iter__.

        Parameters
        ----------
        self: TimeSeries instance
        seq: sequence

        Notes
        -----
        A better implementation might be to use
        and isinstance(seq, collections.Sequence)
        """
        try:
            _ = iter(seq)
        except TypeError as te:
            # J: unified string formatting with .format()
            raise TypeError("{} is not a valid sequence".format(seq))
