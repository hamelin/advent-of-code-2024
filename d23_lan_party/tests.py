import pytest

from . import *  # noqa


@pytest.fixture
def text():
    return """\
        kh-tc
        qp-kh
        de-cg
        ka-co
        yn-aq
        qp-ub
        cg-tb
        vc-aq
        tb-ka
        wh-tc
        yn-cg
        kh-ub
        ta-co
        de-co
        tc-td
        tb-wq
        wh-td
        ta-ka
        td-qp
        aq-cg
        wq-ub
        ub-vc
        de-ta
        wq-aq
        wq-vc
        wh-yn
        ka-de
        kh-ta
        co-tc
        wh-qp
        tb-vc
        td-yn
    """


@pytest.fixture
def network(text):
    return Network.parse(text)


def test_parse(network):
    assert Network(
        connections={
            "aq": {"cg", "vc", "wq", "yn"},
            "cg": {"aq", "de", "tb", "yn"},
            "co": {"de", "ka", "ta", "tc"},
            "de": {"cg", "co", "ka", "ta"},
            "ka": {"co", "de", "ta", "tb"},
            "kh": {"qp", "ta", "tc", "ub"},
            "qp": {"kh", "td", "ub", "wh"},
            "ta": {"co", "de", "ka", "kh"},
            "tb": {"cg", "ka", "vc", "wq"},
            "tc": {"co", "kh", "wh", "td"},
            "td": {"tc", "wh", "qp", "yn"},
            "ub": {"qp", "kh", "vc", "wq"},
            "vc": {"aq", "tb", "ub", "wq"},
            "wh": {"qp", "tc", "td", "yn"},
            "wq": {"aq", "tb", "ub", "vc"},
            "yn": {"aq", "cg", "td", "wh"},
        }
    ) == network


def test_iter_edges(network):
    expected = {
        ("aq", "cg"), ("aq", "vc"), ("aq", "wq"), ("aq", "yn"),
        ("cg", "de"), ("cg", "tb"), ("cg", "yn"),
        ("co", "de"), ("co", "ka"), ("co", "ta"), ("co", "tc"),
        ("de", "ka"), ("de", "ta"),
        ("ka", "ta"), ("ka", "tb"),
        ("kh", "qp"), ("kh", "ta"), ("kh", "tc"), ("kh", "ub"),
        ("qp", "td"), ("qp", "ub"), ("qp", "wh"),
        ("tb", "vc"), ("tb", "wq"),
        ("tc", "td"), ("tc", "wh"),
        ("td", "wh"), ("td", "yn"),
        ("ub", "vc"), ("ub", "wq"),
        ("vc", "wq"),
        ("wh", "yn"),
    }
    list_edges = list(network.iter_edges())
    assert len(expected) == len(list_edges)
    actual = set(list_edges)
    assert expected == actual


def test_iter_cliques3(network):
    expected = {
        ("aq", "cg", "yn"),
        ("aq", "vc", "wq"),
        ("co", "de", "ka"),
        ("co", "de", "ta"),
        ("co", "ka", "ta"),
        ("de", "ka", "ta"),
        ("kh", "qp", "ub"),
        ("qp", "td", "wh"),
        ("tb", "vc", "wq"),
        ("tc", "td", "wh"),
        ("td", "wh", "yn"),
        ("ub", "vc", "wq"),
    }
    actual = set(network.iter_cliques3())
    assert expected == actual


def test_iter_cliques3_with_t_computer(network):
    expected = {
        ("co", "de", "ta"),
        ("co", "ka", "ta"),
        ("de", "ka", "ta"),
        ("qp", "td", "wh"),
        ("tb", "vc", "wq"),
        ("tc", "td", "wh"),
        ("td", "wh", "yn"),
    }
    actual = set(iter_cliques3_with_t_computer(network))
    assert expected == actual


def test_get_largest_cliques(network):
    expected = {("co", "de", "ka", "ta")}
    actual = network.get_largest_cliques()
    assert expected == actual
