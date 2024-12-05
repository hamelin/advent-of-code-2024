import pytest
from textwrap import dedent

from . import (
    fix_update,
    get_middle_page,
    index_first_page_pair_invalid,
    is_update_valid,
    iter_middle_page_updates_invalid_fixed,
    iter_middle_page_updates_valid,
    parse_rules,
    parse_updates,
    split_rules_updates,
)


@pytest.fixture
def example_text():
    return dedent(
        """\
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
        """
    ).rstrip().split("\n")


@pytest.fixture
def text_rules_updates(example_text):
    return split_rules_updates(example_text)


def test_split_rules_updates(text_rules_updates):
    assert (
        [
            "47|53",
            "97|13",
            "97|61",
            "97|47",
            "75|29",
            "61|13",
            "75|53",
            "29|13",
            "97|29",
            "53|29",
            "61|53",
            "97|53",
            "61|29",
            "47|13",
            "75|47",
            "97|75",
            "47|61",
            "75|61",
            "47|29",
            "75|13",
            "53|13",
        ],
        [
            "75,47,61,53,29",
            "97,61,53,29,13",
            "75,29,13",
            "75,97,47,61,53",
            "61,13,29",
            "97,13,75,29,47",
        ]
    ) == text_rules_updates


@pytest.fixture
def rules(text_rules_updates):
    text_rules, _ = text_rules_updates
    return parse_rules(text_rules)


def test_parse_rules(rules):
    assert {
        47: {53, 13, 61, 29},
        97: {13, 61, 47, 29, 53, 75},
        75: {29, 53, 47, 61, 13},
        61: {13, 53, 29},
        29: {13},
        53: {29, 13},
    } == rules


@pytest.fixture
def updates(text_rules_updates):
    _, text_updates = text_rules_updates
    return parse_updates(text_updates)


def test_parse_updates(updates):
    assert [
        [75, 47, 61, 53, 29],
        [97, 61, 53, 29, 13],
        [75, 29, 13],
        [75, 97, 47, 61, 53],
        [61, 13, 29],
        [97, 13, 75, 29, 47],
    ] == updates


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([True, True, True, False, False, False]))
)
def test_evaluate_update_valid(index, expected, rules, updates):
    assert expected == is_update_valid(rules, updates[index])


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([61, 53, 29, 47, 13, 75]))
)
def test_get_middle_page(index, expected, updates):
    assert expected == get_middle_page(updates[index])


def test_iter_middle_page_updates_valid(rules, updates):
    assert [61, 53, 29] == list(iter_middle_page_updates_valid(rules, updates))


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([-1, -1, -1, 0, 1, 1]))
)
def test_index_first_page_pair_invalid(expected, index, rules, updates):
    assert expected == index_first_page_pair_invalid(rules, updates[index])


@pytest.mark.parametrize(
    "index,expected",
    list(enumerate([
        [75, 47, 61, 53, 29],
        [97, 61, 53, 29, 13],
        [75, 29, 13],
        [97, 75, 47, 61, 53],
        [61, 29, 13],
        [97, 75, 47, 29, 13],
    ]))
)
def test_fix_update(expected, index, rules, updates):
    assert expected == fix_update(rules, updates[index])


def test_iter_middle_page_updates_fixed(rules, updates):
    assert [47, 29, 47] == list(
        iter_middle_page_updates_invalid_fixed(rules, updates)
    )
