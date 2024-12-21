import pytest

from . import *  # noqa


@pytest.fixture
def text():
    return """\
        ###############
        #...#...#.....#
        #.#.#.#.#.###.#
        #S#...#.#.#...#
        #######.#.#.###
        #######.#.#...#
        #######.#.###.#
        ###..E#...#...#
        ###.#######.###
        #...###...#...#
        #.#####.#.###.#
        #.#...#.#.#...#
        #.#.#.#.#.#.###
        #...#...#...###
        ###############
    """


@pytest.fixture
def race_track(text):
    return RaceTrack.parse(text)


def test_parse(race_track, text):
    assert dedent(text).strip() == race_track.as_map()


def test_costs_from_to(race_track):
    race_track.init()
    for costs in [race_track.cost_from, race_track.cost_to]:
        assert len(costs) == 85
    assert set(race_track.cost_from.keys()) == set(race_track.cost_to.keys())
    for pos in race_track.cost_from.keys():
        assert race_track.cost_from[pos] + race_track.cost_to[pos] == 84


@pytest.mark.parametrize(
    "cheat,expected",
    [
        (Cheat((1, 7), (1, 9)), 12),
        (Cheat((7, 9), (7, 11)), 20),
        (Cheat((7, 8), (9, 8)), 38),
        (Cheat((7, 7), (7, 5)), 64)
    ]
)
def test_cost_cheat(race_track, expected, cheat):
    race_track.init()
    actual = race_track.saving_with_cheat(cheat)
    assert expected == actual


def test_iter_cheats_up_to_2(race_track):
    race_track.init()
    expected = {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
    actual = {}
    for cheat, saving in race_track.iter_cheats(2):
        actual.setdefault(saving, 0)
        actual[saving] += 1
    assert expected == actual


@pytest.mark.parametrize(
    "position,dist_max,expected",
    [
        ((5, 5), 1, set()),
        ((5, 5), 2, {(5, 7), (7, 5), (3, 5)}),
        (
            (5, 5),
            3,
            {
                (5, 7), (7, 5), (3, 5),
                (4, 7), (2, 5), (3, 4), (7, 4), (6, 7)
            }
        )
    ]
)
def test_iter_free_within(expected, race_track, position, dist_max):
    actual = set(race_track.iter_free_within(position, dist_max))
    assert expected == actual


def test_iter_cheats_up_to_20_saving_ge50(race_track):
    race_track.init()
    expected = {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }
    actual = {}
    for cheat, saving in race_track.iter_cheats(20):
        if saving >= 50:
            actual.setdefault(saving, 0)
            actual[saving] += 1
    assert expected == actual
