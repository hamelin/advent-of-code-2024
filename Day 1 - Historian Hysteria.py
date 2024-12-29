import marimo

__generated_with = "0.10.7"
app = marimo.App(width="full")


@app.cell
def _():
    from collections import defaultdict
    from collections.abc import Mapping
    import itertools as it
    import marimo as mo
    from pathlib import Path
    from textwrap import dedent
    return Mapping, Path, dedent, defaultdict, it, mo


@app.cell
def _():
    text = """
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """
    return (text,)


@app.cell
def _():
    Location = int
    return (Location,)


@app.cell
def _(Location, dedent):
    def parse_lists_side_by_side(text: str) -> tuple[list[Location], list[Location]]:
        pairs_locations = [
            (Location(left), Location(right))
            for left, right in [
                line.strip().split()
                for line in dedent(text).strip().split("\n")
                if line.strip()
            ]
        ]
        return tuple(list(t) for t in zip(*pairs_locations))
    return (parse_lists_side_by_side,)


@app.cell
def _(parse_lists_side_by_side, text):
    lists_side_by_side = parse_lists_side_by_side(text)
    _expected = ([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3])
    _actual = lists_side_by_side
    assert _expected == _actual
    return (lists_side_by_side,)


@app.cell
def _(lists_side_by_side):
    locations_left, locations_right = lists_side_by_side
    return locations_left, locations_right


@app.cell
def _(Location):
    def distance_between_lists(left: list[Location], right: list[Location]) -> int:
        return sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))
    return (distance_between_lists,)


@app.cell
def _(distance_between_lists, locations_left, locations_right):
    _expected = 11
    _actual = distance_between_lists(locations_left, locations_right)
    assert _expected == _actual
    return


@app.cell
def _(Path, distance_between_lists, parse_lists_side_by_side):
    path_input = Path("inputs/01.txt")
    INPUT = path_input.read_text(encoding="utf-8")
    LOCATIONS_LEFT, LOCATIONS_RIGHT = parse_lists_side_by_side(INPUT)
    distance_between_lists(LOCATIONS_LEFT, LOCATIONS_RIGHT)
    return INPUT, LOCATIONS_LEFT, LOCATIONS_RIGHT, path_input


@app.cell
def _(Iterable, Location, Mapping, defaultdict, it):
    def count_frequencies(locations: Iterable[Location]) -> Mapping[Location, int]:
        return defaultdict(
            lambda: 0,
            {
                location: len(list(group))
                for location, group in it.groupby(sorted(locations))
            },
        )
    return (count_frequencies,)


@app.cell
def _(count_frequencies, locations_left, locations_right):
    for i, (_locations, _expected) in enumerate(
        [
            (
                locations_left,
                {1: 1, 2: 1, 3: 3, 4: 1},
            ),
            (
                locations_right,
                {
                    3: 3,
                    4: 1,
                    5: 1,
                    9: 1,
                },
            ),
        ]
    ):
        _actual = count_frequencies(_locations)
        assert _expected == _actual, str(i)
    return (i,)


@app.cell
def _(count_frequencies, locations_left):
    _expected = 0
    _actual = count_frequencies(locations_left)[0]
    assert _expected == _actual, _actual
    return


@app.cell
def _(List, Location, count_frequencies):
    def score_similarity(left: list[Location], right: List[Location]) -> int:
        freq_left, freq_right = [
            count_frequencies(locations) for locations in [left, right]
        ]
        return sum(
            location * freq_left[location] * freq_right[location]
            for location in freq_left.keys() | freq_right.keys()
        )
    return (score_similarity,)


@app.cell
def _(locations_left, locations_right, score_similarity):
    _expected = 31
    _actual = score_similarity(locations_left, locations_right)
    assert _expected == _actual, str(_actual)
    return


@app.cell
def _(LOCATIONS_LEFT, LOCATIONS_RIGHT, score_similarity):
    score_similarity(LOCATIONS_LEFT, LOCATIONS_RIGHT)
    return


if __name__ == "__main__":
    app.run()
