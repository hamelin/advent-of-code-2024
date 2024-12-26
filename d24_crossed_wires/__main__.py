from collections.abc import Iterable
from copy import deepcopy
import itertools as it
import joblib as jl
import json
import math
from pathlib import Path
from tqdm.auto import tqdm, trange

from . import *  # noqa


Pair = tuple[int, int]
Wire = str
Swap = tuple[Wire, Wire]


@dataclass
class Potential:
    swaps: tuple[Swap, Swap, Swap, Swap]

    @classmethod
    def from_combination(cls, combination: Sequence[Swap]) -> Self:
        return tuple(sorted([tuple(sorted(swap)) for swap in combination]))

    def __hash__(self) -> int:
        return hash(self.swaps)


def run_totals(adder: Adder, pairs: Iterator[Pair]) -> Iterator[Pair]:
    for left, right in pairs:
        expected = left + right
        obtained = adder.add(left, right)
        if expected != obtained:
            yield (left, right)


def sweep_bits(num_bits: int, shift: int, capacity: int) -> Iterator[Pair]:
    if shift + num_bits > capacity:
        num_bits = capacity - shift
    bound = 1 << num_bits
    for left in range(bound):
        for right in range(bound):
            yield (left << shift, right << shift)


def wires_from_swap(swaps: Iterable[Swap]) -> list[Wire]:
    return sum(
        (list(swap) for swap in swaps),
        []
    )


def sweep_wire_swaps(
    adder: Adder,
    shift: int,
    num_bits: int,
    capacity: int
) -> dict[str, list[Swap]]:
    group_bits = ",".join(str(n) for n in range(shift, shift + num_bits))
    swaps = []
    errors = set(run_totals(adder, sweep_bits(num_bits, shift, capacity)))
    if errors:
        print(f"Found {len(errors)} errors for bits {group_bits}: will experiment swaps")
        for i, blue in enumerate(adder.wires):
            for red in adder.wires[i + 1:]:
                try:
                    assert blue != red
                    with adder.trying_swap_wires(blue, red) as adder_:
                        errors_new = set(run_totals(adder_, iter(errors)))
                        if errors_new < errors:
                            swaps.append([blue, red])
                except CyclicalWiring:
                    pass

    if swaps:
        return {group_bits: swaps}
    return {}


class FoundError(Exception):
    pass


