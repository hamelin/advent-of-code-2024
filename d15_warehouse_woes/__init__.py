from collections.abc import Iterator, Sequence
from copy import copy
from dataclasses import dataclass
from enum import Enum
import numpy as np
from textwrap import dedent
from typing import Any, Self


class Rosetta:
    rosetta = {}

    @classmethod
    def _carve_rosetta(cls) -> dict[str, Self]:
        if hasattr(cls, "__members__"):
            return {v.value: v for v in cls.__members__.values()}
        raise NotImplementedError()

    @classmethod
    def from_char(cls, c: str) -> Self:
        if not cls.rosetta:
            cls.rosetta = cls._carve_rosetta()
        return cls.rosetta[c]


class Object(Rosetta, Enum):
    empty = "."
    wall = "#"
    box = "O"
    robot = "@"
    wide_left = "["
    wide_right = "]"

    def __int__(self) -> int:
        return ord(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Object):
            return super().__eq__(other)
        elif hasattr(other, "__int__"):
            return int(self) == int(other)
        return False


class Move(Rosetta, Enum):
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)

    @classmethod
    def _carve_rosetta(cls) -> dict[str, Self]:
        return {
            "^": Move.up,
            "v": Move.down,
            "<": Move.left,
            ">": Move.right
        }

    def as_array(self) -> np.ndarray:
        return np.asarray(self.value)


class Warehouse(np.ndarray):

    def __new__(cls, objects: Sequence[Sequence[Object]]) -> Self:
        self = np.asarray(
            [[int(o) for o in row] for row in objects],
            dtype=int
        ).view(cls)
        assert np.all(self[0, :] == Object.wall)
        assert np.all(self[:, 0] == Object.wall)
        assert np.all(self[-1, :] == Object.wall)
        assert np.all(self[:, -1] == Object.wall)
        return self

    @classmethod
    def parse(cls, text: str) -> Self:
        return cls([
            [Object.from_char(c) for c in line.strip()]
            for line in dedent(text).strip().split("\n")
            if line.strip()
        ])

    def print(self) -> None:
        for row in self:
            print("".join(chr(n) for n in row))

    def try_moving(self, robot: np.ndarray, move: np.ndarray) -> np.ndarray:
        assert self[*robot] == Object.robot
        if move[0] == 0:
            return self._try_moving_horizontal(robot, move)
        else:
            return self._try_moving_vertical(robot, move)

    def _try_moving_horizontal(self, robot: np.ndarray, move: np.ndarray) -> np.ndarray:
        i_row, start = robot
        _, nudge = move
        end = start + nudge
        while True:
            match self[i_row, end]:
                case Object.box | Object.wide_left | Object.wide_right:
                    end += nudge
                case Object.empty | Object.wall:
                    break
                case _:
                    raise RuntimeError(
                        f"Weird value at ({i_row}, {end}): {self[i_row, end]}"
                    )

        if self[i_row, end] != Object.wall:
            while end != start:
                self[i_row, end] = self[i_row, end - nudge]
                end -= nudge
            self[i_row, start] = Object.empty
            robot += move
        assert self[*robot] == Object.robot
        return robot

    def _try_moving_vertical(self, robot: np.ndarray, move: np.ndarray) -> np.ndarray:
        moving = {tuple(robot)}
        front = {tuple(robot + move)}

        def add_to_moving_and_front(*spots: np.ndarray) -> None:
            for spot in spots:
                moving.add(tuple(spot))
                front.add(tuple(spot + move))

        one_to_the_left = np.array((0, -1))
        one_to_the_right = np.array((0, 1))
        while front:
            spot = front.pop()
            match self[*spot]:
                case Object.box:
                    add_to_moving_and_front(spot)
                case Object.wide_left:
                    spot_right = spot + one_to_the_right
                    assert self[*spot_right] == Object.wide_right
                    add_to_moving_and_front(spot, spot_right)
                case Object.wide_right:
                    spot_left = spot + one_to_the_left
                    assert self[*spot_left] == Object.wide_left
                    add_to_moving_and_front(spot_left, spot)
                case Object.empty:
                    pass
                case Object.wall:
                    moving.clear()
                    break
                case _:
                    raise RuntimeError(f"Weird value at {tuple(spot)}: {self[*spot]}")

        if moving:
            for spot in sorted(list(moving), reverse=move[0] > 0):
                self[*np.add(spot, move)] = self[*spot]
                self[*spot] = Object.empty
            robot += move
        assert self[*robot] == Object.robot
        return robot

    def boxes(self) -> Iterator[int]:
        rows, cols = np.nonzero((self == Object.box) | (self == Object.wide_left))
        for row, col in zip(rows, cols):
            yield row * 100 + col


@dataclass
class Game:
    warehouse: Warehouse
    moves: Sequence[Move]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Game):
            return np.all(self.warehouse == other.warehouse) and (
                self.moves == other.moves
            )
        return False

    @classmethod
    def parse(cls, text: str) -> Self:
        text_warehouse, text_moves = dedent(text).strip().split("\n\n")
        warehouse = Warehouse.parse(text_warehouse)
        moves = [Move.from_char(c) for c in text_moves.replace("\n", "")]
        return cls(warehouse=warehouse, moves=moves)

    @dataclass
    class Play:
        warehouse: Warehouse
        moves: Iterator[Move]
        robot: np.ndarray

        def move(self) -> None:
            self.robot = self.warehouse.try_moving(
                self.robot,
                next(self.moves).as_array()
            )

        def run(self) -> Self:
            i = 0
            while True:
                try:
                    # if i == 165:
                    #     breakpoint()
                    self.move()
                    i += 1
                except StopIteration:
                    break
                except AssertionError:
                    print(f"-- At move {i} --")
                    raise
            return self

    def play(self) -> Play:
        row, col = np.nonzero(self.warehouse == Object.robot)
        assert row.shape == (1,)
        return Game.Play(
            warehouse=self.warehouse.copy(),
            moves=iter(self.moves),
            robot=np.array([row[0], col[0]])
        )

    def widen(self) -> Self:
        warehouse_wide = [
            [Object.empty for _ in range(2 * self.warehouse.shape[1])]
            for __ in range(self.warehouse.shape[0])
        ]
        for i_row in range(self.warehouse.shape[0]):
            for i_self, i_wide in zip(
                range(0, self.warehouse.shape[1], 1),
                range(0, 2 * self.warehouse.shape[1], 2)
            ):
                match self.warehouse[i_row, i_self]:
                    case Object.empty:
                        pass
                    case Object.wall:
                        warehouse_wide[i_row][i_wide] = Object.wall
                        warehouse_wide[i_row][i_wide + 1] = Object.wall
                    case Object.box:
                        warehouse_wide[i_row][i_wide] = Object.wide_left
                        warehouse_wide[i_row][i_wide + 1] = Object.wide_right
                    case Object.robot:
                        warehouse_wide[i_row][i_wide] = Object.robot
                    case _:
                        raise ValueError(
                            f"Unexpected object at ({i_row}, {i_self}): "
                            f"{chr(self.warehouse[i_row, i_self])}"
                        )
        return type(self)(warehouse=Warehouse(warehouse_wide), moves=copy(self.moves))
