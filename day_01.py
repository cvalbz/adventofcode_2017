# day_01.py

"""
It goes on to explain that you may only leave by solving a captcha to prove
you're not a human. Apparently, you only get one millisecond to solve the
captcha: too fast for a normal human, but it feels like hours to you.

The captcha requires you to review a sequence of digits (your puzzle input)
and find the sum of all digits that match the next digit in the list. The list
is circular, so the digit after the last digit is the first digit in the list.

For example:

    1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the
        second digit and the third digit (2) matches the fourth digit.
    1111 produces 4 because each digit (all 1) matches the next.
    1234 produces 0 because no digit matches the next.
    91212129 produces 9 because the only digit that matches the next one is the
        last digit, 9.
"""

from utils import read_input_data, puzzle_a, puzzle_b
DAY = 1

def parse_data(data):
    data = [int(i) for i in data]
    return data

def solve_challenge_a(data):
    data = parse_data(data)

    shifted = [data[-1]] + data[:-1]
    pairs = zip(data, shifted)
    matching = [i for i,j in pairs if i == j]

    rv = sum(matching)
    return rv

assert solve_challenge_a('1122') == 3
assert solve_challenge_a('1111') == 4
assert solve_challenge_a('1234') == 0
assert solve_challenge_a('91212129') == 9

"""
Now, instead of considering the next digit, it wants you to consider the digit
halfway around the circular list. That is, if your list contains 10 items, only
include a digit in your sum if the digit 10/2 = 5 steps forward matches it.
Fortunately, your list has an even number of elements.

For example:

    1212 produces 6: the list contains 4 items, and all four digits match the
        digit 2 items ahead.
    1221 produces 0, because every comparison is between a 1 and a 2.
    123425 produces 4, because both 2s match each other, but no other digit has
        a match.
    123123 produces 12.
    12131415 produces 4.
"""

def solve_challenge_b(data):
    data = parse_data(data)
    assert len(data) % 2 == 0

    k = len(data) // 2
    shifted = data[k:] + data[:k]
    pairs = zip(data, shifted)
    matching = [i for i,j in pairs if i == j]

    rv = sum(matching)
    return rv

assert solve_challenge_b('1212') == 6
assert solve_challenge_b('1221') == 0
assert solve_challenge_b('123425') == 4
assert solve_challenge_b('123123') == 12
assert solve_challenge_b('12131415') == 4

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)