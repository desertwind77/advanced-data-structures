#!/usr/bin/env python3

import pytest
from FenwickTree import Array, PrefixSumArray, FenwickTree, RangeQueryBase


IMPLEMENTATIONS = [Array, PrefixSumArray, FenwickTree]


@pytest.fixture(params=IMPLEMENTATIONS, ids=lambda c: c.__name__)
def impl(request) -> RangeQueryBase:
    return request.param([3, 1, 4, 1, 5, 9, 2, 6])


# --- range_query ---

def test_single_element(impl):
    assert impl.range_query(0, 0) == 3
    assert impl.range_query(4, 4) == 5

def test_full_range(impl):
    assert impl.range_query(0, 7) == 31

def test_partial_range(impl):
    assert impl.range_query(2, 5) == 19   # 4+1+5+9
    assert impl.range_query(0, 3) == 9    # 3+1+4+1

def test_last_element(impl):
    assert impl.range_query(7, 7) == 6

def test_range_starting_at_zero(impl):
    assert impl.range_query(0, 4) == 14   # 3+1+4+1+5


# --- update then range_query ---

def test_update_middle(impl):
    impl.update(3, 10)
    assert impl.range_query(3, 3) == 10
    assert impl.range_query(0, 3) == 18   # 3+1+4+10
    assert impl.range_query(2, 5) == 28   # 4+10+5+9

def test_update_first(impl):
    impl.update(0, 0)
    assert impl.range_query(0, 0) == 0
    assert impl.range_query(0, 7) == 28

def test_update_last(impl):
    impl.update(7, 100)
    assert impl.range_query(7, 7) == 100
    assert impl.range_query(0, 7) == 125

def test_update_same_value(impl):
    original = impl.range_query(2, 4)
    impl.update(3, 1)   # same as original value
    assert impl.range_query(2, 4) == original

def test_multiple_updates(impl):
    impl.update(0, 10)
    impl.update(0, 20)
    assert impl.range_query(0, 0) == 20


# --- cross-implementation consistency ---

def test_all_implementations_agree():
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    impls = [cls(data) for cls in IMPLEMENTATIONS]
    for left in range(len(data)):
        for right in range(left, len(data)):
            results = [impl.range_query(left, right) for impl in impls]
            assert len(set(results)) == 1, f"Mismatch at [{left},{right}]: {results}"

def test_all_implementations_agree_after_update():
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    impls = [cls(data) for cls in IMPLEMENTATIONS]
    for impl in impls:
        impl.update(3, 10)
    for left in range(len(data)):
        for right in range(left, len(data)):
            results = [impl.range_query(left, right) for impl in impls]
            assert len(set(results)) == 1, f"Mismatch at [{left},{right}]: {results}"


# --- bounds checking ---

def test_range_query_invalid_left_negative(impl):
    with pytest.raises(RuntimeError):
        impl.range_query(-1, 3)

def test_range_query_invalid_right_out_of_bounds(impl):
    with pytest.raises(RuntimeError):
        impl.range_query(0, 8)

def test_range_query_invalid_left_greater_than_right(impl):
    with pytest.raises(RuntimeError):
        impl.range_query(5, 3)

def test_update_invalid_index_negative(impl):
    with pytest.raises(RuntimeError):
        impl.update(-1, 5)

def test_update_invalid_index_out_of_bounds(impl):
    with pytest.raises(RuntimeError):
        impl.update(8, 5)
