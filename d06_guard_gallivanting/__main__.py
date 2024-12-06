from tqdm.auto import tqdm
from . import INPUT, Lab


if __name__ == "__main__":
    lab = Lab.parse_map(INPUT)
    print("Number of steps to the guard's exit:", len(set(lab.walk_guard_out())))
    print(
        "Number of positions where a new obstacle would induce the guard to loop:",
        len(set(lab.iter_obstacles_inducing_loop(tqdm)))
    )
