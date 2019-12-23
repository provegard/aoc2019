from dataclasses import dataclass
import re

@dataclass
class Deal:
    def apply(self, deck): return deck[::-1]

    def moveCard(self, deckLen, cardIndex):
        return deckLen - cardIndex - 1

    def comingFromIdx(self, deckLen, cardIndex):
        return deckLen - cardIndex - 1

@dataclass
class Cut:
    n: int
    def apply(self, deck):
        n = self.n
        a = deck[:n]
        b = deck[n:]
        return b + a

    def moveCard(self, deckLen, cardIndex):
        n = self.n
        if n > 0:
            if cardIndex < n:
                # moves back
                return deckLen - n + cardIndex
            # moves in front
            return cardIndex - n
        if cardIndex < deckLen + n:
            # moves back
            return cardIndex - n
        # moves in front
        return cardIndex - (deckLen + n)

    def comingFromIdx(self, deckLen, cardIndex):
        n = self.n
        moveLen = abs(n)
        stationaryLen = deckLen - moveLen
        if n > 0:
            # n cards were moved from the front
            if cardIndex < stationaryLen:
                # card wasn't one that moved
                return cardIndex + moveLen
            # card did move
            return cardIndex - stationaryLen
        # n cards were moved from the back
        if cardIndex < moveLen:
            # the card did move
            return cardIndex + stationaryLen
        # the card didn't move
        return cardIndex - moveLen

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

    def moveCard(self, deckLen, cardIndex):
        n = self.n
        return (cardIndex * n) % deckLen

    def comingFromIdx(self, deckLen, cardIndex):
        # (N * idx) mod L = new_idx
        # N * idx = yL + new_idx
        # N * idx - newIdx = yL
        # (N * idx - newIdx) / L = y
        n = self.n
        for y in range(0, n):
            c = (y * deckLen) + cardIndex
            if c % n == 0:
                return c // n
        raise Exception(":( for %d, %d" % (deckLen, cardIndex))

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

def testComingFromIdx(move, deckLen, idx):
    """
    >>> testComingFromIdx(Deal(), 5, 1)
    3
    >>> testComingFromIdx(Cut(2), 5, 4)
    1
    >>> testComingFromIdx(Cut(2), 5, 0)
    2
    >>> testComingFromIdx(Cut(-2), 6, 4)
    2
    >>> testComingFromIdx(Cut(-2), 6, 2)
    0
    >>> testComingFromIdx(Cut(-2), 6, 1)
    5
    >>> testComingFromIdx(DealIncrement(3), 10, 1)
    7
    >>> testComingFromIdx(DealIncrement(3), 10, 4)
    8
    >>> testComingFromIdx(DealIncrement(3), 10, 3)
    1
    >>> testComingFromIdx(DealIncrement(52), 10119315717514047, 2020)
    2335226704041742
    """
    return move.comingFromIdx(deckLen, idx)

def testMoveCard(move, deckLen, idx):
    """
    >>> testMoveCard(DealIncrement(52), 10119315717514047, 2335226704041742)
    2020
    """
    return move.moveCard(deckLen, idx)

def readInput():
    with open("input") as f:
        lines = f.readlines()
        return list(map(lambda l:parse(l.strip()), lines))

# def part1():
#     """
#     >>> part1()
#     1510
#     """
#     moves = readInput()
#     cardIndex = 2019
#     deckLen = 10007
#     for move in moves:
#         cardIndex = move.moveCard(deckLen, cardIndex)
#     return cardIndex

def reverse(lst): return lst[::-1]

def part2():
    moves = readInput()
    deckLen = 119315717514047
    repetitions = 101741582076661

    revMoves = reverse(moves)

    r = 0
    cardIndex = 2020
    seen = set([])
    while True: #repetitions:
        before = cardIndex
        if r % 1000 == 0:
            print(r)
        for move in revMoves:
            cardIndex = move.comingFromIdx(deckLen, cardIndex)
        #print(cardIndex)
        if cardIndex < 10000:
            raise Exception("after %d backwards shuffles: %d -> %d" % (r, before, cardIndex))
        #delta = cardIndex - before
        #s += delta
        #print("%d -> %d" % (r, cardIndex))
        #if cardIndex == firstAfter:
        #    raise Exception("Back to %d after %d repetitions" % (firstAfter, r))
        #if firstAfter is None:
        #    firstAfter = cardIndex

        # r -> 0 1 2 3 4 5 6 7 8 9
        # s ->
        # vartannat s är 0, 1, 2, 3, 4, 5, 6

        r += 1

    return 0

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    part2()