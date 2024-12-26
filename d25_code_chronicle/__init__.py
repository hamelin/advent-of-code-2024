from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
import numpy as np
import re
from textwrap import dedent
from typing import Self


Tuple5 = tuple[int, int, int, int, int]
Lock = Tuple5
Key = Tuple5


CH = {".": 0, "#": 1}


@dataclass
class Puzzle:
    height: int
    locks: set[Lock]
    keys: set[Lock]

    @classmethod
    def parse(cls, text: str) -> Self:
        height = 0
        locks = set()
        keys = set()
        for i, schematic in enumerate(dedent(text).strip().split("\n\n")):
            lines = schematic.strip().split("\n")
            if not height:
                height = len(lines)
            else:
                assert len(lines) == height

            if lines[0] == "#####":
                category = locks
            elif lines[-1] == "#####":
                category = keys
                lines = lines[-1::-1]
            else:
                raise ValueError(
                    f"Schematics {i + 1} are not formatted to expectations"
                )

            obj = np.zeros((5,), dtype=int)
            for line in lines:
                obj += np.array([CH[c] for c in line], dtype=int)
            category.add(tuple(obj))

        return cls(height=height, locks=locks, keys=keys)

    def does_key_fit_lock(self, key: Key, lock: Lock) -> bool:
        total = np.add(key, lock)
        return np.all(total <= self.height)

    def count_fits(self) -> int:
        return sum(
            1
            for key in self.keys
            for lock in self.locks
            if self.does_key_fit_lock(key, lock)
        )
