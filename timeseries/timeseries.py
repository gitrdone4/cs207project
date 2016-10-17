class TimeSeries:
    """
    A class that stores a single, ordered set of numerical data.

    Parameters
    ----------
    initial_data : list
        This can be any object that can be treated like a sequence. Mandatory.
    time_input : list
        This can be any object that can be treated like a sequence. Optional.
        If it is not supplied, equally spaced integers are used instead.
    position: int
        The index position at which the requested item should be inserted

    Notes
    -----
    PRE: `initial_data` is sorted in non-decreasing order
    POST:

    INVARIANTS:

    WARNINGS:
        - This class does not maintain an accurate time series if it is provided an unsorted array
    """


    # J: maximum length of `initial_data` after which
    # abbreviation will occur in __str__() and __repr__()
    MAX_LENGTH = 10


    def __init__(self, initial_data, time_input=None):
        """
        The TimeSeries class constructor. It must be provided the initial data
        to fill the time series instance with.

        Parameters
        ----------
        initial_data : sequence-like
            This can be any object that can be treated like a sequence. Mandatory.
        time_input : sequence-like
            This can be any object that can be treated like a sequence. Optional.
            If None, equally spaced integers are used instead.

        Notes
        -----
        PRE: If time_input is not provided, `initial_data` must be sorted
        POST:

        INVARIANTS:
        inital_data and time_input (if provided) must be sequences.

        WARNINGS:

        """

        # Confirm inital_data is a sequence.

        # J: unit test this
        # N: done
        # J: all Python sequences implement __iter__(), which we can use here.
        self.is_sequence(initial_data)
        self.data = list(initial_data)

        if time_input:

            # R: haven't checked if time_input is iterable. make this a precondition?
            # J: can't we simply test for this as well?
            self.is_sequence(time_input)
            self.time = list(time_input)

        else:
            self.time = list(range(len(self.data)))

        if len(self.time)!=len(self.data):

            # R: unit test me
            # N: Done.
            raise ValueError("Time and input data of incompatible dimensions")

        if len(self.time)!=len(set(self.time)):

            # R: unit test me. consider moving to precondition
            # N: Done. 
            raise ValueError("Time data should contain no repeats")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, position):
        if position not in self.time:
            # R: unit test me
            raise ValueError("Choose t from time column")
        return self.data[self.time.index(position)]

    def __setitem__(self, position, item):
        if position not in self.time:
            # R: unit test me
            raise ValueError("Choose t from time column")
        self.data[self.time.index(position)] = item

    def __iter__(self):
        for val in self.data:
            yield val

    def itertimes(self):
        for tim in self.time:
            yield tim

    def iteritems(self):
        for i in range(len(self.data)):
            yield self.time[i], self.data[i]

    def __repr__(self):

        class_name = type(self).__name__
        return '{}(Length: {}, {})'.format(class_name, len(self.data), str(self))

    def __str__(self):
        """
        Description
        -----------
        Instance method for pretty-printing the TimeSeries instance

        Parameters
        ----------
        self: TimeSeries instance

        Returns
        -------
        pretty_printed: string
            an end user friendly printed message that represents the time series
            numerical sequence. If the sequence is longer than `MAX_LENGTH`
            values, the printout will be the first three numbers followed by
            an ellipsis and ending with the last three numbers in the sequence.

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
            pretty_printed = "{}".format(list(self.data))

        return pretty_printed


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
