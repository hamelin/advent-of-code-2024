import numpy as np


def input2lists(input: str) -> np.ndarray:
    return np.array([
        [int(n) for n in line.strip().split()]
        for line in input.split("\n")
        if line.strip()
    ])


def distance_between_lists(lists: np.ndarray) -> int:
    assert lists.ndim == 2
    assert lists.shape[1] == 2
    assert lists.dtype.name == "int64"

    left = np.sort(lists[:, 0]).squeeze()
    right = np.sort(lists[:, 1]).squeeze()
    return np.sum(np.abs(left - right))
