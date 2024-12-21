from collections.abc import Iterator
from dataclasses import dataclass, field
import heapq
from textwrap import dedent
from typing import Self


Color = str
Towel = str
Design = str


@dataclass
class Onsen:
    towels: list[Towel]
    designs: list[Design]
    prefixes: dict[str, set[Design]] = field(default_factory=dict)
    impossibles: set[Design] = field(default_factory=set)

    @classmethod
    def parse(cls, text: str) -> Self:
        text_towels, text_designs = dedent(text).strip().split("\n\n")
        towels = [
            t.strip()
            for t in text_towels.strip().split(",")
        ]
        designs = [
            d.strip()
            for d in text_designs.strip().split("\n")
        ]
        return cls(towels=towels, designs=designs)

    def _is_impossible(self, s: str) -> bool:
        coverage = set()
        for towel in self.towels:
            i = 0
            while True:
                try:
                    found = s.index(towel, i)
                    coverage |= {found + j for j in range(len(towel))}
                    i = found + len(towel)
                except ValueError:
                    break
        return coverage != set(range(len(s)))

    def init(self) -> Self:
        self.impossibles = set()
        for design in self.designs:
            if self._is_impossible(design):
                self.impossibles.add(design)

        self.prefixes = {}
        for design in self.designs:
            if design not in self.impossibles:
                for i in range(1, len(design) + 1):
                    self.prefixes.setdefault(design[:i], set()).add(design)
        return self

    def iter_designs_possible(self, tqdm=lambda x, *_, **__: x) -> Iterator[Design]:
        if not self.prefixes:
            self.init()

        undiscovered = set(self.designs) - self.impossibles
        prefixes = [(len(undiscovered), "")]
        seen = set()
        heapq.heapify(prefixes)

        def importance_prefix(p: str) -> int:
            return -len(self.prefixes[p] & undiscovered) * len(p)

        while prefixes:
            _, prefix = heapq.heappop(prefixes)
            made_discovery = False
            for towel in self.towels:
                longer = prefix + towel
                if designs := self.prefixes.get(longer) or set():
                    if longer in designs:
                        if longer in undiscovered:
                            yield longer
                            undiscovered.remove(longer)
                            made_discovery = True
                    else:
                        if longer not in seen and any(
                            design
                            for design in designs & undiscovered
                            if not self._is_impossible(design[len(longer):])
                        ):
                            seen.add(longer)
                            heapq.heappush(
                                prefixes,
                                (importance_prefix(longer), longer)
                            )

            if made_discovery:
                prefixes = [(importance_prefix(p), p) for _, p in prefixes]
                heapq.heapify(prefixes)

    def count_designs_possible(self) -> int:
        return sum(1 for _ in self.iter_designs_possible())

    def count_arrangements_design(self, design: Design) -> int:
        if not self.prefixes:
            self.init()
        if design in self.impossibles:
            return 0

        prefixes = [""]
        heapq.heapify(prefixes)
        sources = {}
        while prefixes:
            prefix = heapq.heappop(prefixes)
            for towel in self.towels:
                longer = prefix + towel
                if design.startswith(longer):
                    if longer in sources:
                        sources[longer].append(prefix)
                    else:
                        sources[longer] = [prefix]
                        if not self._is_impossible(design[len(prefix):]):
                            heapq.heappush(prefixes, longer)

        num_to_destination = {}
        for destination in sorted(sources.keys()):
            num_to_destination[destination] = sum(
                num_to_destination[source] if source else 1
                for source in sources[destination]
            )
        return num_to_destination[design]
