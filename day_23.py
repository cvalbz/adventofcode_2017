# day_23.py

"""
You decide to head directly to the CPU and fix the printer from there. As you
get close, you find an experimental coprocessor doing so much work that the
local programs are afraid it will halt and catch fire. This would cause serious
issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on
that tablet. The general functionality seems very similar, but some of the
instructions are different:

    set X Y sets register X to the value of Y.
    sub X Y decreases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in
        register X by the value of Y.
    jnz X Y jumps with an offset of the value of Y, but only if the value of X
        is not zero. (An offset of 2 skips the next instruction, an offset of
        -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here,
    named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for
testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul
instruction invoked?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from collections import defaultdict

DAY = 23

def parse_data(data):
    lines = data.split("\n")

    instructions = []
    for line in lines:
        s = line.split()
        v_a = int(s[1]) if not s[1].isalpha() else s[1]
        v_b = int(s[2]) if not s[2].isalpha() else s[2]
        instructions.append( (s[0], v_a, v_b) )

    return instructions

def solve_challenge_a(data):
    instructions = parse_data(data)

    reg_state = defaultdict(int)
    program_counter = 0

    nr_muls = 0
    while 0 <= program_counter < len(instructions):
        instr = instructions[program_counter]
        program_counter += 1
        op, x, y = instr[0], instr[1], instr[-1]
        vy = value(reg_state, y)
        vx = value(reg_state, x)
        if   op == 'set': reg_state[x] = vy
        elif op == 'sub': reg_state[x] -= vy
        elif op == 'mul': reg_state[x] *= vy; nr_muls += 1
        elif op == 'jnz' and vx != 0: program_counter += vy - 1

    return nr_muls

def value(reg_state, y): return (y if isinstance(y, int) else reg_state[y])

"""
Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch,
which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program
obviously didn't choose a very efficient implementation. You'll need to
optimize the program if it has any hope of completing before Santa needs that
printer working.

The coprocessor's ultimate goal is to determine the final value left in
register h once the program completes. Technically, if it had that... it
wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what
value would be left in register h?
"""

def solve_challenge_b(data):
    a = 1
    d = e = f = g = h = 0
    b = 67
    c = b
    if a:
        b *= 100
        b -= -100000
        c = b
        c -= -17000
    while True:
        f = 1
        d = 2
        e = 2
        while True:
            if b % d == 0:
                f = 0
            d -= -1
            g = d - b
            if g == 0:
                if f == 0:
                    h -= -1
                g = b - c
                if g == 0:
                    return h
                b -= -17
                break

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)