import json
from pathlib import Path
import sys
from tqdm.auto import tqdm

from . import *  # noqa


INPUT = """\
540A
582A
169A
593A
579A
"""


def find_best_plan_robot():
    num_keys = len(KEYPAD_ROBOT.buttons)
    plan = {}
    for i_src, src in enumerate(sorted(KEYPAD_ROBOT.buttons)):
        for i_dest, dest in enumerate(sorted(KEYPAD_ROBOT.buttons)):
            pair = f"{src}{dest}"
            print(f"Pair: [{src}] ({i_src + 1}/{num_keys}) -> [{dest}] ({i_dest + 1}/{num_keys})")  # noqa
            solutions = sorted(KEYPAD_ROBOT.iter_solutions_best(dest, start=src))
            assert solutions
            if len(solutions) == 1:
                plan[pair] = solutions[0]
            else:
                print(f"    Must break cost tie between candidates: {', '.join(solutions)}")  # noqa
                candidates = {sol: {sol} for sol in solutions}
                while len(candidates) > 1:
                    for sol in list(candidates.keys()):
                        bag_new = set()
                        for c in tqdm(candidates[sol], desc=f"        {sol}"):
                            bag_new |= set(KEYPAD_ROBOT.iter_solutions_best(c))
                        candidates[sol] = bag_new
                    len_shortest = min(
                        min((len(c) for c in bag))
                        for bag in candidates.values()
                    )

                    candidates_new = {}
                    for sol, bag in candidates.items():
                        bag_distilled = {c for c in bag if len(c) == len_shortest}
                        if bag_distilled:
                            candidates_new[sol] = bag_distilled
                    candidates = candidates_new
                    print(
                        f"    Candidates that yield gesture strings of "
                        f"length {len_shortest}: {', '.join(candidates.keys())}"
                    )
                winner, _ = candidates.popitem()
                print(f"    Winner: {winner}")
                plan[pair] = winner
    return plan


def find_best_plan_door():
    plan_robot = get_plan("robot")
    num_keys = len(KEYPAD_DOOR.buttons)
    plan_door = {}
    for i_src, src in enumerate(sorted(KEYPAD_DOOR.buttons)):
        for i_dest, dest in enumerate(sorted(KEYPAD_DOOR.buttons)):
            pair = f"{src}{dest}"
            print(f"Pair: [{src}] ({i_src + 1}/{num_keys}) -> [{dest}] ({i_dest + 1}/{num_keys})")
            solutions = sorted(KEYPAD_DOOR.iter_solutions_best(dest, start=src))
            assert solutions
            if len(solutions) == 1:
                plan_door[pair] = solutions[0]
            else:
                print(f"    Must break cost tie between candidates: {', '.join(solutions)}")
                candidates = {sol: Summary.from_keys(sol) for sol in solutions}
                while len(candidates) > 1:
                    for sol in list(candidates.keys()):
                        candidates[sol] = candidates[sol].expand(plan_robot)

                    len_shortest = min(len(summary) for summary in candidates.values())
                    candidates_new = {
                        sol: summary
                        for sol, summary in candidates.items()
                        if len(summary) == len_shortest
                    }
                    candidates = candidates_new
                    print(
                        f"    Candidates that yield gesture strings of "
                        f"length {len_shortest}: {', '.join(candidates.keys())}"
                    )
                winner, _ = candidates.popitem()
                print(f"    Winner: {winner}")
                plan_door[pair] = winner
    return plan_door


if __name__ == "__main__":
    if sys.argv[1:]:
        dir_module = Path(__file__).parent
        if sys.argv[1] == "robot":
            plan = find_best_plan_robot()
        elif sys.argv[1] == "door":
            plan = find_best_plan_door()
        else:
            print("Bad arguments.")
            sys.exit(1)
        with (dir_module / f"{sys.argv[1]}.json").open(
            mode="w",
            encoding="utf-8"
        ) as file:
            json.dump(plan, file, indent=2)
    else:
        codes = [code for code in INPUT.split() if code]
        print(
            "Sum of the complexities (2 robots):",
            sum(
                complexity_code(code, measure_xss_2robots(code))
                for code in tqdm(codes)
            )
        )
        print(
            "Sum of the complexities (25 robots)",
            sum(
                complexity_code(code, measure_shortest_solution(code, 25))
                for code in tqdm(codes)
            )
        )