INPUT = """\
x00: 1
x01: 1
x02: 1
x03: 1
x04: 0
x05: 1
x06: 0
x07: 1
x08: 0
x09: 1
x10: 1
x11: 1
x12: 1
x13: 0
x14: 1
x15: 1
x16: 1
x17: 1
x18: 0
x19: 1
x20: 0
x21: 1
x22: 0
x23: 1
x24: 1
x25: 0
x26: 1
x27: 1
x28: 0
x29: 0
x30: 0
x31: 0
x32: 0
x33: 1
x34: 0
x35: 0
x36: 1
x37: 1
x38: 0
x39: 1
x40: 1
x41: 0
x42: 1
x43: 0
x44: 1
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1
y05: 0
y06: 0
y07: 0
y08: 0
y09: 0
y10: 1
y11: 0
y12: 0
y13: 0
y14: 1
y15: 0
y16: 0
y17: 1
y18: 1
y19: 1
y20: 0
y21: 0
y22: 1
y23: 0
y24: 1
y25: 1
y26: 1
y27: 1
y28: 1
y29: 1
y30: 0
y31: 1
y32: 1
y33: 0
y34: 0
y35: 0
y36: 1
y37: 0
y38: 0
y39: 0
y40: 0
y41: 0
y42: 1
y43: 0
y44: 1

vgh OR dhk -> kfp
qpb OR tdt -> z45
njd XOR hwt -> z33
y38 AND x38 -> srk
y25 AND x25 -> sth
jrw OR tmm -> htw
qkn AND dvc -> kff
x08 AND y08 -> kmm
dcj AND wrr -> jkm
mmc XOR mdv -> z05
x35 AND y35 -> vss
x14 AND y14 -> nvj
fks OR mgs -> fww
jnh OR njq -> z24
mfk XOR pwh -> z12
rbc OR kgg -> jqw
cbm OR jjn -> nfn
x30 AND y30 -> fqm
x18 AND y18 -> kgg
x23 XOR y23 -> smg
y36 XOR x36 -> sfh
kvb AND fhp -> dhk
y24 AND x24 -> njq
x20 AND y20 -> hkt
x36 AND y36 -> dcq
y17 AND x17 -> wvs
y09 XOR x09 -> wpr
tjp OR tdk -> trq
gkq XOR qbf -> z08
fmw AND ffk -> twt
y38 XOR x38 -> ccw
vss OR nkn -> bbq
x02 AND y02 -> rfb
wwj OR pjn -> njd
csn XOR jqw -> z19
y06 XOR x06 -> fwp
tms AND wbm -> nkn
tff AND nbm -> jgd
y13 AND x13 -> vgh
y19 AND x19 -> dwn
nfn AND nsk -> jwb
smg XOR hrk -> z23
kkp AND tnm -> jnh
x03 AND y03 -> tjp
qbf AND gkq -> thk
x16 AND y16 -> gjg
mfk AND pwh -> wpw
y06 AND x06 -> jdp
x22 AND y22 -> cnp
bwv OR fwb -> mpd
mpd AND wnw -> hmk
y21 XOR x21 -> hvt
fmd XOR qcw -> z26
tcs XOR hwg -> z10
fwp AND fww -> qjk
x29 AND y29 -> nfp
cmj AND htw -> fpt
x10 AND y10 -> psb
mkr OR tqp -> fhf
bqn XOR kmr -> z15
qkq AND stj -> z20
cnp OR dbc -> hrk
vcg AND qgb -> rss
bqs OR qnq -> qbf
sth OR rss -> qcw
sfh AND bbq -> stg
stj XOR qkq -> jgb
wsq OR wvs -> hrn
y05 XOR x05 -> mdv
y27 XOR x27 -> wnw
nsm XOR mfq -> z32
njd AND hwt -> ppm
csn AND jqw -> skp
y39 AND x39 -> bnj
rkf OR hvk -> tcs
y41 XOR x41 -> nsk
hmk OR tqj -> tff
hrn XOR pfb -> z18
x32 XOR y32 -> mfq
wmj AND djn -> gsj
tnm XOR kkp -> vcg
x00 AND y00 -> mjh
srk OR rtf -> rsg
x04 XOR y04 -> hcs
y33 AND x33 -> fjr
y27 AND x27 -> tqj
psb OR pjf -> whj
jnn AND wpr -> hvk
y42 XOR x42 -> dvc
x18 XOR y18 -> pfb
x25 XOR y25 -> qgb
x03 XOR y03 -> csd
y40 XOR x40 -> qbn
kbq AND csd -> tdk
rdj AND mjh -> tqp
fhp XOR kvb -> z13
y10 XOR x10 -> hwg
x01 AND y01 -> mkr
vpc OR mqg -> wbm
csf XOR rrs -> z31
wmj XOR djn -> z37
mpd XOR wnw -> z27
fwg XOR rvj -> z07
csd XOR kbq -> z03
dwn OR skp -> stj
vfd XOR pjw -> z44
psg OR jgd -> dcj
x15 XOR y15 -> kmr
nbm XOR tff -> z28
x07 XOR y07 -> rvj
rsp AND fsf -> wsq
x16 XOR y16 -> cmj
y05 AND x05 -> mgs
y11 XOR x11 -> bcw
y40 AND x40 -> cbm
bvn OR jwb -> qkn
tkv AND npv -> wkn
grc OR jwd -> mmc
ffk XOR fmw -> z30
ghk OR grb -> pwh
x30 XOR y30 -> fmw
ppm OR fjr -> fsn
khg OR wkn -> pjw
x17 XOR y17 -> fsf
y44 XOR x44 -> vfd
x13 XOR y13 -> fhp
y28 AND x28 -> psg
pcp OR kff -> tkv
bhs XOR fsn -> z34
dvc XOR qkn -> z42
pst AND qbn -> jjn
bcw XOR whj -> z11
kmr AND bqn -> jrw
pfb AND hrn -> rbc
x37 XOR y37 -> djn
x31 AND y31 -> rrs
csf AND rrs -> pgq
tms XOR wbm -> z35
khb AND qtq -> dbc
fsn AND bhs -> vpc
y14 XOR x14 -> rvd
x22 XOR y22 -> khb
rdj XOR mjh -> z01
hvt AND bfp -> shc
rfb OR qtr -> kbq
y26 AND x26 -> bwv
y37 AND x37 -> trf
x12 AND y12 -> qcg
x23 AND y23 -> knh
qcg OR wpw -> kvb
gsj OR trf -> wqq
fmd AND qcw -> fwb
x41 AND y41 -> bvn
nsk XOR nfn -> z41
rvc OR pgq -> nsm
y32 AND x32 -> pjn
vfd AND pjw -> qpb
mfq AND nsm -> wwj
cmj XOR htw -> z16
jkm OR nfp -> ffk
x42 AND y42 -> pcp
fsf XOR rsp -> z17
rvj AND fwg -> bqs
y28 XOR x28 -> nbm
tcs AND hwg -> pjf
x08 XOR y08 -> gkq
qgb XOR vcg -> z25
hcs XOR trq -> z04
jgb OR hkt -> bfp
rvd XOR kfp -> z14
wqq AND ccw -> rtf
y20 XOR x20 -> qkq
kfp AND rvd -> qmp
x04 AND y04 -> grc
qbn XOR pst -> z40
fqm OR twt -> csf
khb XOR qtq -> z22
y00 XOR x00 -> z00
y34 AND x34 -> mqg
x11 AND y11 -> grb
y34 XOR x34 -> bhs
y09 AND x09 -> z09
hrk AND smg -> vvb
x12 XOR y12 -> mfk
gjg OR fpt -> rsp
y39 XOR x39 -> hkr
x31 XOR y31 -> rvc
kmm OR thk -> jnn
rsg XOR hkr -> z39
fht XOR fhf -> z02
hkr AND rsg -> mhh
bfp XOR hvt -> z21
shc OR nvr -> qtq
y01 XOR x01 -> rdj
trq AND hcs -> jwd
y07 AND x07 -> qnq
qmp OR nvj -> bqn
x29 XOR y29 -> wrr
y33 XOR x33 -> hwt
x19 XOR y19 -> csn
whj AND bcw -> ghk
y24 XOR x24 -> tnm
dcq OR stg -> wmj
tkv XOR npv -> z43
mhh OR bnj -> pst
mmc AND mdv -> fks
x02 XOR y02 -> fht
y44 AND x44 -> tdt
x43 AND y43 -> khg
jnn XOR wpr -> rkf
knh OR vvb -> kkp
y15 AND x15 -> tmm
x35 XOR y35 -> tms
fht AND fhf -> qtr
dcj XOR wrr -> z29
fww XOR fwp -> z06
y21 AND x21 -> nvr
y43 XOR x43 -> npv
sfh XOR bbq -> z36
qjk OR jdp -> fwg
y26 XOR x26 -> fmd
wqq XOR ccw -> z38
"""


