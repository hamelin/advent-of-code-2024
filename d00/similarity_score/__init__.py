from collections.abc import Iterator
import numpy as np

from .. import split_lists


def iter_frequencies(ids: np.ndarray, id_end: int) -> Iterator[tuple[int, int]]:
    ids_sorted = np.sort(ids)
    ids_u, ind = np.unique(ids_sorted, return_index=True)
    freq = [*np.split(ids_sorted, ind[1:]), [id_end + 1]]
    j = 0
    for i in range(1, id_end):
        if i == freq[j][0]:
            yield (i, len(freq[j]))
            j += 1
        else:
            yield (i, 0)


def similarity_score(lists: np.ndarray) -> int:
    left, right = split_lists(lists)
    score = 0
    id_end = np.max(lists, axis=None) + 1
    for (left_id, left_freq), (right_id, right_freq) in zip(
        iter_frequencies(left, id_end),
        iter_frequencies(right, id_end)
    ):
        assert left_id == right_id
        score += left_id * left_freq * right_freq
    return score
