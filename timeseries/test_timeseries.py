from pytest import raises
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries
import numpy as np

def threes_fives(class_name):
    """
    Check with fizbuzz data
    projecteuler.net/problem=1
    Note: this is decidely *not* the intended purpose of this class.
    """
    threes = class_name(values=range(0, 1000, 3))
    fives = class_name(values=range(0, 1000, 5))

    s = 0
    for i in range(0, 1000):
        if i in threes or i in fives:
            s += i

    assert s == 233168


def non_iterable(class_name):
    """
    Confirms we get a type error when we try
    to create time series with non-iterable.
    """
    with raises(TypeError):
        _ = class_name(values=42,times=42)


def iterable(class_name):
    """
    Confirms we *don't get a type error when we try
    to create time series with various iterables.
    """
    class_name(values=[1, 2, 3],times=[1,2,3])
    class_name(values={'a': 1, 'b': 2, 'c': 3},times=[1,2,3])
    class_name(values=set([1, 2, 3]),times=[1,2,3])


def incompatible_dimensions(class_name):
    """
    Confirm that we get a value error when times
    is not the same length as initial data.
    """
    with raises(ValueError):
        class_name(values=[1] * 100, times=range(200))


def times_contains_repeats(class_name):
    """
    Confirm that we get a value error when times
    contains repeated values.
    """
    with raises(ValueError):
        class_name(values=[1, 2, 3, 4], times=[1, 2, 2, 3])

    with raises(ValueError):
        class_name(values=[1]*100, times=list(range(100))+[99])

def index_in_time_series(class_name):
    """
    Confirm that get_item and set_item work as expected
    """
    ts = class_name(values=[1,2,3],times=[1,2,3])
    assert ts[2] == 3
    ts[2] = 10
    assert ts[2] == 10


def index_not_in_time_series(class_name):
    """
    Confirm that we get a value error when we
    attempt to access or set an non-existing value
    """
    ts = class_name(values=[1,2,3],times=[1,2,3])

    with raises(IndexError):
        _ = ts[4]

    with raises(IndexError):
        ts[5] = 5

def correct_length(class_name):
    ts = class_name(values=[1] * 100, times=range(100))
    assert len(ts) == 100

def update_get_array_time_series_by_index(class_name):
    """ Confirm that we can set a new time and value for a given index in ArrayTimeSeries"""
    ts = class_name([1,2,3,4,5],[1,2,3,4,5])
    assert ts[1] == (2,2)
    ts[1] = (42,42)
    assert ts[1] == (42,42)

def interpolate_ts(class_name):
    a = class_name(values=[1,2,3],times=[0,5,10])
    b = class_name(values=[100, -100],times=[2.5,7.5])

    c_times=[5,10,15,20]
    c = class_name(values=[i*2 for i in c_times],times=c_times)

    # Simple cases
    assert a.interpolate([1]) == class_name(times=[1],values=[1.2])

    assert c.interpolate([2,6,11,17,25]) == \
        class_name(times=[2,6,11,17,25],values=[10,12,22,34,40])

    assert b.interpolate([-100,100]) == \
        class_name(times=[-100,100],values=[100,-100])


def test_time_series():
    """Calles tests defined above on time series class"""
    threes_fives(TimeSeries)
    non_iterable(TimeSeries)
    iterable(TimeSeries)
    incompatible_dimensions(TimeSeries)
    times_contains_repeats(TimeSeries)
    index_in_time_series(TimeSeries) # (Fixed) get item changed! gets value based on index rather than time now
    index_not_in_time_series(TimeSeries) # (Fixed) get item changed! gets value based on index rather than time now
    correct_length(TimeSeries)
    interpolate_ts(TimeSeries)

def test_array_time_series():
    """Calles tests defined above on array time series class"""
    # threes_fives(ArrayTimeSeries)
    non_iterable(ArrayTimeSeries)
    iterable(ArrayTimeSeries)
    # These are not implemented in array time series yet
    # index_not_in_time_series(ArrayTimeSeries)
    # correct_length(ArrayTimeSeries)
    # incompatible_dimensions(ArrayTimeSeries)
    # times_contains_repeats(ArrayTimeSeries)
    update_get_array_time_series_by_index(ArrayTimeSeries)
    #interpolate_ts(ArrayTimeSeries)

