from copy import copy
import pytest

from . import *  # noqa


@pytest.mark.parametrize(
    "keypad,code,expected",
    [
        (KEYPAD_DOOR, "029A", {"<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"}),
        (KEYPAD_ROBOT, "<A^A>^^AvvvA", {"v<<A>>^A<A>AvA<^AA>A<vAAA>^A"}),
        (
            KEYPAD_ROBOT,
            "v<<A>>^A<A>AvA<^AA>A<vAAA>^A",
            {"<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"}
        )
    ]
)
def test_iter_solutions(keypad, expected, code):
    set_solutions = set(keypad.iter_solutions(code))
    assert expected <= set_solutions


@pytest.fixture
def five_codes():
    return [
        ("029A", "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"),  # noqa
        ("980A", "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"),
        ("179A", "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),  # noqa
        ("456A", "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"),
        ("379A", "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")
    ]


@pytest.mark.parametrize("index", range(5))
def test_find_length_shortest_solution(index, five_codes):
    code, example_solution = five_codes[index]
    expected = len(example_solution)
    solution1 = find_xss_2robots(code)
    actual = len(solution1)
    assert expected == actual


@pytest.mark.parametrize("index,expected", enumerate([29, 980, 179, 456, 379]))
def test_get_number_code(expected, index, five_codes):
    code, _ = five_codes[index]
    actual = get_number_code(code)
    assert expected == actual


@pytest.mark.parametrize(
    "index,expected",
    enumerate([68 * 29, 60 * 980, 68 * 179, 64 * 456, 64 * 379,])
)
def test_complexity_code(expected, index, five_codes):
    code, solution = five_codes[index]
    actual = complexity_code(code, len(solution))
    assert expected == actual


@pytest.mark.parametrize(
    "keypad,code,expected",
    [
        (KEYPAD_DOOR, "029A", 28),
        (KEYPAD_ROBOT, "<A^A^^>AvvvA", 68)
    ]
)
def test_example_least_twists_is_good(keypad, code, expected):
    for elt in keypad.iter_solutions_best(code):
        sol_shortest = min(KEYPAD_ROBOT.iter_solutions_best(elt), key=len)
        actual = len(sol_shortest)
        assert expected == actual


@pytest.fixture
def dict_count_pairs_keys():
    d = {
        f"{a}{b}": 0
        for a in "A^v<>"
        for b in "A^v<>"
    }
    assert 25 == len(d)
    assert all(0 == v for v in d.values())
    return d


@pytest.mark.parametrize(
    "keys_,nonzeros",
    [
        ([], {}),
        (["^<>vAAA^"], {"A^": 2, "^<": 1, "<>": 1, ">v": 1, "vA": 1, "AA": 2}),
        (
            ["^<>vAAA^", "^<AA"],
            {
                "A^": 2,
                "^<": 2,
                "<>": 1,
                ">v": 1,
                "vA": 1,
                "AA": 3,
                "^^": 1,
                "<A": 1,
            }
        )
    ]
)
def test_gestures(dict_count_pairs_keys, nonzeros, keys_):
    g = Gestures()
    for keys in keys_:
        g.update(keys)
    actual = dict(g)

    expected = copy(dict_count_pairs_keys)
    expected.update(nonzeros)
    assert expected == actual


def test_gestures_inflate(dict_count_pairs_keys):
    g = Gestures()
    g.update("v^Av", 5)
    actual = dict(g)

    expected = copy(dict_count_pairs_keys)
    expected.update({"Av": 10, "v^": 5, "^A": 5})
    assert expected == actual


@pytest.mark.parametrize(
    "keys,expected",
    [
        ("", 0),
        ("AAA<>A^v", 8)
    ]
)
def test_summary_len(expected, keys):
    actual = len(Summary.from_keys(keys))
    assert expected == actual


@pytest.fixture
def plan():
    return {
        "AA": "A",
        "A^": "<A",
        "Av": "<vA",
        "A<": "v<<A",
        "A>": "vA",
        "^A": ">A",
        "^^": "A",
        "^v": "vA",
        "^<": "v<A",
        "^>": "v>A",
        "vA": ">^A",
        "v^": "^A",
        "vv": "A",
        "v<": "<A",
        "v>": ">A",
        "<A": ">>^A",
        "<^": ">^A",
        "<v": ">A",
        "<<": "A",
        "<>": ">>A",
        ">A": "^A",
        ">^": "<^A",
        ">v": "<A",
        "><": "<<A",
        ">>": "A",
    }


def test_summary_expand(plan):
    summary = Summary.from_keys("vv>A^AA^")
    assert 8 == len(summary)
    expanded = summary.expand(plan)

    expected = len("<vAA>A^A<A>AA<A")
    actual = len(expanded)
    assert expected == actual


@pytest.fixture
def plan_robot():
    return get_plan("robot")


@pytest.mark.parametrize(
    "keys,expected",
    [
        ("<A^A>^^AvvvA", len("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")),
        (
            "v<<A>>^A<A>AvA<^AA>A<vAAA>^A",
            len("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A")
        )
    ]
)
def test_measure_solution_one_step(expected, keys, plan_robot):
    summary = Summary.from_keys(keys).expand(plan_robot)
    actual = len(summary)
    assert expected == actual


@pytest.mark.parametrize("index", range(5))
def test_measure_shortest_solution_2robots(index, five_codes):
    code, example_solution_best = five_codes[index]
    expected = len(example_solution_best)
    actual = measure_shortest_solution(code, 2)
    assert expected == actual
