# day_16.py

"""
There are sixteen programs in total, named a through p. They start by standing
in a line: a stands in position 0, b stands in position 1, and so on until p,
which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but
    maintain their order otherwise. (For example, s3 on abcde produces cdeab).
    Exchange, written xA/B, makes the programs at positions A and B swap places.
    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do
the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle
input). In what order are the programs standing after their dance?
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 16

def parse_data(data):
    sequences = data.split(",")
    moves = []
    for s in sequences:
        if s[0] == "s":
            moves.append( ("s", int(s[1:])) )
        if s[0] == "x":
            a, b = s[1:].split("/")
            moves.append( ("x", (int(a), int(b))) )
        if s[0] == "p":
            a, b = s[1:].split("/")
            moves.append( ("p", (a, b)) )

    return moves

def move_s(state, val):
    new_state = list(state)
    for _ in range(val):
        new_state = [new_state[-1]] + new_state[:-1]

    state[:] = new_state

def move_x(state, val):
    a, b = val

    state[a], state[b] = state[b], state[a]

def move_p(state, val):
    a, b = val
    ix_a = state.index(a)
    ix_b = state.index(b)

    move_x(state, (ix_a, ix_b) )

def solve_challenge_a(data, initial_size=16):
    moves = parse_data(data)

    state = list(map(chr, range(ord('a'), ord('a')+initial_size)))

    for move, val in moves:
        if move == "s":
            move_s(state, val)
        if move == "x":
            move_x(state, val)
        if move == "p":
            move_p(state, val)

    return "".join(state)

test_data = "s1,x3/4,pe/b"
assert solve_challenge_a(test_data, 5) == "baedc"

"""
Now that you're starting to get a feel for the dance moves, you turn your
attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs
perform it again and again: including the first dance, a total of one billion
(1000000000) times.

In the example above, their second dance would begin with the order baedc,
and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?
"""

def solve_challenge_b(data, initial_size=16, repeats=10**7):
    moves = parse_data(data)
    state_history = []

    state = list(map(chr, range(ord('a'), ord('a')+initial_size)))

    while state not in state_history:
        state_history.append(list(state))

        for move, val in moves:
            if move == "s":
                move_s(state, val)
            if move == "x":
                move_x(state, val)
            if move == "p":
                move_p(state, val)

    cycle = len(state_history)
    rem = repeats % cycle

    state = list(map(chr, range(ord('a'), ord('a')+initial_size)))
    for _ in range(rem):
        for move, val in moves:
            if move == "s":
                move_s(state, val)
            if move == "x":
                move_x(state, val)
            if move == "p":
                move_p(state, val)

    return "".join(state)

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)