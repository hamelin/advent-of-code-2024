from collections.abc import Iterator
from dataclasses import dataclass
from enum import auto, Enum
import numpy as np
from textwrap import dedent
from typing import Self


Position = tuple[int, int]
Shape = tuple[int, int]


class Edge(Enum):
    top = auto()
    bottom = auto()
    left = auto()
    right = auto()


def neighbors(pos: Position) -> Iterator[Position]:
    for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yield tuple(np.add(pos, delta))


@dataclass
class Region:
    plant: str
    positions: set[Position]

    def __hash__(self) -> int:
        return hash((self.plant, tuple(sorted(self.positions))))

    def area(self) -> int:
        return len(self.positions)

    def perimeter(self) -> int:
        return sum(
            len([n for n in neighbors(pos) if n not in self.positions])
            for pos in self.positions
        )

    def cost_fence(self) -> int:
        return self.area() * self.perimeter()

    def iter_edges(self) -> Iterator[tuple[Position, Edge]]:
        for position in self.positions:
            for edge, neighbor in zip(
                [Edge.top, Edge.bottom, Edge.left, Edge.right],
                neighbors(position)
            ):
                if neighbor not in self.positions:
                    yield position, edge


@dataclass
class Garden:
    shape: Shape
    regions: set[Region]

    @classmethod
    def read_map(cls, map: str) -> Self:
        regions = set()
        map_ = np.array([
            [ord(c) for c in line]
            for line in dedent(map).strip().split("\n")
        ])

        while True:
            row, col = np.nonzero(map_)
            if row.shape[0] == 0:
                break
            positions = set()
            plant = map_[row[0], col[0]]

            seeds = {(row[0], col[0])}
            while seeds:
                seed = seeds.pop()
                positions.add(seed)
                for pos in neighbors(seed):
                    if np.all(np.greater_equal(pos, 0) & np.less(pos, map_.shape)):
                        if pos not in positions and np.all(map_[*pos] == plant):
                            seeds.add(pos)

            regions.add(Region(plant=chr(plant), positions=positions))
            rows, cols = zip(*positions)
            map_[rows, cols] = 0

        return cls(shape=map_.shape, regions=regions)

    def geometry(self) -> np.ndarray:
        return np.array(
            [
                (region.plant, region.area(), region.perimeter())
                for region in self.regions
            ],
            dtype=[("name", "<U1"), ("area", int), ("perimeter", int)]
        )

    def cost_fences(self) -> int:
        return sum(region.cost_fence() for region in self.regions)
