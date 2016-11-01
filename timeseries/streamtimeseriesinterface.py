# Implements StreamTimeSeriesInterface ABC.

from timeseriesinterface import TimeSeriesInterface
import abc

class StreamTimeSeriesInterface(TimeSeriesInterface):

	# just making sure that these don't conflict with
	# the @abstractmethods in TimeSeriesInterface
	def __add__(self):
		"""
		"""

	def __iter__(self):
		"""
		"""

	def __mul__(self):
		"""
		"""
	def __neg__(self):
		"""
		"""
	def __pos__(self):
		"""
		"""
	def __radd__(self):
		"""
		"""
	def __rmul__(self):
		"""
		"""
	def __rsub__(self):
		"""
		"""
	def __sub__(self):
		"""
		"""

	def std(self, chunk = None):
		"""
		"""

	def mean(self, chunk = None):
		"""
		"""

	def produce(self, chunk=1):
		"""
		Description
		-----------
		Produces `chunk` new values of the time series
		"""

	def online_mean():
		"""
		Description
		-----------
		Generates a stream of online means.
		"""

	def online_std():
		"""
		Description
		-----------
		Generates a stream of online standard deviations.
		"""

	def mean(self, chunk = None):
		"""
		"""
	def std(self, chunk = None):
		"""
		"""

    # need a way to represent these objects
    # def __repr__(self):
    #   pass

    # def __str__(self):
    #   pass