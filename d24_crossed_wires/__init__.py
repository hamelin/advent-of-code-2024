from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass, field
import functools as ft
import numpy as np
import operator as op
import re
from textwrap import dedent
from typing import Callable, Self


Variable = str
Value = int
Operator = Callable[[Value, Value], Value]


OPERATORS = {
    "AND": op.and_,
    "OR": op.or_,
    "XOR": op.xor
}


class CyclicalWiring(Exception):
    pass


@dataclass
class Circuit:
    values: dict[Variable, Value]
    relations: dict[Variable, "Operation"]

    @classmethod
    def parse(cls, text: str) -> Self:
        text_values, text_relations = dedent(text).strip().split("\n\n")
        values = {
            name.strip(): int(value.strip())
            for line in text_values.split("\n")
            for name, value in [line.split(":")]
        }
        relations = {}
        for line in text_relations.split("\n"):
            text_operation, result = line.split("->")
            left, operator, right = text_operation.split()
            assert result.strip() not in relations
            relations[result.strip()] = Operation(
                operator=OPERATORS[operator.strip()],
                left=left.strip(),
                right=right.strip()
            )
        return cls(values=values, relations=relations)

    def evaluate(self, variable: Variable) -> Value:
        if variable in self.values:
            return self.values[variable]
        elif variable in self.relations:
            return self.relations[variable].evaluate(self)
        else:
            raise ValueError(f"Cannot evaluate {variable} now")

    def simulate(self) -> Self:
        variables = self.values.keys() | self.relations.keys()
        while self.values.keys() < variables:
            found_one_new = False
            for result, operation in self.relations.items():
                try:
                    if result not in self.values:
                        self.values[result] = operation.evaluate(self)
                        found_one_new = True
                except ValueError:
                    pass
            if not found_one_new:
                raise CyclicalWiring()
        return self

    def get_output(self) -> int:
        zs = sorted(
            [
                variable
                for variable in self.values.keys()
                if variable.startswith("z")
            ],
            reverse=True
        )
        output = 0
        for z in zs:
            output <<= 1
            output |= self.values[z]
        return output

    @property
    def capacity(self) -> dict[str, int]:
        def num_variables_starting_with(initial: str) -> int:
            return sum(
                1
                for variable in self.values.keys() | self.relations.keys()
                if variable.startswith(initial)
            )

        return {v: num_variables_starting_with(v) for v in ["x", "y", "z"]}


@dataclass
class Operation:
    operator: Operator
    left: Variable
    right: Variable

    def evaluate(self, circuit: Circuit) -> Value:
        if missing := [
            operand
            for operand in [self.left, self.right]
            if operand not in circuit.values
        ]:
            raise ValueError(f"Missing operands: {', '.join(missing)}")
        return self.operator(circuit.values[self.left], circuit.values[self.right])


def AND(left, right):
    return Operation(op.and_, left, right)


def OR(left, right):
    return Operation(op.or_, left, right)


def XOR(left, right):
    return Operation(op.xor, left, right)


@dataclass
class Adder:
    circuit: Circuit

    @property
    def variables(self) -> list[Variable]:
        return list(self.circuit.values.keys())

    @property
    def wires(self) -> list[Variable]:
        return sorted(list(self.circuit.relations.keys()))

    def swap_wires(self, left: Variable, right: Variable) -> None:
        self.circuit.relations[left], self.circuit.relations[right] = (
            self.circuit.relations[right], self.circuit.relations[left]
        )

    @contextmanager
    def trying_swap_wires(self, left: Variable, right: Variable) -> Iterator[Self]:
        orig = deepcopy(self)
        try:
            self.swap_wires(left, right)
            yield self
        finally:
            self.swap_wires(left, right)
            assert self.circuit.relations == orig.circuit.relations

    def reset(self) -> Self:
        for variable in self.variables:
            if variable[0] in "xy":
                self.circuit.values[variable] = 0
            else:
                del self.circuit.values[variable]

    def load_operand(self, initial: str, value: int) -> None:
        assert initial in "xy"
        for variable in self.variables:
            if variable.startswith(initial):
                self.circuit.values[variable] = 0
        i = 0
        while value != 0:
            self.circuit.values[f"{initial}{i:02d}"] = value & 0x1
            i += 1
            value >>= 1

    def add(self, left: int, right: int) -> int:
        self.reset()
        self.load_operand("x", left)
        self.load_operand("y", right)
        self.circuit.simulate()
        return self.circuit.get_output()
