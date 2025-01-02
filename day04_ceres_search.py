import marimo

__generated_with = "0.10.8"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from util import input_editor
    return input_editor, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Day 4 - [Ceres Search](https://adventofcode_com/2024/day/4)

        This problem is about searching for patterns in a two-dimensional categorical function.
        """
    )
    return


@app.cell(hide_code=True)
def _(input_editor, mo):
    INPUT = input_editor(4)
    mo.accordion({"Input": INPUT})
    return (INPUT,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part I

        The first pattern to look for is the string `XMAS`, but written in any direction.
        A different way to put it is that we are looking for all instances of any of these 2D patterns:

        ```
                    X  S  X     S        S     X
        XMAS  SAMX  M  A   M     M      A     M
                    A  M    A     A    M     A
                    S  X     S     X  X     S
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""

        I want to approach this problem through a weird angle:
        image correlation.
        To cut the theory short, we can compare two images by computing their [convolution product](https://en_wikipedia_org/wiki/Kernel_(image_processing)).
        However, convolutions are typically defined over real functions of vectors.
        So let's give this a categorical twist.

        Given the categorical finite set $L = \{\mathtt{A}, \mathtt{M}, \mathtt{S}, \mathtt{X}, \mathtt{\cdot}\}$, we model discrete images $f$ and $g$ as functions

        $$
            f: \{0, 1, \ldots m_f - 1\} \times \{0, 1, \ldots n_f - 1\} \rightarrow L \\
            g: \{0, 1, \ldots m_g - 1\} \times \{0, 1, \ldots n_g - 1\} \rightarrow L \\
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Let's now define a _product operation_ $\cdot\bullet\cdot: L \times L \rightarrow \mathbb{N}$ such that for $a, b \in L$,

        $$
        a \bullet b = \left\{\begin{array}{ll}
        1 & \text{if a = b} \\
        0 & \text{otherwise}
        \end{array}\right.
        $$

        We will then have the correlation product $\left<\cdot,\cdot\right>$ of two categorical images as the integral of $\bullet$ products across shifts of a function over the other.
        Let's assume that image $g$ is smaller than image $f$ in both dimensions,
        so $m_g \leq m_f$ and $n_g \leq n_f$.
        The correlation product would thus be written as

        $$
        \begin{array}{rrcl}
        \left<f, g\right>:
            & \{0, 1, \ldots m_f - m_g\} \times \{0, 1, \ldots n_f - n_g\} & \rightarrow & \mathbb{N} \\
            & (p, q) & \mapsto & \displaystyle
                                 \sum_{i = 0}^{m_g} \sum_{j = 0}^{n_g} f(i + p, j + q) \bullet g(i, j)
        \end{array}
        $$
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        This means that image $c(p,q) = \left<f,g\right>$ carries a signal that is maximal when
        a certain shift $(p, q)$ of $f$ with respect to $g$ aligns a XMAS pattern with its occurrence.
        The values that $f$ takes will be restricted to $\{\mathtt{A}, \mathtt{M}, \mathtt{S}, \mathtt{X}\} \subset L$;
        the kernel $g$ will take value $\cdot \in L$ for each non-letter spot,
        yielding a maximum of 4 values matching when the shift hits on an occurrence
        (letters X, M, A, and S).
        So to count all XMAS occurrences, we apply these 8 kernels to the input,
        filter for the results for values of 4,
        and count their occurrences.
        It's almost easy!
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We are given two examples in the problem descriptor.
        The first and smaller one is provided without any confounding letter,
        so it has many dot characters in it.
        To avoid the kernel matching spuriously on these,
        I swap them with underscores,
        keeping the clarity of the pattern occurrences.
        """
    )
    return


