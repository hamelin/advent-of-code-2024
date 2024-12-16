import pytest

from . import *  # noqa


@pytest.fixture
def texts():
    return {
        "small": """\
            ###############
            #.......#....E#
            #.#.###.#.###.#
            #.....#.#...#.#
            #.###.#####.#.#
            #.#.#.......#.#
            #.#.#####.###.#
            #...........#.#
            ###.#.#####.#.#
            #...#.....#.#.#
            #.#.#.###.#.#.#
            #.....#...#.#.#
            #.###.#.#.#.#.#
            #S..#.....#...#
            ###############
        """,
        "large": """\
            #################
            #...#...#...#..E#
            #.#.#.#.#.#.#.#.#
            #.#.#.#...#...#.#
            #.#.#.#.###.#.#.#
            #...#.#.#.....#.#
            #.#.#.#.#.#####.#
            #.#...#.#.#.....#
            #.#.#####.#.###.#
            #.#.#.......#...#
            #.#.###.#####.###
            #.#.#...#.....#.#
            #.#.#.#####.###.#
            #.#.#.........#.#
            #.#.#.#########.#
            #S#.............#
            #################
        """
    }


@pytest.fixture
def mazes(texts):
    return {name: Maze.parse(text) for name, text in texts.items()}


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "small",
            Maze(
                shape=(15, 15),
                walls={
                    ( 0, 0), ( 0, 1), ( 0, 2), ( 0, 3), ( 0, 4), ( 0, 5), ( 0, 6), ( 0, 7), ( 0, 8), ( 0, 9), ( 0,10), ( 0,11), ( 0,12), ( 0,13), ( 0,14),  # noqa
                    ( 1, 0),                                                                ( 1, 8),                                              ( 1,14),  # noqa
                    ( 2, 0),          ( 2, 2),          ( 2, 4), ( 2, 5), ( 2, 6),          ( 2, 8),          ( 2,10), ( 2,11), ( 2,12),          ( 2,14),  # noqa
                    ( 3, 0),                                              ( 3, 6),          ( 3, 8),                            ( 3,12),          ( 3,14),  # noqa
                    ( 4, 0),          ( 4, 2), ( 4, 3), ( 4, 4),          ( 4, 6), ( 4, 7), ( 4, 8), ( 4, 9), ( 4,10),          ( 4,12),          ( 4,14),  # noqa
                    ( 5, 0),          ( 5, 2),          ( 5, 4),                                                                ( 5,12),          ( 5,14),  # noqa
                    ( 6, 0),          ( 6, 2),          ( 6, 4), ( 6, 5), ( 6, 6), ( 6, 7), ( 6, 8),          ( 6,10), ( 6,11), ( 6,12),          ( 6,14),  # noqa
                    ( 7, 0),                                                                                                    ( 7,12),          ( 7,14),  # noqa
                    ( 8, 0), ( 8, 1), ( 8, 2),          ( 8, 4),          ( 8, 6), ( 8, 7), ( 8, 8), ( 8, 9), ( 8,10),          ( 8,12),          ( 8,14),  # noqa
                    ( 9, 0),                            ( 9, 4),                                              ( 9,10),          ( 9,12),          ( 9,14),  # noqa
                    (10, 0),          (10, 2),          (10, 4),          (10, 6), (10, 7), (10, 8),          (10,10),          (10,12),          (10,14),  # noqa
                    (11, 0),                                              (11, 6),                            (11,10),          (11,12),          (11,14),  # noqa
                    (12, 0),          (12, 2), (12, 3), (12, 4),          (12, 6),          (12, 8),          (12,10),          (12,12),          (12,14),  # noqa
                    (13, 0),                            (13, 4),                                              (13,10),                            (13,14),  # noqa
                    (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14,10), (14,11), (14,12), (14,13), (14,14),  # noqa
                },
                start=(13, 1),
                end=(1, 13),
            )
        ),
        (
            "large",
            Maze(
                shape=(17,17),
                walls={
                    ( 0, 0), ( 0, 1), ( 0, 2), ( 0, 3), ( 0, 4), ( 0, 5), ( 0, 6), ( 0, 7), ( 0, 8), ( 0, 9), ( 0,10), ( 0,11), ( 0,12), ( 0,13), ( 0,14), ( 0,15), ( 0,16),  # noqa
                    ( 1, 0),                            ( 1, 4),                            ( 1, 8),                            ( 1,12),                            ( 1,16),  # noqa
                    ( 2, 0),          ( 2, 2),          ( 2, 4),          ( 2, 6),          ( 2, 8),          ( 2,10),          ( 2,12),          ( 2,14),          ( 2,16),  # noqa
                    ( 3, 0),          ( 3, 2),          ( 3, 4),          ( 3, 6),                            ( 3,10),                            ( 3,14),          ( 3,16),  # noqa
                    ( 4, 0),          ( 4, 2),          ( 4, 4),          ( 4, 6),          ( 4, 8), ( 4, 9), ( 4,10),          ( 4,12),          ( 4,14),          ( 4,16),  # noqa
                    ( 5, 0),                            ( 5, 4),          ( 5, 6),          ( 5, 8),                                              ( 5,14),          ( 5,16),  # noqa
                    ( 6, 0),          ( 6, 2),          ( 6, 4),          ( 6, 6),          ( 6, 8),          ( 6,10), ( 6,11), ( 6,12), ( 6,13), ( 6,14),          ( 6,16),  # noqa
                    ( 7, 0),          ( 7, 2),                            ( 7, 6),          ( 7, 8),          ( 7,10),                                              ( 7,16),  # noqa
                    ( 8, 0),          ( 8, 2),          ( 8, 4), ( 8, 5), ( 8, 6), ( 8, 7), ( 8, 8),          ( 8,10),          ( 8,12), ( 8,13), ( 8,14),          ( 8,16),  # noqa
                    ( 9, 0),          ( 9, 2),          ( 9, 4),                                                                ( 9,12),                            ( 9,16),  # noqa
                    (10, 0),          (10, 2),          (10, 4), (10, 5), (10, 6),          (10, 8), (10, 9), (10,10), (10,11), (10,12),          (10,14), (10,15), (10,16),  # noqa
                    (11, 0),          (11, 2),          (11, 4),                            (11, 8),                                              (11,14),          (11,16),  # noqa
                    (12, 0),          (12, 2),          (12, 4),          (12, 6), (12, 7), (12, 8), (12, 9), (12,10),          (12,12), (12,13), (12,14),          (12,16),  # noqa
                    (13, 0),          (13, 2),          (13, 4),                                                                                  (13,14),          (13,16),  # noqa
                    (14, 0),          (14, 2),          (14, 4),          (14, 6), (14, 7), (14, 8), (14, 9), (14,10), (14,11), (14,12), (14,13), (14,14),          (14,16),  # noqa
                    (15, 0),          (15, 2),                                                                                                                      (15,16),  # noqa
                    (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 9), (16,10), (16,11), (16,12), (16,13), (16,14), (16,15), (16,16),  # noqa
                },
                start=(15, 1),
                end=(1, 15),
            )
        )
    ]
)
def test_parse(expected, name, mazes):
    assert expected == mazes[name]


