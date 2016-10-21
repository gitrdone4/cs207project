from pytest import raises
from lazy import LazyOperation
from lazy import lazy_add, lazy_mul

def test_isinstance():
    assert isinstance(lazy_add(1,1), LazyOperation) == True
    assert isinstance(lazy_mul(5,1), LazyOperation) == True

def test_add():
    assert lazy_add(1,1).eval() == 2
    assert lazy_add(2,8).eval() == 10

def test_mul():
    assert lazy_mul(5,1).eval() == 5