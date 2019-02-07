# day_08.py

"""
Each instruction consists of several parts: the register to modify, whether to
increase or decrease that register's value, the amount by which to increase or
decrease it, and a condition. If the condition fails, skip the instruction
without modifying the register. The registers all start at 0. The instructions
look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1
        (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to).
However, the CPU doesn't have the bandwidth to tell you what all the registers
are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in
your puzzle input?
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 8

def parse_data(data):
    lines = data.split("\n")

    instructions = []
    for line in lines:
        splitted = line.replace("if", "").split()
        reg, direction, amount, cond_reg, cond_op, cond_amount = splitted
        amount = int(amount)
        cond_amount = int(cond_amount)
        instructions.append( (reg, direction, amount, cond_reg, cond_op, 
                              cond_amount) )

    return instructions

def eval_cond(reg_state, cond_reg, cond_op, cond_amount):
    assert cond_reg in reg_state

    if cond_op == "<":
        return reg_state[cond_reg] < cond_amount
    elif cond_op == "<=":
        return reg_state[cond_reg] <= cond_amount
    elif cond_op == ">":
        return reg_state[cond_reg] > cond_amount
    elif cond_op == ">=":
        return reg_state[cond_reg] >= cond_amount
    elif cond_op == "==":
        return reg_state[cond_reg] == cond_amount
    elif cond_op == "!=":
        return reg_state[cond_reg] != cond_amount

def execute_instructions(instructions, stage_eval_func=lambda x: x):
    """Executes instructions and applies 'stage_eval_func' (on internal state)
        after each execution. Returns the list of results for each eval."""

    reg_state = {}
    eval_results = []
    for reg, direction, amount, cond_reg, cond_op, cond_amount in instructions:
        if reg not in reg_state:
            reg_state[reg] = 0
        if cond_reg not in reg_state:
            reg_state[cond_reg] = 0

        # do not execute this instruction
        if eval_cond(reg_state, cond_reg, cond_op, cond_amount):
            if direction == "inc":
                reg_state[reg] += amount
            elif direction == "dec":
                reg_state[reg] -= amount

        eval_results.append(stage_eval_func(reg_state))

    return eval_results

def solve_challenge_a(data):
    instructions = parse_data(data)

    max_regs = execute_instructions(instructions, lambda x: max(x.values()))
    return max_regs[-1]

test_data_a = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
assert solve_challenge_a(test_data_a) == 1

"""
To be safe, the CPU also needs to know the highest value held in any register
during this process so that it can decide how much memory to allocate to these
operations. For example, in the above instructions, the highest value ever held
was 10 (in register c after the third instruction was evaluated).
"""

def solve_challenge_b(data):
    instructions = parse_data(data)

    max_regs = execute_instructions(instructions, lambda x: max(x.values()))
    return max(max_regs)

test_data_b = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
assert solve_challenge_b(test_data_b) == 10

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)