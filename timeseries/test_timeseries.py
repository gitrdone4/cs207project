from pytest import raises
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries

def threes_fives(class_name):
    """
    Check with fizbuzz data
    projecteuler.net/problem=1
    Note: this is decidely *not* the intended purpose of this class.
    """
    threes = class_name(range(0, 1000, 3))
    fives = class_name(range(0, 1000, 5))

    s = 0
    for i in range(0, 1000):
        if i in threes or i in fives:
            s += i

    assert s == 233168

def non_iterable(class_name):
    """Confirms we get a type error when we try to create time series with non-iterable"""
    with raises(TypeError):
        _ = class_name(42)

def iterable(class_name):
    """Confirms we *don't get a type error when we try to create time series with vairus iterables """
    class_name([1,2,3])
    class_name({'a':1,'b':2,'c':3})
    class_name(set([1,2,3]))

def incompatible_dimensions(class_name):
    """Confirm that we get a value error when time_input is not the same length as initial data"""
    with raises(ValueError):
        class_name([1] * 100,range(200))

def time_input_contains_repeats(class_name):
    """Confirm that we get a value error when time_input contains repeated values"""
    with raises(ValueError):
        class_name([1,2,3,4],[1,2,2,3])

    with raises(ValueError):
        class_name([1]*100,list(range(100))+[99])

def test_time_series():
    """Calles tests defined above on time series class"""
    threes_fives(TimeSeries)
    non_iterable(TimeSeries)
    iterable(TimeSeries)
    incompatible_dimensions(TimeSeries)
    time_input_contains_repeats(TimeSeries)

def test_array_time_series():
    """Calles tests defined above on array time series class"""
    threes_fives(ArrayTimeSeries)
    non_iterable(ArrayTimeSeries)
    iterable(ArrayTimeSeries)
    # These are not implemented in array time series yet
    #incompatible_dimensions(ArrayTimeSeries)
    #time_input_contains_repeats(ArrayTimeSeries)
