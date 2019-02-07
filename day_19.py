# day_19.py

"""
Somehow, a network packet got lost and ended up here. It's trying to follow a
routing diagram (your puzzle input), but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -,
and +) show the path it needs to take, starting by going down onto the only
line connected to the top of the diagram. It needs to follow this path until it
reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to
continue going the same direction, and only turn left or right when there's no
other option. In addition, someone has left letters on the line; these also
don't change its direction, but it can use them to keep track of where it's
been. For example:

     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go down,
        pass through A, and continue onward to the first +.
    Travel right, up, and right, passing through B in the process.
    Continue down (collecting C), right, and up (collecting D).
    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What
letters will it see (in the order it would see them) if it follows the path?
(The routing diagram is very wide; make sure you view it without line wrapping.)
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 19

def parse_data(data):
    map_lines = data.split("\n")
    return map_lines

def get_starting_point(map_lines):
    return map_lines[0].index('|'), 0

def get_oposite_direction(direction):
    rv = dict(up='down', down='up', right='left', left='right')
    return rv[direction]

def get_neighbors(point, direction, map_lines):
    x, y = point
    neighbors = {}
    if y - 1 >= 0:
        neighbors['up'] = x, y-1
    if y + 1 < len(map_lines):
        neighbors['down'] = x, y+1
    if x - 1 >= 0:
        neighbors['left'] = x-1, y
    if x + 1 < len(map_lines[y]):
        neighbors['right'] = x+1, y

    if get_oposite_direction(direction) in neighbors:
        del neighbors[get_oposite_direction(direction)]
    return neighbors

def get_next_step(current_point, direction, map_lines):
    neighs = get_neighbors(current_point, direction, map_lines)
    return neighs[direction]

def turn_direction(current_point, direction, map_lines):
    x, y = current_point
    neighs = get_neighbors(current_point, direction, map_lines)
    neighs = {d: (x,y) for d, (x, y) in neighs.items() 
                                        if map_lines[y][x] != ' '}

    next_point = list(neighs.items())[0][1]
    next_direction = list(neighs.items())[0][0]

    return next_point, next_direction

def get_steps_and_letters(map_lines):
    letters = []
    nr_steps = 0

    x, y = get_starting_point(map_lines)
    direction = 'down'

    while len(get_neighbors((x,y), direction, map_lines)) > 0:
        while map_lines[y][x] not in ['+', ' ']:
            x, y = get_next_step((x,y), direction, map_lines)
            nr_steps += 1
            if map_lines[y][x].isalpha():
                letters.append(map_lines[y][x])

        if map_lines[y][x] == ' ':
            return nr_steps, "".join(letters)

        if map_lines[y][x] == '+':
            (x, y), direction = turn_direction((x,y), direction, map_lines)
            nr_steps += 1
            if map_lines[y][x].isalpha():
                letters.append(map_lines[y][x])

    return nr_steps, "".join(letters)

def solve_challenge_a(data):
    map_lines = parse_data(data)
    return get_steps_and_letters(map_lines)[1]

    
test_data_a = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """
assert solve_challenge_a(test_data_a) == "ABCDEF"

"""
The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |          
     |  +--+    
     A  |  C    
 F---|--|-E---+ 
     |  |  |  D 
     +B-+  +--+ 

...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?
"""

def solve_challenge_b(data):
    map_lines = parse_data(data)
    return get_steps_and_letters(map_lines)[0]
    
test_data_b = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """
assert solve_challenge_b(test_data_b) == 38

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)