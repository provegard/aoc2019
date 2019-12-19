import intcode


def scan(program, mx, my):
    for x in range(0, mx):
        for y in range(0, my):
            output = []
            inp = [x, y]
            intcode.run(program.copy(), inp, output)
            yield (x, y, output[0]) 

def part1():
    # """
    # >>> part1()
    # 199
    # """
    program = intcode.readProgram("input")
    return sum(map(lambda t:t[2], scan(program, 50, 50)))

def hasBeamPullAtPos(program, x, y):
    output = []
    intcode.run(program.copy(), [x, y], output)
    return output[0] == 1

def scan2(program, mx, my, startX, startY, minLen):
    y = max(2, startY) # we know from part 1 that there's nothing on row 1, and row 0 is not interesting
    while y < my:
        inBeam = False
        start = -1
        stop = -1
        x = startX
        while x < mx:
            inBeam = hasBeamPullAtPos(program, x, y)
            if inBeam and start < 0:
                # we found the start
                start = x

                # is the beam (minLen) wide?
                newX = x + minLen - 1
                if hasBeamPullAtPos(program, newX, y):
                    # yes, so look for its end
                    x = newX + 1
                    continue
                else:
                    # No good, will yield (start,-1) below
                    break

            if not inBeam and start >= 0:
                stop = x - 1 # inclusive
                break
            x += 1
        yield (y, (start, stop))
        startX = start # beam extends to the right
        y += 1

def overlap(r1, r2):
    """
    >>> overlap((0, 1), (2, 3))
    >>> overlap((0, 2), (1, 2))
    (1, 2)
    >>> overlap((1, 2), (0, 2))
    (1, 2)
    >>> overlap((0, 2), (0, 3))
    (0, 2)
    """
    x1, y1 = r1
    x2, y2 = r2
    if x2 < x1:
        return overlap(r2, r1)
    if x2 > y1:
        return None
    # x1 < x2
    return (max(x1, x2), min(y1, y2))    

def overlap_len(ol): return ol[1] - ol[0] + 1

def part2():

    program = intcode.readProgram("input")
    mx = 10000
    my = 10000
    side = 100
    ranges = scan2(program, mx, my, 0, 0, side)

    def addRange(dest, r):
        if len(dest) == side:
            dest = dest[1:]
        return dest + [r]
    def testRanges(rr):
        if len(rr) < side:
            return None
        y, ol = rr[0]
        for r2 in rr[1:]:
            _, o2 = r2
            ol = overlap(ol, o2)
            if ol is None:
                return None
        if overlap_len(ol) >= side:
            return (ol[0], y)
        return None

    collectedRanges = []
    for yr in ranges:
        collectedRanges = addRange(collectedRanges, yr)
        result = testRanges(collectedRanges)
        if not (result is None):
            x, y = result
            return (10000 * x) + y

def drawp1():
    program = intcode.readProgram("input")
    mx = 100
    my = 70
    d = {}
    for t in scan(program, mx, my):
        x, y, cell = t
        d[(x, y)] = cell
    for y in range(0, my):
        row = ""
        for x in range(0, mx):
            row += "#" if d[(x, y)] == 1 else "."
        print(row)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    # 940067 is too low
    # 10180726 is correct!
    print(part2())