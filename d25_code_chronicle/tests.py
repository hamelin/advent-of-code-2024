import pytest

from . import *  # noqa


@pytest.fixture
def text():
    return """\
        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....

        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####

        #####
        ##.##
        .#.##
        ...##
        ...#.
        ...#.
        .....

        .....
        .....
        #.#..
        ###..
        ###.#
        ###.#
        #####

        .....
        .....
        .....
        #....
        #.#..
        #.#.#
        #####
    """


@pytest.fixture
def puzzle(text):
    return Puzzle.parse(text)


@pytest.fixture
def locks():
    return [(1, 6, 4, 5, 4), (2, 3, 1, 6, 4)]


@pytest.fixture
def keys():
    return [(6, 1, 3, 2, 4), (5, 4, 5, 1, 3), (4, 1, 3, 1, 2)]


def test_parse(puzzle, locks, keys):
    assert Puzzle(height=7, locks=set(locks), keys=set(keys)) == puzzle


@pytest.mark.parametrize(
    "i_lock,i_key,expected",
    [
        (0, 0, False),
        (0, 1, False),
        (0, 2, True),
        (1, 0, False),
        (1, 1, True),
        (1, 2, True),
    ]
)
def test_does_key_fit_lock(expected, i_key, i_lock, keys, locks, puzzle):
    actual = puzzle.does_key_fit_lock(keys[i_key], locks[i_lock])
    assert expected == actual


def test_count_fits(puzzle):
    expected = 3
    actual = puzzle.count_fits()
    assert expected == actual
