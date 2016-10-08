class TimeSeries:
	"""
    A class that stores a single, ordered set of numerical data.

    Parameters
    ----------
    initial_data : list
        This can be any object that can be treated like a sequence. It is mandatory.
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

	def __init__(self, initial_data):
		"""
	    The TimeSeries class constructor. It must be provided the initial data to fill the time series instance with.

	    Parameters
	    ----------
	    initial_data : list
	        This can be any object that can be treated like a sequence. It is mandatory.

	    Notes
    	-----
    	PRE: `initial_data` is sorted in non-decreasing order
    	POST:

	    INVARIANTS:

	    WARNINGS:

		"""
		self.data = initial_data

	def __len__(self):
		return len(self.data)

	def __getitem__(self, position):
		return self.data[position]

	def __setitem__(self, position, item):
		self.data[position] = item

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

# projecteuler.net/problem=1
# Note: this is decidely *not* the intended purpose of this class.

threes = TimeSeries(range(0,1000,3))
fives = TimeSeries(range(0,1000,5))

s = 0
for i in range(0,1000):
  if i in threes or i in fives:
    s += i

print("sum",s)