# The following tests are interface checks - easy examples that don't handle edge cases

def test_interface():
    method_getitem(TimeSeries)
    method_setitem(TimeSeries)
    method_contains(TimeSeries)
    method_iter(TimeSeries)
    method_values(TimeSeries)
    method_itervalues(TimeSeries)
    method_times(TimeSeries)
    method_itertimes(TimeSeries)
    method_items(TimeSeries)
    method_iteritems(TimeSeries)
    method_len(TimeSeries)
    method_neg(TimeSeries)
    method_add_int(TimeSeries)
    method_add_two_timeseries(TimeSeries)
    method_sub_int(TimeSeries)
    method_sub_two_timeseries(TimeSeries)
    method_mul_int(TimeSeries)
    method_mul_two_timeseries(TimeSeries)
    method_eq(TimeSeries)
    method_ne(TimeSeries)

# should have made a fixture sorry!
def method_getitem(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert threes[1] == 3

def method_setitem(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    threes[0] = 3
    assert threes[0] == 3

def method_contains(class_name):
    x = class_name([5,6])
    assert 5 in x

def method_iter(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    cum_sum = 0
    for val in threes:
        cum_sum += val
    assert cum_sum==18

def method_values(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert isinstance(threes.values(), np.ndarray)

def method_itervalues(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    cum_sum = 0
    for val in threes.itervalues():
        cum_sum += val
    assert cum_sum==18

def method_times(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert isinstance(threes.times(), np.ndarray)

def method_itertimes(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    cum_sum = 0
    for time in threes.itertimes():
        cum_sum += time
    assert cum_sum==406

def method_items(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert threes.items()==[(100,0),(101,3),(102,6),(103,9)]

def method_iteritems(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    cum_sum_time = 0
    cum_sum_value = 0
    for time, value in threes.iteritems():
        cum_sum_time += time
        cum_sum_value += value
    assert cum_sum_time==406 and cum_sum_value==18

def method_len(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert len(threes)==4

def method_neg(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    negthrees = -threes
    assert negthrees.data==[0,-3,-6,-9]

def method_add_int(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    add_v1 = threes + 5
    add_v2 = 5 + threes
    assert add_v1.data==[5,8,11,14] and add_v2.data==[5,8,11,14]

def method_add_two_timeseries(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    fives = class_name(values=range(0, 16, 5),times=range(100,104))
    add_v1 = threes+fives
    add_v2 = fives+threes
    assert add_v1.data==[0,8,16,24] and add_v2.data==[0,8,16,24]

def method_sub_int(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    sub_v1 = threes - 5
    sub_v2 = -(5 - threes)
    assert sub_v1.data==[-5,-2,1,4] and sub_v2.data==[-5,-2,1,4]

def method_sub_two_timeseries(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    fives = class_name(values=range(0, 16, 5),times=range(100,104))
    sub_v1 = threes-fives
    sub_v2 = -(fives-threes)
    assert sub_v1.data==[0,-2,-4,-6] and sub_v2.data==[0,-2,-4,-6]

def method_mul_int(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    mul_v1 = threes * 5
    mul_v2 = 5 * threes
    assert mul_v1.data==[0,15,30,45] and mul_v2.data==[0,15,30,45]

def method_mul_two_timeseries(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    fives = class_name(values=range(0, 16, 5),times=range(100,104))
    mul_v1 = threes*fives
    mul_v2 = fives*threes
    assert mul_v1.data==[0,15,60,135] and mul_v2.data==[0,15,60,135]

def method_eq(class_name):
    eq_v1 = class_name(values=range(0, 10, 3),times=range(100,104))
    eq_v2 = class_name(values=range(0, 10, 3),times=range(100,104))
    assert eq_v1==eq_v2

def method_ne(class_name):
    eq_v1 = class_name(values=range(0, 10, 3),times=range(100,104))
    eq_v2 = -eq_v1
    assert eq_v1!=eq_v2
