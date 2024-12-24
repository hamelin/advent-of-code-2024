from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
import numpy as np
import re
from textwrap import dedent
from typing import Self


Edge = tuple[str, str]
Clique3 = tuple[str, str, str]
Clique = tuple[str, ...]


@dataclass
class Network:
    connections: dict[str, set[str]]

    @classmethod
    def parse(cls, text: str) -> Self:
        connections = {}
        for line_ in text.split("\n"):
            line = line_.strip()
            if line:
                vertices = line.split("-")
                assert len(vertices) == 2
                for left, right in [vertices, vertices[-1::-1]]:
                    connections.setdefault(left, set()).add(right)
        return cls(connections=connections)

    def iter_edges(self) -> Iterator[Edge]:
        for left, rights in self.connections.items():
            for right in rights:
                if left < right:
                    yield (left, right)

    def iter_cliques3(self) -> Iterator[Clique3]:
        for a, b in self.iter_edges():
            assert a < b
            connected_both = self.connections[a] & self.connections[b]
            for c in connected_both:
                if b < c:
                    yield (a, b, c)

    def get_largest_cliques(self, tqdm=lambda x: x) -> Clique:
        len_largest = 0
        cliques_largest = set()
        for clique3 in tqdm(self.iter_cliques3()):
            clique = set(clique3)
            for vertex, connected in self.connections.items():
                if clique <= connected:
                    clique.add(vertex)

            clique_finished = tuple(sorted(list(clique)))
            if len(clique_finished) == len_largest:
                cliques_largest.add(clique_finished)
            elif len(clique_finished) > len_largest:
                len_largest = len(clique_finished)
                cliques_largest = {clique_finished}
        return cliques_largest


def iter_cliques3_with_t_computer(network: Network) -> Iterator[Clique3]:
    for clique3 in network.iter_cliques3():
        for computer in clique3:
            if computer.startswith("t"):
                yield clique3
                break
