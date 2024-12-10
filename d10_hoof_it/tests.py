import pytest

from . import (
    iter_trails,
    N,
    rate_trailhead,
    read_map,
    sum_ratings,
    sum_scores
)


NAMES_MAP = ["fork", "cliff", "rectoverso", "small", "complex"]


@pytest.fixture
def maps():
    return {
       "fork": """\
            ...0...
            ...1...
            ...2...
            6543456
            7.....7
            8.....8
            9.....9
        """,
        "cliff": """\
            ..90..9
            ...1.98
            ...2..7
            6543456
            765.987
            876....
            987....
        """,
        "rectoverso": """\
            10..9..
            2...8..
            3...7..
            4567654
            ...8..3
            ...9..2
            .....01
        """,
        "small": """\
            0123
            1234
            8765
            9876
        """,
        "complex": """\
            89010123
            78121874
            87430965
            96549874
            45678903
            32019012
            01329801
            10456732
        """,
        "threeway": """\
            .....0.
            ..4321.
            ..5..2.
            ..6543.
            ..7..4.
            ..8765.
            ..9....
        """,
        "allaround": """\
            ..90..9
            ...1.98
            ...2..7
            6543456
            765.987
            876....
            987....
        """,
        "allover": """\
            012345
            123456
            234567
            345678
            4.6789
            56789.
        """
    }


@pytest.fixture
def fields(maps):
    return {name: read_map(map) for name, map in maps.items()}


@pytest.mark.parametrize(
    "name,expected",
    [("fork", 1), ("cliff", 1), ("rectoverso", 2), ("small", 1), ("complex", 9)]
)
def test_count_trailheads(expected, name, fields):
    assert expected == len([head for head, _ in iter_trails(fields[name])])


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "small",
            [
                [0, 1, 2, 3],
                [1, 2, 3, 4],
                [8, 7, 6, 5],
                [9, 8, 7, 6]
            ]
        ),
        (
            "fork",
            [
                [N, N, N, 0, N, N, N],
                [N, N, N, 1, N, N, N],
                [N, N, N, 2, N, N, N],
                [6, 5, 4, 3, 4, 5, 6],
                [7, N, N, N, N, N, 7],
                [8, N, N, N, N, N, 8],
                [9, N, N, N, N, N, 9],
            ]
        )
    ]
)
def test_read_map_small(expected, name, fields):
    assert expected == fields[name]


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "fork",
            {(0, 3): {(6, 0), (6, 6)}}
        ),
        (
            "cliff",
            {(0, 3): {(0, 6), (1, 5), (6, 0), (4, 4)}}
        ),
        (
            "rectoverso",
            {
                (0, 1): {(5, 3)},
                (6, 5): {(5, 3), (0, 4)}
            }
        ),
        (
            "small",
            {(0, 0): {(3, 0)}}
        ),
        (
            "complex",
            {
                (0, 2): {(0, 1), (3, 0), (3, 4), (4, 5), (5, 4)},
                (0, 4): {(0, 1), (3, 0), (3, 4), (4, 5), (5, 4), (2, 5)},
                (2, 4): {(0, 1), (3, 0), (3, 4), (4, 5), (5, 4)},
                (4, 6): {(2, 5), (3, 4), (4, 5)},
                (5, 2): {(6, 4)},
                (5, 5): {(2, 5), (3, 4), (4, 5)},
                (6, 0): {(3, 0), (0, 1), (3, 4), (4, 5), (5, 4)},
                (6, 6): {(2, 5), (3, 4), (4, 5)},
                (7, 1): {(3, 0), (0, 1), (3, 4), (4, 5), (5, 4)}
            }
        ),
    ]
)
def test_iter_summits(expected, name, fields):
    assert expected == {
        head: set(summits)
        for head, summits in iter_trails(fields[name])
    }


@pytest.mark.parametrize(
    "name,expected",
    [("fork", 2), ("cliff", 4), ("rectoverso", 3), ("small", 1), ("complex", 36)]
)
def test_sum_scores(expected, name, fields):
    assert expected == sum_scores(fields[name])


@pytest.mark.parametrize(
    "name,trailhead,expected",
    [
        ("threeway", (0, 5), 3),
        ("allaround", (0, 3), 13),
        ("allover", (0, 0), 227),
        ("complex", (0, 2), 20),
        ("complex", (0, 4), 24),
        ("complex", (2, 4), 10),
        ("complex", (4, 6), 4),
        ("complex", (5, 2), 1),
        ("complex", (5, 5), 4),
        ("complex", (6, 0), 5),
        ("complex", (6, 6), 8),
        ("complex", (7, 1), 5),
    ]
)
def test_rate_trailhead(name, trailhead, expected, fields):
    assert expected == rate_trailhead(fields[name], *trailhead)


@pytest.mark.parametrize(
    "name,expected",
    [("threeway", 3), ("allaround", 13), ("allover", 227), ("complex", 81)]
)
def test_sum_ratings(expected, name, fields):
    assert expected == sum_ratings(fields[name])
