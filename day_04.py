# day_04.py

"""
A new system policy has been put in place that requires all accounts to use a
passphrase instead of simply a password. A passphrase consists of a series of
words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

    aa bb cc dd ee is valid.
    aa bb cc dd aa is not valid - the word aa appears more than once.
    aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input. How many
passphrases are valid?
"""

from utils import read_input_data, puzzle_a, puzzle_b

DAY = 4

def parse_data(data):
    lines = data.split("\n")
    return [line.split() for line in lines]

def is_valid_a(passphrase):
    return len(passphrase) == len(set(passphrase))

def solve_challenge_a(data):
    passphrases = parse_data(data)
    return len([p for p in passphrases if is_valid_a(p)])

assert is_valid_a(["aa", "bb", "cc", "dd", "ee"]) == True
assert is_valid_a(["aa", "bb", "cc", "dd", "aa"]) == False
assert is_valid_a(["aa", "bb", "cc", "dd", "aaa"]) == True

"""
For added security, yet another system policy has been put in place. Now, a
valid passphrase must contain no two words that are anagrams of each
other - that is, a passphrase is invalid if any word's letters can be
rearranged to form any other word in the passphrase.

For example:

    abcde fghij is a valid passphrase.
    abcde xyz ecdab is not valid - the letters from the third word can be
        rearranged to form the first word.
    a ab abc abd abf abj is a valid passphrase, because all letters need to be
        used when forming another word.
    iiii oiii ooii oooi oooo is valid.
    oiii ioii iioi iiio is not valid - any of these words can be rearranged to
        form any other word.

Under this new system policy, how many passphrases are valid?
"""

def is_valid_b(passphrase):
    passphrase = ["".join(sorted(word)) for word in passphrase]
    return len(passphrase) == len(set(passphrase))

def solve_challenge_b(data):
    passphrases = parse_data(data)
    return len([p for p in passphrases if is_valid_b(p)])

assert is_valid_b(["abcde", "fghij"]) == True
assert is_valid_b(["abcde", "xyz", "ecdab"]) == False
assert is_valid_b(["a", "ab", "abc", "abd", "abf", "abj"]) == True
assert is_valid_b(["iiii", "oiii", "ooii", "oooo"]) == True
assert is_valid_b(["oiii", "ioii", "iioi", "iiio"]) == False

if __name__ == "__main__":
    puzzle_a(DAY, solve_challenge_a)
    puzzle_b(DAY, solve_challenge_b)