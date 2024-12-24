from copy import copy
import pytest

from . import *  # noqa


@pytest.mark.parametrize(
    "num,expected",
    [(100000000, 16113920)]
)
def test_prune(expected, num):
    actual = prune(num)
    assert expected == actual


@pytest.mark.parametrize(
    "num,secret,expected",
    [(15, 42, 37)]
)
def test_mix(secret, num, expected):
    actual = mix(secret, num)
    assert expected == actual


@pytest.fixture
def sequence():
    return [
        123,
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]


def test_sequence(sequence):
    expected = list(enumerate(sequence))
    actual = list(zip(range(11), iter_secrets(123)))
    assert expected == actual


@pytest.fixture
def seed_secret2000():
    return [
        (1, 8685429),
        (10, 4700978),
        (100, 15273692),
        (2024, 8667524),
    ]


@pytest.mark.parametrize("index", range(4))
def test_secret2000(index, seed_secret2000):
    seed, expected = seed_secret2000[index]
    actual = nth_secret(seed, 2000)
    assert expected == actual


@pytest.fixture
def change_dict(sequence):
    return {
        (-3, 6, -1, -1): {"123": 4},
        (6, -1, -1, 0): {"123": 4},
        (-1, -1, 0, 2): {"123": 6},
        (-1, 0, 2, -2): {"123": 4},
        (0, 2, -2, 0): {"123": 4},
        (2, -2, 0, -2): {"123": 2},
        (-2, 0, -2, 2): {"123": 4}
    }


def test_compile_change_dict(change_dict):
    expected = change_dict
    actual = compile_change_dict("123", 123, 10)
    assert expected == actual


def test_add_to_change_dict(change_dict):
    term = {
        (0, 2, -2, 0): {"asdf": 7},
        (2, -2, 0, -5): {"asdf": 2}
    }
    expected = copy(change_dict)
    expected[(0, 2, -2, 0)]["asdf"] = 11
    expected[(2, -2, 0, -5)] = {"asdf": 2}
    actual = copy(change_dict)
    add_to_change_dict(actual, term)
    assert expected == actual


def test_most_profitable_change():
    expected_change = (-2, 1, -1, 3)
    expected_payoff = 23

    change_dict = {}
    for seed in [1, 2, 3, 2024]:
        term = compile_change_dict(str(seed), seed, limit=2000)
        add_to_change_dict(change_dict, term)
    actual_change, actual_payoff = most_profitable_change(change_dict)

    print(actual_payoff)
    assert expected_change == actual_change
    assert expected_payoff == actual_payoff
