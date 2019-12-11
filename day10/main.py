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


def part1():
    """
    >>> part1()
    344
    """
    rows = readRows("input")
    (_, cnt) = bestPosition(rows)
    return cnt

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
