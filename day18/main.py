
import astar
import immutables

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
    #return m
    return immutables.Map(m)

# class Node:
#     def __init__(self, x, y, value):

def isKey(the_map, pos): return ord(the_map[pos]) >= 97
def isDoor(the_map, pos):
    o = ord(the_map[pos])
    return 65 <= o < 97

def canMove(the_map, pos, okValue):
    if not (pos in the_map):
        return False
    v = the_map[pos]
    if v == "#": return False
    if v == ".": return True
    #if v == "@": return True # needed?
    #return v == okValue
    return isKey(the_map, pos)

def findPos(the_map, sought):
    poss = [k for k in the_map.keys() if the_map[k] == sought]
    if len(poss) == 0:
        return None
    return poss[0]

def findKeyPositions(the_map):
    return [k for k in the_map.keys() if isKey(the_map, k)]

def findDoors(the_map):
    return dict([(the_map[k], k) for k in the_map.keys() if isDoor(the_map, k)])

def clear(the_map, pos):
    #r = dict(the_map)
    #r[pos] = "."
    #return r
    return the_map.set(pos, ".")

# def removeKey(the_map, pos):
#     value = the_map[pos]
#     door = chr(ord(value) - 32)
#     door_pos = findPos(the_map, door)
#     nm = clear(the_map, pos)
#     if not (door_pos is None):
#         nm = clear(the_map, door_pos)
#     return nm

# def pathLen(candidate):
#     _, p = candidate
#     if p is None: return 1e6

class Solver(astar.AStar):

    def __init__(self, lines):
        self.the_map = buildMap(lines)
        self.cache = {}
        #self.original_key_positions = findKeyPositions(self.the_map)
        self.doors = findDoors(self.the_map)
        self.astar_cache = {}
        self.st_cache = {}

    #def findKeyPositions(self, m):
    #    return [p for p in self.original_key_positions if isKey(m, p)]

    def findDoorPos(self, d):
        if not (d in self.doors):
            return
        return self.doors[d]

    def doorsRemaining(self, m):
        return [k for k,v in self.doors.items() if m[v] == k] # isDoor(m, v)]
    def doorsRemainingPoss(self, m):
        return [v for k,v in self.doors.items() if m[v] == k] # isDoor(m, v)]

    def removeKey(self, m, pos):
        key = m[pos]
        door = chr(ord(key) - 32)
        dp = self.findDoorPos(door)
        nm = clear(m, pos)
        if not (dp is None):
            nm = clear(nm, dp)
        return nm

    def canMove(self, pos):
        return not (pos in self.occupied)

    def neighbors(self, node):
        x, y = node
        #return [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if canMove(self.a_map, (nx, ny), self.goal_value)]
        return [(nx, ny) for nx, ny in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if self.canMove((nx, ny))]

    def distance_between(self, n1, n2):
        return 1

    def heuristic_cost_estimate(self, current, goal):
        return manhattan(current, goal)

    def myastar(self, m, a, b):

        self.occupied = self.wall_poss.union(self.doors_remaining_poss)
        
        cacheKey = (a, b, ",".join(self.doorsRemaining(m)))
        if cacheKey in self.astar_cache:
            cv = self.astar_cache[cacheKey]
            #print("astar cache hit: %s" % (cv,))
            #print("astar cache hit")
            return cv
        #print("astar cache miss")

        self.goal_value = m[b]
        self.a_map = m
        ret = self.astar(a, b)
        if not (ret is None):
            ret = list(ret)
        self.a_map = None
        self.goal_value = None
        self.astar_cache[cacheKey] = ret
        return ret

    def run(self, currentPos = None, m = None, keyPoss = None):
        m = self.the_map

        currentPos = findPos(m, "@")
        m = clear(m, currentPos)

        keyPoss = findKeyPositions(m)

        self.wall_poss = set([k[0] for k in m.items() if k[1] == "#"])

        return self.runRec(currentPos, m, keyPoss, 0, 1e6, [])

    def runRec(self, currentPos, m, keyPoss, depth, maxPathLen, paths):
        if len(keyPoss) == 0:
            # Done!
            totPathLen = sum(map(lambda p:len(p)-1, paths))
            print("Done, total path len = %d with %d paths" % (totPathLen, len(paths)))
            return 0

        stCacheKey = (currentPos, ",".join(self.doorsRemaining(m)), ",".join(map(str, keyPoss)))
        if stCacheKey in self.st_cache:
            #print("Yes")
            return self.st_cache[stCacheKey]

        self.doors_remaining_poss = self.doorsRemainingPoss(m)

        # Run A-Star to find paths to all key positions
        candidates = [(kp, self.myastar(m, currentPos, kp)) for kp in keyPoss]
        # Filter on reachable key positions
        candidates = [c for c in candidates if not (c[1] is None)]
        # Sort, closest first
        candidates = sorted(candidates, key=lambda c:len(c[1]))

        shortestPathLen = len(candidates[0][1])
        if shortestPathLen > maxPathLen:
            #print("cutoff 2")
            return 1e6 # a big value

        keys = [m[c[0]] for c in candidates]

        #print("%s%s: %s" % (" " * depth, currentPos, keys))

        cacheKey = (currentPos, ",".join(keys))
        if cacheKey in self.cache:
            #print("%scache hit at %s" % (" " * depth, currentPos,))
            return self.cache[cacheKey]

        rec = []
        bestRecValueSoFar = 1e6
        for c in candidates:
            keyPos, p = c
            testMap = self.removeKey(m, keyPos)
            newKeyPoss = [x for x in keyPoss if x != keyPos]

            recValue = self.runRec(keyPos, testMap, newKeyPoss, depth + 1, bestRecValueSoFar, paths + [p])
            if recValue < bestRecValueSoFar:
                bestRecValueSoFar = recValue

            result = recValue + len(p) - 1
            rec.append(result)
            if recValue == 0:
                #print("cutoff 1")
                break # it doesn't get better

        bestValue = min(rec)
        self.cache[cacheKey] = bestValue

        self.st_cache[stCacheKey] = bestValue

        return bestValue

# 4250 är fel för input
def example(fn):
    """
    >>> example("ex1")
    8
    >>> example("ex2")
    86
    >>> example("ex3")
    132
    >>> example("ex4")
    136
    """
    # >>> example("ex5")
    # 81
    # """
    # >>> example("input")
    # 0
    # """
    lines = readLines(fn)
    return Solver(lines).run()

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    print(example("ex3"))
    #import cProfile
    #cProfile.run("example('ex4')")