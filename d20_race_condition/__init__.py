from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from textwrap import dedent
from typing import Self


Couple = tuple[int, int]
Position = Couple
Shape = Couple
Delta = Couple


class Space:
    EMPTY = "."
    WALL = "#"
    START = "S"
    FINISH = "E"


UNDEFINED = (-1, -1)


class Cardinal:
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

    @classmethod
    def points(cls) -> Iterator[Couple]:
        return iter([cls.NORTH, cls.SOUTH, cls.WEST, cls.EAST])


def move(position: Position, delta: Delta) -> Position:
    return tuple(np.add(position, delta))


@dataclass
class Cheat:
    start: Position
    finish: Position

    def __len__(self) -> int:
        return manhattan(self.start, self.finish)


def manhattan(p: Position, q: Position) -> int:
    return np.sum(np.abs(np.subtract(p, q)))


@dataclass
class RaceTrack:
    shape: Shape
    walls: set[Position]
    start: Position
    finish: Position
    cost_from: dict[Position, int] = field(default_factory=dict)
    cost_to: dict[Position, int] = field(default_factory=dict)

    @classmethod
    def parse(cls, text: str) -> Self:
        lines = dedent(text).strip().split("\n")
        assert all(len(lines[i]) == len(lines[0]) for i in range(1, len(lines)))
        shape = (len(lines), len(lines[0]))

        walls = set()
        start = UNDEFINED
        finish = UNDEFINED
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                match ch:
                    case Space.EMPTY:
                        pass
                    case Space.WALL:
                        walls.add((i, j))
                    case Space.START:
                        assert start == UNDEFINED
                        start = (i, j)
                    case Space.FINISH:
                        assert finish == UNDEFINED
                        finish = (i, j)
                    case _:
                        raise ValueError(f"Unknown value at {(i, j)}: {ch}")
        return cls(shape=shape, walls=walls, start=start, finish=finish)

    def init(self) -> Self:
        if self.cost_from and self.cost_to:
            return self

        for pos, final, costs in [
            (self.finish, self.start, self.cost_from),
            (self.start, self.finish, self.cost_to)
        ]:
            cost = 0
            while True:
                costs[pos] = cost
                cost += 1
                for step in Cardinal.points():
                    pos_next = move(pos, step)
                    if pos_next not in self.walls and pos_next not in costs:
                        pos = pos_next
                        break
                else:
                    assert pos == final
                    break
        return self

    def as_map(self):
        rows = [
            [Space.EMPTY for _ in range(self.shape[1])]
            for __ in range(self.shape[0])
        ]
        for i, j in self.walls:
            rows[i][j] = Space.WALL
        for (i, j), ch in [(self.start, Space.START), (self.finish, Space.FINISH)]:
            rows[i][j] = ch
        return "\n".join("".join(row) for row in rows)

    def is_position_valid(self, position: Position) -> bool:
        return all([*np.greater_equal(position, 0), *np.less(position, self.shape)])

    def is_free_space(self, position: Position) -> bool:
        return self.is_position_valid(position) and position not in self.walls

    def saving_with_cheat(self, cheat: Cheat) -> int:
        self.init()
        return max(
            0,
            self.cost_from[self.start] - (
                self.cost_to[cheat.start] + self.cost_from[cheat.finish] + len(cheat)
            )
        )

    def iter_cheats(self, dist_max: int, tqdm=lambda x, *_, **__: x):
        self.init()
        for start in tqdm(self.cost_from.keys()):
            for finish in self.iter_free_within(start, dist_max):
                cheat = Cheat(start=start, finish=finish)
                assert len(cheat) <= dist_max
                saving = self.saving_with_cheat(cheat)
                if saving > 0:
                    yield cheat, saving

    def iter_free_within(self, center: Position, dist_max: int) -> Iterator[Position]:
        row, col = center
        for i in range(row - dist_max, row + dist_max + 1):
            for j in range(col - dist_max, col + dist_max + 1):
                pos = (i, j)
                if pos != center and manhattan(
                    pos,
                    center
                ) <= dist_max and self.is_free_space(pos):
                    yield pos
