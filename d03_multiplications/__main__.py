from . import INPUT, process_muls, process_muls_cond


if __name__ == "__main__":
    print("Sum of multiplications:", process_muls(INPUT))
    print("Sum of conditional multiplications:", process_muls_cond(INPUT))
