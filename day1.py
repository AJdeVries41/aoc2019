import math

def fuel_recursive(mass: int) -> int:
    additional_fuel = (mass//3)-2
    if (additional_fuel <= 0):
        return 0
    else:
        return additional_fuel + fuel_recursive(additional_fuel)


def part_one(lines: list[int]) -> int:
    return sum(map(lambda i: (i//3)-2, lines))


def part_two(integer_input):
    return sum(map(fuel_recursive, integer_input))


def day1_main():
    file = open("input/day1.txt")
    lines = file.readlines()
    integer_input = list(map(int ,lines))

    part_one_answer = part_one(integer_input)

    part_two_answer = part_two(integer_input)

    print("part 1 answer", part_one_answer)
    print("part 2 answer", part_two_answer)

