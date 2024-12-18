import pytest

from . import *  # noqa


@pytest.fixture
def text():
    return """\
        5,4
        4,2
        4,5
        3,0
        2,1
        6,3
        2,4
        1,5
        0,6
        3,3
        2,6
        5,1
        1,2
        5,5
        2,5
        6,5
        1,4
        0,4
        6,4
        1,1
        6,1
        1,0
        0,5
        1,6
        2,0
    """


@pytest.fixture
def game(text):
    return Game((7, 7)).with_bytes_from_text(text)


def test_parse(game):
    assert Game(
        shape=(7, 7),
        bytes=[
            (4, 5), (2, 4), (5, 4), (0, 3), (1, 2), (3, 6), (4, 2), (5, 1),
            (6, 0), (3, 3), (6, 2), (1, 5), (2, 1), (5, 5), (5, 2), (5, 6),
            (4, 1), (4, 0), (4, 6), (1, 1), (1, 6), (0, 1), (5, 0), (6, 1),
            (0, 2)
        ]
    ) == game


@pytest.fixture
def ram_after_12(game):
    return game.after_fallen(12)


def test_after_fallen(ram_after_12):
    assert RAM(
        shape=(7, 7),
        corrupted={
            (4, 5), (2, 4), (5, 4), (0, 3), (1, 2), (3, 6),
            (4, 2), (5, 1), (6, 0), (3, 3), (6, 2), (1, 5),
        }
    ) == ram_after_12


def test_length_path_shortest(ram_after_12):
    length_path_shortest = ram_after_12.length_path_shortest()
    assert 22 == length_path_shortest


def test_has_path_after_1_1(game):
    for ram in game:
        if (1, 1) in ram.corrupted:
            break
    else:
        pytest.fail("Supposed to stop once got (1,1)")
    assert ram.length_path_shortest() is not None


def test_no_path_after_6_1(game):
    for ram in game:
        if (6, 1) in ram.corrupted:
            break
    else:
        pytest.fail("Supposed to stop once got (6,1)")
    assert ram.length_path_shortest() is None
