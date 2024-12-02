import numpy as np

from .. import split_lists


def distance_between_lists(lists: np.ndarray) -> int:
    left, right = (np.sort(ll) for ll in split_lists(lists))
    return np.sum(np.abs(left - right))
