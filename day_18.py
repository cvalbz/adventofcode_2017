# day_18.py

"""
You discover a tablet containing some strange assembly code labeled simply
"Duet". Rather than bother the sound card with it, you decide to run the code
yourself. Unfortunately, you don't see any documentation, so you're left to
figure out what the instructions mean on your own.

It seems like the assembly is meant to operate on a set of registers that are
each named with a single letter and that can each hold a single integer. You
suppose each register should start with a value of 0.

There aren't that many instructions, so it shouldn't be hard to figure out what
they do. Here's what you determine:

    snd X plays a sound with a frequency equal to the value of X.
    set X Y sets register X to the value of Y.
    add X Y increases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in
        register X by the value of Y.
    mod X Y sets register X to the remainder of dividing the value contained in
        register X by the value of Y (that is, it sets X to the result of X
        modulo Y).
    rcv X recovers the frequency of the last sound played, but only when the
        value of X is not zero. (If it is zero, the command does nothing.)
    jgz X Y jumps with an offset of the value of Y, but only if the value of X
        is greater than zero. (An offset of 2 skips the next instruction, an
        offset of -1 jumps to the previous instruction, and so on.)

Many of the instructions can take either a register (a single letter) or a
number. The value of a register is the integer it contains; the value of a
number is that number.

After each jump instruction, the program continues with the instruction to
which the jump jumped. After any other instruction, the program continues with
the next instruction. Continuing (or jumping) off either end of the program
terminates it.

For example:

set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2

    The first four instructions set a to 1, add 2 to it, square it, and then
        set it to itself modulo 5, resulting in a value of 4.
    Then, a sound with frequency 4 (the value of a) is played.
    After that, a is set to 0, causing the subsequent rcv and jgz instructions
        to both be skipped (rcv because a is 0, and jgz because a is not
        greater than 0).
    Finally, a is set to 1, causing the next jgz instruction to activate,
        jumping back two instructions to another jump, which jumps again to the
        rcv, which ultimately triggers the recover operation.

At the time the recover operation is executed, the frequency of the last sound
played is 4.

What is the value of the recovered frequency (the value of the most recently
played sound) the first time a rcv instruction is executed with a non-zero
value?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from collections import defaultdict, deque

DAY = 18

def parse_data(data):
    lines = data.split("\n")

    instructions = []
    for line in lines:
        s = line.split()
        if s[0] in ["snd", "rcv"]:
            v_b = int(s[1]) if not s[1].isalpha() else s[1]
            instructions.append( (s[0], v_b) )
        else:
            v_a = int(s[1]) if not s[1].isalpha() else s[1]
            v_b = int(s[2]) if not s[2].isalpha() else s[2]
            instructions.append( (s[0], v_a, v_b) )

    return instructions

def solve_challenge_a(data):
    instructions = parse_data(data)

    reg_state = defaultdict(int)
    program_counter = 0
    last_sound = 0

    while True:
        instr = instructions[program_counter]
        program_counter += 1
        op, x, y = instr[0], instr[1], instr[-1]
        vy = value(reg_state, y)
        if   op == 'snd': snd = reg_state[x]
        elif op == 'set': reg_state[x] = vy
        elif op == 'add': reg_state[x] += vy
        elif op == 'mul': reg_state[x] *= vy
        elif op == 'mod': reg_state[x] %=  vy
        elif op == 'jgz' and reg_state[x] > 0: program_counter += vy - 1
        elif op == 'rcv' and reg_state[x] != 0: return snd

def value(reg_state, y): return (y if isinstance(y, int) else reg_state[y])

test_data_a = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
assert solve_challenge_a(test_data_a) == 4

"""
As you congratulate yourself for a job well done, you notice that the
documentation has been on the back of the tablet this entire time. While you
actually got most of the instructions correct, there are a few key differences.
This assembly code isn't about sound at all - it's meant to be run twice at the
same time.

Each running copy of the program has its own set of registers and follows the
code independently - in fact, the programs don't even necessarily run at the
same speed. To coordinate, they use the send (snd) and receive (rcv)
instructions:

    snd X sends the value of X to the other program. These values wait in a
        queue until that program is ready to receive them. Each program has its
        own message queue, so a program can never receive a message it sent.
    rcv X receives the next value and stores it in register X. If no values are
        in the queue, the program waits for a value to be sent to it. Programs
        do not continue to the next instruction until they have received a
        value. Values are received in the order they are sent.

Each program also has its own program ID (one 0 and the other 1); the register
p should begin with this value.

For example:

snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d

Both programs begin by sending three values to the other. Program 0 sends 1, 2,
0; program 1 sends 1, 2, 1. Then, each program receives a value (both 1) and
stores it in a, receives another value (both 2) and stores it in b, and then
each receives the program ID of the other program (program 0 receives 1;
program 1 receives 0) and stores it in c. Each program now sees a different
value in its own copy of register c.

Finally, both programs try to rcv a fourth time, but no data is waiting for
either of them, and they reach a deadlock. When this happens, both programs
terminate.

It should be noted that it would be equally valid for the programs to run at
different speeds; for example, program 0 might have sent all three values and
then stopped at the first rcv before program 1 executed even its first
instruction.

Once both of your programs have terminated (regardless of what caused them to
do so), how many times did program 1 send a value?
"""

import random
def solve_challenge_b(data):
    instructions = parse_data(data)

    queues = [deque(), deque()]
    ps = [dict(id=id, pc=0, sends=0, regs=defaultdict(int, p=id), status='run')
          for id in (0, 1)]
    while ps[0]['status'] == 'run' or ps[1]['status'] == 'run':
        execute_instruction(instructions, queues, random.choice(ps))

    return ps[1]['sends']

def execute_instruction(instructions, queues, p):
    if p['pc'] < 0 or p['pc'] > len(instructions):
        p['status'] = 'end'
    else:
        instr = instructions[p['pc']]
        op, x, y = instr[0], instr[1], instr[-1]
        vx, vy = value(p['regs'], x), value(p['regs'], y)
        if   op == 'snd': queues[1-p['id']].append(vy); p['sends'] += 1
        elif op == 'set': p['regs'][x] = vy
        elif op == 'add': p['regs'][x] += vy
        elif op == 'mul': p['regs'][x] *= vy
        elif op == 'mod': p['regs'][x] %= vy
        elif op == 'jgz' and vx > 0: p['pc'] += vy - 1
        elif op == 'rcv': 
            if not queues[p['id']]:
                p['status'] = 'wait'
                return # don't update pc; try again next time
            else:
                p['regs'][x] = queues[p['id']].popleft()
                p['status'] = 'run'
        p['pc'] += 1

test_data_b = """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""
assert solve_challenge_b(test_data_b) == 3

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)