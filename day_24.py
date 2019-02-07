# day_24.py

"""
The CPU itself is a large, black building surrounded by a bottomless pit.
Enormous metal tubes extend outward from the side of the building at regular
intervals and descend down into the void. There's no way to cross, but you need
to get inside.

No way, of course, other than building a bridge out of the magnetic components
strewn about nearby.

Each component has two ports, one on each end. The ports come in all different
types, and only matching types can be connected. You take an inventory of the
components by their port types (your puzzle input). Each port is identified by
the number of pins it uses; more pins mean a stronger connection for your
bridge. A 3/7 component, for example, has a type-3 port on one side, and a
type-7 port on the other.

Your side of the pit is metallic; a perfect surface to connect a magnetic,
zero-pin port. Because of this, the first port you use must be of type 0. It
doesn't matter what type of port you end with; your goal is just to make the
bridge as strong as possible.

The strength of a bridge is the sum of the port types in each component. For
example, if your bridge is made of components 0/3, 3/7, and 7/4, your bridge
has a strength of 0+3 + 3+7 + 7+4 = 24.

For example, suppose you had the following components:

0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10

With them, you could make the following valid bridges:

    0/1
    0/1--10/1
    0/1--10/1--9/10
    0/2
    0/2--2/3
    0/2--2/3--3/4
    0/2--2/3--3/5
    0/2--2/2
    0/2--2/2--2/3
    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

(Note how, as shown by 10/1, order of ports within a component doesn't matter.
However, you may only use each port on a component once.)

Of these bridges, the strongest one is 0/1--10/1--9/10; it has a strength of
0+1 + 1+10 + 10+9 = 31.

What is the strength of the strongest bridge you can make with the components
you have available?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from collections import defaultdict

DAY = 24

def parse_data(data):
    lines = data.split("\n")

    tubes = []
    for line in lines:
        a, b = line.split("/")
        tubes.append( (int(a), int(b)) )

    return tubes

def match_tube(size, tube):
    return size == tube[0] or size == tube[1]

def get_other_end(size, tube):
    return tube[0] if size == tube[1] else tube[1]

def valid_bridges(start, tubes):
    if len(tubes) == 0:
        return []

    possible_tubes = [tube for tube in tubes if match_tube(start, tube)]
    if len(possible_tubes) == 0:
        return []

    bridges = []
    for tube in possible_tubes:
        tubes_left = tubes[:]
        tubes_left.remove(tube)

        bridges.append( [tube] )
        for b in valid_bridges(get_other_end(start, tube), tubes_left):
            bridges.append([tube] + b)

    return bridges


def bridge_strength(bridge):
    return sum(map(sum, bridge))

assert bridge_strength([(0, 3), (3, 7), (7, 4)]) == 24


def solve_challenge_a(data):
    tubes = parse_data(data)

    bridges = valid_bridges(0, tubes)
    return max(map(bridge_strength, bridges))

test_data_a = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

assert solve_challenge_a(test_data_a) == 31

"""
The bridge you've built isn't long enough; you can't jump the rest of the way.

In the example above, there are two longest bridges:

    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

Of them, the one which uses the 3/5 component is stronger; its strength is
0+2 + 2+2 + 2+3 + 3+5 = 19.

What is the strength of the longest bridge you can make? If you can make
multiple bridges of the longest length, pick the strongest one.
"""

def solve_challenge_b(data):
    tubes = parse_data(data)

    bridges = valid_bridges(0, tubes)
    return max([(len(b), bridge_strength(b)) for b in bridges])[1]

test_data_b = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""

assert solve_challenge_b(test_data_b) == 19

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)