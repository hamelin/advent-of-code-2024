from collections.abc import Iterator, Sequence
from dataclasses import dataclass
import numpy as np
import re
from textwrap import dedent
from typing import Self


def validate_operand(operand: int) -> None:
    if operand < 0 or operand >= 8:
        raise ValueError(f"Wrong operand: {operand}")


RX_COMPUTER = re.compile(
    r"Register A: *(?P<a>\d+)\n"
    r"Register B: *(?P<b>\d+)\n"
    r"Register C: *(?P<c>\d+)\n"
    r"\n"
    r"Program: (?P<code>\d(,\d)*)"
)


@dataclass
class Computer:
    a: int
    b: int
    c: int
    code: list[int]

    @classmethod
    def parse(cls, text: str) -> Self:
        match = RX_COMPUTER.match(dedent(text).strip())
        if not match:
            raise ValueError(f"Invalid computer description")
        return cls(
            a=int(match.group("a")),
            b=int(match.group("b")),
            c=int(match.group("c")),
            code=[int(n) for n in match.group("code").split(",")]
        )

    def literal(self, operand: int) -> int:
        validate_operand(operand)
        return operand

    def combo(self, operand: int) -> int:
        validate_operand(operand)
        match operand:
            case 0 | 1 | 2 | 3:
                return int(operand)
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case 7:
                raise ValueError("Operand 7 should never be used as combo")

    def run(self) -> list[int]:
        ip = self.code[0:]
        output = []
        while ip:
            assert len(ip) >= 2
            instr, operand = ip[:2]
            ip = ip[2:]
            if instr < 0 or instr >= 8:
                raise ValueError(f"Invalid opcode: {instr}")
            match instr:
                case Instruction.adv:
                    self.a = self._bitshift_a_op(operand)
                case Instruction.bxl:
                    self.b = self.b ^ self.literal(operand)
                case Instruction.bst:
                    self.b = self.combo(operand) & 0x7
                case Instruction.jnz:
                    if self.a != 0:
                        ip = self.code[self.literal(operand):]
                case Instruction.bxc:
                    self.b = self.b ^ self.c
                case Instruction.out:
                    output.append(self.combo(operand) & 7)
                case Instruction.bdv:
                    self.b = self._bitshift_a_op(operand)
                case Instruction.cdv:
                    self.c = self._bitshift_a_op(operand)
                case _:
                    raise RuntimeError(
                        f"Why has invalid opcode not been caught earlier?"
                    )
        return output

    def _bitshift_a_op(self, operand: int) -> int:
        op = self.combo(operand)
        if op < 0:
            return self.a << abs(op)
        else:
            return self.a >> op


class Instruction:
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7
