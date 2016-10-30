from pytest import raises
from simulatedtimeseries import SimulatedTimeSeries

def test_chunk_out_of_range():

	with raises(StopIteration):

		chunk = 200

		test_range = range(chunk)

		times_gen = (t for t in [1,2,3])
		values_gen = (v for v in [1,2,3])
		ts = SimulatedTimeSeries(times_gen, values_gen)
		produced = [(next(ts.times), next(ts.values)) for _ in range(chunk)]