@app.cell
def _():
    texts = {
        "5x6": """
            __X___
            _SAMX_
            _A__A_
            XMAS_S
            _X____
        """,
        "10x10": """
            MMMSXXMASM
            MSAMXMSMSA
            AMXSXMAAMM
            MSAMASMSMX
            XMASAMXAMM
            XXAMMXXAMA
            SMSMSASXSS
            SAXAMASAAA
            MAMMMXMMMM
            MXMXAXMASX
        """
    }
    return (texts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Let's put together some abstractions to clarify the objects that wrangle this pattern detection system.""")
    return


@app.cell
def _():
    from dataclasses import dataclass
    from typing import Any, Generic, Protocol, TypeVar
    return Any, Generic, Protocol, TypeVar, dataclass


@app.cell
def _(TypeVar):
    T = TypeVar("T")
    return (T,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        _Categoricals_ are objects with their own identity.
        They are equal to themselves, and different from any other.
        They don't admit any notion of order amongst themselves.
        """
    )
    return


@app.cell
def _(Any, Protocol, T):
    class Categorical(Protocol[T]):
        def __eq__(self, other: Any) -> bool: ...
    return (Categorical,)


@app.cell
def _(Categorical, T):
    class Row(list[Categorical[T]]):
        pass
    return (Row,)


@app.cell
def _(Generic, Row, T, dataclass):
    @dataclass
    class Image(Generic[T]):
        rows: list[Row[T]]

        @property
        def shape(self) -> tuple[int, int]:
            return len(self.rows), len(self.rows[0])

        def __getitem__(self, index) -> Row[T]:
            return self.rows[index]
    return (Image,)


@app.cell
def _():
    from textwrap import dedent
    return (dedent,)


@app.cell
def _(Image, dedent):
    def read_image_letters(text: str) -> Image[str]:
        image = Image(
            rows=[list(line.strip()) for line in dedent(text).strip().split("\n")]
        )
        assert all(
            len(image.rows[i]) == len(image.rows[0]) for i in range(1, len(image.rows))
        )
        return image
    return (read_image_letters,)


@app.cell
def _(read_image_letters, texts):
    examples = {
        name: read_image_letters(text)
        for name, text in texts.items()
    }
    return (examples,)


@app.cell
def _(Image, examples):
    _expected = {
        "5x6": Image(
            rows=[
                ["_", "_", "X", "_", "_", "_"],
                ["_", "S", "A", "M", "X", "_"],
                ["_", "A", "_", "_", "A", "_"],
                ["X", "M", "A", "S", "_", "S"],
                ["_", "X", "_", "_", "_", "_"],
            ]
        ),
        "10x10": Image(
            rows=[
                ["M", "M", "M", "S", "X", "X", "M", "A", "S", "M"],
                ["M", "S", "A", "M", "X", "M", "S", "M", "S", "A"],
                ["A", "M", "X", "S", "X", "M", "A", "A", "M", "M"],
                ["M", "S", "A", "M", "A", "S", "M", "S", "M", "X"],
                ["X", "M", "A", "S", "A", "M", "X", "A", "M", "M"],
                ["X", "X", "A", "M", "M", "X", "X", "A", "M", "A"],
                ["S", "M", "S", "M", "S", "A", "S", "X", "S", "S"],
                ["S", "A", "X", "A", "M", "A", "S", "A", "A", "A"],
                ["M", "A", "M", "M", "M", "X", "M", "M", "M", "M"],
                ["M", "X", "M", "X", "A", "X", "M", "A", "S", "X"],
            ]
        ),
    }
    _actual = examples
    assert _expected == _actual
    return


@app.cell
def _(examples):
    _expected = {"5x6": (5, 6), "10x10": (10, 10)}
    _actual = {name: image.shape for name, image in examples.items()}
    assert _expected == _actual, _actual
    return


@app.cell
def _(Image, T):
    def correlate_images(left: Image[T], right: Image[T]) -> Image[int]:
        assert left.shape >= right.shape
        shape_result = tuple(l - r + 1 for l, r in zip(left.shape, right.shape))
        return Image(
            rows=[
                [
                    sum(
                        1
                        for i in range(right.shape[0])
                        for j in range(right.shape[1])
                        if left[i + p][j + q] == right[i][j]
                    )
                    for q in range(shape_result[1])
                ]
                for p in range(shape_result[0])
            ]
        )
    return (correlate_images,)


@app.cell
def _(read_image_letters):
    images_xmas = {
        ">>": read_image_letters("XMAS"),
        "<<": read_image_letters("SAMX"),
        "vv": read_image_letters(
            """\
            X
            M
            A
            S
            """
        ),
        "^^": read_image_letters(
            """\
            S
            A
            M
            X
            """
        ),
        "^>": read_image_letters(
            """\
            ...S
            ..A.
            .M..
            X...
            """
        ),
        "<^": read_image_letters(
            """\
            S...
            .A..
            ..M.
            ...X
            """
        ),
        "v>": read_image_letters(
            """\
            X...
            .M..
            ..A.
            ...S
            """
        ),
        "<v": read_image_letters(
            """\
            ...X
            ..M.
            .A..
            S...
            """
        )
    }
    return (images_xmas,)


@app.cell
def _(Image, correlate_images, examples, images_xmas):
    _expected = {
        ">>": Image([
            [0, 0, 1],
            [1, 0, 1],
            [0, 0, 1],
            [4, 0, 1],
            [0, 1, 0]
        ]),
        "<<": Image([
            [0, 0, 0],
            [0, 4, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]),
        "vv": Image([
            [0, 1, 1, 2, 1, 1],
            [0, 0, 1, 0, 1, 0]
        ]),
        "^^": Image([
            [1, 0, 1, 0, 0, 0],
            [0, 4, 0, 0, 1, 0]
        ]),
        "^>": Image([
            [2, 0, 0],
            [1, 1, 1]
        ]),
        "<^": Image([
            [0, 1, 0],
            [1, 1, 0]
        ]),
        "v>": Image([
            [1, 0, 4],
            [1, 0, 0]
        ]),
        "<v": Image([
            [1, 1, 0],
            [0, 2, 0]
        ])
    }
    _actual = {
        name: correlate_images(examples["5x6"], kernel)
        for name, kernel in images_xmas.items()
    }
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Now we have this correlation, we must filter its results,
        so as to count how often we hit the maximum for each kernel.
        """
    )
    return


@app.cell
def _(Image):
    def threshold_image(image: Image[int], threshold: int) -> Image[int]:
        return Image(rows=[[x if x >= threshold else 0 for x in row] for row in image.rows])
    return (threshold_image,)


@app.cell
def _(Image, correlate_images, examples, images_xmas, threshold_image):
    _expected = {
        ">>": Image([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [4, 0, 0],
            [0, 0, 0]
        ]),
        "<<": Image([
            [0, 0, 0],
            [0, 4, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]),
        "vv": Image([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]),
        "^^": Image([
            [0, 0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0]
        ]),
        "^>": Image([
            [0, 0, 0],
            [0, 0, 0]
        ]),
        "<^": Image([
            [0, 0, 0],
            [0, 0, 0]
        ]),
        "v>": Image([
            [0, 0, 4],
            [0, 0, 0]
        ]),
        "<v": Image([
            [0, 0, 0],
            [0, 0, 0]
        ])
    }
    _actual = {
        name: threshold_image(correlate_images(examples["5x6"], kernel), 4)
        for name, kernel in images_xmas.items()
    }
    assert _expected == _actual, _actual
    return


@app.cell
def _(Image):
    def count_nonzeros(image: Image[int]) -> int:
        return sum(
            sum(1 for x in row if x)
            for row in image.rows
        )
    return (count_nonzeros,)


@app.cell
def _(
    correlate_images,
    count_nonzeros,
    examples,
    images_xmas,
    threshold_image,
):
    _expected = {
        ">>": 1,
        "<<": 1,
        "vv": 0,
        "^^": 1,
        "^>": 0,
        "<^": 0,
        "v>": 1,
        "<v": 0
    }
    _actual = {
        name: count_nonzeros(threshold_image(correlate_images(examples["5x6"], kernel), 4))
        for name, kernel in images_xmas.items()
    }
    assert _expected == _actual, _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now wrap this so that counting the occurrences of all these XMASes is not such a mouthful.""")
    return


@app.cell
def _(Generic, Image, T, dataclass):
    @dataclass
    class Kernel(Generic[T]):
        image: Image[T]
        threshold: int
    return (Kernel,)


@app.cell
def _(Kernel, images_xmas):
    kernels_xmas = {
        name: Kernel(image=image, threshold=4)
        for name, image in images_xmas.items()
    }
    return (kernels_xmas,)


@app.cell
def _(
    Image,
    Iterator,
    Kernel,
    T,
    correlate_images,
    count_nonzeros,
    mo,
    threshold_image,
):
    def count_xmasses(image: Image[T], kernels: Iterator[Kernel[T]]) -> int:
        return sum(
            count_nonzeros(
                threshold_image(correlate_images(image, kernel.image), kernel.threshold)
            )
            for kernel in mo.status.progress_bar(kernels)
        )
    return (count_xmasses,)


@app.cell
def _(count_xmasses, examples, kernels_xmas):
    _expected = {
        "5x6": 4,
        "10x10": 18
    }
    _actual = {
        name: count_xmasses(image, kernels_xmas.values())
        for name, image in examples.items()
    }
    assert _expected == _actual
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Good, so how does this approach fare against the gigantic input we have?""")
    return


@app.cell
def _(INPUT, count_xmasses, kernels_xmas, mo, read_image_letters):
    IMAGE = read_image_letters(INPUT.value)
    mo.md(f"Number of occurrences of the XMAS patterns: **{count_xmasses(IMAGE, kernels_xmas.values())}**")
    return (IMAGE,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Part II

        Now this looks suspiciously arranged with the effects department,
        but when I first ran through this problem,
        I _really_ came up with this weird approach derived from image processing methods.
        And so when this second part was revealed,
        I found myself laughing gleefully: 
        my current solution was _perfectly_ adapted to this second challenge!

        So as it were, we are simply to look for a different set of patterns,
        which can be respectively encoded as images.
        Thesae patterns are 3x3 images of the word `MAS` expressed on the diagonals,
        in any direction.
        All these patterns have thus letter `A` in the center.
        Furthermore, since the word `MAS` must appear along each diagonal,
        the two `M`'s and `S`'s must show up on the same column or row of the image
        (otherwise we have, say, `M`s on both end of a diagonal,
        and thus we are not spelling `MAS` anymore).
        Let's thus enumerate these.
        """
    )
    return


@app.cell
def _(read_image_letters):
    images_X_MAS = {
        name: read_image_letters(text)
        for name, text in {
            "|..": """\
                M.S
                .A.
                M.S
            """,
            "^^^": """\
                M.M
                .A.
                S.S
            """,
            "..|": """\
                S.M
                .A.
                S.M
            """,
            "vvv": """\
                S.S
                .A.
                M.M
            """,
        }.items()
    }
    return (images_X_MAS,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        These kernels all count 5 letters to match,
        so we must threshold their detections to that value.
        """
    )
    return


@app.cell
def _(Kernel, images_X_MAS):
    kernels_X_MAS = {
        name: Kernel(image=image, threshold=5)
        for name, image in images_X_MAS.items()
    }
    return (kernels_X_MAS,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We are given a new example to test this.
        Once again, we express the spaces irrelevant to the detection as underscores,
        in order to avoid spurious matching on dots.
        """
    )
    return


@app.cell
def _(read_image_letters):
    example_X_MAS = read_image_letters(
        """
        _M_S______
        __A__MSMS_
        _M_S_MAA__
        __A_ASMSM_
        _M_S_M____
        __________
        S_S_S_S_S_
        _A_A_A_A__
        M_M_M_M_M_
        __________
        """
    )
    return (example_X_MAS,)


@app.cell
def _(count_xmasses, example_X_MAS, kernels_X_MAS):
    _expected = 9
    _actual = count_xmasses(example_X_MAS, kernels_X_MAS.values())
    assert _expected == _actual
    return


@app.cell
def _(IMAGE, count_xmasses, kernels_X_MAS, mo):
    mo.md(f"Number of X-MAS occurrences: **{count_xmasses(IMAGE, kernels_X_MAS.values())}**")
    return


if __name__ == "__main__":
    app.run()
