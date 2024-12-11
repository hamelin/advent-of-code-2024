import functools as ft


StoneRow = list[int]


def blink(stones_in: StoneRow) -> StoneRow:
    stones_out = []
    for stone in stones_in:
        if stone == 0:
            stones_out.append(1)
        elif len(s := str(stone)) & 1 == 0:
            j = len(s) // 2
            stones_out += [int(s[:j]), int(s[j:])]
        else:
            stones_out.append(stone * 2024)
    return stones_out


@ft.cache
def count_stones_after_blinks(stone: int, num_blinks: int, rng=range) -> int:
    assert num_blinks > 0
    stones = blink([stone])
    if num_blinks == 1:
        return len(stones)

    return sum(
        count_stones_after_blinks(s, num_blinks - 1, rng=rng)
        for s in stones
    )
