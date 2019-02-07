# day_21.py

"""
You find a program trying to generate some art. It uses a strange process that
involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either
on (#) or off (.). The program always begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have
a size of 3.

Then, the program repeats the following process:

    If the size is evenly divisible by 2, break the pixels up into 2x2 squares,
        and convert each 2x2 square into a 3x3 square by following the
        corresponding enhancement rule.
    Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3
        squares, and convert each 3x3 square into a 4x4 square by following the
        corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains
pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however,
it seems to be missing rules. The artist explains that sometimes, one must
rotate or flip the input pattern to find a match. (Never rotate or flip the
output pattern, though.) Each pattern is written concisely: rows are listed as
single units, ordered top-down, and separated by slashes. For example, the
following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For
example, all of the following patterns match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It
divides evenly into a single square; the square matches the second rule, which
produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is
used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of
which require some flipping and rotation to line up with the rule. The output
for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from math import sqrt

DAY = 21

def Pixels(text):
    return tuple(tuple(row) for row in text.split('/'))

def rotate(subgrid): 
    return tuple(zip(*reversed(subgrid)))

def flip(subgrid): 
    return tuple(tuple(reversed(row)) for row in subgrid)

def parse_data(data):
    lines = data.split("\n")
    rules = {}
    for line in lines:
        k, v = map(Pixels, line.split(" => "))
        for i in range(4):
            rules[k] = rules[flip(k)] = v
            k = rotate(k)

    return rules

def divide_grid(grid):
    N = len(grid[0])
    d = (2 if N % 2 == 0 else 3 if N % 3 == 0 else error())
    return [[tuple(row[c:c+d] for row in grid[r:r+d]) for c in range(0, N, d)]
            for r in range(0, N, d)]

def flatten(lists):
    rv = []
    for l in lists:
        rv.extend(l)

    return rv

def stitch_grid(squares): 
    "Stitch the pieces back into one big grid."
    N = sum(map(len, squares[0]))
    return tuple(tuple(getpixel(squares, r, c)
                        for c in range(N))
                        for r in range(N))

def getpixel(squares, r, c):
    "The pixel at location (r, c), from a matrix of d x d squares."
    d = len(squares[0][0])
    piece = squares[r // d][c // d]
    return piece[r % d][c % d]

def solve_challenge_a(data, n_iters=5):
    rules = parse_data(data)
    matrix = Pixels(".#./..#/###")

    for ix in range(n_iters):
        squares = divide_grid(matrix)
        for i in range(len(squares)):
            for j in range(len(squares[0])):
                squares[i][j] = rules[squares[i][j]]

        matrix = stitch_grid(squares)

    nr_pix = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '#':
                nr_pix += 1 

    return nr_pix

    
test_data_a = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
assert solve_challenge_a(test_data_a, 2) == 12

"""
How many pixels stay on after 18 iterations?
"""

def solve_challenge_b(data):
    return solve_challenge_a(data, 18)

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)
