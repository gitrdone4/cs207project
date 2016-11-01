from pytest import raises
import pytest
from timeseries import TimeSeries
from arraytimeseries import ArrayTimeSeries
from simulatedtimeseries import SimulatedTimeSeries
import numpy as np
from lazy import lazy
from lazy import LazyOperation

def test_sized_container_timeseries():
    """calls tests on *both* TimeSeries and ArrayTimeSeries"""
    for class_name in [TimeSeries,ArrayTimeSeries]:
        non_iterable(class_name)
        iterable(class_name)
        incompatible_dimensions(class_name)
        times_contains_repeats(class_name)
        index_in_time_series(class_name)
        index_not_in_time_series(class_name)
        correct_length(class_name)
        interpolate_ts(class_name)
        method_getitem(class_name)
        method_setitem(class_name)
        method_iter(class_name)
        method_contains(class_name)
        method_values(class_name)
        method_itervalues(class_name)
        method_times(class_name)
        method_itertimes(class_name)
        method_items(class_name)
        method_iteritems(class_name)
        method_len(class_name)
        method_eq(class_name)
        method_pos(class_name)
        method_neg(class_name)
        method_add_int(class_name)
        method_add_two_timeseries(class_name)
        method_sub_int(class_name)
        method_sub_two_timeseries(class_name)
        method_mul_int(class_name)
        method_mul_two_timeseries(class_name)
        method_ne(class_name)
        method_produce()

def test_time_series():
    """Calles tests on list-based timeseries class exclusively"""
    threes_fives(TimeSeries)
    verify_lazy_property_time_series(TimeSeries)
    verify_lazyfied_time_series_check_length(TimeSeries)
    add_timeseries_nparray_not_allowed(TimeSeries)
    add_timeseries_list_not_allowed(TimeSeries)
    sub_timeseries_nparray_not_allowed(TimeSeries)
    sub_timeseries_list_not_allowed(TimeSeries)
    mul_timeseries_nparray_not_allowed(TimeSeries)
    mul_timeseries_list_not_allowed(TimeSeries)
    # Code for these tests still needs to be abtracted to sizedcontainertimeseries interface

##############################################################################
## Unit Tests
##############################################################################

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

# J: why are we using `class_name` as an arg
# if this is only to be used for ArrayTimeSeries
# def update_get_array_time_series_by_index(class_name):
#     """ Confirm that we can set a new time and value for a given index in ArrayTimeSeries"""
#     ts = class_name(values=[1,2,3,4,5],times=[1,2,3,4,5])
#     assert ts[1] == (2,2)
#     ts[1] = (42,42)
#     assert ts[1] == (42,42)

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

def verify_lazy_property_time_series(class_name):
    ts = class_name([1,2,3,4,5],[1,2,3,4,5])

    # verify that TimeSeries.lazy is a LazyOperation
    assert isinstance(ts.lazy, LazyOperation) == True

    # verify that ts and ts.lazy.eval() give identical results
    assert ts == ts.lazy.eval()

def verify_lazyfied_time_series_check_length(class_name):
    """A check length method to verify the lazy property method in the TimeSeries class."""
    @lazy
    def check_length(a,b):
        return len(a)==len(b)
    thunk = check_length(class_name(range(0,4),range(1,5)), class_name(range(1,5),range(2,6)))
    assert thunk.eval()==True

def add_timeseries_nparray_not_allowed(class_name):
    """
        It should fail when we try to add a numpy array or list to a TimeSeries instance
    """
    ts = class_name(values=[1,2,3] , times=[1,2,3])
    with raises(TypeError):
        rhs = np.array([1,2,3])
        ts + rhs

def add_timeseries_list_not_allowed(class_name):
    """
        It should fail when we try to add a numpy array or list to a TimeSeries instance
    """
    ts = class_name(values=[1,2,3] , times=[1,2,3])
    with raises(TypeError):
        rhs = list([1,2,3])
        ts + rhs

def sub_timeseries_nparray_not_allowed(class_name):
    """
        It should fail when we try to add a numpy array or list to a TimeSeries instance
    """
    ts = class_name(values=[1,2,3] , times=[1,2,3])
    with raises(TypeError):
        rhs = np.array([1,2,3])
        ts - rhs

