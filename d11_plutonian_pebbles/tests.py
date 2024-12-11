import pytest

from . import blink, count_stones_after_blinks


def test_transition_stone_0():
    assert [1] == blink([0])


@pytest.mark.parametrize(
    "num,expected",
    [(10, [1, 0]), (99, [9, 9]), (1000, [10, 0]), (2024, [20, 24])]
)
def test_transition_log10_even(expected, num):
    assert expected == blink([num])


@pytest.mark.parametrize("num,expected", [(1, [2024]), (999, [2021976])])
def test_transition_mul_2024(expected, num):
    assert expected == blink([num])


def test_blink_many():
    assert [1, 2024, 1, 0, 9, 9, 2021976] == blink([0, 1, 10, 99, 999])


@pytest.mark.parametrize(
    "stone,expected",
    [(0, 1), (1, 1), (10, 2), (99, 2), (999, 1)]
)
def test_count_stones_after_blink(expected, stone):
    assert expected == count_stones_after_blinks(stone, 1)
