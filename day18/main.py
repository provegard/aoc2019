
import astar

def readLines(fn):
    with open(fn) as f:
        return f.readlines()
def manhattan(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
def splitStr(word): return [char for char in word]
def buildMap(lines):
    m = {}
    for y, line in enumerate(lines):
        for x, cell in enumerate(splitStr(line)):
            m[(x, y)] = cell
    return m

# class Node:
#     def __init__(self, x, y, value):

def isKey(the_map, pos): return ord(the_map[pos]) >= 97

def canMove(the_map, pos):
    if not (pos in the_map):
        return False
    v = the_map[pos]
    if v == "#": return False
    if v == ".": return True
    #if v == "@": return True # needed?
    return isKey(the_map, pos)

def findPos(the_map, sought):
    poss = [k for k in the_map.keys() if the_map[k] == sought]
    if len(poss) == 0:
        return None
    return poss[0]

def findKeyPositions(the_map):
    return [k for k in the_map.keys() if isKey(the_map, k)]

def clear(the_map, pos):
    the_map[pos] = "."

def removeKey(the_map, pos):
    value = the_map[pos]
    door = chr(ord(value) - 32)
    door_pos = findPos(the_map, door)
    clear(the_map, pos)
    if not (door_pos is None):
        clear(the_map, door_pos)

def pathLen(candidate):
    _, p = candidate
    if p is None: return 1e6

class Solver(astar.AStar):

    def __init__(self, lines):
        self.width = len(lines[0])
        self.height = len(lines)
        self.the_map = buildMap(lines)

    def neighbors(self, node):
        x, y = node
        return [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if canMove(self.the_map, (nx, ny))]

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        return manhattan(current, goal)

    def run(self):
        currentPos = findPos(self.the_map, "@")
        clear(self.the_map, currentPos)
        keyPoss = findKeyPositions(self.the_map)
        paths_taken = []
        while len(keyPoss) > 0:
            candidates = [(kp, self.astar(currentPos, kp)) for kp in keyPoss]
            candidates = [(c[0], list(c[1])) for c in candidates if not (c[1] is None)]
            if len(candidates) == 0:
                raise Exception("nowhere to go :(")
            keyPos, bestPath = min(candidates, key=lambda c:len(c[1]))

            print("%s -- took %s" % (bestPath, self.the_map[keyPos]))
            removeKey(self.the_map, keyPos)

            paths_taken.append(bestPath[1:]) # skip start step
            currentPos = bestPath[-1]
            keyPoss = findKeyPositions(self.the_map) # TODO: behöver inte göra om denna om vi muterar keyPoss

        return sum([len(p) for p in paths_taken])

# 4250 är fel för input
def example(fn):
    # """
    # >>> example("ex1")
    # 8
    """
    >>> example("ex2")
    86
    """
    # >>> example("ex3")
    # 132
    # >>> example("ex4")
    # 136
    # >>> example("ex5")
    # 81
    # """
    lines = readLines(fn)
    return Solver(lines).run()

if __name__ == "__main__":
    import doctest
    doctest.testmod()