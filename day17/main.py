import intcode
import itertools

def flatten(lists): return list(itertools.chain(*lists))

def splitStr(word): return [char for char in word]  

def draw(output):
    chars = list(map(chr, output))
    print("".join(chars))

def valueAt(coords, pos):
    if not (pos in coords):
        return " "
    return coords[pos]

def isIntersection(coords, pos):
    (x, y) = pos
    return valueAt(coords, pos) == 35 and \
        valueAt(coords, (x-1, y)) == 35 and \
        valueAt(coords, (x+1, y)) == 35 and \
        valueAt(coords, (x, y-1)) == 35 and \
        valueAt(coords, (x, y+1)) == 35

def toCoords(output):
    y = 0
    x = 0
    coords = {}
    for charCode in output:
        coords[(x, y)] = charCode
        if charCode == 10:
            y += 1
            x = -1
        x += 1
    return coords

def part1():
    program = intcode.readProgram("input")
    output = []
    intcode.run(program, [], output)
    coords = toCoords(output)
    intersectionPoints = filter(lambda p:isIntersection(coords, p), coords.keys())

    #width = output.index(10)
    #for p in intersectionPoints:
    #    (x, y) = p
    #    idx = (width+1)*y + x
    #    output[idx] = ord("O")
    #draw(output)

    return sum(map(lambda p: p[0]*p[1], intersectionPoints))
    #draw(output)

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

faces = list(map(ord, ["^", ">", "v", "<"]))
moveDeltas = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def turnRight(face): return faces[(faces.index(face) + 1) % len(faces)]
def turnLeft(face): return faces[(faces.index(face) - 1) % len(faces)]

def canMoveTo(coords, pos): return pos in coords and coords[pos] == 35
def moveDeltaForFace(face): return moveDeltas[faces.index(face)]
def movementDeltaForward(face): return moveDeltaForFace(face)
def movementDeltaRight(face): return moveDeltaForFace(turnRight(face))
def movementDeltaLeft(face): return moveDeltaForFace(turnLeft(face))

def add(pos, delta):
    (x, y) = pos
    (dx, dy) = delta
    return (x + dx, y + dy)

def movement(coords, pos, face):
    delta = movementDeltaForward(face)
    newPos = add(pos, delta)
    if canMoveTo(coords, newPos):
        # can move forward
        nxt = movement(coords, newPos, face)
        if len(nxt) > 0 and isInt(nxt[0]):
            return [1 + nxt[0]] + nxt[1:]
        return [1] + nxt
    else:
        # need to turn
        rightDelta = movementDeltaRight(face)
        rightPos = add(pos, rightDelta)
        if canMoveTo(coords, rightPos):
            nxt = movement(coords, pos, turnRight(face))
            return ["R"] + nxt
        leftDelta = movementDeltaLeft(face)
        leftPos = add(pos, leftDelta)
        if canMoveTo(coords, leftPos):
            nxt = movement(coords, pos, turnLeft(face))
            return ["L"] + nxt
    # Done!
    return []

def findVacuumRobot(coords):
    poss = list(filter(lambda k:coords[k] in faces, coords.keys()))
    return poss[0]

def movementPairs(mm): return list(map(lambda i: "%s%s" % (mm[i], mm[i+1]), range(0, len(mm), 2)))

def find_sub_list(sl,l):
    if len(sl) == 0:
        return []
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll-1))

    return results

def overlaps(r1, r2):
    """
    >>> overlaps((0, 1), (1, 2))
    True
    >>> overlaps((0, 1), (2, 3))
    False
    >>> overlaps((2, 3), (0, 4))
    True
    """
    (r1s, r1e) = r1
    (r2s, _) = r2
    if r1s == r2s: return True
    if r2s < r1s: return overlaps(r2, r1)
    # r1s < r2s
    return r1e >= r2s

def overlap(ranges1, ranges2):
    for r1 in ranges1:
        for r2 in ranges2:
            if overlaps(r1, r2):
                return True
    return False

def addDicts(d1, d2): return dict(d1, **d2)

def nextFree(ranges, start, end):
    n = start
    for r in sorted(ranges, key=lambda r:r[0]):
        if n < r[0]:
            return n
        n = r[1] + 1
    return n

def split(items, subListPredicate, start = 0, ranges = [], name = "A", mappings = {}):
    """
    >>> split([1, 2, 3, 1, 2, 3], lambda x:len(x)<=3)
    (['A', 'A'], {'A': [1, 2, 3]})
    >>> split([1, 2, 3, 4, 4, 1, 2, 3], lambda x:len(x)<=3)
    (['A', 'B', 'A'], {'A': [1, 2, 3], 'B': [4, 4]})
    >>> split([1, 2, 3, 5, 1, 2, 3, 5], lambda x:len(x)<=3)
    """
    #print("ranges: %s" % (ranges,))
    start = nextFree(ranges, start, len(items))

    if start >= len(items):
        # done!!
        names = []
        for r in sorted(ranges, key=lambda r:r[0]):
            sl = items[r[0]:r[1]+1]
            theNames = [k for k in mappings.keys() if mappings[k] == sl]
            names.append(theNames[0])

        test = []
        for n in names:
            test = test + mappings[n]
        if test != items:
            raise Exception("%s != %s" % (test, items))

        return (names, mappings)

    #print("start: %d" % (start,))
    for l in range(len(items), 0, -1):
        sl = items[start:start+l]
        if not subListPredicate(sl):
            continue
        sll = find_sub_list(sl, items)
        #sll = list(filter(lambda x:x[0] >= start, sll))
        #print("found: %s" % (sll,))
        if len(sll) > 0 and not overlap(ranges, sll):
            #print(sll)
            nextName = chr(ord(name) + 1)
            newMappings = addDicts(mappings, {name: sl})
            ret = split(items, subListPredicate, 0, ranges + sll, nextName, newMappings)
            if ret != False:
                return ret
    
    # found nothing :(
    return False

def part2():
    program = intcode.readProgram("input")
    pcopy = program.copy()

    output = []
    intcode.run(program, [], output)
    draw(output)
    coords = toCoords(output)
    pos = findVacuumRobot(coords)
    mm = movement(coords, pos, coords[pos])
    mm = list(map(str, mm))
    # print(mm)
    pred = lambda sl: len(",".join(sl)) <= 20
    (names, mappings) = split(mm, pred, 0, [])

    # print(names)
    # print(mappings)

    program = pcopy
    program[0] = 2 # activate

    inputs = [",".join(names) + "\n"]
    for k in sorted(mappings.keys(), key=ord):
        inputs.append(",".join(mappings[k]) + "\n")
    inputs.append("n\n")

    def toAscii(inp): return list(map(ord, splitStr(inp)))
    inputs = flatten(list(map(toAscii, inputs)))

    print(inputs)
    output = []
    state = intcode.run(program, inputs, output)
    print("done? %s" % (state[0],))
    print(output)
    #draw(output)

if __name__ == "__main__":
    part2()
    #print(part1())
    #import doctest
    #doctest.testmod()