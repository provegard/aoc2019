from dataclasses import dataclass
import re

@dataclass
class Deal:
    def apply(self, deck): return deck[::-1]

    def calcAB(self, deckLen, a, b):
        return (-a, -b - 1)

    def desc(self, deckLen, input):
        return "%d-(%s)-1" % (deckLen, input,)

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

    def calcAB(self, deckLen, a, b):
        n = self.n
        if n < 0:
            n = deckLen + n
        return (a, b - n)

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

    def calcAB(self, deckLen, a, b):
        n = self.n
        return (a * n, b * n)

    def moveCard(self, deckLen, cardIndex):
        n = self.n
        #return (cardIndex * n) % deckLen
        return cardIndex * n

    def desc(self, deckLen, input):
        n = self.n
        return "(%s)*%d" % (input, n,)

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
    moves = readInput()
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

def reverse(lst): return lst[::-1]

def executeMoves(deckLen, moves, idx):
    for move in moves:
        idx = move.moveCard(deckLen, idx) % deckLen
    return idx

def findCycle(deckLen, moves, oneRep):
    idx0 = 0
    idx1 = 1
    idx2 = 2
    rep = 0
    if oneRep is None:
        oneRep = lambda i:executeMoves(deckLen, moves, i)
    while rep < 200000000:
        idx0 = oneRep(idx0)
        idx1 = oneRep(idx1)
        idx2 = oneRep(idx2)
        rep += 1
        if idx1 == idx0 + 1 and idx2 == idx1 + 1:
            return rep
        if rep % 10000 == 0:
            print(rep)
    raise Exception("Didn't find a cycle")


def part2x():
    moves = readInput()
    # deckLen = 983     # 982    (n-1)      # 982: 2 x 491
    # deckLen = 991     # 990    (n-1)
    # deckLen = 997     # 996    (n-1)
    # deckLen = 1009    # 336    (n-1)/3    # 1008: 2 x 2 x 2 x 2 x 3 x 3 x 7
    # deckLen = 1013    # 253    (n-1)/4    # 1012: 2 x 2 x 11 x 23
    # deckLen = 1019    # 509    (n-1)/2    # 1018: 2 x 509
    # deckLen = 1021    # 68     (n-1)/15   # 1020: 2 x 2 x 3 x 5 x 17
    # deckLen = 1039    # 346    (n-1)/3    # 1038: 2 x 3 x 173
    # deckLen = 1049    # 1048   (n-1)   
    # deckLen = 1997    # 499    (n-1)/4
    # deckLen = 1999    # 999    (n-1)/2
    # deckLen = 2927    # 1463   (n-1)/2
    # deckLen = 10007   # 5003   (n-1)/2
    # deckLen = 13997   # 6998   (n-1)/2     
    # deckLen = 19997   # 19996  (n-1)
    # deckLen = 30011   # 15005  (n-1)/2
    # deckLen = 97777   # 97776  (n-1)
    # deckLen = 97787   # 97786  (n-1)
    # deckLen = 100019  # 100018 (n-1)
    # deckLen = 1299827 # 649913 (n-1)/2

    p = -2370828689882754717559498128567964034494557509910528000000
    q = 39498975727710714403582787330038714109202045914535069409110464016
    nextIdx = lambda i:(p*i+q) % deckLen
    deckLen     = 119315717514047 # prime factors of 119315717514046: 2 × 59657858757023
    repetitions = 101741582076661
    print(findCycle(deckLen, moves, nextIdx))

    idx = 0
    #for move in moves:
    #    idx = move.moveCard(deckLen, idx) % deckLen
    #print(deckLen / repetitions)

    # rep = 0
    # start = 0
    # i = start
    # while True:
    #     for move in moves:
    #         i = move.moveCard(deckLen, i) % deckLen
    #     rep += 1
    #     if i == start:
    #         raise Exception("back to i==%d after %d reps" % (start, rep,))
    #     if rep % 100 == 0:
    #         print(rep)

    # 1. Create the shuffle expression
    # deckLen = 1021
    # expr = "I"
    # for move in moves:
    #    expr = move.desc(deckLen, expr)
    # print(expr)

    # 2. Simplify via # https://www.dcode.fr/math-simplification:
    # -39216*(60455647946826670684401727064666565547086839808000000*i-1007215823330036576998745086955291567452112553920212908229051)
    # a*(b*i+c) => a*b*i + a*c, set p=a*b and q=a*c:
    
    #print(findCycle(deckLen, moves, nextIdx))

        
    # ---> 649913 reps
    # 101741582076661 % 649913 = 19029

    # 927987 är för lågt!!
    # 98130591375625 är fel (ger 2020 efter rep 19028)

    # 11084257945798 då? (ger 2020 efter rep 19029)
    # 11084257945798 OCKSÅ FEL!!

    # 56052654109315 är fel, ett steg bakåt från 2020

    # idx = 2020
    # revMoves = reverse(moves)
    # for _ in range(0, 1):
    #     nxt = idx
    #     for move in revMoves:
    #         idx = move.comingFromIdx(deckLen, idx)
    #     calcNxt = nextIdx(idx)
    #     assert(nxt == calcNxt)
    # print(idx)


    start = 11084257945798
    idx = start
    rep = 0
    # while True:
    #     idx = nextIdx(idx)
    #     rep += 1
    #     if idx == start:
    #         raise Exception("back to idx==%d after %d reps" % (start, rep,))
    #     if rep % 10000 == 0:
    #         print(rep)
    # while rep < 19100:
    #     idx = nextIdx(idx)
    #     rep += 1
    #     if rep >= 19000:
    #         print("rep %d -> %d" % (rep, idx))
    # print(idx)
    # idx = 2020
    # lastDiff = 0
    # for x in range(0, 5):
    #     #print(idx)
    #     ni = nextIdx(idx)
    #     diff = ni - idx
    #     print("==")
    #     print(diff // p) # 0
    #     lastDiff = diff
    #     idx = ni


    #fwd = lambda n, i:((p**n)*i + q*((p**n)-1)) % deckLen

    #print(fwd(repetitions, 2020))

def part2():
    import functools

    deckLen     = 119315717514047
    repetitions = 101741582076661

    p = -2370828689882754717559498128567964034494557509910528000000 % deckLen
    q = 39498975727710714403582787330038714109202045914535069409110464016 % deckLen
    
    shuffle1 = (p, q)
    
    def newShuffle(s1, s2):
        a, b = s1
        c, d = s2
        return (a * c % deckLen, (b * c + d) % deckLen)

    def doShuffle(s, idx):
        a, b = s
        return (idx * a + b) % deckLen

    def findShuffle(maxRep):
        n = 1
        s = shuffle1
        while n * 2 < maxRep:
            s = newShuffle(s, s)
            n *= 2
        return (s, n)
    
    maxRep = repetitions
    shuffles = []
    while maxRep > 0:
        s, n = findShuffle(maxRep)
        shuffles.append(s)
        maxRep -= n

    finalShuffle = functools.reduce(newShuffle, shuffles)
    a, b = finalShuffle
    #print(finalShuffle)

    # reverse: i = (q*deckLen + x - b) / a
    # - x = 2020
    # - q = ????

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

    # (q * deckLen + x - b) = 0 (mod a)
    # q * deckLen = (b-x) mod a ??

    #print(q) # 3396925699541
    def revIdx(x):
        q = linear_congruence(deckLen, b-x, a)
        return ((q*deckLen + x - b) / a) % deckLen

    print(revIdx(2020)) # 10307144922975
    print(doShuffle(finalShuffle, 10307144922975))
    # -> 10307144922975

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    part2()