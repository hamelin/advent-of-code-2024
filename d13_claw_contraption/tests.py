import pytest

from . import ClawMachine, assess_cost, parse_machines


@pytest.fixture
def claw_machines_and_solutions():
    return [
        (ClawMachine(a=a, b=b, prize=prize), solution, cost)
        for a, b, prize, solution, cost in [
            ([94, 34], [22, 67], [8400, 5400], [80, 40], 280),
            ([26, 66], [67, 21], [12748, 12176], None, 0),
            ([17, 86], [84, 37], [7870, 6450], [38, 86], 200),
            ([69, 23], [27, 71], [18641, 10279], None, 0)
        ]
    ]


@pytest.mark.parametrize("index", [0, 1, 2, 3])
def test_solve(index, claw_machines_and_solutions):
    claw_machine, solution_expected, *_ = claw_machines_and_solutions[index]
    solution_actual = claw_machine.solve()
    assert solution_expected == (
        None
        if solution_actual is None
        else list(solution_actual)
    )


@pytest.mark.parametrize("index", [0, 1, 2, 3])
def test_cost_tokens(index, claw_machines_and_solutions):
    claw_machine, _, cost_expected = claw_machines_and_solutions[index]
    assert cost_expected == assess_cost(claw_machine)


@pytest.fixture
def text():
    return """\
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400

        Button A: X+26, Y+66
        Button B: X+67, Y+21
        Prize: X=12748, Y=12176

        Button A: X+17, Y+86
        Button B: X+84, Y+37
        Prize: X=7870, Y=6450

        Button A: X+69, Y+23
        Button B: X+27, Y+71
        Prize: X=18641, Y=10279
    """


def test_parse_machines(text, claw_machines_and_solutions):
    assert [cm for cm, *_ in claw_machines_and_solutions] == list(parse_machines(text))


def test_solve_machine_rounding():
    assert [12, 27] == list(
        ClawMachine(a=[30, 84], b=[74, 60], prize=[2358, 2628]).solve()
    )


@pytest.fixture
def machines_post_correction(claw_machines_and_solutions):
    return [
        (ClawMachine(a=cm.a, b=cm.b, prize=prize), has_solution)
        for cm, (prize, has_solution) in zip(
            (cm for cm, *_ in claw_machines_and_solutions),
            [
                ([10000000008400, 10000000005400], False),
                ([10000000012748, 10000000012176], True),
                ([10000000007870, 10000000006450], False),
                ([10000000018641, 10000000010279], True),
            ]
        )
    ]


@pytest.mark.parametrize("index", [0, 1, 2, 3])
def test_machines_having_solution(index, machines_post_correction):
    machine, expected = machines_post_correction[index]
    solution = machine.solve()
    print(solution, machine.solve_real())
    assert expected == (False if solution is None else True)


def test_parse_machines_correction(text, machines_post_correction):
    assert [cm for cm, *_ in machines_post_correction] == list(
        parse_machines(text, correction_prize=10000000000000)
    )
