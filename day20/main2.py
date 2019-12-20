
import astar

WALL = 1
PASSAGE = 2
LABEL = 3
BLANK = 4

def readLines(fn):
    with open(fn) as f:
        lines = f.readlines()
        return [l.replace("\n", "") for l in lines]
def manhattan(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
def splitStr(word): return [char for char in word]
def neighboring(pos, m):
    x, y = pos
    return [n for n in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if n in m]
def isLabel(x): return ord(x) >= 65

def linesToMap(lines):
    m = {}
    for y, line in enumerate(lines):
        for x, cell in enumerate(splitStr(line)):
            m[(x, y)] = cell
    return m

def findFullLabel(m, pos):
    x, y = pos
    for n in neighboring(pos, m):
        if isLabel(m[n]):
            # make sure it's the right order
            l1 = m[pos]
            l2 = m[n]
            if pos[0] > n[0] or pos[1] > n[1]:
                l1, l2 = l2, l1
            return l1 + l2
    raise Exception("Couldn't get label from pos %s" % (pos,))

def processMap(m):
    newMap = {}
    positionLabel = {}
    for pos, cell in m.items():
        x, y = pos
        newPos = (x - 2, y - 2) # remove "border"
        if cell == ".":
            label = None
            for n in neighboring(pos, m):
                if isLabel(m[n]):
                    label = findFullLabel(m, n)
                    break
            newMap[newPos] = PASSAGE
            if not (label is None):
                positionLabel[newPos] = label
        elif cell == "#": newMap[newPos] = WALL
    return (newMap, positionLabel)

def findPositionByLabel(pl, label, skip = None):
    for pos, l in pl.items():
        if l == label and pos != skip: return pos
    return None

def buildNeighbors(m, pl):
    neighborMap = {}
    for pos, typ in m.items():
        if typ != PASSAGE: continue
        ns = [n for n in neighboring(pos, m) if m[n] == PASSAGE]
        if pos in pl:
            # pos has a label
            label = pl[pos]
            # find the other pos with the same label (ugly!)
            otherPos = findPositionByLabel(pl, label, pos)
            if not (otherPos is None):
                ns = ns + [otherPos]
        neighborMap[pos] = ns
    return neighborMap

class Solver(astar.AStar):

    def __init__(self, lines):
        self.width = len(lines[0]) - 4 # remove margin
        self.height = len(lines) - 4   # remove margin
        m0 = linesToMap(lines)
        m1, pl = processMap(m0)
        self.pl = pl
        self.neighborLookup = buildNeighbors(m1, pl)
        self.theMap = m1

    def hasLabel(self, pos): return pos in self.pl
    def getLabel(self, pos):
        if pos in self.pl:
            return self.pl[pos]
        return None
    def isOuterLabel(self, pos):
        if not self.hasLabel(pos): return False
        x, y = pos
        return x == 0 or x == (self.width - 1) or y == 0 or y == (self.height - 1)

    def neighbors(self, posWithLayer):
        pos, layer = posWithLayer
        ret = []
        myLabel = self.getLabel(pos)
        if myLabel is None:
            # This position is not labeled, but one if its neighbors might be.
            for nPos in self.neighborLookup[pos]:
                nLabel = self.getLabel(nPos)
                if nLabel is None:
                    # Nope, regular neighbor
                    ret.append((nPos, layer)) # same layer
                else:
                    # Labeled neighbor, is it a wall or not?
                    # if layer==0: only AA and ZZ work, other OUTER are walls
                    # but INNER work.
                    isAAOrZZ = nLabel == "AA" or nLabel == "ZZ"
                    isOuter = self.isOuterLabel(nPos)
                    if layer == 0:
                        if isAAOrZZ or not isOuter:
                            ret.append((nPos, layer))
                    else:
                        #  On layer!=0, AA and ZZ are walls.
                        if not isAAOrZZ:
                            ret.append((nPos, layer))
        else:
            # This is a labeled position. One of the neighbors is in a different layer.
            layerDelta = -1 if self.isOuterLabel(pos) else 1
            for nPos in self.neighborLookup[pos]:
                if manhattan(pos, nPos) == 1:
                    # adjacent, same layer
                    ret.append((nPos, layer))
                else:
                    # teleport neighbor
                    ret.append((nPos, layer + layerDelta))
        return ret

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        return 1

    def run(self):
        start = (findPositionByLabel(self.pl, "AA"), 0) # layer 0
        goal = (findPositionByLabel(self.pl, "ZZ"), 0)  # layer 0
        result = self.astar(start, goal)
        if result is None:
            return None
        path = list(result)
        return len(path) - 1 # don't count the start

def example(fn):
    """
    >>> example("ex3")
    396
    >>> example("input")
    6452
    """
    lines = readLines(fn)
    return Solver(lines).run()

if __name__ == "__main__":
    import doctest
    doctest.testmod()