import numpy as np
import pytest

from d00.similarity_score import iter_frequencies, similarity_score


def test_iter_frequencies():
    assert [
        (1, 0),
        (2, 0),
        (3, 3),
        (4, 1),
        (5, 1),
        (6, 0),
        (7, 0),
        (8, 0),
        (9, 1),
        (10, 0),
        (11, 0)
    ] == list(iter_frequencies(np.array([4, 3, 5, 3, 9, 3]), 12))


def test_similarity_score():
    assert 31 == similarity_score(np.array([
        [3, 4],
        [4, 3],
        [2, 5],
        [1, 3],
        [3, 9],
        [3, 3],
    ]))
