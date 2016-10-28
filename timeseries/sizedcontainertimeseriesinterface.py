from timeseriesinterface import TimeSeriesInterface
import abc

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
	"""
	Description
	-----------
	Abstract interface class for a TimeSeries of a fixed size.
	"""

	
	##############################################################################
	## ABSTRACT METHODS TO BE IMPLEMENTED BY ALL TIMESERIES OF FIXED LENGTH
	##############################################################################

	#J: Should these interfaces also contain implementations?
	# Python doesn't seem to make a real distinction between
	# Interfaces and ABCs! See http://bit.ly/2eOU0tk
	@abc.abstractmethod
	def __len__(self):
		"""
		Description
		-----------
		All TimeSeries of fixed length must implement __len__
		"""
		pass

	@abc.abstractmethod
	def __getitem__(self):
		"""
		Description
		-----------
		All TimeSeries of fixed length must support index-based item retrieval
		"""

	@abc.abstractmethod
	def __setitem__(self):
		"""
		Description
		-----------
		All TimeSeries of fixed length must support index-based item retrieval
		"""
		pass

	@abc.abstractmethod
	def __contains__(self, needle):
		"""
		Description
		-----------
		A TimeSeries of fixed length must support checking whether it contains an item
		"""
		pass

	@abc.abstractmethod
	def __repr__(self):
		"""
		Description
		-----------
		Internal String representation for TimeSeries
		"""
		pass
	
	@abc.abstractmethod
	def __str__(self):
		"""
		Description
		-----------
		User-friendly representation for TimeSeries
		"""
		pass
	
	@abc.abstractmethod
	def __abs__(self):
		"""
		Description
		-----------
		"Absolute value" of TimeSeries, e.g. vector norm
		"""
		pass

	@abc.abstractmethod
	def __bool__(self):
		"""
		Description
		-----------
		Checks if TimeSeries values are empty?
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

	##############################################################################
	## GLOBAL HELPER METHODS FOR ALL CONTAINER TIME SERIES.
	## NO NEED TO IMPLEMENT IN SUBCLASS.
	##############################################################################

	@staticmethod
	def _check_length_helper(lhs , rhs):
		if not len(lhs)==len(rhs):
			raise ValueError(str(lhs)+' and '+str(rhs)+' must have the same length')

	
	# makes check lengths redundant. However I keep them separate in case we want 
    # to add functionality to add objects without a defined time dimension later.
	@staticmethod
	def _check_time_domains_helper(lhs , rhs):
		if not lhs._times==rhs._times:
			raise ValueError(str(lhs)+' and '+str(rhs)+' must have identical time domains')






