
def manhattan(a, b):
    """
    >>> manhattan((0, 0), (5, 5))
    10
    >>> manhattan((1, 1), (-5, -5))
    12
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def readWires():
    with open("input") as f:
        return f.readlines()

def delta(direction):
    if direction == "R": return (1, 0)
    if direction == "L": return (-1, 0)
    if direction == "U": return (0, 1)
    if direction == "D": return (0, -1)
    raise Exception("Unknown direction: %s" % (direction,))

def dictCoordsFor(wire):
    parts = wire.split(",")
    (x, y) = (0, 0)
    result = {}
    stepsTaken = 0
    for part in parts:
        direction = part[0]
        steps = int(part[1:])
        d = delta(direction)
        for _ in range(0, steps):
            x += d[0]
            y += d[1]
            stepsTaken += 1
            result[(x, y)] = stepsTaken
    return result

def coordsFor(wire):
    return set(dictCoordsFor(wire).keys())

def findIntersect(wires):
    """
    >>> findIntersect(["R8,U5,L5,D3", "U7,R6,D4,L4"])
    6
    >>> findIntersect(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
    159
    >>> findIntersect(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])
    135
    """
    allSets = list(map(lambda w: coordsFor(w), wires))
    baseSet = allSets[0]
    for s in allSets[1:]:
        baseSet.intersection_update(s)
    central = (0, 0)
    distances = list(map(lambda c: manhattan(central, c), baseSet))
    return min(distances)

def sumSteps(allDicts, c):
    return sum(map(lambda d: d[c], allDicts))

def findSteps(wires):
    """
    >>> findSteps(["R8,U5,L5,D3", "U7,R6,D4,L4"])
    30
    >>> findSteps(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
    610
    >>> findSteps(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])
    410
    """
    allDicts = list(map(lambda w: dictCoordsFor(w), wires))
    baseDict = allDicts[0]
    for i in range(1, len(allDicts)):
        otherDict = allDicts[i]
        for k in list(baseDict.keys()):
            if not k in otherDict:
                del baseDict[k]
    
    keys = list(baseDict.keys())
    sums = list(map(lambda c: sumSteps(allDicts, c), keys))
    return min(sums)

def part1():
    """
    >>> part1()
    375
    """
    wires = readWires()
    return findIntersect(wires)

def part2():
    """
    >>> part2()
    14746
    """
    wires = readWires()
    return findSteps(wires)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