@pytest.mark.parametrize(
    "moves,expected",
    [
        ([], [0]),
        ([FORWARD], [0, 1]),
        ([CW], [0, 1000]),
        ([CCW], [0, 1000]),
        ([FORWARD, CW, FORWARD], [0, 1, 1001, 1002])
    ]
)
def test_cost_accrual(expected, moves):
    actual = [trace.cost for trace in Path.from_steps(Reindeer((5,5), SOUTH), *moves)]
    assert expected == actual


@pytest.mark.parametrize(
    "path_so_far,expected",
    [
        (
            Path.from_steps(Reindeer((8,3), NORTH), FORWARD),
            {
                Path.from_steps(Reindeer((8,3), NORTH), FORWARD, FORWARD),
                Path.from_steps(Reindeer((8,3), NORTH), FORWARD, CW, FORWARD),
                Path.from_steps(Reindeer((8,3), NORTH), FORWARD, CCW, FORWARD),
            }
        ),
        (
            Path.from_steps(Reindeer((6,3), SOUTH), FORWARD),
            {
                Path.from_steps(Reindeer((6,3), SOUTH), FORWARD, FORWARD),
                Path.from_steps(Reindeer((6,3), SOUTH), FORWARD, CW, FORWARD),
                Path.from_steps(Reindeer((6,3), SOUTH), FORWARD, CCW, FORWARD),
            }
        ),
        (
            Path.from_steps(Reindeer((7,2), EAST), FORWARD),
            {
                Path.from_steps(Reindeer((7,2), EAST), FORWARD, FORWARD),
                Path.from_steps(Reindeer((7,2), EAST), FORWARD, CW, FORWARD),
                Path.from_steps(Reindeer((7,2), EAST), FORWARD, CCW, FORWARD),
            }
        ),
        (
            Path.from_steps(Reindeer((7,4), WEST), FORWARD),
            {
                Path.from_steps(Reindeer((7,4), WEST), FORWARD, FORWARD),
                Path.from_steps(Reindeer((7,4), WEST), FORWARD, CW, FORWARD),
                Path.from_steps(Reindeer((7,4), WEST), FORWARD, CCW, FORWARD),
            }
        ),
        (
            Path.from_steps(Reindeer((9,2), EAST), FORWARD),
            {
                Path.from_steps(Reindeer((9,2), EAST), FORWARD, CW, FORWARD),
                Path.from_steps(Reindeer((9,2), EAST), FORWARD, CCW, FORWARD),
            }
        ),
        (
            Path.from_steps(Reindeer((7,10), EAST), FORWARD),
            {Path.from_steps(Reindeer((7,10), EAST), FORWARD, CW, FORWARD)}
        ),
        (
            Path.from_steps(Reindeer((12,11), SOUTH), FORWARD),
            {Path.from_steps(Reindeer((12,11), SOUTH), FORWARD, CCW, FORWARD)}
        ),
        (
            Path.from_steps(Reindeer((7,8), EAST), FORWARD),
            {
                Path.from_steps(Reindeer((7,8), EAST), FORWARD, FORWARD),
                Path.from_steps(Reindeer((7,8), EAST), FORWARD, CCW, FORWARD),
            }
        )
    ]
)
def test_progress(expected, path_so_far, mazes):
    maze = mazes["small"]
    actual = set(path_so_far.progress(maze))
    assert expected == actual


