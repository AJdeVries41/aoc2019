

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
    if (i >= l):
        raise ValueError(f"index {i} is out of bounds for number {num}")
    cur_num = num
    division_result = None
    rest = None
    for exp in range(l-1, l-i-2, -1):
        division_result = int(cur_num / (10**exp))
        rest = cur_num % (10**exp)

        cur_num = rest
    return division_result

"""
Returns true if a candidate number satisfies the part1 criteria, else false
Criterium 1: two adjacent digits must be the same
Criterium 2: numbers are non-decreasing going left-to-right
"""
def meets_part1_criteria(num: int):
    l = length(num)
    two_adjacent_digits_equal = False
    prev_digit = -1
    for i in range(0, l):
        cur_digit = ith_digit(num, i)
        # Criterium 1
        if (cur_digit == prev_digit):
            two_adjacent_digits_equal = True
        # Criterium 2 
        if (cur_digit < prev_digit):
            return False 
        prev_digit = cur_digit
    return two_adjacent_digits_equal



def part2_criterium_1(prev_digits, cur_digit):
    # The condition is satisfied if the current_digit is greater than the previous digit,
    # and if the size of the previous digits is 2
    if len(prev_digits) == 2 and (prev_digits[len(prev_digits)-1] == prev_digits[len(prev_digits)-2]) and cur_digit > prev_digits[len(prev_digits)-1]:
        return True
    else:
        return False


"""
Returns true if a candidate satisfies the part2 criteria, else false
Criterium 1: two adjacent digits must be the same
Criterium 2: numbers are non-decreasing going left-to-right
"""
def meets_part2_criteria(num: int):
    l = length(num)
    criterium1 = False
    prev_digits = []
    for i in range(0, l):
        cur_digit = ith_digit(num, i)

        #print(f"Current digit: {cur_digit}")
        #print(f"Previous digits: {prev_digits}")
        #print(f"Criterium1 status: {criterium1}")

        # Criterium 2
        if (len(prev_digits) != 0 and cur_digit < prev_digits[len(prev_digits)-1]):
            return False  
        
        # Criterium1
        criterium1 = criterium1 or part2_criterium_1(prev_digits, cur_digit)

        # Be sure to clear prev_digits when we are at a greater number
        if len(prev_digits) != 0 and cur_digit > prev_digits[len(prev_digits)-1]:
            prev_digits.clear()

        # Append current digits to prev_digits for next run
        prev_digits.append(cur_digit)
    # Check once more if criterium1 is satisfied after the last digit, inserting 10 as a dummy value
    #print(f"Current digit: {10}")
    #print(f"Previous digits: {prev_digits}")
    criterium1 = criterium1 or part2_criterium_1(prev_digits, 10)
    return criterium1




"""
Returns the amount of passwords that satisfy the criteria 
(for both part1 and part2)
"""
def solve(inp_path):
    f = open(inp_path)
    line = f.readline().strip()
    start = int(line.split("-")[0])
    stop = int(line.split("-")[1])


    # Count number of passwords that meet the criteria
    candidate_count_part1 = 0
    for candidate in range(start, stop):
        if meets_part1_criteria(candidate):
            candidate_count_part1 += 1 
    print(f"Part 1 solution: {candidate_count_part1}")


    candidate_count_part2 = 0
    for candidate in range(start, stop):
        if meets_part2_criteria(candidate):
            candidate_count_part2 += 1 
    print(f"Part 2 solution: {candidate_count_part2}")

    

def main():
    solve("input/day4.txt")

