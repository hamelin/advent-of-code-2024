import pytest

from . import City, HARMONIC, RESTRICTED


@pytest.fixture
def aa():
    return City.parse_map(
        """\
        ..........
        ..........
        ..........
        ....a.....
        ..........
        .....a....
        ..........
        ..........
        ..........
        ..........
        """
    )


@pytest.fixture
def aaa():
    return City.parse_map(
        """\
        ..........
        ..........
        ..........
        ....a.....
        ........a.
        .....a....
        ..........
        ..........
        ..........
        ..........
        """
    )


@pytest.fixture
def AAA0000():
    return City.parse_map(
        """\
        ............
        ........0...
        .....0......
        .......0....
        ....0.......
        ......A.....
        ............
        ............
        ........A...
        .........A..
        ............
        ............
        """
    )


@pytest.fixture
def city(request, aa, aaa, AAA0000):
    return {"aa": aa, "aaa": aaa, "AAA0000": AAA0000}[request.param]


@pytest.mark.parametrize(
    "expected,city",
    [
        (
            City(
                 shape=(10, 10),
                 antennas={"a": {(3, 4), (5, 5)}}
            ),
            "aa"
        ),
        (
            City(
                 shape=(10, 10),
                 antennas={"a": {(3, 4), (5, 5), (4, 8)}}
            ),
            "aaa"
        ),
        (
            City(
                shape=(12, 12),
                antennas={
                    "0": {(1, 8), (2, 5), (3, 7), (4, 4)},
                    "A": {(5, 6), (8, 8), (9, 9)}
                }
            ),
            "AAA0000"
        )
    ],
    indirect=["city"]
)
def test_parse_map(expected, city):
    assert expected == city


@pytest.mark.parametrize(
    "expected,city",
    [
        (
            {(1, 3), (7, 6)},
            "aa"
        ),
        (
            {(2, 0), (1, 3), (7, 6), (6, 2)},
            "aaa"
        ),
        (
            {
                (0, 11), (3, 2),   # 0: (1,8) to (2,5)
                (5, 6),            # 0: (1,8) to (3,7)
                (7, 0),            # 0: (1,8) to (4,4)
                (1, 3), (4, 9),    # 0: (2,5) to (3,7)
                (0, 6), (6, 3),    # 0: (2,5) to (4,4)
                (2, 10), (5, 1),   # 0: (3,7) to (4,4)
                (2, 4), (11, 10),  # A: (5,6) to (8,8)
                (1, 3),            # A: (5,6) to (9,9)
                (7, 7), (10, 10),  # A: (8,8) to (9,9)
            },
            "AAA0000"
        )
    ],
    indirect=["city"]
)
def test_iter_antinodes_restricted(expected, city):
    assert expected == set(city.iter_antinodes(RESTRICTED))


@pytest.mark.parametrize(
    "expected,city",
    [(2, "aa"), (4, "aaa"), (14, "AAA0000")],
    indirect=["city"]
)
def test_count_antinodes_restricted(expected, city):
    assert expected == city.count_antinodes(RESTRICTED)


@pytest.mark.parametrize(
    "expected,city",
    [
        (
            {(1, 3), (3, 4), (5, 5), (7, 6), (9, 7)},
            "aa"
        ),
        (
            {
                (1, 3), (3, 4), (5, 5), (7, 6), (9, 7),  # a: (3,4) to (5,5)
                (2, 0), (3, 4), (4, 8),                  # a: (3,4) to (4,8)
                (6, 2), (5, 5), (4, 8),                  # a: (5,5) to (4,8)
            },
            "aaa"
        ),
        (
            {
                (0, 11), (1,8), (2,5), (3, 2),                   # 0: (1,8) to (2,5)
                (11, 3), (9, 4), (7, 5), (5, 6), (3, 7), (1, 8), # 0: (1,8) to (3,7)
                (1, 8), (4, 4), (7, 0),                          # 0: (1,8) to (4,4)
                (0, 1), (1, 3), (2, 5), (3, 7), (4, 9), (5, 11), # 0: (2,5) to (3,7)
                (0, 6), (2, 5), (4, 4), (6, 3), (8, 2), (10, 1), # 0: (2,5) to (4,4)
                (2, 10), (3, 7), (4, 4), (5, 1),                 # 0: (3,7) to (4,4)
                (2, 4), (5,6), (8,8), (11, 10),                  # A: (5,6) to (8,8)
                (1, 3), (5,6), (9,9),                            # A: (5,6) to (9,9)
                (0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6),
                (7, 7), (8,8), (9,9), (10, 10), (11,11),         # A: (8,8) to (9,9)
            },
            "AAA0000"
        ),
    ],
    indirect=["city"]
)
def test_iter_antinodes_harmonic(expected, city):
    assert expected == set(city.iter_antinodes(HARMONIC))


@pytest.mark.parametrize(
    "expected,city",
    [(5, "aa"), (8, "aaa"), (34, "AAA0000")],
    indirect=["city"]
)
def test_count_antinodes_harmonic(expected, city):
    assert expected == city.count_antinodes(HARMONIC)
