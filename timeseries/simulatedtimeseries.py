from streamtimeseriesinterface import StreamTimeSeriesInterface

class SimulatedTimeSeries(StreamTimeSeriesInterface):
	"""
	Description
	-----------
	Implements a Time Series without a fixed storage.
	Uses generators to produce a streaming effect.

	Parameters
	----------
	times_gen: generator
		lazily evaluated generator representing time values
	values: generator
		lazily evaluated generator representing data values
	"""
	def __init__(self, times_gen, values_gen):
		super(SimulatedTimeSeries, self).__init__()
		self.times = times_gen
		self.values = values_gen

	def produce(self, chunk):
		"""
		Description
		-----------
		Produces `chunk` new values of the time series

		Parameters
		----------
		self: SimulatedTimeSeries instance
		chunk: int
			"chunk size", i.e. number of values to produce

		Returns
		-------
		list consisting of `chunk` (time, ts_value) pairs
		"""

		try:
			produced = [(next(self.times), next(self.values)) for _ in range(chunk)]

		except StopIteration:
			# not sure what the optimal error type is here
			raise IndexError("Make sure you don't produce more values than the generator has!")

		return produced