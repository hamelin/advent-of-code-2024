import numpy as np
import pytest

from . import count_robots_by_quadrant, Horde, Robot


@pytest.fixture
def positions_velocities():
    return """\
        p=0,4 v=3,-3
        p=6,3 v=-1,-3
        p=10,3 v=-1,2
        p=2,0 v=2,-1
        p=0,0 v=1,3
        p=3,0 v=-2,-2
        p=7,6 v=-1,-3
        p=3,0 v=-1,-2
        p=9,3 v=2,3
        p=7,3 v=-1,2
        p=2,4 v=2,-3
        p=9,5 v=-3,-3
    """


@pytest.fixture
def horde(positions_velocities):
    return Horde.parse_positions_velocities(positions_velocities)


def test_parse_positions_velocities(horde):
    assert (expected := Horde(  # noqa
        robots=[
            Robot.make(position=position, velocity=velocity)
            for position, velocity in [
                ((0,4), (3,-3)),
                ((6,3), (-1,-3)),
                ((10,3), (-1,2)),
                ((2,0), (2,-1)),
                ((0,0), (1,3)),
                ((3,0), (-2,-2)),
                ((7,6), (-1,-3)),
                ((3,0), (-1,-2)),
                ((9,3), (2,3)),
                ((7,3), (-1,2)),
                ((2,4), (2,-3)),
                ((9,5), (-3,-3)),
            ]
        ]
    )) == horde


@pytest.mark.parametrize(
    "expected_position,position,velocity,boundaries",
    [
        ((4,1), (2,4), (2,-3), (11,7)),
        ((6,5), (4,1), (2,-3), (11,7)),
        ((8,2), (6,5), (2,-3), (11,7)),
        ((10,6), (8,2), (2,-3), (11,7)),
        ((1,3), (10,6), (2,-3), (11,7)),
    ]
)
def test_advance_once(expected_position, position, velocity, boundaries):
    robot = Robot.make(position, velocity)
    robot.advance(boundaries, 1)
    assert np.all(np.asarray(expected_position) == robot.position)


@pytest.mark.parametrize(
    "expected,steps",
    [
        (
            [
                [1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            ],
            0
        ),
        (
            [
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            ],
            100
        )
    ]
)
def test_map(expected, horde, steps):
    boundaries = np.array((11, 7))
    horde.advance(boundaries=boundaries, steps=steps)
    assert expected == horde.map(boundaries=boundaries)


@pytest.mark.parametrize(
    "steps,expected",
    [
        (0, (4, 0, 2, 2)),
        (100, (1, 3, 4, 1)),
    ]
)
def test_count_robots_by_quadrant(expected, horde, steps):
    boundaries = np.array([11, 7])
    horde.advance(boundaries=boundaries, steps=steps)
    assert expected == count_robots_by_quadrant(horde, boundaries)
