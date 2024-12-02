import numpy as np
import pytest

from d00 import input2lists
from d00.distance_between_lists import distance_between_lists


def test_input2lists():
    input = """
5 8
9 10
5      1
"""
    assert np.all(
        np.array([[5, 8], [9, 10], [5, 1]]) == input2lists(input)
    )


def test_distance_between_lists():
    assert 5 == distance_between_lists(np.asarray([
        [5, 1],
        [2, 8],
        [0, 2],
        [3, 0],
    ], dtype=int))
