import math

def readRows(name):
    with open(name) as f:
        return f.readlines()

def parseMap(rows):
    """
    >>> parseMap([".#..#"])
    [(1, 0), (4, 0)]
    >>> parseMap([".#..#", "#..#."])
    [(1, 0), (4, 0), (0, 1), (3, 1)]
    """
    ys = range(0, len(rows))
    xs = range(0, len(rows[0]))
    result = []
    for (row, y) in zip(rows, ys):
        for (pos, x) in zip(row, xs):
            if pos == "#":
                result.append((x, y))

    return result

def roundToSane(x):
    x = round(x, 6) # avoid things like 1.0000000000000002
    if x.is_integer():
        return int(x)
    return x

def hasLineOfSightNew(asteroidsSet, posFrom, posTo):
    (x0, y0) = posFrom
    (x1, y1) = posTo
    if x0 == x1:
        # vertical line
        step = 1 if y1 >= y0 else -1
        for y in range(y0+step, y1, step): # will exclude y1, which is fine
            pos = (x0, y)
            if pos in asteroidsSet:
                return False
    else:
        b = (y1 - y0) / (x1 - x0)
        a = -(b * x1) + y1
        calc_y = lambda x: roundToSane(a + b * x)
        step = 1 if x1 >= x0 else -1
        for x in range(x0+step, x1, step): # will exclude x1, which is fine
            y = calc_y(x)
            pos = (x, y)
            if pos in asteroidsSet:
                return False
    return True

    # y − y1 = m(x − x1)
    # y = m(x - x1) + y1
    # y = mx - mx1 + y1

def hasLineOfSight(asteroidsSet, posFrom, posTo):
    """
    >>> hasLineOfSight(set([(4, 0), (0, 2)]), (4, 0), (0, 2))
    True
    >>> hasLineOfSight(set([(0, 0), (1, 1), (2, 2)]), (0, 0), (2, 2))
    False
    >>> hasLineOfSight(set([(4, 0), (18, 2), (11, 1)]), (4, 0), (18, 2))
    False
    """
    return hasLineOfSightNew(asteroidsSet, posFrom, posTo)

def countLOS(losMap, a):
    if not (a in losMap):
        raise Exception("Unknown asteroid: %s" % (a, ))
    return len(losMap[a])

def insertInLOSMap(losMap, a, b):
    lst = None
    if a in losMap:
        lst = losMap[a]
    else:
        lst = []
        losMap[a] = lst
    lst.append(b)

# Build a Map with
#     asteroid -> [asteroids]
# so that for a given asteroid, it points to a list of asteroids it "sees"
def buildLOSMap(asteroids):
    result = {}
    asteroidsSet = set(asteroids)
    for idx, a in enumerate(asteroids):
        for b in asteroids[idx+1:]:
            hasLos = hasLineOfSight(asteroidsSet, a, b)
            if hasLos:
                insertInLOSMap(result, a, b)
                insertInLOSMap(result, b, a)
    return result

def buildLOSMapForOne(asteroids, a):
    result = {}
    asteroidsSet = set(asteroids)
    for b in asteroids:
        if a == b:
            continue
        hasLos = hasLineOfSight(asteroidsSet, a, b)
        if hasLos:
            insertInLOSMap(result, a, b)
            insertInLOSMap(result, b, a)
    return result

def bestPosition(rows):
    """
    >>> bestPosition([".#..#", ".....", "#####", "....#", "...##"])
    ((3, 4), 8)
    """
    asteroids = parseMap(rows)
    losMap = buildLOSMap(asteroids)
    scoreByPos = {}
    for a in asteroids:
        scoreByPos[a] = countLOS(losMap, a)
    pos = max(scoreByPos.keys(), key=lambda k:scoreByPos[k])
    return (pos, scoreByPos[pos])

def angleDegrees(a, b):
    """
    >>> angleDegrees((0, 0), (0, 10))
    270.0
    >>> angleDegrees((0, 0), (10, 0))
    0.0
    >>> angleDegrees((0, 0), (-10, 0))
    180.0
    >>> angleDegrees((0, 0), (0, -10))
    90.0
    >>> angleDegrees((0, 0), (-5, -5))
    135.0
    """
    (x0, y0) = a
    (x1, y1) = b
    dx = x1 - x0
    dy = y0 - y1 # because y grows down
    rad = math.atan2(dy, dx)
    deg = rad * 180 / math.pi
    if deg < 0:
        deg += 360
    return deg

# Make clockwise, and 0 is up
def angleDegreesCW(a, b):
    """
    >>> angleDegreesCW((0, 0), (0, 10))
    180.0
    >>> angleDegreesCW((0, 0), (10, 0))
    90.0
    >>> angleDegreesCW((0, 0), (-10, 0))
    270.0
    >>> angleDegreesCW((0, 0), (0, -10))
    0.0
    >>> angleDegreesCW((0, 0), (-5, -5))
    315.0
    """
    deg = angleDegrees(a, b)
    return (450 - deg) % 360


def vaporizeOneRound(asteroidsSet, losMap, pos):
    visible = losMap[pos]
    inOrder = sorted(visible, key=lambda v:angleDegreesCW(pos, v))
    for v in inOrder:
        asteroidsSet.remove(v)
    return inOrder

def vaporize(rows, pos):
    asteroidsSet = set(parseMap(rows))
    while True:
        losMap = buildLOSMapForOne(list(asteroidsSet), pos)
        zapped = vaporizeOneRound(asteroidsSet, losMap, pos)
        for z in zapped:
            yield z

def part1():
    """
    >>> part1()
    ((30, 34), 344)
    """
    rows = readRows("input")
    return bestPosition(rows)

def part2():
    """
    >>> part2()
    2732
    """
    rows = readRows("input")
    gen = vaporize(rows, (30, 34))
    for i, pos in enumerate(gen):
        if i == 199:
            (x, y) = pos
            return x * 100 + y
        elif i > 199:
            raise Exception("went too far")

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
