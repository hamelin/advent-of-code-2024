from collections.abc import Iterator, Sequence
from copy import copy
from dataclasses import dataclass
from enum import Enum
import functools as ft
import numpy as np
from operator import or_
from textwrap import dedent
from typing import Any, Self


Couple = tuple[int, int]
Shape = Couple
Position = Couple
Vector = Couple


@dataclass
class Move:
    name: str
    rotation: np.ndarray
    length: int

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Move):
            return self.length == other.length and np.all(
                self.rotation == other.rotation
            )
        return False

    def __hash__(self) -> int:
        return hash((self.length, *self.rotation.ravel()))


EAST = (0, 1)
NORTH = (-1, 0)
WEST = (0, -1)
SOUTH = (1, 0)
START = Move(name="START", rotation=np.eye(2, dtype=int), length=0)
FORWARD = Move(name="FORWARD", rotation=np.eye(2, dtype=int), length=1)
CCW = Move(
    name="CCW",
    rotation=np.array([
        [0, -1],
        [1, 0]
    ], dtype=int),
    length=0
)
CW = Move(
    name="CW",
    rotation=np.array([
        [0, 1],
        [-1, 0]
    ], dtype=int),
    length=0
)


@dataclass
class Reindeer:
    position: Position
    heading: Vector

    def step(self, move: Move) -> Self:
        return Reindeer(
            position=tuple(
                np.add(self.position, np.multiply(move.length, self.heading))
            ),
            heading=tuple(move.rotation @ self.heading)
        )

    def __hash__(self) -> int:
        return hash((self.position, self.heading))


@dataclass
class Maze:
    shape: Shape
    walls: set[Position]
    start: Position
    end: Position

    @classmethod
    def parse(cls, text: str) -> Self:
        lines = dedent(text).strip().split("\n")
        assert all(len(lines[i]) == len(lines[0]) for i in range(1, len(lines)))
        shape = (len(lines), len(lines[0]))

        start = ()
        end = ()
        walls = set()
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                match ch:
                    case "#":
                        walls.add((i, j))
                    case "S":
                        assert not start
                        start = (i, j)
                    case "E":
                        assert not end
                        end = (i, j)
                    case ".":
                        pass
                    case _:
                        raise ValueError(f"Unknown char at ({i}, {j}): {ch}")

        return cls(shape=shape, walls=walls, start=start, end=end)

    def dist_to_end(self, pos: Position) -> int:
        return np.sum(np.abs(np.subtract(pos, self.end)))


@dataclass
class Trace:
    move: Move
    reindeer: Reindeer
    cost: int

    def __hash__(self) -> int:
        return hash((self.move, self.reindeer))


COSTS = {
    START: 0,
    FORWARD: 1,
    CW: 1000,
    CCW: 1000
}


class Path(list[Trace]):

    @classmethod
    def from_steps(cls, start: Reindeer, *moves: Move):
        self = cls()
        self.append(Trace(move=START, reindeer=start, cost=COSTS[START]))
        r = start
        for move in moves:
            r = r.step(move)
            self.append(Trace(move=move, reindeer=r, cost=self[-1].cost + COSTS[move]))
        return self

    def __hash__(self) -> int:
        return hash(tuple(self))

    def progress(self, maze: Maze) -> Iterator["Path"]:
        assert self
        last = self[-1]
        assert last.move in {FORWARD, START}
        for moves_prior in [[], [CW], [CCW]]:
            r = last.reindeer
            cost = last.cost
            traces = []
            for move in [*moves_prior, FORWARD]:
                r = r.step(move)
                cost += COSTS[move]
                traces.append(Trace(move, r, cost))
            if r.position not in maze.walls | set(t.reindeer.position for t in self):
                path = copy(self)
                for t in traces:
                    path.append(t)
                yield path

    def print(self, maze: Maze) -> None:
        ar = np.full(maze.shape, ord(' '))
        for position in maze.walls:
            ar[*position] = ord('#')
        for trace in self[:-1]:
            ar[*trace.reindeer.position] = ord("x")
        ar[*self[-1].reindeer.position] = ord(
            {NORTH: "^", SOUTH: "v", EAST: ">", WEST: "<"}[self[-1].reindeer.heading]
        )
        for row in ar:
            print("".join(chr(n) for n in row))


def find_paths_cost_minimum(maze: Maze) -> set[Path]:
    assert maze.end != maze.start
    cost_best = np.inf
    paths_best = set()
    visited: dict[Reindeer, int] = {}
    work = [Path.from_steps(Reindeer(maze.start, EAST))]
    i = 0
    while work:
        path = work.pop(0)
        i += 1
        if not (i % 10000):
            # path.print(maze)
            print(f"Work yet: {len(work)}")
        # breakpoint()
        for longer in path.progress(maze):
            here = longer[-1]
            if here.reindeer.position == maze.end:
                if here.cost < cost_best:
                    print(f"Found new family of best paths; cost = {here.cost}")
                    paths_best = {longer}
                    cost_best = here.cost
                elif here.cost == cost_best:
                    print(f"Found minimum-cost path; now got {len(paths_best)}")
                    paths_best.add(longer)
            if here.cost <= min(cost_best, visited.get(here.reindeer, np.inf)):
                visited[here.reindeer] = here.cost
                cost_bound = here.cost
                dist = maze.dist_to_end(here.reindeer.position)
                cost_bound += dist * COSTS[FORWARD]
                axis = np.subtract(maze.end, here.reindeer.position) / dist
                if np.any(np.not_equal(axis, here.reindeer.heading)):
                    cost_bound += COSTS[CW]
                # if maze.dist_to_end(here.reindeer.step(FORWARD).position) > dist:
                #     cost_bound += COSTS[CW]
                if cost_bound <= cost_best:
                    work.append(longer)

        n = len(work)
        work = sorted(
            work,
            key=lambda p: maze.dist_to_end(p[-1].reindeer.position)
        )
        assert len(work) == n

    return paths_best


def enum_positions_on_paths(paths: Iterator[Path]) -> set[Position]:
    return ft.reduce(
        or_,
        ({tr.reindeer.position for tr in path} for path in paths),
        set()
    )
