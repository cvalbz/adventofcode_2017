# day_03.py

"""
Each square on the grid is allocated in a spiral pattern starting at a location
marked 1 and then counting up while spiraling outward. For example, the first
few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data
must be carried back to square 1 (the location of the only access port for this
memory system) by programs that can only move up, down, left, or right. They
always take the shortest path: the Manhattan Distance between the location of
the data and square 1.

For example:

    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in
your puzzle input all the way to the access port?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from itertools import cycle

DAY = 3

def parse_data(data):
    data = int(data)
    return data

def directions_generator():
    return cycle(["RIGHT", "UP", "LEFT", "DOWN"])

def steps_generator():
    steps = 1
    while True:
        yield steps
        yield steps
        steps += 1

def next_point(point, direction):
    x, y = point

    if direction == "RIGHT":
        return x+1, y
    elif direction == "UP":
        return x, y+1
    elif direction == "LEFT":
        return x-1, y
    elif direction == "DOWN":
        return x, y-1

def points_generator():
    current_nr = 1
    current_point = 0, 0

    yield current_nr, current_point

    directions = directions_generator()
    steps = steps_generator()

    while True:
        direction = next(directions)
        step = next(steps)
        for _ in range(step):
            current_nr += 1
            current_point = next_point(current_point, direction)

            yield current_nr, current_point

def solve_challenge_a(data):
    input_nr = parse_data(data)

    points = points_generator()

    nr, point = next(points)
    while nr < input_nr:
        nr, point = next(points)

    x, y = point
    return abs(x) + abs(y)

assert solve_challenge_a("1") == 0
assert solve_challenge_a("12") == 3
assert solve_challenge_a("23") == 2
assert solve_challenge_a("1024") == 31

"""
As a stress test on the system, the programs here clear the grid and then store
the value 1 in square 1. Then, in the same allocation order as shown above,
they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1),
        so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of
        their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and
        stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets
        the value 5.

Once a square is written, its value does not change. Therefore, the first few
squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?
"""

def compute_adjacent_sum(points_dict, point):
    adjacent_diffs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1),
                      (0, -1), (1, -1)]

    x, y = point
    neighbors_sum = 0
    for x_diff, y_diff in adjacent_diffs:
        neighbor = x + x_diff, y + y_diff
        neighbors_sum += points_dict.get(neighbor, 0)

    return neighbors_sum

def points_sum_generator():
    current_nr = 1
    current_point = 0, 0

    points_dict = {}
    points_dict[current_point] = current_nr

    yield current_nr, current_point

    directions = directions_generator()
    steps = steps_generator()

    while True:
        direction = next(directions)
        step = next(steps)
        for _ in range(step):
            current_point = next_point(current_point, direction)
            current_nr = compute_adjacent_sum(points_dict, current_point)

            points_dict[current_point] = current_nr
            yield current_nr, current_point

def solve_challenge_b(data):
    input_nr = parse_data(data)

    points = points_sum_generator()

    nr, _ = next(points)
    while nr <= input_nr:
        nr, _ = next(points)

    return nr

assert solve_challenge_b("1") == 2
assert solve_challenge_b("2") == 4
assert solve_challenge_b("4") == 5
assert solve_challenge_b("5") == 10

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)