import numpy as np
import pytest

from . import (
    as_int_image,
    convolve,
    convolve_step,
    count_xmas_hits,
    eq,
    extend_mask,
    KERNELS_XMAS,
    reformat_indented_string,
)


def test_reformat_indented_string():
    assert "heyhey\nhoho" == reformat_indented_string(
        """\
        heyhey
        hoho
        """
    )


X, M, A, S, _, pt = [ord(c) for c in "XMAS_."]


def test_kernel():
    assert np.all(
        np.array([
            [X, _, _, _],
            [_, M, _, _],
            [_, _, A, _],
            [_, _, _, S],
        ]) == as_int_image("""\
            X___
            _M__
            __A_
            ___S
        """)
    )


@pytest.mark.parametrize(
    "expected,kernel",
    [
        (shape, KERNELS_XMAS[direction])
        for shape, direction in [
            ((1, 4), 0),
            ((4, 4), 45),
            ((4, 1), 90),
            ((4, 4), 135),
            ((1, 4), 180),
            ((4, 4), 225),
            ((4, 1), 270),
            ((4, 4), 315),
        ]
    ]
)
def test_shape_kernels_xmas(expected, kernel):
    assert expected == kernel.shape


@pytest.mark.parametrize(
    "expected,canvas,mask_extended",
    [
        (
            np.array([[1, 1, 1, 1, 0]]),
            np.array([[X, M, A, S, pt]]),
            np.array([[X, M, A, S, _]]),
        ),
        (
            np.array([[0, 0, 0, 0, 0]]),
            np.array([[pt, X, M, A, S]]),
            np.array([[X, M, A, S, _]])
        ),
        (
            np.array([[1], [1], [1], [1], [0]]),
            np.array([[X], [M], [A], [S], [pt]]),
            np.array([[X], [M], [A], [S], [_]]),
        ),
        (
            np.array([[0], [0], [0], [0], [0]]),
            np.array([[pt], [X], [M], [A], [S]]),
            np.array([[X], [M], [A], [S], [_]])
        ),
        (
            np.array([
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ]),
            np.array([
                [pt, pt, pt, pt, pt],
                [pt, X, pt, pt, pt],
                [pt, pt, M, pt, pt],
                [pt, pt, pt, A, pt],
                [pt, pt, pt, pt, S],
            ]),
            np.array([
                [_, _, _, _, _],
                [_, X, _, _, _],
                [_, _, M, _, _],
                [_, _, _, A, _],
                [_, _, _, _, S],
            ]),
        ),
        (
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]),
            np.array([
                [X, pt, pt, pt, pt],
                [pt, M, pt, pt, pt],
                [pt, pt, A, pt, pt],
                [pt, pt, pt, S, pt],
                [pt, pt, pt, pt, pt],
            ]),
            np.array([
                [_, _, _, _, _],
                [_, X, _, _, _],
                [_, _, M, _, _],
                [_, _, _, A, _],
                [_, _, _, _, S],
            ]),
        )
    ]
)
def test_eq(expected, canvas, mask_extended):
    assert np.all(expected == eq(canvas, mask_extended))


@pytest.mark.parametrize(
    "expected,canvas,mask_extended",
    [
        (
            1,
            np.array([[X, M, A, S, pt]]),
            np.array([[X, M, A, S, _]]),
        ),
        (
            0,
            np.array([[pt, X, M, A, S]]),
            np.array([[X, M, A, S, _]])
        ),
        (
            1,
            np.array([[X], [M], [A], [S], [pt]]),
            np.array([[X], [M], [A], [S], [_]]),
        ),
        (
            0,
            np.array([[pt], [X], [M], [A], [S]]),
            np.array([[X], [M], [A], [S], [_]])
        ),
        (
            1,
            np.array([
                [pt, pt, pt, pt, pt],
                [pt, X, pt, pt, pt],
                [pt, pt, M, pt, pt],
                [pt, pt, pt, A, pt],
                [pt, pt, pt, pt, S],
            ]),
            np.array([
                [_, _, _, _, _],
                [_, X, _, _, _],
                [_, _, M, _, _],
                [_, _, _, A, _],
                [_, _, _, _, S],
            ]),
        ),
        (
            0,
            np.array([
                [X, pt, pt, pt, pt],
                [pt, M, pt, pt, pt],
                [pt, pt, A, pt, pt],
                [pt, pt, pt, S, pt],
                [pt, pt, pt, pt, pt],
            ]),
            np.array([
                [_, _, _, _, _],
                [_, X, _, _, _],
                [_, _, M, _, _],
                [_, _, _, A, _],
                [_, _, _, _, S],
            ]),
        )
    ]
)
def test_convolve_step(expected, canvas, mask_extended):
    assert expected == convolve_step(canvas, mask_extended)


def test_extend_mask():
    assert np.all(
        np.array([
            [_, _, _, _, _, _, _],
            [_, X, M, A, S, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
            [_, _, _, _, _, _, _],
        ]) == extend_mask(np.array([[X, M, A, S]]), (1, 3), (1, 2))
    )

    
def test_convolve_step_partial_means_0():
    assert 0 == convolve_step(
        np.array(
            [
                [M, M, A, X, S],
                [S, M, X, A, S]
            ],
        ),
        extend_mask(KERNELS_XMAS[0], (0, 1), (0, 1))
    )


@pytest.fixture
def xmasses():
    return as_int_image("""\
        ..S..
        ..A..
        SSM..
        .AXXS
        .XMAS
        SAMXX
        SX.AM
        .M..S
        .A..S
        .S...
    """)


@pytest.mark.parametrize(
    "expected,direction",
    [
        (
            np.array([
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 1],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ]),
            0,
        ),
        (
            np.array([
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 1],
                [0, 0],
                [0, 0],
                [0, 0],
            ]),
            45,
        ),
        (
            np.array([
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]),
            90,
        ),
        (
            np.array([
                [0, 0],
                [0, 0],
                [1, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ]),
            135,
        ),
        (
            np.array([
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [1, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ]),
            180,
        ),
        (
            np.array([
                [0, 0],
                [0, 0],
                [0, 0],
                [1, 0],
                [0, 0],
                [0, 0],
                [0, 0],
            ]),
            225,
        ),
        (
            np.array([
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
            ]),
            270,
        ),
        (
            np.array([
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 0],
                [0, 1],
                [0, 0],
                [0, 0],
            ]),
            315,
        ),
    ],
)
def test_convolve(expected, direction, xmasses):
    assert np.all(expected == convolve(xmasses, KERNELS_XMAS[direction]))


def test_count_xmas_hits(xmasses):
    assert 8 == count_xmas_hits(xmasses)
