from dataclasses import dataclass
import numpy as np
import re
from textwrap import dedent
from typing import Any, Self


@dataclass
class Robot:
    position: np.ndarray
    velocity: np.ndarray

    @classmethod
    def make(cls, position: tuple[int, int], velocity: tuple[int, int]) -> Self:
        return cls(position=np.asarray(position), velocity=np.asarray(velocity))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Robot):
            return False
        return all((
            np.all(self.position == other.position),
            np.all(self.velocity == other.velocity)
        ))

    def advance(self, boundaries: np.ndarray, steps: int) -> None:
        assert steps >= 0
        for _ in range(steps):
            self.position = (self.position + self.velocity) % boundaries


RX_POSITION_VELOCITY = re.compile(
    r"p=(?P<px>-?\d+),(?P<py>-?\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)"
)


@dataclass
class Horde:
    robots: list[Robot]

    @classmethod
    def parse_positions_velocities(cls, positions_velocities: str) -> Self:
        robots = []
        for i, line in enumerate(dedent(positions_velocities).split("\n")):
            if line := line.strip():
                match = RX_POSITION_VELOCITY.match(line)
                if not match:
                    raise ValueError(f"Parse error at line {i}: {line}")

                def param_robot(name):
                    return int(match.group(name))

                params = {
                    name: int(match.group(name))
                    for name in ["px", "py", "vx", "vy"]
                }
                robots.append(
                    Robot.make(
                        (params["px"], params["py"]),
                        (params["vx"], params["vy"])
                    )
                )
        return cls(robots=robots)

    def advance(self, boundaries: np.ndarray, steps: int) -> None:
        for robot in self.robots:
            robot.advance(boundaries=boundaries, steps=steps)

    def map(self, boundaries: np.ndarray) -> list[list[int]]:
        assert boundaries.shape == (2,)
        m = [[0 for __ in range(boundaries[0])] for _ in range(boundaries[1])]
        for robot in self.robots:
            m[robot.position[1]][robot.position[0]] += 1
        return m


def count_robots_by_quadrant(
    horde: Horde,
    boundaries: np.ndarray
) -> tuple[int, int, int, int]:
    map = np.asarray(horde.map(boundaries))
    assert map.ndim == 2
    middle = np.asarray(map.shape) // 2
    return tuple(
        np.sum(map[xs:xe, ys:ye], axis=None)
        for xs, xe, ys, ye in [
            (0, middle[0], 0, middle[1]),
            (0, middle[0], middle[1] + 1, None),
            (middle[0] + 1, None, 0, middle[1]),
            (middle[0] + 1, None, middle[1] + 1, None)
        ]
    )
