# day_12.py

"""
Walking along the memory banks of the stream, you find a small village that
is experiencing a little confusion: some programs can't communicate with each
other.

Programs in this village communicate using a fixed system of pipes. Messages
are passed between programs using these pipes, but most programs aren't
connected to each other directly. Instead, programs pass messages between each
other until the message reaches the intended recipient.

For some reason, though, some of these messages aren't ever reaching their
intended recipient, and the programs suspect that some pipes are missing. They
would like you to investigate.

You walk through the village and record the ID of each program and the IDs with
which it can communicate directly (your puzzle input). Each program has one or
more programs with which it can communicate, and these pipes are bidirectional;
if 8 says it can communicate with 11, then 11 will say it can communicate
with 8.

You need to figure out how many programs are in the group that contains program
ID 0.

For example, suppose you go door-to-door like a travelling salesman and record
the following list:

0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5

In this example, the following programs are in the group that contains program
ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.

Therefore, a total of 6 programs are in this group; all but program 1, which
has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 12

def parse_data(data):
    lines = data.split("\n")
    graph = {}
    for line in lines:
        node, neighbors = line.split(" <-> ")
        graph[int(node)] = list(map(int, neighbors.split(", ")))

    return graph


def DFS(graph, starting_node=0):
    visited = {node:False for node, _ in graph.items()}

    stack = [starting_node]
    while len(stack) > 0:
        current_node = stack.pop()
        visited[current_node] = True

        for neighbor in graph[current_node]:
            if not visited[neighbor]:
                stack.append(neighbor)

    return [k for k in visited if visited[k]]

def solve_challenge_a(data):
    graph = parse_data(data)

    reachable = DFS(graph)
    return len(reachable)

test_data = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
assert solve_challenge_a(test_data) == 6

"""
There are more programs than just the ones in the group containing program ID
0. The rest of them have no way of reaching that group, and still might have no
way of reaching each other.

A group is a collection of programs that can all communicate via pipes either
directly or indirectly. The programs you identified just a moment ago are all
part of the same group. Now, they would like you to determine the total number
of groups.

In the example above, there were 2 groups: one consisting of programs
0,2,3,4,5,6, and the other consisting solely of program 1.

How many groups are there in total?
"""

def solve_challenge_b(data):
    graph = parse_data(data)
    nodes_to_visit = list(graph.keys())

    nr_components = 0
    while len(nodes_to_visit) > 0:
        start_dfs = nodes_to_visit[0]
        scc = DFS(graph, start_dfs)

        nr_components += 1
        for node in scc:
            nodes_to_visit.remove(node)

    return nr_components


test_data_b = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
assert solve_challenge_b(test_data_b) == 2


if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)