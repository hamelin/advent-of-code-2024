from collections.abc import Iterable
import numpy as np
from textwrap import dedent


def reformat_indented_string(s: str) -> str:
    return dedent(s).rstrip()


def as_int_image(desc: str) -> np.ndarray:
    return np.array([
        [ord(c) for c in line]
        for line in reformat_indented_string(desc).split("\n")
    ])


CHAR_MASK_EMPTY = ord("_")
KERNELS_XMAS = {
    direction: as_int_image(desc)
    for direction, desc in [
        (
            0,
            "XMAS",
        ),
        (
            45,
            """\
            ___S
            __A_
            _M__
            X___
            """,
        ),
        (
            90,
            """\
            S
            A
            M
            X
            """,
        ),
        (
            135,
            """\
            S___
            _A__
            __M_
            ___X
            """,
        ),
        (
            180,
            """\
            SAMX
            """,
        ),
        (
            225,
            """\
            ___X
            __M_
            _A__
            S___
            """,
        ),
        (
            270,
            """\
            X
            M
            A
            S
            """,
        ),
        (
            315,
            """\
            X___
            _M__
            __A_
            ___S
            """,
        )
    ]
}
KERNELS_X_MAS = [
    as_int_image(desc)
    for desc in [
        """\
        M_M
        _A_
        S_S
        """,
        """\
        S_M
        _A_
        S_M
        """,
        """\
        S_S
        _A_
        M_M
        """,
        """\
        M_S
        _A_
        M_S
        """,
    ]
]


def eq(canvas: np.ndarray, mask_extended: np.ndarray) -> np.ndarray:
    assert canvas.shape == mask_extended.shape
    assert canvas.ndim == 2
    return (canvas == mask_extended).astype(int)


def convolve_step(canvas: np.ndarray, mask_extended: np.ndarray) -> int:
    power_mask = np.sum((mask_extended != CHAR_MASK_EMPTY).astype(int))
    return int(np.sum(eq(canvas, mask_extended)) == power_mask)


def extend_mask(
    mask: np.ndarray,
    ext_row: tuple[int, int],
    ext_col: tuple[int, int],
) -> np.ndarray:
    return np.pad(mask, [ext_row, ext_col], constant_values=CHAR_MASK_EMPTY)


def convolve(canvas: np.ndarray, mask: np.ndarray) -> np.ndarray:
    assert canvas.ndim == 2
    assert mask.ndim == 2
    assert mask.shape[0] <= canvas.shape[0]
    assert mask.shape[1] <= canvas.shape[1]

    diff_shape = np.asarray(canvas.shape) - np.asarray(mask.shape)
    shape_result = tuple(diff_shape + 1)
    result = np.zeros(shape_result, dtype=int)
    for row in range(shape_result[0]):
        for col in range(shape_result[1]):
            mask_extended = extend_mask(
                mask,
                (row, diff_shape[0] - row),
                (col, diff_shape[1] - col),
            )
            result[row, col] = convolve_step(canvas, mask_extended)

    return result


def count_hits(canvas: np.ndarray, kernels: Iterable[np.ndarray]) -> int:
    return sum(
        np.sum(convolve(canvas, kernel), axis=None)
        for kernel in kernels
    )


def count_xmas_hits(canvas: np.ndarray) -> int:
    return count_hits(canvas, KERNELS_XMAS.values())


def count_x_mas_hits(canvas: np.ndarray) -> int:
    return count_hits(canvas, KERNELS_X_MAS)


