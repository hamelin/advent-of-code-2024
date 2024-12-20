import pytest

from . import *  # noqa


@pytest.fixture
def text():
    return """\
        r, wr, b, g, bwu, rb, gb, br

        brwrr
        bggr
        gbbr
        rrbgbr
        ubwu
        bwurrg
        brgr
        bbrgwb
    """


@pytest.fixture
def onsen(text):
    return Onsen.parse(text)


def test_parse(onsen):
    assert Onsen(
        towels=["r", "wr", "b", "g", "bwu", "rb", "gb", "br"],
        designs=[
            "brwrr",
            "bggr",
            "gbbr",
            "rrbgbr",
            "ubwu",
            "bwurrg",
            "brgr",
            "bbrgwb"
        ],
        prefixes={}
    ) == onsen


def test_init(onsen):
    onsen.init()
    assert {"ubwu", "bbrgwb"} == onsen.impossibles
    assert {
        "b": {"bggr", "brgr", "brwrr", "bwurrg"},
        "bg": {"bggr"},
        "bgg": {"bggr"},
        "bggr": {"bggr"},
        "br": {"brwrr", "brgr"},
        "brg": {"brgr"},
        "brgr": {"brgr"},
        "brw": {"brwrr"},
        "brwr": {"brwrr"},
        "brwrr": {"brwrr"},
        "bw": {"bwurrg"},
        "bwu": {"bwurrg"},
        "bwur": {"bwurrg"},
        "bwurr": {"bwurrg"},
        "bwurrg": {"bwurrg"},
        "g": {"gbbr"},
        "gb": {"gbbr"},
        "gbb": {"gbbr"},
        "gbbr": {"gbbr"},
        "r": {"rrbgbr"},
        "rr": {"rrbgbr"},
        "rrb": {"rrbgbr"},
        "rrbg": {"rrbgbr"},
        "rrbgb": {"rrbgbr"},
        "rrbgbr": {"rrbgbr"},
    } == onsen.prefixes


def test_iter_designs_possible(onsen):
    expected = {"brwrr", "bggr", "gbbr", "rrbgbr", "bwurrg", "brgr"}
    actual = set(onsen.iter_designs_possible())
    assert expected == actual


def test_count_designs_possible(onsen):
    assert 6 == onsen.count_designs_possible()


@pytest.mark.parametrize(
    "design,expected",
    [
        ("brwrr", 2),
        ("bggr", 1),
        ("gbbr", 4),
        ("rrbgbr", 6),
        ("bwurrg", 1),
        ("brgr", 2),
        ("ubwu", 0),
        ("bbrgwb", 0)
    ]
)
def test_count_arrangements_design(expected, design, onsen):
    actual = onsen.count_arrangements_design(design)
    assert expected == actual
