import marimo

__generated_with = "0.10.8"
app = marimo.App(width="full", css_file=".git/info/local.css")


@app.cell
def _():
    import marimo as mo
    from util import input_editor
    return input_editor, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Day 3 &mdash; [Mull It Over](https://adventofcode.com/2024/day/3)

        This problem is about parsing well-formed multiplication instructions out of a jumble of bytes, and crunching their results.
        """
    )
    return


@app.cell(hide_code=True)
def _(input_editor, mo):
    # We set the input editor in its own cell, because it is misbehaving when embedded in the notebook heading Markdown text.
    # Perhaps this is because the input string stuck in the editor is a very long unbroken mess?
    # CodeMirror is likely expecting a more regular line-based structure. Anyway, moving on.
    INPUT = input_editor(3)
    mo.accordion({"Input": INPUT})
    return (INPUT,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part I

        The problem statement provides the following example of the string that must be scanned for multiplication instructions:
        """
    )
    return


@app.cell
def _():
    example = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    example
    return (example,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        A well-formed multiplication takes the form `mul(X,Y)`, where `X` and `Y` are positive integers.
        This is a job easily done using regular expressions.
        For the sake of testing, let's articulate the multiplications we find into objects.
        """
    )
    return


@app.cell
def _():
    from dataclasses import dataclass
    return (dataclass,)


@app.cell
def _(dataclass):
    @dataclass
    class Multiplication:
        left: int
        right: int

        def compute(self) -> int:
            return self.left * self.right
    return (Multiplication,)


@app.cell
def _():
    from collections.abc import Iterator
    import re
    return Iterator, re


@app.cell
def _(re):
    RX_MULTIPLICATION = re.compile(r"mul\((?P<left>\d+),(?P<right>\d+)\)")
    return (RX_MULTIPLICATION,)


@app.cell
def _(Iterator, Multiplication, RX_MULTIPLICATION):
    def extract_multiplications(text: str) -> Iterator[Multiplication]:
        for match in RX_MULTIPLICATION.finditer(text):
            yield Multiplication(**{s: int(match.group(s)) for s in ["left", "right"]})
    return (extract_multiplications,)


@app.cell
def _(Multiplication, example, extract_multiplications):
    _expected = [
        Multiplication(2, 4),
        Multiplication(5, 5),
        Multiplication(11, 8),
        Multiplication(8, 5),
    ]
    _actual = list(extract_multiplications(example))
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Further with the example, let's ensure these multiplications sum up to expectations.""")
    return


@app.cell
def _(Iterator, Multiplication):
    def sum_multiplications(multiplications: Iterator[Multiplication]) -> int:
        return sum(mul.compute() for mul in multiplications)
    return (sum_multiplications,)


@app.cell
def _(example, extract_multiplications, sum_multiplications):
    _expected = 161
    _actual = sum_multiplications(extract_multiplications(example))
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""With the provided problem input:""")
    return


@app.cell
def _(INPUT, extract_multiplications, mo, sum_multiplications):
    mo.md(
        f"""
        Sum of the multiplications: **{sum_multiplications(extract_multiplications(INPUT.value))}**
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part II

        We now add into the mix two new instructions: `do()` and `don't()`.
        When running the latter, `mul(X,Y)` instructions become _disabled_, and thus ignored from processing.
        When running the former, multiplications become enabled again, and processing resumes as has happened so far.
        It is best to handle this with a new parser.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We are given a new example:""")
    return


@app.cell
def _():
    example_do_dont = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    example_do_dont
    return (example_do_dont,)


@app.cell
def _(re):
    RX_INSTRUCTION = re.compile(r"(?P<mul>mul)\((?P<left>\d+),(?P<right>\d+)\)|(?P<dodont>do|don't)\(\)")
    return (RX_INSTRUCTION,)


@app.cell
def _(Iterator, Multiplication, RX_INSTRUCTION):
    def parse_memory(text: str) -> Iterator[Multiplication]:
        multiplications_enabled = True
        for match in RX_INSTRUCTION.finditer(text):
            if match.groupdict()["dodont"]:
                multiplications_enabled = (match.group("dodont") == "do")
            elif match.groupdict()["mul"]:
                if multiplications_enabled:
                    yield Multiplication(**{s: int(match.group(s)) for s in ["left", "right"]})
            else:
                raise ValueError(f"Don't know how to handle match {match}")
    return (parse_memory,)


@app.cell
def _(Multiplication, example_do_dont, parse_memory):
    _expected = [
        Multiplication(2, 4),
        Multiplication(8, 5),
    ]
    _actual = list(parse_memory(example_do_dont))
    assert _expected == _actual, _actual
    return


@app.cell
def _(example_do_dont, parse_memory, sum_multiplications):
    _expected = 48
    _actual = sum_multiplications(parse_memory(example_do_dont))
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Apply this to the input:""")
    return


@app.cell
def _(INPUT, mo, parse_memory, sum_multiplications):
    mo.md(f"Sum of multiplications with do()/don't() handling: **{sum_multiplications(parse_memory(INPUT.value))}**")
    return


if __name__ == "__main__":
    app.run()