@pytest.mark.parametrize(
    "name,expected_path,expected_cost",
    [
        (
            "small",
            Path.from_steps(
                Reindeer((13,1), EAST),
                CCW,
                *([FORWARD] * 4), CW,
                *([FORWARD] * 2), CCW,
                *([FORWARD] * 2), CW,
                *([FORWARD] * 8), CW,
                *([FORWARD] * 6), CCW,
                *([FORWARD] * 2), CCW,
                *([FORWARD] * 12),
            ),
            7036
        ),
        (
            "large",
            Path.from_steps(
                Reindeer((15,1), EAST),
                CCW,
                *([FORWARD] * 10), CW,
                *([FORWARD] * 2), CW,
                *([FORWARD] * 10), CCW,
                *([FORWARD] * 2), CCW,
                *([FORWARD] * 4), CW,
                *([FORWARD] * 2), CCW,
                *([FORWARD] * 2), CW,
                *([FORWARD] * 4), CCW,
                *([FORWARD] * 2), CW,
                *([FORWARD] * 4), CCW,
                *([FORWARD] * 6),
            ),
            11048
        )
    ]
)
def test_find_paths_cost_minimum(expected_path, expected_cost, name, mazes):
    paths_best = find_paths_cost_minimum(mazes[name])
    assert len(paths_best) > 1
    assert expected_path in paths_best
    assert expected_cost == paths_best.pop()[-1].cost


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "small",
            {
                (1,13),
                (2,13),
                (3,13),
                (4,13),
                (5,13),
                (6,13),
                (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9), (7,10), (7,11), (7,13),
                (8,3), (8,5), (8,11), (8,13),
                (9,1), (9,2), (9,3), (9,5), (9,11), (9,13),
                (10,1), (10,3), (10,5), (10,11), (10,13),
                (11,1), (11,2), (11,3), (11,4), (11,5), (11,11), (11,13),
                (12,1), (12,11), (12,13),
                (13,1), (13,11), (13,12), (13,13)
            }
        ),
        (
            "large",
            {
                (1,15),
                (2,15),
                (3,15),
                (4,15),
                (5,1), (5,2), (5,3), (5,15),
                (6,1), (6,3), (6,15),
                (7,1), (7,3), (7,11), (7,12), (7,13), (7,14), (7,15),
                (8,1), (8,3), (8,11), (8,15),
                (9,1), (9,3), (9,7), (9,8), (9,9), (9,10), (9,11), (9,13), (9,14), (9,15),  # noqa
                (10,1), (10,3), (10,7), (10,13),
                (11,1), (11,3), (11,5), (11,6), (11,7), (11,11), (11,12), (11,13),
                (12,1), (12,3), (12,5), (12,11),
                (13,1), (13,3), (13,5), (13,6), (13,7), (13,8), (13,9), (13,10), (13,11),  # noqa
                (14,1), (14,3), (14,5),
                (15,1), (15,3), (15,4), (15,5)
            }
        )
    ]
)
def test_positions_best_paths(expected, name, mazes):
    paths_best = find_paths_cost_minimum(mazes[name])
    actual = enum_positions_on_paths(paths_best)
    assert expected == actual
