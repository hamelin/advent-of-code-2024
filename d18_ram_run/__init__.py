from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
import numpy as np
from textwrap import dedent
from typing import Optional, Self


Position = int
Position = tuple[int, int]
Shape = tuple[int, int]
Path = Sequence[Position]


DIRECTIONS = [
    np.array((-1, 0), dtype=int),
    np.array((1, 0), dtype=int),
    np.array((0, -1), dtype=int),
    np.array((0, 1), dtype=int),
]


@dataclass
class Suffix:
    cost: int
    steps: list[np.ndarray]

    def to_path(self) -> Path:
        return tuple(tuple(step) for step in self.steps)

    def first(self) -> Position:
        assert self.steps
        return tuple(self.steps[0])

    def prepend(self, direction: np.ndarray) -> Self:
        assert self.steps
        return Suffix(
            cost=self.cost + 1,
            steps=[self.steps[0] + direction, *self.steps]
        )


@dataclass
class RAM:
    shape: Shape
    corrupted: set[Position]

    def length_path_shortest(self) -> Optional[int]:
        ar_shape = np.array(self.shape)
        work: list[Suffix] = [Suffix(cost=0, steps=[ar_shape - 1])]
        costs_best: dict[Position, Suffix] = {}
        costs_best[work[-1].first()] = work[-1].cost
        i = 0
        num_spots = np.prod(self.shape) - len(self.corrupted)
        while work:
            i += 1
            if i % 100000 == 0:
                print(f"{len(costs_best)} spots mapped ({int(100. * len(costs_best) / num_spots)}%) | {len(work)} work items")

            suffix = work.pop()
            for direction in DIRECTIONS:
                longer = suffix.prepend(direction)
                pos = longer.first()
                if np.all(
                    np.greater_equal(pos, 0) & np.less(pos, self.shape)
                ) and (
                    pos not in self.corrupted
                ) and (
                    longer.cost < costs_best.get(pos, np.inf)
                ):
                    costs_best[pos] = longer.cost
                    work.append(longer)
        return costs_best.get((0, 0), None)


@dataclass
class Game:
    shape: Shape
    bytes: list[Position] = field(default_factory=list)

    def with_bytes_from_text(self, text: str) -> Self:
        self.bytes += [
            tuple(int(n) for n in line.strip().split(","))[-1::-1]
            for line in dedent(text).strip().split("\n")
            if line
        ]
        return self

    def __iter__(self) -> Iterator[RAM]:
        ram = RAM(shape=self.shape, corrupted=set())
        for pos in self.bytes:
            ram.corrupted.add(pos)
            yield ram

    def after_fallen(self, num: int) -> RAM:
        for i, ram in enumerate(self):
            if i == num - 1:
                break
        return ram
