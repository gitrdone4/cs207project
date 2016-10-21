from pytest import raises
from lazy import LazyOperation
from lazy import lazy_add, lazy_mul

def test_isinstance():
    assert isinstance(lazy_add(1,2), LazyOperation) == True
    #add one for lazy_mul

def test_add():
    assert lazy_add(1,1).eval()==2