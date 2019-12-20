
import astar
#import immutables

WALL = 1
PASSAGE = 2
LABEL = 3
BLANK = 4

def readLines(fn):
    with open(fn) as f:
        return f.readlines()
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
    #return immutables.Map(m)
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
    #labeledPositions = {}
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
            # if not (label is None):
            #     if label in labeledPositions:
            #         labeledPositions[label] = labeledPositions[label] + [newPos]
            #     else:
            #         labeledPositions[label] = [newPos]
        elif cell == "#": newMap[newPos] = WALL
    return (newMap, positionLabel)

def findPositionByLabel(pl, label, skip = None):
    for pos, l in pl.items():
        if l == label and pos != skip: return pos
    return None
    #raise Exception("Found no pos for %s in %s with skip='%s'" % (label, pl, skip))

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
        m0 = linesToMap(lines)
        #print(m0)
        m1, pl = processMap(m0)
        #print(m1)
        #print(pl)
        self.pl = pl
        self.neighborLookup = buildNeighbors(m1, pl)
        #print(pl)
        #print(self.neighborLookup)
        self.theMap = m1

    def neighbors(self, pos):
        #ns = [pos neighboring(pos)
        #return [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if canMove(self.a_map, (nx, ny), self.goal_value)]
        #return [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if self.canMove((nx, ny))]
        return self.neighborLookup[pos]

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        return 1
        #return manhattan(current, goal)

    def run(self):
        #if True: return
        start = findPositionByLabel(self.pl, "AA")
        goal = findPositionByLabel(self.pl, "ZZ")
        result = self.astar(start, goal)
        if result is None:
            return None
        path = list(result)
        #print(path)
        return len(path) - 1 # don't count the start

# 4250 är fel för input
def example(fn):
    """
    >>> example("ex1")
    23
    >>> example("ex2")
    58
    >>> example("input")
    548
    """
    lines = readLines(fn)
    return Solver(lines).run()

if __name__ == "__main__":
    import doctest
    doctest.testmod()