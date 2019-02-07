# day_02.py

"""
The spreadsheet consists of rows of apparently-random numbers. To make sure the
recovery process is on the right track, they need you to calculate the
spreadsheet's checksum. For each row, determine the difference between the
largest value and the smallest value; the checksum is the sum of all of these
differences.

For example, given the following spreadsheet:

5 1 9 5
7 5 3
2 4 6 8

    The first row's largest and smallest values are 9 and 1, and their
        difference is 8.
    The second row's largest and smallest values are 7 and 3, and their
        difference is 4.
    The third row's difference is 6.

In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.
"""

from utils import read_input_data, puzzle_a, puzzle_b
DAY = 2

def parse_data(data):
    spreadsheet = [line.split() for line in data.split("\n")]
    spreadsheet = [[int(i) for i in row] for row in spreadsheet]

    return spreadsheet

def solve_challenge_a(data):
    spreadsheet = parse_data(data)

    diffs = [max(row) - min(row) for row in spreadsheet]

    rv = sum(diffs)
    return rv

test_data = "5 1 9 5\n7 5 3\n2 4 6 8"""
assert solve_challenge_a(test_data) == 18


"""
It sounds like the goal is to find the only two numbers in each row where one
evenly divides the other - that is, where the result of the division operation
is a whole number. They would like you to find those numbers on each line,
divide them, and add up each line's result.

For example, given the following spreadsheet:

5 9 2 8
9 4 7 3
3 8 6 5

    In the first row, the only two numbers that evenly divide are 8 and 2;
        the result of this division is 4.
    In the second row, the two numbers are 9 and 3; the result is 3.
    In the third row, the result is 2.

In this example, the sum of the results would be 4 + 3 + 2 = 9.
"""

from itertools import combinations

def solve_challenge_b(data):
    spreadsheet = parse_data(data)

    s = 0
    for row in spreadsheet:
        comb_pairs = combinations(row, 2)
        for a, b in comb_pairs:
            if a < b:
                a, b = b, a

            if a % b == 0:
                s += a // b

    return s

test_data = "5 9 2 8\n9 4 7 3\n3 8 6 5"""
assert solve_challenge_b(test_data) == 9

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)