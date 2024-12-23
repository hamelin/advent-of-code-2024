from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
import json
import numpy as np
from pathlib import Path
import re
from typing import Callable, Self


Couple = tuple[int, int]
Position = Couple
Button = str


# @dataclass
# class Move:
#     name: str
#     step: Position


MOVES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
    "A": (0, 0)
}
DIFF2MOVE = {
    (-3, 0): "^^^",
    (-2, 0): "^^",
    (-1, 0): "^",
    (3, 0): "vvv",
    (2, 0): "vv",
    (1, 0): "v",
    (0, -2): "<<",
    (0, -1): "<",
    (0, 2): ">>",
    (0, 1): ">",
    (0, 0): "",
}


def manhattan(p: Position, q: Position) -> int:
    return np.sum(np.abs(np.subtract(p, q)))


def advance(p: Position, move: str) -> Position:
    return tuple(np.add(p, MOVES[move]))


COMBINE_MOVES = {
    ">": {
        "^": lambda h, v: h + v,
        "v": lambda h, v: v + h,
        "": lambda h, v: h,
    },
    "<": {
        "^": lambda h, v: h + v,
        "v": lambda h, v: v + h,
        "": lambda h, v: h,
    },
    "": {
        "^": lambda h, v: v,
        "v": lambda h, v: v,
        "": lambda h, v: "",
    }
}


@dataclass
class KeyPad:
    buttons: dict[str, Position]
    inverse: dict[Position, str] = field(default_factory=dict)

    def init(self) -> Self:
        self.inverse = {v: k for k, v in self.buttons.items()}
        return self

    def min_cost_sequence(self, sequence: str, start: str = "A") -> int:
        seq_with_start = [self.buttons[c] for c in [start, *list(sequence)]]
        dists = [
            manhattan(seq_with_start[i - 1], seq_with_start[i])
            for i in range(1, len(seq_with_start))
        ]
        return sum(dists) + len(sequence)

    def is_move_valid(self, pos: Position, steps: str) -> bool:
        assert pos in self.inverse
        for step in steps:
            pos = advance(pos, step)
            if pos not in self.inverse:
                return False
        return True

    def iter_solutions_best(
        self,
        sequence: str,
        start: str = "A"
    ) -> Iterator[str]:
        if sequence:
            goal = self.buttons[sequence[0]]
            cur = self.buttons[start]
            diff = np.subtract(goal, cur)
            move_vert = DIFF2MOVE[(diff[0], 0)]
            move_horiz = DIFF2MOVE[(0, diff[1])]
            moves = [move_horiz + move_vert]
            vh = move_vert + move_horiz
            if vh != moves[0]:
                moves.append(vh)
            for move_total in moves:
                if self.is_move_valid(cur, move_total):
                    for sol in self.iter_solutions_best(sequence[1:], sequence[0]):
                        yield move_total + "A" + sol
        else:
            yield ""

    def iter_solutions(self, sequence: str, current: str = "A") -> Iterator[str]:
        if sequence:
            pos = self.buttons[current]
            goal = self.buttons[sequence[0]]

            dist_to_button = manhattan(pos, goal)
            if dist_to_button == 0:
                move = "A"
                for solution in self.iter_solutions(sequence[1:], current):
                    yield move + solution
            else:
                for move in MOVES.keys():
                    pos_new = advance(pos, move)
                    if pos_new in self.inverse and (
                        manhattan(pos_new, goal) < dist_to_button
                    ):
                        for solution in self.iter_solutions(
                            sequence,
                            self.inverse[pos_new]
                        ):
                            yield move + solution
        else:
            yield ""

    def get_example_solution_least_twists(
        self,
        sequence: str,
        current: str = "A",
        last_move: str = ""
    ) -> str:
        if sequence:
            pos = self.buttons[current]
            goal = self.buttons[sequence[0]]

            dist_to_goal= manhattan(pos, goal)
            if dist_to_goal== 0:
                return "A" + self.get_example_solution_least_twists(
                    sequence[1:],
                    current,
                    last_move="A"
                )
            else:
                moves_good = set()
                for move in MOVES.keys():
                    pos_new = advance(pos, move)
                    dist_new = manhattan(pos_new, goal)
                    if pos_new in self.inverse and dist_new < dist_to_goal:
                        moves_good.add(move)
                assert moves_good

                if last_move in moves_good:
                    move_chosen = last_move
                else:
                    move_chosen = moves_good.pop()
                pos_next = advance(pos, move_chosen)
                return move_chosen + self.get_example_solution_least_twists(
                    sequence,
                    self.inverse[pos_next],
                    move_chosen
                )
        else:
            return ""


KEYPAD_DOOR = KeyPad(
    buttons={
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
    }
).init()
KEYPAD_ROBOT = KeyPad(
    buttons={
        "^": (0, 1),
        "A": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }
).init()


class Gestures:

    def __init__(self, start: str = "A", buttons: str = KEYPAD_ROBOT.buttons):
        self._d = {
            f"{prior}{posterior}": 0
            for prior in KEYPAD_ROBOT.buttons
            for posterior in KEYPAD_ROBOT.buttons
        }
        self._key_last = start

    def update(self, keys: str, factor: int = 1) -> None:
        if keys:
            keys_from_last = f"{self._key_last}{keys}"
            for i in range(1, len(keys_from_last)):
                self._d[keys_from_last[i - 1:i + 1]] += factor
            self._key_last = keys[-1]

    def __iter__(self) -> Iterator[tuple[str, int]]:
        return iter(self._d.items())


@dataclass
class Summary:
    gestures: Gestures

    @classmethod
    def from_keys(cls, keys: str = "", buttons: str = KEYPAD_ROBOT.buttons) -> Self:
        gestures = Gestures(buttons=buttons)
        gestures.update(keys)
        return cls(gestures)

    def __len__(self) -> int:
        return sum(num for _, num in self.gestures)

    def expand(self, plan: dict[str, str]) -> Self:
        gestures = Gestures()
        for pair, num in self.gestures:
            gestures.update(plan[pair], num)
        return type(self)(gestures)


def find_example_shortest_solution(keypads: Sequence[KeyPad], code: str) -> str:
    if keypads:
        keypad, *remaining = keypads
        return min(
            (
                find_example_shortest_solution(remaining, solution)
                for solution in keypad.iter_solutions_best(code)
            ),
            key=len
        )
    else:
        return code


def find_xss_2robots(code: str) -> str:
    return find_example_shortest_solution(
        [KEYPAD_DOOR, KEYPAD_ROBOT, KEYPAD_ROBOT],
        code
    )


def measure_xss_2robots(code: str) -> str:
    return len(find_xss_2robots(code))


RX_NUMBER = re.compile(r"0*(?P<number>\d+)A")


def get_number_code(code: str) -> int:
    match = RX_NUMBER.match(code)
    assert match
    return int(match.group("number"))


def complexity_code(code: str, len_shortest: str) -> int:
    return len_shortest * get_number_code(code)


def get_plan(name: str) -> dict[str, str]:
    path = Path(__file__).parent / f"{name}.json"
    with path.open(mode="r", encoding="utf-8") as file:
        return json.load(file)


def measure_shortest_solution(code: str, num_robots: int) -> int:
    plan_door = get_plan("door")
    A_code = f"A{code}"
    keys = "".join(
        plan_door[A_code[i - 1:i + 1]]
        for i in range(1, len(A_code))
    )

    summary = Summary.from_keys(keys)
    plan_robot = get_plan("robot")
    for _ in range(num_robots):
        summary = summary.expand(plan_robot)
    return len(summary)
