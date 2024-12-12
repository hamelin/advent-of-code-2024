import pytest
from textwrap import dedent

from . import Garden, Region, Edge


@pytest.fixture
def maps():
    return {
        "small": """\
            AAAA
            BBCD
            BBCC
            EEEC
        """,
        "fragmented": """\
            OOOOO
            OXOXO
            OOOOO
            OXOXO
            OOOOO
        """,
        "large": """\
            RRRRIICCFF
            RRRRIICCCF
            VVRRRCCFFF
            VVRCCCJFFF
            VVVVCJJCFE
            VVIVCCJJEE
            VVIIICJJEE
            MIIIIIJJEE
            MIIISIJEEE
            MMMISSJEEE
        """,
        "ex": """\
            EEEEE
            EXXXX
            EEEEE
            EXXXX
            EEEEE
        """,
        "Bblocks": """\
            AAAAAA
            AAABBA
            AAABBA
            ABBAAA
            ABBAAA
            AAAAAA
        """,
        "bigu": """\
            XOOOX
            XOOOX
            XXXXX
        """
    }


@pytest.fixture
def gardens(maps):
    return {name: Garden.read_map(map) for name, map in maps.items()}


@pytest.mark.parametrize(
    "name,shape,regions",
    [
        (
            "small",
            (4, 4),
            {
                Region("A", {(0,0), (0,1), (0,2), (0,3)}),
                Region("B", {(1,0), (1,1), (2,0), (2,1)}),
                Region("C", {(1,2), (2,2), (2,3), (3,3)}),
                Region("D", {(1,3)}),
                Region("E", {(3,0), (3,1), (3,2)})
            }
        ),
        (
            "fragmented",
            (5, 5),
            {
                Region(
                    "O",
                    {
                        (0,0), (0,1), (0,2), (0,3), (0,4),
                        (1,0),        (1,2),        (1,4),
                        (2,0), (2,1), (2,2), (2,3), (2,4),
                        (3,0),        (3,2),        (3,4),
                        (4,0), (4,1), (4,2), (4,3), (4,4),
                    }
                ),
                Region("X", {(1,1)}),
                Region("X", {(1,3)}),
                Region("X", {(3,1)}),
                Region("X", {(3,3)}),
            }
        ),
        (
            "large",
            (10, 10),
            {
                Region(
                    "R",
                    {
                        (0,0), (0,1), (0,2), (0,3),
                        (1,0), (1,1), (1,2), (1,3),
                                      (2,2), (2,3), (2,4),
                                      (3,2),
                    }
                ),
                Region(
                    "I",
                    {
                        (0,4), (0,5),
                        (1,4), (1,5),
                    }
                ),
                Region(
                    "C",
                    {
                                             (0,6), (0,7),
                                             (1,6), (1,7), (1,8),
                                      (2,5), (2,6),
                        (3,3), (3,4), (3,5),
                               (4,4),
                               (5,4), (5,5),
                                      (6,5),
                    }
                ),
                Region(
                    "F",
                    {
                               (0,8), (0,9),
                                      (1,9),
                        (2,7), (2,8), (2,9),
                        (3,7), (3,8), (3,9),
                               (4,8),
                    }
                ),
                Region(
                    "V",
                    {
                        (2,0), (2,1),
                        (3,0), (3,1),
                        (4,0), (4,1), (4,2), (4,3),
                        (5,0), (5,1),        (5,3),
                        (6,0), (6,1),
                    }
                ),
                Region(
                    "J",
                    {
                               (3,6),
                        (4,5), (4,6),
                               (5,6), (5,7),
                               (6,6), (6,7),
                               (7,6), (7,7),
                               (8,6),
                               (9,6),
                    }
                ),
                Region(
                    "E",
                    {
                                      (4,9),
                               (5,8), (5,9),
                               (6,8), (6,9),
                               (7,8), (7,9),
                        (8,7), (8,8), (8,9),
                        (9,7), (9,8), (9,9),
                    }
                ),
                Region("C", {(4,7)}),
                Region(
                    "I",
                    {
                               (5,2),
                               (6,2), (6,3), (6,4),
                        (7,1), (7,2), (7,3), (7,4), (7,5),
                        (8,1), (8,2), (8,3),        (8,5),
                                      (9,3),
                    }
                ),
                Region(
                    "M",
                    {
                        (7,0),
                        (8,0),
                        (9,0), (9,1), (9,2),
                    }
                ),
                Region(
                    "S",
                    {
                        (8,4),
                        (9,4), (9,5),
                    }
                )
            }
        )
    ]
)
def test_read_map(regions, shape, name, gardens):
    assert Garden(shape=shape, regions=regions) == gardens[name]


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "small",
            [
                ("A", 4, 10),
                ("B", 4, 8),
                ("C", 4, 10),
                ("D", 1, 4),
                ("E", 3, 8),
            ]
        ),
        (
            "fragmented",
            [
                ("O", 21, 36),
                ("X", 1, 4),
                ("X", 1, 4),
                ("X", 1, 4),
                ("X", 1, 4),
            ]
        ),
        (
            "large",
            [
                ("C", 1, 4),
                ("C", 14, 28),
                ("E", 13, 18),
                ("F", 10, 18),
                ("I", 4, 8),
                ("I", 14, 22),
                ("J", 11, 20),
                ("M", 5, 12),
                ("R", 12, 18),
                ("S", 3, 8),
                ("V", 13, 20),
            ]
        )
    ]
)
def test_geometry(expected, name, gardens):
    assert expected == sorted([tuple(g) for g in gardens[name].geometry()])


