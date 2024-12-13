from collections.abc import Iterator, Sequence
from dataclasses import dataclass
import numpy as np
import re
from textwrap import dedent
from typing import Optional


Solution = Optional[np.ndarray]


@dataclass
class ClawMachine:
    a: Sequence[int]
    b: Sequence[int]
    prize: Sequence[int]

    @property
    def matrix(self) -> np.ndarray:
        return np.transpose([self.a, self.b])

    def solve_real(self) -> np.ndarray:
        return np.linalg.solve(self.matrix, self.prize)

    def solve(self) -> Solution:
        r, s, t, u = self.matrix.ravel()
        determinant = r * u - s * t
        if determinant == 0:
            return None
        sol_rem = [
            divmod(divid, determinant)
            for divid in [
                u * self.prize[0] - s * self.prize[1],
                r * self.prize[1] - t * self.prize[0],
            ]
        ]
        if any(rem != 0 for _, rem in sol_rem):
            return None
        return np.array([sol for sol, _ in sol_rem])


def assess_cost(cm: ClawMachine) -> int:
    solution = cm.solve()
    if solution is None:
        return 0
    return solution @ [3, 1]


RX_MACHINE = re.compile(
    r"Button A: X\+(?P<ax>\d+), Y\+(?P<ay>\d+)\n"
    r"Button B: X\+(?P<bx>\d+), Y\+(?P<by>\d+)\n"
    r"Prize: X=(?P<prizex>\d+), Y=(?P<prizey>\d+)"
)


def parse_machines(desc: str, correction_prize: int = 0) -> Iterator[ClawMachine]:
    desc = dedent(desc).strip()
    while desc:
        if not (match := RX_MACHINE.match(desc)):
            raise ValueError(
                f"Parse error at desc=[{desc[:128]}{'...' if len(desc) > 128 else ''}]"
            )

        def params_machine(*groups: str) -> list[int]:
            return [int(match.group(g)) for g in groups]

        yield ClawMachine(
            a=params_machine("ax", "ay"),
            b=params_machine("bx", "by"),
            prize=list(
                np.add(params_machine("prizex", "prizey"), correction_prize)
            )
        )
        assert 0 == match.start()
        desc = desc[match.end():].strip()
