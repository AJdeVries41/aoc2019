

from copy import copy

"""
It is assumed a valid intcode program is given to this function
"""
def interp_intcode(prog: list[int], verb=-1, noun=-1):
    if verb != -1:
        prog[1] = verb
    if noun != -1:
        prog[2] = noun
    interp_intcode_rec(prog, 0)


def interp_intcode_rec(prog: list[int], counter: int):
    match prog[counter]:
        case 99:
            return
        case 1:
            prog[prog[counter+3]] = prog[prog[counter+1]] + prog[prog[counter+2]]
            interp_intcode_rec(prog, counter+4)
        case 2:
            prog[prog[counter + 3]] = prog[prog[counter + 1]] * prog[prog[counter + 2]]
            interp_intcode_rec(prog, counter + 4)
        case opcode:
            raise ValueError(f"Invalid opcode given: {opcode}")



def part1_answer(prog: list[int]) -> int:
    copied = copy(prog)
    prog[1] = 12
    prog[2] = 2
    interp_intcode(copied, 12, 2)
    return copied[0]


def part2_answer(prog: list[int]) -> int:
    copied = copy(prog)
    desired_output = 19690720
    for verb in range(100):
        for noun in (range(100)):
            interp_intcode(copied, verb, noun)
            if (copied[0] == desired_output):
                return 100*verb+noun
            copied = copy(prog)
    return -1

def day2_main():
    file = open("input/day2.txt")
    gravity_assist_program = list(map(int, file.readline().split(",")))
    part1_answer(gravity_assist_program)
    print("Part 1 answer: ", part1_answer(gravity_assist_program))
    print("Part2 answer: ", part2_answer(gravity_assist_program))

if __name__ == "__main__":
    day2_main()