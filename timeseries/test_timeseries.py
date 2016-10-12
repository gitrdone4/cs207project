from pytest import raises
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries

def threes_fives(class_name):
    # projecteuler.net/problem=1
    # Note: this is decidely *not* the intended purpose of this class.
    threes = class_name(range(0,1000,3))
    fives = class_name(range(0,1000,5))
    
    s = 0
    for i in range(0,1000):
      if i in threes or i in fives:
        s += i
    
    assert(s == 233168)

def non_iterable(class_name):
    #Confirms we get a type error when we try to create with non-iterable
    with raises(TypeError):
            non_iterable = class_name(42)

def test_TimeSeries():
    threes_fives(TimeSeries)
    non_iterable(TimeSeries)

def test_ArrayTimeSeries():
    threes_fives(ArrayTimeSeries)
    non_iterable(ArrayTimeSeries)