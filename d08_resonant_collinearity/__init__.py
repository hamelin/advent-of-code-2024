from collections.abc import Iterator, Sequence
from dataclasses import dataclass
import itertools as it
import numpy as np
import re
from textwrap import dedent
from typing import Callable, Self


Couple = tuple[int, int]
Position = Couple


RX_ANTENNA = re.compile(r"[0-9a-zA-Z]")


Model = Callable[[], Iterator[Sequence[int]]]


def RESTRICTED():
    yield (-1, 2)


def HARMONIC():
    n = np.array([0, 1])
    inc = np.array([-1, 1])
    while True:
        yield tuple(n)
        n += inc


@dataclass
class City:
    shape: Couple
    antennas: dict[str, set[Position]]

    def iter_antinodes(self, model: Model) -> Iterator[Position]:
        for antennas in self.antennas.values():
            for a, b in it.combinations(antennas, 2):
                diff = np.subtract(b, a)
                for seq in model():
                    has_yielded_once = False
                    for i in seq:
                        pos = np.add(a, i * diff)
                        if np.all(
                            np.greater_equal(pos, (0, 0)) & np.less(pos, self.shape)
                        ):
                            yield tuple(pos)
                            has_yielded_once = True
                    if not has_yielded_once:
                        break

    def count_antinodes(self, model: Model):
        return len(set(self.iter_antinodes(model)))

    @classmethod
    def parse_map(cls, map_city: str) -> Self:
        lines = dedent(map_city).strip().split("\n")
        assert lines
        shape = (len(lines), len(lines[0]))
        assert all(len(line) == shape[1] for line in lines[1:])

        antennas = {}
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                assert len(ch) == 1
                if RX_ANTENNA.match(ch):
                    antennas.setdefault(ch, set()).add((i, j))

        return cls(shape=shape, antennas=antennas)
