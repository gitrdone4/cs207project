from pytest import raises
from timeseries import TimeSeries
import numpy as np

def test_threes_fives():
    # projecteuler.net/problem=1
    # Note: this is decidely *not* the intended purpose of this class.
    threes = TimeSeries(range(0,1000,3))
    fives = TimeSeries(range(0,1000,5))
    
    s = 0
    for i in range(0,1000):
      if i in threes or i in fives:
        s += i
    
    assert(s == 233168)

def test_non_iterable():
    #Confirms we get a type error when we try to create with non-iterable
    with raises(TypeError):
            non_iterable = TimeSeries(42)
   