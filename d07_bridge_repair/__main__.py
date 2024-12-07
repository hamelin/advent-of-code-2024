from tqdm.auto import tqdm
from . import (
    AM,
    AMC,
    INPUT,
    parse_equations,
    sum_results_equations_computing,
)


if __name__ == "__main__":
    equations = parse_equations(INPUT)
    print(
        "Sum of results of computing equations (AM):",
        sum_results_equations_computing(equations, AM, tqdm)
    )
    print(
        "Sum of results of computing equations (AM):",
        sum_results_equations_computing(equations, AMC, tqdm)
    )
