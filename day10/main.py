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

def dist(p1, p2):
    (x0, y0) = p1
    (x1, y1) = p2
    return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

def eq(a, b):
    return abs(a - b) < 1e-6

def isOnLine(a, b, c):
    """
    >>> isOnLine((1, 0), (4, 3), (3, 2))
    True
    """
    return eq(dist(a, c) + dist(b, c), dist(a, b))

def hasLineOfSight(asteroids, posFrom, posTo):
    """
    >>> hasLineOfSight([(4, 0), (0, 2)], (4, 0), (0, 2))
    True
    >>> hasLineOfSight([(0, 0), (1, 1), (2, 2)], (0, 0), (2, 2))
    False
    """
    for pos in asteroids:
        if pos == posFrom or pos == posTo:
            continue # skip endpoints
        if isOnLine(posFrom, posTo, pos):
            return False
    return True

def countLOS(asteroids, a):
    s = 0
    for other in asteroids:
        if other == a:
            continue
        hasLOS = hasLineOfSight(asteroids, a, other)
        if hasLOS:
            s += 1
    return s

def bestPosition(rows):
    """
    >>> bestPosition([".#..#", ".....", "#####", "....#", "...##"])
    ((3, 4), 8)
    """
    asteroids = parseMap(rows)
    scoreByPos = {}
    for a in asteroids:
        scoreByPos[a] = countLOS(asteroids, a)
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
