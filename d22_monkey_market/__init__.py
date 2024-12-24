from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
import numpy as np
import re
import scipy
from textwrap import dedent
from typing import Self


MASK_PRUNE = (1 << 24) - 1


def prune(n: int) -> int:
    return n & MASK_PRUNE


def mix(secret: int, n: int) -> int:
    return secret ^ n


def iter_secrets(seed: int) -> Iterator[int]:
    secret = seed
    yield secret
    while True:
        secret = prune(mix(secret, secret << 6))
        secret = prune(mix(secret, secret >> 5))
        secret = prune(mix(secret, secret << 11))
        yield secret


def nth_secret(seed: int, n: int) -> int:
    for i, secret in enumerate(iter_secrets(seed)):
        if i >= n:
            return secret


def secrets_up_to_nth(seed: int, n: int) -> int:
    for i, secret in enumerate(iter_secrets(seed), start=0):
        if i > n:
            break
        yield secret


# Quintuple = np.ndarray


# def quintuples(seq: Iterator[int]) -> Iterator[Quintuple]:
#     quintuple = []
#     for n in seq:
#         quintuple.append(n)
#         if len(quintuple) > 5:
#             del quintuple[0]
#         if len(quintuple) == 5:
#            yield np.asarray(quintuple, dtype=int)


Change = tuple[int, int, int, int]
ChangeDict = dict[Change, dict[str, int]]


def compile_change_dict(name: str, seed: int, limit: int) -> ChangeDict:
    units = np.array(list(secrets_up_to_nth(seed, limit)), dtype=int) % 10
    assert len(units) == limit + 1
    stream_changes = np.diff(units)
    changes_by_4 = scipy.linalg.hankel(
        stream_changes,
        np.zeros((4,), dtype=int)
    )[:len(units) - 4]
    change_dict = {}
    assert changes_by_4.shape[0] == units[4:].shape[0]
    for change_, cost in zip(changes_by_4, units[4:]):
        change = tuple(change_)
        if change not in change_dict:
            change_dict[change] = {name: cost}
    return change_dict


def add_to_change_dict(accum: ChangeDict, term: ChangeDict) -> None:
    for change, name_cost in term.items():
        accum.setdefault(change, {})
        accum[change].update(name_cost)


def most_profitable_change(change_dict: ChangeDict) -> tuple[Change, int]:
    assert change_dict
    change_best = max(change_dict.keys(), key=lambda k: sum(change_dict[k].values()))
    payoff = sum(change_dict[change_best].values())
    return change_best, payoff
