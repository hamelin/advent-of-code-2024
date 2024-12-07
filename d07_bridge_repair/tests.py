from collections.abc import Sequence
import pytest
from textwrap import dedent

from . import (
    ADD,
    AM,
    AMC,
    Computation,
    CON,
    Equation,
    MUL,
    parse_equations,
    sum_results_equations_computing
)


@pytest.fixture
def text() -> str:
    return dedent(
        """\
        190: 10 19
        3267: 81 40 27
        83: 17 5
        156: 15 6
        7290: 6 8 6 15
        161011: 16 10 13
        192: 17 8 14
        21037: 9 7 18 13
        292: 11 6 16 20
        """
    ).strip()


@pytest.fixture
def equations(text) -> Sequence[Equation]:
    return parse_equations(text)


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([
        (190, [10, 19]),
        (3267, [81, 40, 27]),
        (83, [17, 5]),
        (156, [15, 6]),
        (7290, [6, 8, 6, 15]),
        (161011, [16, 10, 13]),
        (192, [17, 8, 14]),
        (21037, [9, 7, 18, 13]),
        (292, [11, 6, 16, 20]),
    ]))
)
def test_parse_equation(expected, index, equations):
    assert Equation(*expected) == equations[index]


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([
        [[MUL]],
        [[ADD, MUL], [MUL, ADD]],
        [],
        [],
        [],
        [],
        [],
        [],
        [[ADD, MUL, ADD]]
    ]))
)
def test_iter_computations_am(expected, index, equations):
    assert {Computation(list(seq)) for seq in expected} == set(
        equations[index].iter_computations(AM)
    )


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([True, True, False, False, False, False, False, False, True]))
)
def test_does_compute(expected, index, equations):
    assert expected == equations[index].does_compute(AM)


def test_sum_results_equations_computing_am(equations):
    assert 3749 == sum_results_equations_computing(equations, AM)


def test_CON():
    assert 156 == CON(15, 6)


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([
        [[MUL]],
        [[ADD, MUL], [MUL, ADD]],
        [],
        [[CON]],
        [[MUL, CON, MUL]],
        [],
        [[CON, ADD]],
        [],
        [[ADD, MUL, ADD]]
    ]))
)
def test_iter_computations_amc(expected, index, equations):
    assert {Computation(list(seq)) for seq in expected} == set(
        equations[index].iter_computations(AMC)
    )


def test_sum_results_equations_computing_amc(equations):
    assert 11387 == sum_results_equations_computing(equations, AMC)
