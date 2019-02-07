# day_09.py

"""
A large stream blocks your path. According to the locals, it's not safe to
cross the stream at the moment because it's full of garbage. You look down at
the stream; rather than water, you discover that it's a stream of characters.

You sit for a while and record part of the stream (your puzzle input). The
characters represent groups - sequences that begin with { and end with }.
Within a group, there are zero or more other things, separated by commas:
either another group or garbage. Since groups can contain other groups, a }
only closes the most-recently-opened unclosed group - that is, they are
nestable. Your puzzle input represents a single, large group which itself
contains many smaller ones.

Sometimes, instead of a group, you will find garbage. Garbage begins with < and
ends with >. Between those angle brackets, almost any character can appear,
including { and }. Within garbage, < has no special meaning.

In a futile attempt to clean up the garbage, some program has canceled some of
the characters within it using !: inside garbage, any character that comes
after ! should be ignored, including <, >, and even another !.

You don't see any characters that deviate from these rules. Outside garbage,
you only find well-formed groups, and garbage always terminates according to
the rules above.

Here are some self-contained pieces of garbage:

    <>, empty garbage.
    <random characters>, garbage containing random characters.
    <<<<>, because the extra < are ignored.
    <{!>}>, because the first > is canceled.
    <!!>, because the second ! is canceled, allowing the > to terminate the
          garbage.
    <!!!>>, because the second ! and the first > are canceled.
    <{o"i!a,<{i<a>, which ends at the first >.

Here are some examples of whole streams and the number of groups they contain:

    {}, 1 group.
    {{{}}}, 3 groups.
    {{},{}}, also 3 groups.
    {{{},{},{{}}}}, 6 groups.
    {<{},{},{{}}>}, 1 group (which itself contains garbage).
    {<a>,<a>,<a>,<a>}, 1 group.
    {{<a>},{<a>},{<a>},{<a>}}, 5 groups.
    {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

Your goal is to find the total score for all groups in your input. Each group
is assigned a score which is one more than the score of the group that
immediately contains it. (The outermost group gets a score of 1.)

    {}, score of 1.
    {{{}}}, score of 1 + 2 + 3 = 6.
    {{},{}}, score of 1 + 2 + 2 = 5.
    {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
    {<a>,<a>,<a>,<a>}, score of 1.
    {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
    {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
    {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

What is the total score for all groups in your input?
"""

from utils import read_input_data, puzzle_a, puzzle_b
import re

DAY = 9

def parse_data(data):
    return data

def clean_ignored_characters(stream):
    stream = re.sub(r"!.", "", stream)
    return stream

def clean_garbage_groups(stream):
    stream = re.sub(r"<.*?>", "", stream)
    return stream

def clean_groups_score(stream):
    """Computes the total score of a clean stream"""
    total_score = 0
    current_group_score = 0
    for c in stream:
        if c == "{":
            current_group_score += 1
            total_score += current_group_score
        elif c == "}":
            current_group_score -= 1

    return total_score
    

assert clean_groups_score("{}") == 1
assert clean_groups_score("{{{}}}") == 6
assert clean_groups_score("{{},{}}") == 5
assert clean_groups_score("{{{},{},{{}}}}") == 16

def solve_challenge_a(data):
    stream = parse_data(data)
    stream = clean_ignored_characters(stream)
    stream = clean_garbage_groups(stream)

    return clean_groups_score(stream)

assert solve_challenge_a("{<a>,<a>,<a>,<a>}") == 1
assert solve_challenge_a("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
assert solve_challenge_a("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
assert solve_challenge_a("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3

"""
Now, you're ready to remove the garbage.

To prove you've removed it, you need to count all of the characters within the
garbage. The leading and trailing < and > don't count, nor do any canceled
characters or the ! doing the canceling.

    <>, 0 characters.
    <random characters>, 17 characters.
    <<<<>, 3 characters.
    <{!>}>, 2 characters.
    <!!>, 0 characters.
    <!!!>>, 0 characters.
    <{o"i!a,<{i<a>, 10 characters.

How many non-canceled characters are within the garbage in your puzzle input?
"""

def count_garbage_characters(stream):
    no_garbage_characters = re.sub(r"<.*?>", "<>", stream)
    return len(stream) - len(no_garbage_characters)

def solve_challenge_b(data):
    stream = parse_data(data)
    stream = clean_ignored_characters(stream)

    return count_garbage_characters(stream)

assert solve_challenge_b("<>") == 0
assert solve_challenge_b("<random characters>") == 17
assert solve_challenge_b("<<<<>") == 3
assert solve_challenge_b("<{!>}>") == 2
assert solve_challenge_b("<!!>") == 0
assert solve_challenge_b("<!!!>>") == 0
assert solve_challenge_b('<{o"i!a,<{i<a>') == 10

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)