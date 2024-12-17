from . import *  # noqa


INPUT = """\
Register A: 25986278
Register B: 0
Register C: 0

Program: 2,4,1,4,7,5,4,1,1,4,5,5,0,3,3,0
"""


def create_self_output(program: list[int], a: int, indent: int = 0) -> int:
    spaces = " " * indent
    if not program:
        print(f"{spaces}Found a proper a: {a}")
        return a

    *prefix, out = program
    print(f"{spaces}a = {a} | To output {out} | Remains {prefix}")
    for tryte in range(1 if a == 0 else 0, 8):
        a_ = (a << 3) | tryte
        r = a_ >> (tryte ^ 4)
        if ((tryte ^ r) & 7) == out:
            print(f"{spaces}Tryte {tryte} fits")
            if seed := create_self_output(prefix, a_, indent + 4):
                return seed

    print(f"{spaces}This set of hypotheses has failed; backing off")
    return 0

if __name__ == "__main__":
    computer = Computer.parse(INPUT)
    print(
        "Outputs:",
        ",".join([str(n) for n in computer.run()])
    )

    a_output_program = create_self_output(computer.code, 0)
    assert Computer(
        a=a_output_program,
        b=0,
        c=0,
        code=computer.code
    ).run() == computer.code
    print("Value of a that spits program back out:", a_output_program)
