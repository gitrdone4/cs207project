# Implements StreamTimeSeriesInterface ABC.

from timeseriesinterface import TimeSeriesInterface
import abc

class StreamTimeSeriesInterface(TimeSeriesInterface):

    # just making sure that these don't conflict with
    # the @abstractmethods in TimeSeriesInterface
    def __add__(self):
        pass
    def __iter__(self):
        pass
    def __mul__(self):
        pass
    def __neg__(self):
        pass
    def __pos__(self):
        pass
    def __radd__(self):
        pass
    def __rmul__(self):
        pass
    def __rsub__(self):
        pass
    def __sub__(self):
        pass

    # need a way to represent these objects
    # def __repr__(self):
    #   pass

    # def __str__(self):
    #   pass