@pytest.mark.parametrize(
    "name,expected",
    [("small", 140), ("fragmented", 772), ("large", 1930)]
)
def test_cost_fences(expected, name, gardens):
    assert expected == gardens[name].cost_fences()


def as_edge_sets(s):
    return [
        [
            {
                e
                for s, e in {
                    "t": Edge.top,
                    "b": Edge.bottom,
                    "l": Edge.left,
                    "r": Edge.right
                }.items()
                if s in group
            }
            for group in line.split("|")
        ]
        for line in dedent(s).strip().split("\n")
    ]


@pytest.mark.parametrize(
    "name,expected",
    [
        (
            "small",
            """\
                tbl |tb  |tb  |tb r
                t l |t  r|t lr|tblr
                 bl | b r| bl |t  r
                tbl |tb  |tb r| blr
            """
        ),
        (
            "fragmented",
            """\
                t l |tb  |t   |tb  |t  r
                  lr|tblr|  lr|tblr|  lr
                  l |tb  |    |tb  |   r
                  lr|tblr|  lr|tblr|  lr
                 bl |tb  | b  |tb  | b r
            """
        ),
        (
            "large",
            """\
                t l |t   |t   |t  r|t l |t  r|t l |t  r|tbl |t  r
                 bl | b  |    |   r| bl | b r|  l | b  |tb r|  lr
                t l |t  r|  l | b  |tb r|t l | b r|t l |t   |   r
                  l |   r| blr|tbl |t   | b r|t lr| bl |    | b r
                  l |    |tb  |t  r|  lr|tbl |   r|tblr| blr|t lr
                  l |   r|t lr| blr| bl |t  r|  l |t  r|t l |   r
                 bl | b r|  l |t   |t  r| blr|  l |   r|  l |   r
                t lr|t l |    |    | b  |t  r|  l | b r|  l |   r
                  lr| bl | b  |   r|t lr| blr|  lr|t l |    |   r
                 bl |tb  |tb r| blr| bl |tb r| blr| bl | b  | b r
            """
        ),
        (
            "ex",
            """\
                t l |tb  |tb  |tb  |tb r
                  lr|tbl |tb  |tb  |tb r
                  l |tb  |tb  |tb  |tb r
                  lr|tbl |tb  |tb  |tb r
                 bl |tb  |tb  |tb  |tb r
            """
        ),
        (
            "Bblocks",
            """\
                t l |t   |t   |tb  |tb  |t  r
                  l |    |   r|t l |t  r|  lr
                  l | b  | b r| bl | b r|  lr
                  lr|t l |t  r|t l |t   |   r
                  lr| bl | b r|  l |    |   r
                 bl |tb  |tb  | b  | b  | b r
            """
        ),
        (
            "bigu",
            """\
                t lr|t l |t   |t  r|t lr
                  lr| bl | b  | b r|  lr
                 bl |tb  |tb  |tb  | b r
            """
        )
    ]
)
def test_edge_sets(expected,name,gardens):
    garden = gardens[name]
    edge_set_actual = [
        [set() for __ in range(garden.shape[1])]
        for _ in range(garden.shape[0])
    ]
    for region in garden.regions:
        for (row, col), edge in region.iter_edges():
            edge_set_actual[row][col].add(edge)
    assert as_edge_sets(expected) == edge_set_actual


# @pytest.mark.parametrize(
#     "name,expected",
#     [
#         (
#             "small",
#             {
#                 ("A", TOP, (0,0), 4),
#                 ("A", LEFT, (0,0), 1),
#                 ("A", RIGHT, 1),
#                 ("A", BOTTOM, 4),
#                 ("B", TOP, 2),
#                 ("B", "LEFT", 2),
#                 ("B", "RIGHT", 2),
#                 ("B", BOTTOM, 2),
#                 ("C", TOP, 1),
#                 ("C", TOP, 1),
#                 ("C", "LEFT", 2),
#                 ("C", "RIGHT", 2),
#                 ("C", LEFT, 1),
#                 ("C", RIGHT, 1),
#                 ("C", )
#             }
#         )
#     ]
# )
# def test_find_sides(expected,name,gardens):
