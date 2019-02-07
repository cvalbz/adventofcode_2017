# day_11.py

"""
Crossing the bridge, you've barely reached the other side of the stream when a
program comes up to you, clearly in distress. "It's my child process," she
says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be
found to the north, northeast, southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need
to determine the fewest number of steps required to reach him. (A "step" means
to move from the hex you are in to any adjacent hex.)

For example:
    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 11

def parse_data(data):
    data = data.split(",")
    return data


def hex_manhattan_distance(a, b):
    return (abs(a[0] - b[0]) 
            + abs(a[0] + a[1] - b[0] - b[1])
            + abs(a[1] - b[1])) // 2


def solve_challenge_a(data):
    steps = parse_data(data)

    deltas = dict(n=(0,-1), ne=(1,-1), se=(1,0), s=(0,1), sw=(-1,1), nw=(-1,0))
    current_point = 0, 0

    for step in steps:
        dx, dy = deltas[step]
        x, y = current_point
        current_point = x + dx, y + dy

    return hex_manhattan_distance(current_point, (0, 0))


assert solve_challenge_a("ne,ne,ne") == 3
assert solve_challenge_a("ne,ne,sw,sw") == 0
assert solve_challenge_a("ne,ne,s,s") == 2
assert solve_challenge_a("se,sw,se,sw,sw") == 3

"""
How many steps away is the furthest he ever got from his starting position?
"""

def solve_challenge_b(data):
    steps = parse_data(data)

    deltas = dict(n=(0,-1), ne=(1,-1), se=(1,0), s=(0,1), sw=(-1,1), nw=(-1,0))
    current_point = 0, 0

    max_dist = 0
    for step in steps:
        dx, dy = deltas[step]
        x, y = current_point
        current_point = x + dx, y + dy
        max_dist = max(max_dist, hex_manhattan_distance(current_point, (0, 0)))

    return max_dist

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)