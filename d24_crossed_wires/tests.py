import itertools as it
import pytest

from . import *  # noqa


@pytest.fixture
def text():
    return """\
        x00: 1
        x01: 0
        x02: 1
        x03: 1
        x04: 0
        y00: 1
        y01: 1
        y02: 1
        y03: 1
        y04: 1

        ntg XOR fgs -> mjb
        y02 OR x01 -> tnw
        kwq OR kpj -> z05
        x00 OR x03 -> fst
        tgd XOR rvg -> z01
        vdt OR tnw -> bfw
        bfw AND frj -> z10
        ffh OR nrd -> bqk
        y00 AND y03 -> djm
        y03 OR y00 -> psh
        bqk OR frj -> z08
        tnw OR fst -> frj
        gnj AND tgd -> z11
        bfw XOR mjb -> z00
        x03 OR x00 -> vdt
        gnj AND wpb -> z02
        x04 AND y00 -> kjc
        djm OR pbm -> qhw
        nrd AND vdt -> hwm
        kjc AND fst -> rvg
        y04 OR y02 -> fgs
        y01 AND x02 -> pbm
        ntg OR kjc -> kwq
        psh XOR fgs -> tgd
        qhw XOR tgd -> z09
        pbm OR djm -> kpj
        x03 XOR y03 -> ffh
        x00 XOR y04 -> ntg
        bfw OR bqk -> z06
        nrd XOR fgs -> wpb
        frj XOR qhw -> z04
        bqk OR frj -> z07
        y03 OR x01 -> nrd
        hwm AND bqk -> z03
        tgd XOR rvg -> z12
        tnw OR pbm -> gnj
    """


@pytest.fixture
def circuit(text):
    return Circuit.parse(text)


def test_parse(circuit):
    assert Circuit(
        relations={
            "mjb": XOR("ntg", "fgs"),
            "tnw": OR("y02", "x01"),
            "z05": OR("kwq", "kpj"),
            "fst": OR("x00", "x03"),
            "z01": XOR("tgd", "rvg"),
            "bfw": OR("vdt", "tnw"),
            "z10": AND("bfw", "frj"),
            "bqk": OR("ffh", "nrd"),
            "djm": AND("y00", "y03"),
            "psh": OR("y03", "y00"),
            "z08": OR("bqk", "frj"),
            "frj": OR("tnw", "fst"),
            "z11": AND("gnj", "tgd"),
            "z00": XOR("bfw", "mjb"),
            "vdt": OR("x03", "x00"),
            "z02": AND("gnj", "wpb"),
            "kjc": AND("x04", "y00"),
            "qhw": OR("djm", "pbm"),
            "hwm": AND("nrd", "vdt"),
            "rvg": AND("kjc", "fst"),
            "fgs": OR("y04", "y02"),
            "pbm": AND("y01", "x02"),
            "kwq": OR("ntg", "kjc"),
            "tgd": XOR("psh", "fgs"),
            "z09": XOR("qhw", "tgd"),
            "kpj": OR("pbm", "djm"),
            "ffh": XOR("x03", "y03"),
            "ntg": XOR("x00", "y04"),
            "z06": OR("bfw", "bqk"),
            "wpb": XOR("nrd", "fgs"),
            "z04": XOR("frj", "qhw"),
            "z07": OR("bqk", "frj"),
            "nrd": OR("y03", "x01"),
            "z03": AND("hwm", "bqk"),
            "z12": XOR("tgd", "rvg"),
            "gnj": OR("tnw", "pbm"),
        },
        values={
            "x00": 1,
            "x01": 0,
            "x02": 1,
            "x03": 1,
            "x04": 0,
            "y00": 1,
            "y01": 1,
            "y02": 1,
            "y03": 1,
            "y04": 1,
        }
    ) == circuit


@pytest.fixture
def simple():
    return Circuit(
        values={"x": 0xa, "y": 0xc},
        relations={
            result: operator("x", "y")
            for result, operator in [("p", AND), ("q", OR), ("r", XOR)]
        }
    )


@pytest.mark.parametrize(
    "variable,expected",
    [("x", 0xa), ("y", 0xc), ("p", 0x8), ("q", 0xe), ("r", 0x6)]
)
def test_evaluate(expected, variable, simple):
    actual = simple.evaluate(variable)
    assert expected == actual


def test_simulate(circuit):
    values_new = {
        "bfw": 1,
        "bqk": 1,
        "djm": 1,
        "ffh": 0,
        "fgs": 1,
        "frj": 1,
        "fst": 1,
        "gnj": 1,
        "hwm": 1,
        "kjc": 0,
        "kpj": 1,
        "kwq": 0,
        "mjb": 1,
        "nrd": 1,
        "ntg": 0,
        "psh": 1,
        "pbm": 1,
        "rvg": 0,
        "qhw": 1,
        "tgd": 0,
        "tnw": 1,
        "vdt": 1,
        "wpb": 0,
        "x00": 1,
        "x01": 0,
        "x02": 1,
        "x03": 1,
        "x04": 0,
        "y00": 1,
        "y01": 1,
        "y02": 1,
        "y03": 1,
        "y04": 1,
        "z00": 0,
        "z01": 0,
        "z02": 0,
        "z03": 1,
        "z04": 0,
        "z05": 1,
        "z06": 1,
        "z07": 1,
        "z08": 1,
        "z09": 1,
        "z10": 1,
        "z11": 0,
        "z12": 0,
    }
    expected = Circuit(values=values_new, relations=circuit.relations)
    actual = circuit.simulate()
    assert expected == actual


def test_output(circuit):
    expected = 2024
    actual = circuit.simulate().get_output()
    assert expected == actual


def test_operand_capacity(circuit):
    expected = {"x": 5, "y": 5, "z": 13}
    actual = circuit.capacity
    assert expected == actual


@pytest.fixture
def adder_2bits():
    circuit = Circuit(
        values={name: 0 for name in ["x00", "x01", "y00", "y01"]},
        relations={
            "ac": AND("x01", "y01"),
            "axc": XOR("x01", "y01"),
            "bd": AND("x00", "y00"),
            "ef": AND("axc", "bd"),
            "z00": XOR("x00", "y00"),
            "z01": XOR("axc", "bd"),
            "z02": OR("ef", "ac"),
        }
    )
    return Adder(circuit)


def test_encode_operand(adder_2bits):
    expected = {"x00": 1, "x01": 1, "y00": 0, "y01": 0}
    adder_2bits.load_operand("x", 3)
    adder_2bits.load_operand("y", 0)
    actual = adder_2bits.circuit.values
    assert expected == actual


@pytest.mark.parametrize(
    "left,right",
    it.product(range(4), range(4))
)
def test_adder_2bits(left, right, adder_2bits):
    expected = left + right
    actual = adder_2bits.add(left, right)
    assert expected == actual
