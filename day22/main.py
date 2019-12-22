from dataclasses import dataclass
import re

@dataclass
class Deal:
    def apply(self, deck): return deck[::-1]

@dataclass
class Cut:
    n: int
    def apply(self, deck):
        n = self.n
        a = deck[:n]
        b = deck[n:]
        return b + a

@dataclass
class DealIncrement:
    n: int
    def apply(self, deck):
        space = [0] * len(deck)
        n = self.n
        for idx, card in enumerate(deck):
            pos = (idx * n) % len(deck)
            space[pos] = card
        return space


def parse(line):
    """
    >>> parse("cut 4753")
    Cut(n=4753)
    >>> parse("cut -37")
    Cut(n=-37)
    >>> parse("deal with increment 64")
    DealIncrement(n=64)
    >>> parse("deal into new stack")
    Deal()
    """
    m = re.match("^cut ([0-9-]+)$", line)
    if not (m is None):
        return Cut(int(m[1]))
    m = re.match("^deal with increment ([0-9]+)$", line)
    if not (m is None):
        return DealIncrement(int(m[1]))
    m = re.match("^deal", line)
    if not (m is None):
        return Deal()
    raise Exception("Cannot parse: %s" % (line,))

def testApply(move, deck):
    """
    >>> testApply(Deal(), [1,2,3])
    [3, 2, 1]
    >>> testApply(Cut(2), [1,2,3])
    [3, 1, 2]
    >>> testApply(Cut(-2), [1,2,3])
    [2, 3, 1]
    >>> testApply(DealIncrement(3), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    """
    return move.apply(deck)

def readInput():
    with open("input") as f:
        lines = f.readlines()
        return list(map(lambda l:parse(l.strip()), lines))

def part1():
    """
    >>> part1()
    1510
    """
    moves = readInput()
    deck = list(range(0, 10007))
    for move in moves:
        deck = move.apply(deck)
    return deck.index(2019)

if __name__ == "__main__":
    import doctest
    doctest.testmod()