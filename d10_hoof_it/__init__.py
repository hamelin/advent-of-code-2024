from collections.abc import Iterator
import numpy as np
import re
from textwrap import dedent


Position = tuple[int, int]
Delta = tuple[int, int]
Field = list[list[int]]
N = 1000
TRAILHEAD = 0
SUMMIT = 9


def read_map(map: str) -> Field:
    lines = dedent(map).strip().split("\n")
    assert lines
    assert all(len(line) == len(lines[0]) for line in lines[1:])

    map = []
    for line in lines:
        map.append(row := [])
        for ch in line:
            row.append(int(ch) if re.match(r"[0-9]", ch) else N)
    return map


def iter_positions(field: Field) -> Iterator[Position]:
    for i in range(len(field)):
        for j in range(len(field[i])):
            yield (i, j)


def iter_trails(field: Field) -> Iterator[tuple[Position, Iterator[Position]]]:
    for row, col in iter_positions(field):
        if field[row][col] == TRAILHEAD:
            yield (row, col), iter_summits(field, row, col)


def directions() -> Iterator[Delta]:
    yield from [(0, 1), (-1, 0), (0, -1), (1, 0)]


def measure_field(field: Field) -> tuple[int, int]:
    return len(field), len(field[0])


def is_next_step(field: Field, here: Position, there: Position) -> bool:
    return np.all(np.greater_equal(there, 0)) & np.all(
        np.less(there, (len(field), len(field[0])))
    ) and field[there[0]][there[1]] == field[here[0]][here[1]] + 1


def iter_summits(field: Field, row: int, col: int) -> Iterator[Position]:
    assert field[row][col] == TRAILHEAD
    num_rows, num_cols = measure_field(field)

    work = [(row, col, directions())]
    summits = set()
    while work:
        row, col, dirs = work[-1]
        try:
            row_, col_ = np.add(here := (row, col), next(dirs))
            if is_next_step(field, here, (row_, col_)):
                if field[row_][col_] == SUMMIT:
                    summit = (row_, col_)
                    if summit not in summits:
                        yield summit
                        summits.add(summit)
                else:
                    work.append((row_, col_, directions()))
        except StopIteration:
            work.pop()


def sum_scores(field: Field) -> int:
    return sum(len(set(summits)) for _, summits in iter_trails(field))


def rate_trailhead(field: Field, row: int, col: int) -> int:
    num_rows, num_cols = measure_field(field)
    rating = 0
    paths = [(row, col)]
    while paths:
        here = paths.pop(0)
        for delta in directions():
            there = np.add(here, delta)
            if is_next_step(field, here, there):
                if field[there[0]][there[1]] == SUMMIT:
                    rating += 1
                else:
                    paths.append(there)
    return rating


def sum_ratings(field: Field) -> int:
    return sum(
        rate_trailhead(field, *head)
        for head, _ in iter_trails(field)
    )