if __name__ == "__main__":
    circuit = Circuit.parse(INPUT).simulate()
    print(
        "Circuit output",
        circuit.get_output()
    )
    capacity = circuit.capacity
    print(
        "Binary capacity:",
        capacity
    )

    assert capacity["x"] == capacity["y"]
    adder = Adder(circuit)
    ORIG = deepcopy(adder)
    num_bits = 2
    path_subproblems = Path(__file__).parent / "subproblems.json"
    if path_subproblems.is_file():
        print("Fetch cached subproblems")
        with path_subproblems.open(mode="r", encoding="utf-8") as file:
            subproblems = json.load(file)
    else:
        print("Enumerate subproblems")
        subproblems: dict[str, list[Swap]] = {}
        for sprob in jl.Parallel(n_jobs=-1)(
            jl.delayed(sweep_wire_swaps)(adder, shift, num_bits, capacity["x"])
            for shift in range(0, capacity["x"], num_bits)
        ):
            if sprob:
                assert all(sprob.values())
                subproblems.update(sprob)
        with path_subproblems.open(mode="w", encoding="utf-8") as file:
            json.dump(subproblems, file)

    groups_bits = [
        (min(bits), len(bits))
        for k in subproblems.keys()
        for bits in [[int(n) for n in k.split(",")]]
    ]
    swaps = sum(subproblems.values(), [])
    num_combinations = math.comb(len(swaps), 4)
    print(f"Got {len(swaps)} swaps, thus {num_combinations} potential wire swap combinations to explore")
    solutions = []
    for combination in tqdm(it.combinations(swaps, 4), total=num_combinations):
        # assert adder.circuit.relations == ORIG.circuit.relations
        adder = Adder(Circuit.parse(INPUT))

        # Check that no wire is involved in more than one swap.
        wires_involved = sum(combination, [])
        wires_unique = set(wires_involved)
        if len(wires_involved) > len(wires_unique):
            continue

        try:
            for swap in combination:
                adder.swap_wires(*swap)

            for shift, num_bits in groups_bits:
                for _error in run_totals(
                    adder,
                    sweep_bits(num_bits, shift, capacity["x"])
                ):
                    raise FoundError()

            for shift in range(0, capacity["x"], num_bits):
                for _error in run_totals(
                    adder,
                    sweep_bits(num_bits, shift, capacity["x"])
                ):
                    raise FoundError()

            solutions.append([list(swap) for swap in combination])
        except FoundError:
            pass
        except CyclicalWiring:
            pass

    if solutions:
        for i, solution in enumerate(solutions, start=1):
            print(f"Solution {i}")
            print(f"    Swaps: {solution}")
            print(f"    Wires: {','.join(sorted(sum(solution, [])))}")
    else:
        print("No winner for you bud. Back to the drawing board.")