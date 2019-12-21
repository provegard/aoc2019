
import astar
import immutables

def readLines(fn):
    with open(fn) as f:
        lines = f.readlines()
        return [l.strip() for l in lines]
def splitStr(word): return [char for char in word]

def isKey(the_map, pos): return ord(the_map[pos]) >= 97
def isDoor(the_map, pos):
    o = ord(the_map[pos])
    return 65 <= o < 97

def findKeyPositions(the_map):
    return [k for k in the_map.keys() if isKey(the_map, k)]
def findDoorPositions(the_map):
    return [k for k in the_map.keys() if isDoor(the_map, k)]

def isWall(the_map, pos):
    return pos in the_map and the_map[pos] == "#"
def findNonWallNeighbors(the_map):
    ret = {}
    for pos in the_map.keys():
        x, y = pos
        ns = [n for n in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)] if not isWall(the_map, n)]
        ret[pos] = ns
    return ret

def clear(the_map, pos): return the_map.set(pos, ".")

class Maze:
    def __init__(self, immMap, keyPoss = None, doorPoss = None, nonWallNeighbors = None, passagePositions = None):
        self.map = immMap
        if keyPoss is None:
            keyPoss = findKeyPositions(immMap)
        self.keyPoss = set(keyPoss)
        if doorPoss is None:
            doorPoss = findDoorPositions(immMap)
        self.doorPoss = set(doorPoss)
        if nonWallNeighbors is None:
            nonWallNeighbors = findNonWallNeighbors(immMap)
        self.nonWallNeighbors = nonWallNeighbors
        if passagePositions is None:
            passagePositions = [k for k in immMap.keys() if not isWall(immMap, k)]
        self.passagePositions = passagePositions

    def stateKey(self, curPos):
        tup = (str(curPos), ",".join(map(str, self.keyPoss)), ",".join(map(str, self.doorPoss)))
        return ";".join(tup)

    def isDone(self): return len(self.keyPoss) == 0

    def naiveClear(self, pos):
        nm = clear(self.map, pos)
        return Maze(nm, self.keyPoss, self.doorPoss, self.nonWallNeighbors)

    def findPos(self, sought):
        maze = self.map
        poss = [k for k in maze.keys() if maze[k] == sought]
        if len(poss) == 0:
            return None
        return poss[0]

    def findDoorPos(self, door):
        poss = [p for p in self.doorPoss if self.map[p] == door]
        return poss[0] if len(poss) > 0 else None

    def hasDoorAt(self, pos): return pos in self.doorPoss

    def removeKey(self, pos):
        key = self.map[pos]
        door = chr(ord(key) - 32)
        dp = self.findDoorPos(door)
        nm = clear(self.map, pos)
        newDoorPoss = self.doorPoss
        if not (dp is None):
            nm = clear(nm, dp)
            newDoorPoss = newDoorPoss.difference(set([dp]))
        
        return Maze(nm, self.keyPoss.difference(set([pos])), newDoorPoss, self.nonWallNeighbors, self.passagePositions)

    def neighborsForIgnoringDoors(self, pos): return self.nonWallNeighbors[pos]

    def allPassagePositions(self): return self.passagePositions
    def allKeyPositions(self): return self.keyPoss

def buildMaze(lines):
    m = {}
    for y, line in enumerate(lines):
        for x, cell in enumerate(splitStr(line)):
            m[(x, y)] = cell
    return Maze(immutables.Map(m))

Inf = float("inf")
BigValue = 1e6

def dijkstra(maze, source):
    q = set(maze.allPassagePositions())
    dist = {}
    prev = {}
    dist[source] = 0
    while len(q) > 0:
        u = min(q, key=lambda x:dist.get(x, Inf))
        q.discard(u) # mutable ftw
        for n in maze.neighborsForIgnoringDoors(u):
            alt = dist.get(u, Inf) + 1 # 1 = distance between u and n
            if alt < dist.get(n, Inf):
                dist[n] = alt
                prev[n] = u
    return (dist, prev)


class DijkstraResult:
    def __init__(self, source, dist, prev):
        self.source = source
        self.dist = dist
        self.prev = prev

    def pathTo(self, goal, isDoorFun):
        path = []
        cur = goal
        start = self.source
        prevDict = self.prev
        while cur != start:
            if isDoorFun(cur):
                return None
            path.append(cur)
            cur = prevDict[cur]
            if cur is None:
                return None
        path.append(start)
        path.reverse()
        return path

def reverse(lst): return lst[::-1]

def pathHasDoor(path, isDoorFun): return any(map(isDoorFun, path))

class Solver:

    def __init__(self, lines):
        self.maze = buildMaze(lines)
        self.stateCache = {}

    def run(self):
        m = self.maze

        currentPos = m.findPos("@")
        m = m.naiveClear(currentPos)

        #print("preparing...")
        drs = {}
        sources = [currentPos] + list(m.allKeyPositions())
        paths = {}
        for idx, p in enumerate(sources):
            dist, prev = dijkstra(m, p)
            drs[p] = DijkstraResult(p, dist, prev)

            for j in range(idx + 1, len(sources)):
                other = sources[j]
                path = drs[p].pathTo(other, lambda _:False)
                paths[(p, other)] = path
                paths[(other, p)] = reverse(path)

        #print("starting...")
        return self.runRec3(currentPos, m, paths)

    def runRec3(self, currentPos, maze, paths):
        if maze.isDone():
            return 0

        stateKey = maze.stateKey(currentPos)
        if stateKey in self.stateCache:
            #print("state cache hit")
            return self.stateCache[stateKey]

        def isDoorFun(pos): return maze.hasDoorAt(pos)
        def findPath(a, b):
            p = paths[(a, b)]
            return None if pathHasDoor(p, isDoorFun) else p

        candidates = [(kp, findPath(currentPos, kp)) for kp in maze.allKeyPositions()]
        candidates = [c for c in candidates if not (c[1] is None)]
        candidates = sorted(candidates, key=lambda c:len(c[1]))

        bestSoFarTot = BigValue
        for c in candidates:
            kp, path = c
            nm = maze.removeKey(kp)
            recValue = self.runRec3(kp, nm, paths)

            result = recValue + len(path) - 1 # -1 to exclude start
            if result < bestSoFarTot:
                bestSoFarTot = result

        self.stateCache[stateKey] = bestSoFarTot
        return bestSoFarTot

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
    >>> example("ex5")
    81
    """
    #>>> example("input")
    #3646
    #"""
    lines = readLines(fn)
    return Solver(lines).run()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #print(example("ex3"))
    #import cProfile
    #cProfile.run("example('ex4')")