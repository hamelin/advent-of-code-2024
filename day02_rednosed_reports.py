import marimo

__generated_with = "0.10.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from util import input_editor
    return input_editor, mo


@app.cell
def _(input_editor, mo):
    editor_input = input_editor(2)
    mo.md(
        f"""
        # Day 2 &mdash; [Red-nosed reports](https://adventofcode.com/2024/day/2)

        {mo.accordion({"Input": editor_input})}

        This problem is a rather simple time series analysis instance.
        """
    )
    return (editor_input,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Part I

        Each row of input is a _report_, each consisting in a sequence of _levels_ (integer values).
        A report is safe if it is strictly monotonically increasing or decreasing,
        and if the amount of variation at each step is either 1, 2 or 3.
        Let's start with reading in such reports,
        using the following example.
        """
    )
    return


@app.cell
def _():
    text = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """
    return (text,)


@app.cell
def _():
    from dataclasses import dataclass
    return (dataclass,)


@app.cell
def _(dataclass):
    @dataclass
    class Report:
        levels: list[int]
    return (Report,)


@app.cell
def _():
    from collections.abc import Iterator
    return (Iterator,)


@app.cell
def _(Iterator, Report):
    def parse_reports(text: str) -> Iterator[Report]:
        for line_ in text.split("\n"):
            line = line_.strip()
            if line:
                yield Report(
                    levels=[int(n) for n in line.split()]
                )
    return (parse_reports,)


@app.cell
def _(parse_reports, text):
    reports = list(parse_reports(text))
    reports
    return (reports,)


@app.cell
def _(Report, reports):
    _expected = [
        Report(levels=[7, 6, 4, 2, 1]),
        Report(levels=[1, 2, 7, 8, 9]),
        Report(levels=[9, 7, 6, 2, 1]),
        Report(levels=[1, 3, 2, 4, 5]),
        Report(levels=[8, 6, 4, 4, 1]),
        Report(levels=[1, 3, 6, 7, 9]),
    ]
    _actual = reports
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Safety of a report can be assessed by looking at the levels of a report in pairs.""")
    return


@app.cell
def _():
    import itertools as it
    from util import add_method
    return add_method, it


@app.cell
def _(Report, add_method, it):
    @add_method(Report)
    def is_safe(self) -> bool:
        variations = [pair[1] - pair[0] for pair in it.pairwise(self.levels)]
        return all(v >= 1 and v <= 3 for v in variations) or all(
            v >= -3 and v <= -1 for v in variations
        )
    return (is_safe,)


@app.cell
def _(reports):
    for _i, _expected in enumerate([True, False, False, False, False, True]):
        _actual = reports[_i].is_safe()
        assert _expected == _actual, reports[_i]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We now have the means to crunch the problem input.""")
    return


@app.cell
def _(editor_input, mo, parse_reports):
    REPORTS = list(parse_reports(editor_input.value))
    NUM_REPORTS_SAFE = sum(1 for report in REPORTS if report.is_safe())
    mo.center(mo.md(f"**Number of safe reports: {NUM_REPORTS_SAFE}**"))
    return NUM_REPORTS_SAFE, REPORTS


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part II

        Any level of a report can be now removed to make the report safe.
        From my perspective, this can bring a few problems.
        Report safety entails ensuring strict monotonicity of the level sequence.
        If the report carries less than 2 levels,
        then our current code for evaluating monotonicity must be revisited.
        The example we were given only has reports with 5 levels,
        but let's not trust this as an assumption we can rest on.
        Check our full input.
        """
    )
    return


@app.cell
def _(Report, add_method):
    # Add this to avoid breaking the abstraction barrier.
    @add_method(Report)
    def __len__(self) -> int:
        return len(self.levels)
    return (__len__,)


@app.cell
def _(editor_input, mo, parse_reports):
    mo.md(
        f"""
        Minimum number of levels per report: **{min(len(report) for report in parse_reports(editor_input.value))}**
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Ok, we're fine.
        Then, assessing the safety under the problem dampener is really the matter of trying to remove any of the levels of a given report,
        and checking the safety of this shortened sequence.

        A great way to do this is to use the [`itertools.combinations`](https://docs.python.org/3/library/itertools.html#itertools.combinations) iterator.
        Combinations of one-less levels of the original report are the cases that may yield a safe report.
        """
    )
    return


@app.cell
def _(Report, add_method, it):
    @add_method(Report)
    def is_safe_under_problem_dampener(self) -> bool:
        for subseq in it.combinations(self.levels, len(self) - 1):
            if type(self)(levels=subseq).is_safe():
                return True
        return False
    return (is_safe_under_problem_dampener,)


@app.cell
def _(reports):
    for _i, _expected in enumerate([True, False, False, True, True, True]):
        _actual = reports[_i].is_safe_under_problem_dampener()
        assert _expected == _actual, reports[_i]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""And finally, handling the problem input.""")
    return


@app.cell
def _(REPORTS, mo):
    mo.center(
        mo.md(
            f"Number of safe reports with consideration to the problem dampener: **{sum(1 for report in REPORTS if report.is_safe_under_problem_dampener())}**"
        )
    )
    return


if __name__ == "__main__":
    app.run()
