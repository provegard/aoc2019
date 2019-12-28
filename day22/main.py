from dataclasses import dataclass
import re

@dataclass
class Deal:
    def apply(self, deck): return deck[::-1]

    def desc(self, deckLen, input):
        return "%d-(%s)-1" % (deckLen, input,)

    def moveCard(self, deckLen, cardIndex):
        return deckLen - cardIndex - 1

@dataclass
class Cut:
    n: int
    def apply(self, deck):
        n = self.n
        a = deck[:n]
        b = deck[n:]
        return b + a

    def desc(self, deckLen, inp):
        n = self.n
        if n < 0:
            n = deckLen + n
        return "(%s)-%d" % (inp, n)

    def moveCard(self, deckLen, cardIndex):
        n = self.n
        if n < 0:
            n = deckLen + n
        #if cardIndex < n:
        #    # moves back
        #    return cardIndex + deckLen - n
        # moves in front
        return cardIndex - n

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
        #return (cardIndex * n) % deckLen
        return cardIndex * n

    def desc(self, deckLen, input):
        n = self.n
        return "(%s)*%d" % (input, n,)

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

def testMoveCard(move, deckLen, idx):
    """
    >>> testMoveCard(DealIncrement(52), 10119315717514047, 2335226704041742)
    2020
    """
    return move.moveCard(deckLen, idx) % deckLen

def readInput():
    with open("input") as f:
        lines = f.readlines()
        return list(map(lambda l:parse(l.strip()), lines))

def part1():
    """
    >>> part1()
    1510
    """
    #moves = readInput()
    cardIndex = 2019
    deckLen = 10007

    # 24*(484073215445737332847972805145995073566485967947327460534999−98784528745114779898312422023665168103939896246272000000*i)
    calc = lambda i:24*(484073215445737332847972805145995073566485967947327460534999-98784528745114779898312422023665168103939896246272000000*i)

    result = calc(cardIndex) % deckLen
    return result

    # for move in moves:
    #     cardIndex = move.moveCard(deckLen, cardIndex)
    # return cardIndex % deckLen

    #expr = "I"
    #for move in moves:
    #    expr = move.desc(deckLen, expr)
    #print(expr)

# from the Internet
def linear_congruence(a, b, m):
    if b == 0:
        return 0

    if a < 0:
        a = -a
        b = -b

    b %= m
    while a > m:
        a -= m

    return (m * linear_congruence(m, -b, a) + b) // a

def part2():
    import math
    import functools

    deckLen     = 119315717514047
    repetitions = 101741582076661

    # 1. Create the shuffle expression
    # expr = "I"
    # for move in moves:
    #    expr = move.desc(deckLen, expr)
    # print(expr)

    # 2. Simplify via # https://www.dcode.fr/math-simplification:
    # to get p and q in p*i+q:
    p = -2370828689882754717559498128567964034494557509910528000000 % deckLen
    q = 39498975727710714403582787330038714109202045914535069409110464016 % deckLen
    
    # one complete shuffle
    shuffle1 = (p, q)
    
    # combine two shuffles
    def newShuffle(s1, s2):
        a, b = s1
        c, d = s2
        return (a * c % deckLen, (b * c + d) % deckLen)

    # apply a shuffle
    def doShuffle(s, idx):
        a, b = s
        return (idx * a + b) % deckLen

    # combine shuffles so that we do 2^n individual shuffles, return the shuffle + n
    def findShuffle(maxRep):
        n = 1
        s = shuffle1
        while n * 2 < maxRep:
            s = newShuffle(s, s)
            n *= 2
        return (s, n)

    # create a list of shuffles so that we reach 'repetitions' shuffles in total
    maxRep = repetitions
    shuffles = []
    while maxRep > 0:
        s, n = findShuffle(maxRep)
        shuffles.append(s)
        maxRep -= n

    # simplify into a single big shuffle
    finalShuffle = functools.reduce(newShuffle, shuffles)
    a, b = finalShuffle
    #print(finalShuffle)

    # The reverse of the final shuffle, where 'q' is some integer so that dividing by 'a'
    # yields a whole number:
    # reverse: i = (q*deckLen + x - b) / a
    # - x = 2020
    # - q = ????

    # (q * deckLen + x - b) = 0 (mod a)
    # q * deckLen = (b-x) mod a
    def revIdx(x):
        q = linear_congruence(deckLen, b-x, a)
        return math.floor(((q*deckLen + x - b) / a) % deckLen)

    answer = revIdx(2020)
    print("answer  = %d" % (answer,)) # 10307144922975
    control = doShuffle(finalShuffle, answer)
    print("control = %d" % (control,))
    # -> 10307144922975

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    part2()