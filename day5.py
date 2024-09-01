

param_count_per_opcode = {
    99: 0,
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3
}

"""
Return length of a number, i.e. how many digits represent the number
"""
def length(n: int):
    res = 1
    while n >= (10**res):
        res += 1
    return res

"""
Return ith digit of a number, reading left-to-right
"""
def ith_digit(num: int, i: int):
    l = length(num)
    if (i < 0 or i >= l):
        raise ValueError(f"index {i} is out of bounds for number {num}")
    cur_num = num
    division_result = None
    rest = None
    for exp in range(l-1, l-i-2, -1):
        division_result = int(cur_num / (10**exp))
        rest = cur_num % (10**exp)

        cur_num = rest
    return division_result


def extract_opcode(instruction_code):
    l = length(instruction_code)

    # extract last two digits of instruction_code to get opcode
    last_digit = ith_digit(instruction_code, l-1)
    
    if l == 1:
        second_to_last_digit = 0
    else:
        second_to_last_digit = ith_digit(instruction_code, l-2)
    opcode = second_to_last_digit * 10 + last_digit

    return opcode

def extract_opcode_and_parameter_modes(instruction_code):
    """
    instruction_code = opcode including parameter modes to the right
    """
    # get opcode from last 2 digits
    opcode = extract_opcode(instruction_code)

    l = length(instruction_code)

    # extract parameter modes by looping backwards until 0
    parameter_modes = []
    for i in range(l-3, -1, -1):
        parameter_modes.append(ith_digit(instruction_code, i))

    # Append zero to parameter_modes list for any omitted values
    # (this can go wrong if param_count_per_opcode does not contain opcode)
    while len(parameter_modes) < param_count_per_opcode[opcode]:
        parameter_modes.append(0)

    return (opcode, parameter_modes)
    

def read_args(prog: list[int], pc: int, amount: int):
    args = []
    for i in range(1, amount+1):
        args.append(prog[pc + i])
    return args


def to_imm(prog: list[int], parameter: int, parameter_mode: int):
    # Position mode
    if (parameter_mode == 0):
        return prog[parameter]
    # Immediate mode
    else:
        return parameter

def to_imms(prog: list[int], args: list[int], 
                      parameter_modes: list[int]):
    """
    Convert arguments to immediate numbers if they are of position mode
    """
    assert len(args) == len(parameter_modes)
    
    imms = []
    for i in range(0, len(args)):
        imms.append(to_imm(prog, args[i], parameter_modes[i]))
    return imms

    
def interp_intcode(prog: list[int], verb=-1, noun=-1):
    if verb != -1:
        prog[1] = verb
    if noun != -1:
        prog[2] = noun
    interp_intcode_rec(prog, 0)


def interp_intcode_rec(prog: list[int], counter: int):
    # instruction_code = opcode including parameter modes to the left
    instruction_code = prog[counter]
    opcode, parameter_modes = extract_opcode_and_parameter_modes(instruction_code)
    param_count = param_count_per_opcode[opcode]
    args = read_args(prog, counter, param_count)
    # pattern-match on the current opcode
    match opcode:
        # exit
        case 99:
            return
        # add next two arguments and store at final argument
        case 1:
            # we should not convert the 3rd arg (write location) to an immediate
            args_interped = to_imms(prog, args[:2], parameter_modes[:2]) + [args[2]]

            prog[args_interped[2]] = args_interped[0] + args_interped[1]

            next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        # multiply next two arguments and store at final argument
        case 2:
            # we should not convert the 3rd arg (write location) to an immediate
            args_interped = to_imms(prog, args[:2], parameter_modes[:2]) + [args[2]]

            prog[args_interped[2]] = args_interped[0] * args_interped[1]

            next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        # read input from user, write to the address given by the first argument
        case 3:
            input_integer = int(input("Please type an integer: "))
            prog[args[0]] = input_integer
            
            next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        # output the given argument, depending on its parameter
        case 4:
            arg1_interped = to_imm(prog, args[0], parameter_modes[0])

            print(arg1_interped)

            next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        # jump-if-true arg1 arg2
        case 5:
            args_interped = to_imms(prog, args, parameter_modes)

            if args_interped[0] != 0:
                next_pc = args_interped[1]
            else:
                next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        # jump-if-false arg1 arg2
        case 6:
            args_interped = to_imms(prog, args, parameter_modes)

            if args_interped[0] == 0:
                next_pc = args_interped[1]
            else:
                next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        
        # less-than arg1 arg2 arg3
        case 7:
            # we should not convert the 3rd arg (write location) to an immediate
            args_interped = to_imms(prog, args[:2], parameter_modes[:2]) + [args[2]]

            if (args_interped[0] < args_interped[1]):
                prog[args_interped[2]] = 1
            else:
                prog[args_interped[2]] =  0
            
            next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        # == arg1 arg2 arg3
        case 8:
            # we should not convert the 3rd arg (write location) to an immediate
            args_interped = to_imms(prog, args[:2], parameter_modes[:2]) + [args[2]]

            if (args_interped[0] == args_interped[1]):
                prog[args_interped[2]] = 1
            else:
                prog[args_interped[2]] = 0

            next_pc = counter+(param_count + 1)
            interp_intcode_rec(prog, next_pc)
        case _:
            raise ValueError(f"Invalid opcode given: {opcode}")

def read_intcode_input(path):
    program = list(map(int, open(path).readline().split(",")))
    return program 

def main():
    day5_intcode = read_intcode_input("input/day5.txt")
    interp_intcode(day5_intcode)