INPUT = as_int_image("""\
MSMSMAXXAXXXXAXXAXMASMXSXMASMXMXMASMSSXASAMXSAMXXSAMXXMAMMSSMSSSMXSAMXXXXXSXSXSMSMMMMSXMASMMMSMSSSSMMMSAXSSSSSSXMASAMXMSSMMSMMMSAMSAMXAMAMXS
SAAMMAMSSMMMSMMMSMXMXMAMAMAMAAMXMAMXAMXXMMSMSASXMSASAXXMXMAAXXAAAAMMXSMXSAAASAMAAMXSAMXXXAAAAAASAMMAAAMMMMAAAXMASAMXMAXAAAXAXAASMSMXMXSAMSAA
XMXMMAXMAAXAAAMAAAAMXMASAMMXSAMXSSSMMSSXMXAASAMXAXAAXMXSAMSSMMAMMMXMMMSAAMMMMAMSMSAMASXMMSSMMSSMAMSSMSMSAMMMMMMMMMSSXMMSSMSASMXSXAAASAXMMMXS
SSMSSSSSSMMSSMMSSSXSXSXMXSMAXAAAXAAXMAMAMXMXMMMASMMMXMAMAXAMAMSMMSAMSAMXSXSXMMMMAMXSSMXXAAAAAMAMXMAMAXASXXAMXMXAMXAAAXXAAMAMXMAMMMSMMASXMSMM
SAAMAAAXAMXMAXAXXAAMAXMMSMMMSMSSMSMMMASXMASAMAXSXMXSAMMSXMASMMXAAMASMAMAMAMASAMXSMMMMXMASXXMMSSXMAMMSMMMAXSSMSSMSMMSMMMMXAXMASAXAXXXMXMAXXAA
SMMMMMMMMSXSAMXSMMSMAMXXAAAAAXXAXMXASMSASASASMXXAMASMSAAXSAMXAMSMMXMMAMSSMXAMXMAXAXXMASMAMXSXMAAAAMMAMXMSMAAAMAMAAMMXAXXAXMSXSMSMXMMMASXMSSM
MXAASMMXXAXXXAMXXAXAASXSSSMSSSSMMMSMSASXMXSMMMAXAMXSAMMSXMASMSMMSSXMSXSAAMSMSMMASMMASASXSXASASXSMMXSAMXAAMMMAMAXXSMASMMMSMASAXMAXAMASASAMAXM
SSSXSAASMMSSSSXSMSMMASAAAXAMXMASAXASMXMASAMXAMAXAMAMXMAMASAMXMAAAMAAAXMMSMAAAAMASMMXMASAMMXXAMAMAAXAMXSSXMMSXMMSMXMAMSXAAMXMAMSMMASASXSAMMSM
MAXASXMMAXSAXMASAAXSXXMMMMMMMSAMSSXSMMXAMASXMXSAAMASMMAMMAASAMMMMSSMASXAAXMMMMMXSXXAXAMXMAXMAMSMMMSAMAMMMSAMAMSAMXAAAMMSMSSMSMAXSAMASAXAMAAA
MAMXMASMXMMMMMAMMMXAXSXSMXAAXMASAMAXASMMSMMASAXXXMXSMMSSMMXMASXXXAAMXMMSSSSMSXMASXSMSASXXAMSXMAAMASMMXSAMMAMAMSAMXAMXMAMAXAAAMXMAAMMMMMAMMSM
MSSMSAMXAXSXXMASXMASMMMAMSSSMSXMASMSMMAXXASMMXSMMSAMAAAAAMMMMMMXMSSMXMAXAAXAXXMAMAXAAAMMMXXSASXSMMSASAMASMXMXMXAMAXMXMSSMSMMMMSASXMXAXMXSXMA
XAAXMASMMSAMXMAMXXAAAAAAMMAXASMMMAXAMMSAMXMAXMAAAMASMMSSMMSASAAMAAMMSSMMMMMSMMXMMAMMMSMXXXAXAMAMXXMASMSMMXAMXXSAMXSSMMXAXXXSXAAMASAMXSAXSAMX
MSSMSMSMMAASAMXMSMMSSMSSXMAMXSAASXXASAAMXSSMMAMSMXMMXMXMXAMASXSXMASAMXAAMMAMMMAMXAMXAAMMSSSMSMMSMMMAMMAXXXXMMXMXMAMAAXSAMMSXMSMSMMXMAMMMMAMS
XAAAAAMAXMMXMMAAMAXAMXMAASXMAMMMMAMSMMXXMMAXMSXAXXSAMXAMMSMAMAXAMXMASMSMMMAXAMMSAAMMSSSMAAXSAXAAAAMMXSMSSMASAAMXMASXMMMAXXAAMAXSXSAMXSXXMXMX
MXSSMSSMMXXMSXSASMMMSAMXMMAMASASXMMAASMSSSSMSXSMSMMAMSASAMMSMAMMXXXAMXMAXSMSASAAMMMXAAAMMSMSMMSSSMXSAASAASAMSASXSXSXMAAMAMXASMMXASXSMSASMSSS
XMAMXAAXMXSAAAXAAMAXSASXSXXMASAMMASMSMMXAAXXSAXXAASAMSXMMSAAMSSMSSXMMAMMMSASAMXMMXSMMSMMMMASXAAMAXAMMSMSXMMXMMMMMXMASMSXSSMMAXSMMMXXAMAMMAMX
SAMXMSSMSAMMMMMSMSSMSAMAMXXMXMAMSAMMAAXMMMMMMMMSSMMAXXXMXMMMMXAAAXAASMMSAMXMXMSMSXSAXMASXMAMMMMSAMXXMAMXXAMSXMAAXASAMAMMAMASAMSASXSMAMXMMAMM
SXMAXXAMMASMXAXXMMAMMMMSMMSMMMXMMAMSSMMAASAAXMAAXXSXMXMSAMXXXSMMMSSMMSAMMXSMMXSAAASAMSAMAMAXXXAMXMSSSMSASAMMASMMSASXSAMSMSAMSASAMAMMXSAMMSSM
XAMSMSSMSAMAMMSMXXAMASXMAXAMXSMASAMMAMXSXXXSXMSSSMMMSXASXMXMAXAAXAMMMMMXSASAMAMMMAMAXMASASMSMMXMAXSASAXASMAMMMAAMAMAMXXXXMXSXXMXMAMASMMSAMMM
MSMMAMXASXMSXMAXMSXSASXSMMMSAASAMAMSAMMMSMXMAMAAAMAAXAXXMSSMASMMMASXXMAMMAMAMXSXSASXXMASAMXAMXSMSMMAMMMAMMSMXMMMMAMXMSMSMSMMXXSMSMMMXAAMASAS
AAAXSAMXMAAXAXXMXAAMXSAAAAAMMXMXXAMSAMSAAMASMMMAMXMSSXXAMAXMAMXXAAAMAMMXSAXXMMXAXXMXXSAMXMSXSAXXXAMXMXAXMAMAAXXASMSMMSAAAAMAMXAAMAASXMMSXMAS
SMMMXASXSXMSSMSMMMXMAXMSMMXSMMMMMSMMAMMSSSMMXASAXAMXAXMAMASMSSSXSXAMAMAXMAXSAMMMMAXMXMSSMASAMXSASXMXSSSMMMXSAMXXXMAMAMXMSMMSAAMSMSMSAMXXMMAM
AXAASAMASMAXMAAAXAMSMXAXMXASAMXSAXMMAMXAXMAXXASAMSSMAMSSMMSAMAXMXMXXASMAAAAXMMAMMSMXMAMXAMMXMXAAMXAAMMAMMAAMAMSAMXSMXXMXMXAMXSXXXAMXAMXXMMAS
MMMMMAMAMMSMMSMSMXMAAMSMXAXSASAMMSASXMMMMSMMMXMXMAAMXMAMAXMAMSMSAASXMMMXMMMXMMXSMASAMXMASXMASXMSMXMAMSAMMMMSASAMXSXSMMSAMXXSXMASMMSSSMMSSMAS
MSMSSSMMSAMXXXAMXSMMSMAAXMASAMXSSMMMSAASAAAMXAAAMSMMSMSSSMSAMXMXAXSAMXSAXAAMSMAXXXMSMAMAMAMXAXXMXXAAAMASASAMXMXMMSAMXASAXSAMXMAMSXAMAAAAAMAX
MAAXAMAAMASMSMAMAMXMXXSSXMAMAMAXMAMAXSAMMSSMSMSMXXAXXAAAAASXSAMSSMSXMASMSMSAAASAMXXXXAMASXSMMXSAMSSMMSASXMAMXMXMXMXMMASAMMSMAMAMMMASMMMXSMSM
MMSMASXMSAMMAMSMSXAXSAXXAMXSSXMASAMSXMMSAMMAAAAMASMMMMMSMXMASAMAAAXAMAMXAMXMXSMSXMXSXMSASXXASAMAAAXAMMAMASMMAMAMAMASXMMMXMAMAMAXAAXMASMXMAXM
SAXMXMAAMASMSMXAMAMSMMXSSMAMXAAAXAXXXAMSASMSMSMSASAAAAXAMXMMMXMAXASXMASMMSAMXMAXSMASAAMMSMSXMXSMMMSXMAMXXXSAASASASASAAMAASMSMSSSXSMSAMXSMAMX
MASMSSSMMAMAXAMAMAXAAMAMAMASXMMXXSMSMSMSAMAAAXAMASXMXMSAMXMMMMMMSAMASMSAAMMSXMAMAMASMMMMXAMXMAMASXSAMXSSMMMSMXMSASASMMMXXSAMAAAMAMXMAMXAMMMA
XMMAAAXMMXMXMMSSSMSXSMAXAMSAMXSMXXASAXAMMMXMAMSMXMMSAAMMMAXMASAAMMMASXMAMXMAMMXSMMXSMMSSSSSXMXMAMXSASAAXAAMASXXMMMASXMXXMMAMMMXMAXMMSMMMMMSX
MXMXMMMXMXXXAMAMAXAXMXSMSSXMAMMMMMAMAMSMSSXMASAMXSASMSMAXXXSAMMXXAMASXMAMSASASAMXMAMXXAAXXAXSAMSSMSAMMSMSXSASXMASMSMMSSSXAMMSMSSMXSAAAAXAAXX
MASAMAXMXASXXMAXMMSMSAMAXXAMMSAAAMAMAXXAASAXXMAMAMASXMMSXSASASAXSMMMMAMXXXAMAMXSAMMSMMMSMMMMMASAAAMXMXAXMAMXSMSMMMXASAAMSXMAXMASXAMASXMSMXSA
SASASXMAMXMAASASMSMAMAMSMSMMASMSSSXMXSMMMSMMSSSMMMMMMMAMAMASAMAXAXAMSMMSSMSMXMASAXSAMAXAXAXXSXMXMMMAXMAMSAMAMXXAAASMMMSMAXMXSMMSMSSXXXAAXAMM
MMSXMASXXSMSMMAMXAMMMAMAAAXMASAMAMMSMMXMAXAAAAXXASXSAMMMAMMMMMXAMXMMAAXASXMAMMXSXMSMSMSSSSSXMAMXMAXXSAMXSAMSSSMMMMMMXXMXMXMMXAXXMXAAMMXMMSSM
SXXXMMMMAAAXAMXMSSMMXXSMSMSMASMMXMAAAXSXXSSSMAMSASASMSSMAMAAXMXMSASXSSMMSMMAAAXMMMMXMMXAAAAAMSXMMSSSMMSAMXMAAAASXMSSMMMAXSXSMMSSMMSMAAAXAMAM
XXMMXAAMMMSMMMAMAAAAMMMMAMAMMSXSMMSSSMMMXAAXXMMSAMMMXAASASMSMXSMMAMAMXAXMASMSMXSAAMSSMMXMAMMMAAAAAMAAAMXMMMMMMMMAAAAAAMMMAAASMAMAAMXXSAMSSSM
MSMASMSMSAAAXSXMXSMMXAASXMXSMXAAAXMMAMAAMMXMMMAMAMXSMMMSMSXXMASAMAMXMMSXSXMMAXASMXMAAXSSSSSSXSSMMMSAMXSMMAMXAAASMMMSSMXSAMXMSMAXMMXSMMXXXAAS
AAAXSAAXMSSSMMASAMAXMSMMAXSXMMSMSAMXAMMXSMASAMAXASMSASASXSMSMASMMASAAXAASXSXXMMSAMMSMMSAAAAMMMMAMXAASXXAXXXSSSXXAMAAAXAAXSAMXMSMMAXXAXMMMSMM
SASAMMXMMAXAAXAMAMSMMMAMAMMAMMAAXMSSSMXAAMASASMSMSASAMASASAXMAMXSAXMAMMAMASXMXAMMMAAAXMMMMMMAXMXMMMMMAMSXSAAXMASMXMASMMMSAMXXAMAMMMSAMXAAAAX
MAMAMXAAMXXMSMMMMMMXASAMSASAMSMSMXAAAAMSSMMSAMXAXMMMAMMMAMXMMXMMMMSSMAXAMAMMAXMASMMMXXMAXSXSSSMXSAXSMXMAAMMMMMXAAAXXXMXXAAASMASAMAAXMASMXMSM
MSMMSSMSXMMMAXSMAAMAMSMMXAXMMSAMXSMMMMMMAAAMASXMMSXSAMXMMMSMSXMXAMXAASMMMASASAMAMAMSSMXAMSAMAAAASMSASMMMSMXXMMMAMMMAXMXMSMMMMASMMMSSMXAMMSMM
XXAXXMAXXAASMMMMMSSSMMMSMMMSMMAXAXMAMMXMSMMMAXAAAXMASAMXSAAAAMMASXSSMMAMSMSXMXSAXXMAMXAMMSAMSMMMSXSAMXAAMXMMAXSSMAXXMMMXMSAXSASMAMMAXMXXMAAA
MSMMAMAMMSMSAXMAMXMAXXAAAAAMASMMSMMXXXMXXSSMASXMMMSAXXSMSXMMMSMAMAMAXXAMMASAMAMXSMMMSSXSASAMXXAASMMMMXSXSASAAMAXSXMMSMAAXMMMSAMXAXSAMXMXSMXM
AAAAXMMXAAXXAMSSMASXMMSSSMSSXMMAXAMSXSAAXAXMMMMAMAMASXMASXXMAXMAMXMAMXAXSAXXMAMAAAASXMAMASAMXSMXSAAMMXMASASASAXXAMAMAMSSSMSAMAMMMXAMXAAMXSXX
SSSMSASXSXSAMXAAMXMXMAMXAAMMMAMAMAMAASMSMMMSAASAMAMAMMMAMAMMMSMXMSMAMMAMMAMSSMSSSSMSMMSMMSAMMXMAXXMSMAMAMAMAXXMMSXSSMMAXAAMXSAMSSMAXSMSAASXS
MXMAMAXXAXMAMMMSMMMMMMXSMMMMSSMXSSMMXMXMAXAMXXSXSASAMSMMSMXASXXAAXMASAMSMMMMAXAAMXAXXAAAASAMXAMXSXMAMASAMXMXMMSAMAXXXMAXMMMAMASAMMMMXAMMAMXX
MAMMMAMXMSSSMSAAXAAAAMMSAMSXAXMAMAAXSSMSSMSSMXMAMMMXAAAAAXXMSAMMMMMAMMAAAASXSMMMMSXMMSSMMXAMMMSXAAMXSASMSMMSAXASMXMASXSSXAMXSMMMSAMMXMMMSSSM
MSMXMMXAMXAXAMSMSSMSMXAXAMSMSSMSSSMMXXAAXXAAXMSASXSSSSSMXMMAMXMSMSMXXXSMMMSAXAXAAMAXMAXAMSSMAASXSXMAMXSMSAAASXMXMAMSMAAXXXSAAXSASAXXAAXAXAAX
MXXXSASXSMSMMMXXAMXXAMSSSMXAXXAAMXMASMMMSMSSMAMAXAAAAAMXAMXSAMXAAAASMMMMSMXAXXMMAMSXMAXXMAAMMMSAAXSMSAMASMMMAMXASXSAMMMMMMMMMMMASAMSAMMSSSXM
MSMAXMASMXMAMAXAMXAMAMXAAXMMMMMMSAMSSXXAMAAAASMSMMMMMMMMXXAMAMSMSMSMAAXSAAXSMSMSMSMMMSMMMSMXAXMXMMAAAMMMMAXXMASXMMSXSASAAAAAAAMXMXMXAXAAAAMA
SAMSSXMMXXSAMASMXMMSSMSMSMXXAXMAMAXAXMMMSMSMSMAMAMAMXXAMXMXSAMAAXMAXMMMSMSAXAXMAXAAAAAAXXAAXSMMAXXMMMXSASAMXXMMASMXAMASMSSSMSMSAMXSSMMMSSMAM
SASXMAAXMMSAMXAMAMXAXMMAAAASMSXMSSMAMSAMAMAXAMAMSSSSMXSAAXASXMMXMMMSXAAMXMMMSMSSSMSMSMSMMMSMMASMMSMSAMMAMSSXAXSAMMMMMAMMXXMAXMSASAMASAXAMXSM
SXMASAMXAASAMXMSSSMSSMMSMSMAAAAMAXXMMAMMAMXXMMMMMXMAMAMXSMASXSAXSAASMMSSXAAAXAAAAAXAXAAAMAAMXMMAAMMMAMMXMAXMMMMAMXAAMASAMMMSMASXMASAXMMAMAAX
XAMAMXXMMXSXMMMAAAAXAAAXAAMMMMMMASMMXXAMXSSMSASASASAMXSAXMMMAAMAMMXMASAMXXMSSMMMMMMAMSSMMMXSAASMMSXMXMSAMXSMMAMMMSSMMASMXMAMMXMASXMMSMSAMXSM
MSSMMASXXAMAMXMMSSMXSMMSMMSSXSXMXMAXMSXSAAXASXSASASXSAMXSMAMXMMMXSMSSMMSSXAXAMASAAMAMMAMXAAMMXMMXMXMSMMASAAMSMSAAMASMMMXSXMXMASAMXXSAMXMASAA
AMAASAXXMAXSMSXMAXXAMXXSAMXMAMMMMSSMXAAMMMMAXAMXMAMAMMSSMXAASXXMASMMXAXAMMMMMSASXSSMXXAMMMSSSSXMAXMXAAXAMMSMAASMMMAMXMSAMAMMSXMAMMMMAMSAMXXS
SMSMMXSMSAMMXSAMXMASXSAMXMAMAMAAMAAAMMSMXXMSMMMMMSMXMAXAXMXMXASMAXAASAMXSAMAXMXSXXMMMMSMMXXAXAASMSSSSSMSSXMMMMMMAMMSMAMASXMAMASAMSMSAMXMAMXX
AMMAXXAAXMASAXXMXXXXASXMASASMSSSMSSMMAMAMXAAAAXAAAAAMXSMMMSXAAMMXXXMSAMXSASXSXSXMSSSXAMAMMMMMSMMAAAXAAAXXXMAMXAXXSXAAMSAMXMAXAMXSAAMXSSSSSSM
MMSAMXMASAAMXMSMMSAMMMASASXSAAAXAMXAMXSAMXMSMMXMSSSXMAAXAMMMMMAXSASXMASMMXMMSMMAXMAMMASAMAXXAMAMMMMMSMMMMXSAMSSMXMMXXXMASXSMMSSXMMSMMMAAAAMA
XAAAXXXXSMXMAXSAAXXXXSMMXMXMMMMMSMSSMMSAMSXMAAXXAMAXMSMMXXAAASAMXMAAMASASXSASASMMMAMSMXASXSMSSSSSSMAXAMAMAMAMAAXSMMSSXSXMMMMAAAXMAXXAMAMMMMS
MMSSMMMXMXAXMSMMMSXSXSXSMMSXSASMXAXMAASAMXASMMMMASMAXAASMXSXXXXXAXSXMASMAAMASAAXASAAAMMMMMXAAAAAXXMXSAMAMASMMSSMAAAAXAASAXAMMSSXMMSMSMAMSXAA
MMMMMAMAMSMSMMAAASMSAMASAASASASAMSMSMMXMMMMMMXXSMMMMMMSMAAXXSXSSMMXMMXSXMXMAMMMSXSMSXSAMXSMSMSMMMXAAMMSAXAMAAAAASMMMSAMXXMAMXAMXSAAAMXSMMMMS
XAAAXMMAXAMAAMSMXSAMXMASMMMAMAMMXXAMXSXXAXMAAMMXMAMXSXMMMSMAMAMXSAXMXAXAXMSSMSASMXAMASASXSAAAAXXMXMASAXMSSSMMMMMXXMXSXXXXMASMAMASXMXMAMAMMSX
SSSSSSSMSASXSMXSAMAMMMXSMXMXMXMSAMMMAMMSSSSMMXSAMSMAXSMAXXMAMXMAMSSMSMSSMMAMXMASXMAMAMAAAMSMSMSMXSXMXMXAAMXXAAXMMXMAXSAMXMASXMMASMSSMASAMXAX
AAXAAAAXSXMAMXSMMSSMMAAXMAMXXAMMASXMAMXAXMASMAAXAMMMSXSMSMMMXAMMMAXMAMAAAMAMAMAMASXMXMXMSMMMMAMMAMXMASMMSSSSSMSAMXMAMAXSAMASAMMXSXAAMXSMMMSS
MSMXMMMMMMSMXSAMXAAASMSSSSSSMSAXAMXMSMMMSXAXMMMMAMAXMMMXSAMSSMSSMSSSSMSSSMMSSMSSMMASAMXXMASAMAMMXSXMAXAAAAAAAXMAMXMSSSMSXSXSXMXMMMSSMMMMXSAS
MMMMMAMAAAAXMXMSMASMMXAMXXAMXXAMSSSXXASXMMMMMAXMAXMMMXSAMXMAAAAAXXMAXAAAXXXAMXAAASAMASMMSAMAMMSMAMAMSSSMMSMSMMSMMMAMAAAXAXMSXMASAAMAXMMAMAMM
MAAAMASMMXSSMAXXMAMASMSMSMSMAMAMAAXAXXMASXXASXSMSAAXSMMSXMMSSMSSMSMAMMMMMXMAMMSSMMASAMMAMASXMXXMAXAMAAAXXMMAMMAAAXAMSMMMMSASASASMSSMMMSASMXA
XSSMMASXSAMXMAXXXAXXMAAAXAMMXSAAMXMXMMSAMXMXSAAAMMMXSASAMSAAAXAXMXMAMMXAXSMSMXMXXXMMXSXASXMMXXSSMMSSSMSMXASASMSSMSXXAMXAXAXSAMASAAMAAXXAMXSX
AMAMSASAMXSXSSSSMMSAMXMAMMMAMXXSSSMAXMASASAMXMMMMAMAMXMAAMMMSXXAMAXAMMMSAAAMSAMMMSSMMXMMSAMXAAXXXXXAXAAXMMMXSAXXMAMSAMSMSMAMXMAMMMSMMMMAMASM
XMAMSAMASASMAAAXXAAAASXXMAMASXAXAAXAMMXMMMAXXXAXMAMMXSMXMAAAXMSXSASXXMAXMMSMSXSAXAAASMMXSMMSSMMSMSMAMSMMAASXMXMAXXAMAMMXMXAAXMASAAXMASMSMAMA
SMSMMASXMAXMMMMMMMSSMMXSXMMAMMMMSMMSXSAXAMXMSSMSSSMSAAXSXXMASAAXMAMAAMSMXXMAMASMXMSMMXMAMMAMAXXAAAMAMAMXSMSMSXSXMMMMAMMASMMSXSASMXSXXAAMMMSS
MAXXSAMMMSMSXAAAAAAXAMAAMSSXXASAMXXMASASMMMAXAAXAAAMMSMXASMXMMMSMSMMMMAAXMMAMMMXAXXXMMMSMMASMMXMSMSMSMSAMAXAXMSAMASMMMSMSAMXAMXSXASMSMSMAXAM
MAMAMASAAAMXXSMSSSMSAMMSAAAMSMMMMMMMAMXSAASMSMMMSMMMMMXSMXMAMAXAAMSMSXMMSASXSMAMXXSAXAMXASASASAMXMAMAXXAMAMSMASXMASASAAXSMMMXMAMMMXAAAMMMMMM
MMSXMSSMSSXSAMMAMAXSXXXMMMMMXAAAXAAMMXAXXMMAAXMAXXXSXMAMMAMAMMXMSMSXMASASMMXAMXMMASXMSASXMASAMXSASMXXSMMMAMMAMSMMASAMMXXMXSMXSMXSSSSMSMAMSSS
MAMXXXXAMAASAMMASXMMXSXAXSSMMSSSSSSMSMMSXXMAMXMAMSAMAMAXXASMSMSMMASXXAMAMXSSMMASMAMMAMXMMMXMAMAXXMXSMMASAMXXMXMASAMMSSMSMAXMASXMXAAAXMMMMAAM
SSSMSMMMMMXMAXSASMAMAMMSXMAAAAAXMAMAMAASMSMMMXMASMASXMAMSASAAAAAMAMMSSMSMMXAXSAAMXXSSXMMASMSSMSMMSXAASAMASMMSMSAMXSAAAMMMSSMMSASMSMMXXAXMMSM
XAAAMAAXAXXMAMSAMXAMXSAMASXMMMMMMAMMMMMMAXAAXMMSXMAMXXAMXAMMMSMSMSMXAMAMMMMMMSMMXSAAXAASXMXAAMAASASMXMASXMAAAXMXSAMMSSMAAAXAMSAMAMXXXSSSXSXM
MSMMXMMXAXXMAMXAASXSSMASAMXXSSMXMSSXMXSMSSSMSMXMASMMAMSASXSSXMMAAXAMMMSMMSASAMAAAMMMMXMMASMMSMSSMAXXASMMAMMSMAXSMMSAAAMMSSXMMMMMMMMXXAAXMASX
AXAXXMSXMSMAMMXXMXXMAMMMMMSMSASXAXAMXAXAAAMAXMSMAXAMAAAASAXMAASMMMAMXAAAASAMMSMMMMAAXMASAMXAXAMAMAMSXSMXMMAMXSMXMXSMSXMAMAMSAMXSXAXAMXXAXMMS
MSMMSMAASAMAMXSSMSMSMSSXXAAXMAMMSMAMMASMMMMSMXXMAMAMMSMSMXMSMMAAMMAMXSSSMMAMAXMASXSMSAMMASMAXAMAMXXMAXMASMMSAXAMSAMXMAMMSAAXAMAMASXSAMMXMXSA
MAXAMMAMSASXSASAAMAXXXAAMSSXMAMAMAAXXXSAAMAMMMSXXAAXXMXXAXXASMMSXSASAMXAASAMSSSMSAXASXXSXMMSSSMSMSAMMMXXMAXMMMMAMAXAMXMXSMSMXMASAMAXAXSAAMSM
SSMMSSSMXAMXMMMMMMXMMMMMMAAMSAMXXMSAMXXXMMASAMAMXMXSXMASXMSMAXAAXMAMMSAMXMAMAAXMMAMAMMMMAXAMXXAAAMSASMSMSMMAAAMSMSMXSASXXXAAASXMASASMMSXSASX
AAAAAAMMMSMXMAXSAXSAMAMAMSSMSAXASXAASASXSSXSASMMMSMMMMASAMXXAMMSSMMMSXAXSXMMMMMMMMMAMAASMMSSMXMMSMXXXAAMASASMXXAAAMXMASAMSXSMSASAMXAMXXAMAMA
MMMMMSMAAAASAMXSASXMSASXMMAMXMMSAMXXMXSAAXASMMAAAAAMSMXSASAXXSAAAAAXMAAXMASMMXSAAASMSMMXAXAAASMAXXXXMSMSMAXMSSXMSMSXSAXAMMMMXSAMXSAXSAMXMAMA
SXMXAMMMSMSAAMAMXMAXSAXXXSXMAMXMAXMMMXMMMMMMMSXMXXXMAMXMAMXSMMMSSMMSSXMSMAMAAAXMMXXAMXSSXMSSMXMAMMSMMXXAXMXMASMXAMXMMMSAMXAXMMXMXMMXSAXXXAMA
AMXMAMAMXMXMSMAMAMXXXMXSXMASASXSXMAAMAXAMAAAAXASASXSXSAMAMXXAXXAAAAAXAAXXASMMMSSSSMMMAXMAMXAAXMMMAAAMAMXMXXMASMSAXXXAAMASMSSMSAMXMSAXSAMSSSM
MAMASMMSMMSAXXMSMSAMXMASASAMXSAMXAMSSMSSMSMSSMMMASAAXSXMAXSMMMMSSMMSXMMASASXMAMXAAAXSMMMMMXMMSMAMSMSMMSAAMXMXSASAMSSMXSAMXXSMAAXXSMMSAXMAAAM
SSMAXMASAAMMMMXAMXAMAMMMAMXSASASMSMAMAAXAMXAXAXMAMMMMMASMXSAAAXAXMAXXSAMXAXMMAXMMMMMAXAAAMXSAMXAMXAMAXSXSMASAMMMAMXAAMMMXAMXSSSMXAMXAMMMMSMX
AAMMMMASMMMSAMSASMSMSSSMSMMMASMMAAMXMMASMMMSSSMMMSXMAMMMMAMSMMSSSMAMASMSMSXXSSXSASMSXXSMMXAMASXSSXASAMXAAMXMAMAMMMSMMMXSMSMAMMAXMMSXMXSAAXXM
SXMXAMXMXSXMAMSAMAXXMAXXXAXMMMASXMMMSXAAXAXMAMXAAXMSMSMSMSMXMMXMSMASASAXAXMMMMASASASAXMASMASMMMMXMXMAMXXMXMASAXSSXMMSSMSAAMASMMMMXAAMASMSMSA
MASXMSSXAXXMXMMAMAMAMXMASMMMMSAMMSXAXMSXSASMSMSMMSAASAXAAAXMAMSAXSMAAMAMAMAMAMMMXMAMSAMAMSAMXAAXXXXMASXSMXMAMMAMXAAAAMAMSMSMSAASMAXSMASXMAMS
MXMAMAMMMMMMSSSSMASXMMSMSAMAAMASAMMXSXMAMAXAAAXAAMMMSXMMMMSAAAMXMASMSMSSSSSMMSSMXMXMMXMAMXMASMSSSMXMASMAMAMASAMXSXMMSMSMMXSASXMSSSXXMASMMAMX
MSMSMASMXAASAAAXSASAMASXSAMMXSAMASMXSAMAMMMMMSMAMXAMXXMXMAMMMXSAAASXXAXSAAMAMAAMMSAXSMMSXMAXAXXAMXAMAXMASXSASXSMMXXXXAMASAMMMXMXAMASMXSXSSMM
AAAMSXMXSMMXMMMMMSSXMASXMAMXMMMMMMMAMASXMMMSMMMAXSMSAMXAMASXSASXMAXXMMMXMASAMSXMAMAXXAAXXSSMSSMSMXXMAXXAMXMASMMAXXMMMAMAMMMMSAMMXMSMAXMASASX
SMMMAMXMMSSSMMSXMAMAMSSXMSMMMAMAMAMXSXMMASXAAAXXMAMMASMMSXSAMXSAMXSSMMAXXMXAXAAMMSSMSMMSXSAAMAAAAXMSMSMXSAMMSASXMMSASAMSSMSASMSAMSASXMXXSAMX
MMMSXAMMAAMAAMMMMASXMMMXAAMAMSMMMASAXMASAMSSXMXAXMXSAMXXSAMXMXXXMAMAAXASMSSSMMMSMAMMXAAMXSMMMMSMSMAAAXASXXSASMMXSAXMXAMXAAMASXMAXSAMMMXXMXMM
SAMXASAMMSSSMMAASMSMAAAXSAMMMXAMSMMMSSMMAMAXXMASMMAMASMMMMSAMXSMSSSSMMASAAAAXAAMMAMMSSMSMXAAXMAXAAMASMMMMMMASMSAMMSSSSMSMMMASAMSMMSMAAMSMAMA
SAMSMMXSAXMMXMSXSAMXSMAMXMXMAMMMAMAAMAXSXMASMXMAAMASAMMAASXMMXMAAAAAXXAMMMMMSMSSMMMMMXAAMXSMSSSXSSXXXXXAMSMSMMMXSASXAAAXAXMASAMXMAMSSMAASAMS
MMMSAAXMXSAMSMMXMMMAMMXSASXMASXSAXMSSXMSAMXMMAXSXMXXMAXSXSAXSAMXMSSMMMSSMXAXSAMAASXSSMSMSAXAXAAXXAXSAMXSMAXMMSAMMXSMSMMMMSMAXMMAMAXXXMSXSMSX
MAMMMMSAAMAMSASXMXMSMSASAMASASMXMASXMASMMMAAMAMXMSMXXSXMASAMSXSAAAAAXXMAMMAMMAMSMMAXAAAAMMSAMMMMMAMMAMAXXMXSAMAMSAMXMXSXAAMMSMSSSMSAXMAMXMAM
SMSMSASMSMMAMAMASAMMAMASMXXMASAMXMXAMXSAAMSSSMSAXAAXAXAMXMSXXASMSSSMSASAMSSMSXMXMMMMXMMAMAMAMXMAMMMSAMXSAXXMASAMMAMMSASMMXSXAMAMAAMMMMMMSMAX
AXAAMASAAMXAMAMMMASMAMXMAMSMMMMSSMSSMXMMMXMAAAXMMMSMMSAMXAXMMAXXAXMASAMAXAAMXXMMSAXMSMXMMMXSXMXXXMAXAMAMMMMXMMXXSSMAMASXAAXMMMASMMMMMAAASXMX
MMMSMAMXMASXSMSASXMXSMAMSXMAAMXAAXAASXXXMSMMMMMSAMXXAAAXMSAXMXMXSMMMMXMMMSSMSMSASXXMASAMASMMASMSSMMXSMASXXSAXASXAAMAMSMMMXMAASXSAXXAAMMMSASM
AAAAMXXAXMXAAASASXMAXMXSAAXSMMMSSMSAXSAMXAAMXMAMAXAMMMMXAMMXMASAMXASAMXMAXMXAAMXSMMMAMMMAXASAMAAAASAMXMMAAXAMXMMMMMAMAAAAXMSMSASXMSXSSSXSAMS
SSSXSXSMSMMMMMMXMMMMMMXMMSMAAXAMXXMASASMSXSMAMSSSMMSMSMMAXAAXAMMSXXXAMMXSXMSMSMXXAAMXSXMASMMMMXMSAMXSXSMMMMSMMMAXXSSSMSSSXAAAMAMAMXMMXMAMAMA
XAAMXMAMAMAXXXMAMAMMAMXAAXXSMMSSMXMXMAXXAAXMASMAMAXAAAXMASMMSMMMSASMXMASMAMXXAMSMMMSAAMSXMMAXAMXAMXAMXXXXAAAAASMSXSXAAAAAMMMSMSXXMAMXAMMMSMM
MXMMSAXSASAMXSSMSMXSASAMXXXMAXMMMASAMAMMMSMAXXMASXSMMXXXMAXXAMXAXXMAXMSASAMXSXXAAAAAMMMSASMSMMSAMXSAMXSMSMSSSMSASMSSMMMMMXXSAMXMMXSSSXSAAAAX
XMXMAXMMASMSAAAAAXXMASXMASMSSMSAMMSXSASMMMMMMXMXSMXAMSMMXAXSXSMSSSSSMMXMSMSXSMSSSMSSXSASAMAMSMXAXMAAXAAXXXMAMMMXMAXXXAXMAMSASMMSAAMAMXSMMXMM
XMAXMXSMMMAMMSMSMXXMXSAMXAMAAASASAMXSMMMAAAMMXMAMAMAMAAXMXASAXAMAXAAMXSAMASASAAMAMXXAAXMAMAMMSSSMASMMSMMSMMMXMASMSMXMASMAMMAMXAMMSMAMASXSSSS
XXMMSAAASMXMAXMAXMXSMSMMMXMMMXMXAMAAXAASMSMMXAMASASXSMXSAMAMMMSMMMSMMXMAXXMAMXXXSMSMMMMSXMXSMAMXMMAXAAAMMAMMAMSMMMMMMAMMMMMAMMSMMXXAMXMAXAAA
SXSAMXSAMXAMMXSASMMMAXXXSMSXXXAMMAMMSMMSAXMASXSMXAXAMAAXXMXAXAXAMXMASMXSMAMXMMXSMMSAAXAXASXMMASAMASMSMSMSAMMASAAASAAMSSXMASASAXAAXSXSAMSMMMM
SMMASAMAMXXXAXMAMAAMSMMMMASAMSAMXXSAMMAMXMMASAAMMSMMMMMSXMSMMMMMMAXSXMAMMSMSMSXAAASXMMXSXMAASMSXSAMMAMMMSMSSXSXSMSXMXAAASASASMSMMMMXMASAAXAX
MASAMXSXXXMMSSXASMMMAXAMMAMAXXMXXXMAXXMSMSMASMSMXMASXMXSAMAMASAMXSMMAMASAMASAMSSMMXAXSASASXMSAMXMASMAMXASAMXAMAMMSXSMMSMMASXMXSAMMSASMMMSMSA
MMMASXSASMAMAMXMAMMSMSXSMSSXMASXMSMSMMXAAXMASAXAAASMASAMASXMASASMMASAMASAMAMAMAXXXSMMMAXAMMXMAMXMMMMMSMMMMMMMMAMAXAMMAMMMAXXSXXAMAAMASAXXAAX
SMSMMMMAMMAMXMAXAXXAXAXSAMXASAMAAAAAMAXMSMSXMMMXXMAXAMASXMXXASXMASAMASASAMXSAMSSMXSXAMAMSMMASAMSMASXMAXXAMASXMSMSMAMMAMXMMSAMMSSMMSXMXXMASAM
AXAAAXMAMSMSSSMSAMSAMXSMAMSMMMSMSMSXSMMXMAMMAAAXSSSMMSXMAAXMXMAXMMXSXMXSAXASAMXAMASMMMMSMASAMAXAXXSASMXMASASMAMAASXMMASAAAMAMMAMAAAMXSAMXMXA
MSSSMSXMMSMAMAMMMMMMXSAXAMAMAXXXXAXXAASAMAMXSMSXMAXAAXMSMMMSMMXMSMMSMSXMMSMXXXXAMAMMXAXAMMMSSMSSSMMAMAASXMASMAMMMMSXXMAXMXXAXMASAMMAASXMSMMS
XXAMASXMASMSMXMASXSAMSASXSXSXSXSMMSXMAMAXMMXMAMAMAMMMMMXMAAMAMAMXAAXAMASAAXSXSMMMXSASMSMSMAXMXAAAXMAMXMAAMXMMSXSAMXSMMMXMASAMMAMAAXMAMAXASAM
XMMMAMXMXSAXXAMXSAMSXMMMXAMXXMXSAAAXXASXMASMSASAMASXSXMASMXSAMASXSMMMMAMXMXMAMXSAMXAAAAXAMSSSMMXMMMXXAXXSMSAXAASMMAMXAMXXXAAMMMSAMXSMSMSAMXS
SMXMASASXMAMSASAMAMMSMSXXSMXASAMMMSSXMAXSMAAMAXXMXSAMMSMSAXSXSASXAAASMSSSMSMXMAMAMXMMSMMMXXAMXXAAMSSSMSXMAMXMMXMAMASMMMMAAMMMXMAMMXSAAXXXAMA
XMASASMMAMXMMXMASMMAAMXMAXAMXMMXSXAXMXAXSXMMMSMMSAMAMXAAMMMMXMASMMMSAXMAMAAXSMXMSMSMXXMASMMAMASXSMAXXAMMMAMMXXAMXMMSAXSAMXXXSXMASXAMSMSMMMXS
SXMXASXSAMMAXAXMXXMSMSAAXMAXSASAXMAMMMSSMXXXAAAXMAMMMSMSMSAMMAAXASMXMXMAMMMMXAAAAAXMASXSMASMMXSMAMMSMMMASASMMSXSASASMMAAXXSAMASAMMMMMMAAMSAX
XASMMMASMSASXSSXSAMAASASXMAMMAMMSSMMSAMAMMMMMSMMMMMAAXAMMSASAMXSMMAAXMMMSAAMSSMSMSMMAMMMMAMXMAXXASXSAXSASMSAMAXSAMXMXSSMMXSAXAMASMXAMXSSMMAM
SAMAASXSAAXMAMAXSAMMXMAXAMSMMXMXAAMAMMSASAAAAMASASXMMXXMASAMXMXSXMSSMAXAMMSMAXMXMAAMASASASXMXSXSXSAMXMMAMMSAMMMMXMSXAMASMASXMXSMXXMSSMAAXMAM
MMMAMSAMXSMMAMSMSMMMMMMMMMMAXMSMSSMASMSAMMSMXSAMMXAAASMMMMMMASMMAMAMXSMMSAMXMMSAMMSMMSASAXXAMMAMAMAMMSMSMAXMMMAXAXAMXSAXMAXSMXAMAXAAAMSSMSAS
SASXSMAMAMMSSSMASAMXAAMXSASMMAXXMAMXMAMXMAMAAMAXXSSMMAMAMXXSAMASXMASXXAXMASXXASASAXXAMXMXMXSAXAMAMXMXAAAXSMSSSMSMSMMXMASMXMAXMAMXMSMMMXMASXS
AXASXMAMAXMAMAMAMMMSSMSAMXMXAXSMSSMMSXMAXMMMMSMMAAAXXASAXSAMAXMMSMSMAMMMSMMXMASAMAXMXSAMMXMMMSMSMXAMXMMMMMAXAAXAAAAXAAXMASMMASMMXMAAXMAMXMXM
MXMSXSXMAMMXSSMMSAMXAAMASMSMSXSASMSAAAAMMSXMXAMMSMMSSMXMSMAMAMMAMXAAMXAAAMMXMAXXAMXSAMAXXAMAASMAMSASXSASAMSMMMSMSMSMMMMMAMMXAAXMXSAMMXAMAAAA
XSXSASAMMXSAAAAXSMXXXMSSMAAAXMMSMAAMMSXMAMAMMMXMAAXAASXSAMAMMSMASMXSMMSSSXMAMMSSMMXSASAMXXXASXXAXXXMASASMXMASAXXMAAAXXAMXSSMSSMSAXXMMSASXSMS
XMAMAMAMAAMMSMMMSASMSMSXMSMMMAXXMXMXXXXMASAMXAASMMMSMMXMAMXMAXMXMMSAAXMAXAXSSMAAAMMSXMASMXSMMMMSSMSMMMMMXAAXAXSAMSSXMMSXMMAAXXAMASMMXAXXAAXA
XMASASAMMXSAAAAAXAAAAXMAMAASMSMMMMXSMMASAXMSMSXSAMXMXMAMXMSMSSSMAXASXMMMMXMMAMSSMMAXMXAMMAAAMXAAAXAAXMASXSSMMSMMMAAXSXAMAXMMMMSMAMAASXMXMMSM
MSXSAMMXSAMMSSMMMMMSMXXMMSXMAXMASAAAAMMMSSMXMASMXMASAMASAAXAAAMSMXMAMXMASMMSAMXXAMXSAXSAMXMXMMMSXSMSMMMAAAAAXXAAMMSMSAMXXAXAXAAMSSSMSAMXAAXX
AXAMAMSAMMSAMXMMSMMAMSSSMXXMXMSSMMMSSMAAMXMMMXMSAMASASASMSMMMSMSSSXAMSXMMAAMMMMSXMASXMXAAMXXXMAMMXAMAAXMMSMMMMSMXAMAXSMAAXSSXMXSMXXASAMSAMSA
SMMMMXMASAXMSASAAASXSXAAASXMXMXMXAXMXXMSMAMASAASXSMSAMMMMMMAMMAMASAMXSAXSSMSXAXSXMMSASXSMMXMASAMXMXXAMXXAMMAXXMMSMMSMAMXSAAAASXMMAMMMAMXASXM
AXMAMASMMMSMSAMMSMMMMMMMMMAMAXAMMSSMAMMAXMSAXMMMXXAMMMXAAASMSMAMMXXMAMAMAXAMMSSMASASMMXAASMMMSAAXAAXSMMMXSXSXSAAAXMASMXAXMMMMMAAMXMASXMSXMAM
SXMASAXAAXAAMAMAMXMASMMSXSAMXMAXAAAMSMSMSXMMXSAASMXMMMSSSMSAAXXMXXSMSSMAMMSMAXAXXMASXMSXMMAAAXMMMSMMXAXSXMMMAXMXSMSASXMMXAMMAXMMMXSXMMMMXXAM
MASASXSSMSSSSSMASASXMAAXASAMMSSMMSSMAMAASMMAAMMSMSAXAXMAXAMXMMSSSMXAMAAXMAAXXSAMXMMMAMASMSSMSSMXAASAMSMMASAMSMSAMMMSSMASXMMSSSMMSAMAXMASMSSS
SAMMSAMAAXAAAXMASMMMSMMMMSAMAAAAXMAMSSMMMAMMSSXMASXSXSMXMXMAXAAAASMXMASMMSSSXMXMASASXMAMXAAAAXAMSSSSXXASAMMXMAMXSMMAXAMSAAAAXAMAMASMMSAXMAAM
MMSAMXSMMMMMMMAMSMXMASAMXSXMMSSMSAXMXXXXSXMMMAMMXMMAMXMAMXSXSMMSMMXAMXMAXAMXMXXSXMASXMXMMSMMMMSAMXMASXXMSSXSMSMMMMMMSSXSMMMSSXMASXMAXMXSMMMM\
""")
