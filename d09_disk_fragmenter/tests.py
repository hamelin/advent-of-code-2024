import pytest

from . import Disk, FREE


@pytest.fixture
def maps():
    return [
        "12345",
        "90909",
        "2333133121414131402",
    ]


@pytest.mark.parametrize(
    "index,expected",
    enumerate([
        Disk([0, FREE, FREE, 1, 1, 1, FREE, FREE, FREE, FREE, 2, 2, 2, 2, 2]),
        Disk([0] * 9 + [1] * 9 + [2] * 9),
        Disk([
            0, 0,
            FREE, FREE, FREE,
            1, 1, 1,
            FREE, FREE, FREE,
            2,
            FREE, FREE, FREE,
            3, 3, 3,
            FREE,
            4, 4,
            FREE,
            5, 5, 5, 5,
            FREE,
            6, 6, 6, 6,
            FREE,
            7, 7, 7,
            FREE,
            8, 8, 8, 8,
            9, 9,
        ]),
    ])
)
def test_read_map(expected, index, maps):
    assert expected == Disk.read_map(maps[index])


@pytest.mark.parametrize(
    "index,lower,size,expected",
    [
        (0, 15, 1, (1, 2)),
        (0, 15, 2, (1, 3)),
        (0, 15, 3, (6, 9)),
        (0, 15, 4, (6, 10)),
        (0, 15, 5, None),
        (0, 10, 4, (6, 10)),
        (0, 9, 4, None),
        (2, 25, 1, (2, 3)),
        (2, 25, 3, (2, 5)),
        (2, 25, 4, None),
    ]
)
def test_find_free_lower(expected, index, lower, size, maps):
    assert expected == Disk.read_map(maps[index]).find_free_lower(lower, size)


@pytest.mark.parametrize(
    "index,expected",
    enumerate([
        Disk([0, 2, 2, 1, 1, 1, 2, 2, 2] + [FREE] * 6),
        Disk([0] * 9 + [1] * 9 + [2] * 9),
        Disk(
            [
                0, 0,
                9, 9, 8,
                1, 1, 1,
                8, 8, 8,
                2,
                7, 7, 7,
                3, 3, 3,
                6,
                4, 4,
                6,
                5, 5, 5, 5,
                6, 6,
            ] + [FREE] * 14
        )
    ])
)
def test_defragment(expected, index, maps):
    assert expected == Disk.read_map(maps[index]).defragment()


@pytest.mark.parametrize(
    "index,expected",
    enumerate([
        60,
        513,
        1928,
    ])
)
def test_checksum_defragment(expected, index, maps):
    assert expected == Disk.read_map(maps[index]).defragment().checksum()


@pytest.mark.parametrize(
    "index,expected",
    enumerate([
        [(10, 15), (3, 6), (0, 1)],
        [(18, 27), (9, 18), (0, 9)],
        [
            (40, 42),
            (36, 40),
            (32, 35),
            (27, 31),
            (22, 26),
            (19, 21),
            (15, 18),
            (11, 12),
            (5, 8),
            (0, 2)
        ]
    ])
)
def test_iter_blocks_reverse(expected, index, maps):
    assert expected == list(Disk.read_map(maps[index]).iter_blocks_reverse())


@pytest.mark.parametrize(
    "index,expected",
    enumerate([
        Disk([0, FREE, FREE, 1, 1, 1, FREE, FREE, FREE, FREE, 2, 2, 2, 2, 2]),
        Disk([0] * 9 + [1] * 9 + [2] * 9),
        Disk(
            [
                0, 0, 9, 9, 2, 1, 1, 1, 7, 7, 7, FREE,
                4, 4, FREE,
                3, 3, 3, FREE, FREE, FREE, FREE,
                5, 5, 5, 5, FREE,
                6, 6, 6, 6, FREE, FREE, FREE, FREE, FREE,
                8, 8, 8, 8, FREE, FREE
            ]
        )
    ])
)
def test_defragment_free(expected, index, maps):
    assert expected == Disk.read_map(maps[index]).defragment_free()


@pytest.mark.parametrize(
    "index,expected",
    enumerate([
        132,
        513,
        2858,
    ])
)
def test_checksum_defragment_free(expected, index, maps):
    assert expected == Disk.read_map(maps[index]).defragment_free().checksum()
