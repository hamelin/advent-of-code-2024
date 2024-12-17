import pytest

from . import *  # noqa


@pytest.fixture
def operand_tester():
    return Computer(a=77, b=88, c=99, code=[])


@pytest.mark.parametrize(
    "value",
    list(range(8))
)
def test_literal(value, operand_tester):
    assert value == operand_tester.literal(value)


@pytest.mark.parametrize(
    "operand,expected",
    [(n, n) for n in range(4)] + [(4, 77), (5, 88), (6, 99)]
)
def test_combo(expected, operand, operand_tester):
    assert expected == operand_tester.combo(operand)


def test_combo_operand_illegal(operand_tester):
    with pytest.raises(ValueError):
        operand_tester.combo(7)


@pytest.mark.parametrize(
    "instr,operand,a_init,b_init,c_init,a_final,b_final,c_final,output",
    [
        (Instruction.adv, 0, 0xff, 5, -2, 0xff, 5, -2, []),
        (Instruction.adv, 1, 0xff, 5, -2, 0x7f, 5, -2, []),
        (Instruction.adv, 2, 0xff, 5, -2, 0x3f, 5, -2, []),
        (Instruction.adv, 3, 0xff, 5, -2, 0x1f, 5, -2, []),
        (Instruction.adv, 4, 0xff, 5, -2,   0,  5, -2, []),
        (Instruction.adv, 5, 0xff, 5, -2,   7,  5, -2, []),
        (Instruction.adv, 6, 0xff, 5, -2, 0x3fc, 5, -2, []),
        (Instruction.bxl, 0, 77, 0xff, 99, 77, 0xff, 99, []),
        (Instruction.bxl, 1, 77, 0xff, 99, 77, 0xfe, 99, []),
        (Instruction.bxl, 2, 77, 0xff, 99, 77, 0xfd, 99, []),
        (Instruction.bxl, 3, 77, 0xff, 99, 77, 0xfc, 99, []),
        (Instruction.bxl, 4, 77, 0xff, 99, 77, 0xfb, 99, []),
        (Instruction.bxl, 5, 77, 0xff, 99, 77, 0xfa, 99, []),
        (Instruction.bxl, 6, 77, 0xff, 99, 77, 0xf9, 99, []),
        (Instruction.bxl, 7, 77, 0xff, 99, 77, 0xf8, 99, []),
        (Instruction.bst, 0, 77, 89, 99, 77, 0, 99, []),
        (Instruction.bst, 1, 77, 89, 99, 77, 1, 99, []),
        (Instruction.bst, 2, 77, 89, 99, 77, 2, 99, []),
        (Instruction.bst, 3, 77, 89, 99, 77, 3, 99, []),
        (Instruction.bst, 4, 77, 89, 99, 77, 5, 99, []),
        (Instruction.bst, 5, 77, 89, 99, 77, 1, 99, []),
        (Instruction.bst, 6, 77, 89, 99, 77, 3, 99, []),
        (Instruction.bxc, 0, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 1, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 2, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 3, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 4, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 5, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 6, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.bxc, 7, 77, 0xac, 0x53, 77, 0xff, 0x53, []),
        (Instruction.out, 0, 77, 89, 99, 77, 89, 99, [0]),
        (Instruction.out, 1, 77, 89, 99, 77, 89, 99, [1]),
        (Instruction.out, 2, 77, 89, 99, 77, 89, 99, [2]),
        (Instruction.out, 3, 77, 89, 99, 77, 89, 99, [3]),
        (Instruction.out, 4, 77, 89, 99, 77, 89, 99, [5]),
        (Instruction.out, 5, 77, 89, 99, 77, 89, 99, [1]),
        (Instruction.out, 6, 77, 89, 99, 77, 89, 99, [3]),
        (Instruction.bdv, 0, 0xff, 5, -2, 0xff, 0xff, -2, []),
        (Instruction.bdv, 1, 0xff, 5, -2, 0xff, 0x7f, -2, []),
        (Instruction.bdv, 2, 0xff, 5, -2, 0xff, 0x3f, -2, []),
        (Instruction.bdv, 3, 0xff, 5, -2, 0xff, 0x1f, -2, []),
        (Instruction.bdv, 4, 0xff, 5, -2, 0xff,   0,  -2, []),
        (Instruction.bdv, 5, 0xff, 5, -2, 0xff,   7,  -2, []),
        (Instruction.bdv, 6, 0xff, 5, -2, 0xff, 0x3fc, -2, []),
        (Instruction.cdv, 0, 0xff, 5, -2, 0xff, 5, 0xff, []),
        (Instruction.cdv, 1, 0xff, 5, -2, 0xff, 5, 0x7f, []),
        (Instruction.cdv, 2, 0xff, 5, -2, 0xff, 5, 0x3f, []),
        (Instruction.cdv, 3, 0xff, 5, -2, 0xff, 5, 0x1f, []),
        (Instruction.cdv, 4, 0xff, 5, -2, 0xff, 5,   0,  []),
        (Instruction.cdv, 5, 0xff, 5, -2, 0xff, 5,   7,  []),
        (Instruction.cdv, 6, 0xff, 5, -2, 0xff, 5, 0x3fc, []),
    ]
)
def test_single_instruction(
    a_init,
    b_init,
    c_init,
    instr,
    operand,
    a_final,
    b_final,
    c_final,
    output
):
    computer = Computer(a=a_init, b=b_init, c=c_init, code=[instr, operand])
    assert output == computer.run()
    assert Computer(a=a_final, b=b_final, c=c_final, code=computer.code) == computer


@pytest.mark.parametrize("a,expected", [(0, [0, 3]), (1, [3])])
def test_jnz(expected, a):
    output = Computer(
        a=a,
        b=0,
        c=0,
        code=[
            Instruction.jnz, 4,
            Instruction.out, 0,
            Instruction.out, 3,
        ]
    ).run()
    assert expected == output


@pytest.mark.parametrize(
    "computer,registers,output",
    [
        (
            Computer(a=77, b=88, c=9, code=[2, 6]),
            (77, 1, 9),
            []
        ),
        (
            Computer(a=10, b=88, c=99, code=[5, 0, 5, 1, 5, 4]),
            (10, 88, 99),
            [0, 1, 2]
        ),
        (
            Computer(a=2024, b=88, c=99, code=[0, 1, 5, 4, 3, 0]),
            (0, 88, 99),
            [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
        ),
        (
            Computer(a=77, b=29, c=99, code=[1, 7]),
            (77, 26, 99),
            []
        ),
        (
            Computer(a=77, b=2024, c=43690, code=[4, 0]),
            (77, 44354, 43690),
            []
        )
    ]
)
def test_run(registers, output, computer):
    assert output == computer.run()
    assert registers == (computer.a, computer.b, computer.c)


@pytest.fixture
def text():
    return """\
        Register A: 729
        Register B: 0
        Register C: 0

        Program: 0,1,5,4,3,0 
    """


@pytest.fixture
def computer(text):
    return Computer.parse(text)


def test_parse(computer):
    assert Computer(a=729, b=0, c=0, code=[0, 1, 5, 4, 3, 0]) == computer


def test_run_(computer):
    assert [4, 6, 3, 5, 6, 3, 5, 2, 1, 0] == computer.run()
    assert 0 == computer.a
