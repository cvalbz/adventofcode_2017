# day_07.py

"""
Wandering further through the circuits of the computer, you come upon a tower
of programs that have gotten themselves into a bit of trouble. A recursive
algorithm has gotten out of hand, and now they're balanced precariously in a
large tower.

One program at the bottom supports the entire tower. It's holding a large disc,
and on the disc are balanced several more sub-towers. At the bottom of these
sub-towers, standing on the bottom disc, are other programs, each holding their
own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many
programs stand simply keeping the disc below them balanced but with no disc of
their own.

You offer to help, but first you need to understand the structure of these
towers. You ask each program to yell out their name, their weight, and (if
they're holding a disc) the names of the programs immediately above them
balancing on that disc. You write this information down (your puzzle input).
Unfortunately, in their panic, they don't do this in an orderly fashion; by the
time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)

...then you would be able to recreate the structure of the towers that looks
like this:

                gyxo
              /     
         ugml - ebii
       /      \     
      |         jptl
      |        
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |             
      |         ktlj
       \      /     
         fwft - cntj
              \     
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and
is holding up ugml, padx, and fwft. Those programs are, in turn, holding up
other programs; in this example, none of those programs are holding up any
other programs, and are all the tops of their own towers. (The actual tower
balancing in front of you is much larger.)

Before you're ready to help them, you need to make sure your information is
correct. What is the name of the bottom program?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from anytree import Node, RenderTree
from collections import Counter

DAY = 7

def parse_data(data):
    lines = data.split("\n")

    nodes = []
    for line in lines:
        splitted = line.split(" ")
        program = splitted[0]
        weight = int(splitted[1].replace("(", "").replace(")", ""))
        if '->' not in line:
            nodes.append( (program, weight) )
        else:
            children = [i.replace(",", "") for i in splitted[3:]]
            nodes.append( (program, weight, children) )

    return nodes

def build_tree(nodes):
    programs_dict = {}

    # create all nodes
    for node in nodes:
        program, weight = node[0], node[1]
        programs_dict[program] = Node(program, weight=weight)

    # create parent-child relationships
    for node in [i for i in nodes if len(i) == 3]:
        program, weight, children = node
        for child in children:
            programs_dict[child].parent = programs_dict[program]

    return programs_dict

def solve_challenge_a(data):
    nodes = parse_data(data)
    programs_dict = build_tree(nodes)

    roots = [node for node in programs_dict.values() if node.is_root]
    assert len(roots) == 1
    return roots[0].name


test_data_a = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
assert solve_challenge_a(test_data_a) == "tknk"

"""
The programs explain the situation: they can't get down. Rather, they could get
down, if they weren't expending all of their energy trying to keep the tower
balanced. Apparently, one program has the wrong weight, and until it's fixed,
they're stuck here.

For any program holding a disc, each program standing on that disc forms a
sub-tower. Each of those sub-towers are supposed to be the same weight, or the
disc itself isn't balanced. The weight of a tower is the sum of the weights of
the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo,
ebii, and jptl must all have the same weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and
all programs above it must each match. This means that the following sums must
all be the same:

    ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
    padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
    fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the
other two. Even though the nodes above ugml are balanced, ugml itself is too
heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the
towers balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need
to be to balance the entire tower?
"""

def augment_with_subweights(node):
    if node.is_leaf:
        setattr(node, "subweight", node.weight)
        return

    subweight = node.weight
    for child in node.children:
        augment_with_subweights(child)
        subweight += child.subweight

    setattr(node, "subweight", subweight)

def find_majority(values):
    c = Counter(values)
    return c.most_common()[0][0]

def find_imbalance(node):
    # we assume there is an imbalance somewhere, will never arrive at leaves
    children_subweights = [i.subweight for i in node.children]

    # 'node' is the imbalanced one, it's children are balanced
    if len(set(children_subweights)) == 1:
        sibling_subweights = [i.subweight for i in node.siblings]
        assert len(set(sibling_subweights)) == 1
        return node.weight + (sibling_subweights[0] - node.subweight)

    # find the imbalanced one among 'node' children    
    majority = find_majority(children_subweights)
    for child in node.children:
        if child.subweight != majority:
            return find_imbalance(child)


def solve_challenge_b(data):
    nodes = parse_data(data)
    programs_dict = build_tree(nodes)
    roots = [node for node in programs_dict.values() if node.is_root]
    assert len(roots) == 1
    root = roots[0]

    augment_with_subweights(root)
    rv = find_imbalance(root)

    return rv

test_data_b = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
assert solve_challenge_b(test_data_b) == 60

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)