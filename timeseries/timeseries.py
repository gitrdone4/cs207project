class TimeSeries:
    """
    A class that stores a single, ordered set of numerical data.

    Parameters
    ----------
    initial_data : list
        This can be any object that can be treated like a sequence. It is mandatory.
    time_input : list
        This can be any object that can be treated like a sequence. It is optional. If it is not supplied, equally spaced integers are used instead.
    position: int
        the index position at which the requested item should be inserted

    Notes
    -----
    PRE: `initial_data` is sorted in non-decreasing order
    POST:

    INVARIANTS:

    WARNINGS:
        - This class does not maintain an accurate time series if it is provided an unsorted array
    """

    def __init__(self, initial_data, time_input=None):
        """
        The TimeSeries class constructor. It must be provided the initial data to fill the time series instance with.

        Parameters
        ----------
        initial_data : list
            This can be any object that can be treated like a sequence. It is mandatory.
        time_input : list
            This can be any object that can be treated like a sequence. It is optional. If it is not supplied, equally spaced integers are used instead.

        Notes
        -----
        PRE: If time_input is not provided, `initial_data` must be sorted
        POST:

        INVARIANTS:
        inital_data and time_input (if provided) must be sequences. 

        WARNINGS:

        """

        # Confirm inital_data is a sequence. 
        try: 
            _ = (e for e in initial_data) # R: O(n) to check if iterable. can we stop this earlier?
        except TypeError:
            raise TypeError("%s is not iterable" % initial_data) # R: moved print into error msg R
        else:
            self.data = list(initial_data)
        
        if time_input!=None:
            self.time = list(time_input) # R: haven't checked if time_input is iterable. make this a precondition?
        else:
            self.time = list(range(len(self.data)))
            
        if len(self.time)!=len(self.data):
            raise ValueError("Time and input data of incompatible dimensions") # R: unit test me
        
        if len(self.time)!=len(set(self.time)):
            raise ValueError("Time data should contain no repeats") # R: unit test me. consider moving to precondition

    def __len__(self):
        return len(self.data)

    def __getitem__(self, position):
        try:
            _ = self.time.index(position)
        except ValueError:
            raise ValueError("Time value error: choose t from time column") # R: unit test me
        return self.data[self.time.index(position)]
        
    def __setitem__(self, position, item):
        try:
            _ = self.time.index(position)
        except ValueError:
            raise ValueError("Time value error: choose t from time column") # R: unit test me
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

        if len(self.data) > 10:
            print_data = "["+str(self.data[0])+","+str(self.data[1])+","+str(self.data[2])+",...,"+str(self.data[-3])+","+ str(self.data[-2])+","+ str(self.data[-1])+"]"
            return '{}(Length: {}, {})'.format(class_name, len(self.data), print_data)
        else:
            return '{}(Length: {}, {})'.format(class_name, len(self.data), self.data)

    def __str__(self):
        """
        The TimeSeries class constructor. It must be provided the initial data to fill the time series instance with.

        Parameters
        ----------

        Returns
        -------
        print_data: string
            an end user friendly printed message that represents the time series numerical sequence. If the 
            sequence is longer than 10 values, the printout will be the first three numbers followed by 
            an ellipsis and ending with the last three numbers in the sequence. 

        Notes
        -----
        PRE:
        POST:

        INVARIANTS:

        WARNINGS:

        """
        if len(self.data) > 10:
            print_data = "["+str(self.data[0])+","+str(self.data[1])+","+str(self.data[2])+",...,"+str(self.data[-3])+","+ str(self.data[-2])+","+ str(self.data[-1])+"]"
            return print_data
        else:
            return '{}'.format(self.data)

## projecteuler.net/problem=1
## Note: this is decidely *not* the intended purpose of this class.
#

# threes = TimeSeries(range(0,1000,3))
# fives = TimeSeries(range(0,1000,5))

# s = 0
# for i in range(0,1000):
#  if i in threes or i in fives:
#    s += i

# print("sum",s)
# print(threes)