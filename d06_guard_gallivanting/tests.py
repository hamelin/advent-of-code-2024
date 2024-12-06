from copy import deepcopy
import pytest
from textwrap import dedent

from . import (
    Guard,
    Lab,
)


@pytest.fixture
def the_map():
    return """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...\
"""


@pytest.fixture
def the_lab(the_map):
    return Lab.parse_map(the_map)


def test_parse_map(the_lab):
    assert (10, 10) == the_lab.shape
    assert {
        (0, 4),
        (1, 9),
        (3, 2),
        (4, 7),
        (6, 1),
        (7, 8),
        (8, 0),
        (9, 6),
    } == the_lab.obstacles
    assert Guard(direction=(-1, 0), position=(6, 4)) == the_lab.guard


@pytest.mark.parametrize(
    "expected_position,expected_direction,expected_exited,map",
    [
        (
            (0, 1),
            (-1, 0),
            False,
            """\
            ...
            .^.
            """
        ),
        (
            (0, 2),
            (0, 1),
            False,
            """\
            .>.
            """
        ),
        (
            (0, 0),
            (0, -1),
            False,
            """\
            .<.
            """
        ),
        (
            (1, 1),
            (1, 0),
            False,
            """\
            .v.
            ...
            """
        ),
        (
            (0, 3),
            (0, 1),
            True,
            """\
            ..>
            """
        ),
        (
            (-1, 1),
            (-1, 0),
            True,
            """\
            .^.
            """
        ),
        (
            (1, 1),
            (1, 0),
            True,
            """\
            .v.
            """
        ),
        (
            (0, -1),
            (0, -1),
            True,
            """\
            <..
            """
        ),
        (
            (1, 1),
            (0, 1),
            False,
            """\
            .#.
            .^.
            ...
            """
        ),
        (
            (1, 1),
            (1, 0),
            False,
            """\
            ...
            .>#
            ...
            """
        ),
        (
            (1, 1),
            (0, -1),
            False,
            """\
            ..#
            .v.
            .#.
            """
        ),
        (
            (1, 1),
            (-1, 0),
            False,
            """\
            ...
            #<.
            ...
            """
        ),
    ]
)
def test_step(expected_position, expected_direction, expected_exited, map):
    lab = Lab.parse_map(dedent(map).strip())
    guard = lab.step()
    assert Guard(
        position=expected_position,
        direction=expected_direction
    ) == guard
    assert expected_exited == lab.has_guard_exited()


def test_walk_guard(the_lab):
    expected = dedent(
        """\
        ....#.....
        ....XXXXX#
        ....X...X.
        ..#.X...X.
        ..XXXXX#X.
        ..X.X.X.X.
        .#XXXXXXX.
        .XXXXXXX#.
        #XXXXXXX..
        ......#X..
        """
    ).strip().replace("#", ".")
    actual_ = [["." for _ in range(10)] for _ in range(10)]
    for irow, icol in the_lab.walk_guard_out():
        actual_[irow][icol] = "X"
    actual = "\n".join("".join(row) for row in actual_)
    assert expected == actual


def test_count_steps_guard(the_lab):
    assert 41 == len(set(the_lab.walk_guard_out()))


def test_deepcopy_lab(the_lab):
    lab = deepcopy(the_lab)
    assert lab.obstacles is not the_lab.obstacles
    assert lab.guard is not the_lab.guard


OBSTACLES_INDUCING_LOOP = [(6, 3), (7, 6), (7, 7), (8, 1), (8, 3), (9, 7)]


@pytest.fixture
def obstacles_possible(the_lab):
    return [
        position
        for position in deepcopy(the_lab).walk_guard_out()
        if position != the_lab.guard.position
    ]


def test_would_guard_loop_original(the_lab):
    assert not the_lab.would_guard_loop()


@pytest.mark.parametrize("index", list(range(0, 53)))
def test_would_guard_loop_with_loop(the_lab, obstacles_possible, index):
    obstacle_new = obstacles_possible[index]
    assert obstacle_new != the_lab.guard.position
    assert (obstacle_new in OBSTACLES_INDUCING_LOOP) == the_lab.with_new_obstacle(
        obstacle_new
    ).would_guard_loop()


def test_iter_obstacles_inducing_loop(the_lab):
    assert set(OBSTACLES_INDUCING_LOOP) == set(the_lab.iter_obstacles_inducing_loop())
