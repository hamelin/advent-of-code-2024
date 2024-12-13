from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from enum import auto, Enum
import numpy as np
from textwrap import dedent
from typing import Self


class Edge(Enum):
    top = auto()
    bottom = auto()
    left = auto()
    right = auto()


Position = tuple[int, int]
Shape = tuple[int, int]
Side = tuple[str, Edge, Position, int]


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

    def cost_fence_perimeter(self) -> int:
        return self.area() * self.perimeter()

    def iter_edges(self) -> Iterator[tuple[Position, Edge]]:
        for position in self.positions:
            for edge, neighbor in zip(
                [Edge.top, Edge.bottom, Edge.left, Edge.right],
                neighbors(position)
            ):
                if neighbor not in self.positions:
                    yield position, edge

    def iter_sides(self) -> Iterator[Side]:
        indices_shared_specific = {
            Edge.top: (0, 1),
            Edge.bottom: (0, 1),
            Edge.left: (1, 0),
            Edge.right: (1, 0),
        }
        map_shared = {}
        for position, edge in self.iter_edges():
            i_shared, i_specific = indices_shared_specific[edge]
            shared = position[i_shared]
            specific = position[i_specific]
            map_shared.setdefault(shared, {}).setdefault(edge, []).append(specific)

        for shared, map_edges in map_shared.items():
            for edge, specifics in map_edges.items():
                assert specifics
                i_shared, i_specific = indices_shared_specific[edge]
                for group in _iter_contiguous_groups(sorted(specifics)):
                    start = [-1, -1]
                    start[i_shared] = shared
                    start[i_specific] = group[0]
                    yield (self.plant, edge, tuple(start), len(group))

    def num_sides(self) -> int:
        return sum(1 for _ in self.iter_sides())

    def cost_fence_num_sides(self) -> int:
        return self.area() * self.num_sides()


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

    def cost_fences_perimeter(self) -> int:
        return sum(region.cost_fence_perimeter() for region in self.regions)

    def cost_fences_num_sides(self) -> int:
        return sum(region.cost_fence_num_sides() for region in self.regions)


def _iter_contiguous_groups(seq: Sequence[int]) -> Iterator[list[int]]:
    assert len(seq) > 0
    group = []
    for n in seq:
        if not group or n == group[-1] + 1:
            group.append(n)
        else:
            yield group
            group = [n]
    yield group
