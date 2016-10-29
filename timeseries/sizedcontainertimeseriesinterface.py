
from timeseriesinterface import TimeSeriesInterface
import numpy as np
import abc

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
	"""
	Description
	-----------
	Abstract interface class for a TimeSeries of a fixed size.
	"""

	## NOTES (clean up later before tuesday):
	# J: how to cleanly enforce that all subclasses
	# of SizedContainerTimeSeriesInterface implement
	# self._values and self._times ??

	# J: maximum length of `values` after which
	# abbreviation will occur in __str__() and __repr__()
	MAX_LENGTH = 10

	###############################################################
	## Abstract methods that are defined differently for different
	## subclasses of SizedContainerTimeSeriesInterface
	###############################################################

	@abc.abstractmethod
	def __len__(self):
		"""
		Description
		-----------
		All TimeSeries of fixed length must implement __len__.
		"""
		pass

	@abc.abstractmethod
	def __eq__(self):
		"""
		Description
		-----------
		All TimeSeries of fixed size must support equality checking with '=='
		"""
		pass
	
	@abc.abstractmethod
	def __ne__(self):
		"""
		Description
		-----------
		All TimeSeries of fixed size must support the '!='' operator
		"""
		pass

	###############################################################
	## Methods with the same implementation for all subclasses
	## of SizedContainerTimeSeriesInterface.
	###############################################################

	def __iter__(self):
		"""
		Description
		-----------
		Iterates over `self._values`.
		Equivalent to calling iter() on the instance.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface
		"""
		for val in self._values:
			yield val

	def itertimes(self):
		"""
		Description
		------------
		Iterates over the times in `self._times`

		Parameters
		----------
		self: instance of subclass of SizedTimeSeriesInterface

		Returns
		-------
		Yields values from `self._times`

		Notes
		-----
		"""
		for tim in self._times:
			yield tim

	def itervalues(self):
		"""
		Description
		------------
		Iterates over the values of the time eries
		
		Parameters
		----------
		self: instance of subclass of SizedTimeSeriesInterface
		
		Returns
		-------
		Yields values from `self._values`

		Notes
		-----
		Identical to iter(self)
		"""
		for val in self._values:
			yield val

	def iteritems(self):
		"""
			Description
			------------
			Iterates over (time, value) tuples of the time series

			Parameters
			----------
			self: instance of subclass of SizedTimeSeriesInterface

			Returns
			-------
			Yields (time, value) tuples

			Notes
			-----
		"""
		for i in range(len(self._values)):
			yield self._times[i], self._values[i]

	def __getitem__(self, index):
		"""
		Description
		-----------
		Instance method for indexing into a fixed-size Time Series.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		The value of `self._values` located at index `index`.
		"""
		try:    
			return self._values[index]
		except IndexError:
			raise IndexError("Index out of bounds!")

	def __setitem__(self, index, item):
		"""
		Description
		-----------
		Sets the element of `self._values`
		at index `index` equal to `item`. 

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface
		index: int
			index to change values at
		item: tuple
			(time, value) tuple
		"""
		try:
			self._values[index] = item
		except IndexError:
			raise IndexError("Index out of bounds!")

	def __contains__(self, needle):
		"""
		Description
		-----------
		Checks if `needle` is contained in `self._values`

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface
		needle: float
			Time series value to search for

		Returns
		-------
		True if `needle` found in `self._values`, else False
		"""
		return needle in self._values

	def __repr__(self):
		"""
		Description
		-----------
		Internal String representation for all subclasses of
		SizedContainerTimeSeriesInstance
		"""
		class_name = self.__class__.__name__
		return '{}(Length: {}, {})'.format(class_name,
											len(self._values),
											str(self))
	
	def __str__(self):
		"""
		Description
		-----------
		Instance method for pretty-printing the time series contents.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		pretty_printed: string
		    an end-user-friendly printout of the time series.
		    If `len(self._values) > MAX_LENGTH`, printout abbreviated
		    using an ellipsis: `['a','b','c', ..., 'x','y','z']`.

		Notes
		-----
		PRE:
		POST:

		INVARIANTS:

		WARNINGS:
		"""
		if len(self._values) > self.MAX_LENGTH:
			needed = self._values[:3]+self._values[-3:]
			pretty_printed = "[{} {} {}, ..., {} {} {}]".format(*needed)

		else:
			pretty_printed = "{}".format(list(self._values))

		return pretty_printed

	
	def __abs__(self):
		"""
		Description
		-----------
		Returns the L2-norm of `self._values`

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		L2-norm as a float

		Notes
		-----
		Casts `self._values` into a np-array for fasted norm calcualtion.
		This won't impact the final return value, as it is a float.
		"""
		return (np.array(self._values)**2).sum()

	def __bool__(self):
		"""
		Description
		-----------
		Checks if `self._values` is empty.

		Parameters
		----------
		self: instance of subclass of SizedContainerTimeSeriesInterface

		Returns
		-------
		True/False
		"""
		return bool(abs(self._values))


	# J: why do these return np.arrays? 
	def values(self):
		return np.array(self._values)

	def times(self):
		return np.array(self._times)

	def items(self):
		return list(zip(self._times, self._values))


	##############################################################################
	## GLOBAL HELPER METHODS FOR ALL CONTAINER TIME SERIES.
	## NO NEED TO IMPLEMENT IN SUBCLASS.
	##############################################################################

	@staticmethod
	def _check_length_helper(lhs, rhs):
		if not len(lhs)==len(rhs):
			raise ValueError(str(lhs)+' and '+str(rhs)+' must have the same length')

	
	# makes check lengths redundant. However I keep them separate in case we want 
	# to add functionality to add objects without a defined time dimension later.
	@staticmethod
	def _check_time_domains_helper(lhs, rhs):

		# J: casting to list here since comparing np.arrays
		# with == yields a boolean array with results of elemwise
		# comparinsons.
		if not list(lhs._times)==list(rhs._times):
			raise ValueError(str(lhs)+' and '+str(rhs)+' must have identical time domains')

	@staticmethod
	def is_sequence(seq):
		"""
		Description
		-----------
		Checks if `seq` is a sequence by verifying if it implements __iter__.
		Parameters
		----------
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
