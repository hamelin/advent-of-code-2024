import marimo

__generated_with = "0.10.8"
app = marimo.App(
    width="full",
    layout_file="layouts/Day 1 - Historian Hysteria.slides.json",
    css_file="custom.css",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    from pathlib import Path
    mo.md(
        f"""
        # Day 1 &mdash; [Historian Hysteria](https://adventofcode.com/2024/day/1)

        {mo.accordion({"Input": (INPUT := mo.ui.code_editor(value=Path("inputs/01.txt").read_text(encoding="utf-8"), language=""))})}

        We begin with with a list comparison problem.
        In essence, if the lists were identical, they would contain the same location IDs.
        """
    )
    return INPUT, Path


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        ## Part I

        The problem's solution is almost spelled out:
        compare how far apart location IDs are, going from smallest to largest.
        Thus, sort the two columns respectively, and compute the differences.
        For that, we want to first read the two lists.
        Since text shows up line by line, the two lists are intermingled.
        We should thus first learn how to disentangle them. Here's an example.
        """
    )
    return


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Each _location ID_ is an integer.
        An abstraction will help track what it is we are doing.
        I dislike using words like _ID_ and _identifier_ when I talk about things,
        let's just call location IDs `Location`s.
        """
    )
    return


@app.cell
def _():
    Location = int
    return (Location,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        So parsing our two-column list should yield two `list[Location]`'s.
        In Python 3, from a list of tuples, getting a tuple of lists requires but a clever application of `zip`.
        """
    )
    return


@app.cell
def _(Location):
    from textwrap import dedent


    def parse_lists_side_by_side(text: str) -> tuple[list[Location], list[Location]]:
        pairs_locations = (
            (Location(left), Location(right))
            for left, right in [
                line.strip().split()
                for line in dedent(text).strip().split("\n")
                if line.strip()
            ]
        )
        return tuple(list(t) for t in zip(*pairs_locations))
    return dedent, parse_lists_side_by_side


@app.cell
def _(parse_lists_side_by_side, text):
    lists_side_by_side = parse_lists_side_by_side(text)
    _expected = ([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3])
    _actual = lists_side_by_side
    assert _expected == _actual
    return (lists_side_by_side,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now we parse these two-column texts, let's grab each list on its own.""")
    return


@app.cell
def _(lists_side_by_side):
    locations_left, locations_right = lists_side_by_side
    return locations_left, locations_right


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        As discussed above, measuring the distance between both lists is merely a matter of crunching the difference between locations,
        in increasing order.
        """
    )
    return


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We're ready to handle the problem input.""")
    return


@app.cell
def _(INPUT, distance_between_lists, mo, parse_lists_side_by_side):
    LOCATIONS_LEFT, LOCATIONS_RIGHT = parse_lists_side_by_side(INPUT.value)
    DIST = distance_between_lists(LOCATIONS_LEFT, LOCATIONS_RIGHT)
    mo.center(mo.md(f"**{DIST}**"))
    return DIST, LOCATIONS_LEFT, LOCATIONS_RIGHT


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part II

        We are asked to compute a different similarity measure over matching locations,
        one that would ignore locations present in just one of the two lists.
        So what we want to calculate, here, is a number that depends on an [inner join](https://en.wikipedia.org/wiki/Join_(SQL)) of the two lists.
        In particular, as one understands the example given,
        for each matching ID,
        the _similarity score_ involves computing the product of the frequencies of the locations in each list,
        respectively. Let's focus on this first.

        An easy way to compute the frequency distribution of a list of integers in Python is to use `itertools.groupby`.
        It is slightly tricky to understand, please do look up its [documentation](https://docs.python.org/3/library/itertools.html#itertools.groupby).
        """
    )
    return


@app.cell
def _(Iterable, Location):
    from collections import defaultdict
    from collections.abc import Mapping
    import itertools as it


    def count_frequencies(locations: Iterable[Location]) -> Mapping[Location, int]:
        return defaultdict(
            lambda: 0,
            {
                location: sum(1 for _ in group)
                for location, group in it.groupby(sorted(locations))
            },
        )
    return Mapping, count_frequencies, defaultdict, it


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Test using the example lists given above.""")
    return


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We also ensure these location-to-frequency dictionaries can handle locations not present in the list.
        For these, the frequency is 0.
        Python's `collections.defaultdict` makes easy work of handling default value reporting on unknown keys.
        """
    )
    return


@app.cell
def _(count_frequencies, locations_left):
    _expected = 0
    _actual = count_frequencies(locations_left)[0]
    assert _expected == _actual, _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We have all the ingredients in place to crunch these similarity scores.""")
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Finish this on the problem input.""")
    return


@app.cell
def _(LOCATIONS_LEFT, LOCATIONS_RIGHT, mo, score_similarity):
    SCORE = score_similarity(LOCATIONS_LEFT, LOCATIONS_RIGHT)
    mo.center(mo.md(f"**{SCORE}**"))
    return (SCORE,)


if __name__ == "__main__":
    app.run()
