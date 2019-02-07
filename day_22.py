# day_22.py

"""
Diagnostics indicate that the local grid computing cluster has been
contaminated with the Sporifica Virus. The grid computing cluster is a
seemingly-infinite two-dimensional grid of compute nodes. Each node is either
clean or infected by the virus.

To prevent overloading the nodes (which would render them useless to the virus)
or detection by system administrators, exactly one virus carrier moves through
the network, infecting or cleaning nodes as it moves. The virus carrier is
always located on a single node in the network (the current node) and keeps
track of the direction it is facing.

To avoid detection, the virus carrier works in bursts; in each burst, it wakes
up, does some work, and goes back to sleep. The following steps are all
executed in order one time each burst:

    If the current node is infected, it turns to its right. Otherwise, it turns
      to its left. (Turning is done in-place; the current node does not change.)
    If the current node is clean, it becomes infected. Otherwise, it becomes
      cleaned. (This is done after the node is considered for the purposes of
      changing direction.)
    The virus carrier moves forward one node in the direction it is facing.

Diagnostics have also provided a map of the node infection status (your puzzle
input). Clean nodes are shown as .; infected nodes are shown as #. This map
only shows the center of the grid; there are many more nodes beyond those
shown, but none of them are currently infected.

The virus carrier begins in the middle of the map facing up.

For example, suppose you are given a map like this:

..#
#..
...

Then, the middle of the infinite grid looks like this, with the virus carrier's
position marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on a clean node, so it turns left, infects the node, and
moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]# . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on an infected node, so it turns right, cleans the node,
and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . . # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Four times in a row, the virus carrier finds a clean, infects it, turns left,
and moves forward, ending in the same place and still facing up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . #[#]. # . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Now on the same node as before, it sees an infection, which causes it to turn
right, clean the node, and move forward:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . # .[.]# . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

After the above actions, a total of 7 bursts of activity had taken place. Of
them, 5 bursts of activity caused an infection.

After a total of 70, the grid looks like this, with the virus carrier facing up:

. . . . . # # . .
. . . . # . . # .
. . . # . . . . #
. . # . #[.]. . #
. . # . # . . # .
. . . . . # # . .
. . . . . . . . .
. . . . . . . . .

By this time, 41 bursts of activity caused an infection (though most of those
nodes have since been cleaned).

After a total of 10000 bursts of activity, 5587 bursts will have caused an
infection.

Given your actual map, after 10000 bursts of activity, how many bursts cause a
node to become infected? (Do not count nodes that begin infected.)
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 22

def parse_data(data):
    lines = data.split("\n")
    return [list(line) for line in lines]

def turn_right(direction):
    return dict(up='right', down='left', left='up', right='down')[direction]

def turn_left(direction):
    return dict(up='left', down='right', left='down', right='up')[direction]

def step(x, y, direction):
    if   direction == 'up':    return x, y-1
    elif direction == 'down':  return x, y+1
    elif direction == 'left':  return x-1, y
    elif direction == 'right': return x+1, y

def solve_challenge_a(data, n_iter=10000):
    infection_map = parse_data(data)

    infections = []
    for i in range(len(infection_map)):
        for j in range(len(infection_map[0])):
            if infection_map[i][j] == '#':
                infections.append( (j, i) )

    x = len(infection_map[0]) // 2
    y = len(infection_map) // 2
    direction = 'up'
    nr_infections = 0
    
    for i in range(n_iter):
        if (x,y) in infections:
            direction = turn_right(direction)
            infections.remove((x,y))
        else:
            direction = turn_left(direction)
            infections.append((x,y))
            nr_infections += 1

        x, y = step(x, y, direction) 

    return nr_infections

    
test_data_a = """\
.........
.........
.........
.....#...
...#.....
.........
.........
........."""
assert solve_challenge_a(test_data_a, 7) == 5
assert solve_challenge_a(test_data_a) == 5587

"""
As you go to remove the virus from the infected nodes, it evolves to resist
your attempt.

Now, before it infects a clean node, it will weaken it to disable your
defenses. If it encounters an infected node, it will instead flag the node to
be cleaned in the future. So:

    Clean nodes become weakened.
    Weakened nodes become infected.
    Infected nodes become flagged.
    Flagged nodes become clean.

Every node is always in exactly one of the above states.

The virus carrier still functions in a similar way, but now uses the following
logic during its bursts of action:

    Decide which way to turn based on the current node:
        If it is clean, it turns left.
        If it is weakened, it does not turn, and will continue moving in the
            same direction.
        If it is infected, it turns right.
        If it is flagged, it reverses direction, and will go back the way it
            came.
    Modify the state of the current node, as described above.
    The virus carrier moves forward one node in the direction it is facing.

Start with the same map (still using . for clean and # for infected) and still
with the virus carrier starting in the middle and facing up.

Using the same initial state as the previous example, and drawing weakened as W
and flagged as F, the middle of the infinite grid looks like this, with the
virus carrier's position again marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

This is the same as before, since no initial nodes are weakened or flagged. The
virus carrier is on a clean node, so it still turns left, instead weakens the
node, and moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on an infected node, so it still turns right, instead
flags the node, and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . F W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

This process repeats three more times, ending on the previously-flagged node
and facing right:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
. . W[F]W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Finding a flagged node, it reverses direction and cleans the node:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
. .[W]. W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The weakened node becomes infected, and it continues in the same direction:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
.[.]# . W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Of the first 100 bursts, 26 will result in infection. Unfortunately, another
feature of this evolved virus is speed; of the first 10000000 bursts, 2511944
will result in infection.

Given your actual map, after 10000000 bursts of activity, how many bursts cause
a node to become infected? (Do not count nodes that begin infected.)
"""

def turn_back(direction):
    return dict(up='down', down='up', left='right', right='left')[direction]


from collections import defaultdict
def solve_challenge_b(data, n_iter=10000000):
    infection_map = parse_data(data)

    cells = defaultdict(lambda: 'C')

    for i in range(len(infection_map)):
        for j in range(len(infection_map[0])):
            if infection_map[i][j] == '#':
                cells[(j, i)] = 'I'

    x = len(infection_map[0]) // 2
    y = len(infection_map) // 2
    direction = 'up'
    nr_infections = 0
    
    for i in range(n_iter):
        if cells[(x,y)] == 'C':
            direction = turn_left(direction)
            cells[(x,y)] = 'W'
        elif cells[(x,y)] == 'F':
            direction = turn_back(direction)
            cells[(x,y)] = 'C'
        elif cells[(x,y)] == 'W':
            cells[(x,y)] = 'I'
            nr_infections += 1
        elif cells[(x,y)] == 'I':
            direction = turn_right(direction)
            cells[(x,y)] = 'F'            
            
        x, y = step(x, y, direction)

    return nr_infections

    
test_data_b = """\
.........
.........
.........
.....#...
...#.....
.........
.........
........."""
assert solve_challenge_b(test_data_b, 100) == 26
assert solve_challenge_b(test_data_b) == 2511944


if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)