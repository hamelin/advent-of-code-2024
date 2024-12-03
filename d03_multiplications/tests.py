import pytest

from . import (
    iter_pairs_factors,
    iter_pairs_factors_cond,
    process_muls,
    process_muls_cond,
)


@pytest.mark.parametrize(
    "expected,mul",
    [([(44, 46)], "mul(44,46)"), ([(123, 4)], "mul(123,4)")]
)
def test_ipf_alone(expected, mul):
    assert expected == list(iter_pairs_factors(mul))


@pytest.mark.parametrize("mul", ["mul(4*", "mul(6,9!", "?(12,34)", "mul ( 2, 4 )"])
def test_corrupted(mul):
    assert [] == list(iter_pairs_factors(mul))


@pytest.fixture
def mul_complicated():
    return "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"


def test_ipf_complicated(mul_complicated):
    assert [(2, 4), (5, 5), (11, 8), (8, 5)] == list(
        iter_pairs_factors(mul_complicated)
    )


def test_mul_complicated(mul_complicated):
    assert 161 == process_muls(mul_complicated)


@pytest.fixture
def mul_do_dont():
    return "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def test_iter_pairs_factors_cond(mul_do_dont):
    assert [(2, 4), (8, 5)] == list(iter_pairs_factors_cond(mul_do_dont))


def test_mul_cond(mul_do_dont):
    assert 48 == process_muls_cond(mul_do_dont)