def sub_timeseries_list_not_allowed(class_name):
    """
        It should fail when we try to add a numpy array or list to a TimeSeries instance
    """
    ts = class_name(values=[1,2,3] , times=[1,2,3])
    with raises(TypeError):
        rhs = list([1,2,3])
        ts - rhs

def mul_timeseries_nparray_not_allowed(class_name):
    """
        It should fail when we try to add a numpy array or list to a TimeSeries instance
    """
    ts = class_name(values=[1,2,3] , times=[1,2,3])
    with raises(TypeError):
        rhs = np.array([1,2,3])
        ts * rhs

def mul_timeseries_list_not_allowed(class_name):
    """
        It should fail when we try to add a numpy array or list to a TimeSeries instance
    """
    ts = class_name(values=[1,2,3] , times=[1,2,3])
    with raises(TypeError):
        rhs = list([1,2,3])
        ts * rhs

# should have made a fixture sorry!
def method_getitem(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert threes[1] == 3

def method_setitem(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    threes[0] = 3
    assert threes[0] == 3

def method_contains(class_name):
    x = class_name(values=[5,6],times=[1,2])
    assert 5 in x

def method_iter(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    cum_sum = 0
    for val in threes:
        cum_sum += val
    assert cum_sum==18

def method_values(class_name):
    #N: Changed from np array to list
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert isinstance(threes.values(), np.ndarray)

def method_itervalues(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    cum_sum = 0
    for val in threes.itervalues():
        cum_sum += val
    assert cum_sum==18

def method_times(class_name):
    #N: Changed from np array to list
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

def method_pos(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    posthrees = +threes
    assert posthrees.values_lst() == [0,3,6,9]

def method_neg(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    negthrees = -threes
    assert negthrees.values_lst()==[0,-3,-6,-9]

def method_add_int(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    add_v1 = threes + 5
    add_v2 = 5 + threes
    assert add_v1.values_lst() == [5,8,11,14] and add_v2.values_lst() == [5,8,11,14]

def method_add_two_timeseries(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    fives = class_name(values=range(0, 16, 5),times=range(100,104))
    add_v1 = threes+fives
    add_v2 = fives+threes
    assert add_v1.values_lst()==[0,8,16,24] and add_v2.values_lst()==[0,8,16,24]

def method_sub_int(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    sub_v1 = threes - 5
    sub_v2 = -(5 - threes)
    assert sub_v1.values_lst()==[-5,-2,1,4] and sub_v2.values_lst()==[-5,-2,1,4]

def method_sub_two_timeseries(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    fives = class_name(values=range(0, 16, 5),times=range(100,104))
    sub_v1 = threes-fives
    sub_v2 = -(fives-threes)
    assert sub_v1.values_lst()==[0,-2,-4,-6] and sub_v2.values_lst()==[0,-2,-4,-6]

def method_mul_int(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    mul_v1 = threes * 5
    mul_v2 = 5 * threes
    assert mul_v1.values_lst()==[0,15,30,45] and mul_v2.values_lst()==[0,15,30,45]

def method_mul_two_timeseries(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    fives = class_name(values=range(0, 16, 5),times=range(100,104))
    mul_v1 = threes*fives
    mul_v2 = fives*threes
    assert mul_v1.values_lst()==[0,15,60,135] and mul_v2.values_lst()==[0,15,60,135]

def method_eq(class_name):
    eq_v1 = class_name(values=range(0, 10, 3),times=range(100,104))
    eq_v2 = class_name(values=range(0, 10, 3),times=range(100,104))
    assert eq_v1==eq_v2

def method_ne(class_name):
    eq_v1 = class_name(values=range(0, 10, 3),times=range(100,104))
    eq_v2 = -eq_v1
    assert eq_v1!=eq_v2

def method_mean(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert threes.mean()==4.5

def method_std(class_name):
    threes = class_name(values=range(0, 10, 3),times=range(100,104))
    assert threes.std()==3.3541019662496847

def method_produce():
    t = iter(range(1,11))
    v = iter([2*x + 1 for x in range(1,11)])
    sts = SimulatedTimeSeries(t, v)
    assert sts.produce(3) == [(1,3), (2,5), (3,7)]